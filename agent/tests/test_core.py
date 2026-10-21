from __future__ import annotations

import json
import os
import plistlib
from types import SimpleNamespace

import pytest

from xguard.actions import ActionError, execute, restore
from xguard.agent import Agent
from xguard.models import Action, Finding
from xguard.triage import triage


def finding(key="k", sev="medium", actions=()):
    return Finding("test", key, sev, f"title {key}", "detail", {"x": 1}, tuple(actions))


# ---- store ----------------------------------------------------------------
def test_upsert_dedupes_and_reopens(store):
    f = finding()
    a, new = store.upsert(f)
    assert new
    b, new = store.upsert(f)
    assert not new and a.id == b.id
    store.resolve_missing("test", set())
    assert store.get(a.id).status == "resolved"
    c, new = store.upsert(f)
    assert new and c.status == "open"


def test_dismissed_stays_dismissed(store):
    a, _ = store.upsert(finding())
    store.set_status(a.id, "dismissed", "dismissed")
    b, new = store.upsert(finding())
    assert not new and b.status == "dismissed"


def test_bad_severity():
    with pytest.raises(ValueError):
        finding(sev="urgent")


# ---- actions --------------------------------------------------------------
def test_quarantine_and_restore(store, cfg, runner, tmp_path):
    target = tmp_path / "evil.command"
    target.write_text("#!/bin/sh\n")
    os.chmod(target, 0o755)
    act = Action("quarantine", "q", "auto", {"path": str(target)})
    f, _ = store.upsert(finding(actions=[act]))
    msg = execute(store, cfg, runner, f, act)
    assert not target.exists() and "xguard restore" in msg
    stored = cfg.quarantine_dir / str(f.id) / "evil.command"
    assert stored.exists() and (stored.stat().st_mode & 0o777) == 0o600
    assert store.get(f.id).status == "acted"
    restore(store, cfg, runner, store.get(f.id))
    assert target.exists() and (target.stat().st_mode & 0o777) == 0o755
    assert store.get(f.id).status == "open"


def test_disable_launch_agent(store, cfg, runner, tmp_path):
    plist = tmp_path / "com.evil.plist"
    plist.write_bytes(plistlib.dumps({"Label": "com.evil"}))
    act = Action("disable", "d", "auto", {"plist": str(plist), "label": "com.evil"})
    f, _ = store.upsert(finding(actions=[act]))
    execute(store, cfg, runner, f, act)
    assert not plist.exists()
    assert runner.calls[0][:2] == ["launchctl", "bootout"]
    restore(store, cfg, runner, store.get(f.id))
    assert plist.exists() and runner.calls[-1][:2] == ["launchctl", "bootstrap"]


def test_fix_perms_and_restore(store, cfg, runner, tmp_path):
    key = tmp_path / "id"
    key.write_text("k")
    os.chmod(key, 0o644)
    act = Action("fix-perms", "p", "auto", {"path": str(key), "old_mode": 0o644})
    f, _ = store.upsert(finding(actions=[act]))
    execute(store, cfg, runner, f, act)
    assert key.stat().st_mode & 0o777 == 0o600
    restore(store, cfg, runner, store.get(f.id))
    assert key.stat().st_mode & 0o777 == 0o644


def test_manual_action_runs_nothing(store, cfg, runner):
    act = Action("enable-firewall", "fw", "manual", instructions="Do X")
    f, _ = store.upsert(finding(actions=[act]))
    assert "Do X" in execute(store, cfg, runner, f, act)
    assert runner.calls == [] and store.get(f.id).status == "open"


def test_stop_process_refuses_reused_pid(store, cfg, runner):
    runner.on("ps", out="/usr/bin/something-else\n")
    act = Action("stop-process", "s", "auto", {"pid": 99999, "executable": "/tmp/evil"})
    f, _ = store.upsert(finding(actions=[act]))
    with pytest.raises(ActionError, match="refusing"):
        execute(store, cfg, runner, f, act)


def test_cannot_act_twice(store, cfg, runner, tmp_path):
    target = tmp_path / "a.sh"
    target.write_text("x")
    act = Action("quarantine", "q", "auto", {"path": str(target)})
    f, _ = store.upsert(finding(actions=[act]))
    execute(store, cfg, runner, f, act)
    with pytest.raises(ActionError):
        execute(store, cfg, runner, store.get(f.id), act)


# ---- triage ---------------------------------------------------------------
class FakeClient:
    def __init__(self, text=None, stop="end_turn"):
        self.kwargs = None
        block = SimpleNamespace(type="text", text=text)
        self.response = SimpleNamespace(stop_reason=stop, content=[block] if text else [], model="claude-opus-5-5")
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kw):
        self.kwargs = kw
        return self.response


def test_triage_parses_and_validates(store, cfg):
    cfg = cfg.__class__(**{**cfg.__dict__, "triage_enabled": True})
    act = Action("quarantine", "q", "auto")
    f, _ = store.upsert(finding(actions=[act]))
    body = {"summary": "s", "risk": "likely_malicious", "reasoning": "r",
            "recommended_action": "rm -rf /", "what_to_check": ""}
    client = FakeClient(json.dumps(body))
    out = triage(cfg, f, client)
    assert out["recommended_action"] == "none"          # unknown action id is never passed through
    assert out["risk"] == "likely_malicious"
    kw = client.kwargs
    assert kw["model"] == "claude-opus-5-5" and kw["fallbacks"] == "default"
    assert kw["output_config"]["format"]["type"] == "json_schema"
    assert "<finding>" in kw["messages"][0]["content"]
    assert "untrusted" in kw["system"]


def test_triage_refusal(store, cfg):
    cfg = cfg.__class__(**{**cfg.__dict__, "triage_enabled": True})
    f, _ = store.upsert(finding())
    assert triage(cfg, f, FakeClient(None, stop="refusal")) == {"error": "triage declined by the model"}


def test_triage_off(store, cfg):
    f, _ = store.upsert(finding())
    assert triage(cfg, f, FakeClient("{}")) is None


# ---- agent cycle ----------------------------------------------------------
class StaticMonitor:
    def __init__(self, name, findings):
        self.name, self.findings = name, findings

    def scan(self, ctx):
        return list(self.findings)


class BrokenMonitor:
    name = "broken"

    def scan(self, ctx):
        raise RuntimeError("boom")


def test_cycle(store, cfg, runner):
    cfg = cfg.__class__(**{**cfg.__dict__, "notify": True})
    mon = StaticMonitor("test", [finding("a", "high"), finding("b", "low")])
    triaged = []
    agent = Agent(cfg, store, runner, [mon, BrokenMonitor()],
                  triage_fn=lambda c, f: triaged.append(f.id) or {"summary": "ok", "risk": "needs_review"})
    r = agent.cycle()
    assert len(r.new) == 2 and "broken" in r.errors
    assert len(triaged) == 2
    assert any(c[0] == "osascript" for c in runner.calls)      # high finding notified
    mon.findings = [finding("a", "high")]
    r2 = agent.cycle()
    assert r2.new == [] and r2.still_open == 1 and r2.resolved == 1
    assert len(triaged) == 2                                    # not re-triaged
