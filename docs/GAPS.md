# Gap scan — what was missing, what was fixed, what still needs you

Result of auditing the six Claude Design prototypes in `project/` against the
question "what stops this being deployable?", plus what the rebuild changed.

**Section A needs decisions from you. Section B is done. Section C is optional.**

---

## A. Still open — needs your input

### A1. Claims on the site that nothing has sourced

These are the highest-risk text on the site, because a compliance firm is held
to what it publishes.

| Claim | Where | Status |
| --- | --- | --- |
| "Licenced ZIMRA tax agent" | top bar of **every** page, About, Tax advisory | No agent number anywhere. Please confirm it is current. |
| "Led by an award-winning consultant" | About | No award named. Asked for twice in the transcripts, never supplied. |
| "Incorporated in Zimbabwe" | About, footer | No company number or year. |
| "8 accounting systems supported" | Home, Fiscalisation | Kept, because the Fiscalisation page lists exactly 8. Confirm the platform supports all 8. |
| "Real time transmission to FDMS" | Home, Fiscalisation | Kept — describes how VFD software works rather than a performance promise. |
| "We use what you send here only to reply to your enquiry. No mailing list." | Contact form | I wrote this, and the build honours it. Confirm you are happy to commit to it. |
| "Start with a free compliance check" — what it covers, "No charge" | Home, Compliance, Contact lede | **New.** Built from the client's own note, *"We do free compliance checks. And assessment."* The three bullets (registration status, outstanding returns, what to fix first) are my wording for what a check plausibly covers — confirm they match what is actually done for free, and whether there is a limit on it. |

**Softened on your instruction** (was unsourced, now non-numeric): "48 hrs
average go-live" → "Rapid — go-live after sign-up"; "24/7 FDMS monitoring" →
"Ongoing — FDMS monitoring"; "No card up front" → removed; "A 20-minute
walkthrough" → "A walkthrough". The originals are in git if you can source them.

**Not added, per your instruction to leave them out:** founding year, award
name, ZIMRA agent number, a WhatsApp number distinct from the mobile line.

### A2. ~~The logo you supplied does not match the site's identity~~ — placed

**Done.** The client's note — *"the logo can't be seen"* — settled the open
question in favour of using their artwork rather than the typeset wordmark.

There was no vector master: the PDF turned out to embed the same 691×418 bitmap
as the white-background JPEG. The sharpest original is the light-on-black JPEG
(969×362 of logo), so `tools/trace_logo.py` traces that into SVG once, and every
brand surface now comes off it:

| Surface | Asset |
| --- | --- |
| Header, every page | `mbc-mark.svg` at 40px (34px on mobile) |
| Footer, every page | `mbc-mark-light.svg` at 46–58px |
| Favicon, app icons | the tick, tinted cyan on `--teal-900` |
| Share card (`og.png`) | the mark in the on-dark colourway |
| Full lockup master | `tools/brand/mbc-logo{,-light}.svg` |

Two deliberate departures from the supplied artwork, both worth confirming with
the client:

- **Letters at `#8D8D8D`, not `#B8B8B8`.** The white-background file sets them
  at `#B8B8B8`, which is 1.9:1 on white — faint enough to reproduce the
  complaint that started this. `#8D8D8D` is the same silver measured off their
  own light-on-black file and reads at 3.3:1.
- **The tick goes `--cyan-300` on dark ground.** The logo teal `#1E6360` on the
  `--teal-900` footer is too close in value to read; the site's own cyan keeps
  the tick as the loudest thing in the mark.

**The tagline is not on the site.** "MASH BUSINESS CONSULTANCY" is 5% of the
lockup's height — it needs the logo about 180px tall before it is legible, which
no placement on the page gives it. So the mark carries the tick and letters, and
the firm's name is re-set beside it in Archivo, where it stays sharp at any
size. The full lockup is kept in `tools/brand/` for print and stationery.

That leaves the naming question open but no longer contradictory: the logo and
the header now both say **Mash Business Consultancy**, while body copy and the
page titles still say **MBC Consultancy**. That reads as legal name vs. short
name, which is normal — but if the client wants one of the two everywhere, it is
a find-and-replace in `src/pages/` plus the `PAGES` table in `build.py`.

### A2b. Three things the client's own uploads say that the site does not

