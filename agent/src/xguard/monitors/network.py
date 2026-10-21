"""Programs accepting connections from the network.

Without admin rights macOS only shows your own processes, which is where
user-level malware and forgotten dev servers live. A listener bound to every
interface (*, 0.0.0.0, ::) can be reached by anyone on the same network.
"""

from __future__ import annotations

from ..models import Action, Finding
from .base import Context, signature

WILDCARDS = ("*", "0.0.0.0", "[::]", "::")


def parse_lsof(out: str) -> list[dict]:
    """Parse `lsof -F pcn` output into {pid, command, address, port} records."""
    rows: list[dict] = []
    pid = cmd = None
    for line in out.splitlines():
        if not line:
            continue
        tag, value = line[0], line[1:]
        if tag == "p":
            pid, cmd = value, None
        elif tag == "c":
            cmd = value
        elif tag == "n" and pid:
            addr, _, port = value.rpartition(":")
            if port.isdigit():
                rows.append({"pid": int(pid), "command": cmd or "?", "address": addr, "port": int(port)})
    return rows


class NetworkMonitor:
    name = "network"

    def scan(self, ctx: Context) -> list[Finding]:
        res = ctx.runner.run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN", "-F", "pcn"])
        if res.code not in (0, 1):  # lsof exits 1 when nothing matches
            return []
        exposed = [r for r in parse_lsof(res.out) if r["address"] in WILDCARDS]

        baseline = ctx.baseline(self.name)
        first_run = baseline is None
        known = set(baseline or [])
        seen: dict[str, dict] = {}
        for r in exposed:
            seen.setdefault(f"{r['command']}:{r['port']}", r)

        findings: list[Finding] = []
        for key, r in sorted(seen.items()):
            exe = ctx.runner.run(["ps", "-o", "comm=", "-p", str(r["pid"])]).out.strip()
            sig = signature(ctx.runner, exe) if exe.startswith("/") else None
            reasons = []
            severity = "info"
            if sig is not None and sig.checked and not sig.signed:
                reasons.append("the program is not code-signed")
                severity = "high"
            if not first_run and key not in known:
                reasons.append("it started listening since the last scan")
                severity = "high" if severity == "high" else "medium"
            if not reasons:
                continue
            findings.append(Finding(
                self.name, key, severity,
                f"{r['command']} is open to the network on port {r['port']}",
                "Anyone on the same network can try to connect to it: " + "; ".join(reasons) + ".",
                {"pid": r["pid"], "command": r["command"], "executable": exe or None, "port": r["port"],
                 "address": r["address"], "signature": sig.describe() if sig else None},
                (Action("stop-process", f"Quit {r['command']} (process {r['pid']})", "auto",
                        params={"pid": r["pid"], "executable": exe}),
                 Action("firewall", "Block incoming connections for it", "manual",
                        instructions="System Settings → Network → Firewall → Options → add the app and set "
                                     "“Block incoming connections”."),),
            ))
        if first_run:
            ctx.save_baseline(self.name, set(seen))
        return findings
