---
version: 0.6.1
name: krea-generate
description: "Use before prompting Krea for any generation or transformation beyond the simplest one-shot request. Provides generic image, video, edit, enhancement, and reference-handling workflow guidance; route marketing, campaign, UGC, marketplace, and paid-social work to krea-marketing."
license: MIT
---

# Krea Generate - Media Generation

This skill is a workflow layer for generic Krea generation work. The host agent owns the voice, tool-call status, model shortlist, subagent behavior, progress display, and media presentation. Do not repeat or override those instructions here.

Use this skill for generation primitives and non-marketing creative workflows. It is not the marketing router and does not provide the animation production pipeline.

## Tool Discipline

Use the Krea tools supplied in the current turn. For generation models, the normal flow is `list_models` -> `get_model_schema` -> submit the job -> `wait_for_job` -> inspect the result -> `present_media`.

Do not invent tool names, model IDs, input fields, result URLs, job IDs, or local files. If a needed tool or capability is unavailable, say what is missing and stop or offer a simpler available path.

## Universal Rules

1. Use live model discovery and schema inspection before the first use of any model in a turn.
2. Read attached/source images before generating, and inspect generated stills/frames before approving, reusing, or presenting them. Use `references/vision-qa.md`.
3. For video, LoRA training, batches, 4K, premium models, or >100 CU, run `references/cost-preflight.md`.
4. Inspect references visually when understanding matters, then pass media through fields confirmed by `get_model_schema`. If a reference cannot be used directly by the selected model, use the available upload/asset tool and pass the resulting asset URL.
5. Follow the host agent's runtime rules for async job waiting and user-visible progress. Do not define separate status-update rules in this skill.
6. Do not pretend weak outputs are fine. Name the mismatch and offer a concrete retry path.

## Model Selection

Do not maintain a separate model catalog in this skill. Use the live `list_models` result, the selected model's schema, and the host agent's current model guidance. Workflow docs may name a narrow default when the task has special requirements, such as archviz preservation, enhancement, typography, or video.

If the user names a model, verify it live and use it only if the schema fits. If a preferred model is missing or cannot accept the required inputs, choose the nearest live alternative and say why.

## Image Workflow

Use this directly for generic image generation, image-to-image edits, restyles, references, options, and non-marketing final stills. Do not load another workflow for ordinary image work.

### Recognize Implicit Edit Requests

If the conversation already contains a generated or user-provided image, and the user follows up with an implicit edit request, you MUST use an edit model and you MUST feed the prior image into the edit model as a reference image.

Signals that the user wants you to edit a prior image:
1. the prompt contains phrases like 'make it', 'edit', 'change', 'remove', 'what if', etc.
2. the user makes reference to the content of the prior image

EXAMPLE OF AN IMPLICIT EDIT REQUEST
Original prompt: "generate a white motorcycle, studio shot on a film camera"
Follow-up prompt example 1: "make a few variations on the vantage point"
Follow-up prompt example 2: "what if the motorcycle was red"
Follow-up prompt example 3: "change the backdrop to a forest"
All examples are scenarios that MUST be considered an implicit edit request.

For implicit reference requests, you MUST:

1. Use an editing/reference-capable model such as `google/nano-banana-pro`, or `openai/gpt-image-2` when the request is complex, premium, or text-heavy.
2. Scan the conversation and track down the prior (or relevant) output and its associated prompt.
3. Feed the existing image output into the model as a conditional image input using the exact reference/source/image field from the live schema.

For implicit reference requests, you MUST NOT use prompt-only text-to-image generation such as Krea 2 Large/Medium. Prompt-only regeneration creates unrelated subjects and fails the task. If the prior image is not available as a Krea asset URL, local file, or uploadable source, stop and ask the user for the image instead of generating from text alone.

### Route

| Request | Mode |
|---|---|
| Loose concept, quick draft, exploration | Fast draft |
| Final, hero, production-quality, polished, detailed brief | High fidelity |
| User provides image(s), says edit/restyle/turn this into, or needs subject preservation | Image-to-image |
| User implicitly refers to an existing image: pronouns, definite subject, "different angles", "alternate views", "vantage points", "variations", "more like that" | Image-to-image using the prior output as a conditional reference input |
| Poster, flyer, signage, packaging copy, readable typography | Load `workflows/image-text-poster.md` |
| Upscale, sharpen, denoise, relight, enhance, 4K | Load `workflows/enhance.md` |
| Repeatable identity/style across many future outputs | Load `workflows/lora-train-and-use.md` |
| Product photo, campaign, ad, UGC, marketplace, paid social | Use `../krea-marketing/SKILL.md` |

### Clarify

Ask once, in a single batched message, only for details that block a useful result. Skip anything the user already gave.

