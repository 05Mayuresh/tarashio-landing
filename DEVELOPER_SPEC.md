# Tarashio Landing Page: Developer Build Spec

> **Who this is for:** the developer (human or AI) who will rebuild this landing page in production.
> **Source of truth:** the reference build `index.html` (single file, with assets in `a/`). It is live at https://claude.ai/artifact/1Lb1XV2JxNj9uxPawNGHQr.
> When this document and the reference build disagree, **the reference build wins**. Open it next to this spec and match it frame by frame.
>
> **How to read it:** every rule uses one of these words:
> - **MUST**: required behaviour.
> - **NEVER**: forbidden.
> - **Value**: an exact number to copy.
>
> Timings are in ms. Scroll distances are in `vh` (viewport heights) unless stated. Easing names refer to §4.1.

---

## 0. Non-negotiables (read first)

1. **Calm, adult motion.** Everything moves with ease-in-out or decelerate curves.
   - NEVER use bounce, spring overshoot, elastic or linear motion on anything visible.
   - NEVER let anything "pop" in at full opacity.
2. **Scroll-driven scenes are scroll-linked, not time-based.**
   - Their state is a pure function of scroll progress, so they are reversible: scrolling up plays them backwards exactly.
   - NEVER trigger those scenes with one-shot timers.
3. **Only composited properties animate** (`transform`, `opacity`, `clip-path`, `filter` on small elements).
   - NEVER animate `top`, `left`, `width`, `height` or `margin` in scroll scenes.
   - The one allowed exception is the nav CTA `height` (§5.4).
4. **Yellow (`#FFC300`) is reserved for action and labels:** buttons, chips, tab hover and small accents. NEVER use it as a large fill area. Black and yellow are the only pair used in interactive hover inversions.
5. **One heading pattern everywhere:** chip, then heading, then lead, with fixed gaps (§3.6).
6. **Do not change, only reproduce:**
   - "What is a mindset" deck: the shuffle (§6.3).
   - "Same situation, two mindsets" split slider (§6.4).
   - Button and chip hover choreography (§5.1, §5.2).
   - Phone home-screen walkthrough (§6.6, phase 3).
7. **Respect `prefers-reduced-motion: reduce`** (§8).

---

## 1. Page structure and scroll lengths

The order is top to bottom. "Pinned" means a `position: sticky; top:0; height:100vh` stage inside a taller section. While the user scrolls through the extra height, the stage stays in place and its scene is driven by progress `p ∈ [0,1]`.

| # | Section | id / anchor | Total height | Pinned scroll length | Ground |
|---|---|---|---|---|---|
| 1 | Nav (fixed, overlays everything) | `#nav` | – | – | glass |
| 2 | Hero | `#top` | `max(720px,100svh)`, max 1012px | not pinned | video |
| 3 | Mindset intro + shuffle deck | `#mindset` | intro + **320vh** deck | 220vh | page bg |
| 4 | Split slider "Same situation, two mindsets." | – | auto | not pinned | page bg |
| 5 | Trainable → Research → Meet Tarashio | `#trainable` (`#tarashio` anchor at 680vh inside) | **910vh** | **810vh** | page bg |
| 6 | Method → app explainer | `#how` | **820vh** | 720vh | page bg |
| 7 | What Tarashio is not | `#not` | auto | not pinned | page bg |
| 8 | Reviews | – | **360vh** | 260vh | `#0B0B0D` night |
| 9 | End card + footer | `#try` | auto | not pinned | `#0B0B0D` night |
| – | Video modal | `#modal` | fixed overlay | – | – |

Pinned progress formula (per scene): `p = clamp((scrollY − sectionTop) / (sectionHeight − innerHeight))`.

---

## 2. Grid and layout

| Token | Value | Notes |
|---|---|---|
| Design frame | 1440px | Figma frame |
| Content width `--maxw` | **1240px** | `.wrap{width:min(1240px, 100% − 2×margin); margin-inline:auto}` |
| Side margin `--margin` | `clamp(20px, 6.94vw, 100px)` | 100px at 1440 |
| Columns | 12 col, 24px gutter | three-card rows use `repeat(3,1fr)` with `--gap-card` |
| Page overflow | `html{overflow-x:clip}` | NEVER allow horizontal scroll at any width |

**Three-card grids** (Research and "Not") MUST use CSS **subgrid**: each card spans 3 rows (`grid-row: span 3; grid-template-rows: subgrid`). Stat/title, body and divider/citation then line up across all three cards whatever the text length.

### Breakpoints used

| Max width | What changes |
|---|---|
| 1100px | nav tabs hidden; language switch pushed right |
| 900px / 899px | method section stacks vertically; hero becomes auto height |
| 860px | research and "not" grids become 1 column |
| 760px | deck card becomes vertical (image on top); train cards and spheres use mobile mapping; reviews use mobile offsets |
| 640px / 639px | hero phone moves into normal flow under the copy; comparison slider becomes 4:5 |
| 560px | smaller nav, buttons and chips |
| 480px | hero phone scale .56 |
| 420px | nav brand word hidden (logo only) |

Test at **1440×900, 820×1180 and 390×844** at minimum.

---

## 3. Design tokens

### 3.1 Colour

| Token | Hex | Use |
|---|---|---|
| `--bg` / `--mint` | `#E7FBFA` | page ground (under the ambient gradient) |
| `--surface` | `#FFFFFF` | cards |
| `--surface-warm` | `#F6F2EF` | review cards |
| `--night` | `#0B0B0D` | reviews and end section ground |
| `--ink` | `#0E0E10` | primary text, dark buttons, selected states |
| `--ink-2` | `#2B2F33` | secondary text (tabs, labels, explainer copy) |
| `--muted` | `#555555` | lead and body copy on light |
| `--subtle` | `#6E6E6E` | meta, citations, unselected language |
| `--line` | `rgba(14,14,16,.08)` | hairlines and card outline ring |
| `--brand` | `#1490C2` | accent blue: focus ring, links hover, "Yes" switch, index fill, numbers |
| `--brand-deep` | `#23147A` | gradient end |
| `--teal` | `#2FB6CB` | phone highlight ring, small accents |
| `--aqua` | `#71DAD5` | background blob, phone day dots |
| `--deep` | `#0981BE` | phone thumb sphere |
| `--yellow` | `#FFC300` | buttons, chips, tab hover, review stars, active review dot |
| `--orange` | `#FF7B00` | phone mockup only (notification dot, streak flame, book) |

**Brand gradient** `--grad-text: linear-gradient(104deg, #1490C2 12%, #23147A 96%)`. Use it only as **text fill** (`background-clip:text; color:transparent`) on:
- the mindset H2
- research stats
- the "not" titles
- the "TARASHIO" meet word

### 3.2 Typography

- **Font:** Poppins (Google Fonts) at weights 300/400/500/600/700, with fallback `system-ui, sans-serif`. Use `-webkit-font-smoothing:antialiased`.
- **Body:** 16px / 1.55, weight 400, colour `--ink`.