`project/uploads/` is eight screenshots of the client's **WhatsApp Business
catalogue**. Read for imagery they were no use — flyers with baked-in text at
486×1080, and the people in them are stock photography inside those flyers, not
the firm. But they answer three open questions:

| Their catalogue says | The site says |
| --- | --- |
| **Mildred Mashingaidze**, "award-winning business consultant. Expert guidance on CIPZ, ZIMRA, NSSA, NEC & PRAZ" | "Led by an award-winning consultant" — no name (A1) |
| TaRMS Registration **US$100**, Compliance Packages **US$50** | prices removed, "Request a quote" |
| A **Master of Ceremonies / moderator** service — social, corporate, educational and cultural events | not mentioned anywhere |

None of this is on the site, and all three are the client's call:

- **The name.** "Led by an award-winning consultant" is weak precisely because
  it is anonymous. Naming Mildred Mashingaidze on About, with the award, would
  do more for trust than anything else available. The award still needs naming
  — the catalogue asserts it without saying which.
- **The prices.** Publishing a from-price generally makes prospects
  self-select better than "request a quote" does, and the numbers are already
  public in their own catalogue, so the site is the only place hiding them.
- **The MC service.** It sits oddly against a compliance brief and may be
  deliberately kept separate. Worth one question rather than an assumption.

Also note the catalogue leans **green**, where the site is teal/cyan. If the
catalogue is staying in circulation, one of the two should move.

### A2c. ~~The photography is stock~~ — stock is the decision

Seven Unsplash photographs are on the site, one per page plus a second on
Services, all free-licensed for commercial use and all recorded in
**[docs/photo-credits.md](photo-credits.md)** with photographer, photo id and
placement. Confirmed as the finished set; nothing here is waiting on the client.

Two constraints came with the licence and are written up in that file. They are
settled rather than open, but they bind future edits:

- The home band shows identifiable people who do not work for MBC. Ordinary
  editorial use as built — but it must never be captioned "our team", given a
  name, or paired with a testimonial, because that converts permitted use into
  an implied endorsement.
- The Contact band is a real Bulawayo building that is **not** 58 Fife Street.
  Copy over it stays at city level; the address stays in the Reach us block. A
  draft headline reading "58 Fife Street, Bulawayo." over that frame was caught
  and changed.

### A3. The public email is a personal Gmail

`mmazha800@gmail.com` is the firm's contact address on every page. Against a
brief asking for "precision, reliability and deep regulatory knowledge", a
firm-domain address would carry more weight — and it is required anyway before
the form can send from your own domain (see `DEPLOY.md` §3).

### A4. No privacy notice

The site now collects names, emails and phone numbers through a form. There is
no privacy page. For a firm that sells compliance this is a conspicuous gap. A
short page covering what is collected, why, where it is stored and how to have
it deleted would close it — happy to draft one.

### A5. Fiscal Shift's outbound links are unverified

`fiscalshift.co.zw/login/`, `/register/`, `/how-it-works/` and `/contact/` are
linked from the Fiscalisation page. This environment could not reach
`fiscalshift.co.zw` (HTTP 403), so **none of the four were confirmed to exist**.
Worth one manual click each before launch.

### A6. "Accounting" in the nav opens a page titled "Other services"

The nav pill says **Accounting**; the page it opens is headed *"Other services —
Audit, accounting, tax and governance under one engagement"*, where accounting
is section 02 of 5. Chat 3 fixed the three visible pills as Compliance /
Accounting / Fiscalisation, so I kept them, and the pill now links to the top of
the page rather than mid-scroll into `#accounting`.

It still reads slightly off. Cleanest fix is renaming the page heading to
"Accounting & advisory" and leading with accounting. Your call.

---

## B. Fixed in this rebuild

### B1. It was not deployable at all

The prototypes were **not web pages**. Each was a React application: `support.js`
is a 1,900-line design-canvas runtime that parses `<x-dc>` markup and renders it
through React pulled from unpkg, with GSAP from jsDelivr and fonts from Google.
Consequences: nothing rendered without JavaScript, search engines got an empty
page, and three third-party CDNs sat on the critical path.

Now: static HTML with a 30 KB stylesheet and a 12 KB script, **no third-party
requests at all**. Archivo is self-hosted as two variable-font subsets (68 KB
for all four weights, SIL OFL, licence included).

