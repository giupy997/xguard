"""What every monitor shares: the scan context and the code-signing helper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..config import Config
from ..models import Finding
from ..runner import Runner
from ..store import Store


@dataclass
class Context:
    config: Config
    runner: Runner
    store: Store

    def baseline(self, monitor: str) -> list[str] | None:
        """Items seen on previous scans, or None if this monitor has never run."""
        return self.store.get_state(f"baseline:{monitor}")

    def save_baseline(self, monitor: str, items: set[str]) -> None:
        self.store.set_state(f"baseline:{monitor}", sorted(items))


class Monitor(Protocol):
    name: str

    def scan(self, ctx: Context) -> list[Finding]: ...


@dataclass(frozen=True)
class Signature:
    signed: bool
    valid: bool
    authority: str | None
    team_id: str | None
    checked: bool = True   # False when the file could not be read (for example, owned by root)

    @property
    def apple(self) -> bool:
        return bool(self.authority and self.authority.startswith("Software Signing")) or self.team_id == "APPLE"

    def describe(self) -> str:
        if not self.checked:
            return "could not be checked (no permission to read the file)"
        if not self.signed:
            return "not signed"
        if not self.valid:
            return f"signature invalid ({self.authority or 'unknown signer'})"
        return self.authority or "signed"


def signature(runner: Runner, path: str) -> Signature:
    """Read the code signature of a file or bundle. Read-only."""
    info = runner.run(["codesign", "-dv", "--verbose=2", path])
    text = info.err + info.out
    if "Permission denied" in text or "Operation not permitted" in text:
        return Signature(False, False, None, None, checked=False)
    if "not signed at all" in text or (not info.ok and "Authority=" not in text):
        return Signature(False, False, None, None)
    authority = None
    team = None
    for line in text.splitlines():
        if line.startswith("Authority=") and authority is None:
            authority = line.split("=", 1)[1].strip()
        elif line.startswith("TeamIdentifier="):
            value = line.split("=", 1)[1].strip()
            team = None if value == "not set" else value
    verify = runner.run(["codesign", "--verify", "--strict", path])
    return Signature(True, verify.ok, authority, team)


SUSPICIOUS_DIRS = ("/tmp/", "/private/tmp/", "/var/tmp/", "/Users/Shared/", "/private/var/folders/")


def suspicious_location(path: str) -> str | None:
    """Why a program's location is unusual for something that runs at login, if it is."""
    for d in SUSPICIOUS_DIRS:
        if path.startswith(d):
            return f"runs from a temporary or shared folder ({d})"
    parts = Path(path).parts
    if any(p.startswith(".") and p not in (".", "..") for p in parts[:-1]):
        return "runs from a hidden folder"
    return None
