# MediClinic Design Language

This document defines the UI/UX design language for **MediClinic** — a premium aesthetic surgery clinic web application. All future UI work must follow these guidelines to keep the product visually consistent.

**Source of truth for tokens:** `static/clinic/styles.css`  
**Base layout:** `templates/base.html`

---

## 1. Brand & Design Intent

MediClinic should feel:

| Pillar | Expression |
|--------|------------|
| **Medical trust** | Clean layout, navy blues, readable typography, structured content |
| **Luxury** | Gold accents, soft shadows, generous spacing, premium hero blocks |
| **Modern** | Rounded pill buttons, subtle motion, glass-like nav, animated starfield background |

**Avoid:** script/handwriting fonts, cluttered layouts, harsh pure-black text, emoji flags (use SVG), flat generic Bootstrap look.

---

## 2. Color System

### 2.1 Core Palette

| Role | Token | Hex | Usage |
|------|-------|-----|--------|
| Primary Blue | `--primary` | `#3FA9F5` | Links, focus rings, icon highlights, hero borders, statistics accents |
| Accent Gold | `--accent` | `#F5B94C` | Badges (`hero-chip`), nav underline hover, active flag state, section title underline |
| Background | `--bg-soft` | `#F4F6F9` | Page background base |
| Heading Navy | `--heading` | `#1A2D4D` | H1–H3, labels, card titles, form labels |
| Navy Strong | `--navy-strong` | `#10233F` | Header/footer gradients, primary button gradient base |
| Navy Soft | `--navy-soft` | `#16345C` | Card kicker text, pair titles, image item titles |
| Body Gray | `--body` | `#6B7280` | Paragraphs, hints, secondary copy |
| White | `--white` | `#FFFFFF` | Cards, forms, modal dialogs, content surfaces |
| Line | `--line` | `#E4E9F2` | Borders, dividers |

### 2.2 Recommended Surface Ratio (60 / 25 / 10 / 5)

| Share | Color | Where |
|-------|-------|--------|
| **60%** | White `#FFFFFF` | Cards, modals, form panels, image panels |
| **25%** | Soft Gray `#F4F6F9` | Page background, alternate subtle fills |
| **10%** | Primary Blue `#3FA9F5` | CTAs accents, borders, glows, focus states |
| **5%** | Gold `#F5B94C` | Chips, hover accents, decorative underlines |

### 2.3 Dark Navy Surfaces (Preferred for Chrome)

The user prefers **darker blue** for structural UI:

- **Header:** `linear-gradient(90deg, rgba(16,35,63,0.95), rgba(26,45,77,0.95))`
- **Footer:** `linear-gradient(90deg, var(--navy-strong), var(--heading))`
- **Hero blocks:** `linear-gradient(135deg, #122a4a, #1a2d4d 55%, #1f3f69)` with white heading text
- **Primary buttons:** dark navy gradient (`#1d3f6e` → `#102b4e`), not bright blue fills

Bright blue (`#3FA9F5`) is an **accent**, not the dominant button fill.

### 2.4 Shadows

```css
--shadow-soft: 0 12px 40px rgba(26, 45, 77, 0.08);
--shadow-card: 0 10px 24px rgba(26, 45, 77, 0.1);
```

Use soft navy-tinted shadows — never heavy black drops.

---

## 3. Typography

### 3.1 Font Stack

| Use | Font | Weights | Notes |
|-----|------|---------|-------|
| **Headings** (H1–H3, brand) | **Montserrat** | 600, 700, 800 | Modern geometric sans — **not** serif, **not** script |
| **Body** | **Inter** | 400–800 | All paragraphs, buttons, forms, nav |

Google Fonts import (in `base.html`):

```
Inter:wght@400;500;600;700;800
Montserrat:wght@600;700;800
```

### 3.2 Type Scale & Usage

| Element | Font | Size / style |
|---------|------|----------------|
| Brand (`brand-main`) | Montserrat 800 | `1.28rem`, `letter-spacing: 0.1em` |
| Brand subtitle | Inter | `0.74rem`, uppercase, muted white on nav |
| H1 (hero) | Montserrat | `clamp(1.8rem, 2.8vw, 2.5rem)`, white on hero |
| Section title | Montserrat | `1.45rem` + gold/navy gradient underline |
| Body | Inter | `0.93–0.95rem`, `line-height: 1.7–1.8` |
| Labels / chips | Inter 700 | uppercase chips: `0.79rem`, `letter-spacing: 0.08em` |
| Image item title | Inter 700 | `0.82rem`, `--navy-soft` |

---

## 4. Layout & Spacing

### 4.1 Page Structure

```
[ sticky top-nav — dark navy ]
[ main.container.main-content — flex: 1 ]
[ site-footer — dark navy ]
```

- **Sticky footer pattern:** `body` is `display: flex; flex-direction: column; min-height: 100vh`
- **Max content width:** `1120px` via `.container`
- **Horizontal gutter:** `--page-gutter: clamp(24px, 5vw, 48px)` (20px on mobile ≤860px)
- **Main vertical padding:** `40px` top, `64px` bottom

