# Photography — source, licence, placement

Seven photographs, all from **Unsplash** under the
[Unsplash License](https://unsplash.com/license): free for commercial use, no
attribution required, no permission needed. **This is the finished set, not a
placeholder** — the site is not waiting on anything.

This file exists anyway. A firm that sells compliance should be able to say,
from its own repository, where every asset on its website came from and under
what terms.

Originals are committed at `images/photos/` (not deployed).
`tools/make_photos.py` crops, mirrors and re-encodes them into
`src/assets/img/photos/` as WebP with a JPEG fallback, at two widths.

| Slot | Photographer | Photo | Where it appears |
| --- | --- | --- | --- |
| `advisers` | Christina @ wocintechchat.com | [`UcZcsHSp8o4`](https://unsplash.com/photos/UcZcsHSp8o4) | Home — "One adviser who already knows the file" |
| `documents` | Wesley Tingey | [`snNHKZ-mGfE`](https://unsplash.com/photos/snNHKZ-mGfE) | Compliance — "Arrears, lapsed renewals…" |
| `fiscalisation` | Towfiqu barbhuiya | [`xkArbdUcUeE`](https://unsplash.com/photos/xkArbdUcUeE) | Fiscalisation — "Your existing till, fiscalised" |
| `accounting` | Jakub Żerdzicki | [`8wLZi9OhsWU`](https://unsplash.com/photos/8wLZi9OhsWU) | Services — "Statements an auditor… will accept" |
| `training` | Christina @ wocintechchat.com | [`faEfWCdOKIg`](https://unsplash.com/photos/faEfWCdOKIg) | Services — Training & capacity building |
| `bulawayo` | Omoniyi David | [`MdKSczxB43A`](https://unsplash.com/photos/MdKSczxB43A) | About — hero aside figure |
| `city` | Omoniyi David | [`63wC6e_0ZCM`](https://unsplash.com/photos/63wC6e_0ZCM) | Contact — "In Bulawayo, and wherever you are registered" |

Both Bulawayo frames are genuinely Bulawayo — Unsplash records the location on
each, and they are by a photographer who shoots the city.

## Two constraints that came with the licence

These are settled, not open questions. They are recorded because they constrain
future edits, and someone changing a caption a year from now will not otherwise
know.

**1. `advisers` shows identifiable people who do not work for MBC.**
The Unsplash License permits commercial use but grants no model release, and it
does not allow using a photograph of a person to imply their endorsement. As
built, the band's copy is about the service model, the caption is empty, and
nothing names or claims them — which is ordinary editorial use and fine.

> **Never** caption this photograph "our team", place a person's name beside it,
> or run a testimonial against it. Any of those turns permitted use into an
> implied endorsement. If a section ever needs a named face, it needs a real
> photograph, not this one.

**2. `city` is a real, identifiable building that is not the firm's office.**
It is a street view in central Bulawayo; the office is on Fife Street. The
band's headline therefore claims the *city* — "In Bulawayo, and wherever you are
registered" — and points at the address block below rather than captioning the
building. An earlier draft read "58 Fife Street, Bulawayo." over this frame,
which would have been read as a photograph of the office. It is not.

> Keep any copy laid over this frame at city level. The exact address belongs in
> the Reach us block, in text.

## The treatment, and why

Every band photograph is desaturated, colourised teal through a `color` blend
layer, then veiled with a gradient (`.photoband` in `mbc.css`). Three reasons:

1. Seven unrelated photographs, shot by five people in four countries, read as
   one set once they share a hue.
2. Text over an untreated photograph is a contrast lottery. The veil makes the
   headline's contrast a property of the CSS, not of the picture.
3. Untreated stock is what makes a small-firm site look assembled from a
   template. The treatment is the difference between a picture that was dropped
   in and one that was chosen.

The two column figures (`bulawayo`, `training`) are shown close to the original,
lightly desaturated only — they are photographs of a real place and a real kind
of session, and the captions say so, which the duotone would undercut.

## Rejected, and why

Kept here so the same ground is not covered twice:

- **Two "businessmen shaking hands" frames.** Synthetic-looking, and the
  handshake-across-a-desk shot is the single most templated image in the genre.
- **A set of glass-tower facades.** Legible as global corporate, not as a
  Bulawayo practice.
- **A point-of-sale terminal carrying SumUp branding**, and its first
  replacement, which had a furniture retailer's placard legible in frame. On a
  page about a named partner product, a stranger's brand in the photograph is a
  claim nobody meant to make.
- **A signed document over Polish banknotes.** Wrong currency for the audience.
- **An aerial of the whole town as a full-bleed band.** Illegible at band size
  behind a veil, and the foliage detail cost 180 KB to say nothing. It is now
  the About figure instead, where it is small, sharp and cheap.

## If a real photograph ever arrives

Not needed, but the swap is one command. Drop a replacement into
`images/photos/` under the same filename and re-run `tools/make_photos.py`;
crop bias, mirroring and per-image quality live in that script's `PLAN` table,
and nothing in `src/pages/` has to change.
