---
name: gpt-image-2-prompting
description: Prompting playbook for GPT-Image-2 and ChatGPT Images 2.0 style models, focused on structured image generation, edits, exact text, layout, transparent backgrounds, preservation, and production workflows.
---

# GPT-Image-2 Prompting Guide

Load this file only after the selected model is `openai/gpt-image-2`, ChatGPT Images 2.0, or a closely related OpenAI image model. This is not a recommendation to choose GPT-Image-2.

Always verify the live Krea model schema before submitting. Use only fields exposed by the selected model. Prompt examples here describe intent; schema controls such as size, quality, references, transparency, and masks must come from the live schema.

This guide distills OpenAI's GPT Image Generation Models Prompting Guide into reusable prompt craft for `gpt-image-2`.

## Core Prompting Fundamentals

Write prompts as production briefs, not keyword bags. The most reliable order is:

```text
Intended use / deliverable
Background or scene
Subject
Key visual details
Layout, camera, or artifact structure
Text, labels, or data if any
Constraints: what to avoid, preserve, or keep unchanged
```

For complex requests, use short labeled blocks or line breaks. Minimal prompts, paragraphs, JSON-like prompts, tag-based prompts, and numbered instructions can all work, but production templates should be easy to skim and maintain.

### Specificity And Quality Cues

Be concrete about visible details:

- materials: brushed steel, worn cotton, translucent plastic, ceramic glaze
- shapes and proportions: strong silhouette, rounded corners, compact body
- textures: pores, wrinkles, film grain, paper fibers, brushstrokes
- medium: photorealistic photo, watercolor, vector-like logo, app UI, classroom handout

Use targeted quality cues only where they matter. For photorealism, include `photorealistic` directly. Phrases like `real photograph`, `taken on a real camera`, `professional photography`, or `iPhone photo` can guide the general look, but exact camera specs should be treated as visual direction, not physical guarantees.

### Composition And Placement

Name framing, viewpoint, mood, and placement:

- framing: close-up, full body visible, medium close-up, wide establishing shot
- viewpoint: eye-level, top-down, low-angle, three-quarter view
- lighting: soft diffuse daylight, golden hour, high contrast, studio softbox
- placement: logo top-right, subject centered, negative space on left, footer at bottom

For wide cinematic, low-light, rain, neon, or atmospheric scenes, add scale, color, and environment details so the output does not become shallow mood styling.

### People, Pose, And Action

For people, describe body framing, scale, gaze, and interactions:

```text
Full body visible, feet included. The child is small relative to the table,
looking down at the open book rather than at the camera. Hands naturally
grip the handlebars.
```

These details help with body proportion, object interaction, and gaze alignment.

### Constraints And Iteration

State exclusions and invariants explicitly:

- `no watermark`
- `no extra text`
- `no logos or trademarks`
- `preserve identity, geometry, layout, brand elements`

For edits, use:

```text
Change only <target>. Keep everything else the same.
Preserve exactly: <identity, pose, camera, lighting, layout, text, labels>.
Do not alter: <saturation, contrast, arrows, labels, surrounding objects>.
```

Repeat the preserve list on every iteration. Debug with small single-change follow-ups instead of overloading one retake.

## Quality And Resolution Prompt Implications

Use live schema controls, not prompt prose, for quality and size. Prompt-writing implications:

- `low` can be enough for fast exploration and high-volume drafts.
- Compare `medium` or `high` for small text, dense infographics, close-up portraits, identity-sensitive edits, and high-resolution outputs.
- For dense labels, legends, axes, footnotes, or production slide assets, prefer a higher quality setting when the schema exposes one.
- If output above roughly 2K is used, inspect more carefully; large outputs can be more variable.

## Prompt Skeletons

### Text-To-Image

```text
Create <deliverable> for <audience/use>.
Scene/background: <where this happens>.
Subject: <who/what, action, pose, scale>.
Composition: <shot size, viewpoint, placement, aspect intent>.
Style: <medium, visual language, lighting, color>.
Details: <materials, textures, props, atmosphere>.
Constraints: <no extra text/logos/watermarks, safe margins, preserve simplicity>.
```

### Image Edit

```text
Edit the source image: <specific change>.
Change only: <region/object/text/style/background>.
Preserve exactly: <identity/product shape/layout/pose/camera/lighting/text>.
Integration: <match shadows, color temperature, occlusion, perspective>.
Constraints: do not add unrelated objects, do not change preserved details.
```

### Multi-Image Edit Or Composite

