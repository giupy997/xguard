"""Command line interface. `xguard --help` lists everything."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import shutil
import sys
import time
from pathlib import Path

from . import __version__
from .actions import ActionError, execute, restore
from .agent import Agent, CycleReport
from .config import Config, load_config
from .models import severity_rank
from .runner import SystemRunner
from .store import Store, StoredFinding
from .triage import has_credentials

AGENT_LABEL = "com.xguard.agent"
TTY = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
COLORS = {"critical": "31;1", "high": "31", "medium": "33", "low": "36", "info": "2"}


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if TTY else text


def sev(s: str) -> str:
    return paint(f"{s.upper():<8}", COLORS.get(s, "0"))


def ago(ts: float) -> str:
    d = time.time() - ts
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if d >= size:
            return f"{int(d // size)}{unit} ago"
    return "just now"


def line(f: StoredFinding) -> str:
    hint = ""
    if f.triage and "risk" in f.triage:
        hint = paint(f"  [{f.triage['risk'].replace('_', ' ')}]", "2")
    return f"  {f.id:>4}  {sev(f.severity)} {f.title}{hint}"


def print_report(r: CycleReport, store: Store) -> None:
    if r.new:
        print(f"{len(r.new)} new finding(s):")
        for f in sorted(r.new, key=lambda f: -severity_rank(f.severity)):
            print(line(store.get(f.id) or f))
    else:
        print("Nothing new.")
    extra = []
    if r.still_open:
        extra.append(f"{r.still_open} still open")
    if r.resolved:
        extra.append(f"{r.resolved} resolved since last scan")
    if extra:
        print(", ".join(extra).capitalize() + ".")
    for name, err in r.errors.items():
        print(paint(f"Monitor {name} failed: {err}", "31"))
    if r.new:
        print("Details: xguard show <id>")


def cmd_scan(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    report = Agent(cfg, store).cycle()
    print_report(report, store)
    return 0


def cmd_watch(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    print(f"xguard is watching. A scan runs every {args.interval}s. Ctrl+C to stop.")
    stamp = lambda: time.strftime("%H:%M:%S")

    def on_cycle(r: CycleReport) -> None:
        msg = f"{len(r.new)} new" if r.new else "nothing new"
        print(f"[{stamp()}] scan done in {r.duration:.1f}s, {msg}.", flush=True)
        for f in r.new:
            print(line(store.get(f.id) or f), flush=True)

    try:
        Agent(cfg, store).watch(args.interval, on_cycle=on_cycle)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


def cmd_findings(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    statuses = ("open", "acted", "dismissed", "resolved") if args.all else ("open",)
    items = store.list(statuses)
    if not items:
        print("No open findings." if not args.all else "No findings yet. Run: xguard scan")
        return 0
    items.sort(key=lambda f: (-severity_rank(f.severity), -f.last_seen))
    for f in items:
        status = "" if f.status == "open" else paint(f"  ({f.status})", "2")
        print(line(f) + status)
    return 0


def cmd_show(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    f = store.get(args.id)
    if not f:
        print(f"No finding {args.id}.")
        return 1
    print(f"{sev(f.severity)} {f.title}")
    print(f"Status: {f.status} · monitor: {f.monitor} · first seen {ago(f.first_seen)} · last seen {ago(f.last_seen)}")
    print()
    print(f.detail)
    if f.triage:
        print()
        if "error" in f.triage:
            print(paint(f"Triage: {f.triage['error']}", "2"))
        else:
            print(paint("What xguard thinks", "1"))
            print(f"  {f.triage['summary']}")
            print(f"  Risk: {f.triage['risk'].replace('_', ' ')}. {f.triage['reasoning']}")
            if f.triage.get("what_to_check"):
                print(f"  Check: {f.triage['what_to_check']}")
            if f.triage.get("recommended_action", "none") != "none":
                print(f"  Suggested: {f.triage['recommended_action']}")
    print()
    print(paint("Evidence", "1"))
    for k, v in f.evidence.items():
        if v not in (None, "", [], {}):
            print(f"  {k}: {v if not isinstance(v, (list, dict)) else json.dumps(v)}")
    if f.actions and f.status == "open":
        print()
        print(paint("What you can do", "1"))
        for a in f.actions:
            how = "xguard does it, reversible" if a.kind == "auto" else "you do it, instructions shown"
            if a.id == "stop-process":
                how = "xguard does it, not reversible"
            print(f"  xguard approve {f.id} {a.id:<16} {a.label} ({how})")
        print(f"  xguard dismiss {f.id}{'':<17} It is expected, stop reporting it")
    return 0


def confirm(prompt: str) -> bool:
    try:
        return input(f"{prompt} [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def cmd_approve(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    f = store.get(args.id)
    if not f:
        print(f"No finding {args.id}.")
        return 1
    action = f.action(args.action) if args.action else (f.actions[0] if len(f.actions) == 1 else None)
    if not action:
        print("Choose an action: " + ", ".join(a.id for a in f.actions))
        return 1
    if action.kind == "auto" and not args.yes and not confirm(f"{action.label}: {f.title}?"):
        print("Nothing done.")
        return 1
    try:
        print(execute(store, cfg, SystemRunner(), f, action))
    except (ActionError, OSError) as e:
        print(paint(f"Could not do it: {e}", "31"))
        store.log(f.id, "action-failed", {"action": action.id, "error": str(e)})
        return 1
    return 0


def cmd_dismiss(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    f = store.get(args.id)
    if not f:
        print(f"No finding {args.id}.")
        return 1
    store.set_status(f.id, "dismissed", event="dismissed", data={"reason": args.reason or ""})
    print(f"Dismissed. xguard will not report this again unless it changes.")
    return 0


def cmd_restore(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    f = store.get(args.id)
    if not f:
        print(f"No finding {args.id}.")
        return 1
    try:
        print(restore(store, cfg, SystemRunner(), f))
    except (ActionError, OSError) as e:
        print(paint(f"Could not restore: {e}", "31"))
        return 1
    return 0


def cmd_log(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    for row in store.audit(args.id):
        when = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row["at"]))
        fid = f"#{row['finding_id']}" if row["finding_id"] else "-"
        print(f"{when}  {fid:>5}  {row['event']:<14} {row['data']}")
    return 0


def cmd_status(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    last = store.get_state("last_cycle")
    print(f"xguard {__version__}")
    print(f"Data: {cfg.data_dir}")
    print(f"Last scan: {ago(last['at']) if last else 'never'}")
    open_ = store.list(("open",))
    worst = max((f.severity for f in open_), key=severity_rank, default=None)
    print(f"Open findings: {len(open_)}" + (f" (worst: {worst})" if worst else ""))
    triage_state = "off" if not cfg.triage_enabled else (
        f"on ({cfg.model})" if has_credentials() else "off (no Anthropic credentials found)")
    print(f"Claude triage: {triage_state}")
    print(f"Background agent: {'installed' if agent_plist().exists() else 'not installed'}")
    return 0


def agent_plist() -> Path:
    return Path.home() / "Library/LaunchAgents" / f"{AGENT_LABEL}.plist"


def cmd_install_agent(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    exe = shutil.which("xguard")
    if not exe:
        print("Install xguard on your PATH first (for example: uv tool install ./agent).")
        return 1
    plist = {
        "Label": AGENT_LABEL,
        "ProgramArguments": [exe, "watch", "--interval", str(args.interval)],
        "RunAtLoad": True,
        "KeepAlive": True,
        "ProcessType": "Background",
        "LowPriorityIO": True,
        "Nice": 10,
        "StandardOutPath": str(cfg.data_dir / "agent.log"),
        "StandardErrorPath": str(cfg.data_dir / "agent.log"),
    }
    env = {k: v for k, v in os.environ.items() if k.startswith("XGUARD_")}
    if env:
        plist["EnvironmentVariables"] = env
    path = agent_plist()
    if not args.yes and not confirm(f"Write {path} and start xguard in the background?"):
        print("Nothing done.")
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    cfg.data_dir.mkdir(parents=True, exist_ok=True)
    path.write_bytes(plistlib.dumps(plist))
    SystemRunner().run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(path)])
    print(f"xguard now runs in the background every {args.interval}s. Log: {cfg.data_dir / 'agent.log'}")
    print("Note: Claude triage needs ANTHROPIC_API_KEY in the environment the agent starts with.")
    return 0


def cmd_uninstall_agent(cfg: Config, store: Store, args: argparse.Namespace) -> int:
    path = agent_plist()
    if not path.exists():
        print("The background agent is not installed.")
        return 0
    SystemRunner().run(["launchctl", "bootout", f"gui/{os.getuid()}", str(path)])
    path.unlink()
    print("Background agent removed. Your findings and quarantine are kept in " + str(cfg.data_dir))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="xguard", description="An always-on security agent for your Mac. "
                                "It watches continuously; you decide.")
    p.add_argument("--version", action="version", version=f"xguard {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("scan", help="run every check once").set_defaults(fn=cmd_scan)
    w = sub.add_parser("watch", help="keep scanning in the foreground")
    w.add_argument("--interval", type=int, default=600, help="seconds between scans (default 600)")
    w.set_defaults(fn=cmd_watch)
    fl = sub.add_parser("findings", help="list open findings")
    fl.add_argument("--all", action="store_true", help="include dismissed, resolved and acted-on findings")
    fl.set_defaults(fn=cmd_findings)
    s = sub.add_parser("show", help="explain one finding and what you can do")
    s.add_argument("id", type=int)
    s.set_defaults(fn=cmd_show)
    a = sub.add_parser("approve", help="let xguard act on a finding")
    a.add_argument("id", type=int)
    a.add_argument("action", nargs="?")
    a.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    a.set_defaults(fn=cmd_approve)
    d = sub.add_parser("dismiss", help="mark a finding as expected")
    d.add_argument("id", type=int)
    d.add_argument("--reason")
    d.set_defaults(fn=cmd_dismiss)
    r = sub.add_parser("restore", help="undo an action")
    r.add_argument("id", type=int)
    r.set_defaults(fn=cmd_restore)
    lg = sub.add_parser("log", help="show the audit log")
    lg.add_argument("id", type=int, nargs="?")
    lg.set_defaults(fn=cmd_log)
    sub.add_parser("status", help="show agent status").set_defaults(fn=cmd_status)
    ia = sub.add_parser("install-agent", help="run xguard in the background at login")
    ia.add_argument("--interval", type=int, default=600)
    ia.add_argument("--yes", action="store_true")
    ia.set_defaults(fn=cmd_install_agent)
    sub.add_parser("uninstall-agent", help="stop the background agent").set_defaults(fn=cmd_uninstall_agent)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config()
    store = Store(cfg.db_path)
    try:
        return args.fn(cfg, store, args)
    finally:
        store.close()


if __name__ == "__main__":
    sys.exit(main())