| Role | Size | Weight | Letter-spacing | Line-height |
|---|---|---|---|---|
| Display (hero lockup word) | `clamp(48px,6.1vw,88px)` | 700 | .01em | 1 |
| H2 (every section heading, hero H1 too) | `clamp(30px,3.35vw,48px)` | 600 | −.03em | 1.15 (hero 1.18) |
| H3 / card statement | `clamp(20px,1.8vw,26px)` | 500–600 | −.02em | 1.3 |
| Deck card title | `clamp(28px,2.9vw,42px)` | 600 | −.03em | 1.1 |
| Research stat | `clamp(36px,3.6vw,52px)` (mobile 32px) | 600 | −.035em | 1 |
| "Not" title | `clamp(28px,2.6vw,38px)` | 600 | −.03em | 1.1 |
| Meet word "TARASHIO" | `clamp(56px,10vw,144px)` | 700 | .01em | .95 |
| Meet descriptor | `clamp(18px,2.2vw,30px)` | 400 | −.015em | – |
| Lead | `clamp(16px,1.3vw,19px)` | 400 | – | 1.6, colour `--muted` |
| Small | 14px | – | – | – |
| XS / meta / citation | 13px | 500 for labels | .04–.06em on labels | – |
| Button label | 16px (nav 15px, end CTA 18px, ≤560px 15px) | 500 | −.005em | – |
| Chip label | 15px (≤560px 14px) | 400 | 0 | – |

- Headings use `text-wrap: balance` and leads use `text-wrap: pretty`.
- Body copy never exceeds about 720px (lead) or 420px (card copy).

### 3.3 Radius (taken from Figma)

| Token | Value | Use |
|---|---|---|
| `--r-sm` | 8px | focus ring, review video area |
| `--r-md` | 14px | small cards (train cards), slider image, captions |
| `--r-lg` | 24px | containers: deck cards, research, "not", method cards, frames, end card, modal video |
| `--r-pill` | 999px | buttons, chips, nav bar, tabs, language switch, segmented control |

NEVER use radii outside this set, except inside the phone mockup.

### 3.4 Elevation and the Figma 3D bevel

```css
--sh-1: 0 1px 16px rgba(0,0,0,.08);                                     /* segmented control */
--sh-2: 0 1px 2px rgba(0,0,0,.04), 0 18px 40px -24px rgba(9,40,60,.22);  /* every card */
/* cards also get an outline ring:  , 0 0 0 1px var(--line) */

/* the Figma "chip bevel": soft lift + top-right highlight + bottom-left inner shade */
--bevel:       0 1px 8px rgba(0,0,0,.19), inset -5px 6px 4px rgba(255,255,255,.49), inset 3px -2px 8.6px rgba(0,0,0,.25); /* yellow surfaces */
--bevel-dark:  0 1px 8px rgba(0,0,0,.22), inset -4px 5px 4px rgba(255,255,255,.16), inset 3px -2px 8px rgba(0,0,0,.7);    /* ink surfaces */
--bevel-light: 0 1px 8px rgba(0,0,0,.10), inset -4px 5px 4px rgba(255,255,255,1),   inset 3px -2px 8px rgba(0,0,0,.08);   /* white surfaces */
```

Every pill-shaped control (button, chip, selected tab, selected language, selected segment, round icon buttons) MUST carry the bevel that matches its fill colour. This gives the "3D chip" feel from Figma.

### 3.5 Spacing (8-pt)

`--s1 8 · --s2 16 · --s3 24 · --s4 32 · --s5 48 · --s6 64 · --s7 96 · --s8 128` (px)

| Semantic token | Value | Meaning |
|---|---|---|
| `--section` | `clamp(88px,8.9vw,128px)` | vertical padding of normal sections |
| `--gap-chip` | `clamp(24px,2.2vw,32px)` | chip → heading |
| `--gap-head` | `clamp(16px,1.7vw,24px)` | heading → lead |
| `--gap-content` | `clamp(40px,4.4vw,64px)` | heading block → content |
| `--gap-card` | `clamp(16px,1.7vw,24px)` | card ↔ card |
| `--clear` | `clamp(40px,5vw,64px)` | minimum clearance around animated elements |

### 3.6 Section heading pattern

```
[chip]            ← .tag
  ↕ --gap-chip
[H2]              ← centred, max-width ~900px
  ↕ --gap-head
[lead]            ← centred, max-width ~720px
  ↕ --gap-content
[content]
```

Centred in every section except Method, which is left-aligned at the content edge.

---

## 4. Motion system

### 4.1 Easing curves (only these)

| Name | Curve | Use |
|---|---|---|
| `--ease` (out) | `cubic-bezier(.22,1,.36,1)` | things **arriving** (reveal in, lift, arrow nudge) |
| `--ease-in` | `cubic-bezier(.55,0,.75,.2)` | things leaving fast (rare) |
| `--ease-std` (in-out) | `cubic-bezier(.65,0,.35,1)` | on-screen changes: hover fills, colour swaps, exits, toggles, strike |
| nav curve | `cubic-bezier(.45,0,.15,1)` | nav expand and collapse only |
| JS `eio(t)` | `-(cos(πt) − 1) / 2` (sine in-out) | **all scroll-linked scene values** |
| JS `eo(t)` | `1 − (1−t)³` | method heading fade-in only |

JS helpers used everywhere:
```js
clamp(v,a=0,b=1); lerp(a,b,t)=a+(b-a)*t;
seg(p,a,b)=clamp((p-a)/(b-a));     // local 0→1 progress of a sub-range
```

### 4.2 Durations

| Token | ms | Use |
|---|---|---|
| `--t-fast` | 220 | press / lift |
| `--t-out` | 360 | exits, hover colour changes |
| `--t-in` | 700 | entrance opacity |
| `--t-hero` | 900 | entrance transform, phone screen scroll, highlight ring |
| `--stagger` | 110 | between siblings |
| nav | 860 | every nav state change |
| hover fill | 640 | button and chip fill sweep |

Rule: **entrances are slower than exits.** In = opacity 700ms plus transform 900ms (`--ease`); out = 360ms (`--ease-std`).

### 4.3 Scroll engine (MUST replicate; this is what makes it smooth)

One `requestAnimationFrame` loop drives every pinned scene. Each scene's displayed progress **glides** toward the real scroll progress with a ~140ms exponential time constant. This removes mouse-wheel stepping without feeling laggy.

```js
// on scroll: request one frame (passive listener). In the frame:
const dt = Math.min(64, now - lastT);          // ms since last frame
const k  = reducedMotion ? 1 : 1 - Math.exp(-dt / 140);
scene.tgt = clamp((scrollY - scene.top) / scene.len);
if (scene off-screen by > 60px)  scene.cur = scene.tgt;   // snap, skip work
else scene.cur = |tgt-cur| < .0004 ? tgt : cur + (tgt-cur)*k;
render(scene.cur);
// keep requesting frames while any scene is still gliding; stop when settled
```

- Cache `top`/`len` and re-measure on resize, on `document.fonts.ready` and on `load`.
- NEVER call `getBoundingClientRect` per frame per element.
- Write transforms with `translate3d(...)`, rounded to 2 decimals (scale to 4).

### 4.4 Viewport reveal (non-pinned content)

`.reveal` elements:

