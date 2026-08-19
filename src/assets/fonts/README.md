# Fonts

`archivo-latin.woff2` and `archivo-latin-ext.woff2` are subsets of **Archivo**,
a variable font covering weights 400–700 in a single file each.

- Upstream: https://github.com/Omnibus-Type/Archivo
- Licence: SIL Open Font License 1.1 — full text in `OFL.txt`
- Copyright 2020 The Archivo Project Authors

They are self-hosted rather than loaded from Google Fonts so the site makes no
third-party requests: nothing to block, nothing to leak a visitor's IP to, and
no render delay waiting on another origin. The two files together are ~68 KB and
cover all four weights the design uses.

To refresh them, take the `latin` and `latin-ext` `src` URLs from:

    https://fonts.googleapis.com/css2?family=Archivo:wght@400..700&display=swap

requested with a current-browser User-Agent (an older UA returns .ttf instead of
.woff2). Keep the `unicode-range` values in `assets/css/mbc.css` in step with
whatever that stylesheet declares.
