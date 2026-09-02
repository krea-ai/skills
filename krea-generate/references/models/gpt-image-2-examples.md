---
name: gpt-image-2-examples
description: Searchable concrete prompt examples for GPT-Image-2, adapted from OpenAI's GPT image prompting guide. Load only the section matching the active workflow.
---

# GPT-Image-2 Examples

Use only after reading `gpt-image-2.md`. Search by heading and read the smallest matching section:

```bash
rg -n "^##|^###" gpt-image-2-examples.md
```

These examples are adapted from OpenAI's GPT Image Generation Models Prompting Guide. They are prompt cards for reuse and modification, not API payloads. Always apply live Krea schema fields for size, quality, references, masks, and background.

## Generate Examples

### Infographic

Use when the deliverable explains a process, system, timeline, or labeled concept for a defined audience.

```text
Create a detailed infographic for curious home coffee drinkers
explaining how an automatic espresso machine works.

Show the complete flow from bean hopper to grinder, dosing chamber, water
tank, pump, boiler, brew group, pressure path, coffee spouts, and used-puck
bin. Use numbered sections, arrows, cutaway details, short labels, and a
clean technical illustration style.

The goal is to understand the machine visually and mechanically. Keep labels
readable, spacing generous, and avoid decorative clutter or tiny text.
```

Retake lever: if crowded, reduce the component list and ask for bigger labels and fewer arrows.

### Localization

Use when translating an existing design without rebuilding it.

```text
Translate all visible text in the source infographic into Spanish.

Preserve everything else exactly: diagrams, arrows, icons, colors, layout,
typography style, spacing, hierarchy, margins, and image content.

Use natural Spanish. Do not add extra words. Reflow text only where needed
to keep labels readable and aligned with the original design.
```

Retake lever: name the specific label that mistranslated and ask to correct only that label.

### Natural Photorealism

Use when the image should feel captured, unposed, and materially real.

```text
Create a photorealistic candid photograph of an older harbor mechanic
standing beside a small weathered workboat.

He has sun-worn skin, visible pores, wrinkles, faded forearm tattoos, and
rough work gloves. He is tightening a rope while a scruffy dog waits on the
deck nearby. Medium close-up at eye level, real 35mm film-photo feeling,
soft coastal daylight, shallow depth of field, subtle grain, natural color.

The image should feel honest and unposed, with worn fabric, chipped paint,
salt residue, and everyday imperfections. No glamorization, no heavy
retouching, no staged studio look.
```

Retake lever: if too polished, add "documentary snapshot, imperfect posture, uneven daylight, no fashion styling."

### World-Knowledge Scene

Use when the image depends on time, place, or historical context.

```text
Create a realistic outdoor music-festival crowd scene in Bethel, New York,
mid-August 1969.

Photorealistic documentary style. Make clothing, hair, stage equipment,
vehicles, blankets, signage, and crowd behavior period-accurate. Wide scene
with muddy grass, summer haze, informal gathering energy, and no modern
objects.
```

Retake lever: list the specific historical inaccuracies to remove.

### Logo

Use for original, scalable identity exploration. For multiple directions, run several generations (batch), not one grid image.

```text
Create an original logo for "Miller & Seed", a neighborhood bakery focused
on sourdough and seasonal pastries.

The brand should feel warm, simple, timeless, and local. Use clean
vector-like shapes, a strong silhouette, balanced negative space, and a form
that reads clearly at small and large sizes.

Flat design, minimal strokes, plain background, a single centered mark,
generous padding. No watermark, no mockup scene, no trademarked symbols, no
complex illustration.
```

Retake lever: if the marks are too detailed, ask for simpler silhouette-only logos.

### Ad

Use when the model should infer taste from brand, audience, and culture.

```text
Create a polished campaign image for a fictional streetwear brand called
"Threadline".

Audience: young urban creatives who care about style, music, and making
things together. Scene: a group of friends hanging out after a late-night
studio session, wearing clean contemporary streetwear, relaxed and natural.

Composition: premium fashion photography, strong color direction, natural
poses, crisp styling, tasteful energy, room for one tagline.

Exact tagline, rendered once and legibly: "YOURS TO CREATE"

No extra text, no watermarks, no unrelated logos.
```

Retake lever: if the image feels generic, specify the subculture, location, and palette more tightly.

### Comic Strip

Use when converting a story into a panel sequence.