| State | opacity | transform | Transition |
|---|---|---|---|
| Hidden | 0 | `translate3d(0,20px,0)` | out: 360ms `--ease-std` |
| In (`.in`) | 1 | none | opacity 700ms `--ease` + transform 900ms `--ease`, optional delay `--d` |

- **Trigger:** IntersectionObserver, `threshold .2`, `rootMargin 0 0 -6% 0`.
- **The class toggles both ways:** content re-hides when it leaves the viewport, so it animates in again next time.

### 4.5 Tactile ("haptic") feedback

The web build uses **no vibration API**. Tactile feel is created visually, and every interactive element MUST have it:

| Element | Hover | Press (`:active`) |
|---|---|---|
| Buttons | lift `translateY(-1px)` 220ms `--ease`; arrow dot nudges `translateX(2px)` 360ms | `translateY(0) scale(.98)` |
| Chips (labels, not clickable) | arrow dot nudges `translate(1px,-1px)` | – |
| Split slider handle | – | `scale(.96)` 360ms |
| Review play button | `scale(1.05)` 360ms | – |
| Modal close | background → yellow, `rotate(90deg)` 360ms | – |
| Cursor | `pointer` on buttons, `ew-resize` on the slider, `default` on chips and the selected language | – |

---

## 5. Components

### 5.1 Buttons: the "fill sweep" hover. DO NOT ALTER

**Anatomy:** a pill, 52px tall (nav 52/42 compact, end CTA 60, ≤560px 48), padding `0 6px 0 22px`, gap 12px. Inside are the label and a round **arrow dot**: a 40px circle with a 15px "→" (stroke 2.4, round caps).

**Variants**

| Variant | Rest | Dot | Hover end state |
|---|---|---|---|
| `btn-dark` (Try Tarashio) | ink pill, white label, `--bevel-dark` | yellow circle, ink arrow | **yellow** pill, **ink** label |
| `btn-yellow` (nav CTA) | yellow pill, ink label, `--bevel` | ink circle, yellow arrow | **ink** pill, **yellow** label |
| `btn-light` (Watch 2-min story) | white pill, ink label, `--bevel-light`; the dot is a **play** icon on the **left** (padding mirrored `0 22px 0 6px`) | ink circle, white play icon | **ink** pill, **white** label, play icon turns yellow |

**Mechanism:** a `::before` layer in the dot's colour is clipped to exactly the dot's circle at rest. On hover the clip grows to the full pill.

```css
.btn::before{ background:var(--fill);
  clip-path: inset(calc(50% - var(--dot)/2) var(--pr) calc(50% - var(--dot)/2) calc(100% - var(--pr) - var(--dot)) round 999px);
  transition: clip-path 640ms var(--ease-std); }
.btn:hover::before{ clip-path: inset(0 0 0 0 round 999px); }
```

(For `btn-light` the rest clip sits on the **left** side, so the fill grows left → right.)

**Timeline, hover IN:**

| t (ms) | What happens |
|---|---|
| 0 | fill starts growing out of the dot (640ms, `--ease-std`); pill lifts 1px (220ms); arrow nudges 2px right (360ms) |
| 220 → 500 | label colour crossfades to the opposite colour (280ms, `--ease-std`, delay 220): it flips as the fill passes under it |
| 620 | the pill's own background snaps to the fill colour (1ms), so no anti-aliased fringe remains at the edge |
| 640 | done |

**Hover OUT:** the background colour reverts instantly (it is hidden under the fill). The fill retracts into the dot (640ms `--ease-std`), and the label returns (260ms, delay 140).
**Focus-visible:** identical to hover.

### 5.2 Section chips (`.tag`): same gesture

- **Size:** a 40px tall pill (≤560px: 38px), yellow, `--bevel`, padding `0 5px 0 16px`, gap 10, label 15px/400 ink.
- **Dot:** a 30px ink circle (≤560px: 28px) with a yellow arrow **rotated −45° (↗)**.
- **Hover:** the ink fills the chip from the dot (640ms `--ease-std`), the label turns yellow (280ms, delay 220), the background snaps to ink at 620ms, and the dot nudges `(1px,-1px)`.
- **Leave:** reverses.
- **Behaviour:** chips are **labels, not links**, so `cursor: default`.
- **Arrow system rule:** **chips = ↗, action buttons = →.** NEVER mix them.

### 5.3 Focus

The global `:focus-visible` style is a `2px solid #1490C2` outline, offset 3px, radius 8px. Buttons also show their hover fill on focus.

### 5.4 Navigation (fixed, one continuous gesture)

**Geometry**
- `position:fixed; top:20px`, horizontally centred.
- Width: `min(1240px, 100% − 2×margin)`; height 68px; padding `0 7px 0 24px`; gap 16.
- **Bar surface** (`::before`): `rgba(255,255,255,.7)`, a 1px border of `rgba(255,255,255,.95)`, `backdrop-filter: blur(16px) saturate(1.3)`, pill radius.
- **Contents, left → right:**
  1. Brand: 30×31 logo plus "TARASHIO" at 20px/700, .02em.
  2. Tabs, centred.
  3. Language switch.
  4. CTA `btn-yellow`: "Try" + " Tarashio now", with the long part hidden at ≤560px.

**States**

| State | When | Visual |
|---|---|---|
| **Full** | `scrollY < 0.55 × innerHeight` (on the hero) | full bar, CTA 52px with a 40px dot |
| **Min** (`.min.compact`) | the user scrolls **down** past the hero | the bar's left edge sweeps **right into the CTA** and fades. Brand, tabs and language slide 28px right and fade. **Only the CTA remains, anchored right**, with an extra shadow `0 12px 28px -12px rgba(0,0,0,.35)`. The CTA shrinks to 42px with a 32px dot. The empty area is `pointer-events:none`. |
| **Compact** (`.compact`) | the user scrolls **up** (not on the hero) | the full bar returns, but slimmer. The bar is inset 6px top and bottom, the whole nav moves up 6px, the bar becomes `rgba(255,255,255,.86)`, and the CTA is 42px with a 32px dot. |
| **Peek** (`.peek`) | mouse enters the nav, or focus inside it, while Min | behaves as Compact (full content returns). Removed on mouse leave or focus out. |

- **Direction detection** accumulates scroll delta in one direction. It switches to Min only after **+24px** of continuous downward scroll, and to Compact after **−24px** upward. This prevents flicker from jittery trackpads.
- **The CTA is never moved sideways.** NEVER centre it in Min; it covers content there.

**Motion:** every nav change uses **one duration (860ms)** and **one curve `cubic-bezier(.45,0,.15,1)`**, so the bar and its content move as a single gesture.
- **Bar:** a `clip-path` inset from the left, `calc(100% − ctaWidth)`, where `--cta-w` = CTA width + 14px, measured in JS and re-measured on language change.
- **Content:**
  - opacity uses `--ease-std` over 860 × .6–.7 ms;
  - transform uses the nav curve over 860ms;
  - on expand, opacity starts after a 0.12 × 860ms delay, so content appears as the bar reaches it, never before;
  - on collapse, the bar's opacity fades in the second half (delay .45 × 860, duration .55 × 860).
