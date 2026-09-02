---
name: nano-banana-examples
description: Searchable concrete prompt examples for Nano Banana, Nano Banana 2, Nano Banana Pro, and Gemini image models. Load only the section matching the active workflow.
---

# Nano Banana Examples

Use only after reading `nano-banana.md`. Search by heading and read the smallest matching section:

```bash
rg -n "^##|^###" nano-banana-examples.md
```

These examples are adapted from Google's Nano Banana prompting guide. They are prompt cards for reuse and modification, not API payloads. Always apply live Krea schema fields for aspect, size, resolution, references, masks, documents, and search/current-data options.

## Generate Examples

### Text-To-Image

Use when starting from a blank canvas with no references.

```text
Create a fashion editorial image of a model in a structured rust-brown coat,
black knee-high boots, and a geometric handbag.

The model stands with a confident statuesque pose, one shoulder turned
slightly toward camera, against a seamless deep burgundy studio backdrop.

Composition: medium-full shot, centered, full outfit visible.
Style: high-fashion magazine editorial, analog medium-format look, visible
film grain, saturated color, cinematic studio lighting.
```

Retake lever: if generic, add a clearer action, more specific clothing materials, and stronger camera language.

### Multimodal Reference

Use when references define structure, material, product identity, or style.

```text
Use Image 1 as the structural sketch for the chair silhouette and Image 2
as the upholstery texture reference.

Transform them into a high-fidelity 3D render of a lounge chair. Preserve
the sketch's proportions and armrest shape, and apply the fabric sample as
the visible seat and backrest material.

Place the chair in a sunlit minimalist living room with pale wood floors,
soft shadows, and quiet editorial styling.
```

Retake lever: if one reference dominates, restate exactly what to take from each image.

### Real-Time Information

Use only when the selected Krea schema/surface supports current-data or web/search behavior.

```text
Search for today's weather and local time in Seattle.

Use the result to decide the mood, sky, lighting, and ground conditions.
Visualize it as a miniature city-in-a-glass-terrarium concept inside a
clean modern smartphone weather app UI.

The UI should show concise current-weather information, while the miniature
scene inside the phone reflects the actual conditions.
```

Retake lever: if current-data is unavailable, provide the data manually and prompt the visual translation only.

### Text Rendering

Use for posters, product mockups, and precise typography.

```text
Create a high-end commercial beauty image of a minimalist cream-colored
moisturizer jar on a warm beige studio background with soft radiant lighting.

Render three text lines beside the product:
Top line: "GLOW" in an elegant flowing script font.
Middle line: "15% OFF" in a heavy bold sans-serif font.
Bottom line: "FIRST ORDER" in a thin minimalist geometric sans-serif font.

Keep text sharp, legible, and aligned. No other words.
```

Retake lever: if text fails, shorten the copy and keep only one or two lines.

### Localization

Use when the prompt or design is in one language but output text should be another.

```text
Create a premium skincare product poster. Write all visible text in Korean.

Text meaning:
Headline: "Glow starts here"
Offer line: "15% off your first order"

Use elegant skincare typography, clean spacing, warm cream background,
minimal product photography, and no other words.
```

Retake lever: if translation is awkward, supply exact translated text and ask it to render only that.

### Typographic Poster

Use for strong graphic type treatments.

```text
Create a typographic poster on a solid black background.

Large bold letters spell "TOKYO" across the center. The letterforms act as
windows: a night photo of Tokyo streets, signage, and reflections is visible
only inside the letters.

Everything outside the letters is pure black. No extra words, no border,
no watermark.
```

Retake lever: if the image appears outside the text, say the city photo must be clipped only inside the letters.

### Subject Consistency

Use for same-subject variants from a source image.

```text
Create three alternate views of the same ceramic table lamp from the source
image: front three-quarter view, side profile, and overhead detail.

Keep it recognizably the exact same lamp design in every view. Use consistent
warm studio lighting and a neutral background.
```

Retake lever: if a feature drifts, reuse the source image and name only that feature to correct.

### Multi-Image Story

Use for short visual sequences.

```text
Create a four-panel visual story using the same small yellow delivery robot.

Panel 1: the robot waits at a rainy apartment entrance holding a tiny package.
Panel 2: the door opens and warm light spills onto the robot.
Panel 3: the robot offers the package with a cheerful screen-face expression.
Panel 4: the robot rolls away under the rain, screen-face smiling.

Keep the exact same robot design across all panels.
```

Retake lever: if continuity fails, create a character/object anchor first and reuse it.

## Edit Examples

### Conversational Edit