```text
Image 1: <role, e.g. product photo>.
Image 2: <role, e.g. style reference or background>.

Task: <apply Image 2's style to Image 1 / place subject from Image 1 into Image 2>.
Preserve from Image 1: <identity, shape, label, materials>.
Use from Image 2: <palette, texture, environment, camera, lighting>.
Constraints: <no extra elements, realistic contact shadows, consistent perspective>.
```

### Text And Layout

```text
Create <poster/card/banner/slide> with exact text:
Headline: "<exact headline>"
Subhead: "<exact subhead>"
Footer: "<exact footer>"
Layout: <headline largest, subhead medium, footer small, alignment, margins>.
Visual: <background subject/style/lighting>.
Typography: <font style, size relationship, color, placement, contrast>.
Constraints: no other words, all text correctly spelled, generous safe margins.
```

For unusual spellings or brand names, spell the word out letter-by-letter in the prompt.

## Generate Workflows

### Infographics

Prompt infographics as structured explainers for a specific audience. Include the topic, desired learning outcome, main components, flow/order, label requirements, and visual style.

```text
Create a detailed infographic for <audience> explaining <process>.
Show the flow from <step 1> to <step N>.
Include and label: <component list>.
Use arrows, numbered sections, simple icons, clear hierarchy, and enough
white space to scan quickly.
Avoid tiny text, decorative clutter, or extra labels not requested.
```

Use higher quality when the image contains dense labels or heavy in-image text.

### Translation And Localization

For localization edits, preserve everything except the text. Name layout invariants explicitly.

```text
Translate all visible text in the source image to <language>.
Preserve every non-text element exactly: imagery, icons, layout, typography
style, placement, spacing, hierarchy, logos, and colors.
Use natural, accurate translation with no extra words. Reflow only where
necessary to preserve readability.
```

### Natural Photorealism

Prompt like a real photo captured in the moment. Use natural imperfections and avoid over-polished language.

```text
Create a photorealistic candid photograph of <subject> <action>.
Details: <skin texture, fabric wear, real materials, everyday imperfections>.
Camera: <shot size, viewpoint, approximate lens/look>.
Lighting: <natural source, color balance, depth of field>.
Mood: honest, unposed, realistic.
Constraints: no glamorization, no heavy retouching, no staged studio look.
```

### World-Knowledge Scenes

When the scene depends on factual context, give time, place, and the realism target. The model can infer some context, but prompt the required visible constraints.

```text
Create a realistic scene set in <place> on <date or era>.
Make clothing, environment, objects, signage, and staging period-accurate.
Use <documentary / photorealistic / educational> visual style.
```

Avoid over-specifying uncertain facts. If exact historical accuracy matters, list the required items.

### Logos

Logo prompts should emphasize brand personality, originality, simplicity, silhouette, scalability, and negative space.

```text
Create an original, non-infringing logo for <brand>, <business/category>.
Brand feel: <personality>.
Use clean vector-like shapes, strong silhouette, balanced negative space,
and simple forms that read clearly at small and large sizes.
Plain background, single centered mark, generous padding.
Constraints: no watermark, no trademarks, no complex illustration.
```

For variants, request multiple outputs only when the schema supports it, then compare for distinct silhouettes.

### Ads And Campaign Images

Write ad prompts like creative briefs. Include brand, audience, culture/context, concept, composition, exact copy, and design constraints.

```text
Create a polished campaign image for <brand>.
Audience: <target audience>.
Brand positioning/vibe: <tone and culture>.
Scene/concept: <what is happening>.
Composition: <layout, poses, color direction>.
Exact copy: "<tagline>" rendered once, clearly and legibly.
Constraints: no extra text, no watermarks, no unrelated logos.
```

Let the model make taste-driven details inside those boundaries; do not reduce ads to a purely technical scene description.

### Comic Strips And Panels

Prompt comics as a sequence of visual beats. One action per panel.

```text
Create a <format> comic with <N> equal panels.
Panel 1: <concrete visual beat>.
Panel 2: <concrete visual beat>.
Panel 3: <concrete visual beat>.
Panel 4: <concrete visual beat>.
Use consistent character design, readable pacing, and clear panel separation.
No extra captions unless specified.
```

### UI Mockups

Describe the product as if it already exists. Focus on usability, hierarchy, spacing, and real interface elements. Avoid concept-art language.

```text
Create a realistic <device/platform> UI mockup for <product>.
Show: <real sections, cards, controls, navigation, data>.
Layout: <header/sidebar/grid/list, hierarchy, spacing>.
Visual language: <background, accent colors, typography, density>.
Make it look like a usable shipped interface, not a concept poster.
Avoid decorative clutter, fake marketing copy, and impractical controls.
```

