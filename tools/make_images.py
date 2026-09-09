#!/usr/bin/env python3
"""Generate MBC Consultancy raster brand assets.

Produces the icon set and the social-share card, so nothing has to be
hand-exported from a design tool. The tick and the MBC mark come from
tools/brand/*.png -- greyscale alpha masters cut from the client's own logo by
tools/trace_logo.py -- and are tinted here, so the favicon, the app icons and
the share card all carry the real mark rather than a redrawn approximation.

Requires Pillow and the two Archivo TTFs (see tools/README.md for how to fetch
them; they are not committed because the site itself ships the woff2 subsets).

    python3 tools/make_images.py
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "src", "assets", "img")
BRAND = os.path.join(HERE, "brand")

TEAL = (6, 51, 60)
CYAN = (0, 188, 212)
CYAN_MID = (0, 151, 173)
ROSE = (217, 120, 140)
WHITE = (255, 255, 255)
MIST = (177, 197, 201)
CYAN_LIGHT = (77, 217, 232)  # --cyan-300, the tick colour on dark

FONT_BOLD = os.environ.get("ARCHIVO_BOLD", "/tmp/Archivo-700.ttf")
FONT_REG = os.environ.get("ARCHIVO_REG", "/tmp/Archivo-400.ttf")


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        sys.exit(
            "Missing font: %s\nSee tools/README.md for the download step." % path
        )


def rounded_mask(size, radius, scale=4):
    """A crisp rounded-square alpha mask, supersampled to hide jaggies."""
    big = Image.new("L", (size * scale, size * scale), 0)
    ImageDraw.Draw(big).rounded_rectangle(
        (0, 0, size * scale - 1, size * scale - 1), radius=radius * scale, fill=255
    )
    return big.resize((size, size), Image.LANCZOS)


def alpha_master(name):
    """One of the greyscale masters cut from the supplied logo."""
    path = os.path.join(BRAND, name)
    try:
        return Image.open(path).convert("L")
    except OSError:
        sys.exit(
            "Missing brand master: %s\nRegenerate it with tools/trace_logo.py." % path
        )


def tinted(mask, colour, width):
    """Scale a greyscale master to `width` and paint it a flat colour."""
    h = max(1, round(mask.height * width / mask.width))
    a = mask.resize((width, h), Image.LANCZOS)
    layer = Image.new("RGBA", a.size, colour + (0,))
    layer.putalpha(a)
    return layer


def paste_centred(img, layer, box):
    """Drop `layer` into `box` (l, t, r, b), centred, without distorting it."""
    left, top, right, bottom = box
    bw, bh = right - left, bottom - top
    scale = min(bw / layer.width, bh / layer.height)
    w, h = max(1, round(layer.width * scale)), max(1, round(layer.height * scale))
    layer = layer.resize((w, h), Image.LANCZOS)
    img.alpha_composite(layer, (round(left + (bw - w) / 2), round(top + (bh - h) / 2)))


TICK_MASK = alpha_master("tick.png")
MARK_MASK = alpha_master("mark.png")
MARK_TICK_MASK = alpha_master("mark-tick.png")


def make_icon(size, radius_ratio=0.22, supersample=4):
    """Teal rounded square carrying the logo's own tick in cyan."""
    s = size * supersample
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(
        (0, 0, s - 1, s - 1), radius=int(s * radius_ratio), fill=TEAL + (255,)
    )
    pad = s * 0.26
    paste_centred(img, tinted(TICK_MASK, CYAN, s), (pad, pad, s - pad, s - pad))
    return img.resize((size, size), Image.LANCZOS)


def make_maskable(size=512, supersample=2):
    """Android adaptive icon — art kept inside the safe circle, full-bleed teal."""
    s = size * supersample
    img = Image.new("RGBA", (s, s), TEAL + (255,))
    pad = s * 0.33
    paste_centred(img, tinted(TICK_MASK, CYAN, s), (pad, pad, s - pad, s - pad))
    return img.resize((size, size), Image.LANCZOS)


def make_og(w=1200, h=630):
    """Link-preview card. WhatsApp and LinkedIn both render this; without one a
    shared link shows as bare text, which matters for a WhatsApp-first audience.
    """
    img = Image.new("RGBA", (w, h), TEAL + (255,))
    d = ImageDraw.Draw(img)

    # Soft cyan/rose bloom, echoing the home hero.
    bloom = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    for i in range(70, 0, -1):
        t = i / 70.0
        r = int(300 * t) + 90
        alpha = int(20 * (1 - t))
        mix = (
            int(CYAN[0] * (1 - t) + ROSE[0] * t),
            int(CYAN[1] * (1 - t) + ROSE[1] * t),
            int(CYAN[2] * (1 - t) + ROSE[2] * t),
        )
        bd.ellipse((w - 250 - r, -220 - r // 2, w - 250 + r, -220 + r + r // 2),
                   fill=mix + (alpha,))
    img.alpha_composite(bloom)

    f_sub = font(FONT_REG, 20)
    f_head = font(FONT_BOLD, 82)
    f_meta = font(FONT_REG, 25)

    pad = 84

    # The real mark, in the on-dark colourway the footer uses.
    mark_h = 72
    mark_w = round(MARK_MASK.width * mark_h / MARK_MASK.height)
    img.alpha_composite(tinted(MARK_MASK, WHITE, mark_w), (pad, pad - 8))
    img.alpha_composite(tinted(MARK_TICK_MASK, CYAN_LIGHT, mark_w), (pad, pad - 8))
    d.text(
        (pad + mark_w + 22, pad + 24),
        "M A S H   B U S I N E S S   C O N S U L T A N C Y",
        font=f_sub,
        fill=MIST,
    )

    # Headline — bottom line's descenders must clear the rule at h-118.
    y = 198
    for line in ("Compliance,", "handled with"):
        d.text((pad, y), line, font=f_head, fill=WHITE)
        y += 94
    d.text((pad, y), "precision.", font=f_head, fill=CYAN)

    # Contact strip
    d.line((pad, h - 118, w - pad, h - 118), fill=(255, 255, 255, 55), width=2)
    d.text(
        (pad, h - 92),
        "NSSA  ·  ZIMRA  ·  CIPZ  ·  PRAZ  ·  Vendor registration",
        font=f_meta,
        fill=MIST,
    )
    right = "58 Fife Street, Bulawayo"
    d.text(
        (w - pad - d.textlength(right, font=f_meta), h - 92),
        right,
        font=f_meta,
        fill=MIST,
    )

    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    written = []

    def save(img, name, **kw):
        path = os.path.join(OUT, name)
        img.save(path, **kw)
        written.append((name, os.path.getsize(path)))

    # Favicon fallback for browsers that ignore SVG icons.
    ico = make_icon(64)
    ico.save(
        os.path.join(OUT, "favicon.ico"),
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    written.append(("favicon.ico", os.path.getsize(os.path.join(OUT, "favicon.ico"))))

    # iOS masks this itself and composites anything transparent on black, so
    # it ships square and opaque rather than pre-rounded.
    save(make_icon(180, radius_ratio=0).convert("RGB"), "apple-touch-icon.png",
         optimize=True)
    save(make_icon(192), "icon-192.png", optimize=True)
    save(make_icon(512), "icon-512.png", optimize=True)
    save(make_maskable(512), "icon-maskable-512.png", optimize=True)
    save(make_og(), "og.png", optimize=True, quality=90)

    for name, size in written:
        print("  %-28s %6.1f KB" % (name, size / 1024.0))


if __name__ == "__main__":
    main()
