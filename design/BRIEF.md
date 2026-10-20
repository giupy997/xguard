# GUARDIAN — Final Design Brief

**Direction:** The Red Pen (Editorial Clarity) · **Version:** 1.0 final · **Date:** 2026-10-20
**Deliverable:** one self-contained `index.html` (inline CSS + JS, no frameworks, no build step, no external JS, fonts from Google Fonts only, no raster images).
**Companion files:** `design/tokens.css` (paste verbatim), `assets/logo-mark.svg`, `assets/logo-lockup.svg`, `assets/favicon.svg`.

This document is the contract. Where it is silent, follow the rule in §1.2. Where it conflicts with an earlier draft or a judge note, this document wins. Items marked **VERIFY** are placeholders that must be confirmed or replaced before launch; they are collected in §15.

---

## 0. How to read this brief

| § | What it settles |
|---|---|
| 1 | The brand idea, the one rule, positioning |
| 2 | Voice: rules, do/don't, banned words, canonical lines |
| 3 | Logo: the Open G (geometry, lockup, clear space, sizes, color, favicon, seal), and the caret's new job |
| 4 | Design tokens (the `:root` block) with verified contrast |
| 5 | Typography: fonts, weights, loading, fallbacks, full scale |
| 6 | Layout: the Manuscript grid, spacing, section rhythm, content devices, nav |
| 7 | Motion: principles, durations, reduced motion |
| 8 | Components (buttons, inputs, chips, ruled lists, ledger tables, code, details, tabs, address spans) |
| 9 | Page structure and section-by-section spec with FINAL copy |
| 10 | The signature interaction, "The Reading": states, timing, controls, a11y, and the complete data for five cases |
| 11 | Diagrams, drawn precisely |
| 12 | Forms: endpoint, validation, states |
| 13 | `<head>`, SEO, favicon wiring |
| 14 | Quality bar: the self-verification checklist |
| 15 | VERIFY list: every figure that must be confirmed before launch |
| 16 | Engineering notes: file structure, JS budget, build order |

---

## 1. Brand idea

### 1.1 The idea in one paragraph

A Solana transaction is a document your wallet asks you to sign, and almost nobody reads it. GUARDIAN is the proofreader. It reads the document aloud in plain language, marks the line that lies, and hands it back before you sign. The whole brand is that one gesture: an editor's red pen on a typeset page. Large serif headlines that state facts. A sans for the body. A mono for anything that is literally on-chain. Exactly one chromatic color, used only to say that something is wrong. The site is laid out like a security whitepaper that somebody at Stripe designed: numbered sections, hairline rules, ledger tables instead of cards, precise line-art diagrams, and a hero that is a single sentence with a red full stop.

Restraint is the trust signal. A product that never raises its voice reads as a product that knows what it is looking at.

### 1.2 The one rule (auditable on every screen)

> **The only color on the site is the one we use to say no.**

