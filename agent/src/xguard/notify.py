"""macOS notifications through Notification Center. Text is passed as an argument, never interpolated."""

from __future__ import annotations

from .runner import Runner

SCRIPT = 'on run argv\ndisplay notification (item 2 of argv) with title (item 1 of argv)\nend run'


def notify(runner: Runner, title: str, message: str) -> None:
    runner.run(["osascript", "-e", SCRIPT, title[:120], message[:240]], timeout=5)
