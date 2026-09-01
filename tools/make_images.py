#!/usr/bin/env python3
"""Generate MBC Consultancy raster brand assets.

Produces the icon set and the social-share card from the site's own palette and
typeface, so nothing has to be hand-exported from a design tool.

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

TEAL = (6, 51, 60)
CYAN = (0, 188, 212)
CYAN_MID = (0, 151, 173)
ROSE = (217, 120, 140)
WHITE = (255, 255, 255)
MIST = (177, 197, 201)

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


def draw_tick(img, box, colour, weight):
    """The angular check that gives the logo its M — sharp ends, no round caps.

    box is (left, top, right, bottom) of the tick's bounding area.
    """
    left, top, right, bottom = box
    w = right - left
    h = bottom - top
    # Three points: start of the short arm, the elbow, the tip of the long arm.
    p_start = (left, top + h * 0.46)
    p_elbow = (left + w * 0.34, bottom)
    p_tip = (right, top)

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([p_start, p_elbow], fill=colour, width=weight)
    d.line([p_elbow, p_tip], fill=colour, width=weight)
    # Fill the mitre the two strokes leave open at the elbow.
    d.polygon(
        [
            (p_elbow[0] - weight * 0.5, p_elbow[1]),
            (p_elbow[0] + weight * 0.5, p_elbow[1]),
            (p_elbow[0], p_elbow[1] - weight * 0.6),
        ],
        fill=colour,
    )
    img.alpha_composite(layer)


def make_icon(size, radius_ratio=0.22, supersample=4):
    """Teal rounded square carrying a cyan compliance tick."""
    s = size * supersample
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(
        (0, 0, s - 1, s - 1), radius=int(s * radius_ratio), fill=TEAL + (255,)
    )
    pad = s * 0.24
    draw_tick(
        img,
        (pad, pad * 1.12, s - pad, s - pad * 1.24),
        CYAN + (255,),
        int(s * 0.115),
    )
    return img.resize((size, size), Image.LANCZOS)


def make_maskable(size=512):
    """Android adaptive icon — art kept inside the safe circle, full-bleed teal."""
    img = Image.new("RGBA", (size, size), TEAL + (255,))
    pad = size * 0.30
    draw_tick(
        img,
        (pad, pad * 1.1, size - pad, size - pad * 1.2),
        CYAN + (255,),
        int(size * 0.10),
    )
    return img


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

    f_mark = font(FONT_BOLD, 58)
    f_sub = font(FONT_REG, 20)
    f_head = font(FONT_BOLD, 82)
    f_meta = font(FONT_REG, 25)

    pad = 84

    # Wordmark, matching the site header's baseline-aligned pair.
    d.text((pad, pad - 6), "MBC", font=f_mark, fill=WHITE)
    mark_w = d.textlength("MBC", font=f_mark)
    d.text(
        (pad + mark_w + 18, pad + 26),
        "C O N S U L T A N C Y",
        font=f_sub,
        fill=MIST,
    )

    # Tick, sitting opposite the wordmark.
    draw_tick(img, (w - pad - 78, pad + 2, w - pad, pad + 68), CYAN + (255,), 13)

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

    save(make_icon(180), "apple-touch-icon.png", optimize=True)
    save(make_icon(192), "icon-192.png", optimize=True)
    save(make_icon(512), "icon-512.png", optimize=True)
    save(make_maskable(512), "icon-maskable-512.png", optimize=True)
    save(make_og(), "og.png", optimize=True, quality=90)

    for name, size in written:
        print("  %-28s %6.1f KB" % (name, size / 1024.0))


if __name__ == "__main__":
    main()
