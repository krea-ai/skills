# DTC Static Ad Formats

The concrete, generatable layer of the **Static Format Families** in
`marketing-creative-anatomy.md`. Each entry is an original, brand-agnostic
**structure + treatment** spec — not a copied competitor layout. Use it to turn **one
product reference photo** into a set of on-brand static ad stills, one finished image per
format. Driven by `../workflows/dtc-ad-templates.md`.

Two layers per format:

- **Structural device** — the thing that makes it *that* format (a two-panel split, a
  comparison diptych, leader-line callouts, a review card). This is also the QA target: if
  the device isn't legible in the output, the image is off-type and must be regenerated.
- **Treatment** — the art-direction recipe (light, palette, type, mood).

## A. How to use

1. Collect a brief (section B) and the product reference image.
2. Pick formats — default the **core set** (the table in F), or a subset the user names.
   **Drop** any format whose `required` fields the brief cannot honestly supply (no real
   press name → skip `press-feature`; no real quote → skip the testimonial formats). Never
   invent claims, quotes, press, ratings, or pricing.
3. For real product references, keep `{{product}}` category-level, such as "the referenced
   product" or "the referenced garment." Do not insert product color/material/garment
   descriptors; let the reference image carry the product.
4. Fill each chosen template's `{{placeholders}}` from the brief and append the universal
   tail (section D).
5. Generate (see the workflow) and vision-QA each output against its structural device.

## B. Placeholders

| token | meaning |
|---|---|
| `{{product}}` | product noun. With a real reference, use category-level wording such as "the referenced water bottle"; do not include material/color/garment descriptors |
| `{{brand}}` | brand name as it reads on the page |
| `{{wordmark}}` | wordmark text (usually the brand, rendered letter-spaced) |
| `{{headline}}` | the main line (short, ≤6 words unless the format is copy-led) |
| `{{subline}}` | supporting line, e.g. "category · key attributes · size" |
| `{{proof_points}}` | 3–5 short supported claims; render per format (slash-joined list, quoted small-caps labels, or one line each) |
| `{{attributes}}` | materials / contents / spec phrases for craft, utility, and benefit formats |
| `{{offer}}` | offer or CTA line (offer formats only) |
| `{{quote}}` / `{{attribution}}` | a real customer line and who said it (testimonial / UGC) |
| `{{publication}}` / `{{kicker}}` | press: a REAL outlet name (never invented) / a section label, composable (e.g. "THE SUMMER EDIT") |
| `{{caption}}` / `{{note}}` | before/after caption; handwritten organic-post note |
| `{{rival_label}}` / `{{rival_points}}` | the generic alternative's label and matched weaknesses (comparison) |
| `{{palette}}` / `{{accent}}` / `{{surface}}` | brand palette, single accent, staging surface |
| `{{aspect}}` / `{{aspect_px}}` | e.g. `4:5` / `1080×1350` (section E) |
| `{{orientation}}` | orientation word from the aspect map: portrait, square, or wide landscape |

Two classes of token, with different rules:

- **Proof tokens** — `{{proof_points}}`, `{{quote}}`, `{{attribution}}`, `{{publication}}`,
  `{{offer}}`, ratings — must come from the user. Never invent them; drop the line (or the
  whole format, when the token is `required`) instead.
- **Composable tokens** — `{{headline}}`, `{{subline}}`, `{{kicker}}`, `{{caption}}`,
  `{{note}}`, `{{rival_label}}`, `{{rival_points}}` — you may write these in brand voice
  when the user didn't supply them. Keep the rival generic ("the ordinary water bottle");
  never name a real competitor.

When visual tokens (`{{palette}}`, `{{accent}}`, `{{surface}}`) are unspecified, derive
them from the product reference: palette from the product's own colours plus neutrals,
accent from the brand colour, surface a neutral stone/linen/wood that suits the category.
Never emit an empty quote or a literal placeholder string into the image.