If a pixel is red (`--pen`), something is wrong at that pixel: a flagged instruction, a mismatched simulation cell, a Blocked or Caution chip, a form error, the single flagged node in a diagram, and the full stop of the hero sentence (the editor's mark). Red is never used for a CTA, never for the logo, never for decoration, never for "brand". Everything else is ink and paper. When in doubt, it is not red.

Corollaries:
- No cards, no shadows, no gradients, no canvas, no particles, no glows, no blur.
- No icons except the mark, the caret glyph, the check glyph, the status glyphs in the roadmap, and arrows drawn as 1px lines.
- No section-entrance animations. Sections are simply there, like pages of a document. Motion is reserved for reading (§7).
- Every claim on the page is pinned to an instruction name, a program id, a rule id, a list provenance, a date, or a balance diff.

### 1.3 Positioning statement

For Solana holders who sign transactions every day and distrust being sold to, GUARDIAN is the non-custodial defense layer that sits between the wallet and the signature: it decodes and simulates every pending transaction, diffs what the page says against what the payload does, matches every counterparty against threat intelligence with the provenance shown, and keeps watching approvals after the signature. Unlike a wallet's built-in warning (a label) or a hosted screening API (a verdict you cannot audit), GUARDIAN shows its reading row by row, cites the rule that fired, never touches a key, and leaves the decision to you.

Three-line promise (footer, canonical): **Non-custodial. Not a wallet. Never your keys.**

### 1.4 Who it is for, and what they test first

DeFi-native Solana holders on Phantom, Solflare and Backpack. Technically literate, security-conscious, allergic to hype. They will (1) look for the instruction names and program ids, (2) check whether the product cries wolf on a legitimate swap, (3) look for the seed-phrase question, (4) check whether the numbers have sources. The page answers all four in order: the demo (§10) includes a real-shaped `jup.ag` swap that resolves CLEAR, the custody strip under the hero answers keys before the first scroll, and every figure carries its source.

---

## 2. Voice

### 2.1 Rules

1. **State the mechanism, not the feeling.** "Runs `simulateTransaction` against the RPC you configure", never "keeps you safe".
2. **Prefer the instruction name to the metaphor.** If a metaphor is used, the instruction name follows in the same sentence.
3. **Short declarative sentences.** Full stops. No exclamation marks. No rhetorical questions in body copy (FAQ questions are questions, that is fine).
4. **Every number carries its unit and its source.** "$494M across chains in 2024 (ScamSniffer, 2024 annual report)."
5. **Admit the limit in the same breath as the claim.** "Blocked is advice, not a lock."
6. **Banned words:** secure, safe, safety, 100%, military-grade, revolutionary, seamless, next-gen, unlock, supercharge, frictionless, Web3, bulletproof, cutting-edge, game-changing, trustless (as a boast), "peace of mind".
7. **Second person, present tense.** The product is "GUARDIAN" or "it". "We" appears only in the waitlist section and the footer, where humans are speaking.
8. **Addresses are truncated 4…4** (first four, ellipsis U+2026, last four) with the full key in a `title` attribute, and never invented without a fixture behind them (§10.6 lists the fixture keys).
9. **Program and instruction names are set in mono, exactly as decoded:** `System.Assign`, `Token.SetAuthority`, `Token.Approve`, `Jupiter v6.sharedAccountsRoute`, `ComputeBudget.SetComputeUnitLimit`.
10. **GUARDIAN is always uppercase** in running text and the wordmark. Never "Guardian", never "guardian" except in the domain `guardian.sh`.
11. **No italics anywhere on the site.** Emphasis is done with a sentence break, a mono span, or a hairline.

### 2.2 Do / don't

| Don't | Do |
|---|---|
| Keep your assets safe with next-gen protection. | Nothing gets signed unread. |
| Our AI detects threats in real time! | It decodes and simulates every pending Solana transaction, compares what the page says with what the payload does, and tells you in one sentence when they disagree. |
| Military-grade security you can trust. | The agent that reads your transaction runs inside a TEE. Each release publishes an attestation you can verify against the binary. |
| Stops drainers dead. | Instruction 4 hands your USDC account to a flagged address. The swap pays out into an account that is no longer yours. |
| Guardian blocks dangerous transactions. | GUARDIAN never rejects a transaction. You do. A Blocked verdict is evidence, not a lock. |
| Join thousands of happy users! | We add wallets in batches of 100. Leave an address; we tell you when yours is up, and nothing else. |
| Seamless integration with your favorite wallet. | GUARDIAN is an adapter for Phantom, Solflare and Backpack. Your wallet stays your wallet. |
| Oops, something went wrong. | That doesn't look like an email address. Check for a stray space. |

### 2.3 Canonical lines (reuse verbatim)

- Headline: **Nothing gets signed unread.**
- Threat H2: **Your wallet shows you a button. The chain executes the payload.**
- Sparse act: **GUARDIAN never rejects a transaction. You do.**
- Button: **Join the waitlist**
- Error: **That doesn't look like an email address. Check for a stray space.**
- Success: **You're on the list. We'll write once.**
- Empty state (approvals index, Pro alert preview): **No outstanding delegates or authorities. Nothing to watch.**
- Footer: **Non-custodial. Not a wallet. Never your keys.**
- Footer notice: **GUARDIAN never asks for a seed phrase or private key. If something claiming to be GUARDIAN does, it is not GUARDIAN.**
- Legal: **A Clear verdict describes a payload, not an investment.**
- Pricing: **No GUARDIAN token. There will not be one.**

---

## 3. Logo

### 3.1 Decision: the Open G replaces the caret

Three judges reviewed the caret. Two found it the weakest mark in the set (a bar over a chevron reads as an inverted eject or a collapse icon before it reads as a proofreader's caret, and the claimed shield silhouette only appears if you are told to see it) and both independently rated the squared G with a detached corner the strongest construction of the five. The caret's one real virtue, that the logo is literally the reading cursor in the demo, does not require the caret to be the logo: a red-pen brand can own the caret as its proofreading glyph without putting it on the masthead.

So: **the mark is the Open G.** The caret stays in the product as the reading cursor and the FAQ disclosure glyph (§3.8).

### 3.2 Concept

A squared G whose loop never closes. The corner that would close it is lifted out and held as a single square point, one stroke-width away. Read as a letter, it is the G of GUARDIAN, built like a block of set type. Read as a gesture, it is a sentence held open: the point is not placed until the line has been read. The crossbar that enters from the right is the line between the user and the signature. The mark says "G", it says "not closed yet", and it never says "shield", "lock" or "alarm".

### 3.3 Geometry (64-unit master, `assets/logo-mark.svg`)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" role="img" aria-labelledby="t"><title id="t">GUARDIAN</title>
  <path d="M40 12H18A6 6 0 0 0 12 18V46A6 6 0 0 0 18 52H46A6 6 0 0 0 52 46V36H34"
        stroke="currentColor" stroke-width="8" stroke-linecap="butt" stroke-linejoin="miter"/>
  <rect x="48" y="8" width="8" height="8" fill="currentColor"/>
</svg>
```

- Stroke 8 on a 64 grid (1/8 of the box). Butt caps, miter joins. Outer bounds 8..56 on both axes.
- Three corners are true arcs of radius 6 on the centerline (10 outer, 2 inner). The fourth corner, where the right stem meets the crossbar at (52,36), is a square miter: its outer corner sits at (56,32), echoing the square point.
- The top stroke ends with a butt cap at x=40. The point occupies x 48..56, y 8..16: exactly the band the missing corner would fill. The gap between stroke and point is 8 units = one stroke width = 2px at 16px, so it never closes on fractional device-pixel ratios.
- The crossbar enters at y=36 and stops at x=34, reaching to just past the center of the counter. The mouth (point bottom y=16 to stem top y=32) is 16 units: generous at every size.
- Every coordinate sits on a 2-unit grid. Rendered at 16, 20, 24, 32, 64 and 200px the strokes land on whole or half pixels.

### 3.4 Lockup (`assets/logo-lockup.svg`)

- Horizontal lockup: mark, a gap of half the mark's height, then the wordmark **GUARDIAN** in Geist 500, uppercase, letter-spacing 0.16em, no ligatures, never italic.
- Vertical alignment: the wordmark's cap height is centered on the center of the mark's box (y=32 of 64). The crossbar sits slightly below the cap midline, which is correct optically.
- Nav size: mark 20px tall (so the G box is 15px), gap 10px, wordmark 13px (cap height ≈ 9.2px ≈ 60% of the G box). Footer: mark 28px, gap 14px, wordmark 16px, tracking 0.16em. Large (trust/OG contexts): mark 200px, wordmark 28px, tracking 0.22em, stacked and centered, gap 24px.
- In `index.html` build the lockup inline (SVG mark + HTML text in Geist), not by embedding `logo-lockup.svg`: the SVG file carries the wordmark as live `<text>` and depends on the font loading, which an `<img>` cannot do.
- Stacked lockup (footer column 1, avatars): mark centered above the wordmark, gap 0.75× mark height.

### 3.5 Clear space and minimum sizes

- Clear space on every side = one stroke width at the rendered size (1/8 of the mark's height). Nothing enters it, including the wordmark's own gap, which is defined separately above.
- Minimum sizes: mark alone 16px (favicon cut, §3.7), mark in a lockup 20px, lockup width 110px minimum.
- The mark never ships alone except as favicon and the seal variant (§3.6). On the page it always has the wordmark next to it or beneath it.

### 3.6 Seal variant (avatars, the Telegram bot, social)

Mark inside a 1px hairline circle, 64 viewBox, mark scaled to 60% and centered:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="currentColor">
  <circle cx="32" cy="32" r="31.5" stroke-width="1"/>
  <g transform="translate(32 32) scale(.6) translate(-32 -32)" stroke-width="8" stroke-linejoin="miter" stroke-linecap="butt">
    <path d="M40 12H18A6 6 0 0 0 12 18V46A6 6 0 0 0 18 52H46A6 6 0 0 0 52 46V36H34"/>
    <rect x="48" y="8" width="8" height="8" fill="currentColor" stroke="none"/>
  </g>
</svg>
```

For raster avatar exports (outside this site's scope), render on a solid `--ink-0` disc, mark in `--paper`.

### 3.7 Favicon (`assets/favicon.svg`)

A dedicated 16–32px cut, not a scaled master: `--ink-0` tile with radius 12/64 (3px at 16px), mark in `--paper` inset to a 40-unit box so strokes stay 2px at 16px, point 2px, gap 2px, mouth 3px. Colors are hard-coded because a favicon cannot inherit `currentColor`. Wire it as an inline data URI (§13). There is no light-tile variant: the dark tile is visible on both light and dark browser chrome.

### 3.8 The caret: the proofreading glyph

The caret is GUARDIAN's proofreading mark ("insert here"). It is not the logo and never appears in the lockup. It appears in exactly three places:

```svg
<svg class="caret" viewBox="0 0 16 12" width="14" height="10" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"><path d="M1.5 10.5 8 2l6.5 8.5"/></svg>
```

1. **The reading cursor** in the demo (§10.3): a 1px `--paper` rule across the READ column with the caret at its left end, pushed up against the current row. The caret points up: it is inserting GUARDIAN's reading under the line.
2. **The FAQ disclosure glyph**: rotated 180° (pointing down) when closed, upright when open, 200ms.
3. **The nav menu disclosure on mobile**: same behavior as the FAQ glyph.

### 3.9 Color rules for the mark

- Always one color, always `currentColor`: `--paper` on ink, or `--ink-0` on paper (print, light surfaces). Both strokes and the point are the same color. No outline-only version, no two-tone, no gradient.
- The red pen (`--pen`) is never used in the logo, the favicon or the seal. The brand itself must never look like an alarm; red is reserved for things that are wrong.
- Hover on the wordmark link (nav): the point translates 2px up and 2px right over 200ms and returns on leave (the corner lifts a little further). This is the only time the mark moves. Under reduced motion it does not.
- Never rotate, never place inside a shield or a rounded square other than the favicon tile, never add a drop shadow, never animate the stroke drawing itself.

---

## 4. Design tokens

The complete block lives in `design/tokens.css`; paste it unchanged. Core values and verified contrast:

```css
:root {
  --ink-0: #0A0A0B;  --ink-1: #121214;  --ink-2: #1A1A1D;
  --rule: #2A2A2E;   --rule-strong: #626268;
  --paper: #EDEBE6;  --paper-2: #A8A6A0;  --paper-3: #85837E;  --paper-hi: #FFFFFF;
  --pen: #FF5A4E;    --pen-wash: #2A1512;
  --focus: var(--paper);
}
```

| Foreground | on `--ink-0` | on `--ink-1` | on `--ink-2` | on `--pen-wash` | Use |
|---|---|---|---|---|---|
| `--paper` #EDEBE6 | **16.6:1** | 15.7:1 | 14.6:1 | 14.5:1 | primary text, headlines, CLEAR chip outline, cursor rule |
| `--paper-2` #A8A6A0 | **8.1:1** | 7.7:1 | 7.1:1 | 7.1:1 | secondary text, body on panels, check glyphs |
| `--paper-3` #85837E | **5.2:1** | 4.9:1 | 4.6:1 | 4.6:1 | eyebrows, metadata, footnotes, 12px minimum |
| `--pen` #FF5A4E | **6.4:1** | 6.1:1 | 5.6:1 | 5.6:1 | everything that is wrong |
| `--rule-strong` #626268 | 3.3:1 | 3.1:1 | 2.9:1 | — | perceivable UI boundaries (WCAG 1.4.11 needs 3:1): inputs, ghost buttons, meaningful diagram strokes. Not on `--ink-2` |
| `--rule` #2A2A2E | 1.4:1 | 1.3:1 | 1.2:1 | — | decorative hairlines only, exempt |
| `--ink-0` on `--paper` | **16.6:1** | | | | primary button text |
| `--ink-0` on `--paper-hi` | 19.8:1 | | | | primary button hover |
| `--ink-0` on `--pen` | **6.4:1** | | | | BLOCKED chip text (the only text on a red fill) |
| `--paper` on `--pen` | 2.6:1 ✗ | | | | never. Text on a pen fill is always ink |

All text pairs pass WCAG AA 4.5:1 at any size. The hairline `--rule` is decorative and carries no information on its own; any stroke that does carry information (an arrow, a boundary, a node) uses `--rule-strong` or `--paper-3` or `--paper`. The verification script lives in the design notes; the numbers above are computed from WCAG relative luminance, not estimated.

Semantic aliases (`--bg`, `--surface`, `--border`, `--text`, `--text-muted`, `--text-faint`, `--danger`, `--verdict-*`) are defined in `tokens.css`; components use the aliases, the demo uses `--pen` and `--pen-wash` directly.

---

## 5. Typography

### 5.1 Families (all on Google Fonts, all variable)

| Role | Family | Axis / weights loaded | Where |
|---|---|---|---|
| Display | **Newsreader** | `opsz 6..72`, `wght 400..500` (upright only, no italic file) | H1, H2, pricing tier names, the sparse act |
| Body | **Geist** | `wght 400..500` | body, lead, H3, UI labels, nav, buttons, forms, FAQ, tables |
| Mono | **Geist Mono** | `wght 400` | eyebrows, section numbers, instruction names, addresses, amounts, rule samples, demo rows, code, captions, status line |

Single stylesheet request (two preconnects + one link; keep it exactly in this form so only the used ranges download):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400..500&family=Geist:wght@400..500&family=Geist+Mono:wght@400&display=swap">
```

Budget: under 160KB of font bytes on first load (VERIFY in the network panel; if Newsreader exceeds 90KB, request `opsz,wght@6..72,450` only).

### 5.2 Display craft rules (Newsreader on ink)

A high-contrast serif on near-black blooms: thin hairlines sparkle and break. Therefore:
- `font-weight: 450` for H1 and H2 (variable axis), `500` for tier names and the sparse act at 32–40px.
- `font-optical-sizing: none; font-variation-settings: "opsz" 48;` for H1 and H2. Do not let the browser pick opsz 72 at 104px.
- Tracking: H1 −0.025em, H2 −0.015em. Never looser.
- No italics (none loaded; the browser must never synthesize one: `font-synthesis: none` on `html`).
- `text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased;` on `html`.

### 5.3 Fallback metrics (no layout jump on swap)

```css
@font-face { font-family: "Newsreader Fallback"; src: local("Georgia"), local("Times New Roman"); size-adjust: 97%; ascent-override: 93%; descent-override: 25%; line-gap-override: 0%; }
@font-face { font-family: "Geist Fallback"; src: local("Inter"), local("Helvetica Neue"), local("Arial"); size-adjust: 99%; ascent-override: 92%; descent-override: 23%; line-gap-override: 0%; }
@font-face { font-family: "Geist Mono Fallback"; src: local("Menlo"), local("Consolas"), local("Courier New"); size-adjust: 96%; ascent-override: 92%; descent-override: 23%; line-gap-override: 0%; }
```

Tune `size-adjust` so the hero sentence keeps its line count (2 lines at 1440px, 3 lines at 320px) with fonts blocked. Test with the fonts URL blocked in devtools. CLS target is 0.

### 5.4 Type scale (final)

| Token | Size / line-height | Family, weight, tracking | Color | Used for |
|---|---|---|---|---|
| `--t-h1` | clamp(42px, 8vw, 104px) / 0.98 | Newsreader 450, opsz 48, −0.025em | `--paper` | hero sentence only |
| `--t-h2` | clamp(32px, 4.6vw, 56px) / 1.05 | Newsreader 450, opsz 48, −0.015em | `--paper` | section headlines, the sparse act, waitlist H2 |
| `--t-tier` | 32px / 1.1 | Newsreader 500, opsz 32 | `--paper` | pricing tier names |
| `--t-h3` | 24px / 1.25 | Geist 500, −0.01em | `--paper` | sub-headlines inside sections (I/II/III blocks, "Six instructions…") |
| `--t-lead` | 21px / 1.45 | Geist 400 | `--paper-2` | hero lead, section intros; max-width 56ch |
| `--t-body` | 17px / 1.6 | Geist 400 | `--paper-2` on panels, `--paper` for primary paragraphs | body; max-width 62ch |
| `--t-small` | 14px / 1.5 | Geist 400 | `--paper-3` or `--paper-2` | proof line, captions, footnotes, footer, table footnotes |
| `--t-ui` | 14px / 1 | Geist 500 | `--paper-2` → `--paper` on hover | nav links, buttons, tab labels (tab labels are mono, see below) |
| `--t-eyebrow` | 12px / 1.4 | Geist Mono 400, uppercase, +0.14em | `--paper-3` | eyebrows, running heads, section numbers, table column heads |
| `--t-mono` | 13.5px / 1.6 (12.5px under 400px viewport) | Geist Mono 400, `font-variant-numeric: tabular-nums` | per context | demo rows, diff cells, code, ledger cells, addresses, tab labels, spec lists |
| `--t-mono-sm` | 12.5px / 1.5 | Geist Mono 400 | `--pen` on `--pen-wash`, `--paper-3` | margin notes, expanded-row insets, demo caption |
| FAQ question | 20px / 1.35 | Geist 500 | `--paper` | `summary` text |
| FAQ answer | 17px / 1.6 | Geist 400 | `--paper-2` | |

Rhythm: 8px grid. Headline `margin-bottom: 0.5em`; lead `margin-bottom: 40px` (2.5rem); paragraph gap 16px; H3 to body 12px. `font-feature-settings: "tnum"` is on wherever a number sits in a table, a diff, or a spec list. Nothing on the page is smaller than 12px. Body stays 17px at every viewport.

---

## 6. Layout system: the Manuscript grid

### 6.1 Container and gutters

- `max-width: 1180px`, centered. Side gutters: 20px (320–599), 40px (600–1023), 64px (1024+).
- On 1024+ the container is a 12-column grid, `column-gap: 24px`. **Columns 1–3 are the margin; columns 4–12 are the text block.** The margin holds the editorial apparatus (§6.2). Headlines span columns 4–11. Full-width devices (demo panel, ledger tables, diagrams) span columns 4–12. Nothing is centered except the waitlist block and the footer colophon.
- Below 1024px everything is one column; the margin apparatus collapses to a single mono line above each section.

### 6.2 The margin apparatus

Every numbered section renders:

```html
<section id="threat" class="sec" aria-labelledby="threat-h">
  <div class="sec-rule"><span class="sec-no">02</span></div>           <!-- 1px --rule across the full container; the number sits ON the rule, flush left, --ink-0 padding so it interrupts the line -->
  <aside class="margin" aria-hidden="true">                            <!-- cols 1–3, position: sticky; top: var(--sticky-top) -->
    <span class="eyebrow">02</span>
    <span class="eyebrow">The threat</span>
    <span class="footnote">Instruction names as decoded by build 0.4.</span>   <!-- optional, --t-small, --paper-3 -->
  </aside>
  <div class="text">…</div>                                             <!-- cols 4–12 -->
</section>
```

Below 1024px the `aside.margin` is replaced (CSS, not JS) by a single mono line in the text column: `02 / The threat`. The sticky offset is 96px (nav 56 + 40). The number on the rule and the number in the margin are the same number; the running title is the section's short name (table in §9.1).

### 6.3 Spacing and rhythm

- Between sections: 112px desktop, 72px mobile (padding-top of each section, measured from the rule).
- Between sub-blocks inside a section: 48px desktop, 32px mobile.
- 8px base unit for everything else; tokens `--s-1`…`--s-12`.
- The sparse act (§9.7) has 160px above and below on desktop, 96px on mobile, and no section rule or number.
- `scroll-margin-top: 72px` on every section so anchor links land under the sticky nav.

### 6.4 Content devices (in order of preference; the three-card grid is banned)

1. **Ruled list.** A stack of rows separated by 1px `--rule`, each row a grid: a mono label column (160px on 1024+, stacked above the text below 840px) and a text column. Used for the threat exhibits, the How-it-works layers, the trust facts, the verdict definitions, the roadmap items.
2. **Ledger table.** One `<table>` with hairline rows, mono column heads (`--t-eyebrow`), `tabular-nums` cells. Used for Can/Cannot, the comparison, pricing. On mobile: sticky first column with horizontal scrolling inside the table (`overflow-x: auto` on a wrapper, never on the page), except pricing, which stacks into three ruled lists.
3. **Two-column prose.** `columns: 2; column-gap: 48px;` at 1024+ for the threat lead (21px). Single column below.
4. **Full-width line art.** HTML/CSS diagrams (§11) spanning columns 4–12, hairline strokes, `--paper` emphasis, `--pen` for the single flagged element. Inline SVG only for arrowheads and the pen circle.
5. **The timeline.** A single horizontal 1px rule with ticks (roadmap), vertical on mobile.

Backgrounds: the page is `--ink-0` everywhere. The only `--ink-1` surfaces are the demo panel, the code block, inputs, and the message card in demo case 4. There are no colored bands.

### 6.5 Navigation

- 56px bar, 1px `--rule` underneath, `--ink-0` background, no blur. `position: sticky; top: 0` at 840px and above; static below.
- Left: the lockup (mark 20px + GUARDIAN 13px), links to `#top`.
- Right, 840px+: four text links (Geist 500 14px, `--paper-2`, hover `--paper` with underline offset growing 2px): **How it works** `#how` · **Trust** `#trust` · **Pricing** `#pricing` · **Rules** `#rules`; then, at 1180px+ only, a mono status line `Rules v0.4 · 61 rules` in `--paper-3` (VERIFY numbers; no dot, no color); then the primary button **Join the waitlist** (36px tall in the nav), `href="#waitlist"`.
- Below 840px: the lockup and a `<details class="menu"><summary>Menu <caret/></summary>…</details>` on the right. The open menu is an absolutely positioned `--ink-0` panel under the bar with a hairline bottom, listing the four links, the status line and the waitlist button as a vertical ruled list. No JS. Closing on link click: `onclick="this.closest('details').removeAttribute('open')"` on each link is allowed (three lines of JS total) but not required.
- No "Launch app" button. There is no app to launch, and the audience notices fake buttons.
- A visually hidden "Skip to content" link is the first focusable element and becomes visible on focus (top-left, `--paper` on `--ink-0`, 2px outline).

---

## 7. Motion

### 7.1 Principles

Motion is reserved for reading. The page does not animate on scroll, on load, or on hover, except as listed here. Properties are limited to `opacity` and `transform` (plus `max-height` on margin notes and `width` on the hold bar, both inside the demo). Easing is `cubic-bezier(.2,.8,.2,1)` everywhere. No `requestAnimationFrame` loops, no canvas, no parallax, no scroll-jacking, no hover scale.

### 7.2 Inventory (complete)

| Element | What moves | Duration |
|---|---|---|
| Hero full stop | opacity 0→1, 200ms after first paint (CSS animation, `animation-delay: 200ms`, no transform) | 400ms |
| Demo reading cursor | `translateY` row to row, then dwells | 200ms move, 380ms dwell |
| Demo instruction row | opacity 0.35→1 on arrival | 160ms |
| Demo flagged argument | underline `scaleX` 0→1, `transform-origin: left` | 240ms |
| Demo flagged row | background `--ink-1`→`--pen-wash` (background-color is allowed here, once) | 160ms |
| Demo margin note | `max-height` 0→120px, opacity 0→1 | 200ms |
| Demo diff rows | opacity 0→1 + `translateY` 4px→0, one row per 180ms | 160ms each |
| Demo verdict | opacity 0→1 | 200ms |
| Demo heading hairlines (DECLARED / READ / SIMULATION / VERDICT) | `scaleX` 0→1 once per case start, `transform-origin: left` | 300ms |
| "Sign anyway" hold bar | `::after` width 0→100% while pressed, linear | 1000ms |
| Links | `text-underline-offset` 2px→4px | 160ms |
| Primary button | background `--paper`→`--paper-hi`, no movement | 160ms |
| Ghost button | border `--rule-strong`→`--paper` | 160ms |
| Logo point | `translate(2px,-2px)` on wordmark-link hover | 200ms |
| FAQ caret | `rotate(180deg)`→`rotate(0)` on open | 200ms |
| Form success/error | content crossfade, opacity, same height reserved | 200ms |
| Tabs | underline moves by changing which tab has the 2px `--paper` bottom border; no sliding indicator | 0 |

Nothing else moves. Section headings do not fade in. Diagrams do not draw themselves. Numbers do not count up.

### 7.3 Reduced motion

A single media query at the end of the stylesheet:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 1ms !important; animation-delay: 0ms !important; transition-duration: 1ms !important; }
  .cursor { display: none !important; }
}
```

In JS, `matchMedia('(prefers-reduced-motion: reduce)').matches` means: do not register the IntersectionObserver; render the selected case in its final state immediately; tab changes swap content instantly; the hold-to-sign still requires the 1s hold (it is a safeguard, not a decoration) but shows no bar, only the note. The hero full stop is simply present.

---

## 8. Components

### 8.1 Buttons

- **Primary** (`.btn`): `--paper` fill, `--ink-0` text, Geist 500 14px, height 48px (36px in nav and demo toolbar), padding 0 20px, radius 4px, no border. Hover `--paper-hi`. Active: no transform; `--paper` again. Disabled: opacity .5, `cursor: not-allowed`. Used for: Join the waitlist (nav, hero, pricing ×3, waitlist), Reject / Revoke / Continue in the demo toolbar.
- **Ghost** (`.btn-ghost`): transparent, 1px `--rule-strong` border, `--paper` text; hover border `--paper`. Used for: Read again, Sign anyway (hold), Keep the approval.
- **Text link** (`.link`): `--paper`, `text-decoration: underline; text-decoration-color: var(--paper-3); text-underline-offset: 2px;` hover offset 4px and color `--paper`. Trailing arrow glyph `→` as text, not an icon.
- Focus (all): `outline: 2px solid var(--focus); outline-offset: 3px;` via `:focus-visible`. Never remove outlines.

### 8.2 Inputs

- Email/text: height 48px, `--ink-1` fill, 1px `--rule-strong` border, radius 4px, padding 0 14px, Geist 400 17px `--paper`, placeholder `--paper-3`. Focus: border `--paper`, plus the focus ring. Invalid (after submit attempt only, `aria-invalid="true"`): border `--pen`, the error line below in `--pen` 14px with `role="alert"`.
- Select (wallet): same chrome, native `<select>` with a caret glyph drawn as a background-free inline SVG next to it; `appearance: none`.
- Checkbox (Team): native checkbox, 18px, `accent-color: var(--paper)`; label Geist 400 14px `--paper-2`.
- Every field has a visible label (`--t-eyebrow`, mono) above it on the waitlist form; the hero form uses a visually hidden label plus placeholder "you@domain.sol".

### 8.3 Verdict chips

Inline, mono 12px uppercase tracking .08em, height 24px, padding 0 8px, radius 2px, always followed by the rule id in mono (`BLOCKED · R-021`):
- **BLOCKED**: `--pen` fill, `--ink-0` text. Pairs with a 2px solid `--pen` underline under the flagged argument.
- **CAUTION**: transparent, 1px `--pen` border, `--pen` text. Pairs with a 1px dotted `--pen` underline.
- **CLEAR**: transparent, 1px `--paper` border, `--paper` text. No underline anywhere.
The word is always present; color and weight never carry the state alone.

### 8.4 Ruled list

```html
<dl class="ruled">
  <div class="row"><dt class="mono">System.Assign</dt><dd>…</dd></div>
</dl>
```
Row: `grid-template-columns: 160px 1fr; column-gap: 24px; padding: 20px 0; border-top: 1px solid var(--rule);` last row also gets a bottom rule. Below 840px: `grid-template-columns: 1fr; row-gap: 6px`. The `dt` may carry a second mono line (rule id) in `--paper-3`.

### 8.5 Ledger table

`<table class="ledger">` with `<caption class="sr-only">`, `<thead>` cells in `--t-eyebrow`, `<th scope="row">` for the first column (Geist 400 15px `--paper`), body cells mono 13.5px `--paper-2`, `tabular-nums`, `border-top: 1px solid var(--rule)` on every row, 14px vertical padding, no vertical rules, no zebra. Sticky first column on mobile: `position: sticky; left: 0; background: var(--ink-0)` on the row header; the wrapper `.ledger-wrap { overflow-x: auto; }` with a visible 1px `--rule` right edge fade is not needed.

### 8.6 Code block

`<pre class="code"><code>` on `--ink-1`, 1px `--rule` border, radius 4px, padding 20px 24px, mono 13.5px/1.6, line numbers via `counter-increment` on `span.ln` in `--paper-3`, horizontal scroll inside the block only. No syntax colors. The `say:` line is `--paper`; everything else `--paper-2`. A mono header row above the code (`rules/R-021.rule` left, `Apache-2.0 · Q3 2027` right) in `--t-eyebrow`.

### 8.7 Details / summary (FAQ, mobile menu)

`<details class="faq-item">` with a hairline top border; `summary` is Geist 500 20px with the caret glyph at the right, `list-style: none` (and `::-webkit-details-marker { display: none }`); the answer has 12px top padding and 24px bottom padding. `summary` is keyboard-operable by default; add `cursor: pointer`.

### 8.8 Tabs (demo)

`<div role="tablist" aria-label="Recorded cases">` of five `<button role="tab" aria-selected aria-controls id tabindex>` with roving tabindex (only the selected tab is tabbable; arrow keys Left/Right move and activate; Home/End jump). Labels mono 13.5px `--paper-2`, selected `--paper` with a 2px `--paper` bottom border, hover `--ink-2` background. The tablist has a 1px `--rule` bottom border as the track. Below 600px the tablist scrolls horizontally with `scroll-snap-type: x mandatory`, `overflow-x: auto`, and 20px padding on the ends; the page never overflows.

### 8.9 Address span

`<span class="addr" title="7vfbPS4Dro8L7SavGjQjd3CpwyoFGS2aDgufVnu4JtQy">7vfb…JtQy</span>`: mono, `tabular-nums`, the ellipsis is U+2026, the full key in `title`. Program ids (System, Token, ComputeBudget, Jupiter v6, Memo, ATA) are shown in full inside expanded rows and the rules block; truncation is reserved for wallet and token-account addresses.

---

## 9. Page structure and section specs

### 9.1 Order, ids, numbers, running titles

| Order | id | Rule number | Running title (margin) | Headline |
|---|---|---|---|---|
| 0 | `nav` | — | — | GUARDIAN |
| 0 | `hero` (`#top`) | — | (eyebrow stack in the margin) | Nothing gets signed unread. |
| 1 | `reading` | 01 | A transaction, read aloud | A transaction, read aloud. |
| 2 | `threat` | 02 | The threat | Your wallet shows you a button. The chain executes the payload. |
| 3 | `how` | 03 | How it works | Three readings before the signature. One after. |
| 4 | `rules` | 04 | The rules | The rules are the product. Read them. |
| — | `act` | — | — | GUARDIAN never rejects a transaction. You do. |
| 5 | `trust` | 05 | Trust | What GUARDIAN can see, and what it can't. |
| 6 | `comparison` | 06 | Comparison | Where the wallet's warning stops. |
| 7 | `pricing` | 07 | Pricing | Pay in the unit you're protecting. |
| 8 | `roadmap` | 08 | Roadmap | What ships when. |
| 9 | `faq` | 09 | Questions | Questions a careful person asks. |
| 10 | `waitlist` | 10 | Waitlist | Join the next hundred. |
| — | `footer` | — | — | Non-custodial. Not a wallet. Never your keys. |

Headline casing is sentence case with a full stop, always. H2s are `<h2>`; the hero is the page's single `<h1>`; sub-blocks use `<h3>`. Heading levels never skip.

### 9.2 Nav

Specified in §6.5. Copy: **How it works · Trust · Pricing · Rules · [Join the waitlist]** · status `Rules v0.4 · 61 rules` · mobile `Menu`.

### 9.3 Hero (`#hero`, also `#top`)

**Purpose.** State the product in one sentence, answer custody before the first scroll, and get the reader to the demo.

**Layout.** Manuscript grid. Top padding 96px desktop (not 128: the demo's tab strip must be visible within 900px of viewport height at 1440px wide), 64px mobile. On 1024+ the margin column (cols 1–3) holds the eyebrow stack, top-aligned with the H1's cap line; the H1 spans cols 4–11; the lead, form, proof line and custody strip span cols 4–12. Below 1024 the eyebrow becomes a single line above the H1. At 320px the sentence runs three lines at 42px.

**Copy.**
- Eyebrow (mono, `--paper-3`), desktop as three short lines then a gap then two: `NON-CUSTODIAL` / `DEFENSE AGENT` / `FOR SOLANA` · `PRIVATE BETA` / `100 WALLETS`. Mobile single line: `NON-CUSTODIAL DEFENSE AGENT FOR SOLANA · PRIVATE BETA · 100 WALLETS`.
- H1: `Nothing gets signed unread` + `<span class="stop">.</span>` — the full stop is set in `--pen`. It is the only red pixel above the fold.
- Lead (21px, `--paper-2`, max 56ch): **GUARDIAN decodes and simulates every Solana transaction before you sign, compares what the page says with what the payload does, and tells you in one sentence when they disagree. It never sees your keys.** (34 words. Do not lengthen it.)
- Form (single row at 600+, stacked below): email input (placeholder `you@domain.sol`, visually hidden label "Email") + primary button **Join the waitlist**. Honeypot field (§12). Inline error/success under the row, height reserved (24px).
- Proof line (14px, `--paper-3`, 12px under the form): **Phantom, Solflare, Backpack · Free tier stays free · One email, when your wallet is up.**
- Custody strip, 32px under the proof line: a ruled row (1px `--rule` top and bottom) of five mono key/value cells separated by 1px `--rule` vertical dividers on 840+, a 2-column grid with hairline rows below (the fifth cell spans both columns). Keys in `--t-eyebrow` `--paper-3`, values mono 13.5px `--paper`:
  `KEYS TOUCHED` → `0` · `DATA READ` → `public on-chain only` · `SIMULATION` → `your machine, your RPC` · `RULES` → `Apache-2.0, Q3 2027` · `EXECUTION` → `TEE-attested`
- Then the section-01 rule with the number `01` and the demo begins. The first scroll reveals proof, not features.

**Interaction.** Only the full stop moves (opacity, 400ms, 200ms after paint). No canvas, no gradient, no particles. The form behaves per §12.

### 9.4 Section 01 — The Reading (`#reading`)

**Purpose.** Show the product doing the thing, on realistic data, including a case where it says yes and a case where it acts after the signature.

**Layout.** Rule + `01`. Headline cols 4–11; intro lead; then the panel full width (cols 4–12) with the tablist above it; then the caption; then the verdict-definitions ruled list.

**Copy.**
- H2: **A transaction, read aloud.**
- Intro (lead): **Five shapes of transaction, replayed from the beta fixtures. Left is what the page and the wallet told the user. Right is what GUARDIAN read in the payload.**
- Tabs (mono): `Swap · lookalike Jupiter` · `Airdrop claim` · `Unlimited approval` · `After the signature` · `Swap · jup.ag`
- Caption under the panel (mono 12.5px, `--paper-3`): **Replayed from beta fixtures · build 0.4 · addresses are fixture keys, not live accounts · full keys in the rule repository test fixtures.**
- Verdict definitions (ruled list, mono label = chip):
  - `BLOCKED` — A match against a malicious-address list, or an undeclared instruction that changes ownership, authority or delegation. The wallet still asks you to sign.
  - `CAUTION` — A reversible but undeclared change, an unlimited approval, or a counterparty with no history. Whatever you proceed with, GUARDIAN keeps watching.
  - `CLEAR` — The payload matches the declared intent, every program is verified, no authority or delegate changes. A Clear verdict is a statement about the payload, not about the token you are buying.

**Interaction.** The full specification, with data, is §10.

### 9.5 Section 02 — The threat (`#threat`)

**Purpose.** Explain the gap between declared intent and payload with the specific instructions attackers use, so a technical reader nods.

**Layout.** Rule + `02`. H2 cols 4–11. Lead in two columns at 1024+ (21px). Then H3 + a six-row ruled list (mono label column holds the instruction name on line one and the rule id on line two in `--paper-3`). Then the closing line as a 24px Geist 500 paragraph. Then the "Declared vs. actual" diagram (§11.1), full width.

**Copy.**
- H2: **Your wallet shows you a button. The chain executes the payload.**
- Lead: **A Solana transaction is a list of instructions. The page shows you a button. Your wallet shows you a summary. Neither one is the payload, and drainers live in that gap. In 2024, wallet drainers took roughly $494M across chains (ScamSniffer, 2024 annual report). Every one of those transactions was signed by its victim.** (VERIFY the figure against the published report before launch.)
- H3: **Six instructions that empty wallets**
- Rows:
  1. `System.Assign` / `R-014` — Hands ownership of your wallet account to another program. Dressed up as "Claim airdrop".
  2. `Token.SetAuthority` / `R-021` — Changes who owns a token account, or who can mint. Dressed up as "Swap".
  3. `Token.Approve` `amount: 18446744073709551615` / `R-003` — An unlimited delegate: that number is `u64::MAX`. Dressed up as "Enable trading". Drained later, when you have stopped paying attention.
  4. `Token.CloseAccount` `destination ≠ you` / `R-008` — Closes a token account and sends the balance and the rent to someone else. Dressed up as "Reclaim rent from empty accounts".
  5. `Durable nonce` `delayed broadcast` / `R-033` — A transaction you signed in March, broadcast in June, when the balance is worth taking. Dressed up as "Verify wallet ownership".
  6. `Lookalike origin` `real route` / `R-050` — A real Jupiter route built by `jup-ag.app` instead of `jup.ag`, with one instruction appended at the end. Dressed up as the site you meant to visit.
- Closing line: **None of these need your seed phrase. They need your signature, once.**

### 9.6 Section 03 — How it works (`#how`)

**Purpose.** The three layers, each tied to a concrete mechanism, a spec list, and a sample of what the user actually sees.

**Layout.** Rule + `03`. H2. A vertical ruled stack of three blocks; each block is a grid at 1024+: mono numeral column (`I`, `II`, `III`, 160px) and a text column holding H3, body (62ch), a two-column mono spec list (`Input / Output / Latency / Runs`, labels `--paper-3`, values `--paper-2`, 1px `--rule` between rows), and a "what you see" sample: a mono block on `--ink-1`, 1px `--rule`, radius 4px, 14px padding. Then the sequence diagram (§11.2) full width.

**Copy.**
- H2: **Three readings before the signature. One after.**
- **I. Simulate and diff.** Body: **GUARDIAN decodes the unsigned transaction instruction by instruction and runs `simulateTransaction` on the RPC you configure, with signature verification off and the blockhash replaced, so the result reflects the chain as it is now, not a third party's summary. It records every balance change, every authority change, every account closed or assigned, then diffs that against the declared intent. If the page says "Swap" and the simulation shows your USDC account changing owner, the verdict is Blocked, with the instruction number and the rule that fired.**
  Spec: `Input` unsigned transaction + page origin · `Output` effect list, intent diff, rule hits · `Latency` p50 under 400 ms, beta measurement · `Runs` your machine (decode, simulate) · agent in TEE (diff)
  Sample: `expected  SOL −12.5 · USDC +2,431.18` / `observed  SOL −12.5 · USDC account owner → 3kvc…rmjA`
- **II. Match against intel.** Body: **Every counterparty address, program and origin is checked against the SlowMist malicious-address database, public STRIDE findings and a crowdsourced phishing-domain list refreshed every ten minutes. A program's age, verified source and upgrade authority are scored too, so a three-hour-old program with no source is flagged before anyone has reported it. A match explains itself: who flagged it, when, and how many reports.**
  Spec: `Input` counterparties from reading I · `Output` match, provenance, report count · `Latency` under 120 ms · lists cached 24 h · `Runs` agent in TEE · cached lists on your machine
  Sample: `3kvc…rmjA · SlowMist · 2026-09-14 · drainer · 212 reports`
- **III. Watch after the signature.** Body: **Approvals outlive the click. GUARDIAN keeps an index of every delegate and authority you have granted and alerts you on Telegram or email when one moves funds, grows, or appears on a list. Each alert carries a one-tap link that builds the Revoke instruction. You sign it. GUARDIAN never can.**
  Spec: `Input` your public account state · `Output` alert + prepared revoke transaction · `Latency` within one slot cycle, about 2 s target · `Runs` agent in TEE · public RPC reads only
  Sample: `Delegate B49K…wkS4 on your USDC moved 1,250.00 USDC at 14:02 UTC.` / `Revoke → guardian.sh/r/7vfb…JtQy`

### 9.7 Section 04 — The rules (`#rules`)

**Purpose.** Make the open-source promise tangible with the rule that produced case 1's verdict, so the demo and the rules visibly link.

**Layout.** Rule + `04`. H2, lead, the code block (§8.6) with header `rules/R-021.rule` · `Apache-2.0 · Q3 2027`, a text link, a mono note.

**Copy.**
- H2: **The rules are the product. Read them.**
- Lead: **A detection engine you cannot read is a detection engine you have to trust. The rule below is the one that blocked case 1 above. Every rule has a severity, a condition on the decoded instruction, and the sentence the user sees. Sixty-one rules ship with build 0.4. They go public under Apache-2.0 in Q3 2027, with the fixtures behind the demo.** (VERIFY: 61.)
- Code (line numbers 1–11):
```
id: R-021
name: token.set_authority.to_unknown
severity: block
when:
  program: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
  instruction: SetAuthority
  authority_type: AccountOwner
  new_authority: not_in [signer, verified_programs, user_known]
say: "Instruction {index} hands your {mint} account to {new_authority}."
tests: fixtures/R-021/set_authority_drainer.json
# 23 cases · 0 false positives on the beta corpus
```
  (VERIFY: 23 cases / 0 false positives.)
- Link: **Browse the rules and fixtures →** — `href` is the public repository URL (VERIFY). If no public URL exists at launch, omit the link entirely; never point it at `#` or at the waitlist.
- Note (mono, `--paper-3`): **Bug bounty terms publish with the Q3 2027 release.**

### 9.8 Sparse act (`#act`)

One line, Newsreader 450 at `--t-h2`, left-aligned on cols 4–11, 160px of air above and below (96px mobile), no rule, no number, no eyebrow:

**GUARDIAN never rejects a transaction. You do.**

### 9.9 Section 05 — Trust (`#trust`)

**Purpose.** Pre-empt the skeptic's questions about custody, keys and infrastructure with a ledger of what the product can and cannot do, and one unambiguous data-path paragraph.

**Layout.** Rule + `05`. H2. Two-column ledger table (Can / Cannot), hairline rows, mono column heads; on mobile the two columns stack as two ruled lists with the heads as eyebrows. Then four ruled facts (mono label column). Then the data-path diagram (§11.3) full width.

**Copy.**
- H2: **What GUARDIAN can see, and what it can't.**
- `CAN`: Read your public address and on-chain state. · Decode and simulate the unsigned transaction your wallet is about to display. · Prepare a Revoke transaction for you to sign. · Send the alerts you asked for, to the channel you chose.
- `CANNOT`: Read your seed phrase or private key. There is no field for it and no code path to it. · Sign, submit, modify or delay a transaction. · Move funds. · Stop you. The final decision is always yours; a Blocked verdict is evidence, not a lock. · See a program's future upgrade. A verified program can turn malicious after an upgrade, which is why GUARDIAN keeps watching after the signature.
- Facts:
  - `DATA PATH` — **Decoding and simulation happen on your machine, against the RPC you configure. The decoded transaction and its simulated effects, never a key, go to the agent, which runs inside a trusted execution environment and returns the verdict with its rule id. If the agent is unreachable, your wallet behaves as before and shows an "unverified" state. Fail-open is deliberate.**
  - `TEE` — **Each release publishes an attestation you can verify against the binary, so the code that read your transaction is the code that was published, and nobody can change it silently, GUARDIAN's operators included.**
  - `OPEN RULES` — **The detection rules and the decoder ship under Apache-2.0 in Q3 2027. The intent-diff grammar and the fixtures behind the demo above are public from the first release. The intel feeds and the TEE build are published as attestation reports, not source.**
  - `NOT A WALLET` — **GUARDIAN is an adapter for Phantom, Solflare and Backpack. Your wallet stays your wallet, your keys stay where they are. Remove it and your wallet works exactly as before.**

### 9.10 Section 06 — Comparison (`#comparison`)

**Purpose.** Position against what the reader already has, without naming competitors.

**Layout.** Rule + `06`. H2. One ledger table, four columns: capability (row header) · `Built-in wallet warnings` · `Hosted screening APIs` · `GUARDIAN`. Cells mono: `yes`, `partial¹`, `—`, `Q3 2027`. Sticky first column with horizontal scroll inside the table on mobile. Footnotes and the closing lines in `--t-small`.

**Copy.**
- H2: **Where the wallet's warning stops.**
- Rows:
  - Decodes every instruction — `partial¹` · `yes` · `yes`
  - Simulates on your machine, against your RPC — `—` · `—` · `yes`
  - Diffs declared intent against the payload — `—` · `—` · `yes`
  - Threat intel with the provenance shown — `partial²` · `yes` · `yes`
  - Watches approvals after signing — `—` · `—` · `yes`
  - One-tap revoke links — `—` · `—` · `yes`
  - Rules you can read — `—` · `—` · `Q3 2027`
  - Runs in a TEE with published attestations — `—` · `—` · `yes`
- Footnotes: **¹ For some transaction types. ² A label, without the source or the date.**
- Closing: **Keep your wallet warnings on. GUARDIAN runs in addition to them, not instead of them. Wallet teams ship good warnings; GUARDIAN is the second reader.**

### 9.11 Section 07 — Pricing (`#pricing`)

**Purpose.** Three tiers as one table, priced in the unit being protected.

**Layout.** Rule + `07`. H2. One ledger table: the header row holds the tier names in Newsreader 500 32px with the price beneath in mono 13.5px `--paper-2`; ten feature rows (row header Geist 15px, cells mono); a final row with a primary button in each column. On mobile (<840) the table becomes three stacked ruled lists (tier head, then rows as `label · value`), no borders, hairlines only; buttons at the end of each list. Footnotes under the table in `--t-small` `--paper-3`, max 62ch.

**Copy.**
- H2: **Pay in the unit you're protecting.**
- Heads: **Free** / `0 SOL` · **Pro** / `0.1 SOL per month` · **Team** / `custom`
- Rows:
  - Simulation and decoded instruction list — `yes` · `yes` · `yes`
  - Known-malicious matching (SlowMist, phishing domains) — `yes` · `yes` · `yes`
  - Intent diff with rule ids — `—` · `yes` · `yes`
  - Real-time approval monitoring — `—` · `yes` · `yes`
  - Anomalous-approval alerts — `—` · `yes` · `yes`
  - Intel feed refresh — `24 h` · `10 min` · `dedicated feed`
  - Alerts — `email` · `Telegram, email, revoke links` · `+ webhooks`
  - Wallets — `1` · `3` · `unlimited`
  - Verdict API — `—` · `—` · `yes`
  - Support — `community` · `48 h` · `priority`
- Buttons: **Join the waitlist** ×3. The Team button links to `#waitlist` and ticks the Team checkbox (`href="#waitlist"` plus `data-team="1"`; three lines of JS).
- Footnotes: **Prices in SOL because the thing you are protecting is in SOL. Billed on-chain, from the protected wallet. No card: a card form on a security product is a phishing vector. Cancel by not paying. Free stays free after the beta. Beta wallets get Pro free until Q2 2027. No GUARDIAN token. There will not be one.**

### 9.12 Section 08 — Roadmap (`#roadmap`)

**Purpose.** Show the plan as dates, not promises.

**Layout.** Rule + `08`. H2. The timeline: a single horizontal 1px `--rule-strong` line spanning cols 4–12 with three ticks (6px vertical, `--paper-3`) at 0%, 50%, 100% and a `--paper` 8px square marker labeled `you are here` (mono, `--paper`) on the first segment at ~12%; above each tick a mono quarter label, below it a short ruled list with status glyphs. On mobile the line becomes vertical on the left (24px from the gutter), ticks become horizontal, columns stack. Status glyphs are text in mono with visually hidden labels: `■` shipped, `◧` in progress, `□` planned. A caption at the end in `--t-small`.

**Copy.**
- H2: **What ships when.**
- Tick 1 label: `NOW → Q1 2027 · CLOSED BETA` — `■ Simulation engine` · `■ Base intel: SlowMist, public STRIDE findings, phishing domains` · `◧ Intent diff with rule ids` · `■ 100 wallets onboarded` · marker: `you are here`
- Tick 2 label: `Q2 2027 · MONITORING` — `□ Real-time approval monitoring` · `□ Telegram and email alerts with revoke links` · `□ Phantom, Solflare and Backpack adapters` · `□ Pro opens`
- Tick 3 label: `Q3 2027 · OPEN` — `□ Rules and decoder under Apache-2.0` · `□ Bug bounty` · `□ Sui and Eclipse`
- Caption: **Updated 2026-10-20. Dates are targets, not promises. This page changes when they slip.**
- VERIFY: the client's roadmap gave quarters without years; 2027 is inferred from today's date and the "private beta now" status. If the client means other calendar quarters, change the three labels and the pricing/rules/trust mentions of `Q2 2027` and `Q3 2027` (search the file for `2027`).

### 9.13 Section 09 — Questions (`#faq`)

**Purpose.** Answer the objections a DeFi-native reader has already formed.

**Layout.** Rule + `09`. H2. Ten `details/summary` rows (§8.7), single column, max-width 760px within cols 4–12. No JS.

**Copy.**
1. **Does GUARDIAN need my seed phrase?** — No. It never asks and has no field for it. It reads the unsigned transaction your wallet is about to display and the public state of the chain.
2. **Can it block a transaction without my consent?** — No. It shows a verdict with evidence; your wallet still asks you to sign. Blocked is advice, not a lock.
3. **What happens if the service is down?** — Fail-open is deliberate: your wallet behaves as before and shows an "unverified" state. Known-malicious matching keeps working from lists cached on your machine for 24 hours. You lose freshness, not your wallet.
4. **Why a TEE?** — So the agent that sees your pending transactions cannot be modified silently, by anyone. Each release publishes an attestation you can verify against the binary.
5. **What exactly is open source?** — The rule set and the decoder, under Apache-2.0 from Q3 2027. The intel feeds and the TEE build ship as attestation reports, not source, so an attacker cannot test against the exact matching logic.
6. **What if GUARDIAN is wrong?** — You override with a one-line reason. The override is logged and becomes a test fixture, so the rule gets a counter-example and false positives go down for everyone.
7. **Which wallets?** — Phantom, Solflare and Backpack adapters ship in Q2 2027. Any wallet that exposes the unsigned transaction can be supported.
8. **Does it slow down signing?** — Simulation adds 180–400 ms in the beta build. The verdict renders before the wallet modal finishes animating. (VERIFY the range.)
9. **Why 0.1 SOL and not dollars?** — Because what you are protecting is denominated in SOL, and because a card form on a security product is a phishing vector we would rather not create. Billed on-chain from the protected wallet; cancel by not paying.
10. **Is there a token?** — No. There will not be one. A security product that depends on its own token price has the wrong incentives.

### 9.14 Section 10 — Waitlist (`#waitlist`)

**Purpose.** The single conversion point, repeated from the hero with more room.

**Layout.** Rule + `10`. Centered block, max-width 560px: H2, one paragraph, the form (email, wallet select, Team checkbox, button), the privacy line. Success and error states replace the form in place with the same reserved height (`min-height` on the form wrapper).

**Copy.**
- H2: **Join the next hundred.**
- Body: **We add wallets in batches of 100. Leave an address; we tell you when yours is up, and nothing else.**
- Fields: `EMAIL` [input, placeholder `you@domain.sol`] · `WALLET` [select: Phantom / Solflare / Backpack / Other] · `[ ] I'm asking for a team` · button **Join the waitlist**
- Privacy line (14px, `--paper-3`): **One email when your batch opens. No newsletter. Addresses are deleted when you join or when you ask.**
- Success (replaces the form): **You're on the list. We'll write once.**
- Error (email): **That doesn't look like an email address. Check for a stray space.**
- Error (network): **Could not reach the waitlist. Nothing was saved. Try again, or write to hello@guardian.sh.** (VERIFY address.)

### 9.15 Footer (`#footer`)

**Purpose.** Close with the brand's three-line promise, the notice a security-minded reader wants, and the colophon.

**Layout.** Hairline above. Three columns at 840+ (lockup + promise · product links · legal), stacked below. 14px text, `--paper-3`; links `--paper-2`. The notice spans the full width below the columns, then the colophon in mono 12px centered.

**Copy.**
- Column 1: stacked lockup (mark 28px, wordmark 16px), then **Non-custodial. Not a wallet. Never your keys.**
- Column 2 (`PRODUCT`): Rules (GitHub) · Attestations · Status · Docs · Telegram · X (VERIFY all hrefs; omit any link that has no destination rather than linking `#`).
- Column 3 (`LEGAL`): Privacy · Terms · Security disclosure: `security@guardian.sh` (VERIFY).
- Notice (full width, Geist 14px `--paper-2`): **GUARDIAN never asks for a seed phrase or private key. If something claiming to be GUARDIAN does, it is not GUARDIAN.**
- Legal line: **A Clear verdict describes a payload, not an investment.**
- Colophon (mono 12px, centered): **Set in Newsreader, Geist and Geist Mono. Rules under Apache-2.0. Rules v0.4 · 61 rules · slot 441,906,318 · Updated 2026-10-20. © 2026 GUARDIAN.** (VERIFY slot: replace with the slot of the newest fixture.)

---

## 10. The signature interaction: "The Reading"

### 10.1 What it is

A verdict transcript that reads a transaction row by row and marks the line that lies. It is the first thing after the hero and the only choreographed element on the page. Five recorded cases. One `setTimeout` chain. CSS transitions driven by class toggles. No `requestAnimationFrame`, no canvas, no network.

### 10.2 Structure

```html
<section id="reading" class="sec">
  …rule, margin, h2, intro…
  <div role="tablist" aria-label="Recorded cases" class="tabs">
    <button role="tab" id="tab-a" aria-selected="true" aria-controls="panel" tabindex="0">Swap · lookalike Jupiter</button>
    <button role="tab" id="tab-b" aria-selected="false" aria-controls="panel" tabindex="-1">Airdrop claim</button>
    <button role="tab" id="tab-c" …>Unlimited approval</button>
    <button role="tab" id="tab-d" …>After the signature</button>
    <button role="tab" id="tab-e" …>Swap · jup.ag</button>
  </div>
  <div id="panel" role="tabpanel" aria-labelledby="tab-a" class="panel" data-state="idle">
    <div class="declared">  <h3 class="eyebrow">DECLARED</h3> …  </div>   <!-- or ALERT in case D -->
    <div class="read">      <h3 class="eyebrow">READ</h3> <ol class="rows">…</ol> <div class="cursor" aria-hidden="true"><caret/></div> </div>   <!-- or APPROVALS INDEX in case D -->
    <div class="sim">       <h3 class="eyebrow">SIMULATION</h3> <table>…</table> </div>   <!-- or REVOKE, PREPARED in case D -->
    <div class="verdict" aria-live="polite" aria-atomic="true"> <span class="chip">…</span> <span class="rule-id">…</span> <p>…</p> </div>
    <div class="toolbar"> <button class="btn">…</button> <button class="btn-ghost hold">…</button> <button class="btn-ghost again">Read again</button> <span class="note mono" role="status"></span> </div>
  </div>
  <p class="caption mono">Replayed from beta fixtures · build 0.4 · …</p>
  …verdict definitions…
</section>
```

Panel: `--ink-1` background, 1px `--rule` border, radius 4px, padding 24px (16px under 600px). `min-height: 560px` at 840+, `760px` below, so no case changes the page height (the Reading never shifts layout). Inside, four regions: DECLARED and READ side by side in a 5/7 column split at 840+ (gap 32px), stacked below; SIMULATION and VERDICT full width beneath; the toolbar last. Each region heading is a mono eyebrow with a 1px `--rule` hairline under it that draws in (`scaleX`) once per case start.

**DECLARED** (what the user saw): a definition list in mono 13.5px:
`origin` → domain (plus a `--paper-3` note where listed) · `button` → the page's button rendered as a 44px-tall fake button outline (1px `--rule-strong`, radius 4px, Geist 500 14px, non-interactive, `aria-hidden`) · `wallet said` → the wallet's own summary line · `signer` → address span.

**READ** (what GUARDIAN read): an `<ol class="rows">` of instruction rows. Each row is a `<li>` containing a `<button aria-expanded="false" aria-controls="x-i">` that spans the row: grid `28px 1fr 96px` (index · body · status), the body holding line one `Program.Instruction` (mono 13.5px `--paper`) and line two the arguments (mono 13.5px `--paper-2`, wraps). The status cell (right, `text-align: right`) is empty in idle. Under the button an `<div id="x-i" class="inset" hidden>` lists the program id in full and the accounts with flags (mono 12.5px on `--ink-2`, 12px padding). Rows are separated by 1px `--rule`. The flagged argument is wrapped in `<span class="flag">…</span>` whose `::after` is the pen underline (2px solid for blocked, 1px dotted for caution, `transform: scaleX(0)`, `transform-origin: left`). Under a flagged row, a `<div class="margin-note">` (mono 12.5px, `--pen` on `--pen-wash`, 10px 12px padding, `max-height: 0; overflow: hidden; opacity: 0`).

**The cursor**: `<div class="cursor">` absolutely positioned inside `.read`, width 100%, a 1px `--paper` rule with the caret (14px, `--paper`) at its left end sitting on top of the rule; `transform: translateY(var(--y))`; `transition: transform 200ms var(--ease)`. It sits at the top edge of the current row. `display: none` in idle and after the verdict, and always under reduced motion.

**SIMULATION**: a 3-column ledger (`asset · expected · observed`; case D uses `field · before · after`) plus an `authority` row where listed. Rows start `opacity: 0; transform: translateY(4px)`; heights are reserved (`visibility` not `display`), so nothing shifts. The observed cell that disagrees is set in `--pen`.

**VERDICT**: the chip (§8.3) + rule id + one sentence (Geist 17px, `--paper`), `opacity: 0` until state 3. `aria-live="polite"` on this region only, so screen readers hear the sentence and not the row-by-row churn.

**Toolbar**: per case (table in §10.6). Always ends with **Read again** (ghost) and a mono `role="status"` note span (empty until a demo button is used).

### 10.3 States and timing

| State | What happens | Timing |
|---|---|---|
| 0 idle | Rows at `opacity: .35`, status cells empty, underlines at `scaleX(0)`, margin notes collapsed, simulation rows invisible, verdict invisible, cursor hidden, toolbar visible but the primary/hold buttons `disabled` | — |
| 1 reading | Starts once, when 40% of the panel is visible (`IntersectionObserver`, threshold .4), after 600ms. Heading hairlines draw (300ms). Cursor appears at row 1's top edge. For each row: cursor moves (`translateY`, 200ms), the row goes to `opacity: 1` (160ms) on arrival, dwell 380ms, then the status cell paints. OK rows: `✓` in `--paper-2` + a 12.5px mono note (e.g. `expected`). Flagged rows: the underline draws (240ms), the row background becomes `--pen-wash` (160ms), the status cell shows `blocked` or `caution` in `--pen` mono, and the margin note expands (200ms). | 580ms per row |
| 2 simulating | 300ms after the last status paints, the cursor hides and the diff rows appear one per 180ms (opacity + 4px rise, 160ms). | 300 + 180×n |
| 3 verdict | 300ms after the last diff row: chip, rule id and sentence fade in (200ms); the toolbar's buttons enable. `data-state="done"`. | 300 + 200 |

Totals (600ms start delay + 580ms per row + 300 + 180 per diff row + 300 + 200): case A ≈ 4.3s, B ≈ 3.1s, C ≈ 2.9s, D ≈ 3.7s, E ≈ 5.6s. Constant reading speed is part of the calm: the CLEAR case is not read faster.

### 10.4 Controls

- Clicking a tab: cancel the chain, swap the panel's content (all five cases are pre-rendered in the DOM; only the active one is `display: block`, others `hidden`; this keeps the JS to toggling), reset to idle with transitions disabled for one frame (`.no-transition` class, removed on the next `requestAnimationFrame` callback — the single allowed rAF call, not a loop), then start state 1 after 120ms (no 600ms delay). `aria-selected` and `tabindex` update; the panel's `aria-labelledby` points at the active tab.
- Arrow Left/Right move between tabs and activate; Home/End jump; focus follows.
- **Read again**: same as clicking the active tab.
- **Pause**: while any row is expanded (`aria-expanded="true"`) or focus is inside `.read`, the chain pauses (clear the pending timeout, remember the step index); it resumes 1.5s after the last row collapses and focus leaves. Plain hover does not pause: a pointer resting on the panel while scrolling must not freeze it.
- **Row expansion**: click/Enter/Space toggles `aria-expanded` and `hidden` on the inset. Multiple rows may be open.
- **Demo buttons** (primary / hold): on use, the toolbar note shows for 4s then clears: see §10.6 for the text per case. The hold button needs a continuous 1000ms `pointerdown` (or Space/Enter keydown without keyup); releasing early resets the bar with no note. These buttons never navigate and never submit anything.
- Visibility: on `document.hidden`, pause; resume on visible. On tab (page) switch the chain is cancelled, never left running.

### 10.5 Accessibility and reduced motion

- Tabs: roving tabindex, `aria-selected`, `aria-controls`; panel `role="tabpanel"`.
- Rows: real `<button>`s with `aria-expanded`; the status cell text (`✓ expected`, `blocked`) is in the DOM as text, so the final state is readable without color.
- The cursor and the caret are `aria-hidden`. The fake "button" in DECLARED is `aria-hidden` and non-focusable, with an `sr-only` text "the page's button label: Swap".
- The verdict region is the only live region. The toolbar note uses `role="status"`.
- Reduced motion: no observer; the selected case renders in its final state at once; tab switches are instant; the cursor is never shown; the hold button shows no bar but still requires the hold.
- Every address span carries the full key in `title`; every program row's inset carries the full program id as text.

### 10.6 Data (verbatim; paste as the JS object)

Fixture keys. These are generated fixture keys for the demo (valid base58, 32-byte, not live accounts). Replace with the real fixture keys when the rule repository publishes; the truncations on the page are derived from these.

```js
const KEYS = {
  you:      "7vfbPS4Dro8L7SavGjQjd3CpwyoFGS2aDgufVnu4JtQy", // 7vfb…JtQy  your wallet (signer)
  yourUsdc: "EMhrmyE8Dh1jhwsUpq5irLjS4TJcFgr1WGCyaow4w3BW", // EMhr…w3BW  your USDC token account
  yourWsol: "ErdTDAc9UWqKQ73zGUeDHcxfByBNS5JgNxr8gqECoH6w", // ErdT…oH6w  your wSOL token account (case E)
  drainer:  "3kvcMxEvn847ybfqd8X5srMEzoL6DFMuNbyURiX4rmjA", // 3kvc…rmjA  new_authority in case A
  claimPrg: "Cfk2Q5AUQhwKqoJ8YjQsQQusLGW7qU5ihowe9JobABzW", // Cfk2…ABzW  three-hour-old program, case B
  delegate: "B49KpszWVuN2V1J7mZaKVt5KYJLownRcXyYBYMvkwkS4", // B49K…wkS4  delegate, cases C and D
};
const PROGRAMS = { // public constants; VERIFY against the Solana docs before launch
  system:        "11111111111111111111111111111111",
  token:         "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
  ata:           "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
  computeBudget: "ComputeBudget111111111111111111111111111111",
  memo:          "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",
  jupiterV6:     "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
  usdcMint:      "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  wsolMint:      "So11111111111111111111111111111111111111112",
};
```

Rule registry used on the page (ids are stable; names appear in the rules section and the threat list):

| id | name | severity |
|---|---|---|
| R-003 | token.approve.unbounded_to_unknown | caution |
| R-008 | token.close_account.destination_not_signer | block |
| R-014 | system.assign.to_unknown_owner | block |
| R-021 | token.set_authority.to_unknown | block |
| R-033 | nonce.durable.authority_not_signer | block |
| R-041 | counterparty.on_malicious_list | block (caution when raised after signature) |
| R-050 | origin.lookalike_of_known_domain | block |

#### CASE A — tab `Swap · lookalike Jupiter` (`id: lookalike-swap`)

DECLARED: `origin` `jup-ag.app` · `button` `Swap` · `wallet said` `Swap 12.5 SOL → ~2,431 USDC` · `signer` `7vfb…JtQy`

READ rows:
1. `ComputeBudget.SetComputeUnitLimit` — `units: 200,000` — ✓ `expected` — inset: program `ComputeBudget111111111111111111111111111111` · accounts: none
2. `ComputeBudget.SetComputeUnitPrice` — `5,000 µlamports per unit` — ✓ `expected` — inset: same program · accounts: none
3. `Jupiter v6.sharedAccountsRoute` — `in: 12.5 SOL · min out: 2,419.02 USDC · via Orca Whirlpool` — ✓ `program verified · route matches the quote` — inset: program `JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4` · accounts (31, showing 4): `7vfb…JtQy user transfer authority · signer` / `ErdT…oH6w source token account · writable` / `EMhr…w3BW destination token account · writable` / `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA token program`
4. `Token.SetAuthority` — `account: EMhr…w3BW (your USDC) · authority_type: AccountOwner · new_authority: ` **`3kvc…rmjA`** (flag span, blocked underline) — `blocked` — margin note: `R-021 · 3kvc…rmjA · SlowMist malicious-address DB · added 2026-09-14 · drainer · 212 reports` — inset: program `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` · accounts: `EMhr…w3BW token account (yours) · writable` / `7vfb…JtQy current owner · signer` · data: `authority_type = 2 (AccountOwner) · new_authority = 3kvc…rmjA`

SIMULATION (`asset · expected · observed`):
- `SOL` · `−12.5` · `−12.5`
- `USDC` · `+2,431.18` · **`+2,431.18 · into an account no longer yours`** (pen)
- `authority · USDC account owner` · `you` · **`3kvc…rmjA`** (pen)

VERDICT: `BLOCKED` · `R-021` (also `R-041 · R-050`, shown after the primary id in `--paper-3`) — **Instruction 4 hands your USDC account to a flagged address. The swap pays out into an account that is no longer yours.**

Toolbar: **Reject** (primary) · **Sign anyway** `hold 1 s` (ghost, hold) · **Read again**. Notes: Reject → `Demo · in the extension this returns your decision to the wallet. Nothing was sent.` Hold complete → `Override logged with your reason · it becomes fixture R-021/override_001.json`.

#### CASE B — tab `Airdrop claim` (`id: airdrop-assign`)

DECLARED: `origin` `claim-jto-season3.xyz` · `button` `Claim 1,400 JTO` · `wallet said` `Interact with program Cfk2…ABzW` · `signer` `7vfb…JtQy`

READ rows:
1. `Memo` — `"Season 3 rewards"` — ✓ `no effect` — inset: program `MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr` · accounts: `7vfb…JtQy · signer`
2. `System.Assign` — `account: 7vfb…JtQy (your wallet) · owner: ` **`Cfk2…ABzW`** (blocked underline) — `blocked` — margin note: `R-014 · Cfk2…ABzW · deployed 3 h ago · no verified source · upgrade authority live · Assign makes it the owner of your wallet account` — inset: program `11111111111111111111111111111111` · accounts: `7vfb…JtQy assigned account · signer · writable` · data: `owner = Cfk2…ABzW`

SIMULATION:
- `SOL` · `−0.000005 (fee)` · `−0.000005`
- `JTO` · `+1,400` · **`+0`** (pen)
- `authority · wallet owner` · `System Program` · **`Cfk2…ABzW`** (pen)

VERDICT: `BLOCKED` · `R-014` — **Instruction 2 gives a three-hour-old program ownership of your wallet. No airdrop pays out.**

Toolbar: as case A.

#### CASE C — tab `Unlimited approval` (`id: unlimited-approve`)

DECLARED: `origin` `trade.finance-dex.io` · `button` `Enable USDC` · `wallet said` `Approve USDC` · `signer` `7vfb…JtQy`

READ rows:
1. `ComputeBudget.SetComputeUnitLimit` — `units: 50,000` — ✓ `expected`
2. `Token.Approve` — `account: EMhr…w3BW (your USDC) · delegate: B49K…wkS4 · amount: ` **`18446744073709551615`** (caution underline, dotted) — `caution` — margin note: `R-003 · amount = u64::MAX, unlimited · delegate is a wallet, not a program · 2 transactions on record · no list match` — inset: program `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` · accounts: `EMhr…w3BW token account (yours) · writable` / `B49K…wkS4 delegate` / `7vfb…JtQy owner · signer` · data: `amount = 18446744073709551615 (u64::MAX)`

SIMULATION:
- `USDC` · `0` · `0`
- `delegate` · `none` · **`B49K…wkS4 · up to the full balance`** (pen)

VERDICT: `CAUTION` · `R-003` — **Unlimited delegate to an unknown wallet. If you proceed, GUARDIAN watches it and keeps a revoke link ready.**

Toolbar: as case A.

#### CASE D — tab `After the signature` (`id: after-signature`)

This case shows the Pro tier doing its job 41 days after the user proceeded with case C. The left region is headed `ALERT` instead of DECLARED, the right region `APPROVALS INDEX` instead of READ, the diff region `REVOKE, PREPARED`.

ALERT: a message card on `--ink-2`, 1px `--rule`, radius 4px, 16px padding, no messenger branding: header mono 12.5px `--paper-3` `GUARDIAN · Telegram · 14:02 UTC`; body Geist 15px `--paper`: **Delegate B49K…wkS4 on your USDC account was added to the SlowMist malicious-address list 2 hours ago. The approval you signed 41 days ago is unlimited.**; a mono line `Revoke → guardian.sh/r/7vfb…JtQy` (text, not a link); footer mono 12.5px `--paper-3` `one tap builds the Revoke instruction · you sign it`.

APPROVALS INDEX rows (read by the cursor like instruction rows):
1. `USDC · delegate` — `B49K…wkS4 · unlimited · granted 41 d ago` with **`B49K…wkS4`** as the caution-underlined span — `caution` — margin note: `R-041 · B49K…wkS4 · SlowMist malicious-address DB · added 2026-10-20 12:01 UTC · 17 reports` — inset: `token account EMhr…w3BW · delegated_amount = 18446744073709551615 · approved in tx from case 3`
2. `USDC · close authority` — `none` — ✓ `nothing to watch`
3. `wallet · owner` — `System Program` — ✓ `nothing to watch`

REVOKE, PREPARED (`field · before · after`):
- `instruction` · `—` · `Token.Revoke · account: EMhr…w3BW`
- `delegate` · **`B49K…wkS4`** (pen) · `none`
- `fee` · `—` · `0.000005 SOL · you sign it`

VERDICT: `CAUTION` · `R-041` — **A delegate you approved 41 days ago was listed two hours ago. The revoke transaction is built; it moves nothing until you sign it.**

Toolbar: **Revoke** `0.000005 SOL` (primary) · **Keep the approval** (ghost, plain click) · **Read again**. Notes: Revoke → `Demo · in the extension this opens your wallet with the Revoke instruction prepared.` Keep → `Demo · the delegate stays on the watch list.`

#### CASE E — tab `Swap · jup.ag` (`id: clear-swap`)

Deliberately last: it proves the product does not cry wolf.

DECLARED: `origin` `jup.ag` (note, `--paper-3`: `verified origin`) · `button` `Swap` · `wallet said` `Swap 2 SOL → ~310.2 USDC` · `signer` `7vfb…JtQy`

READ rows:
1. `ComputeBudget.SetComputeUnitLimit` `· SetComputeUnitPrice` (index `1–2`) — `units: 400,000 · 10,000 µlamports per unit` — ✓ `expected`
2. `AssociatedToken.CreateIdempotent` (index `3`) — `wSOL account ErdT…oH6w · owner: you` — ✓ `owner is you` — inset: program `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` · accounts: `7vfb…JtQy payer · signer · writable` / `ErdT…oH6w associated token account · writable` / `7vfb…JtQy owner` / `So11111111111111111111111111111111111111112 mint`
3. `System.Transfer` (index `4`) — `2 SOL → ErdT…oH6w (your wSOL account)` — ✓ `destination is yours · wraps SOL for the route` — inset: program `11111111111111111111111111111111` · accounts: `7vfb…JtQy from · signer · writable` / `ErdT…oH6w to · writable`
4. `Token.SyncNative` (index `5`) — `ErdT…oH6w` — ✓ `expected`
5. `Jupiter v6.sharedAccountsRoute` (index `6`) — `in: 2 SOL · min out: 308.65 USDC · via Orca Whirlpool` — ✓ `program verified · route matches the quote` — inset: program `JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4` · accounts (31, showing 4) as in case A
6. `Token.CloseAccount` (index `7`) — `ErdT…oH6w → rent to 7vfb…JtQy` — ✓ `destination is you` — inset: program `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` · accounts: `ErdT…oH6w account to close · writable` / `7vfb…JtQy destination · writable` / `7vfb…JtQy owner · signer`

SIMULATION:
- `SOL` · `−2.00` · `−2.0021 · fee and priority` 
- `USDC` · `+310.20` · `+310.19 · within 0.3% of the quote`
- `authority` · `no changes` · `no changes`
- `delegates` · `none` · `none`

VERDICT: `CLEAR` · `0 findings` — **Does what it says. Received amount within 0.3% of the quote.**

Toolbar: **Continue to wallet** (primary) · **Read again**. Note: `Demo · in the extension the wallet's own Approve button is released.`

### 10.7 Implementation shape (so two engineers build the same thing)

```js
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let token = 0, pending = null, stepIndex = 0, paused = false, steps = [];
function build(caseId) { /* produce steps = [{at, fn}] from the DOM rows of the active case */ }
function run(caseId, delay) {
  cancel(); const my = ++token; build(caseId); stepIndex = 0;
  const next = () => { if (my !== token || paused) return; const s = steps[stepIndex++]; if (!s) return;
    pending = setTimeout(() => { s.fn(); next(); }, s.gap); };
  pending = setTimeout(next, delay);
}
function cancel() { token++; clearTimeout(pending); }
function pause() { paused = true; clearTimeout(pending); }
function resume() { if (!paused) return; paused = false; stepIndex = Math.max(0, stepIndex - 1); /* re-run the current step */ … }
```

Step gaps: row move 200 → arrival class → 380 → status class → next row; after the last row 300 → each diff row at 180 → 300 → verdict. All five cases are in the DOM at build time (no templating); JS only toggles `hidden`, classes and the cursor's `--y` (computed from `row.offsetTop`). Total JS for the demo under 180 lines; whole page under 260 lines including the forms and the menu close.

---

## 11. Diagrams

All diagrams are HTML + CSS (so labels stay 12–13.5px at every viewport and remain real text), with inline SVG only for arrowheads and the pen circle. Strokes that carry meaning use `--rule-strong`; emphasis uses `--paper`; the single flagged element uses `--pen`. Every diagram sits in a wrapper with `aspect-ratio` (desktop) or a `min-height` (mobile) so there is no layout shift, and has an `sr-only` paragraph describing it. Labels are mono 12.5px `--paper-3`; node titles mono 13.5px `--paper`.

Arrow component: a 1px `--rule-strong` line with an open arrowhead `<svg viewBox="0 0 8 8" width="8" height="8"><path d="M1 1l5 3-5 3" fill="none" stroke="currentColor" stroke-width="1"/></svg>`; on mobile the row becomes a column and the arrow rotates 90°.

### 11.1 Declared vs. actual (section 02)

Three columns at 840+ (`1fr 56px 1.4fr`), stacked below. Left: a fake button outline (1px `--rule-strong`, radius 4px, 44px tall, 160px wide, label `Swap` Geist 500 14px `--paper`) with the eyebrow `WHAT THE PAGE SHOWS` above it. Middle: the arrow. Right: eyebrow `WHAT THE PAYLOAD DOES`, then four mono lines (12.5px, `--paper-2`, 28px line height) `1 ComputeBudget.SetComputeUnitLimit` / `2 ComputeBudget.SetComputeUnitPrice` / `3 Jupiter v6.sharedAccountsRoute` / `4 Token.SetAuthority → 3kvc…rmjA`. Line 4 is wrapped in a span with a `--pen` ellipse drawn around it (an absolutely positioned `<svg>` overlay: `<ellipse>` 1.5px stroke, no fill, extending 6px beyond the text box), and a `--pen` mono note to its right at 840+ (below it on mobile): `not declared · R-021`. Nothing else is red.

### 11.2 Sequence (section 03)

A row of five nodes with arrows between them at 1024+, a column on smaller screens:
`Page` → `Wallet` → **`GUARDIAN`** → `Signature` → `Watch`.
Nodes are 1px `--rule-strong` boxes, radius 4px, 12px 16px padding, mono 13.5px `--paper`. The GUARDIAN node is double-ruled (an outer 1px `--rule-strong` box and an inner 1px `--rule` box, 3px apart) and contains four sub-steps in a row (column on mobile): `decode` · `simulate` · `diff` · `intel`, mono 12.5px, separated by 1px `--rule` dividers; `diff` is outlined 1px `--pen` with `--pen` text. Under the row, three mono captions aligned under the arrows: `unsigned tx`, `verdict + rule id`, `delegates, authorities`. The `Watch` node sits after `Signature` with a dotted arrow (1px dotted `--rule-strong`).

### 11.3 Data path (section 05)

Three regions at 840+ (`1.2fr 1.6fr 1.6fr`), stacked below.
- Left region, eyebrow `YOUR WALLET`: a 1px `--rule-strong` box `Wallet` containing a mono line `private key · stays here` in `--paper`. To the right of the box, a vertical 1px dashed `--paper-3` line spanning the diagram height with a rotated (or, on mobile, horizontal) mono label `keys never cross`.
- Middle region, eyebrow `YOUR MACHINE`: box `Adapter` with three mono lines `decode` / `simulate · your RPC` / `cached lists · 24 h`.
- Right region, eyebrow `TEE`: a double-ruled box `Agent` with lines `intent diff` / `intel match` / `monitoring` / `attestation per release`.
- A dashed 1px `--paper-3` boundary (rounded 4px) encloses the middle and right regions with the label `public data only` at its top-left on the boundary (mono, `--ink-0` background padding so it interrupts the dashes).
- Arrows: Wallet → Adapter `unsigned transaction`; Adapter → Agent `decoded tx + simulated effects`; Agent → Adapter (a second, lower arrow pointing left) `verdict · rule id`; Adapter → Wallet (lower, left) `verdict shown · wallet still asks you`. On mobile the arrows stack vertically with labels beneath.
- Nothing in this diagram is red.

### 11.4 Roadmap (section 08)

Specified in §9.12. No red.

---

## 12. Forms

- Both forms (hero: email only; waitlist: email + wallet + team) submit to the same endpoint: `const WAITLIST_ENDPOINT = "https://guardian.sh/api/waitlist";` (VERIFY). `fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, wallet, team, source: "site", hp }) })`. Honeypot: a visually hidden text input named `company` (`hp`), `tabindex="-1"`, `autocomplete="off"`, `aria-hidden="true"`; if filled, show the success state without sending.
- Validation on submit only (never on keystroke): `type="email"` plus a check for whitespace and a dot after the `@`. On failure: `aria-invalid="true"`, the error line with `role="alert"`, focus returns to the input.
- During the request the button text becomes `Sending…` and is `disabled`; no spinner.
- 2xx: crossfade (200ms) to the success block (same height): **You're on the list. We'll write once.** Non-2xx or network error: the network error line (§9.14), the form stays filled.
- Never fake a success state. If the endpoint is not configured at build time, the form must still POST and show the network error; do not ship a `#` action or a `mailto:`.
- The Team checkbox is ticked when the URL hash is `#waitlist` and `sessionStorage.team === "1"` set by the pricing Team button, or more simply via `data-team` on that button's click handler.
- `autocomplete="email"` on the email field; `inputmode="email"`.

---

## 13. `<head>`, SEO, favicon

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GUARDIAN — Nothing gets signed unread.</title>
<meta name="description" content="A non-custodial defense agent for Solana. GUARDIAN decodes and simulates every pending transaction, compares what the page says with what the payload does, and tells you when they disagree. It never sees your keys.">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0A0A0B">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,…favicon.svg, URL-encoded…">
<meta property="og:title" content="GUARDIAN — Nothing gets signed unread.">
<meta property="og:description" content="Non-custodial defense agent for Solana. Decodes, simulates and diffs every transaction before you sign. Never your keys.">
<meta property="og:type" content="website">
<!-- og:image: none at launch (no raster available). Add a 1200×630 PNG of the stacked lockup on ink later. -->
```

Plus the two preconnects and the fonts link (§5.1), then the inline `<style>`. No analytics, no tracking pixels, no third-party scripts of any kind.

---

## 14. Quality bar (the engineer self-verifies every line before handing over)

**Identity**
- [ ] The only chromatic pixels on the page are `--pen` and every one of them marks something wrong (hero full stop, demo flags and chips, diagram flagged element, form errors). Search the CSS for any other hue: there must be none.
- [ ] The mark is never red, never animated except the 2px point lift on hover, never shown without the wordmark except in the favicon.
- [ ] No cards, shadows, gradients, blur, canvas, particles, scroll-triggered reveals, number count-ups.
- [ ] Nothing is centered except the waitlist block and the colophon.
- [ ] No italic glyph anywhere (`font-synthesis: none` is set and no `<em>`/`<i>` is styled italic).
- [ ] Every section has its rule, number and running title; headings never skip a level.

**Type and contrast**
- [ ] H1/H2 render at Newsreader weight 450, opsz 48 (inspect computed `font-variation-settings`).
- [ ] No text under 12px. `--paper-3` never sits on `--ink-2`. No `--paper` text on a `--pen` fill.
- [ ] All text passes 4.5:1 (axe or Lighthouse a11y audit shows zero contrast issues).
- [ ] Measure ≤ 62ch on every paragraph; lead ≤ 56ch.

**Layout**
- [ ] 320px: no horizontal page scroll (check `document.documentElement.scrollWidth === innerWidth` at 320, 360, 390, 600, 840, 1024, 1180, 1440). Tables and the demo simulation scroll inside their own boxes only.
- [ ] The hero sentence is 2 lines at 1440px and 3 lines at 320px, with and without web fonts.
- [ ] The demo tab strip is visible within a 1440×900 viewport without scrolling.
- [ ] Switching demo cases never changes the page height; no CLS during the reading (Lighthouse CLS 0).
- [ ] Sticky margin apparatus does not overlap the nav; `scroll-margin-top` lands anchors below the nav.

**Interaction and a11y**
- [ ] Keyboard only: skip link, nav, menu (mobile), every tab (arrow keys, Home/End), every row button (expand), toolbar buttons (hold works with Space/Enter), FAQ summaries, both forms. Focus ring visible on every one of them on both ink surfaces.
- [ ] Screen reader: the verdict sentence is announced once per case; rows are not announced during reading; the status note is announced on demo button use.
- [ ] `prefers-reduced-motion: reduce`: no cursor, no transitions beyond 1ms, the selected case renders in its final state, tabs still switch, the full stop is present.
- [ ] The reading never runs while `document.hidden` and never runs two chains at once (switch tabs rapidly; only one cursor, one verdict).
- [ ] Pause/resume: expand a row during reading; the cursor stops; collapse; it resumes after 1.5s.

**Forms**
- [ ] Email validation only on submit; the error reads exactly as specified and has `role="alert"`.
- [ ] A failed POST shows the network error and keeps the input; a 2xx shows the success copy at the same height. No fake success.
- [ ] Honeypot present, hidden from AT and tab order.

**Performance**
- [ ] Lighthouse mobile: Performance ≥ 90, Accessibility 100, Best Practices ≥ 95, SEO ≥ 95.
- [ ] Fonts ≤ 160KB total, one stylesheet request, `display=swap`, fallbacks with `size-adjust` so CLS stays 0 on swap.
- [ ] HTML ≤ 180KB uncompressed, no external JS, no inline base64 other than the favicon.
- [ ] No `requestAnimationFrame` loops; the only rAF call is the one-frame transition reset on tab switch.
- [ ] Works with JavaScript disabled: the page reads top to bottom, the nav menu and FAQ open (native `details`), the demo shows case A in its final state (add a `<noscript>` style that sets the final-state classes), the form posts natively to the endpoint (set `action` and `method` on the `<form>` too).

**Honesty**
- [ ] Every VERIFY item in §15 is confirmed or replaced.
- [ ] Every link resolves; no `href="#"`.
- [ ] The demo caption says the keys are fixture keys.

---

## 15. VERIFY before launch

| Item | Where | Action |
|---|---|---|
| `$494M` wallet-drainer losses in 2024, ScamSniffer | §9.5 lead | Confirm against the published 2024 annual report; keep the citation form |
| `Rules v0.4 · 61 rules` | nav status, rules lead, colophon | Replace with the real build and count |
| `23 cases · 0 false positives` | rules code block | Replace with the fixture count for R-021 |
| `212 reports`, `added 2026-09-14` | case A note, how-it-works sample | Must come from a real list entry or be labelled fixture data in the caption (it is) |
| `17 reports`, `added 2026-10-20 12:01 UTC` | case D note | Same |
| `180–400 ms`, `p50 under 400 ms`, `under 120 ms`, `about 2 s` | FAQ 8, spec lists | Replace with measured beta numbers |
| `slot 441,906,318` | colophon | Replace with the newest fixture's slot |
| Fixture keys (6) | §10.6 | Replace with the real fixture keys when the repository publishes; regenerate truncations |
| Program ids (8) | §10.6 | Confirm against Solana documentation |
| `Q1/Q2/Q3 2027` | roadmap, pricing, rules, trust, FAQ 5 and 7, custody strip | Confirm the calendar with the client |
| `WAITLIST_ENDPOINT`, `hello@guardian.sh`, `security@guardian.sh`, `guardian.sh/r/…` | forms, footer, samples | Confirm the domain and endpoints |
| Repository, Attestations, Status, Docs, Telegram, X, Privacy, Terms hrefs | rules link, footer | Provide real URLs or omit the link |
| Jupiter route minimum-out and received amounts | cases A and E | Any plausible quote is acceptable for a fixture; keep received within 0.3% of quote in case E |

---

## 16. Engineering notes

**File structure of `index.html`** (one file, in this order): `<head>` (§13) → `<style>` (tokens block verbatim, then base, type, layout, components, sections, demo, diagrams, forms, and the reduced-motion query last) → `<body>`: skip link → `header.nav` → `main` (hero, reading, threat, how, rules, act, trust, comparison, pricing, roadmap, faq, waitlist) → `footer` → one `<script>` at the end of body (demo chain, tabs, row expansion, hold button, forms, menu close, team pre-tick). No `defer`/`async` needed since it is inline and last.

**JS budget**: ≤ 260 lines, no dependencies, strict mode, every listener attached once, no globals except the data object and the endpoint constant.

**CSS budget**: ≤ 1,400 lines. Use logical, flat class names (`.sec`, `.margin`, `.ruled`, `.ledger`, `.panel`, `.rows`, `.flag`, `.margin-note`, `.cursor`, `.chip`, `.btn`, `.btn-ghost`). No utility soup, no nesting deeper than three levels.

**Build order** (for two engineers working in parallel): Engineer 1: tokens, base, type, grid, nav, hero, custody strip, ruled list, ledger table, code block, details, forms, footer, diagrams. Engineer 2: the Reading (panel, tabs, five cases in DOM, chain, cursor, pause, hold button, reduced motion), verdict definitions, pricing table responsive stacking. Integration: Engineer 1 owns `index.html`; Engineer 2 delivers the demo as a self-contained `<section>` plus its CSS and JS blocks pasted into the marked places. Both run the §14 checklist independently before handover.

**Density rule**: if a region of the page feels empty, add content (another fixture row, a footnote with a source, a second rule), never decoration. Austerity read as unfinished is the one risk of this direction, and the cure is always more precision, not more ornament.

*End of brief.*
