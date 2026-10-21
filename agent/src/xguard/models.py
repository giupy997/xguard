"""Core data types: what a monitor reports and what a user can approve."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

SEVERITIES = ("info", "low", "medium", "high", "critical")


@dataclass(frozen=True)
class Action:
    """Something xguard can do about a finding, but only after the user approves it.

    kind "auto" actions are executed by xguard and are reversible.
    kind "manual" actions are instructions: xguard never runs them (they need admin rights).
    """

    id: str
    label: str
    kind: str  # "auto" | "manual"
    params: dict[str, Any] = field(default_factory=dict)
    instructions: str = ""


@dataclass(frozen=True)
class Finding:
    monitor: str
    key: str                # stable identity within the monitor (path, setting name, port...)
    severity: str
    title: str
    detail: str
    evidence: dict[str, Any] = field(default_factory=dict)
    actions: tuple[Action, ...] = ()

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"unknown severity {self.severity!r}")

    @property
    def fingerprint(self) -> str:
        """Same problem, same fingerprint: used to dedupe across scans."""
        raw = json.dumps([self.monitor, self.key, self.title], sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


def severity_rank(sev: str) -> int:
    return SEVERITIES.index(sev)