Use for simple follow-up edits on an existing image.

```text
Remove the person standing near the left edge of the photo.

Reconstruct the background naturally where they were removed. Otherwise
preserve the source image exactly, including the composition.
```

Retake lever: if surrounding details change, name the altered detail and ask to restore it.

### Object Removal

Use for precise cleanup.

```text
Remove only the red construction cone from the sidewalk.

Fill in the sidewalk texture and shadow naturally. Otherwise preserve the
source image exactly, including the composition.
```

Retake lever: if it removes too much, add "only the cone, nothing else."

### Composition

Use when adding an object or combining subject and scene references.

```text
Use Image 1 as the base room photo and Image 2 as the lamp to add.

Place the lamp on the small table beside the sofa. Match its scale, contact
shadow, color temperature, and reflections so it looks naturally present.
Otherwise preserve Image 1 exactly, including the composition.
```

Retake lever: if pasted-looking, ask for stronger contact shadows and matching light direction.

### Style Transfer

Use when converting existing content into a new visual style.

```text
Transform the source city-street photo into an expressive post-impressionist
oil-painting style with thick brush texture, swirling sky movement, saturated
complementary colors, and visible paint strokes. Change only the visual
treatment; preserve the composition exactly.
```

Retake lever: if content changes, restate that style changes but composition stays fixed.

### Background Replacement

Use for environment swaps.

```text
Change the background to a bright sunlit kitchen.

Match the new background's light and depth of field to the foreground.
Otherwise preserve the source image exactly, including the composition.
```

Retake lever: if the foreground changes, retry from the source and name only the altered detail to restore.

### Product In New Environment

Use for product mockups or lifestyle staging.

```text
Place the product from the source image on a wet stone countertop in a
bright spa bathroom.

Add realistic contact shadows, subtle reflections, and soft morning light.
Preserve the product's exact label text; otherwise keep the product unchanged.
```

Retake lever: if label warps, reduce environment complexity and emphasize label preservation.

## Creative Director Examples

### Lighting

Use when the image needs a specific illumination setup.

```text
Create a premium product photo of a matte black ceramic coffee mug.

Lighting: three-point softbox setup with a large soft key light from front
left, gentle fill from right, and a narrow rim light separating the mug from
the charcoal background.

Composition: centered three-quarter view, subtle contact shadow, glossy
coffee surface visible, clean commercial photography.
```

Retake lever: if flat, add stronger rim light, darker background, and clearer shadow direction.

### Camera / Lens / Focus

Use when perspective and optical feel matter.

```text
Create an action-style image of a skateboarder launching off a concrete
ledge.

Camera: ultra-wide GoPro-like low-angle shot from near the ground, slight
fisheye distortion, dynamic foreground, city background stretched by the
wide lens.

Focus: sharp skateboarder, motion energy in limbs and wheels, dramatic
perspective, late-afternoon light.
```

Retake lever: if too static, specify low camera height and stronger foreground scale distortion.

### Color Grading

Use when mood depends on palette and film treatment.

```text
Create a cinematic portrait of a musician backstage before a show.

Color grade: muted teal shadows, warm amber practical lights, subtle film
grain, soft halation, restrained contrast.

Composition: medium close-up, mirror lights in background, shallow depth of
field, quiet tense mood.
```

Retake lever: if too colorful, ask for muted grade and lower saturation.

### Materiality

Use when products, costumes, or characters need physical specificity.

```text
Create a close-up fantasy character portrait.

The character wears ornate dark steel plate armor etched with fine silver
leaf patterns, layered over deep navy wool and cracked brown leather straps.
The cloak is heavy weathered velvet with rain-darkened edges.

Lighting: cool moonlit rim light with warm torch glow from below. Texture
should be tactile: scratched metal, damp fabric, worn leather, visible seams.
```

Retake lever: if generic, replace adjectives with specific materials and surface details.

## Retake Examples

### Text Correction

```text
Retake: correct only the middle text line to "15% OFF". Otherwise preserve
the poster exactly, including all other text.
```

### Reference Ignored

```text
Retake: use Image 1 only for the chair shape and proportions, and Image 2
only for the fabric texture. Keep both roles separate. Do not copy the room
or color palette from Image 2.
```

### Identity Drift

```text
Retake from the source: apply only the requested style change without
changing the person's identity. Otherwise preserve the source image exactly.
```

### Layout Clutter

```text
Retake: simplify the layout to one clear subject, one headline, and one
supporting visual element. Increase margins and white space. Remove extra
icons, labels, and decorative background details.
```

## Source

- `https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana`
