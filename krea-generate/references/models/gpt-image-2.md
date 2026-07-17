---
name: gpt-image-2-prompting
description: Prompting playbook for GPT-Image-2 and ChatGPT Images 2.0 style models, focused on structured image generation, edits, exact text, layout, transparent backgrounds, and preservation.
---

# GPT-Image-2 Prompting Guide

Load this file only after the selected model is `openai/gpt-image-2`, ChatGPT Images 2.0, or a closely related OpenAI image model. This is not a recommendation to choose GPT-Image-2.

Always verify the live Krea model schema before submitting. Use only fields exposed by the selected model.

## What This Model Rewards

GPT-Image-2 follows explicit instructions well. Write prompts like a compact creative brief:

1. Start with the operation.
2. State the subject and visible result.
3. Define layout, camera, style, lighting, and aspect.
4. Quote exact text when text appears in the image.
5. List preservation constraints for edits.
6. End with hard output constraints.

Good operations:

- `Create`
- `Edit`
- `Replace`
- `Remove`
- `Add`
- `Extend`
- `Reframe`
- `Make the background transparent`

## Prompt Skeletons

### Text-To-Image

```text
Create <format/aspect> image of <subject> in <setting>.
Composition: <shot size, camera angle, layout, focal point>.
Style: <medium, art direction, color, lighting>.
Details: <materials, props, expression, atmosphere>.
Constraints: <no extra text/logos unless specified, clean edges, safe margins>.
```

### Image Edit

```text
Edit the source image: <specific change>.
Preserve exactly: <identity/product shape/layout/pose/camera/lighting/text>.
Adjust only: <region/object/style/background>.
Output: <aspect/quality/background/margins>.
Constraints: do not add unrelated objects, do not change preserved details.
```

### Text And Layout

```text
Create <poster/card/banner> with exact text:
Headline: "<exact headline>"
Subhead: "<exact subhead>"
Footer: "<exact footer>"
Layout: <headline largest, subhead medium, footer small, alignment, margins>.
Visual: <background subject/style/lighting>.
Constraints: no other words, all text correctly spelled, high contrast,
generous safe margins.
```

## Text Rendering

GPT-Image-2 is a strong choice for text-heavy prompts, but text still needs explicit handling:

- Keep copy short.
- Quote exact words.
- Declare hierarchy by role, not just "make a poster".
- Say "no other words" when extra text would be a failure.
- For long copy, generate the image background separately and add final typography outside the image model.

Bad:

```text
Make a cool event poster for Night Market with date and details.
```

Better:

```text
Create a vertical 4:5 event poster. Exact text only:
Headline: "NIGHT MARKET"
Subhead: "FRIDAY 8 PM"
Footer: "PIER 3"
Largest headline centered at top, subhead below, footer small at bottom.
Neon street-food photography, wet pavement reflections, high contrast,
clean margins, no other words.
```

## Editing Discipline

For edits, do not redescribe the whole image as if generating from scratch. Lead with the desired delta and preserve list.

Strong edit prompt:

```text
Edit the source image by changing only the sofa fabric to deep forest green
velvet. Preserve the room layout, camera angle, window light, wall art,
floor, pillows, and all object positions. Keep the result photorealistic
with natural fabric texture.
```

When a user points to an implicit prior output ("make it red", "try a new angle"), use that image as the source input. Prompt-only regeneration is not a valid same-subject edit.

## Transparent Backgrounds And Cutouts

When the requested output is a sticker, icon, product cutout, or asset:

```text
Create a clean product cutout of <subject> on a transparent background.
Preserve exact silhouette and visible materials. Centered composition,
soft natural contact shadow only if transparency supports it, crisp edges,
no backdrop, no text.
```

If the live schema has a background/transparency field, use that field instead of relying on prompt words alone.

## Complex Editorial Changes

For multi-part edits, structure the prompt as a numbered change list:

```text
Edit the source image:
1. Replace the sky with a soft overcast dawn sky.
2. Add warm interior lights in the visible windows.
3. Change the ground from dry concrete to lightly wet pavement.

Preserve exactly: building massing, window rhythm, camera perspective,
facade proportions, signage text, and all people positions.
```

Keep each requested change compatible with the source image. If the prompt asks for a new camera angle, new pose, and new scene at once, treat it as a controlled variation and use strong reference/preservation language.

## Common Failure Fixes

| Symptom | Fix |
|---|---|
| Extra text appears | Add "no other words" and reduce decorative signage language |
| Text misspelled | Shorten copy, quote exact text by role, increase text contrast |
| Source identity drifts | Move the preserve list earlier and make the change more local |
| Layout is busy | Specify alignment, safe margins, and one focal point |
| Edit changes too much | Use "change only..." and list every protected element |
| Wrong dimensions | Inspect schema; for GPT-image style models in Krea, explicit width/height may be required and may need multiples of 16 |

## Retake Pattern

After vision QA, retake with one concise correction:

```text
Retake: keep the previous composition and lighting. Correct only the
headline spelling to "NIGHT MARKET"; remove all extra background words.
```

Do not stack unrelated fixes in one retake unless the output is unusable.

## Public Source Pointers

- `https://help.openai.com/en/articles/11084440-chatgpt-image-library`
- `https://help.openai.com/en/articles/6654000-best-practices`
