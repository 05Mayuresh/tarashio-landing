# Tarashio landing page

Tarashio is a mindset improvement tool: one small drill a day, inside your real life.

This repository holds the complete codebase for the Tarashio landing page. It's a single-page site written in plain HTML, CSS and JavaScript, with no build step and no dependencies.

## What's in here

| Path | What it is |
|---|---|
| `index.html` | The whole website. All CSS is in the `<style>` block and all JavaScript (scroll scenes, nav, deck shuffle, slider, language switch) is in the `<script>` block at the end. |
| `a/` | All assets: logo, megaphone illustration, hero loop video, the 2-minute story film and photography. |
| `design-sheet.html` | The design system: grid, colour, type, radius, spacing, chips and buttons (with live hover), navigation, background and motion rules. |
| `DEVELOPER_SPEC.md` | The detailed build spec: every token, easing curve, duration, scroll timeline, interaction and responsive rule, written so a developer (or an AI) can rebuild the site exactly. |
| `serve_landing.py` | A tiny local preview server that disables browser caching. |
| `archive/index.before-redesign.html` | The page before the redesign, kept for reference. |

## Run it locally

The site needs Python 3 to serve it:

```bash
python serve_landing.py 8080
```

Then open http://localhost:8080.

Opening `index.html` directly from disk also works, but the server avoids stale caching while you edit.

## Notes for the developer

- Start with `DEVELOPER_SPEC.md`. Wherever it and `index.html` differ, `index.html` is the source of truth.
- Fonts come from Google Fonts (Poppins).
- Copy exists in English and Hinglish, held in the `data-en` / `data-hi` attributes on each element.
- The review cards, the review quotes and the "Try Tarashio now" trial link are placeholders.
- View on a laptop at full width and scroll at a normal pace. Most sections are scroll-driven animations.
