"""Programs that start by themselves: LaunchAgents and LaunchDaemons.

This is the most common way Mac malware survives a restart. On the first scan
xguard records what is already there and only reports items that look wrong on
their own (unsigned, missing, hidden, or a shell one-liner). After that, any new
or changed item is reported too, until the user reviews it.
"""

from __future__ import annotations

import hashlib
import os
import plistlib
from pathlib import Path

from ..models import Action, Finding, severity_rank
from .base import Context, signature, suspicious_location

INTERPRETERS = {"sh", "bash", "zsh", "dash", "python", "python3", "perl", "ruby", "osascript", "node", "curl"}


def launch_dirs(home: Path) -> list[tuple[Path, bool]]:
    """(directory, user_owned). User-owned items can be disabled without admin rights."""
    return [
        (home / "Library/LaunchAgents", True),
        (Path("/Library/LaunchAgents"), False),
        (Path("/Library/LaunchDaemons"), False),
    ]


def program_of(plist: dict) -> tuple[str | None, list[str]]:
    args = plist.get("ProgramArguments") or []
    args = [str(a) for a in args] if isinstance(args, list) else []
    prog = plist.get("Program") or (args[0] if args else None)
    return (str(prog) if prog else None), args


class PersistenceMonitor:
    name = "persistence"

    def __init__(self, dirs: list[tuple[Path, bool]] | None = None) -> None:
        self._dirs = dirs

    def scan(self, ctx: Context) -> list[Finding]:
        dirs = self._dirs or launch_dirs(ctx.config.home)
        baseline = ctx.baseline(self.name)
        first_run = baseline is None
        known = set(baseline or [])
        current: set[str] = set()
        findings: list[Finding] = []

        for directory, user_owned in dirs:
            if not directory.is_dir():
                continue
            for path in sorted(directory.glob("*.plist")):
                try:
                    raw = path.read_bytes()
                except OSError:
                    continue
                ident = f"{path}:{hashlib.sha256(raw).hexdigest()[:16]}"
                current.add(ident)
                f = self._inspect(ctx, path, ident, raw, user_owned, is_new=not first_run and ident not in known)
                if f:
                    findings.append(f)

        # New items are not folded into the baseline: they keep being reported until
        # the user dismisses or acts on them (a dismissal sticks to that exact content).
        if first_run:
            ctx.save_baseline(self.name, current)
        return findings

    def _inspect(self, ctx: Context, path: Path, ident: str, raw: bytes, user_owned: bool,
                 is_new: bool) -> Finding | None:
        reasons: list[str] = []
        severity = "info"

        def bump(level: str, why: str) -> None:
            nonlocal severity
            reasons.append(why)
            if severity_rank(level) > severity_rank(severity):
                severity = level

        try:
            plist = plistlib.loads(raw)
        except Exception:
            plist = {}
            bump("medium", "the file is not a valid launch configuration")

        label = str(plist.get("Label", path.stem))
        prog, args = program_of(plist)
        sig_text = None

        if prog:
            base = os.path.basename(prog)
            where = suspicious_location(prog)
            if where:
                bump("high", where)
            if base in INTERPRETERS and any(a in ("-c", "-e") for a in args[1:]):
                bump("high", f"it runs an inline {base} command instead of an installed program")
            elif base in INTERPRETERS:
                bump("medium", f"it runs a {base} script")
            if base not in INTERPRETERS:
                if not Path(prog).exists():
                    bump("medium", "the program it points to does not exist")
                else:
                    sig = signature(ctx.runner, prog)
                    sig_text = sig.describe()
                    if not sig.checked:
                        pass  # root-only file: we cannot judge it, so we do not guess
                    elif not sig.signed:
                        bump("high", "the program is not code-signed")
                    elif not sig.valid:
                        bump("high", "the program's code signature is invalid")
        elif plist:
            bump("medium", "it does not say which program it runs")

        if is_new:
            bump("medium", "it appeared since the last scan")

        if not reasons:
            return None

        evidence = {
            "plist": str(path), "label": label, "program": prog, "arguments": args[:8],
            "signature": sig_text, "run_at_load": bool(plist.get("RunAtLoad")),
            "keep_alive": bool(plist.get("KeepAlive")),
        }
        if user_owned:
            actions = (Action("disable", "Stop it and move it to the xguard quarantine", "auto",
                              params={"plist": str(path), "label": label}),)
        else:
            actions = (Action("disable-admin", "Stop it (needs admin rights)", "manual",
                              instructions=f"In Terminal: sudo launchctl bootout system \"{path}\" && "
                                           f"sudo mv \"{path}\" ~/Desktop/  (moves it out so it cannot restart)"),)
        return Finding(
            self.name, ident, severity,
            f"Startup item {label} needs a look",
            "This runs automatically when you log in or the Mac starts: " + "; ".join(reasons) + ".",
            evidence, actions,
        )
