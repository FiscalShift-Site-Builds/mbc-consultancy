# MBC Consultancy — website

Static site for MBC Consultancy (Bulawayo, Zimbabwe): regulatory compliance,
auditing, accounting and fiscalisation.

Built from the Claude Design prototypes in `project/`. No framework, no
third-party requests, no build step on the host.

## Quick start

```bash
python3 build.py --check      # regenerate site/ and verify it
python3 tools/serve.py        # preview at http://127.0.0.1:8000
```

## Layout

```
src/                 authoring source — EDIT HERE
  layout.html        page shell: head, meta, JSON-LD
  partials/          header (nav) and footer, defined once
  pages/             per-page content only
  assets/            css, js, self-hosted font, images
  _headers           security headers + caching (Cloudflare)
  _redirects         old prototype URLs -> new paths
build.py             assembles src/ into site/, with checks
site/                BUILD OUTPUT — committed, deployed. Do not edit.
functions/api/       Cloudflare Pages Function for the contact form.
                     Must stay at the repo root, not inside site/.
tools/               dev server, brand-image generator
docs/DEPLOY.md       deployment + contact-form setup
docs/GAPS.md         what still needs a decision before launch
project/             the original design prototypes, kept for reference
```

Edit `src/`, run `build.py`, commit both. Anything written directly into
`site/` is overwritten by the next build.

## Pages

`/` · `/compliance` · `/services` · `/fiscalisation` · `/about` · `/contact`,
plus `/thanks` and a `404`.

## Picking this up locally

This archive is the whole git repository — five commits, history already clean,
`origin` pointed at the deployment repo. Unzip it and:

```bash
cd mbc-consultancy
git log --oneline          # five commits, main checked out
python3 build.py --check   # regenerate site/ and verify
python3 tools/serve.py     # preview at http://127.0.0.1:8000
git push -u origin main    # deploy
```

The push needs write access to
`FiscalShift-Site-Builds/mbc-consultancy`; it could not be done from the
session that built this, whose sandbox would not authorise that repository.

Nothing else is required — there is no dependency install and no build step on
the host. `build.py` needs only Python 3; the image generator in `tools/` is the
one exception and needs Pillow, but you only need it if the palette or wordmark
changes.

## Before it goes live

Three things need action — see **[docs/GAPS.md](docs/GAPS.md)**:

1. Set the real domain (`MBC_SITE_URL`) — canonical, Open Graph and sitemap
   URLs are placeholders until you do.
2. Connect the contact form — it currently falls back to WhatsApp because no
   mail provider is configured. See [docs/DEPLOY.md](docs/DEPLOY.md) §3.
3. Confirm or remove the unsourced claims listed in GAPS.md §A1 — including
   "licenced ZIMRA tax agent" and "award-winning consultant".
