# Ad Formats

The format taxonomy and aspect ratios you'll route between when shipping commercial creative.

## Aspect ratios by platform

| Platform / placement | Aspect | Resolution recommendation |
|---|---|---|
| TikTok feed / Reels | 9:16 | 1080×1920 |
| TikTok in-feed ads | 9:16 | 1080×1920 |
| Instagram feed (square) | 1:1 | 1080×1080 |
| Instagram feed (portrait) | 4:5 | 1080×1350 |
| Instagram Story / Reel | 9:16 | 1080×1920 |
| Instagram landscape (legacy) | 1.91:1 | 1080×566 |
| Facebook feed | 1:1 or 4:5 | Same as IG |
| YouTube video | 16:9 | 1920×1080 |
| YouTube Shorts | 9:16 | 1080×1920 |
| LinkedIn feed | 1.91:1 or 1:1 | 1200×627 or 1080×1080 |
| Twitter / X feed | 16:9 or 1:1 | 1200×675 or 1080×1080 |
| Pinterest pin | 2:3 | 1000×1500 |
| Pinterest video pin | 9:16 or 1:1 | Same shape |
| Hero web banner | 16:9 or 21:9 | 1920×1080 or 2560×1080 |
| Email header | 2:1 or 3:1 | 1200×600 or 1200×400 |
| Print poster (portrait) | ~3:4 or 2:3 | 4K+ |
| Print spread (landscape) | ~4:3 | 4K+ |

## Format types

### Hero banner

Single image, wide horizontal aspect. Used for website hero sections, email headers, web ads.

- **Aspect**: 16:9 or wider (21:9 for cinematic feel)
- **Composition**: product or scene fills the frame, leaves room for headline overlay on one side
- **Resolution**: 2K for web, 4K for print

### Social square

Most common Instagram / Facebook feed format. Versatile.

- **Aspect**: 1:1
- **Composition**: product centered, room for overlay text top or bottom third
- **Resolution**: 2K (1080×1080 native, 2K for sharper rendering)

### Story / Reel vertical

Full-screen mobile. Native to TikTok, IG Stories, Reels, Shorts, Pinterest video.

- **Aspect**: 9:16
- **Composition**: subject vertical, room for overlay text top and bottom (mobile UI eats edges)
- **Resolution**: 2K (1080×1920 native, 2K for sharper rendering)

### Carousel slides

Series of images, same product, varied context or messaging. IG carousels typically 1:1 or 4:5.

- **Aspect**: same across all slides (don't mix 1:1 with 4:5 — looks broken)
- **Composition**: slide 1 hooks, slides 2-N elaborate, last slide CTA
- **Volume**: typically 3-10 slides

### Ad creative pack

A bundle of variants for a single product / campaign for A/B testing.

Common bundle:
- 3 hero variants (different lighting / background)
- 4 lifestyle variants (different contexts)
- 1 white-background ecommerce shot
- 1 social-square graphic with text

Or just-video:
- 1 UGC-style 9:16
- 1 product showcase 16:9
- 1 talking head 9:16

### Print / large-format

Higher resolution requirements. 4K minimum, ideally 6K for billboards / large-format display.

- **Aspect**: matches the print piece (A4 / A3 / poster / billboard)
- **Resolution**: 4K or higher
- **Process**: generate at 2K, vision-verify, then enhance to 4K via `enhance_image`

## Picking volume

For exploratory work: 1 variant first, get feedback, then 3 more if directionally right.

For A/B testing: minimum 4 variants per format (so the test has something to compare). 8+ is better if the cost is justified.

For final production: 1 winner + 1 backup of each chosen format.

## Cost preflight

Always preflight cost when:

- Generating ≥ 5 images for any single brief
- Generating any video (regardless of duration)
- Generating any 4K resolution image
- Generating across multiple formats (a "creative pack" of 5+ images)

Format the preflight as one line:

> "About to generate: 1 hero (16:9, 2K) + 4 social variants (TikTok 9:16, IG square, IG portrait, Pinterest 2:3) at 2K. Estimated ~[N] CU. Proceed?"

User says yes, you ship. User adjusts, you adjust.

## Naming conventions for delivered files

Suggested file naming for multi-format batches so the user can find them later:

```
yyyy-mm-dd-<brand>-<product>-<format>-<variant>.png

# Examples:
2026-05-16-acme-lemonade-hero-16x9-v1.png
2026-05-16-acme-lemonade-tiktok-9x16-v1.png
2026-05-16-acme-lemonade-ig-square-v2.png
2026-05-16-acme-lemonade-pinterest-2x3-v1.png
```

Or simpler if the brief is single-format:

```
2026-05-16-acme-lemonade-hero-v1.png
2026-05-16-acme-lemonade-hero-v2.png
```

Pick a convention per project and stick with it.