### B2. GSAP replaced — which fixed the two bugs you kept hitting

The transcripts show the same two problems recurring across many rounds:
content *"stranded"* invisible, and page transitions *"mostly broken"*. Both
were structural to the approach, so rather than patch them again:

- **Stranded content** happened because GSAP set `opacity: 0` from JavaScript;
  if a tween was built over nodes that had not streamed in yet, content stayed
  hidden. Now the hidden state lives in CSS behind a `.js` class set before
  first paint, revealed by IntersectionObserver, with a 2.5-second failsafe and
  a global error handler that reveals everything. **Script cannot hide content —
  only reveal it.** Verified: with JavaScript disabled, all 21 animated
  elements render visible.

- **The pinned "Five doors" scene** used ScrollTrigger's `pin`, which desynced.
  It is now `position: sticky` — the browser owns the pinning, so it cannot
  drift. Scroll progress lights each authority in turn and drives the
  cyan-to-rose bar. Verified at four scroll depths: 1→2→4→5 lit, bar 0→1.


- **Page transitions** only had the exit half, and the click handler keyed off
  `href.endsWith('.dc.html')`. Now: the arrival curtain is pure CSS so it runs
  without waiting for a download; the exit wipe always navigates even if
  `transitionend` never fires; and it correctly ignores modifier-clicks,
  `target=_blank`, downloads, external origins, `mailto:`/`tel:`, and same-page
  anchors. It also resets on back-button restore — previously a restored page
  would have come back still covered by the teal panel.

All motion now respects `prefers-reduced-motion`, which the CSS entry curtain
and smooth-scroll previously ignored.

**Motion parity was audited afterwards, and the first pass had dropped three
things.** All are restored:

| Prototype behaviour | First pass | Now |
| --- | --- | --- |
| Hero bloom parallax (`yPercent 18`, `xPercent -6`, scrubbed over 900px) | Dropped entirely — the bloom was static | `data-parallax`, rAF scroll handler, exact same extent |
| Chooser rows: separate tween, `delay .3`, `stagger .07` | Merged into one flat 90ms cascade, landing at 990ms instead of 650ms | Own group, 300ms base + 70ms step |
| Service cards: one trigger, `stagger .12` | Each card revealed independently, so on desktop all three fired at once and the left-to-right cascade was lost | Group reveal, 120ms step, fired by the first card |

The full behaviour-by-behaviour coverage table is in the commit for that fix;
all thirteen distinct motion behaviours in the prototype logic are now
accounted for, with 15 dedicated tests covering the three above.


### B3. Six copies of the header and footer, already drifting

Header, footer and the ~60-line motion script were duplicated in all six files,
and had diverged: the home page's top bar was missing the phone number, its
breakpoint was 1040px where others used 900px, and Contact's "Book a
consultation" pill was a different colour with a hover state that changed
nothing.

Now one `src/layout.html` plus `src/partials/`, assembled by `build.py`. A check
asserts the footer is byte-identical across all pages.

### B4. Mobile navigation

Five pills plus the wordmark simply wrapped — roughly four stacked rows, with
the sticky header eating a fifth of a phone screen. Now the horizontal
scrolling carousel you asked for: scroll-snapping strip, edge-fade masks,
chevron buttons that appear only when there is overflow and disable at each end,
and the current page's pill scrolled into view on load. It reacts to measured
overflow rather than a breakpoint, so it never triggers when the pills fit.
Header is now 142px on a 390px-wide screen, down from 167px.

### B5. Everything a page needs to be indexed or shared

None of the prototypes had a `<title>`. Also missing: meta descriptions,
canonical URLs, Open Graph and Twitter cards, `lang`, favicon, `robots.txt`,
`sitemap.xml`, a 404 page, and structured data.

All present now, per-page, from one table in `build.py` — plus an
`AccountingService` JSON-LD block with the address and service areas, and a
generated 1200×630 share card. That card matters more than usual here: your
audience shares links on WhatsApp, and without one a shared link is bare text.

### B6. Accessibility

- **Focus states**: the prototypes had `:hover` only, so keyboard users got no
  indication of position at all. Every interactive element now has a visible
  focus ring, and a skip link is the first tab stop.