- No `height` or `top` changes, except the CTA height and dot size, which animate on the same 860ms curve.

**Tabs:** Mindset · Why it's trainable · Tarashio · How it works.

| Tab state | Style |
|---|---|
| Rest | transparent, `--ink-2`, 14px/500, padding 8×14, pill |
| Hover | **yellow** background, ink text, `--bevel` (360ms `--ease`) |
| Selected (`.on`) | **ink** background, white text, `--bevel-dark`; hover does not change it |

- **Active tab:** the last section whose top is above `scrollY + 0.4 × innerHeight`.
- No tab is active near the page end (`scrollY > scrollHeight − 1.6 × innerHeight`).
- Hidden at ≤1100px.

**Language switch (EN / Hinglish):**
- **Container:** `rgba(14,14,16,.05)`, padding 3, pill, 12px/500.

| Option state | Style |
|---|---|
| Unselected | `--subtle` grey text, padding 6×11 |
| Unselected hover | background `rgba(14,14,16,.09)`, ink text (360ms) |
| Selected (`aria-pressed=true`) | **ink** background, white text, `--bevel-dark`, `cursor:default`, no hover change |

- The choice is persisted in `localStorage('tl')`.
- Switching swaps every `[data-en]`/`[data-hi]` text and sets `<html lang>` to `en` or `hi-Latn`.

**Mobile nav (≤560px):**
- **Bar:** height 60, top 12, inset 4px, padding `0 6px 0 16px`.
- **Brand and language:** brand 17px with a 26×27 logo; language buttons padded 5×8 at 11px.
- **CTA:** 46px with a 34px dot (compact: 40 and 30).
- **≤420px:** the brand word is hidden and only the logo shows.

### 5.5 Segmented control (split slider)

- **Container:** white, padding 4, gap 4, pill, `--sh-1`, centred.
- **Buttons:** 8×20 padding, 14px/500, `--ink-2`; selected is ink with white text and `--bevel-dark`. Colour transitions take 360ms.

### 5.6 Phone mockup (reused in hero and method)

- **Built in HTML**, not an image: 451×919 at scale 1, scaled with `--ps` via `transform: scale()`.
- **Frame:** a peach shell `#FFE3D1` with radius 74 and padding 8, then a black bezel (radius 66, padding 11), then the screen `#F2F1EC` (radius 56).
- **Top of screen:** a 112×33 dynamic island and the status bar "13:13".
- **Screen content, top → bottom:**

| Region | `data-r` | Content |
|---|---|---|
| Header | `top` | avatar "A" (yellow), "Good evening / Aarav", energy pill "2", streak pill "4", bell with orange dot |
| Next task | `task` | "Your next task / Picked from your answers"; yellow task card: "Ready" badge, "Phone down for 5 minutes", chips "6 h to finish · 5 min · 1 Energy", black CTA "See my task" with a yellow arrow circle; illustration (sun, book, hourglass, shelf) |
| Reflection | `refl` | "Reflection waiting / Drink water with your other hand / Add my reflection" |
| Week | `week` | "Your week · Thu, 12 Nov · Day 4 of 7"; 7 pill days (M T W done in teal/aqua with ✓, T today black with a yellow 4, F S S empty) |
| Reads | `reads` | "Your brain · Two-minute reads"; 2 read cards |

- **Fixed tab bar:** black, 82px, 4 icons, Home selected in white.
- **Highlight ring** `.p-hl`: radius 28, `box-shadow: 0 0 0 3px #2FB6CB, 0 0 0 9px rgba(47,182,203,.18)`. It moves between regions with left/top/width/height plus opacity, 900ms `--ease-std` (opacity 700). The screen content scrolls with `translateY` over 900ms `--ease-std`.
- **Drop shadows:** hero `drop-shadow(0 28px 44px rgba(9,40,60,.16))`; method `drop-shadow(0 20px 36px rgba(9,40,60,.14))`.

---

## 6. Sections

### 6.1 Ambient background (whole page, fixed behind everything)

**Layers, bottom → top:**
1. The solid `--bg` `#E7FBFA`.
2. A **blob layer** (`.bg-in`, 150% of viewport tall).
3. A **grain layer**.

The whole background is `position:fixed; z-index:-2; pointer-events:none`.

**Blobs:** circular `radial-gradient(circle, colour 0, transparent ~62%)` shapes.

| Blob | Size | Position | Colour (alpha) | Drift period | Delay |
|---|---|---|---|---|---|
| b1 aqua | 70vmax | left −22vmax, top −26vmax | `rgba(113,218,213,.55)` | 58s | 0 |
| b2 brand blue | 62vmax | right −24vmax, top 12% | `rgba(20,144,194,.20)` | 72s | −20s |
| b3 warm yellow | 54vmax | left −14vmax, top 38% | `rgba(255,214,120,.22)` | 66s | −34s |
| b4 periwinkle | 60vmax | right −18vmax, top 52% | `rgba(120,138,226,.14)` | 80s | −12s |
| b5 teal | 66vmax | left 22%, top 74% | `rgba(47,182,203,.22)` | 70s | −46s |

- **Drift:** each blob uses `alternate infinite` with `--ease-std`. The keyframes go 0% `translate(0,0) scale(1)` → 50% `translate(4vmax,−3vmax) scale(1.06)` → 100% `translate(−3vmax,4vmax) scale(.97)`.
- **Scroll parallax:** the blob layer moves `translateY(−(scrollY / maxScroll) × 0.5 × innerHeight)`, so across the whole page it drifts up half a screen.
- **Rule:** yellow stays faint and only in negative space. The background must **never** compete with text or cards.

**Grain:** fine, minute specks that "buzz". NEVER use a cloudy or paper texture.
- **Tile:** a 128×128px SVG `feTurbulence type=fractalNoise baseFrequency=1.15 numOctaves=1 seed=3 stitchTiles=stitch`.
- **Colour matrix:** `0 0 0 0 .04 / 0 0 0 0 .06 / 0 0 0 0 .09 / 2.2 0 0 0 −.95`. This alpha-thresholds the noise into discrete dark specks.
- **Layer:** `inset:-64px`, **opacity .085**, tiled at 128px.
- **Buzz:** `1s steps(1) infinite`, hopping between 8 offsets each 1/8 s: (0,0), (−23,11), (17,−29), (−9,−14), (31,19), (−27,−5), (6,27), (−14,−31) px. Only the transform changes, so it costs no repaint.
- **Reduced motion:** the grain buzz and blob drift stop.

### 6.2 Hero

- **Height:** `max(720px, 100svh)`, max 1012px. White text.
- **Media:** a looping muted video `a/hero-loop.mp4` (`autoplay muted loop playsinline`, poster `a/hero.jpg`), `object-fit:cover`.
  - **Overlay:** `linear-gradient(90deg, rgba(10,14,24,.72) 0%, .42 45%, .06 78%)` plus `linear-gradient(0deg, rgba(10,14,24,.35), transparent 40%)`.
  - **Bottom edge:** a **mask fade**, `mask-image: linear-gradient(to bottom, #000 72%, transparent 100%)`, so the video dissolves into the page. NEVER use a hard edge.