For real-product work, these templates describe the ad format, scene, light, copy, and
placement. The reference image defines the product's exact material, color, silhouette,
trim, hardware, label, and proportion.

## C. Treatments

- **HERO-CINEMATIC** — single product, one low-key practical light into near-black falloff; sparse serif headline; dramatic negative space.
- **STILL-LIFE-LUXE** — tabletop/coffret on stone or linen, soft directional light, a few tactile props; craft over abundance.
- **TESTIMONIAL-EDITORIAL** — one customer line as a large serif pull-quote over space; hairline stars; no UI card.
- **PRESS-EDITORIAL** — real magazine typography (masthead, kicker, standfirst) or a cinematic editorial portrait.
- **SPEC-MINIMAL** — product with hairline leader-line callouts to small-caps labels; one muted accent; vast space.
- **COMPARISON-EDITORIAL** — type-led two-column diptych split by one hairline; no VS badge, no checks/crosses, no color blocks.
- **LIFESTYLE-ANALOG** — real room / candid moment, natural or golden-hour light, 35mm grain, muted earthy palette; product present, not hero-lit.
- **EDITORIAL-COPY** — type-forward manifesto on paper; product a small quiet accent.

## D. Anti-slop taste system + universal tail

Kill: garish or neon gradients, sparkles, glitter, lens flares, starbursts, chunky badges,
rows of giant stars, sticker collages, plastic/CGI sheen, everything centered and
symmetric, emoji-style icons, walls of text, exclamation marks.

Do: photographic realism, one restrained type system (a high-contrast serif + a quiet
grotesque), a narrow low-saturation palette, generous negative space, asymmetric editorial
composition, tactile real materials, and confident minimal copy (one quiet proof point, not
five).

**Universal tail `<TAIL>`** — append to every filled template. This is a value-free
preservation instruction, not permission to name a specific color, material, garment, trim,
or hardware in the prompt:

> Keep the referenced product true to the provided image in shape, colour, material and proportion. Shot
> on medium-format or 35mm film, one practical or natural light source, real soft shadows,
> fine grain, believable shallow depth of field, generous negative space — a photograph,
> not a render. No garish gradients, sparkles, starbursts, sticker collages, chunky badges,
> CGI sheen, or centered symmetry.

## E. Aspect → pixel map

Default **`4:5` (1080×1350)** — the dominant paid-social static ratio. Override per brief.

| aspect | orientation | generic px | `openai/gpt-image-2` (÷16) |
|---|---|---|---|
| 4:5 | portrait | 1080×1350 | 1024×1280 |
| 1:1 | square | 1080×1080 | 1024×1024 |
| 3:4 | portrait | 1080×1440 | 1024×1360 |
| 9:16 | tall portrait | 1080×1920 | 1024×1824 |
| 16:9 (landscape / link placements) | wide landscape | 1920×1080 | 1824×1024 |

`openai/gpt-image-2` requires explicit `width`/`height` in multiples of 16 (use the right
column). `google/nano-banana-pro` takes `aspect_ratio={{aspect}}` instead.

## F. Format registry (core)