### 4.2 Grid Patterns

| Pattern | CSS class | Columns |
|---------|-----------|---------|
| Procedure cards (home) | `.grid` | `repeat(auto-fill, minmax(250px, 1fr))` |
| Before/After cases | `.cases-grid` | **3 columns** desktop → **2** tablet (≤1024px) → **1** mobile (≤860px) |
| Images inside Before/After side | `.side-gallery-grid` | `repeat(auto-fill, minmax(120px, 1fr))` |

### 4.3 Border Radius

| Element | Radius |
|---------|--------|
| Buttons, chips, flags | `999px` (pill) |
| Cards, hero, modals | `16–22px` |
| Image thumbs | `12px` |
| Inputs | `10px` |

---

## 5. Background & Motion

### 5.1 Layered Background (always on `base.html`)

1. **Starfield** (`.starfield` + `.starfield-soft`) — animated floating dots, blue/gold/white, `pointer-events: none`
2. **Page glow** (`.page-glow-top` / `-bottom`) — blurred blue and gold orbs
3. **Base fill** — soft gray with subtle navy radial gradients on `body`

Keep animations **subtle** — they must not reduce readability.

### 5.2 Micro-interactions

- Buttons: `translateY(-1px)` on hover, `0.22s ease`
- Cards: lift + stronger shadow on hover
- Gallery thumbs: `scale(1.03)` on hover
- Nav links: gold underline expands on hover

---

## 6. Component Patterns

### 6.1 Navigation (`.top-nav`)

- Dark navy gradient, sticky top
- White/light nav text (`#e6efff`)
- Ghost logout button on dark background
- Outline buttons use white fill for contrast on dark header
- Language switcher: SVG flags in circular `.flag-btn`, gold border when `.active`

### 6.2 Buttons

| Class | Use |
|-------|-----|
| `.btn-primary` | Main CTA — **dark navy gradient**, white text |
| `.btn-outline` | Secondary actions — white bg, navy border |
| `.btn-ghost` | Tertiary on dark surfaces — transparent, light text |
| `.btn-danger` | Delete — white bg, red text/border |
| `.btn-small` | Inline gallery admin actions |

All buttons: pill shape, `font-weight: 600`, inline-flex.

### 6.3 Hero (`.hero`)

- Dark navy gradient panel, rounded `22px`
- Optional `.hero-chip` — gold-tinted badge at top
- White H1, muted blue-white body text
- Decorative blue radial glow pseudo-element top-right

### 6.4 Cards (`.card`)

- White surface, `border: 1px solid var(--line)`
- Soft shadow, hover lift
- Image: `aspect-ratio: 5/3`, `object-fit: cover`
- **Full card clickable** via `.card-stretched-link` overlay pattern
- `.card-kicker` — small uppercase primary/navy label above title

### 6.5 Before / After Gallery

**Data model UX:**

```
Procedure
 └── GallerySection (Section 1, 2, 3…)
      ├── Before part — multiple images, each with title (EN/TR)
      └── After part  — multiple images, each with title (EN/TR)
```

**Display:**

- `.cases-grid` — responsive case cards (3 / 2 / 1 columns)
- Each `.case-card` shows first Before | After preview thumbs side by side
- Clicking a card opens the gallery modal
- Admin manage panel (authenticated only) via `.case-card-admin` `<details>`

**Gallery modal (`#image-lightbox`):**

- Opens on case card click — must use `[hidden]` + `.lightbox[hidden] { display: none !important }`
- Centered panel with generous outer whitespace (not edge-to-edge fullscreen)
- Before/After toggle buttons in header — only button clicks switch mode
- **Horizontal** scroll through images in the active section (`.lightbox-scroll`)
- Each `.lightbox-slide`: image card + accent-bordered `.lightbox-caption`
- Clicking a slide image opens the nested preview lightbox (`#image-preview-lightbox`, z-index 65)
- Close via backdrop click, × button, or `Escape`
- Body scroll locked via `.lightbox-open` on `<body>`
- Smooth open/close transitions on panel and backdrop

**Image preview lightbox (`#image-preview-lightbox`):**

- Large single-image view for customer presentation
- Elegant pill-style caption (Montserrat)
- Close via backdrop, × button, or `Escape` (closes preview before main modal)
- Smooth scale/fade open and close animations

### 6.6 Modals (`.app-modal`)

- Backdrop: dark navy blur `rgba(7, 18, 34, 0.62)`
- Dialog: white, `border-radius: 16px`, max-height `86vh`, scrollable
- Wide variant: `.app-modal-dialog-wide` for gallery upload forms
- Close via backdrop, × button, or `Escape`
- **Never** show modals when `[hidden]` — critical bug fix pattern

### 6.7 Forms (`.form-card`)

