---
name: nano-banana-prompting
description: Prompting playbook for Nano Banana, Nano Banana 2, Nano Banana Pro, and Gemini image models, focused on verb-led image prompts, editing, subject consistency, multi-image stories, and production specs.
---

# Nano Banana Prompting Guide

Load this file only after the selected model is a Nano Banana, Nano Banana 2, Nano Banana Pro, Gemini Image, or closely related Google image model. This is not a recommendation to choose Nano Banana.

Always verify the live Krea model schema before submitting. Use only fields exposed by the selected model.

## Core Pattern

Start with a strong verb and describe the desired image in concrete visual terms.

```text
<Create/Edit/Transform/Reframe/Upscale> <subject> <action>
in <setting/context>, <composition>, <style>, <lighting>, <production spec>.
```

Useful prompt ingredients:

- subject: who or what is visible
- action: what is happening
- setting: where it happens
- composition: shot size, angle, aspect, focal point
- style: photo, watercolor, claymation, editorial, 3D render, etc.
- lighting: daylight, rim light, overcast, neon, softbox
- output: vertical social post, widescreen backdrop, product mockup, 4K

## Text-To-Image

Text-only prompts need narrative detail, not keyword piles.

Weak:

```text
fashion model, red background, editorial
```

Strong:

```text
Create a fashion editorial image of a model in a tailored brown dress and
sleek boots, posing with a confident statuesque stance against a seamless
deep cherry red studio backdrop. Medium-full shot, center-framed,
medium-format analog film look, pronounced grain, high saturation,
cinematic softbox lighting.
```

## Image Editing

Nano Banana handles iterative edits well when the prompt says what to change and what to preserve.

```text
Edit the source image: change the jacket to matte black leather.
Keep the person's face, pose, hairstyle, camera angle, background,
lighting, and overall composition unchanged.
```

For style transformations:

```text
Transform the source image into a watercolor illustration with soft paper
texture and loose ink edges. Preserve the subject identity, pose, outfit
colors, and background layout.
```

## Positive Framing

Prefer what should appear over what should not appear:

| Instead of | Use |
|---|---|
| no blur | tack sharp subject, crisp focus |
| no cars | empty quiet street |
| no text | clean image with unmarked surfaces |
| don't change the face | preserve the exact face, expression, and head angle |
| no messy background | minimal uncluttered background |

Negative constraints can still be useful at the tail, but they should not carry the main prompt.

## Subject Consistency

For same-subject variants, pass the source image and explicitly ask for the new view or context.

```text
Create three alternate views of the same ceramic lamp from the source image:
front three-quarter, side profile, and overhead detail. Preserve the exact
ceramic shape, glaze color, proportions, cord placement, and visible texture.
Use the same warm studio lighting and neutral background.
```

Do not ask for same-subject variants with text only if a source image exists. Use the image as the reference.

## Multi-Image Stories

When asking for a short sequence, define the constant subject plus what changes frame by frame.

```text
Create a four-panel visual story using the same small blue robot from the
source image. Panel 1: robot finds a glowing seed in a rainy alley.
Panel 2: robot plants it in a cracked sidewalk. Panel 3: green light grows
up around the robot. Panel 4: a tiny tree glows beside the robot at dawn.
Preserve the robot's shape, face screen, color, proportions, and friendly
expression across all panels.
```

If the live schema supports multiple outputs or structured references, use schema fields for that. If not, generate one panel at a time with the same source image and repeated preserve list.

## Production Specs

Nano Banana prompts can include practical output targets:

- `vertical 9:16 social post`
- `4:5 editorial product image`
- `16:9 widescreen website hero`
- `square app icon composition`
- `2K clean product mockup`
- `4K final render`

Still pass aspect, size, and resolution through schema fields when they exist. Prompt words are not a substitute for schema controls.

## Text In Images

Nano Banana can handle text, especially when the copy is short and the layout is simple.

```text
Create a square label mockup with exact text "BLOOM TEA" as the large
centered brand name and "JASMINE" as a smaller line underneath. Cream paper
label, dark green serif lettering, botanical line art border, no other words.
```

If spelling fails after one retry, reduce copy or route to an external typography overlay workflow.

## Conversational Follow-Ups

Follow-up edits should be short but specific:

```text
Make the background a sunlit kitchen instead. Keep the mug, camera angle,
hand position, steam, and soft morning light unchanged.
```

```text
Try a lower camera angle, as if shot from tabletop height. Preserve the same
product design, label text, color, and studio lighting.
```

## Common Failure Fixes

| Symptom | Fix |
|---|---|
| Output is generic | Add action, setting, composition, lighting, and production format |
| Edit changes identity | Put preserve list immediately after the change request |
| Too much changed | Use "change only..." and reduce style pressure |
| Same subject drifts across views | Reuse the same source image and repeat exact preserved traits |
| Text is wrong | Shorten copy, quote exact text, specify hierarchy and "no other words" |
| Aspect is ignored | Inspect schema and pass explicit width/height when available |
| Result feels over-stylized | Reduce style adjectives and ask for natural materials, lighting, and texture |

## Retake Pattern

Use one correction at a time:

```text
Retake: preserve the previous image exactly except make the jacket matte
black leather. Do not alter the face, pose, background, or lighting.
```

## Public Source Pointers

- `https://deepmind.google/models/gemini-image/prompt-guide/`
- `https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana`
- `https://ai.google.dev/gemini-api/docs/image-generation`
