# xguard agent

An always-on security agent for your Mac. It watches continuously; you decide.

xguard runs a set of read-only checks every few minutes, keeps track of what it has
already seen, and tells you when something changes or looks wrong. When Anthropic
credentials are available, Claude explains each new finding in plain language and
suggests one action. Nothing is changed on your Mac until you approve it, and every
change xguard makes can be undone.

## What it checks

| Monitor | What it looks for |
|---|---|
| `posture` | FileVault, firewall, Gatekeeper, System Integrity Protection and automatic updates turned off. |
| `persistence` | Programs that start by themselves (LaunchAgents and LaunchDaemons) that are unsigned, missing, hidden, run from temporary folders, run inline shell commands, or appeared since the last scan. |
| `network` | Your programs accepting connections from the whole network, when they are unsigned or new. |
| `downloads` | Installers, apps, disk images and scripts downloaded in the last 30 days that Gatekeeper rejects, or that lost their quarantine flag. |
| `ssh` | Private SSH keys readable by other users, or without a passphrase. |

The first scan records what is already on the Mac and only reports things that look
wrong on their own. After that, anything new is reported until you review it.

## Install

Requires macOS and [uv](https://docs.astral.sh/uv/).

```bash
uv tool install ./agent
```

For development, from this folder:

```bash
uv sync
uv run xguard scan
```

## Use

```bash
xguard scan                 # run every check once
xguard findings             # what is open
xguard show 3               # explain finding 3 and list what you can do
xguard approve 3 disable    # let xguard act on it (asks for confirmation)
xguard restore 3            # undo that action
xguard dismiss 3            # it is expected: stop reporting it
xguard log                  # everything xguard detected and did
xguard watch                # keep scanning in the foreground
xguard install-agent        # run in the background at login
xguard uninstall-agent
xguard status
```

## What xguard will and will not do

- **Checks are read-only.** They read files, launch configurations, code signatures, Gatekeeper
  assessments and your own listening sockets. They never need admin rights.
- **Actions need your approval** and only touch things you own: moving a file or a launch
  item into `~/.xguard/quarantine` (reversible with `xguard restore`), making an SSH key
  readable only by you (reversible), or asking one of your processes to quit (not reversible,
  and refused if the process ID now belongs to a different program).
- **Anything that needs admin rights is shown as instructions**, never run.
- **Claude never acts.** It reads one finding at a time and suggests at most one of the
  actions listed on it. Evidence from the filesystem is passed as untrusted data, and any
  suggested action that is not on the finding is discarded.

## Claude triage

Triage turns on automatically when Anthropic credentials are available (`ANTHROPIC_API_KEY`,
`ANTHROPIC_AUTH_TOKEN`, or an `ant auth login` profile). It uses `claude-opus-5-5` at medium
effort with structured output and server-side refusal fallbacks. Without credentials, xguard
works the same and skips the explanation.

## Settings

| Variable | Default | Meaning |
|---|---|---|
| `XGUARD_HOME` | `~/.xguard` | Where findings, the audit log and the quarantine live. |
| `XGUARD_MODEL` | `claude-opus-5-5` | Model used for triage. |
| `XGUARD_TRIAGE` | `1` | Set to `0` to never call Claude. |
| `XGUARD_NOTIFY` | `1` | Set to `0` to turn off Notification Center alerts. |
| `XGUARD_LANG` | `en` | Language of Claude's explanations, for example `it`. |

## Tests

```bash
uv run pytest
```

Tests use a fake command runner, so they never touch the real system.

## Limits of this version

- macOS only. Without admin rights, the network check sees only your own processes.
- It does not scan file contents for malware signatures and does not replace an antivirus.
- It has no threat-intelligence feed yet: judgments come from signatures, locations and change.
