#!/usr/bin/env python3
"""Assemble the MBC Consultancy static site.

Every page shares one layout, one header and one footer, so a change to the nav
or the footer is made once rather than six times. Output is plain static HTML —
no runtime framework, no build step needed on the host.

    python3 build.py            # build into site/
    python3 build.py --check    # build, then run the link/consistency checks

The generated site/ directory is committed, so Cloudflare needs no build
command: point it at site/ as the output directory.
"""

import argparse
import base64
import hashlib
import html
import os
import re
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "site")

# ---------------------------------------------------------------------------
# Site config
#
# SITE_URL is the only place the domain appears. It feeds canonical links, the
# Open Graph tags, the JSON-LD and sitemap.xml. Set MBC_SITE_URL in the
# environment, or edit the fallback below, once the domain is registered.
# ---------------------------------------------------------------------------
PLACEHOLDER_URL = "https://mbcconsultancy.example"
SITE_URL = os.environ.get("MBC_SITE_URL", PLACEHOLDER_URL).rstrip("/")

# nav key -> the pages that should show that nav item as current
NAV_KEYS = ("compliance", "services", "fiscalisation", "about", "contact")

PAGES = [
    {
        "slug": "index",
        "path": "/",
        "nav": None,
        "title": "MBC Consultancy — regulatory compliance, accounting & fiscalisation in Zimbabwe",
        "og_title": "Compliance, handled with precision.",
        "desc": (
            "MBC Consultancy keeps Zimbabwean businesses registered, filed and "
            "audit-ready across NSSA, ZIMRA, CIPZ, PRAZ and Ministry of Finance "
            "vendor registration. Bulawayo-based, licenced ZIMRA tax agent."
        ),
        "priority": "1.0",
    },
    {
        "slug": "compliance",
        "path": "/compliance",
        "nav": "compliance",
        "title": "Statutory & regulatory compliance — NSSA, ZIMRA, CIPZ, PRAZ | MBC Consultancy",
        "og_title": "Full regulatory adherence, authority by authority.",
        "desc": (
            "Registrations, contributions, returns and renewals across NSSA, ZIMRA, "
            "CIPZ, PRAZ and Ministry of Finance vendor registration, handled by a "
            "licenced ZIMRA tax agent in Bulawayo."
        ),
        "priority": "0.9",
    },
    {
        "slug": "services",
        "path": "/services",
        "nav": "services",
        "title": "Auditing, accounting, tax advisory & governance | MBC Consultancy",
        "og_title": "Audit, accounting, tax and governance under one engagement.",
        "desc": (
            "Statutory and internal audits, IFRS financial statements, management "
            "accounts, payroll, tax advisory, corporate governance and compliance "
            "training for Zimbabwean businesses."
        ),
        "priority": "0.9",
    },
    {
        "slug": "fiscalisation",
        "path": "/fiscalisation",
        "nav": "fiscalisation",
        "title": "Fiscalisation without the hardware — Fiscal Shift partner | MBC Consultancy",
        "og_title": "Fiscalisation without the hardware.",
        "desc": (
            "Software-only fiscalisation with Fiscal Shift, connected to ZIMRA's "
            "FDMS in real time. We advise on the fit, help you sign up and "
            "reconcile your VAT returns against what the platform transmits."
        ),
        "priority": "0.8",
    },
    {
        "slug": "about",
        "path": "/about",
        "nav": "about",
        "title": "About the firm | MBC Consultancy, Bulawayo",
        "og_title": "A professional services firm built around regulatory knowledge.",
        "desc": (
            "MBC Consultancy is incorporated in Zimbabwe and specialises in "
            "regulatory compliance, auditing and accounting solutions, from offices "
            "at 58 Fife Street, Bulawayo."
        ),
        "priority": "0.6",
    },
    {
        "slug": "contact",
        "path": "/contact",
        "nav": "contact",
        "title": "Book a consultation | MBC Consultancy, Bulawayo",
        "og_title": "Book a consultation.",
        "desc": (
            "Tell us which authorities you are registered with and what the "
            "business needs next. 58 Fife Street, Bulawayo · (+263) 774 121 012 · "
            "WhatsApp or email."
        ),
        "priority": "0.9",
    },
    {
        "slug": "thanks",
        "path": "/thanks",
        "nav": None,
        "title": "Thank you — your enquiry is with us | MBC Consultancy",
        "og_title": "Thank you — your enquiry is with us.",
        "desc": "Your enquiry has reached MBC Consultancy. We aim to reply within one working day.",
        "noindex": True,
    },
    {
        "slug": "404",
        "path": "/404",
        "nav": None,
        "title": "Page not found | MBC Consultancy",
        "og_title": "Page not found",
        "desc": "That page is not here. Find compliance, accounting, fiscalisation, about and contact instead.",
        "noindex": True,
    },
]