- **Contrast**: four palette tokens failed WCAG AA at the small sizes they were
  used at. The top-bar grey was 3.55:1, the cyan eyebrows 3.48:1, the rose
  numerals 2.99:1, the footer sub-label 3.96:1. All four were nudged along
  their own hue until they cleared 4.5:1 (now 4.62, 5.18, 4.95, 5.54). The
  change is subtle but it matters — chats 1 and 2 both asked for a design that
  "appeals to the older generation".
- **Structure**: added a `<main>` landmark; card and row titles that were
  `<span>`s at 38px are now real headings, so the document has an outline;
  `aria-current="page"` marks the nav; decorative `→` glyphs are hidden from
  screen readers; carousel chevrons are out of the tab order since the links
  they scroll to are already reachable.

### B7. Anchor links landed underneath the sticky header

`scroll-margin-top: 140px` was hard-coded, but the header is a different height
on mobile. The header is now measured at runtime — including after the webfont
swaps — into a custom property that drives `scroll-padding-top`.

### B8. Security headers and a form that cannot be abused

Added CSP, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` and
`Permissions-Policy`. The CSP allows no inline scripts; the one inline boot
script is allow-listed by SHA-256 **computed at build time**, so it cannot drift
out of sync. (`'unsafe-inline'` is allowed for *styles* only — the pages carry
inline `style` attributes inherited from the prototypes, and styles cannot
execute.)

The form endpoint validates server-side rather than trusting the browser,
strips CR/LF so a name cannot inject mail headers, caps field lengths, and
verifies Turnstile when configured.

### B9. Other fixes

- `© 2026` was hard-coded; now set from the clock.
- Old prototype URLs (`/MBC%20Contact.dc.html` and friends) 301 to the new
  paths, along with likely guesses like `/accounting` and `/contact-us`.
- Fiscalisation's "Start subscription / How it works" pair no longer crushes
  itself at 360px.
- Contact's mobile hero no longer loses its bottom padding.

---

## C. Worth considering, not blocking

- **Monospace drift.** The eyebrow labels use `ui-monospace`, which resolves to
  a different face on every platform — Menlo on Mac, Consolas on Windows,
  DejaVu on Android. The design leans on those labels heavily. A webfont mono
  (~15 KB) would make it consistent; system mono costs nothing.
- **No analytics.** Cloudflare Web Analytics is free, needs no cookie banner,
  and is one dashboard toggle.
- **The three "packages"** now say "Request a quote" with prices removed, as you
  asked. Prospects generally self-select better with a from-price or a range.
- **Testimonials / client logos.** The strongest available trust signal, and the
  site currently has none.
- **No CI.** `python3 build.py --check` exits non-zero on failure, so it would
  work as a GitHub Action to stop a broken `site/` being committed.
- **`project/uploads/`** holds 8 WhatsApp screenshots from the client: the
  source of the MBC logo, a TaRMS service listing, and event flyers. Kept as
  source material. Note the TaRMS listing shows a USD 100 price, which is
  worth reconciling against the decision to remove prices from the site.

---

## How this was verified

Not by inspection alone — the pages were rendered in Chromium:

- **23 functional tests**: no-JS rendering, reduced-motion, form validation,
  the WhatsApp fallback preserving what was typed, focus order, `aria-current`,
  transition edge cases, counters.
- **15 motion-parity tests**: parallax extent and cap, entrance group timings,
  the card cascade firing from one trigger, and all of it suppressed under
  reduced motion.
- **15 endpoint tests** against the contact function: honeypot, validation,
  Turnstile accept/reject, CRLF header-injection stripping, Reply-To routing,
  the no-JavaScript redirect path, field-length caps.
- **Render checks** on all six pages at 1440px and 390px: no console errors, no
  failed requests, no horizontal overflow, nothing left invisible after
  scrolling.
- Contrast ratios computed arithmetically; HTML checked for balanced tags and
  duplicate ids; both scripts syntax-checked.

Two things could **not** be verified here and are called out above: the Fiscal
Shift links (A5), and live email delivery, since Resend needs an account key
(`DEPLOY.md` §3). The Cloudflare research behind the form recommendation was
also gathered from search summaries rather than the docs themselves — the
network blocked direct access — so spot-check current free-tier limits before
relying on them.