- Goal: draft, final render, edit, restyle, or options.
- Subject and use: what the image is for.
- Aspect/resolution: 1:1, 4:5, 16:9, 9:16; 1K, 2K, or 4K.
- References/preservation: product, face, pose, layout, colors, text, or non-negotiables.
- Edit strength: subtle edit, balanced transformation, or full restyle.

If the brief is specific enough to act on, proceed without asking.

### Recipe

1. Read every attached/source/reference image with vision before model selection. Treat prior generated outputs in the conversation as source/reference images when the user asks for the same subject, alternate angles/views, variations, or preservation. This is mandatory even when the user does not explicitly say "use the previous image."
2. If local files or arbitrary external media URLs are used as model inputs, upload/rehost them to Krea first; pass already-Krea asset URLs and prior Krea generation URLs directly. Use schema-confirmed media fields only.
3. List live image models and apply the host model guidance plus any workflow-specific defaults.
4. Inspect the selected model schema. Confirm exact prompt, reference, aspect, size, quality, resolution, strength, mask, style, moodboard, and LoRA fields before submitting.
5. If live discovery resolves a `krea/krea-2/*` model, or the user asks for K2, Krea 2, moodboards, style references, or Krea 2 LoRAs, load `references/models/krea-2.md` before generation.
6. Write the prompt for the selected mode:
   - Fast draft: concrete subject, setting, camera/style, and aspect.
   - High fidelity: subject, composition, lighting, material, style, resolution, and deliverable constraints.
   - Image-to-image: describe the change first, then list what must stay the same.
   - Same-subject follow-up: use the prior image as a conditional image input, ask for the new angle/view/setting, and explicitly preserve the subject's identity, design, materials, proportions, layout, and distinctive details.
   - K2 moodboard/style-reference: keep the prompt about subject/composition/scene; let the moodboard or style refs carry taste, color, texture, and art direction.
7. Generate one candidate first. If the user asks for multiple same-subject options, pass the same prior image reference into every candidate. Keep the first batch cheap unless cost-preflight approved a premium batch.
8. Read outputs with vision. Compare against source images, references, and non-negotiables.
9. If the result clearly misses the subject or preservation target, retry once with a more literal prompt, stronger preservation language, lower edit strength, or a better live model.
10. Deliver the saved path or URL plus one concise QA note.

### Common Fixes

| Symptom | Fix |
|---|---|
| Generic output | Add concrete subject, setting, camera, composition, and style |
| Wrong aspect | Recheck schema and pass accepted aspect or explicit dimensions |
| Same subject changed across follow-ups | Use the prior generated image as a reference with Nano Banana Pro or GPT-image-2; preserve identity, materials, proportions, and distinctive details |
| Reference ignored | Switch to an image-to-image/reference-capable model and re-upload the source |
| Source changed too much | Lower edit strength and name preserved details explicitly |
| Product/face drifted | Reduce style pressure and use clearer preservation language |
| Good composition, low detail | Route the output through `workflows/enhance.md` |
| Garbled text | Route to `workflows/image-text-poster.md` |

## Routing

| Intent | Workflow |
|---|---|
| generic image generation, image edit, restyle, references, non-marketing final still | use Image Workflow above |
| poster / typography / text-heavy image | `workflows/image-text-poster.md` |
| generic short video / text-to-video / non-ad clip | `workflows/video-generic-short.md` |
| 3D screenshot -> photoreal render / archviz | `workflows/archviz-3d-to-render.md` |
| upscale / 4K / enhance / make sharper / creative enhance / relight / faithful restyle | `workflows/enhance.md` |
| train a LoRA / fine-tune on these images | `workflows/lora-train-and-use.md` |
| product photo / campaign / ad / UGC / key visual / marketplace card / paid social | use `../krea-marketing/SKILL.md` |

Never submit a video generation job without loading a workflow. For marketing video, route to `krea-marketing`; for non-marketing short video, use `workflows/video-generic-short.md`.

## References

Load only what the active workflow needs:

- `references/prompt-engineering.md` - prompt handling by modality.
- `references/vision-qa.md` - output inspection and retake discipline.
- `references/cost-preflight.md` - approval before expensive operations.
- `references/budget-tracking.md` - running CU tracker.
- `references/models/` - per-model prompting playbooks. Load only after resolving that model; for resolved Krea 2 or any moodboard work - discovery, preset-gallery search, or moodboard-driven generation - load `references/models/krea-2.md`.

## Related Skills

- `../krea-marketing/SKILL.md` - product photos, marketplace cards, campaigns, UGC/social ads, Meta Ads performance context, and paid-social activation.

## Filename Pattern

For local outputs, use `yyyy-mm-dd-hh-mm-ss-short-name.ext` with `.png` for images and `.mp4` for videos. Keep short names lowercase and hyphenated.