| id | family | treatment | structural device (QA target) | required |
|---|---|---|---|---|
| `headline-hero` | headline-led | HERO-CINEMATIC | lone product, single side light to near-black, one serif headline, tiny wordmark; no props | headline |
| `offer-still-life` | offer-led | STILL-LIFE-LUXE | tabletop still-life, offer as one quiet small-type line; no color field/starburst | offer |
| `bundle-set` | offer-led | STILL-LIFE-LUXE | open gift set revealing product + a few matching items; craft over abundance | — |
| `testimonial-quote` | social-proof-led | TESTIMONIAL-EDITORIAL | large italic serif pull-quote + hairline 5 stars + attribution; no card | quote |
| `press-feature` | social-proof-led | PRESS-EDITORIAL | flat-shot magazine spread: masthead + kicker + headline + standfirst + portrait | publication, headline |
| `ugc-two-panel` | social-proof-led | LIFESTYLE-ANALOG | two panels split by one hairline: candid photo top, minimal review card bottom | quote |
| `spec-leader-lines` | feature/benefit-led | SPEC-MINIMAL | 3–4 hairline leader lines to small-caps labels, one accent; no icons | proof_points |
| `benefits-stack` | feature/benefit-led | SPEC-MINIMAL | leader-line benefit labels + one quiet proof line; no checkmarks | proof_points |
| `comparison-diptych` | comparison-led | COMPARISON-EDITORIAL | type-led two-column diptych, one hairline; no VS badge / checks / color blocks | proof_points |
| `before-after` | comparison-led | LIFESTYLE-ANALOG | two-panel BEFORE (generic, cool) / AFTER (product, warm), one hairline | — |
| `magazine-portrait` | editorial-led | PRESS-EDITORIAL | cinematic full-bleed portrait, kicker top, one serif line lower | headline |
| `behind-the-product` | editorial-led | STILL-LIFE-LUXE | dark craft still-life of the product's real materials; low-key | attributes |
| `manifesto-copy` | editorial-led | EDITORIAL-COPY | type-forward letter: serif headline + column of short lines; product a small accent | headline |
| `whats-in-the-box` | utility-led | SPEC-MINIMAL | slightly-overhead flat-lay of product + included components, each labelled | attributes |
| `organic-post` | organic-post-led | LIFESTYLE-ANALOG | candid unpolished scene, handwritten note, only a slim footer line | — |
| `lifestyle-in-use` | organic-post-led | LIFESTYLE-ANALOG | candid person using the product, hands relaxed/out of focus; one quiet line | — |

Extras to add as needed: `comparison-table`, `customer-voices` (multi-quote flat-lay),
`mystery-hook`. Move **one** format lever at a time when making variants.

## G. Templates

Each ends with `<TAIL>` (section D). Drop any `{{token}}` line the brief can't fill.

**`headline-hero`** — Using the provided product image as the hero subject, create a {{orientation}} {{aspect}} ({{aspect_px}}) cinematic hero. Stand {{product}} alone, slightly off-center on a {{surface}}, lit by a single low-key practical light that catches it and falls off into near-black shadow; a narrow {{palette}}, real soft shadow, vast dark negative space to one side. In a top corner, one sparse high-contrast serif line in {{accent}} reading "{{headline}}", and a quiet small grotesque line beneath in muted grey reading "{{subline}}". A tiny letter-spaced "{{wordmark}}" wordmark sits low. `<TAIL>`

**`offer-still-life`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) still-life ad. Compose {{product}} on a {{surface}} dressed with crumpled linen and one or two restrained tactile props in soft directional window light; a narrow {{palette}}, real soft shadows, generous negative space. One restrained high-contrast serif line upper-left reading "{{headline}}", and a single quiet small grotesque line beneath in muted grey reading "{{offer}}". A tiny letter-spaced "{{wordmark}}" wordmark low-right. No color field, no badge, no starburst. `<TAIL>`

**`bundle-set`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) still-life of an open gift set. On a {{surface}} with a fold of natural linen, an open presentation box reveals {{product}} nested beside a few matching items and quiet tactile props; soft directional light, real shadows, uncluttered with generous negative space, off-center and unhurried — craft over abundance. One restrained high-contrast serif line reading "{{headline}}", a small spaced small-caps line beneath reading "{{subline}}". A tiny "{{wordmark}}" wordmark at the foot. `<TAIL>`

**`testimonial-quote`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) editorial testimonial on a soft {{surface}} ground. Set one short customer line LARGE as an italic high-contrast serif pull-quote across the upper negative space, wide letter-spacing and real hierarchy: "{{quote}}". Beneath it, small and quiet in a grotesque, an attribution reading "{{attribution}}", and a single hairline row of five small gold stars — no card, no UI chrome. {{product}} sits low and off-center, catching a single soft light, with a believable shadow and generous empty space. A tiny "{{wordmark}}" wordmark in the lower corner. `<TAIL>`

