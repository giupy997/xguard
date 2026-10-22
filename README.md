# xguard

An always-on security agent for your Mac. It watches continuously; you decide. Free, with no account and no subscription.

| Path | What it is |
|---|---|
| `agent/` | The xguard agent (Python, macOS). See [agent/README.md](agent/README.md). |
| `index.html` | The website, one self-contained file: inline CSS and JS, Google Fonts only, no build step. |
| `assets/`, `design/`, `brand.html` | Design tokens, the brief and the brand guidelines from the earlier GUARDIAN direction. The brand page still shows the old name and mark; it has not been redone for xguard yet. |

## Install

Requires macOS 13 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv tool install "git+https://github.com/giupy997/xguard.git#subdirectory=agent"
xguard scan
```

## Preview the site

```bash
python3 -m http.server 4175
```

Then open http://localhost:4175/.

## Design rule

The only chromatic color on the site is the one used to say something is wrong. Red marks a problem; everything else is ink and paper.
