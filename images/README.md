# Client-supplied brand source

Sent by the client, kept as provenance. Nothing here is deployed.

| File | What it is |
| --- | --- |
| `WhatsApp Image 2026-09-01 at 06.08.29.jpeg` | Logo on black, 1021×385 (969×362 of artwork). **The working master** — roughly twice the resolution of the other two. |
| `WhatsApp Image 2026-09-01 at 06.13.34.jpeg` | Same logo on white, 691×418 (496×253 of artwork). |
| `MBC_Logo_White_Background-1.pdf` | An A4 page that embeds the 691×418 bitmap above. Not vector — `pdfimages -list` shows one RGB image and no paths. |

There is no vector master. `tools/trace_logo.py` traces the black-ground JPEG
into the SVGs the site loads, plus the alpha masters `tools/make_images.py`
tints into the favicon, app icons and share card. Re-run it only if the client
supplies new artwork:

    python3 -m venv .venv && .venv/bin/pip install numpy potracer pillow
    .venv/bin/python tools/trace_logo.py

If a real vector master ever turns up, use it instead and drop the tracer.

## photos/

Stock photography sourced for the site, kept as downloaded originals.
`tools/make_photos.py` turns these into the WebP/JPEG set the pages load.
Source, photographer, licence and placement for each: **[docs/photo-credits.md](../docs/photo-credits.md)**.