**`press-feature`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) image of a real printed magazine spread on warm cream paper, photographed flat. A slim elegant serif masthead reads "{{publication}}" across the top with a hairline rule beneath; a small letter-spaced grotesque kicker reads "{{kicker}}". One restrained high-contrast serif headline set large over generous white space reads "{{headline}}", with a short two-line serif standfirst beneath in soft grey. The lower two-thirds is a full-bleed portrait of a person in soft natural light, {{product}} resting beside them. `<TAIL>`

**`ugc-two-panel`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) two-panel layout split top-and-bottom by a single thin hairline rule into two clearly distinct halves. TOP panel: a warm, slightly grainy candid 35mm photo of a person using {{product}} in a real everyday moment, authentic phone-shot mood. BOTTOM panel: a clean minimal review card on soft off-white — a single hairline row of five small gold stars, an italic serif quote "{{quote}}", and a small grotesque attribution "{{attribution}}". The two panels must be visibly separate. A tiny "{{wordmark}}" wordmark at the foot. `<TAIL>`

**`spec-leader-lines`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) minimal spec study. Place {{product}} off-center on a {{surface}} in soft directional light, with vast negative space; a narrow {{palette}}, real soft shadows. Draw three or four hairline leader lines from points on {{product}} out to small-caps grotesque labels in muted grey, generously letter-spaced, reading {{proof_points}} — each a short quoted small-caps label — with a single muted {{accent}} accent on one leader. A tiny "{{wordmark}}" wordmark low-right. No badges, no icons, no gradient. `<TAIL>`

**`benefits-stack`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) minimal benefits study. Stand {{product}} off-center on a {{surface}} in soft directional daylight, generous negative space; a narrow {{palette}}, real soft shadows. Draw three hairline leader lines from {{product}} to small-caps grotesque labels in muted grey, well letter-spaced, reading {{proof_points}} — each a short quoted label — one in a single muted {{accent}}. Set one quiet proof line lower-left in small grotesque reading "{{subline}}". A tiny "{{wordmark}}" wordmark low-right. No badge, no button, no checkmarks, no gradient. `<TAIL>`

**`comparison-diptych`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) editorial comparison diptych, type-led on {{surface}} paper, two columns divided by a single thin vertical hairline rule. Left column header in quiet muted-grey small grotesque reading "{{rival_label}}"; right column header in elegant serif reading "{{brand}}", marked with one restrained {{accent}} underline. Under each, a short matched list in small grotesque separated by hairline rules: left reads "{{rival_points}}" and right reads "{{proof_points}}", matched line for line as short slash-separated phrases. Photograph {{product}} small and calm at lower-right in soft directional light, real soft shadow; vast negative space. No VS badge, no red crosses or green checks, no color blocks. `<TAIL>`

**`before-after`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) two-panel before-and-after, the frame split top-and-bottom by a single thin hairline gutter into two clearly separate photographs. TOP panel, small grotesque label "BEFORE": a cluttered scene of dull, generic alternatives in cool, flat, slightly desaturated light. BOTTOM panel, label "AFTER": {{product}} arranged calmly on a {{surface}} in warm golden-hour light, a muted {{palette}}. Both halves are real photographs and must be visibly distinct, divided by one clean hairline. A small high-contrast serif caption in the lower panel reads "{{caption}}", with a tiny "{{wordmark}}" wordmark. `<TAIL>`

**`magazine-portrait`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) cinematic fashion-magazine editorial: a full-bleed film portrait of a person in warm low light, {{product}} held quietly or resting near them. A small elegant uppercase kicker with generous letter-spacing sits top-center: "{{kicker}}". The lower third carries one restrained high-contrast serif line, not condensed, reading "{{headline}}". A quiet small grotesque line beneath reads "{{brand}}". One type system only, real editorial hierarchy, few words, no color-block accent words, no chrome. `<TAIL>`