### Scientific And Educational Visuals

Prompt as an instructional design brief: audience, lesson objective, visual format, labels, and scientific constraints.

```text
Create a <diagram/handout/slide> titled "<title>" for <audience>.
Lesson objective: <what the viewer should understand>.
Include: <required components and labels>.
Show relationships using <arrows, callouts, sequence, comparison>.
Style: clean flat educational visual system, consistent icons, readable labels,
white space, classroom-friendly colors.
Avoid tiny text, extra decoration, or scientifically misleading elements.
```

When accuracy matters, list required components explicitly and state what must not appear.

### Slides, Diagrams, Charts, And Productivity Images

Write these as artifact specs, not illustration prompts. Name the deliverable, canvas, hierarchy, real text/data, and visual language.

```text
Create one <slide/chart/workflow/page image> titled "<title>".
Canvas: <landscape/portrait, deck-style/page-style>.
Include:
- <specific chart/diagram type>
- <numbers, labels, axes, legends, footnotes>
- <logo placeholder or annotation if needed>
Design: <typography, spacing, color system, hierarchy>.
Constraints: readable text, polished spacing, no stock-photo treatment,
no decorative clutter, no gradients/shadows unless requested.
```

Use landscape sizes for deck-style output and higher quality for legends, axes, footnotes, and small labels.

### Merch, Packaging, And Product Concepts

Prompt early merch concepts like premium product photography with strict originality constraints.

```text
Create a <merch/product> concept of <original character/product> in <packaging>.
Concept: <emotional or commercial positioning>.
Style: premium product photography, realistic materials, studio lighting,
sharp label printing, high-end retail presentation.
Packaging text, verbatim: "<short copy>"
Constraints: original design only, no trademarks, no logos, no watermarks,
no extra packaging text.
```

## Edit Workflows

### Style Transfer

Use a reference image for visual language and a prompt for what changes.

```text
Use the style from the source image: <palette, texture, brushwork, grain>.
Generate <new subject/scene>.
Keep consistent: <style cues>.
Change: <content, subject, background, framing>.
Constraints: <white/plain background, no extra elements, no text>.
```

Do not just say "same style"; name the style cues that must transfer.

### Virtual Clothing Try-On

Lock the person and change only the garments. Require realistic fit and integration.

```text
Dress the person in the provided clothing images.
Do not change face, facial features, skin tone, body shape, pose, identity,
expression, hairstyle, or proportions.
Replace only the clothing. Fit garments naturally to the existing pose and
body geometry with realistic drape, folds, occlusion, lighting, shadows,
and color temperature. The outfit should look worn, not pasted on.
```

### Sketch Or Drawing To Render

Treat rough drawings as intent-preserving layout specs. Preserve the drawing's structure before adding realism.

```text
Turn the source drawing into a photorealistic image.
Preserve the exact layout, proportions, perspective, and composition.
Choose plausible real-world materials, lighting, and environment consistent
with the sketch intent.
Do not add new elements, text, logos, or decorative reinterpretations.
```

### Product Mockups And Label Integrity

For catalog, marketplace, and design-system extraction, protect edges and text. The OpenAI guide recommends an opaque plain background for `gpt-image-2` product extraction, then downstream background removal if a final transparent asset is required.

```text
Extract the product from the source image and place it on a plain white
opaque background.
Output: centered product, crisp silhouette, no halos or fringing.
Preserve product geometry and label legibility exactly.
Add only light polishing and a subtle realistic contact shadow.
Do not restyle the product; only remove the background and lightly polish.
```

### Product Or Subject Compositing

When combining references, assign each input a role and define the interaction.

```text
Image 1: <subject/product>.
Image 2: <target scene/background/style>.
Place <subject from Image 1> into <scene from Image 2>.
Preserve <product shape, label, materials, identity>.
Match <perspective, contact shadows, lighting, reflections, color temperature>.
Avoid <extra objects, warped labels, changed proportions>.
```

### Background Replacement

Background edits need the subject locked and environment integration described.

```text
Replace only the background with <new environment>.
Preserve the subject exactly: silhouette, pose, face/product shape, clothing,
label text, camera angle, and foreground lighting.
Integrate naturally with matching shadows, reflections, depth of field, and
color temperature.
```

### Lighting And Weather Transformation

Change environmental conditions only; preserve the scene identity.

