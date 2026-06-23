# Model Catalog — Live Discovery

Krea's model lineup changes faster than this skill ships. This document intentionally avoids recommending specific model IDs. Use it to map an intent to the kind of capability to look for in live `list_models()` output.

## How To Use This File

1. List live models through Krea MCP.
2. Identify the user's intent.
3. Match that intent to an archetype below.
4. Read the live model `category`, `name`, and `description` for candidates that describe the needed capability.
5. Inspect the schema for each candidate through the same surface.
6. Choose the candidate whose live description and schema best match the request.

Do not choose from memory, local preferences, stale examples, or model IDs in old transcripts. The live catalog and live schema are the source of truth.

---

## Image Archetypes

### Fast Image Draft

**Intent.** The user is exploring, asking for quick concepts, or expects several iterations.

**Live catalog signals.** Look for descriptions that emphasize speed, low cost, drafts, exploration, quick iteration, or lightweight generation.

**Schema hints.** Confirm prompt, aspect or size controls, and optional seed/variation controls.

**Avoid when** the user says final, production, client-ready, delivery, or gives a detailed high-stakes brief.

---

### High-Fidelity Image

**Intent.** The user wants a polished final, hero asset, photoreal render, production image, or high-quality still.

**Live catalog signals.** Look for descriptions that emphasize photorealism, high fidelity, premium quality, production quality, flagship capability, or high resolution.

**Schema hints.** Confirm resolution, quality, aspect ratio or width/height, and reference-image support when references matter.

**Avoid when** the user is still brainstorming or explicitly asks for cheap drafts.

---

### Text In Image / Typography

**Intent.** The image must contain readable words, labels, signage, poster copy, UI text, or packaging text.

**Live catalog signals.** Look for descriptions that emphasize text rendering, typography, lettering, signage, copy fidelity, or design/layout strength.

**Schema hints.** Check whether the model has explicit text/copy fields or expects all text in the prompt. Use only fields present in the live schema.

**Avoid when** the image only contains incidental tiny text; a general high-fidelity model may be enough if live schema and examples suggest it.

---

### Stylized / Illustrated / Character

**Intent.** The user wants illustration, cartoon, anime, painterly style, expressive character design, or a non-photoreal look.

**Live catalog signals.** Look for descriptions that emphasize illustration, stylization, character work, expressive style, art direction, or style transfer.

**Schema hints.** Confirm style fields, reference support, and any style-strength controls.

**Model-specific references.** If live discovery resolves a `krea/krea-2/*` model, or the user asks for K2 moodboards/style references, load `models/krea-2.md` after selecting the model.

---

### Image-To-Image / Subject Reference

**Intent.** The user provides an existing image to edit, transform, restyle, or preserve as a subject/face/product reference.

**Live catalog signals.** Look for descriptions that mention image prompts, references, editing, subject preservation, face reference, style reference, or character reference.

**Schema hints.** Confirm the exact reference fields. Some models accept a single image URL; others accept arrays or structured reference objects.

**Model-specific references.** If live discovery resolves a `krea/krea-2/*` model with `moodboards` or `image_style_references`, load `models/krea-2.md` for moodboard and style-reference rules.

**Pattern.**

- One reference, simple edit: any live candidate with a matching image-reference field may work.
- Several references: require an array or structured multi-reference field.
- Strong identity preservation: prefer live candidates whose description explicitly says they preserve subjects, faces, or characters.

---

### Vector-Like Illustration

**Intent.** The user wants logo-like, icon-like, flat, geometric, or vector-ready artwork.

**Live catalog signals.** Look for descriptions that emphasize vector-like output, flat illustration, clean geometry, logos, icons, or editable-looking shapes.

---

## Video Archetypes

### Fast Video Draft

**Intent.** Quick motion tests, simple generated clips, rough exploration, or short ambient motion.

**Live catalog signals.** Look for descriptions that emphasize speed, draft quality, budget, lightweight video, or fast text-to-video.

**Schema hints.** Confirm duration, aspect ratio, resolution, prompt, and any reference/start-frame fields.

---

### Cinematic Video

**Intent.** Polished clip, coherent camera movement, production feel, multi-action motion, or identity-sensitive video.

**Live catalog signals.** Look for descriptions that emphasize cinematic quality, high fidelity, multi-shot or long motion handling, realistic motion, subject consistency, or production video.

**Schema hints.** Confirm accepted durations, resolution, aspect ratio, audio controls, start/end frame support, and reference media support.

**Avoid when** the user only needs a quick motion test.

---

### Image-To-Video / Start Frame Anchored

**Intent.** The user wants to animate a still image or preserve the first frame.

**Live catalog signals.** Look for descriptions that mention start frames, image-to-video, first-frame anchoring, transitions, or end frames.

**Schema hints.** Confirm the exact field names for start image, end image, and reference media. Upload local or external references to Krea before passing them to the model.

---

### Video With Audio

**Intent.** The final clip needs generated sound, ambient audio, music, speech, or lip sync.

**Live catalog signals.** Look for descriptions that mention audio, sound, voice, speech, music, or lip sync.

**Schema hints.** Confirm whether audio is generated by a boolean flag, a mode, or an audio-reference input.

---

## Image Enhancement Archetypes

### Faithful Upscale

**Intent.** Increase resolution, sharpen, denoise, or clean up an existing image while preserving content.

**Live catalog signals.** Look for descriptions that emphasize faithful upscale, preservation, sharpening, denoise, restoration, or non-generative enhancement.

**Schema hints.** Confirm target width/height or scale, denoise/sharpen controls, and whether face enhancement is optional.

---

### Creative Enhance

**Intent.** Improve an image while allowing the model to invent extra detail, lighting, texture, or polish.

**Live catalog signals.** Look for descriptions that emphasize creative enhancement, generative detail, relighting, refinement, or detail injection.

**Schema hints.** Confirm creativity/detail controls, prompt fields, face enhancement, and target size fields.

---

### Heavy Creative Detail Injection

**Intent.** A strong creative pass that may add texture, depth, embellishment, or visible design changes.

**Live catalog signals.** Look for descriptions that emphasize heavy creative detail, embellishment, generative refinement, or maximal enhancement.

---

## Picking Flow

Classify the request before choosing a model:

1. Quick image concept -> fast image draft.
2. Final still -> high-fidelity image.
3. Poster, banner, UI, packaging, or signage with readable copy -> text in image / typography.
4. Illustration, anime, cartoon, or painted look -> stylized / illustrated / character.
5. Edit or preserve a provided image -> image-to-image / subject reference.
6. Simple generated clip -> fast video draft.
7. Polished or identity-sensitive clip -> cinematic video.
8. Animate a still -> image-to-video / start frame anchored.
9. Add or generate sound -> video with audio.
10. Upscale without changing content -> faithful upscale.
11. Enhance with creative changes -> creative enhance.

Then resolve the archetype through live `list_models`, inspect schema, and submit.

## Boundaries

- Never hardcode a model ID based on memory.
- Do not use generic preference files to override live discovery.
- If the user names a specific model for this request, verify it exists in live `list_models`; use it only if the live schema supports the job.
- Domain-specific skills may add model preferences for their domain. For marketing image preferences, route to `../krea-marketing/SKILL.md`.
- Model name and description are hints, not guarantees. The live schema determines what inputs are valid.
