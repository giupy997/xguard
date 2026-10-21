"""Paths and settings. Everything xguard writes lives under one directory."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    home: Path                 # user's home directory (what we scan)
    data_dir: Path             # where xguard keeps its state
    model: str = "claude-opus-5-5"
    triage_enabled: bool = True
    notify: bool = True
    language: str = "en"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "xguard.db"

    @property
    def quarantine_dir(self) -> Path:
        return self.data_dir / "quarantine"


def load_config() -> Config:
    home = Path(os.environ.get("XGUARD_SCAN_HOME", Path.home())).expanduser()
    data_dir = Path(os.environ.get("XGUARD_HOME", Path.home() / ".xguard")).expanduser()
    return Config(
        home=home,
        data_dir=data_dir,
        model=os.environ.get("XGUARD_MODEL", "claude-opus-5-5"),
        triage_enabled=os.environ.get("XGUARD_TRIAGE", "1") != "0",
        notify=os.environ.get("XGUARD_NOTIFY", "1") != "0",
        language=os.environ.get("XGUARD_LANG", "en"),
    )
