---
name: gpt-image-2-prompting
description: Prompting playbook for GPT-Image-2 and ChatGPT Images 2.0 style models, focused on structured image generation, edits, exact text, layout, transparent backgrounds, preservation, and production workflows.
---

# GPT-Image-2 Prompting Guide

Load this file only after the selected model is `openai/gpt-image-2`, ChatGPT Images 2.0, or a closely related OpenAI image model. This is not a recommendation to choose GPT-Image-2.

## Prompting Stance

You are an expert GPT-Image-2 prompt engineer. For generation, convert the user's intent into a compact production brief with an explicit deliverable, scene, subject, layout, exact text, and reference roles. For edits, write a delta-focused instruction that emphasizes what changes rather than re-describing the source. Prefer clear instruction hierarchy over keyword piles.

Always verify the live Krea model schema before submitting. Use only fields exposed by the selected model. Prompt examples here describe intent; schema controls such as size, quality, references, transparency, and masks must come from the live schema.

This guide distills OpenAI's GPT Image Generation Models Prompting Guide into reusable prompt craft for `gpt-image-2`.

## Examples Appendix

For concrete prompt examples, search `gpt-image-2-examples.md` by heading and read only the matching section:

```bash
rg -n "^##|^###" gpt-image-2-examples.md
rg -n "Product Extraction|Virtual Try-On|Infographic" gpt-image-2-examples.md
```

Do not load the full examples appendix unless the relevant section cannot be identified.

## When To Load Examples

Load `gpt-image-2-examples.md` when the task is a first attempt in a concrete workflow, needs exact text/layout, edits or preserves a source image, or needs a retake after one failed output.

| Task | Search terms |
|---|---|
| infographic, explainer, process diagram | `Infographic|Scientific Diagram` |
| translation or localization | `Localization` |
| photorealistic scene or portrait | `Natural Photorealism` |
| logo or brand mark | `Logo` |
| ad, campaign, product social creative | `Ad|Marketing Creative` |
| comic, storyboard panel, sequential visual | `Comic Strip|Character Anchor|Character Continuation` |
| UI, app screen, product mockup | `UI Mockup` |
| slide, chart, deck, productivity artifact | `Slide / Chart` |
| merch, packaging, product concept | `Merch / Packaging` |
| clothing edit or try-on | `Virtual Try-On` |
| sketch, drawing, rough concept to render | `Sketch To Render` |
| product cutout or marketplace cleanup | `Product Extraction|Label Preservation` |
| subject compositing or background change | `Background Replacement|Lighting / Weather` |
| object/person removal | `Object Removal` |
| room, furniture, material, or object swap | `Interior Swap` |
| exact text correction | `Text Edit|Text Correction` |
| identity drift, clutter, label issues | `Identity Drift|Layout Clutter|Label Preservation` |

## Core Prompting Fundamentals

Write prompts as production briefs, not keyword bags. A reliable order is:

```text
Intended use / deliverable
Background or scene
Subject
Key visual details
Layout, camera, or artifact structure
Text, labels, or data if any
Constraints: what to avoid, preserve, or keep unchanged
```

For complex generation prompts, use short labeled blocks or line breaks. Minimal prompts, paragraphs, JSON-like prompts, tag-based prompts, and numbered instructions can all work; production templates should be skimmable.

Editing is different: the source image is already the brief for everything that is not changing. Start with the exact change, then include only change-specific execution details such as placement, material, lighting integration, perspective, or replacement text. Do not inventory unchanged people, objects, colors, lighting, framing, and other visible content. If needed, close with one compact global constraint such as `Otherwise preserve the rest of the image exactly, including the composition.` Mention a specific invariant in addition to that sentence only when it is central to the request, especially identity, exact text, a logo or product label, or something that drifted in a prior attempt.

## Specificity And Quality Cues

Be concrete about visible details:

- materials: brushed steel, worn cotton, translucent plastic, ceramic glaze
- shapes and proportions: strong silhouette, rounded corners, compact body
- textures: pores, wrinkles, film grain, paper fibers, brushstrokes
- medium: photorealistic photo, watercolor, vector-like logo, app UI, classroom handout

For photorealism, include `photorealistic` directly. Phrases like `real photograph`, `taken on a real camera`, `professional photography`, or `iPhone photo` can guide the general look, but exact camera specs are visual direction, not physical guarantees.

## Composition, People, And Action

Name framing, viewpoint, mood, and placement:

- framing: close-up, full body visible, medium close-up, wide establishing shot
- viewpoint: eye-level, top-down, low-angle, three-quarter view
- lighting: soft diffuse daylight, golden hour, high contrast, studio softbox
- placement: logo top-right, subject centered, negative space on left, footer at bottom

For wide, cinematic, low-light, rain, or neon scenes, add extra detail about scale, atmosphere, and color so the model does not trade mood for surface realism.

For people, describe body framing, scale, gaze, and object interactions:

```text
Full body visible, feet included. The child is small relative to the table,
looking down at the open book rather than at the camera. Hands naturally
grip the handlebars.
```

These details help with body proportion, action geometry, and gaze alignment.

## Quality And Size

