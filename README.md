# GUARDIAN

Landing page and brand system for GUARDIAN, a non-custodial defense agent for Solana holders.
GUARDIAN decodes and simulates every pending transaction before you sign, compares what the page
says with what the payload does, and tells you when they disagree. It never sees your keys.

## Contents

| Path | What it is |
|---|---|
| `index.html` | The landing page. One self-contained file: inline CSS and JS, Google Fonts only, no build step. |
| `brand.html` | Brand guidelines: the mark, lockups, misuse, color, type, voice, components. |
| `assets/` | `logo-mark.svg`, `logo-lockup.svg`, `favicon.svg`. |
| `design/BRIEF.md` | The design brief the site is built from ("The Red Pen" direction). |
| `design/ADDENDUM.md` | Overrides to the brief: placeholders, omitted links, integration notes. |
| `design/tokens.css` | Design tokens (colors with verified contrast, type scale, spacing, motion). |

## Run locally

Any static server works:

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173/ and http://localhost:4173/brand.html.

## Before launch

- The waitlist form posts to `/api/waitlist`, which does not exist yet. Until it does, the form shows a network error by design; it never fakes a success.
- Domains use the placeholder `guardian.example`.
- Every figure marked VERIFY in `design/BRIEF.md` §15 (loss figures, rule counts, latencies, roadmap years, fixture keys) must be confirmed or replaced.

## Design rule

The only chromatic color on the site is the one used to say no. Red marks something wrong; everything else is ink and paper.
