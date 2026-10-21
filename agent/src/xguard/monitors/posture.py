"""Baseline Mac protections: disk encryption, firewall, Gatekeeper, SIP, updates.

Fixing any of these needs administrator rights, so the actions are manual:
xguard explains the fix and never runs it.
"""

from __future__ import annotations

from ..models import Action, Finding
from .base import Context

FIREWALL = "/usr/libexec/ApplicationFirewall/socketfilterfw"


class PostureMonitor:
    name = "posture"

    def scan(self, ctx: Context) -> list[Finding]:
        run = ctx.runner.run
        findings: list[Finding] = []

        fv = run(["fdesetup", "status"])
        if fv.ok and "FileVault is Off" in fv.out:
            findings.append(Finding(
                self.name, "filevault", "high", "FileVault disk encryption is off",
                "Anyone with physical access to this Mac can read its disk without your password.",
                {"fdesetup": fv.out.strip()},
                (Action("open-settings", "Turn on FileVault", "manual",
                        instructions="System Settings → Privacy & Security → FileVault → Turn On. "
                                     "Store the recovery key somewhere other than this Mac."),),
            ))

        fw = run([FIREWALL, "--getglobalstate"])
        if fw.ok and ("disabled" in fw.out.lower() or "state = 0" in fw.out):
            findings.append(Finding(
                self.name, "firewall", "medium", "The macOS firewall is off",
                "Apps on this Mac can accept incoming connections from the network without asking.",
                {"socketfilterfw": fw.out.strip()},
                (Action("enable-firewall", "Turn on the firewall", "manual",
                        instructions="System Settings → Network → Firewall → On. "
                                     f"Or in Terminal: sudo {FIREWALL} --setglobalstate on"),),
            ))

        gk = run(["spctl", "--status"])
        if gk.ok and "disabled" in gk.out.lower():
            findings.append(Finding(
                self.name, "gatekeeper", "high", "Gatekeeper is disabled",
                "macOS will run apps from any developer without checking their signature or notarization.",
                {"spctl": gk.out.strip()},
                (Action("enable-gatekeeper", "Turn Gatekeeper back on", "manual",
                        instructions="In Terminal: sudo spctl --global-enable"),),
            ))

        sip = run(["csrutil", "status"])
        if sip.ok and "disabled" in sip.out.lower():
            findings.append(Finding(
                self.name, "sip", "high", "System Integrity Protection is disabled",
                "Protected system files and processes can be modified by any program running as root.",
                {"csrutil": sip.out.strip()},
                (Action("enable-sip", "Re-enable SIP", "manual",
                        instructions="Restart into Recovery (hold the power button), open Terminal, "
                                     "run: csrutil enable, then restart."),),
            ))

        au = run(["defaults", "read", "/Library/Preferences/com.apple.SoftwareUpdate",
                  "AutomaticallyInstallMacOSUpdates"])
        if au.ok and au.out.strip() == "0":
            findings.append(Finding(
                self.name, "auto-updates", "low", "Automatic macOS updates are off",
                "Security fixes are not installed until you install them by hand.",
                {"AutomaticallyInstallMacOSUpdates": au.out.strip()},
                (Action("enable-updates", "Turn on automatic updates", "manual",
                        instructions="System Settings → General → Software Update → Automatic updates → "
                                     "turn on “Install Security Responses and system files”."),),
            ))
        return findings