**`behind-the-product`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) dark craft still-life centered on materials, not decoration. Rest {{product}} off-center on a dark honed {{surface}} with a few tactile, restrained props that evoke its real materials — no glitter, no clutter. Light it low-key from one side, deep shadow falloff to near-black. One short high-contrast serif line, mixing roman and italic, sits at the top: "{{headline}}". A single quiet small-caps grotesque line beneath, generously letter-spaced, reads "{{attributes}}". Tiny "{{wordmark}}" wordmark at the lower edge. `<TAIL>`

**`manifesto-copy`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) type-forward editorial manifesto on warm off-white paper, styled like a quiet letter. Top-left, one large high-contrast elegant serif headline over two lines: "{{headline}}". Below, a left-aligned column of short single serif lines with generous line spacing and real hierarchy: {{proof_points}}, set one short sentence per line. Let {{product}} sit small and quiet in the lower-right corner as a restrained accent, with a real soft shadow. Tiny "{{wordmark}}" wordmark in a quiet small grotesque at the lower-left. One type system, vast negative space, no graphic devices. `<TAIL>`

**`whats-in-the-box`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) utility "what's included" study, viewed from slightly above. Lay out {{product}} together with its included components, neatly spaced on a {{surface}} in soft even light; a narrow {{palette}}, generous negative space. Label each item with a small-caps grotesque caption, well letter-spaced, drawn from {{attributes}}, with a single muted {{accent}} as the only accent. One quiet high-contrast serif line reads "{{headline}}". A tiny "{{wordmark}}" wordmark in the corner. No badges, no icons, no gradient. `<TAIL>`

**`organic-post`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) candid, unpolished everyday moment: {{product}} resting on a {{surface}} with a real handwritten note curling against it reading "{{note}}". Everyday life sits softly out of focus around it. No headline, no badge. The only set type is a slim grotesque footer line reading "{{subline}}" beside a tiny "{{wordmark}}" wordmark. Soft natural daylight, warm homey muted palette, candid and a little imperfect. `<TAIL>`

**`lifestyle-in-use`** — …create a {{orientation}} {{aspect}} ({{aspect_px}}) analog lifestyle photograph: a candid golden-hour moment of a person naturally using {{product}} in a real setting; the product is present and held naturally, not hero-lit, with any hands relaxed, anatomically correct and out of focus — never the subject. Muted {{palette}}, real soft shadows, generous negative space. One quiet high-contrast serif line in the negative space reads "{{headline}}", with a small grotesque line beneath reading "{{brand}}". `<TAIL>`

## H. Worked example

Brief: brand **NORD**; product reference image for an insulated water bottle; proof
points "24-hour cold / leakproof seal / lifetime warranty"; headline "Cold for 24 hours.";
subline "Insulated Bottle · 750 ml · BPA-free"; aspect 4:5 on `openai/gpt-image-2`
(→ portrait, 1024×1280); palette "slate-bone-steel"; surface "charcoal stone"; accent
"warm bone". Because a real reference exists, `{{product}}` stays category-level:

> Using the provided product image as the hero subject, create a portrait 4:5 (1024×1280)
> cinematic hero. Stand the referenced insulated water bottle alone, slightly
> off-center on a charcoal stone surface, lit by a single low-key practical light that
> catches it and falls off into near-black shadow; a narrow slate-bone-steel palette, real
> soft shadow, vast dark negative space to one side. In a top corner, one sparse
> high-contrast serif line in warm bone reading "Cold for 24 hours.", and a quiet small
> grotesque line beneath in muted grey reading "Insulated Bottle · 750 ml · BPA-free". A
> tiny letter-spaced "NORD" wordmark sits low. Keep the referenced product true to the
> provided image in shape, colour, material and proportion. This is a preservation
> instruction, not a named color or material descriptor. Shot on medium-format film, one practical light
> source, real soft shadows, fine grain, believable shallow depth of field, generous
> negative space — a photograph, not a render. No garish gradients, sparkles, starbursts,
> sticker collages, chunky badges, CGI sheen, or centered symmetry.