def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def render_header(header_tpl, nav_key):
    """Fill the nav's aria-current markers for the page being built."""
    out = header_tpl
    for key in NAV_KEYS:
        marker = "{{CUR_%s}}" % key.upper()
        out = out.replace(marker, ' aria-current="page"' if key == nav_key else "")
    return out


def build_pages(layout, header_tpl, footer):
    built = []
    for page in PAGES:
        content = read(SRC, "pages", page["slug"] + ".html")
        doc = layout
        doc = doc.replace("{{HEADER}}", render_header(header_tpl, page["nav"]))
        doc = doc.replace("{{FOOTER}}", footer)
        doc = doc.replace("{{CONTENT}}", content.rstrip() + "\n")
        doc = doc.replace("{{TITLE}}", html.escape(page["title"], quote=True))
        doc = doc.replace("{{OG_TITLE}}", html.escape(page["og_title"], quote=True))
        doc = doc.replace("{{DESC}}", html.escape(page["desc"], quote=True))
        doc = doc.replace("{{SITE}}", SITE_URL)
        doc = doc.replace("{{PATH}}", "" if page["path"] == "/" else page["path"])
        doc = doc.replace(
            "{{ROBOTS}}",
            '<meta name="robots" content="noindex,follow">\n'
            if page.get("noindex")
            else "",
        )
        write(os.path.join(OUT, page["slug"] + ".html"), doc)
        built.append(page["slug"] + ".html")
    return built


INLINE_SCRIPT_RE = re.compile(r"<script>(.*?)</script>", re.S)


def inline_script_hashes(layout):
    """CSP hashes for the layout's inline scripts.

    Computed from the markup itself so the Content-Security-Policy can stay
    strict without 'unsafe-inline', and cannot silently drift if that boot
    script is ever edited.
    """
    hashes = []
    for body in INLINE_SCRIPT_RE.findall(layout):
        digest = hashlib.sha256(body.encode("utf-8")).digest()
        hashes.append("'sha256-%s'" % base64.b64encode(digest).decode("ascii"))
    return " ".join(hashes)


def copy_static(layout):
    """Assets and platform files. Rewritten every build, so src/ is the truth."""
    shutil.copytree(
        os.path.join(SRC, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True
    )
    for name in ("_headers", "_redirects", "robots.txt", "site.webmanifest"):
        src = os.path.join(SRC, name)
        if not os.path.exists(src):
            continue
        text = read(SRC, name)
        text = text.replace("{{SCRIPT_HASHES}}", inline_script_hashes(layout))
        text = text.replace("{{SITE}}", SITE_URL)
        write(os.path.join(OUT, name), text)


def build_sitemap():
    today = date.today().isoformat()
    rows = []
    for page in PAGES:
        if page.get("noindex"):
            continue
        loc = SITE_URL + ("/" if page["path"] == "/" else page["path"])
        rows.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <priority>%s</priority>\n"
            "  </url>" % (loc, today, page.get("priority", "0.5"))
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "%s\n</urlset>\n" % "\n".join(rows)
    )
    write(os.path.join(OUT, "sitemap.xml"), xml)


# ---------------------------------------------------------------------------
# Checks — cheap guards against the classes of bug this rebuild was fixing.
# ---------------------------------------------------------------------------

