# Deploying the MBC Consultancy site

The site is plain static HTML, CSS, JS and fonts. It has no runtime framework
and no build step on the host: `site/` is committed ready to serve.

---

## 1. GitHub Pages — the current deployment

`.github/workflows/pages.yml` builds `src/` and publishes `site/` on every push
to `main`. Nothing to configure per deploy; the workflow is the whole setup.

The site is served from a **project-site sub-path**:

    https://fiscalshift-site-builds.github.io/mbc-consultancy/

That sub-path is the one thing to understand about this deployment. Every link
and asset reference in `src/` is root-absolute (`/about`, `/assets/css/mbc.css`),
which resolves against `github.io/` — the wrong root — unless it is prefixed.
So `build.py` derives a base path from the *path component of `MBC_SITE_URL`*
and prepends it to every root-absolute URL in the HTML, the manifest,
`robots.txt`, `_headers` and `_redirects`:

```bash
MBC_SITE_URL=https://fiscalshift-site-builds.github.io/mbc-consultancy python3 build.py --check
```

One variable drives both the absolute URLs (canonical, Open Graph, JSON-LD,
`sitemap.xml`) and the base prefix, so they cannot disagree. `tools/serve.py`
reads the same variable, so a local preview serves the same URLs:

```bash
MBC_SITE_URL=https://fiscalshift-site-builds.github.io/mbc-consultancy python3 tools/serve.py
# → http://127.0.0.1:8000/mbc-consultancy/
```

Set `MBC_SITE_URL` in the workflow's `env:` block to change where the site is
published. Point a custom domain at Pages and the path component disappears,
the base prefix becomes empty, and every rewrite is a no-op.

### What does not carry across

| File | On GitHub Pages |
| --- | --- |
| `functions/api/contact.js` | **Not run.** Pages serves static files only. |
| `_headers` | Ignored — no CSP, no cache-control, no `X-Frame-Options`. |
| `_redirects` | Ignored — the prototype-filename and alias redirects 404. |