- White panel, soft shadow, max-width `760px` (or `-wide` for gallery)
- Labels: `--heading`, weight 600
- Inputs: full width, soft border, blue focus ring `rgba(63, 169, 245, 0.15)`
- Gallery upload: nested `.section-block` → `.section-part` (Before/After) → `.media-row` rows
- Dynamic rows via `gallery-form.js` — reindex field names on submit (`s{section}_{b|a}{index}_*`)

### 6.8 Auth Layout (`.auth-layout`)

- Two-column grid on desktop: info panel + form card
- Info panel: light gradient white/blue, hero chip + title
- Single column on mobile

### 6.9 Footer (`.site-footer`)

- Dark navy gradient, light text
- Sticky at bottom via flex layout
- Brand name Montserrat bold + tagline muted

---

## 7. Internationalization (i18n)

- Languages: **English (`en`)** and **Turkish (`tr`)**
- Session-based switch via `/set-language/{code}/?next=…`
- All UI strings live in `clinic/context_processors.py` → `UI_TEXTS`
- Templates use `{{ texts.key }}` — never hardcode user-facing strings in HTML
- Content fields are bilingual: `name_en` / `name_tr`, `title_en` / `title_tr`, `summary_en` / `summary_tr`
- Flags: SVG assets in `static/clinic/flags/en.svg` and `tr.svg`

---

## 8. Iconography & Imagery

- **Flags:** SVG only, circular crop, gold active state
- **Procedure default images:** `aspect-ratio` enforced, `object-fit: cover`
- **Gallery thumbs:** consistent `3/4` ratio, never stretch/distort
- **No decorative stock clutter** — medical/aesthetic context preferred

---

## 9. Accessibility Baselines

- `.sr-only` for screen-reader-only labels (language picker)
- Modal: `role="dialog"`, `aria-modal="true"`
- Visible focus on flag buttons and stretched card links
- Sufficient contrast: white text on navy heroes/headers; dark text on white cards
- Keyboard: `Escape` closes modals/lightbox; arrows navigate lightbox

---

## 10. CSS Architecture Rules

1. **All design tokens** belong in `:root` at the top of `styles.css`
2. **Do not** inline styles in templates except unavoidable dynamic cases
3. **Do not** add one-off hex colors — extend `:root` tokens first
4. New components should reuse: `.btn`, `.form-card`, `.hero`, `.card`, `.pair-section`
5. Modals/lightbox z-index stack: modals `55`, gallery modal `60`, image preview `65`, nav `20`
6. Hidden overlays **must** include `[hidden] { display: none !important }` when CSS sets `display: grid/flex`

---

## 11. JavaScript UI Modules

| File | Responsibility |
|------|----------------|
| `lightbox.js` | Fullscreen gallery modal, before/after mode toggle, vertical image scroll |
| `procedure-search.js` | Instant case-insensitive procedure name filter on home page |
| `modal.js` | Open/close app modals, body scroll lock |
| `gallery-form.js` | Dynamic section/row add, field reindex on submit |

Keep JS vanilla — no framework required for UI interactions.

---

## 12. Do / Don't Quick Reference

### Do

- Use Montserrat + Inter
- Prefer dark navy for header, footer, hero, primary buttons
- Use gold sparingly for luxury accents
- Keep generous page gutters and card spacing
- Maintain 3-column before/after section grid on desktop
- Give every gallery image a title (EN/TR)
- Test modals don't block page when hidden

### Don't

- Don't use Playfair, script, or "tahriri" fonts for headings
- Don't fill primary buttons with bright `#3FA9F5` — use navy gradient
- Don't use emoji for language flags
- Don't let images break layout (always use thumb wrapper + aspect-ratio)
- Don't hardcode UI strings — use `UI_TEXTS`
- Don't remove starfield/glow without explicit user request

---

## 13. File Map (UI-related)

```
templates/
  base.html                 # Shell, nav, footer, lightbox, scripts
  clinic/home.html            # Procedure card grid + search bar
  clinic/procedure_detail.html  # Before/after case card grid
  clinic/manage_content.html  # Admin dashboard cards
  clinic/partials/modals.html # Add procedure / gallery modals
  clinic/partials/gallery_upload_fields.html
  registration/login.html     # Auth split layout

static/clinic/
  styles.css                  # All design tokens & components
  lightbox.js
  procedure-search.js
  modal.js
  gallery-form.js
  flags/en.svg, tr.svg
```

---

## 14. Future UI Checklist

Before shipping UI changes, verify:

- [ ] Colors match `:root` tokens and 60/25/10/5 balance
- [ ] Headings use Montserrat, body uses Inter
- [ ] Page gutters and footer sticky layout intact
- [ ] Cards/sections responsive at ≤860px
- [ ] New strings added to `UI_TEXTS` (en + tr)
- [ ] Modals/lightbox hidden state works on page load
- [ ] Gallery images have titles and consistent thumb sizing
- [ ] Dark navy chrome preserved (nav, footer, hero)

---

*Last updated: July 2026 — MediClinic aesthetic surgery clinic project.*
