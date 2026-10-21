"""SSH private keys that others could read or use."""

from __future__ import annotations

import stat
from pathlib import Path

from ..models import Action, Finding
from .base import Context


def private_keys(ssh_dir: Path) -> list[Path]:
    keys = []
    if not ssh_dir.is_dir():
        return keys
    for p in sorted(ssh_dir.iterdir()):
        if not p.is_file() or p.suffix in (".pub",) or p.name in ("known_hosts", "config", "authorized_keys"):
            continue
        try:
            with p.open("rb") as fh:
                head = fh.read(64)
        except OSError:
            continue
        if b"PRIVATE KEY" in head:
            keys.append(p)
    return keys


class SshMonitor:
    name = "ssh"

    def scan(self, ctx: Context) -> list[Finding]:
        findings = []
        for key in private_keys(ctx.config.home / ".ssh"):
            mode = stat.S_IMODE(key.stat().st_mode)
            if mode & 0o077:
                findings.append(Finding(
                    self.name, f"{key}:perms", "high", f"SSH key {key.name} is readable by other users",
                    f"Its permissions are {oct(mode)}; only you should be able to read a private key.",
                    {"path": str(key), "mode": oct(mode)},
                    (Action("fix-perms", "Make it readable only by you (chmod 600)", "auto",
                            params={"path": str(key), "old_mode": mode}),),
                ))
            res = ctx.runner.run(["ssh-keygen", "-y", "-P", "", "-f", str(key)])
            if res.ok:
                findings.append(Finding(
                    self.name, f"{key}:passphrase", "low", f"SSH key {key.name} has no passphrase",
                    "Anyone who copies this file, for example through a backup or a malicious app, "
                    "can log in wherever this key is accepted.",
                    {"path": str(key)},
                    (Action("add-passphrase", "Add a passphrase", "manual",
                            instructions=f"In Terminal: ssh-keygen -p -f \"{key}\" (then add it to the "
                                         "macOS keychain with ssh-add --apple-use-keychain)."),),
                ))
        return findings