The contact form is the one with a visible consequence. `POST /api/contact`
returns 404 instead of 503, `fetch` rejects, and the page shows its fallback:
*"That did not send. Nothing you typed is lost"* with a WhatsApp link carrying
everything the visitor typed, plus the email address. No enquiry is lost, but
none reaches an inbox automatically either. To take enquiries by email on
GitHub Pages, use the hosted-form option in §4 ("Alternative: skip the function
entirely") — a static host cannot run the function.

Extensionless URLs (`/about` → `about.html`) and `404.html` both work on
GitHub Pages, so those need no change.

---

## 2. Cloudflare Pages setup

Create a Pages project from this repository and set:

| Setting | Value |
| --- | --- |
| Build command | *(leave empty)* |
| Build output directory | `site` |
| Root directory | *(repository root)* |

Leave the build command empty — `site/` is already generated and committed.
`build.py` exists so the HTML can be regenerated locally, not on the host.

> **`functions/` must stay at the repository root, not inside `site/`.**
> Cloudflare reads Pages Functions from the repo root and maps the file tree
> onto URL paths, so `functions/api/contact.js` becomes `/api/contact`. Moving
> it into `site/` silently breaks the contact form.
> <https://developers.cloudflare.com/pages/functions/routing/>

`_headers` and `_redirects` are copied into `site/` by the build and are picked
up automatically.

### A note on Pages vs Workers

Cloudflare's current guidance is that **new** projects should use Workers with
static assets rather than Pages; Pages continues to work but new development
goes to Workers. Pages is the simpler path today and everything here works on
it. If you would rather start on Workers, the site files and the function port
across with no change to the HTML.
<https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/>

---

## 3. Set the domain — do this before launch

Until the real domain is set, the canonical links, Open Graph tags, JSON-LD and
`sitemap.xml` all point at the placeholder `https://mbcconsultancy.example`.
Search engines and WhatsApp link previews will be wrong.

```bash
MBC_SITE_URL=https://the-real-domain.co.zw python3 build.py --check
git add site && git commit -m "Set production domain"
```

Or edit the `PLACEHOLDER_URL` fallback near the top of `build.py`. The build
prints a warning while the placeholder is still in use.

---

## 4. Connect the contact form

The form at `/contact` posts to `/api/contact`. **Until you set the two
variables below it returns 503, and the page offers the visitor a WhatsApp
hand-off with everything they typed pre-filled** — so no enquiry is lost, but
none reaches an inbox either.

### The constraint

The obvious options do not work without a domain:

- **Cloudflare's own Email Service** would be the ideal end state — free
  forever to a verified destination address, no third party at all — but it
  requires a domain onboarded onto your Cloudflare account, because Cloudflare
  has to own the MX, SPF, DKIM and DMARC records.
- **MailChannels**, which almost every "contact form on Cloudflare" tutorial
  still recommends, shut its free Workers integration down in June 2024.
- **SendGrid's** free tier was retired during 2025.
- **Postmark** will not accept a Gmail address at signup.

So: use Resend now, and switch to Cloudflare Email Service once the domain
exists.

### Resend (works today, no domain needed)

1. Create an account at <https://resend.com> **using `mmazha800@gmail.com`**.
   This matters: with Resend's shared `onboarding@resend.dev` sender you may
   only send *to the address on your own account*. For a contact form that is
   exactly the recipient you want, so the restriction is not a problem — but
   the account address and `MAIL_TO` must match.
2. Create an API key.
3. In Cloudflare: **Workers & Pages → your project → Settings → Variables and
   Secrets**, and add these for **Production** (and Preview if you use it):

   | Name | Type | Value |
   | --- | --- | --- |
   | `RESEND_API_KEY` | Secret (encrypt) | your Resend API key |
   | `MAIL_TO` | Text | `mmazha800@gmail.com` |

4. Redeploy. Variables must exist *before* the deployment that uses them.

Enquiries arrive with **Reply-To set to the person who wrote in**, so replying
to the notification replies to them directly. The sender line will read
`onboarding@resend.dev` until step 5.

Free tier at the time of writing: 3,000 emails/month, 100/day. Worth
re-checking on their pricing page — plans in this space change often.

### Upgrading once you own a domain

Add `MAIL_FROM` (e.g. `MBC Consultancy <enquiries@yourdomain.co.zw>`) after
verifying the domain in Resend — that alone removes the Resend-branded sender
and the send-only-to-yourself restriction.

Better still, move to **Cloudflare Email Service** and drop the third party
entirely: onboard the domain, verify `mmazha800@gmail.com` as a destination
address, and sends to it are free on any plan and do not count against quota.
That needs a small change to `sendViaResend()` in `functions/api/contact.js`.
**Check the request body against the current docs before writing it** — this
was not verified during the build:
<https://developers.cloudflare.com/email-service/api/send-emails/rest-api/>

### Alternative: skip the function entirely

If you would rather not run a function or hold an API key, delete
`functions/` and point the form at a hosted form service — change one attribute
in `src/pages/contact.html`:

```html
<form action="https://api.web3forms.com/submit" method="POST" ...>
  <input type="hidden" name="access_key" value="YOUR-KEY">
```

Web3Forms needs no account (just an access key emailed to you) and allows 250
submissions/month free. The trade-off is that a third party sees every enquiry.
Keep the honeypot field, and rebuild afterwards.

---

## 5. Turn on Turnstile (recommended, free)

The form ships with a honeypot, which stops naive bots with zero setup. For
real protection add Cloudflare Turnstile:

1. Cloudflare dashboard → **Turnstile** → add a widget for your hostname.
   Free, and it does not require the site to be on Cloudflare.
2. In `src/pages/contact.html`, uncomment this line and paste the **sitekey**:

   ```html
   <div class="cf-turnstile" data-sitekey="PASTE_TURNSTILE_SITEKEY"></div>
   ```

3. Add the widget script to `src/layout.html`, before `</head>`:

   ```html
   <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
   ```

   The Content-Security-Policy in `src/_headers` already allows
   `challenges.cloudflare.com` for both `script-src` and `frame-src`.

4. Add the **secret key** as a Cloudflare secret named `TURNSTILE_SECRET`.
   The function verifies server-side only when this is present, so nothing
   breaks if you do steps 2–3 and forget step 4 — but it also is not enforced
   until you do.

5. `python3 build.py --check`, commit, redeploy.

---

## 6. Working on the site

```bash
export MBC_SITE_URL=https://fiscalshift-site-builds.github.io/mbc-consultancy
python3 build.py --check      # regenerate site/ and run the checks
python3 tools/serve.py        # preview at http://127.0.0.1:8000/mbc-consultancy/
```

Export `MBC_SITE_URL` first, or you will rebuild `site/` for a domain root and
commit links that 404 on the live sub-path. Both commands read it (§1).

`tools/serve.py` resolves URLs the way Pages does — `/compliance` serves
`compliance.html`, unknown paths serve `404.html` with a real 404, and
`_redirects` rules are honoured. It does **not** run the contact function; for
that use `npx wrangler pages dev site`.

**Edit `src/`, never `site/`.** Everything in `site/` is overwritten by the
build. The header, footer and page shell live in `src/layout.html` and
`src/partials/`, so a nav or footer change is made once and lands on all pages.

`build.py --check` verifies: no unreplaced template placeholders, no leftover
prototype artefacts, every internal link and `#anchor` resolves, every
referenced asset exists, the footer is byte-identical across pages, and each
page has exactly one `<h1>`. It exits non-zero on failure, so it works as a CI
step.

Regenerating the icons and social card (only needed if the palette or wordmark
changes) — see `tools/make_images.py`; it needs Pillow and the Archivo TTFs.

---

## 7. Pre-launch checklist

- [ ] `MBC_SITE_URL` set to the real domain and `site/` rebuilt (§3)
- [ ] `RESEND_API_KEY` + `MAIL_TO` set, and a test enquiry received (§4)
- [ ] Turnstile sitekey + secret in place (§5)
- [ ] Decide on the claims and content flagged in [`GAPS.md`](GAPS.md) §A
- [ ] Submit `sitemap.xml` in Google Search Console
- [ ] Share a link into WhatsApp and confirm the preview card renders