Use live schema controls, not prompt prose, for quality and size. Prompt implications:

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
Composition: <shot size, viewpoint, placement>.
Style: <medium, visual language, lighting, color>.
Details: <materials, textures, props, atmosphere>.
Constraints: <no extra text/logos/watermarks, safe margins, preserve simplicity>.
```

### Image Edit

```text
Edit the source image: <specific change>.
<Details required to execute or integrate the change>.
Otherwise preserve the rest of the image exactly, including the composition.
```

Omit the last sentence when the requested edit changes the whole image or its composition. Do not expand it into a list unless a particular protected detail is essential or has already drifted.

### Multi-Image Edit Or Composite

```text
Image 1: <role, e.g. product photo>.
Image 2: <role, e.g. style reference or background>.

Task: <apply Image 2's style to Image 1 / place subject from Image 1 into Image 2>.
Use from Image 2: <palette, texture, environment, camera, lighting>.
Integration: <realistic contact shadows, consistent perspective, matching light>.
<If applicable, one global preservation sentence.>
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

Put literal text in quotes or ALL CAPS. For unusual spellings or brand names, spell the word out letter-by-letter in the prompt.

## Generate Prompt Rules

- **Infographics:** define audience, learning objective, required components, flow/order, labels, arrows, hierarchy, and white space.
- **Localization:** preserve every non-text element; translate only visible text; keep layout, hierarchy, and spacing.
- **Photorealism:** prompt as a real captured moment with natural light, real material texture, imperfections, and no over-retouching.
- **World-knowledge scenes:** provide place, date/era, realism target, and required visible accuracy constraints.
- **Logos:** ask for original, non-infringing, scalable, simple, vector-like marks with strong silhouette and negative space. One centered mark per image; get variations from multiple generations, not by prompting for a grid of directions.
- **Ads:** write a creative brief: brand, audience, culture, concept, composition, exact copy, and design constraints.
- **Comics:** one concrete visual beat per panel; lock character design and panel count.
- **UI mockups:** describe a usable shipped product with real sections, controls, hierarchy, spacing, and practical density.
- **Education/science:** specify audience, lesson objective, required labels, arrows/callouts, and scientific constraints.
- **Slides/charts:** provide canvas, title, real numbers, labels, axes, legends, footnotes, hierarchy, and spacing.
- **Merch/packaging:** describe original product concept, packaging, materials, label text, retail presentation, and IP constraints.

## Edit Prompt Rules

- **Style transfer:** name the style cues to transfer, not just "same style".
- **Virtual try-on:** replace only the clothing; describe the garment's drape, folds, occlusion, lighting, shadows, and color temperature. Mention identity as the one critical invariant.
- **Sketch to render:** add the requested realistic materials and lighting while keeping the sketch structure fixed; do not enumerate every structural element.
- **Product extraction:** for label integrity, prefer plain opaque background plus downstream background removal; request crisp edges and no halos.
- **Compositing:** assign each input a role and describe perspective, shadows, lighting, reflections, and color needed to integrate the change. Mention identity or label integrity only when critical.
- **Background replacement:** describe the new background and how it should integrate with the foreground, then use one global preservation sentence.
- **Lighting/weather changes:** describe the new environmental conditions and how they affect the scene, then use one global preservation sentence.
- **Object removal:** name the target and how to reconstruct the revealed area, then use one global preservation sentence.
- **Interior/object swaps:** use "replace only," describe the replacement and its integration, then use one global preservation sentence.
- **Surgical text edits:** give the old and new text and say to match the existing typography; avoid reciting every typographic attribute unless one needs to change or previously drifted.
- **Character consistency:** create a character anchor first; reuse it as image input and repeat appearance/proportion/outfit constraints.

## Transparent Backgrounds And Cutouts

For simple stickers/icons/cutouts, use the schema transparency field when available. For product extraction where label or silhouette integrity matters, prefer a plain opaque background first, then remove the background downstream.

Prompt wording:

```text
Create a clean cutout of <subject>.
Preserve exact silhouette and visible materials. Centered composition,
crisp edges, plain background, no text, no watermark.
```

## Common Failure Fixes

| Symptom | Fix |
|---|---|
| Extra text appears | Add "no extra text" / "no other words" and reduce decorative signage language |
| Text misspelled | Quote exact text, spell unusual words letter-by-letter, shorten copy, use higher quality |
| Layout is busy | Specify hierarchy, alignment, margins, and one focal point |
| Infographic is hard to scan | Add audience, objective, required labels, arrows, white space, and "avoid tiny text" |
| Photoreal image feels staged | Ask for candid real-photo language, imperfections, natural light, no glamorization |
| Person identity drifts | Retry from the source, name identity as the critical invariant, and correct only the requested change |
| Product extraction has halos | Ask for plain opaque background, crisp silhouette, no halos/fringing, light polish only |
| Product label warps | Preserve label text and proportions; use source image as reference; request realistic perspective |
| UI looks like concept art | Name real interface sections, controls, hierarchy, spacing, and "usable shipped interface" |
| Character changes across pages | Create a character anchor, reuse it as image input, repeat appearance/proportion/outfit constraints |
| Edit changes too much | Retry from the source with "change only..." plus one global preservation sentence; name only the detail that actually drifted |
| Wrong dimensions | Inspect schema; for GPT-image style models in Krea, explicit width/height may be required and may need multiples of 16 |
