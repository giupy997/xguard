"""Actions xguard can take on a finding. Every one runs only after explicit approval.

Reversible actions keep a manifest in the quarantine folder so `xguard restore`
can put things back exactly where they were.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
from pathlib import Path

from .config import Config
from .models import Action
from .runner import Runner
from .store import Store, StoredFinding


class ActionError(Exception):
    pass


def _manifest_path(cfg: Config, fid: int) -> Path:
    return cfg.quarantine_dir / str(fid) / "manifest.json"


def _move_to_quarantine(cfg: Config, fid: int, src: Path, extra: dict | None = None) -> Path:
    if not src.exists():
        raise ActionError(f"{src} no longer exists; nothing to move.")
    dest_dir = cfg.quarantine_dir / str(fid)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.move(str(src), str(dest))
    # Strip execute bits so a quarantined script or binary cannot be run by accident.
    if dest.is_file():
        os.chmod(dest, 0o600)
    _manifest_path(cfg, fid).write_text(json.dumps({"original": str(src), "stored": str(dest), **(extra or {})}))
    return dest


def execute(store: Store, cfg: Config, runner: Runner, f: StoredFinding, action: Action) -> str:
    if f.status != "open":
        raise ActionError(f"Finding {f.id} is {f.status}; only open findings can be acted on.")
    if action.kind == "manual":
        store.log(f.id, "manual-shown", {"action": action.id})
        return f"xguard does not run this one for you, because it needs admin rights.\n{action.instructions}"

    p = action.params
    if action.id == "quarantine":
        src = Path(p["path"])
        mode = src.stat().st_mode & 0o777 if src.is_file() else None
        dest = _move_to_quarantine(cfg, f.id, src, {"mode": mode})
        msg = f"Moved {src.name} to {dest.parent}. Run `xguard restore {f.id}` to put it back."
    elif action.id == "disable":
        plist = Path(p["plist"])
        runner.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(plist)])  # fine if it was not loaded
        dest = _move_to_quarantine(cfg, f.id, plist, {"launchctl": "gui"})
        msg = (f"Stopped {p.get('label', plist.stem)} and moved its launch file to {dest.parent}. "
               f"It will not start again. Run `xguard restore {f.id}` to undo.")
    elif action.id == "stop-process":
        pid = int(p["pid"])
        current = runner.run(["ps", "-o", "comm=", "-p", str(pid)]).out.strip()
        if not current:
            raise ActionError(f"Process {pid} is no longer running.")
        if p.get("executable") and current != p["executable"]:
            raise ActionError(f"Process {pid} is now {current}, not {p['executable']}; refusing to stop it.")
        try:
            os.kill(pid, signal.SIGTERM)
        except PermissionError as e:
            raise ActionError(f"Not allowed to stop process {pid}: {e}") from e
        msg = f"Asked process {pid} ({current}) to quit. If it comes back, look for a startup item that restarts it."
    elif action.id == "fix-perms":
        path = Path(p["path"])
        os.chmod(path, 0o600)
        _manifest_path(cfg, f.id).parent.mkdir(parents=True, exist_ok=True)
        _manifest_path(cfg, f.id).write_text(json.dumps({"chmod": str(path), "old_mode": p["old_mode"]}))
        msg = f"{path.name} is now readable only by you."
    else:
        raise ActionError(f"Unknown action {action.id!r}.")

    store.set_status(f.id, "acted", event="action", data={"action": action.id, "result": msg})
    return msg


def restore(store: Store, cfg: Config, runner: Runner, f: StoredFinding) -> str:
    mpath = _manifest_path(cfg, f.id)
    if not mpath.exists():
        raise ActionError(f"Nothing to restore for finding {f.id}.")
    m = json.loads(mpath.read_text())
    if "chmod" in m:
        os.chmod(m["chmod"], m["old_mode"])
        msg = f"Restored the previous permissions of {m['chmod']}."
    else:
        original, stored = Path(m["original"]), Path(m["stored"])
        if original.exists():
            raise ActionError(f"{original} exists again; move it away first, then restore.")
        original.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(stored), str(original))
        if m.get("mode") is not None:
            os.chmod(original, m["mode"])
        if m.get("launchctl") == "gui":
            runner.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(original)])
        msg = f"Put {original.name} back in {original.parent}."
    mpath.unlink()
    store.set_status(f.id, "open", event="restored", data={"result": msg})
    return msg
