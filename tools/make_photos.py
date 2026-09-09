#!/usr/bin/env python3
"""Turn the sourced Unsplash photography into the site's image set.

Sources live in images/photos/ as downloaded originals (see
docs/photo-credits.md for the photo id, photographer and licence of each).
This crops each to the aspect its slot needs, writes a WebP and a JPEG at two
widths, and leaves the originals untouched so a crop can be redone.

Bands get a wide, shallow crop because they sit behind text; figures get a
squarer one because they sit in a column. Nothing is upscaled -- if an original
is too small for the largest width, it is written at its own size and reported.

    python3 tools/make_photos.py

Requires Pillow only.
"""

import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "images", "photos")
OUT = os.path.join(ROOT, "src", "assets", "img", "photos")

# name -> (aspect w/h, widths, vertical bias, mirror?). Bands are 21:9-ish so a 400px
# strip can be full-bleed on desktop without the subject drifting out of frame
# on mobile. Bias is where the crop window sits in the slack: 0 is flush to the
# top, 1 flush to the bottom, and 0.4 -- slightly above centre -- suits most
# photographs because subjects usually sit above the middle. Mirror is for a
# frame whose subject sits on the side the text veil is densest -- there is no
# lettering in any of these to read backwards, so flipping is free.
BAND = (2.4, (1600, 900))
FIGURE = (1.5, (1000, 600))

PLAN = {
    "advisers": BAND + (0.34, False),      # home — people at work over documents
    "documents": BAND + (0.4, False),      # compliance — stacked files
    # Terminal and receipt sit left in the original, under the densest part of
    # the veil; mirrored, they land in the clear half.
    "fiscalisation": BAND + (0.42, True),
    "accounting": BAND + (0.45, False),    # services — calculator and statements
    "bulawayo": FIGURE + (0.5, False),     # about — the city the firm works from
    # Contact — an aerial of the same city, biased low to keep street and
    # rooftops rather than empty sky.
    "city": BAND + (0.5, False),
    "training": FIGURE + (0.4, False),     # services — a room mid-session
}

WEBP_Q = 72
JPEG_Q = 78

# Dense foliage costs two to three times what a smooth studio frame does at the
# same quality, so the one photograph full of jacaranda leaves gets its own
# number rather than dragging the global one down.
QUALITY = {"bulawayo": 52, "city": 48}


def crop_to(im, aspect, bias):
    """Crop to `aspect`, placing the window at `bias` through the spare height."""
    have = im.width / im.height
    if have > aspect:
        w = round(im.height * aspect)
        left = (im.width - w) // 2
        box = (left, 0, left + w, im.height)
    else:
        h = round(im.width / aspect)
        top = round((im.height - h) * bias)
        box = (0, top, im.width, top + h)
    return im.crop(box)


def main():
    if not os.path.isdir(SRC):
        sys.exit("No sources in %s -- see docs/photo-credits.md." % SRC)
    os.makedirs(OUT, exist_ok=True)

    total = 0
    for name, (aspect, widths, bias, mirror) in sorted(PLAN.items()):
        path = os.path.join(SRC, name + ".jpg")
        if not os.path.exists(path):
            print("  %-28s MISSING" % (name + ".jpg"))
            continue
        base = Image.open(path).convert("RGB")
        if mirror:
            base = base.transpose(Image.FLIP_LEFT_RIGHT)
        base = crop_to(base, aspect, bias)
        for width in widths:
            w = min(width, base.width)
            h = round(w / aspect)
            im = base.resize((w, h), Image.LANCZOS)
            stem = "%s-%d" % (name, width)
            wq = QUALITY.get(name, WEBP_Q)
            jq = QUALITY.get(name, JPEG_Q)
            for ext, kw in (("webp", {"quality": wq, "method": 6}),
                            ("jpg", {"quality": jq, "optimize": True,
                                     "progressive": True})):
                out = os.path.join(OUT, "%s.%s" % (stem, ext))
                im.save(out, **kw)
                size = os.path.getsize(out)
                total += size
                print("  %-28s %5d x %-4d %6.1f KB" % (
                    "%s.%s" % (stem, ext), w, h, size / 1024))
    print("  %-28s %6.1f KB total" % ("", total / 1024))


if __name__ == "__main__":
    main()