```text
Transform only the environmental conditions to <overcast/dusk/snow/rain>.
Change lighting direction/quality, shadows, atmosphere, precipitation,
ground wetness, and color temperature as needed.
Preserve identity, geometry, camera angle, object placement, architecture,
people, products, and composition exactly.
```

### Object Removal

For removals, make the target and preservation boundary narrow.

```text
Remove only <object/person/mark> from the source image.
Reconstruct the background naturally where it was removed.
Do not change anything else: preserve composition, lighting, shadows,
camera angle, subject identity, surrounding objects, and image quality.
```

### Precision Interior Or Object Swaps

Use "replace ONLY" wording and preserve room context so the edit reads as a real photo rather than a redesign.

```text
In this room photo, replace ONLY <object/material/color> with <new object/material/color>.
Preserve camera angle, room lighting, floor shadows, surrounding objects,
wall/floor geometry, and all other aspects of the image.
Use photorealistic contact shadows, correct perspective, and realistic material texture.
```

### Surgical Text Or Layout Edits

For text edits, preserve every visual element except the target text.

```text
Change only the text "<old text>" to "<new text>".
Keep font style, size, color, placement, line breaks, spacing, layout,
background, icons, and all other text unchanged.
No extra words.
```

### Multi-Step Character Consistency

For story or series work, create a character anchor first, then use it as an image input for later scenes.

Anchor prompt:

```text
Create a character reference image for <project>.
Character: <appearance, proportions, outfit, expression, personality>.
Style: <medium, palette, line/paint/render treatment>.
Constraints: original character, no text, no watermark, plain background,
clear full design for reuse.
```

Continuation prompt:

```text
Continue using the same character from the source image.
Scene: <new story beat and action>.
Character consistency: same facial features, proportions, outfit, palette,
personality, and design language.
Style: <same style plus new environment/mood>.
Constraints: do not redesign the character, no text, no watermark.
```

## Transparent Backgrounds And Cutouts

When the requested output is a sticker, icon, product cutout, or asset:

```text
Create a clean cutout of <subject>.
Preserve exact silhouette and visible materials. Centered composition,
crisp edges, plain background, no text, no watermark.
```

For product extraction where label integrity matters, prefer a plain opaque background first and remove the background downstream. If the live schema explicitly supports transparency and the task is a simple sticker/icon/cutout, use that schema field instead of relying on prompt words alone.

## Retake Pattern

After vision QA, retake with one concise correction and repeat critical invariants:

```text
Retake: preserve the previous composition, lighting, subject identity, and
layout. Correct only <single issue>. Do not alter <protected details>.
```

Good retakes:

- "Correct only the headline spelling to `NIGHT MARKET`; remove all extra background words."
- "Restore the original background and change only the jacket color."
- "Keep the same chart layout and increase label contrast."

Do not stack unrelated fixes unless the output is unusable.

## Common Failure Fixes

| Symptom | Fix |
|---|---|
| Extra text appears | Add "no extra text" / "no other words" and reduce decorative signage language |
| Text misspelled | Quote exact text, spell unusual words letter-by-letter, shorten copy, use higher quality |
| Layout is busy | Specify hierarchy, alignment, margins, and one focal point |
| Infographic is hard to scan | Add audience, objective, required labels, arrows, white space, and "avoid tiny text" |
| Photoreal image feels staged | Ask for candid real-photo language, imperfections, natural light, no glamorization |
| Person identity drifts | Put face/body/pose/hair/expression preserve list immediately after the edit request |
| Sketch render invents new details | Preserve exact layout, proportions, perspective, and say not to add elements/text |
| Product extraction has halos | Ask for plain opaque background, crisp silhouette, no halos/fringing, light polish only |
| Clothing try-on looks pasted | Require drape, folds, occlusion, shadows, color temperature, and existing body geometry |
| Lighting/weather edit changes the scene | Limit changes to environment; preserve geometry, camera, objects, and placement |
| Object removal changes nearby content | Use "remove only" and list surrounding elements to preserve |
| Product label warps | Preserve label text and proportions; use source image as reference; request realistic perspective |
| UI looks like concept art | Name real interface sections, controls, hierarchy, spacing, and "usable shipped interface" |
| Character changes across pages | Create a character anchor, reuse it as image input, repeat appearance/proportion/outfit constraints |
| Edit changes too much | Use "change only..." and list every protected element |
| Wrong dimensions | Inspect schema; for GPT-image style models in Krea, explicit width/height may be required and may need multiples of 16 |

## Public Source Pointers

- `https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide`
- `https://help.openai.com/en/articles/11084440-chatgpt-image-library`
- `https://help.openai.com/en/articles/6654000-best-practices`
