"""All monitors, in the order a scan runs them."""

from .base import Context, Monitor
from .downloads import DownloadsMonitor
from .network import NetworkMonitor
from .persistence import PersistenceMonitor
from .posture import PostureMonitor
from .ssh import SshMonitor


def default_monitors() -> list[Monitor]:
    return [PostureMonitor(), PersistenceMonitor(), NetworkMonitor(), DownloadsMonitor(), SshMonitor()]


__all__ = ["Context", "Monitor", "default_monitors"]