- **Copy** (left, max 640px, padding-top 48):
  1. **Lockup:** the logo mark `clamp(56px,6.6vw,96px)` with a 2px white outline (4 drop-shadows) plus "TARASHIO" in the display style, gap 14.
  2. **H1** "Every big moment is built on small, daily practice.": H2 size, 600, max 480px, margin-top 64.
  3. **CTAs** (margin-top 48, gap 16): `btn-light` "Watch 2-min story" and `btn-dark` "Try Tarashio".
- **Phone:** sits right, overhanging into the next section.
  - Scale `ps = min(1, 0.313W/451, 0.9H/919)`.
  - Position: right `max(16, (W−1240)/2 − 10)`, top `0.23H`.
  - The copy max-width is reduced so it never overlaps the phone.
- **≤639px:** the phone goes into flow below the copy, centred at scale .6 (≤480: .56). It has a negative bottom margin (−200 / −180), and the next section pads its top (260 / 240px) to clear it.
- **Reduced motion:** the video does not autoplay (poster only).

### 6.3 "What is a mindset" + shuffle deck. DO NOT CHANGE

**Head:**
- **Chip:** "What is a mindset".
- **H2** (gradient text): "Same moment. Different mindset. Different next step." (max 900).
- **Lead:** "Your mindset is the lens you see a moment through. It quietly decides whether you try again, ask the question, or put the phone down."

**Deck:**
- **Container:** 320vh tall with a sticky stage. Deck size is `min(1240, …)` × `min(440px, 60vh)`, shifted up 4vh.
- **Cards** (white, radius 24, `--sh-2` plus ring, 2 columns: text | image inset 12px with radius 12):

| # | Title | Copy | Image |
|---|---|---|---|
| 01 / 04 | Nazariya | How you read a moment: a threat, or a chance to practise. | nazariya.jpg |
| 02 / 04 | Focus | Staying with one thing, even when the phone calls. | focus.jpg |
| 03 / 04 | Starting | Moving before you feel ready. Action over inaction. | starting.jpg |
| 04 / 04 | Handling discomfort | Staying steady after a “no” or a bad day. | discomfort.jpg |

- Each card has a progress row of 4 bars (20×3, ink at .12; the current one is brand blue).

**Entrance** (IntersectionObserver on the deck, class `.in`, toggles both ways):
- Cards start at opacity 0, `translateY(64px) scale(.97)`.
- They deal in back card first, front card last: opacity 900ms and transform 1200ms `--ease`, each delayed `k × 150ms`, where k = 3 for the back card down to 0 for the front.
- Exit: opacity 420ms, transform 520ms `--ease-std`.

