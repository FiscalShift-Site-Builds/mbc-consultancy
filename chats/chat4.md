# Chat

_Started 2026-08-19 03:32 UTC_

---

## User

Continuing from "MBC Consultancy website design".

## Assistant

We were rebuilding the MBC Consultancy site to showcase compliance, auditing, accounting, tax advisory, corporate governance, and training services across six pages (Home, About, Compliance, Accounting, Fiscalisation, Contact). The goal: a minimal, flow-led home that routes users into the right service page, with a professional-yet-warm aesthetic using cyan, grey, white, and rose accents, all animated via GSAP.

Decisions made:
- Pill nav with Compliance, Accounting, Fiscalisation as visible buttons plus Book a consultation CTA
- Home stripped to hero statement, six-intent chooser, three service blocks, five authority logos, Fiscal Shift partnership, and footer
- Rose accent (#D9788C) accents only, Archivo sans throughout
- Motion system: hero lines rise, cards stagger in, authorities section pins with cyan-to-rose progress bar, numbers count, page exits/entries wrapped in teal wipes
- Fiscalisation: renamed from Fiscal Shift, pricing removed (swapped for real-time/systems-supported stats)
- Footer added everywhere with "Let's get you compliant" band, brand, services, contact

Current state:
All six pages built with pill nav, rose accents, scroll reveals, hero staggers, and GSAP animations. Entry curtains (CSS) uncover as pages load, exit wipes (GSAP) cover links. Motion boot waits for DOM to stabilize before running tweens, teardown is isolated per instance to avoid cross-contamination. Contact was last patched to include eight scroll-reveal targets (Reach us cells, band, columns).

Open:
Verifier check on Contact didn't complete — re-ran and awaiting result. Once cleared, the site is ready for content review or live testing.

Files: MBC Consultancy v2.dc.html, MBC Compliance.dc.html, MBC About.dc.html, MBC Fiscalisation.dc.html, MBC Other Services.dc.html, MBC Contact.dc.html

