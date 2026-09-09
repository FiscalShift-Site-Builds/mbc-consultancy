#!/usr/bin/env python3
"""Trace the client-supplied MBC logo raster into clean SVG brand assets.

The firm supplied the logo only as JPEGs and a PDF that embeds one of them --
there is no vector master. This turns the best raster into vectors once, so the
site can scale the mark to any size and recolour it for dark backgrounds.

Source: images/WhatsApp Image 2026-09-01 at 06.08.29.jpeg -- the light-on-black
version. It carries 969x362 px of logo against 496x253 in the white-background
JPEG and the PDF (whose page is just that same 691x418 bitmap), so it is the
sharpest original available.

Two masks are traced per asset:

  all ink  -> filled in the letter colour
  teal ink -> filled on top in the tick colour

Tracing "all ink" rather than "grey ink" keeps the tick/letter boundary
*interior* to the lower shape, so the two fills cannot leave a hairline seam
between them the way two abutting outlines would.

    python3 -m venv .venv && .venv/bin/pip install numpy potracer pillow
    .venv/bin/python tools/trace_logo.py

Writes what the site loads into src/assets/img/ -- the wordmark-and-tick mark
in both colourways, plus the tick on its own. The full lockup, tagline and all,
goes to tools/brand/ instead: its "MASH BUSINESS CONSULTANCY" line needs the
logo to be ~180px tall before it is legible, which no placement on the site
gives it, so shipping it would be 100 KB nothing loads. tools/brand/ also holds
greyscale alpha masters that make_images.py tints into the favicon, app icons
and share card -- so every brand surface comes off the same artwork.

Only needs re-running if the client supplies a new logo.
"""

import os
import sys

try:
    import numpy as np
    import potrace
    from PIL import Image
except ImportError as exc:  # pragma: no cover - tooling guard
    sys.exit("%s\nInstall with: pip install numpy potracer pillow" % exc)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "images", "WhatsApp Image 2026-09-01 at 06.08.29.jpeg")
OUT = os.path.join(ROOT, "src", "assets", "img")
BRAND = os.path.join(ROOT, "tools", "brand")

# Supersampling the mask before tracing puts the contour on a sub-pixel grid,
# which is what stops the curves looking faceted at large sizes.
UP = 3

# Ink levels measured off the source: neutral grey letters at ~#8D8D8D and the
# teal tick at ~#035D5B, both over near-black. Dividing by these turns
# brightness into coverage, so the 0.5 threshold lands on the true edge of each
# ink rather than somewhere inside the darker one.
GREY_INK = 141.0
TEAL_INK = 66.0

# Row 316 is the last of the MBC wordmark; the rule and tagline start at 339.
# Splitting in the gap gives a wordmark-only mark for small placements.
WORDMARK_ROWS = 328

# The white-background artwork sets the letters at #B8B8B8, which is only
# 1.9:1 on white -- the client's first note on the site was that the logo
# could not be seen. #8D8D8D is the same silver as measured off their
# light-on-black artwork and reads at 3.3:1, so the mark carries without
# introducing a colour that is not already in their own files.
LETTER = "#8D8D8D"
TICK = "#1E6360"         # logo teal, as supplied
LETTER_ON_DARK = "#FFFFFF"
TICK_ON_DARK = "#4DD9E8"  # site --cyan-300; the supplied teal goes muddy on --teal-900

NAME = "Mash Business Consultancy"


def masks():
    """Coverage maps for all ink and for the teal ink alone."""
    a = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b

    tealish = (g > r + 10) & (b > r + 6) & (g > 12)
    teal = np.where(tealish, np.clip(lum / TEAL_INK, 0, 1), 0.0)
    allink = np.where(tealish, teal, np.clip(lum / GREY_INK, 0, 1))

    ys, xs = np.where(allink > 0.5)
    box = (int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1)
    return allink[box[0]:box[1], box[2]:box[3]], teal[box[0]:box[1], box[2]:box[3]]


def trace(mask):
    im = Image.fromarray((mask * 255).astype(np.uint8))
    im = im.resize((im.width * UP, im.height * UP), Image.BICUBIC)
    big = np.asarray(im).astype(np.float32) / 255.0 > 0.5
    # potracer's Bitmap inverts on construction -- it treats dark as ink -- so
    # the mask goes in negated.
    return potrace.Bitmap(~big).trace(
        turdsize=4 * UP * UP, alphamax=1.0, opticurve=True, opttolerance=0.35
    )


