from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pytest

from xguard.config import Config
from xguard.monitors import Context
from xguard.runner import Result
from xguard.store import Store


class FakeRunner:
    """Answers commands by longest matching prefix. Records every call."""

    def __init__(self, responses: dict[tuple[str, ...], Result] | None = None) -> None:
        self.responses = dict(responses or {})
        self.calls: list[list[str]] = []

    def on(self, *prefix: str, code: int = 0, out: str = "", err: str = "") -> "FakeRunner":
        self.responses[tuple(prefix)] = Result(code, out, err)
        return self

    def run(self, cmd: Sequence[str], timeout: float = 20.0) -> Result:
        cmd = list(cmd)
        self.calls.append(cmd)
        best = None
        for prefix, res in self.responses.items():
            if tuple(cmd[: len(prefix)]) == prefix and (best is None or len(prefix) > len(best[0])):
                best = (prefix, res)
        return best[1] if best else Result(127, "", "not faked")


@pytest.fixture
def cfg(tmp_path: Path) -> Config:
    home = tmp_path / "home"
    home.mkdir()
    return Config(home=home, data_dir=tmp_path / "data", triage_enabled=False, notify=False)


@pytest.fixture
def store(cfg: Config):
    s = Store(cfg.db_path)
    yield s
    s.close()


@pytest.fixture
def runner() -> FakeRunner:
    return FakeRunner()


@pytest.fixture
def ctx(cfg, runner, store) -> Context:
    return Context(cfg, runner, store)