```text
Create a comic-style reel with four equal panels.

Panel 1: A person leaves through the apartment door; their small pet is
visible in the window behind them, tiny against the glass, paws raised.
Panel 2: The door clicks shut. The pet turns toward the empty living room
with sudden mischievous focus.
Panel 3: The living room has become the pet's kingdom: cushions displaced,
snacks scattered, sunbeam like a spotlight across the couch.
Panel 4: The door opens again. The pet sits neatly by the entrance, calm
and innocent, as if nothing happened.

Keep the pet design consistent across all panels. Clear panel borders, no
extra captions unless needed.
```

Retake lever: if continuity fails, create a pet character anchor and reuse it as image input.

### UI Mockup

Use for realistic app/product UI, not concept art.

```text
Create a realistic iPhone app UI mockup for a local weekend farmers market.

Show today's market with a simple header, vendor list with small photos and
categories, a "Today's specials" section, location and hours, and a bottom
navigation bar. White background, subtle natural accent colors, clear
typography, practical spacing, minimal decoration.

It should look like a usable shipped app for a small local market, not a
marketing poster or concept-art screen.
```

Retake lever: if fake or decorative, ask for denser real controls, clearer navigation, and less hero imagery.

### Scientific Diagram

Use for instructional diagrams where accuracy and labels matter.

```text
Create a classroom diagram titled "Cellular Respiration at a Glance"
for high school biology students.

Show how glucose becomes usable cell energy. Include glycolysis, the Krebs
cycle, and the electron transport chain. Use arrows to connect steps and
label: glucose, pyruvate, ATP, NADH, FADH2, CO2, O2, and H2O.

Clean handout style, white background, simple icons, readable labels,
consistent arrows, and enough white space for scanning. Avoid tiny text,
extra decoration, and misleading biology.
```

Retake lever: if labels are wrong, ask to correct only the specific labels and preserve layout.

### Slide / Chart

Use for deck-style productivity visuals with real numbers.

```text
Create one pitch-deck slide titled "Market Opportunity".

Canvas: clean Series A fundraising slide, white background, modern sans-serif
type, crisp minimal layout.

Include:
- TAM / SAM / SOM concentric-circle diagram in muted blues and grays
- TAM: $42B
- SAM: $8.7B
- SOM: $340M
- Small bar chart showing growth from 2021 to 2026 with a steady upward trend
- Footnotes: "Market scan, 2024" and "Internal analysis"
- Small company-logo placeholder bottom-right

Make the hierarchy highly readable and professionally spaced. Avoid clip art,
stock photography, gradients, shadows, and decorative filler.
```

Retake lever: if text is small, ask for fewer elements, larger labels, and higher contrast.

### Merch / Packaging

Use for original product concepts and packaging exploration.

```text
Create a premium product concept image for a limited-edition desk toy called
"Orbit Cat", an original astronaut-cat character in a small retail box.

Show the figure and packaging together on a clean studio surface. Materials:
soft vinyl toy, glossy helmet visor, matte printed box, crisp label printing.

Packaging text, exact: "ORBIT CAT"
Small subtitle, exact: "DESK EXPLORER"

High-end retail presentation, soft studio lighting, realistic shadows,
original design only. No trademarks, no unrelated logos, no extra packaging
copy, no watermark.
```

Retake lever: if label text warps, shorten copy and ask to preserve exact packaging text.

## Edit Examples

### Style Transfer

Use when one image supplies visual language and the new prompt supplies content.

```text
Use the visual style of the source image: its blocky pixel texture, saturated
palette, simple shapes, and playful lighting.

Generate a person riding a motorcycle on a plain white background in that
same style. Preserve the source style cues, but change the subject to the
motorcycle rider.

No extra objects, no text, no watermark.
```

Retake lever: name the exact style cue that failed to transfer.

### Virtual Try-On

Use for ecommerce previews where identity preservation is critical.

```text
Put the supplied garments on the person in the source photo.

Shape the garments naturally around the existing pose with believable fabric
weight, folds, overlaps, shadows, and matching color temperature. Preserve
the person's exact identity. Otherwise keep the source image unchanged.
```

Retake lever: if identity drifts, retry from the source and name identity as the critical invariant.

### Sketch To Render

Use when turning a sketch into a realistic concept without losing layout.

```text
Render the source sketch photorealistically with believable real-world
materials, lighting, terrain, and atmosphere. Preserve its exact structure
and composition; do not add new scene elements.
```