def to_path_data(curves, k, ox, oy):
    num = lambda v: ("%.1f" % v).rstrip("0").rstrip(".")
    x = lambda v: num((v / UP - ox) * k)
    y = lambda v: num((v / UP - oy) * k)
    out = []
    for curve in curves:
        out.append("M%s %s" % (x(curve.start_point.x), y(curve.start_point.y)))
        for seg in curve:
            if seg.is_corner:
                out.append("L%s %sL%s %s" % (x(seg.c.x), y(seg.c.y),
                                             x(seg.end_point.x), y(seg.end_point.y)))
            else:
                out.append("C%s %s %s %s %s %s" % (
                    x(seg.c1.x), y(seg.c1.y), x(seg.c2.x), y(seg.c2.y),
                    x(seg.end_point.x), y(seg.end_point.y)))
        out.append("Z")
    return "".join(out)


def write_svg(name, allink, teal, letter, tick, label, height=100, out=None):
    """Trace one crop at a normalised height and write it out."""
    keep = allink if teal is None else np.maximum(allink, teal)
    ys, xs = np.where(keep > 0.5)
    ox, oy = int(xs.min()), int(ys.min())
    w, h = int(xs.max()) - ox + 1, int(ys.max()) - oy + 1
    k = height / h

    layers = ['<path fill="%s" d="%s"/>' % (letter, to_path_data(trace(allink), k, ox, oy))]
    if teal is not None:
        layers.append('<path fill="%s" d="%s"/>' % (tick, to_path_data(trace(teal), k, ox, oy)))

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %d" '
        'role="img" aria-label="%s"><title>%s</title>%s</svg>\n'
        % (("%.1f" % (w * k)).rstrip("0").rstrip("."), height, label, label, "".join(layers))
    )
    directory = out or OUT
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    label_path = name if directory == OUT else "brand/" + name
    print("  %-24s %6.1f KB" % (label_path, len(svg) / 1024))


def bbox(mask):
    ys, xs = np.where(mask > 0.5)
    return int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1


def write_alpha(name, mask, width, box=None):
    """A greyscale alpha master, for tools that composite rather than render SVG.

    `box` lets a second layer share the first one's frame, so the two stay in
    register when they are stacked back up.
    """
    y0, y1, x0, x1 = box or bbox(mask)
    sub = mask[y0:y1, x0:x1]
    im = Image.fromarray((np.clip(sub, 0, 1) * 255).astype(np.uint8), "L")
    im = im.resize((width, max(1, round(im.height * width / im.width))), Image.LANCZOS)
    os.makedirs(BRAND, exist_ok=True)
    path = os.path.join(BRAND, name)
    im.save(path, optimize=True)
    print("  %-24s %6.1f KB  %dx%d" % ("brand/" + name, os.path.getsize(path) / 1024,
                                       im.width, im.height))


def write_favicon(tick_svg_path):
    """A 32x32 tab icon: teal rounded square, the logo's own tick in cyan."""
    import re
    svg = open(tick_svg_path, encoding="utf-8").read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups())
    d = re.search(r'\sd="([^"]+)"', svg).group(1)

    size, pad = 32, 6.6
    k = min((size - 2 * pad) / w, (size - 2 * pad) / h)
    tx, ty = (size - w * k) / 2, (size - h * k) / 2

    out = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" role="img" '
        'aria-label="%s">\n'
        "  <title>%s</title>\n"
        '  <rect width="32" height="32" rx="7.04" fill="#06333C"/>\n'
        "  <!-- The tick from the firm's own logo. Regenerate with trace_logo.py. -->\n"
        '  <g transform="translate(%.3f %.3f) scale(%.5f)">\n'
        '    <path fill="#00BCD4" d="%s"/>\n'
        "  </g>\n"
        "</svg>\n" % (NAME, NAME, tx, ty, k, d)
    )
    path = os.path.join(OUT, "favicon.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("  %-24s %6.1f KB" % ("favicon.svg", len(out) / 1024))


def main():
    allink, teal = masks()
    word_a, word_t = allink[:WORDMARK_ROWS], teal[:WORDMARK_ROWS]

    # The tick alone: teal ink above the tagline, with nothing under it.
    tick_only = word_t.copy()

    print("Tracing %s" % os.path.basename(SRC))
    write_svg("mbc-logo.svg", allink, teal, LETTER, TICK, NAME, out=BRAND)
    write_svg("mbc-logo-light.svg", allink, teal, LETTER_ON_DARK, TICK_ON_DARK, NAME,
              out=BRAND)
    write_svg("mbc-mark.svg", word_a, word_t, LETTER, TICK, "MBC")
    write_svg("mbc-mark-light.svg", word_a, word_t, LETTER_ON_DARK, TICK_ON_DARK, "MBC")
    write_svg("mbc-tick.svg", tick_only, None, TICK, TICK, "MBC")
    write_favicon(os.path.join(OUT, "mbc-tick.svg"))

    write_alpha("tick.png", tick_only, 1024)
    frame = bbox(word_a)
    write_alpha("mark.png", word_a, 2048, frame)
    write_alpha("mark-tick.png", word_t, 2048, frame)


if __name__ == "__main__":
    main()