**Shuffle** (scroll-linked; each card's wrapper "slot" holds the transform):
- **Stack:** N = 4. Step offset `D = min(22px, 5% of deck height)` and step scale `.035`.
  - The card at stack position `pos` (0 = front) gets `y = pos×D` and `scale = 1 − pos×.035`.
  - Opacity is 1 for pos ≤ 2; the 4th card is .45. z-index = `20 − 2×pos`.
- **Steps:** 3 shuffle steps across the deck's progress. Within each step, motion happens over local 15%–95% with `eio`; the edges are dwell time.
- **The front card travels to the back** in one continuous arc (u: 0 → 1):
  - `y = lerp(0, yBack, u) − sin(πu) × lift`, where `lift = h × lerp(1, sBack, .5) + yBack×.5 + 28`. It rises fully clear above the stack, then sinks into the back slot.
  - Scale goes 1 → back scale. Opacity stays 1 for the first half, then eases to .45.
  - z-index is 40 for u < .5 and 0 after. The swap happens at the top of the arc, where nothing overlaps, so the re-layering is invisible.
- **The rest of the stack** glides one place forward at the same time.

**≤760px:** cards are single-column (image on top, rows 1fr / 1.1fr) and the deck is `min(560px, 72vh)`.

### 6.4 "Same situation, two mindsets." DO NOT CHANGE

- **Head** (padding-top 96, centred row): a white 48px round icon with a swap-arrows glyph in brand blue and `--bevel-light`, plus the H2 "Same situation, two mindsets."
- **Segmented control:** Classroom / Office / Nets.
- **Frame:**
  - **Outer:** white, radius 24, padding `clamp(8,1.2vw,16)`, shadow `0 1px 16.7px rgba(0,0,0,.12)`.
  - **Comparison:** aspect 1206/562 (≤640: 4/5), radius 14, `cursor: ew-resize`, `touch-action: pan-y`.
  - **Left image:** the "fixed" photo (`*-a.jpg`).
  - **Right image:** the "growth" photo (`*-b.jpg`), clipped by a **slanted** polygon. The split line leans: the top is offset +9% and the bottom −9% from the handle position. A 3px white SVG line draws the seam.
  - **Handle:** a 52px white circle at the centre of the seam with ‹ › arrows, `--bevel-light`, shadow `0 8px 24px rgba(0,0,0,.18)`; `scale(.96)` while dragging.
  - **Captions** (bottom, max 44%, radius 14, blur 10):
    - Left: dark `rgba(14,14,16,.58)`, white text, label "Fixed".
    - Right: `rgba(255,255,255,.9)`, label "Growth" in brand blue, right-aligned.
    - A caption fades (360ms) when the handle comes within 22% of its side.
- **Copy:**

| Tab | Fixed caption | Growth caption |
|---|---|---|
| Classroom | “Mujhse nahi hoga.” | “Main karke dikhaunga.” |
| Office | “They said no. I’ll stay quiet.” | “Next meeting, I’ll share my point.” |
| Nets | “Out again. Today is ruined.” | “Five more minutes in the nets.” |

- **Interaction:** pointer drag (pointer capture) and keyboard ← → in steps of 5%. The position is clamped to 6%–94%. The handle has `role=slider` with `aria-valuenow`.
- **Hint animation:** plays once when 60% visible and again on every tab change. Over 2400ms the handle sways `0.5 + sin(eio(t)·2π) × 0.1 × (1 − eio(t))` (a damped sway), then settles at 50%. It is cancelled by user drag and skipped under reduced motion.
- All six images are preloaded. Images crossfade over 500ms `--ease-std`.

### 6.5 Trainable → Research → Meet Tarashio (one pinned scene, 810vh of scroll)

**Timing:** `V = progress × 810`, so **V is literally vh scrolled into the scene.** Every value below is a pure function of V, so the scene is reversible. All curves use `eio`.

**Master timeline**

| V (vh) | Beat |
|---|---|
| 0 → 267 | **Opening scene:** chip "Why a mindset is trainable" at the top; 16 spheres appear and link into a chain; 4 cards arrive |
| 236 → 267 | caption "The more you practise, the more dots connect." shows (bottom, brand blue) |
| 267 → 304 | **opening scene clears completely**: spheres and links fade to 0; cards, chip and caption are hidden |
| 310 → 345 | **"What research says" chip** rises 28px → 0 and fades in |
| 345 → 439 | **the three research cards arrive one by one** (each 50vh, staggered 22vh): card 1 345–395, card 2 367–417, card 3 389–439 |
| 439 → 540 | **hold**, more than a full screen of scroll for reading. Nothing moves. |
| 540 → 620 | **research melts away**: chip 540–600; cards shrink and fade over 60vh each, staggered 10vh (540–600, 550–610, 560–620), chip shrinks and fades; **at the same time the dots drift back in** (dim releases 560–615) |
| 600 → 640 | **gather**: all spheres converge on the hero sphere, which grows |
| 640 → 685 | **travel**: the gathered sphere moves straight down to the logo position, still growing |
| 675 → 715 | **morph**: the sphere fades as the logo fades in (scale .88 → 1) |
| 720 → 745 | **"Meet Tarashio" chip** glides up 44px → 0 and fades in |
| 748 → 782 | **the name "TARASHIO" emerges from behind the logo** and travels down into place |
| 785 → 805 | descriptor "A mindset improvement tool." fades in and rises 16px |

**Opening scene details**
- **Chip:** at `top: clamp(100px,13vh,132px)`, centred. Nothing may start above chip bottom + 64px (mobile 40px).
- **Spheres:** 16 circles with a radial gradient `circle at 32% 28%, light 0 → mid 42% → dark 100%` and shadow `0 10px 20px -12px rgba(9,40,60,.35)`. There is no yellow or orange in this palette.

  | Key | Light | Mid | Dark |
  |---|---|---|---|
  | t | #CDEFF4 | #5CC3D3 | #1A7F95 |
  | m | #E2F7F5 | #93DCD8 | #3E9E9C |
  | d | #CFE6F5 | #3A9FD0 | #125E8C |
  | y | #DCE6F7 | #7D9BD6 | #34508F |
  | o | #E2DEF5 | #8A82CC | #3A3080 |

- **Positions** are `[fx, fy, size px, colour]`, 4 per card, in appearance order:
  ```
  [.35,.30,62,t] [.44,.43,34,y] [.31,.47,22,m] [.40,.20,18,o]
  [.62,.28,28,m] [.66,.42,56,d] [.58,.50,20,y] [.71,.32,24,t]
  [.33,.62,52,o] [.45,.66,96,t] [.37,.80,28,d] [.52,.56,18,m]   ← index 9 (96px) is the "hero sphere"
  [.66,.66,60,y] [.58,.78,52,t] [.70,.54,22,o] [.50,.84,30,m]
  ```
  - Mapping: `x = fx × W` (mobile: `lerp(.1W, .9W, (fx−.3)/.42)`) and `y = lerp(chipBottom+64, .9H, (fy−.18)/.68)`.
- **Appear:** sphere i (card c = i÷4, k = i mod 4) appears over `620 × [.03 + .095c + .018k, +.06]` vh. Scale goes .6 → 1 and opacity 0 → 1.
- **Links:** a 1.5px brand-blue line (round caps) grows from each sphere to the next, starting .025 later than the next sphere's appearance, at opacity up to .45. The final link closes the loop at 248–273vh.
- **Cards** (white, radius 14, padding `12px 20px 18px`, width `min(354px, 40vw)`):
  - Header row: a 14px grey label with the number in brand blue, then a hairline.
  - Statement: 20–26px/500.
  - Entrance: class `.in`, opacity 700ms plus `translateY(16→0)` 900ms `--ease`; exit 360ms.

| # | Label | Statement | Position (desktop) | Appears at V |
|---|---|---|---|---|
| 01 | The brain changes with use | What you practise, your brain builds. | left 8.5%, top = content-top | 12 |
| 02 | Habits take repetition | Cue, urge, action. Then again. | right 5.5%, +9vh | 71 |
| 03 | Attention can be practised | Noticing you drifted is a skill. | left 7%, +37vh | 130 |
| 04 | Small, then slightly harder | Small steps beat big promises. | right 5.5%, +44vh | 189 |

- `content-top = chip top + 40px + --gap-content`.

**Research cards** (subgrid, 3 columns, white, radius 24, padding `clamp(24,2.4vw,32)`):
- **Stat:** gradient text.
- **Body:** 16px muted.
- **Citation:** 13px subtle with a top hairline.
- **Per-card values:** `e` = arrive progress, `x` = exit progress.
  - opacity `e × (1 − x)`
  - `translateY((1−e)×40 + x×18)`
  - `scale(lerp(.96,1,e) × (1 − x×.1))`
- **Chip values:** opacity `rIn × (1−rOut)`, `translateY((1−rIn)×28 − rOut×12)`, `scale(1 − rOut×.06)`.

| Stat | Text | Citation |
|---|---|---|
| 3 months | of juggling practice measurably changed grey matter in the brain. | Draganski et al., *Nature*, 2004 |
| 66 days | median time for a new daily habit to feel automatic. One missed day didn't undo it. | Lally et al., *European Journal of Social Psychology*, 2010 |
| 94 studies | show that small, specific if-then plans make people more likely to follow through. | Gollwitzer & Sheeran, *Advances in Experimental Social Psychology*, 2006 |

**Sphere → logo**
- **Gather point:** x = logo centre; y = `max(110 + 0.32×big, 0.2H)` (mobile 96), where `big = 0.78 × logo width`.
- **Hero sphere scale:** `(.6 + .4·appear) × lerp(1, big/96 × .6, gather) × lerp(1, 1/.6, travel)`, so it keeps growing as it descends. Its opacity fades with morph.
- **Other spheres:** shrink to 15% and fade as they gather. Links fade with gather.

**Meet block** (bottom-aligned, padding-bottom 8vh, centred):
- **Order:** chip, then the logo `clamp(130px,15vw,216px)` (the logo sits **above** the name in z-order), then the name, then the descriptor.
- **Name:**
  - opacity `clamp(r2 × 1.8)`
  - `translateY(−(1−r2) × wDy)`, where `wDy` = distance from the logo centre to the name's resting centre
  - `scale(lerp(.32, 1, r2))`
  - So it starts small, hidden behind the logo, and slides out downward to rest.
- **Gradient:** "TARA" uses the left half of the gradient and "SHIO" the right half (`background-size:200%`).

**≤760px:**
- Chip top 84px.
- Cards `min(260px, 68vw)` at left/right 4%, offsets +0/+16/+33/+49vh.
- The caption wraps (90% width, bottom 4vh).
- Research becomes 1 column, with the cards compacted to padding 16×20, a 32px stat and 15px body.

### 6.6 Method → app explainer (pinned, 720vh of scroll)

**Head** (left-aligned at the content edge, top `clamp(112px,16vh,168px)`, max 520):
- **Chip:** "Our methodology".
- **H2:** "Real actions. Real experiences. Lasting growth."

**Method cards** (white, radius 24, 600×468 base, padding `28 28 24`, gap 14):
- Number: 14px brand, .1em.
- Title: 28px/600.
- Copy: 17px muted.
- Image: radius 14, fills the rest.

| # | Title | Copy | Image |
|---|---|---|---|
| 01 | Action over inaction | Don’t wait for the perfect moment. Small tasks help you act before you feel ready. | m-timed.jpg |
| 02 | No extra time | Your day is your training ground. Every task fits your routine and is done within 24 hours. | m-everyday.jpg |
| 03 | No one-size-fits-all | Your challenges, your pace. The difficulty adapts to how you’re doing. | m-harder.jpg |
| 04 | Awareness through action | Notice your automatic reactions. Practise more deliberate ones. | m-reflect.jpg |

**Layout:**
- **Stack:** right side, `min(600px,46vw) × min(468px,56vh)`, centred vertically (−38%).
- **Thumbnail slots:** a left column under the heading (starting 28px below it), `min(420px,32vw)` wide, with 4 equal slots and a 10px gap.

**Phases** (p = 0…1, all `eio` unless noted):

| p | Beat |
|---|---|
| .00 → .04 | heading area fades in (`eo`) |
| .04 → .33 | **cards arrive one at a time in order 4 → 3 → 2 → 1** (each over .08, starting .07 apart). Each rises 56px into the stack. Cards on top push lower ones +14px right, −18px up and −5% scale per layer, so **card 1 ends on top**. Arriving cards are opaque fast (opacity `clamp(e×3)`), so text never shows through. |
| .37 → .65 | **cards minimise 1 → 2 → 3 → 4** (each .08, .065 apart) from the stack into their left thumbnail slots. A minimising card rides above the stack. At >50% it switches to a lighter "small" shadow. |
| .62 → .68 | heading fades out and lifts 20px |
| .62 → .72 | **phone rises** from below the viewport to its position (centred; scale fits ~94% of height minus 170, max 30% of width) |
| .66 → .80 | **thumbnails tuck behind the phone** (each .08, .02 apart): they move to the phone centre (stacked down its height), scale ×.6, drop below the phone in z-order, and fade over the last 45% |
| .76 → .82 | explainer (index list and description) fades in |
| .80 → 1.0 | **phone walkthrough**: 5 equal steps (see below) |
| after un-pin | **hand-off:** over the next .75 screen of scroll the whole stage fades to 10% and drifts down `0.22H` with `scale(.97)`, so "What Tarashio is not" arrives under a soft crossfade, never a hard edge |

**Phone walkthrough (current version; keep as is):**
- **Left:** the index list of 5 buttons (`role=tab`).
  - Each has a 3×50 track that fills top-down in brand blue as the step progresses.
  - Text `clamp(16px,1.6vw,22px)`/500 at `rgba(14,14,16,.38)`; hover .7; active ink. Colour changes take 700ms.
- **Right:** the description, with a 2px brand-blue left border, label `0N / 05`, and 16–19px `--ink-2` text.
  - Paragraph change: out 360ms; in opacity 700 + transform 900 with a 160ms delay, rising 10px.
- **Phone:** the screen scrolls so the region sits about 110px from the top. The teal highlight ring moves to the region (§5.6).
- **Clicking an index item** smooth-scrolls to that step's midpoint: `top + len × (.80 + (i + .5) × .04)`.

| # | Index | Description | Region |
|---|---|---|---|
| 01 | Energy and streak | How many drills you can still take on today, and how many days in a row you practised. | top |
| 02 | Your next drill | One small task, picked from your answers. A clear time to finish and a clear cost. | task |
| 03 | Quick reflection | One tap on how it went. Honest answers shape what comes next. | refl |
| 04 | Your week | Seven days at a glance. One missed day won’t break your progress. | week |
| 05 | Two-minute reads | Short reads on why each drill works, right on Home. | reads |

**≤900px:**
- The head sits at top 96.
- The stack is full width at the bottom (44vh) and the slots are a horizontal row of 4 (11vh) above it.
- The index becomes 4 small horizontal bars (34×3, filled left → right) at the top.
- The description sits at top 118 with no border.

### 6.7 What Tarashio is not

**Head:**
- **Chip:** "What Tarashio is not".
- **H2:** "Less theory. More real-world application."

**Cards** (subgrid 3-up, white, radius 24, padding `clamp(24,2.4vw,32)`):
- **Label row:** a toggle switch plus "Yes"/"No" text (13px/500, .04em, `--ink-2`).
- **Title:** gradient text, `clamp(28,2.6vw,38)`, margin-top 32.
- **Body:** 16px muted, margin-top 24, a top hairline, padding-top 16.

| Title | Body |
|---|---|
| Motivation | Posts, tips and speeches give a short spark. We give you a task to finish within 24 hours. |
| Meditation | No quiet, seated sessions. Your training happens inside your regular day. |
| Therapy | We don’t diagnose or treat clinical conditions. Tarashio is for healthy people stuck in a mindset loop. |

**Toggle:** 40×23 track, a 17px white knob (shadow `0 1px 3px rgba(0,0,0,.25)`), 3px inset.
- **Yes:** brand-blue track, knob at the right (`translateX(17px)`).
- **No:** ink track, knob at the left.

**Closing pill** (below, centred, margin-top `--gap-content`): ink pill, `--bevel-dark`, padding `8 24 8 8`, lead-size 500 white text "Don’t just learn. Train. Experience. Refine.", with a 36px yellow circle holding an ink ✓.

**Choreography:**
1. **Cards enter** (class `.in` on the section; IntersectionObserver at 20%):
   - From opacity 0 and `translateY(24px)`.
   - Opacity 700ms `--ease`, transform 900ms `--ease`, stagger `i × 110ms`.
2. **The sequence starts** (class `.go`) only when the card grid is **≥60% visible**, so it is actually seen. It **resets only when the grid fully leaves** the viewport. All steps use `--ease-std`.

| Var | Value |
|---|---|
| B (lead-in) | 500ms |
| ts (between toggles) | 420ms |
| sw (toggle duration) | 650ms |
| pause | 350ms |
| strike duration | 1300ms |
| strike-at | B + 2·ts + sw + pause = **2340ms** |

| t (ms) | Event |
|---|---|
| 500 | toggle 1 flips Yes → No: track blue → ink, knob slides left, "Yes" crossfades to "No" (650ms) |
| 920 | toggle 2 flips |
| 1340 | toggle 3 flips (done at 1990) |
| 2340 → 3640 | **all three titles are struck through together**: a 3px ink line (opacity .82, radius 3, at 53% height, extending 4px past each side) draws left → right (`scaleX 0→1`). At the same time each title drains to monochrome: `filter: grayscale(1) brightness(1.1)` |
| 3890 | closing pill fades in and rises 16px (700ms opacity / 900ms transform, `--ease`) |

- **Order is fixed:** toggles one by one **first**, then the strike on all three **together**. NEVER strike before the toggles.
- **≤860px:** 1 column; the closing pill uses radius 24 and auto width.

### 6.8 Reviews (night section, pinned, 260vh of scroll)

- **Ground:** `#0B0B0D`, white text.
- **Chip:** "Hear from our users", centred at `top: clamp(110px,14vh,148px)`.
- **Megaphone:** illustration `a/megaphone.svg` at bottom-left, width `clamp(180px,30vw,420px)`. Cards emerge from its mouth (70% across, 33% down the image).
- **Review card:**
  - **Size and surface:** width `min(clamp(280px,42vw,430px), (100vh − 300px) × 430/468)`, aspect 430/468, `--surface-warm`, radius 14, shadow `0 24px 48px -24px rgba(0,0,0,.6)`.
  - **Who row:** a 48px avatar with a 1.5px ink ring, "Programme member", and 5 yellow stars (17px).
  - **Video area:** radius 8, warm grey gradient. A centred 56px white play button with `--bevel-light`, `scale(1.05)` on hover. A "Video coming soon" pill at the bottom-left.
  - **Quote:** 16px `--ink-2`.
- **Motion** (`t = p × 2.75 − .05`; card j enters over `eio(clamp((t − j)/.6))`):
  - **Entering:** a card moves from the mouth to its rest spot (desktop x = 53% centre; y = max(chip bottom + 56, vertically centred); mobile centred at 24%H, clearance 32). Scale .35 → 1, opacity `clamp(e×1.6)`.
  - **Receding:** each newer card in front pushes older ones back-left by −56px x, +28px y and −7% scale (mobile −14 / +10). They dim with a black overlay of `min(depth,2) × .22`.
  - Cards fade out after depth 2.4. Receding cards **move down, never up** into the chip.
- **Progress dots:** right side, three 3×28 bars (white .16); the current one is yellow (700ms).
- **Footnote:** bottom-right, 12px, white .4: "Sample placeholders. Real video testimonials will replace them."

### 6.9 End card and footer (night ground)

- **Section padding:** 96 top, 48 bottom.
- **Card:** white, radius 24, padding `128 clamp(24,8vw,150) 48`, centred. Two soft glows behind the content: aqua .32 at top-left and brand blue .12 at the right, 560px circles.
- **Contents:**
  1. Logo `clamp(88,9vw,128)`.
  2. **H2** (margin-top 48): "Train your mindset. Reach new heights."
  3. **Lead:** "Your first drill takes five minutes. Try it in your phone's browser before you make an account."
  4. **Large `btn-dark`** "Try Tarashio now": 60px tall, 44px dot, padding `0 8 0 28`, 18px label, 18px arrow.
- **Click:** shows the toast "Trial link coming soon." (14px brand blue). It fades in over 360ms and hides after 2600ms. This is a placeholder until a real trial URL exists.
- **Footer** (margin-top 128, top hairline):
  - **Left:** brand plus "From *tarashna*, polishing a diamond. Small daily drills for a stronger mindset."
  - **Columns:** **Explore** (Mindset, Why it's trainable, Tarashio, How it works) and **Contact** (hello@tarashio.com, tarashio.com). Links turn brand blue on hover (360ms).
  - **Legal row** (13px subtle): "© 2026 Tarashio" and "Builds habits of mind. Not a medical or therapy service."

### 6.10 Video modal

- **Trigger:** the "Watch 2-min story" button. The source `a/film.mp4` is lazy-set on first open, and the video autoplays with controls.
- **Overlay:** `rgba(6,8,14,.82)`; fades in over 700ms `--ease` and out over 360ms.
- **Video:** `min(1100px,100%)`, max 84vh, radius 24. Scale .97 → 1 (900ms in, 360ms out).
- **Close:** a 48px white circle at the top-right, `--bevel-light`; hover turns it yellow and rotates it 90°.
- **Closing:** close button, backdrop click or **Esc**. Focus moves to Close on open and returns to the Watch button on close. The video pauses on close.

---

## 7. Copy and languages

- Every visible string exists in **EN** and **Hinglish** (`data-en`, `data-hi`). The tables above give EN; take the Hinglish strings verbatim from the reference build.
- Product copy rules: plain, calm, adult. No hype, no exclamation marks.
- **Caveat:** the review quotes are placeholders.

---

## 8. Accessibility

- **Contrast** (measured on the reference build):

  | Element | Ratio |
  |---|---|
  | body/lead `#555` on white | ~7.5:1 |
  | chip ink on yellow | ~13:1 |
  | struck "not" titles (large text) | ~3.7:1 |
  | blue "Yes" track vs white | ~3.6:1 (UI component ≥3:1) |

  Keep these at or above AA.
- **Reduced motion** (`prefers-reduced-motion: reduce`):
  - all CSS transitions and animations become 1ms;
  - smooth scroll is off;
  - the hero video does not autoplay;
  - background drift and grain buzz stop;
  - scroll scenes jump directly to their target (`k = 1`, no glide);
  - the slider hint is skipped.
- **Semantics:**
  - landmarks on each `section` (`aria-label`);
  - the language switch is `role=group` with `aria-pressed`;
  - the segmented control is `role=tablist` / `tab` with `aria-selected`;
  - the slider handle is `role=slider` and keyboard operable;
  - explainer descriptions are `aria-live=polite`;
  - the modal is `role=dialog aria-modal`;
  - decorative SVGs and spheres are `aria-hidden`;
  - the meet word has `aria-label="TARASHIO"`;
  - the toast is `role=status`.
- Every hover state also applies on `:focus-visible`.

---

## 9. Assets (`a/`)

| File | Use |
|---|---|
| `logo.svg` | nav brand, hero lockup, meet logo, end card, footer |
| `megaphone.svg` | reviews |
| `hero-loop.mp4`, `hero.jpg` | hero background video and poster (also the modal poster) |
| `film.mp4` | 2-min story (modal) |
| `nazariya.jpg`, `focus.jpg`, `starting.jpg`, `discomfort.jpg` | mindset deck |
| `class-a/b.jpg`, `office-a/b.jpg`, `nets-a/b.jpg` | split slider (a = fixed, b = growth) |
| `m-timed.jpg`, `m-everyday.jpg`, `m-harder.jpg`, `m-reflect.jpg` | method cards |

- The phone mockup, spheres, toggles and icons are built in code (HTML/CSS/inline SVG), not images.
- Lazy-load deck and method images. Preload the split-slider images.

---

## 10. Acceptance checklist

Check each item at 1440×900, 820×1180 and 390×844:

- [ ] No horizontal scroll at any width; no console errors.
- [ ] Nav:
  - [ ] full on the hero; collapses to the right-anchored CTA on scroll-down; slim bar on scroll-up;
  - [ ] full on hover/focus;
  - [ ] the bar and content move as **one** 860ms gesture, with content never appearing before the bar.
- [ ] Tabs: yellow on hover, black when selected. Language: black selected, grey unselected, tinted on hover.
- [ ] Every button and chip hover: the fill grows out of the dot over 640ms, the label flips at about 220ms, and it reverses on leave. Yellow/black only.
- [ ] Deck: the front card visibly arcs over and goes to the back; no popping.
- [ ] Trainable: the opening scene fully clears before the research chip; research cards arrive one by one, hold for more than a screen of scroll, then melt back as the dots return; sphere → logo; the chip rises, the name emerges from behind the logo downward, then the descriptor.
- [ ] Method: cards arrive 4 → 1, minimise 1 → 4, tuck behind the phone; explainer steps; soft crossfade into "not".
- [ ] "Not": toggles flip one by one, then all three titles strike together, then the closing pill appears. It resets only after leaving the viewport.
- [ ] Reviews: cards grow out of the megaphone and recede back-left without overlapping the chip.
- [ ] Background: soft drifting brand light plus fine buzzing grain; it never competes with content.
- [ ] Scrolling backwards plays every scroll scene in reverse, smoothly, with no jitter.
- [ ] Reduced motion is honoured.