Retake lever: if it invents details, name the unwanted addition and ask to remove only that.

### Product Extraction

Use for marketplace/catalog prep where edges and labels matter.

```text
Place the source product on a solid white opaque background with clean edges,
no halos, subtle cleanup, and a restrained contact shadow. Preserve the
product and its exact label text; do not redesign it.
```

Retake lever: if the label changes, ask to preserve label text exactly and reduce polishing.

### Marketing Creative With Real Text

Use when editing or generating a marketing asset with readable copy.

```text
Create a clean square social ad for a fictional skincare serum.

Product in center, soft bathroom daylight, pale green and white palette,
minimal premium composition.

Exact headline: "GLOW WITHOUT GUESSWORK"
Exact CTA: "SHOP THE SERUM"

Headline large at top, product centered, CTA small at bottom. Clean sans-serif
typography, high contrast, generous margins. No other words, no watermark,
no extra logos.
```

Retake lever: if text is wrong, correct only the exact text and remove all extra words.

### Background Replacement

Use when replacing only the environment.

```text
Replace only the background with a bright modern kitchen in soft morning
light. Integrate it naturally with matching shadows, reflections, depth of
field, and color temperature. Otherwise preserve the source image exactly,
including the composition.
```

Retake lever: if the subject changes, retry from the source and name only the changed subject detail to restore.

### Lighting / Weather

Use when changing environmental conditions but not identity or geometry.

```text
Transform only the environmental conditions to a quiet rainy dusk scene.

Change lighting direction, shadow softness, sky tone, wet ground reflections,
air haze, and color temperature. Add subtle rain only where it fits the scene.
Otherwise preserve the source image exactly, including the composition.
```

Retake lever: if geometry shifts, ask to restore the original camera and object positions.

### Object Removal

Use for precise removals.

```text
Remove only the red traffic cone from the sidewalk.

Reconstruct the sidewalk texture naturally where it was removed. Otherwise
preserve the source image exactly, including the composition.
```

Retake lever: if surrounding content changes, name the changed object and tell it to restore it.

### Interior Swap

Use for surgical material, color, or furniture changes.

```text
Replace only the blue sofa with a deep forest green velvet sofa of the same
size and placement. Use photorealistic fabric texture, correct perspective,
and natural contact shadows. Otherwise preserve the source image exactly,
including the composition.
```

Retake lever: if the room redesigns, retry from the source and name only the unintended change to restore.

### Text Edit

Use for surgical text correction on an existing design.

```text
Change only the text "SUMMER SALE" to "SPRING SALE".

Match the existing typography exactly. Otherwise preserve the source image
exactly, including all other text and the composition.
```

Retake lever: if font changes, ask to restore exact typography and change only letters.

### Character Anchor

Use before a multi-step story or comic workflow.

```text
Create a reusable character reference image for an original young inventor.

Character: round glasses, short dark curls, yellow utility jacket, teal
tool belt, expressive eyebrows, compact proportions, curious confident
personality.

Style: clean colorful storybook illustration with soft ink lines and warm
lighting. Plain background, full design visible, no text, no watermark.
```

Retake lever: if later scenes drift, reuse this anchor image and repeat outfit, proportions, and facial features.

### Character Continuation

Use after a character anchor exists.

```text
Continue using the same inventor character from the source image.

Scene: the inventor kneels beside a tiny robot that has just powered on,
holding a screwdriver in one hand and smiling with surprised pride.

Character consistency: same face, glasses, curls, yellow jacket, teal tool
belt, proportions, palette, and storybook line style.

Do not redesign the character. No text, no watermark.
```

Retake lever: if the character changes, ask to restore the anchor's face, outfit, and proportions exactly.

## Retake Examples

### Text Correction

```text
Retake: correct only the headline spelling to "NIGHT MARKET" and remove the
extra background words. Otherwise preserve the poster exactly.
```

### Identity Drift

```text
Retake from the source: apply the clothing edit without changing the person's
identity. Otherwise preserve the source image exactly.
```

### Layout Clutter

```text
Retake: keep the same infographic topic and visual style, but simplify the
layout to five large numbered steps, bigger labels, fewer arrows, and more
white space. Remove decorative elements that do not explain the process.
```

### Label Preservation

```text
Retake: only clean the background and improve the edge silhouette. Preserve
the product's exact label text; otherwise keep the source product unchanged.
```

## Source

- `https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide`
