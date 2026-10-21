"""Runs system commands. Monitors depend on this interface so tests can fake it."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True)
class Result:
    code: int
    out: str
    err: str

    @property
    def ok(self) -> bool:
        return self.code == 0


class Runner(Protocol):
    def run(self, cmd: Sequence[str], timeout: float = 20.0) -> Result: ...


class SystemRunner:
    """Executes commands without a shell. Never escalates privileges."""

    def run(self, cmd: Sequence[str], timeout: float = 20.0) -> Result:
        try:
            p = subprocess.run(list(cmd), capture_output=True, text=True, timeout=timeout)
            return Result(p.returncode, p.stdout, p.stderr)
        except FileNotFoundError:
            return Result(127, "", f"command not found: {cmd[0]}")
        except subprocess.TimeoutExpired:
            return Result(124, "", f"timed out after {timeout}s: {' '.join(cmd)}")
