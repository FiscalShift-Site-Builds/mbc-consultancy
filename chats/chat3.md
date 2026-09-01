# MBC Consultancy website design

_Started 2026-08-16 22:42 UTC_

---

## User

Continuing from "Mildred Mashingaidze design system".

## Assistant

I've reviewed the conversation—you wanted to amp up the animations and movement across the MBC site to make it feel less static. We brainstormed several directions:

- Staggered reveal sequences: hero headline staggering in word-by-word or line-by-line, services cards cascading in on scroll, compliance package cards rolling up sequentially
- Parallax and depth: subtle background shift on hero, floating service icons or stat numbers, depth layering on the Fiscal Shift process steps
- Interactive micro-interactions: regulator badges lighting up on hover with glow/pulse, compliance checklist items animating tick marks, button states with underline draws or fill animations
- Scroll-triggered effects: fade-in-and-up on all major sections as you scroll, counter animations on stats (numbers rolling up), timeline or roadmap feel on the Fiscal Shift four-step process
- Accent motion: animated gradient background on hero or compliance section, subtle looping on icons, underline or border animations on text links

The core idea: keep the professional ledger aesthetic but layer in motion that draws the eye to key sections, builds narrative flow, and feels alive without veering into novelty. Entries, exits, and interactions should all telegraph value and guide the user through the compliance/advisory story.

Ready to pick the strongest ideas and implement them across the pages—or refine any of these directions first?

[files: Mash Business Consultancy.dc.html, MBC Services.dc.html, MBC Compliance.dc.html, MBC Fiscal Shift.dc.html, MBC About.dc.html, MBC Events.dc.html, MBC Contact.dc.html]

## User

Let us now properly adjust content using the following email:

Good day Ashy,

Kindly find below as discussed 

Company Overview:
MBC Consultancy is is a professional services firm incorporated in Zimbabwe and specialises in regulatory compliance, auditing, and accounting solutions. We help businesses navigate complex statutory requirements and maintain full regulatory adherence across Zimbabwe and beyond.

Our Core Service Areas:

Statutory & Regulatory Compliance:

· NSSA (National Social Security Authority) – Registration, contributions, compliance reporting, and exemption applications
· ZIMRA (Zimbabwe Revenue Authority) – Tax compliance, PAYE, VAT, corporate tax, customs & excise, and dispute resolution
· CIPZ (Companies and Intellectual Property of Zimbabwe) – Company Registrations and Re-registration 
· PRAZ (Procurement Regulatory Authority of Zimbabwe) Registration 
· Vendor Registration(Ministry of Finance)– Assistance with registration on supplier databases, tender portals, and government procurement platforms

Auditing & Assurance:

· Statutory audits
· Internal audits
· Risk assessments and internal controls review

Accounting & Financial Services:

· Bookkeeping and financial record keeping
· Financial statement preparation (IFRS compliant)
· Management accounts
· Payroll management and statutory deductions

Tax Advisory:

· Tax planning and structuring
· ZIMRA liaison and dispute resolution
· VAT and customs advisory

Corporate Governance & Secretarial:

· Board advisory and compliance frameworks
· Annual returns and company registrations
· Regulatory filings with relevant authorities

Training & Capacity Building:

· Compliance training for finance, procurement, and HR teams
· Workshops on regulatory updates and best practices.

Core Requirements:

· Brand Image: Clean and professional — conveying precision, reliability, and deep regulatory knowledge
Cyan,Grey and White 
· Key Pages: Home, About Us, Compliance,Fiscalisation,Other Services,Contact us (email,What's app number,business address-58 Fife Street, Bulawayo)


Timeline:
Target launch: a date from you perhaps 

Kind regards,

Mashingaidze Mildred
Managing Consultant
MBC Consultancy
58 Fife Street
Bulawayo 
Zimbabwe
mobile:+263 774121012
email:mmazha800@gmail.com

## Assistant



## Assistant

_[tool: read_file]_

Before I rework seven pages, five calls that change everything downstream.

_[tool: ask_user]_

Waiting on your answers — mainly the name, the cyan/grey/white call, and whether Events stays. Once those land I'll rebuild all pages in one pass.

## User

Answered — Asked for follow-up questions; name: MBC Consultancy; palette: Switch fully to cyan / grey / white; pages: Match the email exactly — retire the Events page; scope: Auditing & assurance, Accounting & financial services, Tax advisory, Corporate governance & secretarial, Training & capacity building, Vendor registration (Ministry of Finance); pricing: Remove prices, show packages only

## Assistant



## Assistant

_[tool: ask_user]_

Round two is up — cyan's register, the logo, and how firm-first About Us should be.

## User

Answered — Asked for follow-up questions; cyan_temper: Deep teal-cyan as the dark anchor, bright cyan only for accents — closest to the current site's weight; logo: Wordmark only — set MBC in type; serif: Switch to all sans — cleaner, more technical; fiscalisation: Keep it as the Fiscal Shift partnership page, lightly renamed; mildred: Firm only, no personal profile

## Assistant



## Assistant

_[tool: ask_user]_

_[tool: ask_user]_

Final round is up — typeface, trust signals, and the home page spine.

## User

Answered — Asked for follow-up questions; sans: Neue Haas Grotesk-style — tight, neutral, Swiss (via Archivo); credentials: Licenced ZIMRA tax agent, Award-winning consultant, Incorporated in Zimbabwe, Years in practice; home_shape: Problem-led — lead with the cost of non-compliance, then the service areas; cta: Book a consultation

## Assistant



## Assistant

_[tool: ask_user]_

Waiting on the facts — founding year, award name, WhatsApp number, and which non-compliance pain leads the hero. Blank fields just mean I leave those claims out.

## User

Answered — problem: Penalties and interest — what ZIMRA and NSSA charge for late or missed filings

## Assistant

_[tool: read_file]_

_[tool: dc_write]_

_[tool: dc_write]_

_[tool: read_file]_

_[tool: dc_write]_

_[tool: dc_write]_

_[tool: dc_write]_

_[tool: dc_write]_

_[tool: delete_file]_

_[tool: ready_for_verification]_

Six pages rebuilt on the email: Home, About Us, Compliance, Fiscalisation, Other Services, Contact. New identity — MBC Consultancy wordmark, deep teal-cyan anchor with bright cyan accents on white and cool grey, all-sans (Archivo). Home leads on penalties and interest, then the six service areas. Events, the old Services page and the green palette are gone.

Two things left open because you didn't supply them: package prices are removed and replaced with "request a quote", and the trust signals say "award-winning consultant" and "incorporated in Zimbabwe" with no award name, year founded, or ZIMRA agent number. Send those and the WhatsApp number if it differs from the mobile, and I'll drop them in.

## User

Found issues — fixing…

## User

Found issues — fixing…

## User

Now I want us to plan the following out. We need to make the different services visible in the navbar(Which will mean having the compliace, accounting and fiscalization links visible. Preferably as buttons which means the nav bar needs a redesign to match the theme).

The next thing is the site flow. The theme for the site should be: A client lands on the site, meets a minimal home page that highlights the services and then is led to explore by a flow. The site should itself be a flow nott that we need some tutorial and this means minimizing the homepage to just a beautiful highlight of the services offered. The site needs color as well following the color scheme specified in the email(needs some femininity in a sense. Mildred is a woman who loves her color). This will also mean some good animations leveraging gsap if possible.

Let us plan this. As as many questions as you need to.

## Assistant



## Assistant

_[tool: ask_user]_

Questions are up — the flow mechanism, where the warmth comes from, and whether I build home first or all six at once are the ones that shape everything else.

## User

Answered — nav_style: option_2; home_keeps: The three service buttons, large, The five authorities (NSSA, ZIMRA, CIPZ, PRAZ, Vendor), The Fiscal Shift partnership; flow: Choose-your-path — home asks what you need, and each answer routes into the right page; colour: Cyan + a warm rose accent — softest, clearly feminine, still professional; colour_amount: Accents only; motion: Reveal on scroll — sections and text rise in as you reach them, Pinned scenes — a section holds while its content plays out, then releases, Element choreography — numbers count, lines draw, cards sta…; shape: Mix — sharp…

## Assistant

_[tool: dc_write]_

_[tool: show_html]_

_[tool: ready_for_verification]_

New home is up as **MBC Consultancy v2** — the old one is untouched until you approve.

What's in it:
- Pill nav with Compliance, Accounting and Fiscalisation as visible buttons, plus a filled Book a consultation
- Minimal hero: one statement, and a "Where would you like to start?" chooser routing six intents into the right page
- Three large service blocks, the five authorities, the Fiscal Shift band, one contact line. Nothing else
- Rose accent (#D9788C) against the cyan and teal, accents only, sharp structure with soft buttons
- GSAP: hero lines rise, cards stagger, the authorities section pins while the five roll in with a cyan-to-rose progress bar, the Fiscal Shift numbers count, and a teal wipe covers page changes

Approve it and I'll roll the nav, palette, motion and flow across Compliance, Accounting, Fiscalisation, About and Contact.

## User

Found issues — fixing…

## Assistant

_[tool: dc_write]_

_[tool: ready_for_verification]_

Fixed the stranded hero: intro copy now animates with explicit fromTo plus clearProps, so it always ends visible, and a failsafe makes everything visible if GSAP never arrives. Boot is wrapped in try/catch and the click and scroll handlers are torn down properly on remount.

Approve the home and I'll roll the pill nav, rose accent and motion system across the other five pages.

## User

Found issues — fixing…

## Assistant

_[tool: dc_js_str_replace]_

_[tool: dc_js_str_replace]_

_[tool: dc_js_str_replace]_

_[tool: ready_for_verification]_

Closed the stranding properly: scroll tweens use `immediateRender: false` so nothing is hidden before its trigger fires, teardown now restores visibility before killing triggers, and a post-boot check forces everything visible if no triggers survived.

## User

I aprove of the changes so far. The footer was removed however and that too needs some improvements. Apply the changes to the rest of the pages while removing pricing on the fiscalization section too.

## Assistant

_[tool: run_script]_

_[tool: run_script]_

_[tool: delete_file]_

_[tool: ready_for_verification]_

Rolled out across all five inner pages: pill nav with the active page filled, the wipe transition, scroll reveals and hero staggers, rose accents on the numbered markers, rounded buttons on sharp structure.

New footer everywhere including home — a "Let's get you compliant" band with a cyan pill CTA, then brand, services, compliance anchors and contact with the address.

Fiscalisation pricing is gone: the $0.19/day and "90% cheaper" stats now read "Real time — transmission to FDMS" and "8 — accounting systems supported", and the Pricing portal row is removed. Subscription and demo links stay.

The old home file is deleted; **MBC Consultancy v2** is the home all pages link to. Say the word if you'd rather it be renamed back to a clean filename.

## User

Found issues — fixing…

## Assistant

_[tool: run_script]_

_[tool: dc_js_str_replace]_

_[tool: run_script]_

_[tool: ready_for_verification]_

Both fixed: the motion logic is now actually present on all five inner pages (hero staggers, scroll reveals, counters, wipe), and every nav pill has `white-space:nowrap` so nothing wraps during the font swap.

## User

Found issues — fixing…

## Assistant

_[tool: run_script]_

_[tool: ready_for_verification]_

Teardown now kills only the tweens and triggers that instance created, and is gated behind a mount token so a stale unmount can't touch the live instance. Applied to all six pages, home included.

## User

Found issues — fixing…

## Assistant

_[tool: run_script]_

_[tool: grep]_

_[tool: dc_js_str_replace]_

Root cause was that `_run()` queried the DOM before the streamed template had rendered its lower sections, so every tween was built over an empty node list. Boot now waits until the animatable node count stops growing before running, on all six pages.

_[tool: ready_for_verification]_

Waiting on the verifier.

## User

Explain how the animation is supposed to erk when moving from one page to the next. From what I see, it seems mostly broken.

## Assistant

Here's what it's meant to do, and where it actually falls short:

**Intended:** click any internal link → a teal panel sweeps up over the page → navigation happens under cover → the new page reveals.

**What's actually happening:** only the first half exists. The exit wipe fires, the browser loads the new document, and the new page just appears — no covered hand-off, so you get a teal flash followed by an abrupt swap. Worse, the new page then has to boot GSAP from the CDN before its own content animates, so there's a visible gap. That's the broken feeling. Fixing the entry half now.

_[tool: run_script]_

_[tool: ready_for_verification]_

Added the arrival half: every page now opens with a teal curtain already covering it that slides up as the page paints. It's pure CSS, so it runs immediately without waiting for GSAP — the exit wipe covers, the arrival curtain uncovers, and the two read as one continuous move.

The one thing I can't remove is the browser's own document load between them, so on a slow connection there will still be a brief hold under the teal rather than a perfectly seamless slide. If that bothers you, the alternative is a single-page build where the sections swap in place with no reload.

## User

Found issues — fixing…

## Assistant

_[tool: run_script]_

_[tool: ready_for_verification]_

Contact now has eight scroll-reveal targets — the three Reach us cells, the band eyebrow and note, and both lower columns — so it moves like the rest of the site. About link in the nav matched to the pills.

## User

Check didn’t complete

## Assistant

_[tool: ready_for_verification]_

Re-ran the check on Contact — waiting on the result.

