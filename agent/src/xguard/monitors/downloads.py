"""Recently downloaded files that can run code: installers, apps, scripts.

Each file is checked once per content hash. Gatekeeper's own assessment (spctl)
decides whether an app or installer is signed and notarized.
"""

from __future__ import annotations

import hashlib
import time
from pathlib import Path

from ..models import Action, Finding
from .base import Context

SCRIPT_EXT = {".command", ".sh", ".tool", ".scpt", ".applescript", ".terminal", ".jar", ".py", ".js"}
INSTALLER_EXT = {".pkg", ".mpkg"}
IMAGE_EXT = {".dmg", ".iso"}
APP_EXT = {".app"}
WINDOW_DAYS = 30
MAX_FILES = 300
MAX_HASH_BYTES = 1 << 30


def sha256(path: Path) -> str | None:
    if path.is_dir():
        return None
    h = hashlib.sha256()
    read = 0
    try:
        with path.open("rb") as fh:
            while chunk := fh.read(1 << 20):
                h.update(chunk)
                read += len(chunk)
                if read > MAX_HASH_BYTES:
                    return None
    except OSError:
        return None
    return h.hexdigest()


class DownloadsMonitor:
    name = "downloads"

    def scan(self, ctx: Context) -> list[Finding]:
        folder = ctx.config.home / "Downloads"
        if not folder.is_dir():
            return []
        cutoff = time.time() - WINDOW_DAYS * 86400
        candidates = []
        try:
            entries = list(folder.iterdir())
        except OSError:
            return []
        for p in entries:
            ext = p.suffix.lower()
            if ext not in SCRIPT_EXT | INSTALLER_EXT | IMAGE_EXT | APP_EXT:
                continue
            try:
                if p.stat().st_mtime < cutoff:
                    continue
            except OSError:
                continue
            candidates.append(p)
        candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        findings = []
        for p in candidates[:MAX_FILES]:
            f = self._inspect(ctx, p)
            if f:
                findings.append(f)
        return findings

    def _inspect(self, ctx: Context, p: Path) -> Finding | None:
        run = ctx.runner.run
        ext = p.suffix.lower()
        digest = sha256(p)
        reasons: list[str] = []
        severity = "info"
        assessment = None

        if ext in INSTALLER_EXT:
            res = run(["spctl", "-a", "-vv", "-t", "install", str(p)])
            assessment = (res.out + res.err).strip()
            if not res.ok:
                reasons.append("Gatekeeper rejects this installer (not signed or not notarized by Apple)")
                severity = "high"
        elif ext in APP_EXT:
            res = run(["spctl", "-a", "-vv", "-t", "exec", str(p)])
            assessment = (res.out + res.err).strip()
            if not res.ok:
                reasons.append("Gatekeeper rejects this app (not signed or not notarized by Apple)")
                severity = "high"
        elif ext in IMAGE_EXT:
            res = run(["spctl", "-a", "-vv", "-t", "open", "--context", "context:primary-signature", str(p)])
            assessment = (res.out + res.err).strip()
            if not res.ok:
                reasons.append("the disk image is not signed, so check what is inside before opening any app")
                severity = "low"
        elif ext in SCRIPT_EXT:
            reasons.append("it is a script: running it gives it the same access to your files as you have")
            severity = "medium"

        if reasons and ext not in SCRIPT_EXT:
            q = run(["xattr", "-p", "com.apple.quarantine", str(p)])
            if not q.ok:
                reasons.append("it has no download quarantine flag, so macOS will not check it when opened")

        if not reasons:
            return None
        key = f"{p}:{(digest or 'dir')[:16]}"
        return Finding(
            self.name, key, severity,
            f"Downloaded file {p.name} can run code",
            "; ".join(r[0].upper() + r[1:] for r in reasons) + ".",
            {"path": str(p), "sha256": digest, "gatekeeper": assessment},
            (Action("quarantine", "Move it to the xguard quarantine (you can restore it)", "auto",
                    params={"path": str(p)}),),
        )
