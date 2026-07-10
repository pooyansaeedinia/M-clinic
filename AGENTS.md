# AGENTS.md — MediClinic Project Guide

Instructions for AI agents working on this repository.

## Project Overview

**MediClinic** is a Django web application for an aesthetic/plastic surgery clinic. It displays cosmetic procedures, before/after gallery sections, bilingual content (English + Turkish), and authenticated content management.

**Stack:** Django 6, SQLite, server-rendered templates, vanilla CSS/JS (no React/Vue).

## Key Commands

```bash
# Run dev server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Seed default procedures
python manage.py seed_procedures

# System check
python manage.py check
```

## Project Structure

```
M_clinic_2/           # Django project settings & urls
clinic/               # Main app (models, views, forms, static, migrations)
templates/            # Django HTML templates
manage.py
DESIGN-LANGUAGE.md    # ← UI/UX design system (READ BEFORE UI CHANGES)
```

## Design Language — REQUIRED READING

**Before any UI, UX, CSS, or template work, read and follow:**

→ **[DESIGN-LANGUAGE.md](./DESIGN-LANGUAGE.md)**

That document defines:

- Color palette & 60/25/10/5 usage ratio
- Typography (Montserrat headings + Inter body)
- Dark navy theme for header, footer, hero, primary buttons
- Gold accent rules
- Component patterns (cards, modals, lightbox, gallery sections)
- Spacing, grids (3-column before/after sections)
- i18n conventions (EN/TR via `UI_TEXTS`)
- Animation (starfield background)
- Do/Don't list

**Do not introduce UI that contradicts DESIGN-LANGUAGE.md** unless the user explicitly requests a design change — then update both the implementation and DESIGN-LANGUAGE.md.

## Coding Conventions

### Django

- App name: `clinic`
- Bilingual content fields: `*_en` and `*_tr` suffixes
- UI strings: `clinic/context_processors.py` → `UI_TEXTS` (never hardcode in templates)
- Auth-required views: `@login_required` decorator
- Static files: `static/clinic/` (project root — no collectstatic needed in development)
- **Image uploads:** JPG, JPEG, PNG, WebP, and GIF (animated GIFs preserved). Shared validation in `clinic/validators.py` — use `validate_image_upload` and `ALLOWED_IMAGE_ACCEPT` on all image form fields and file inputs.

### Templates

- Extend `base.html` for all pages
- Use `{% static %}` for assets
- Use `{{ texts.key }}` for translated UI labels
- Modals in `clinic/partials/modals.html`
- Gallery upload fields in `clinic/partials/gallery_upload_fields.html`

### CSS

- Single stylesheet: `static/clinic/styles.css`
- Define new colors as `:root` CSS variables first
- Match existing class naming (`.btn-*`, `.hero`, `.card`, `.pair-section`, etc.)

### JavaScript

- Vanilla JS only in `static/clinic/`
- Modals must respect `[hidden]` attribute (see DESIGN-LANGUAGE.md §6.6)
- Gallery form field naming: `s{section}_{b|a}{index}_{field}` — map `b`→`before`, `a`→`after` in backend
- **Gallery lightbox (`lightbox.js`):** case cards open the gallery modal; slide images open the nested preview lightbox. Open preview on the `click` event (not `pointerup`) so the synthesized click does not ghost-close the preview backdrop. Use pointer movement tracking to distinguish scroll drags from taps. CRUD overlays must use `pointer-events: none` when hidden. Preview closes only via backdrop, close button, or `Escape` — not dialog-padding clicks.

## Data Model (Gallery)

```
Procedure
  └── GallerySection
        └── SectionImage (title_en, title_tr, image, image_type: before|after)
```

Each **section** has two parts (Before / After). Each part can contain **multiple titled images**.

## i18n

- Languages: `en`, `tr`
- Switch URL: `/set-language/{code}/?next={path}`
- Session key: `lang`
- Flag icons: SVG at `static/clinic/flags/en.svg` and `tr.svg`

## UI Change Checklist

When modifying frontend:

1. Read **DESIGN-LANGUAGE.md**
2. Use existing CSS tokens and component classes
3. Add EN + TR strings to `UI_TEXTS` if needed
4. Verify responsive behavior at ≤860px
5. Verify modals/lightbox hidden on page load
6. Run `python manage.py check`

## What NOT to Do

- Do not use script/serif fonts for headings (user prefers Montserrat)
- Do not use bright blue as primary button fill (use dark navy gradient)
- Do not use emoji flags
- Do not commit `.env` or secrets
- Do not create git commits unless the user asks
- Do not add markdown/docs files unless requested (except this file and DESIGN-LANGUAGE.md)

## Static Files

All static assets live in the project root:

```
static/
  clinic/
    styles.css
    lightbox.js
    procedure-search.js
    modal.js
    gallery-form.js
    flags/en.svg, tr.svg
```

**Settings (`M_clinic_2/settings.py`):**
- `STATIC_URL = '/static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`

In development (`DEBUG=True`), static files are served directly from `static/` — **no `collectstatic` needed**.

Templates still use: `{% static 'clinic/styles.css' %}`

## Allowed Hosts

Default: `127.0.0.1,localhost,testserver` — override with `DJANGO_ALLOWED_HOSTS` env var.

## Hidden Portal (Chat Templates)

A separate internal UI lives at **`/internal/`** — it is **not linked** from the public site.

| Path | Purpose |
|------|---------|
| `/internal/` | Portal login |
| `/internal/dashboard/` | Language list (CRUD) |
| `/internal/language/<code>/` | Template sections for a language |
| `/internal/country/<code>/` | Alias of language page |
| `/internal/logout/` | Sign out (POST) |
| `/internal/api/languages/` | Language list/create (JSON) |
| `/internal/api/languages/<id>/` | Language get/update/delete |
| `/internal/api/languages/<id>/sections/` | Section list/create |
| `/internal/api/sections/<id>/` | Section get/update/delete |

**Architecture (keep separate from public MediClinic UI):**

```
clinic/portal.py              # Session auth, default languages/flags, decorator
clinic/portal_views.py        # Login, dashboard, language CMS + JSON APIs
clinic/portal_templates.py    # Language/section serialization & validation
clinic/portal_urls.py         # Portal URLconf (included in M_clinic_2/urls.py only)
clinic/models.py              # ChatTemplateLanguage, ChatTemplateSection
templates/portal/             # Standalone templates (extend portal/base.html)
templates/portal/partials/    # Reusable modals
static/portal/                # Portal-only CSS + templates.js
static/portal/languages/      # PNG/JPG language card images
```

- Portal auth uses session key `portal_authenticated` — **not** Django `User` auth.
- Do not extend `templates/base.html` or reuse `static/clinic/styles.css` for portal pages.
- Languages are DB-managed (`ChatTemplateLanguage`: name, language_name, code, image). Card images are PNG/JPG under `static/portal/languages/` with upload/replace/remove in the language modal. English is always sorted first. Defaults seed from `DEFAULT_LANGUAGES` in `clinic/portal.py`.
- Sections (`ChatTemplateSection`: title + body) use modal CRUD via JSON APIs; extend with `metadata` / `tags` / `variables` / `template_type` when needed.
- Portal static files live in `static/portal/`. With `DEBUG=False`, run `python manage.py collectstatic` before production deploy so `/static/portal/` assets are included in `staticfiles/`.