HREF_RE = re.compile(r'href="([^"]+)"')
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")


def check(built):
    problems = []
    notes = []

    known = set()
    for page in PAGES:
        known.add("/" if page["path"] == "/" else page["path"])
    # Anchors that exist in the built output, as path#id
    anchors = set()
    docs = {}

    for name in built:
        text = read(OUT, name)
        docs[name] = text
        for match in re.finditer(r'id="([^"]+)"', text):
            slug = name[:-5]
            path = "/" if slug == "index" else "/" + slug
            anchors.add(path + "#" + match.group(1))

    for name, text in docs.items():
        where = name

        # 1. No unfilled template placeholders survived.
        for m in PLACEHOLDER_RE.finditer(text):
            problems.append("%s: unreplaced placeholder %s" % (where, m.group(0)))

        # 2. No prototype artefacts left behind.
        for artefact in (".dc.html", "style-hover", "x-dc", "support.js", "%20"):
            if artefact in text:
                problems.append("%s: prototype artefact %r" % (where, artefact))

        # 3. Internal links resolve to a real page, and anchors to a real id.
        for href in HREF_RE.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            if href.startswith("/assets/") or href in ("/site.webmanifest",):
                target = os.path.join(OUT, href.lstrip("/"))
                if not os.path.exists(target):
                    problems.append("%s: missing asset %s" % (where, href))
                continue
            base, _, frag = href.partition("#")
            base = base.split("?")[0] or "/"
            if base not in known:
                problems.append("%s: link to unknown page %s" % (where, href))
            elif frag and (base + "#" + frag) not in anchors:
                problems.append("%s: link to missing anchor %s" % (where, href))

    # 4. The shared chrome really is identical everywhere.
    def slice_between(text, start, end):
        i, j = text.find(start), text.find(end)
        return text[i:j] if i != -1 and j != -1 else None

    footers = {}
    for name, text in docs.items():
        f = slice_between(text, '<footer class="footer">', "</footer>")
        footers.setdefault(f, []).append(name)
    if len(footers) > 1:
        problems.append(
            "footer differs between pages: %s"
            % " vs ".join(",".join(v) for v in footers.values())
        )

    # 5. Every page has exactly one h1.
    for name, text in docs.items():
        n = len(re.findall(r"<h1\b", text))
        if n != 1:
            problems.append("%s: expected 1 <h1>, found %d" % (name, n))

    # 6. The domain is still a placeholder — a launch blocker, not a bug.
    if SITE_URL == PLACEHOLDER_URL:
        notes.append(
            "SITE_URL is still the placeholder %s — canonical, Open Graph and\n"
            "     sitemap URLs will be wrong until it is set. See docs/DEPLOY.md."
            % PLACEHOLDER_URL
        )

    return problems, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="run consistency checks")
    args = ap.parse_args()

    if not os.path.isdir(SRC):
        sys.exit("No src/ directory next to build.py")

    # Rebuild the HTML from scratch so a deleted page cannot linger.
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            if name.endswith((".html", ".xml")):
                os.remove(os.path.join(OUT, name))

    layout = read(SRC, "layout.html")
    header_tpl = read(SRC, "partials", "header.html")
    footer = read(SRC, "partials", "footer.html")

    built = build_pages(layout, header_tpl, footer)
    copy_static(layout)
    build_sitemap()

    print("Built %d pages into %s/" % (len(built), os.path.relpath(OUT, ROOT)))
    for name in built:
        size = os.path.getsize(os.path.join(OUT, name)) / 1024.0
        print("  %-22s %5.1f KB" % (name, size))

    if args.check:
        problems, notes = check(built)
        print()
        if problems:
            print("FAILED — %d problem(s):" % len(problems))
            for p in problems:
                print("  ✗ %s" % p)
        else:
            print("Checks passed: links, anchors, assets, shared chrome, headings.")
        for n in notes:
            print("  ! %s" % n)
        if problems:
            sys.exit(1)


if __name__ == "__main__":
    main()
