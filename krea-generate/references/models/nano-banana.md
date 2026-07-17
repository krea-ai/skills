---
name: nano-banana-prompting
description: Prompting playbook for Nano Banana, Nano Banana 2, Nano Banana Pro, and Gemini image models, focused on verb-led generation, multimodal references, editing, text rendering, localization, and creative-direction controls.
---

# Nano Banana Prompting Guide

Load this file only after the selected model is a Nano Banana, Nano Banana 2, Nano Banana Pro, Gemini Image, or closely related Google image model. This is not a recommendation to choose Nano Banana.

Always verify the live Krea model schema before submitting. Use only fields exposed by the selected model. Prompt examples here describe intent; schema controls such as aspect, size, resolution, reference images, documents, masks, and web/search options must come from the live schema.

This guide distills Google's official Nano Banana prompting guide into reusable prompt craft for the Nano Banana model family.

## Examples Appendix

For concrete prompt examples, search `nano-banana-examples.md` by heading and read only the matching section:

```bash
rg -n "^##|^###" nano-banana-examples.md
rg -n "Text-To-Image|Multimodal Reference|Text Rendering" nano-banana-examples.md
```

Do not load the full examples appendix unless the relevant section cannot be identified.

## When To Load Examples

Load `nano-banana-examples.md` when the task is a first attempt in a concrete workflow, involves references, needs text/localization, asks for visual style control, or needs a retake after one failed output.

| Task | Search terms |
|---|---|
| text-only image generation | `Text-To-Image` |
| reference image combination, product in scene, design mockup | `Multimodal Reference|Composition` |
| object/person removal or surgical edit | `Conversational Edit|Object Removal` |
| style transfer | `Style Transfer` |
| real-time data, current weather, local context | `Real-Time Information` |
| poster, typography, translated text | `Text Rendering|Localization|Typographic Poster` |
| lighting setup | `Lighting` |
| camera angle, lens, focus, action look | `Camera / Lens / Focus` |
| color grade, film stock, visual mood | `Color Grading` |
| product material, character texture, surface detail | `Materiality` |
| same-subject variants or panels | `Subject Consistency|Multi-Image Story` |
| failed output retake | `Retake Examples` |

## Core Pattern

Start with a strong verb that tells the model the operation:

```text
Create / Edit / Transform / Combine / Replace / Remove / Localize / Render
```

Then describe the desired image in concrete visual terms:

```text
<Operation> <subject> <action>
in <location/context>, <composition>, <style>, <lighting>, <production spec>.
```

## Best Practices

- Be specific about subject, lighting, composition, materials, and context.
- Use positive framing: describe the desired state instead of relying on negatives.
- Control the camera with terms like low angle, aerial view, macro lens, wide-angle lens, shallow depth of field, or top-down view.
- Iterate conversationally with short follow-up prompts.
- Use schema fields for aspect, size, quality, reference images, and resolution; prompt words are not a substitute for controls.

Positive framing examples:

| Instead of | Use |
|---|---|
| no blur | tack sharp subject, crisp focus |
| no cars | empty quiet street |
| no text | clean unmarked surfaces |
| don't change the face | preserve the exact face, expression, and head angle |
| no messy background | minimal uncluttered background |

## Text-To-Image Without References

When starting from text only, write narratively. A keyword list is usually too weak.

Formula:

```text
Subject + action + location/context + composition + style
```

Include action and composition even for static-looking images. Good prompts describe what the subject is doing, where it is, how it is framed, and the intended visual style.

## Multimodal Generation With References

When using reference images, define each reference's role and relationship to the output.

Formula:

```text
Reference images + relationship instruction + new scenario
```

Examples of relationship instructions:

- use this sketch as structure
- use this fabric as material texture
- preserve this product shape and label
- place this subject into this new environment
- keep this character identity but change the scene

Do not assume references are self-explanatory. Name what to take from each reference and what not to take.

## Image Editing

Editing requires a different prompt shape from generation. The base image already contains the subject; focus on what changes and what stays fixed.

```text
Edit the source image: <specific change>.
Change only: <target object/region/style/background>.
Preserve exactly: <identity, pose, camera, lighting, composition, labels, surrounding objects>.
```

Nano Banana responds well to conversational edits. Keep follow-ups short, but include a preserve list whenever identity, layout, product, or text matters.

## Text Rendering And Localization

For typographic work:

- quote exact words
- specify font style, weight, color, placement, hierarchy, and line breaks
- specify the target language for translation/localization
- keep copy short
- for complex campaigns, first generate or approve the text concepts, then request the image with that exact text

Prompt pattern:

```text
Render exact text: "<copy>".
Typography: <font style, weight, color, size relationship, placement>.
Translate/localize into <target language> if needed.
No extra words.
```

## Real-Time Information

If the selected Krea model/schema exposes live web/search or current-data capability, prompt with:

```text
Source/search request + analytical task + visual translation
```

Example structure:

```text
Search for <current data>. Use the result to decide <visual condition>.
Visualize the result as <scene/UI/diagram/concept>.
```

If the live Krea surface does not expose current-data capability, do not pretend it can search. Ask for the data or use another authorized current-data source.

## Creative Director Controls

Use these controls to move beyond generic output:

- **Lighting:** three-point softbox setup, golden-hour backlight, high-contrast chiaroscuro, soft window light, neon rim light.
- **Camera / lens / focus:** GoPro action feel, disposable-camera flash, wide-angle lens, macro lens, low angle, aerial view, shallow depth of field.
- **Color grading / film stock:** muted teal grade, warm commercial grade, 1980s color film, grainy documentary look, high-saturation editorial.
- **Materiality / texture:** navy tweed, translucent plastic, ceramic glaze, brushed aluminum, etched metal, matte paper, glossy label, soft vinyl.

Use specific physical materials instead of generic adjectives. For example, "navy tweed blazer" is stronger than "nice jacket."

## Subject Consistency

For same-subject variants, pass the source image and explicitly ask for the new view or context.

```text
Create alternate views of the same <subject> from the source image.
Preserve exact <shape, face, label, colors, proportions, texture>.
Change only <angle, pose, setting, lighting, or panel action>.
```

Do not ask for same-subject variants with text only if a source image exists. Use the image as the reference.

## Multi-Image Stories

For short sequences, define the constant subject plus what changes frame by frame.

```text
Create a <N>-panel visual story using the same <subject>.
Panel 1: <visual beat>.
Panel 2: <visual beat>.
Panel 3: <visual beat>.
Preserve <identity/design/proportions/colors> across all panels.
```

If the live schema supports multiple outputs or structured references, use schema fields for that. If not, generate one panel at a time with the same source image and repeated preserve list.

## Retake Pattern

Use one correction at a time:

```text
Retake: preserve <protected details>. Correct only <single issue>.
Do not alter <identity/layout/background/lighting/text>.
```

## Common Failure Fixes

| Symptom | Fix |
|---|---|
| Output is generic | Add action, setting, composition, lighting, materiality, and production format |
| Reference ignored | Assign each reference a role and relationship to the output |
| Edit changes identity | Put preserve list immediately after the change request |
| Too much changed | Use "change only..." and reduce style pressure |
| Same subject drifts across views | Reuse the same source image and repeat exact preserved traits |
| Text is wrong | Quote exact text, specify font/hierarchy, shorten copy, and say "no extra words" |
| Localization changes layout | Preserve layout, hierarchy, spacing, and typography while translating only text |
| Aspect is ignored | Inspect schema and pass explicit aspect or width/height when available |
| Result feels over-stylized | Reduce style adjectives and ask for concrete materials, lighting, and texture |
