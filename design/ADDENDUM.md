# Brief addendum (creative director, 2026-10-20) — overrides BRIEF.md where they differ

1. **Domain and endpoints are placeholders.** No real domain exists yet. Use `guardian.example` everywhere a domain
   is shown (`hello@guardian.example`, `security@guardian.example`, `guardian.example/r/7vfb…JtQy`). The waitlist
   endpoint is the relative path `/api/waitlist` (`const WAITLIST_ENDPOINT = "/api/waitlist"`), and the `<form>` also
   carries `method="post" action="/api/waitlist"` as the no-JS fallback. A non-2xx or network failure shows the
   network error copy from BRIEF §9.14. Never fake a success state. Leave a `// TODO: point WAITLIST_ENDPOINT at the
   real service` comment.
2. **Drop invented commercial commitments.** Remove "Beta wallets get Pro free until Q2 2027" from the pricing
   footnotes. Keep "No GUARDIAN token. There will not be one." and the SOL billing lines (they are in BRIEF §15 VERIFY).
3. **Links with no destination are omitted, never `#`.** The rules section has no "Browse the rules" link at launch.
   Footer column 2 becomes `CONTACT`: `hello@guardian.example` and `security@guardian.example` as `mailto:` links.
   Footer column 3 becomes `LEGAL`: the line "A Clear verdict describes a payload, not an investment." and the text
   "Privacy policy and terms publish with the public beta." (plain text, no link).
4. **Nav status line** stays `Rules v0.4 · 61 rules` (VERIFY item). No dot, no color.
5. **Roadmap years**: keep `NOW → Q1 2027`, `Q2 2027`, `Q3 2027` exactly as BRIEF §9.12 (VERIFY item).
6. **Integration markers** (engineer 1 must leave these, engineer 2 must target them):
   - In `<style>`, after all base/component CSS and BEFORE the reduced-motion query: a line `/* READING-CSS */`.
   - In `<main>`, between the hero section's closing tag and the threat section: `<!-- READING-START -->` and
     `<!-- READING-END -->` on their own lines.
   - In the final `<script>`, inside the IIFE after the shared helpers and before forms/menu code: `/* READING-JS */`.
   Engineer 2's fragment files are pasted verbatim at those markers by the integrator. The integrator also removes
   the markers.
7. **Shared base classes** (engineer 1 defines them exactly per BRIEF §8; engineer 2 uses them and defines nothing
   with these names): `.sr-only`, `.eyebrow`, `.mono`, `.btn`, `.btn-ghost`, `.link`, `.chip` with modifiers
   `.chip-blocked`, `.chip-caution`, `.chip-clear`, `.ruled` (+ `.row`), `.ledger` (+ `.ledger-wrap`), `.code`,
   `.caret` (the SVG glyph class), `.addr`, `.sec`, `.sec-rule`, `.sec-no`, `.margin`, `.text`, `.container`.
   Engineer 2 scopes every selector under `#reading` and uses the token names from `design/tokens.css`.
8. **No-JS state for the demo**: a `<noscript><style>` block in the Reading fragment forces case A into its final
   state (rows opaque, status text visible, flagged underline at scaleX(1), diff rows and verdict visible).
9. **Red audit**: the only chromatic color is `--pen` and it appears only where something is wrong. The logo, CTAs,
   the "you are here" marker and the roadmap glyphs are never red. Section numbers are not red.
10. **Measure**: paragraphs max-width 62ch, leads 56ch, per BRIEF §5.4. The three-column grid is banned; use ruled
    lists, ledger tables and full-width line art.
11. **Deliverable paths** (absolute root: the working directory):
    - engineer 1 → `index.html` (shell: everything except the Reading section)
    - engineer 2 → `design/reading/section.html`, `design/reading/reading.css`, `design/reading/reading.js`,
      plus `design/reading/test.html` (a standalone harness that inlines tokens.css, a minimal copy of the shared
      base classes, and the three fragments, for visual testing only)
    - engineer 3 → `brand.html` (brand guidelines page), reusing `assets/*.svg` inline
