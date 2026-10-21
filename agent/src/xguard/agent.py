"""One scan cycle, and the always-on loop around it.

The agent runs every monitor, records what it finds, asks Claude to explain new
findings, and notifies you about the serious ones. It never acts on its own.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from .config import Config
from .models import severity_rank
from .monitors import Context, Monitor, default_monitors
from .notify import notify
from .runner import Runner, SystemRunner
from .store import Store, StoredFinding
from .triage import triage

NOTIFY_AT = "medium"


@dataclass
class CycleReport:
    new: list[StoredFinding] = field(default_factory=list)
    still_open: int = 0
    resolved: int = 0
    errors: dict[str, str] = field(default_factory=dict)
    duration: float = 0.0


class Agent:
    def __init__(self, cfg: Config, store: Store, runner: Runner | None = None,
                 monitors: list[Monitor] | None = None,
                 triage_fn: Callable[[Config, StoredFinding], dict[str, Any] | None] = triage) -> None:
        self.cfg = cfg
        self.store = store
        self.runner = runner or SystemRunner()
        self.monitors = monitors if monitors is not None else default_monitors()
        self.triage_fn = triage_fn

    def cycle(self) -> CycleReport:
        start = time.time()
        report = CycleReport()
        ctx = Context(self.cfg, self.runner, self.store)
        for m in self.monitors:
            try:
                found = m.scan(ctx)
            except Exception as e:  # one broken monitor must not stop the others
                report.errors[m.name] = f"{type(e).__name__}: {e}"
                self.store.log(None, "monitor-error", {"monitor": m.name, "error": str(e)})
                continue
            seen = set()
            for f in found:
                seen.add(f.fingerprint)
                stored, is_new = self.store.upsert(f)
                if is_new:
                    report.new.append(stored)
                elif stored.status == "open":
                    report.still_open += 1
            report.resolved += len(self.store.resolve_missing(m.name, seen))

        for f in report.new:
            result = self.triage_fn(self.cfg, f)
            if result:
                self.store.set_triage(f.id, result)

        if self.cfg.notify:
            serious = [f for f in report.new if severity_rank(f.severity) >= severity_rank(NOTIFY_AT)]
            if serious:
                worst = max(serious, key=lambda f: severity_rank(f.severity))
                more = f" and {len(serious) - 1} more" if len(serious) > 1 else ""
                notify(self.runner, "xguard", f"{worst.title}{more}. Run: xguard findings")
                for f in serious:
                    self.store.mark_notified(f.id)

        report.duration = time.time() - start
        self.store.set_state("last_cycle", {"at": start, "new": len(report.new),
                                            "resolved": report.resolved, "errors": report.errors})
        return report

    def watch(self, interval: float, on_cycle: Callable[[CycleReport], None] | None = None,
              max_cycles: int | None = None) -> None:
        n = 0
        while max_cycles is None or n < max_cycles:
            r = self.cycle()
            if on_cycle:
                on_cycle(r)
            n += 1
            if max_cycles is not None and n >= max_cycles:
                break
            time.sleep(interval)
