# Aspect Ratios for Archviz

Picking the right aspect ratio matters more in archviz than in casual generation. Wrong ratio crops important architecture (cuts off the ceiling on an interior, or crops the sky context off an exterior hero) or wastes resolution on dead space.

## Quick lookup

| Use case | Default ratio | Why |
|---|---|---|
| Exterior hero | 16:9 | Captures sky context + ground plane, cinematic feel |
| Wide context / urban scale | 21:9 or 2:1 | Lets the building sit in its surroundings without dominating |
| Interior hero | 3:2 or 4:3 | 16:9 typically crops the ceiling on standard floor-to-floor heights; portrait-leaning ratios show more of the room |
| Detail / texture | 4:3 or 1:1 | Square framing lets the detail be the subject without competing context |
| Portfolio cover | 16:9 or 2:1 | Reads consistently across web layouts and print spreads |
| Moodboard tile | 1:1 | Stacks cleanly in grids |
| Social media post | 1:1 (IG square) or 4:5 (IG portrait) | Platform native crops |
| Vertical mobile / story | 9:16 | Tall buildings, atrium / lobby vertical features |

## Detailed guidance

### Exterior shots

**Default to 16:9** unless the brief calls otherwise. Reasons:

- Cinematic association (we're conditioned to read landscape as "scene")
- Gives the sky context without dominating
- Matches client presentation slide aspect (PowerPoint, Keynote)

**Use 21:9 or 2:1** when:

- Showing the building in a wide horizontal context (waterfront, skyline)
- Producing portfolio cover images that need to crop down without losing the architecture
- Brief calls for "panorama" or "wide context shot"

**Use 4:3 or 1:1** when:

- Detail shot — a corner condition, a material study, a window detail
- The brief is "this specific element, isolated"

### Interior shots

**Default to 3:2 or 4:3.** 16:9 is too wide for most interiors at typical ceiling heights — you end up with empty walls left and right, and the ceiling cropped tight.

- **3:2** — the photographer's classic 35mm ratio, reads natural for most interior compositions
- **4:3** — even taller, good when the ceiling treatment or vertical proportions matter (double-height spaces, ribbed barrel vaults, monumental volumes)
- **16:9** — only when explicitly cinematic / mood is the goal, OR when the room is exceptionally long (corridor, gallery, retail aisle)
- **1:1** — for detail shots, hero materials, focused furniture vignettes

### Detail and material studies

**Square (1:1)** or **4:3**. Detail shots benefit from the subject filling the frame. 16:9 leaves too much air around a single element.

### Portfolio output

Pick the aspect once for the whole set, not per-image. Mixing 16:9 hero shots with 4:3 interior shots in a portfolio looks visually inconsistent. Common portfolio aspects:

- **16:9 horizontal** — cleanest for web layouts
- **2:1** — good for hero + detail crop variants
- **4:5 vertical** — good for print spreads and Instagram cross-posting

### Social and presentation outputs

| Platform | Aspect |
|---|---|
| Instagram square | 1:1 |
| Instagram portrait | 4:5 |
| Instagram story / reel | 9:16 |
| LinkedIn / Twitter | 16:9 |
| Pinterest | 2:3 |
| Slide deck (16:9 default) | 16:9 |
| Slide deck (4:3 legacy) | 4:3 |
| A4 / Letter portrait | ~3:4 |
| A3 / Tabloid landscape | ~4:3 |

## Cost vs ratio

Aspect ratio doesn't directly drive cost — resolution does. But picking the wrong aspect and re-cropping wastes pixels. If you know the final use case (say, IG square), generate at that aspect from the start rather than 16:9 and cropping later.

## Asking the user

If the brief doesn't specify, default by intent type from the table above. Confirm only if the user's intent is ambiguous (e.g. "make a render of this building" — exterior hero or detail study?). Don't ask about aspect ratio specifically unless the model offers a meaningful trade-off (some models have ratio-specific compositional behavior).
