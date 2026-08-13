# Product Photo Hero

## Trigger

User asks for a product hero shot, ecommerce hero, PDP lead image, white-background catalog shot, premium product render, or commercial product still. When in doubt between this workflow and `product-photo-lifestyle.md`, pick this if the product should be the unambiguous subject.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Product reference**: local file, external URL to download/upload, or existing Krea asset.
- **Use and aspect**: PDP, ad hero, web banner, marketplace, print.
- **Background**: white, gradient, plinth, fabric, marble, contextual.
- **Accuracy constraints**: label, color, shape, material, logo.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Load `../references/product-photoshoot.md` and classify the request; hero/catalog work maps to `studio_product` or `hero_banner`.
2. Read the product reference with vision; note only visible shape, label, material, colors, proportions, and hardware/trim. Use URL/PDP copy only for supported claims or copy, not visual truth.
3. Resolve a final still model from the marketing image set in `../SKILL.md`: default `openai/gpt-image-2`, offering live Nano Banana 2 / Nano Banana Pro as alternatives the user can pick; require image-to-image support from the live schema. If Nano Banana is chosen for a real product ref, keep the prompt scene-only because prompt words can override the reference.
4. Inspect schema for reference fields and resolution.
5. Run cost-preflight if generating a batch, 4K, or >100 CU.
6. Upload product refs to Krea if local or external/non-Krea.
7. Prompt as a hero product photograph: surface, lighting, lens, contact shadow/reflection, framing, copy, and accuracy constraints. When a real reference exists, do not include product material, color, label, trim, hardware, or garment descriptors in the generation prompt; keep those facts in the confirmation and QA checklist only.
8. Generate one hero candidate first. Offer variants only after the product reads correctly.
9. Read output with vision; verify product identity, proportions, label, and color. This inspection is blocking before variants, upscale, or delivery.
10. **Deliver** with a one-line summary and QA notes.

### MCP path

Use the available Krea MCP tools to upload product references, list models, inspect the selected model schema, then call image generation with schema-verified product reference, prompt, aspect, and quality fields.

## Banned

- Do not generate from text alone when the real product reference exists.
- Do not build faithful product prompts from PDP copy alone.
- Do not let prompt text fight the reference image; remove product material/color/garment words from real-product generation prompts.
- Do not prioritize aesthetics over product accuracy.
- Do not invent label text, claims, certifications, or ingredients.
- Do not batch variants before checking one accurate candidate.

## Cost & time

- Per-job: medium to high CU, 1-3 minutes.
- Typical full workflow: 1 validated hero plus 2-3 approved variants.
- Hard caps the user should know about: exact labels and fine typography may need a text-friendly workflow or manual finishing.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Product looks similar but wrong | Reference too weak or prompt too aesthetic | Use higher-res ref and stronger preservation |
| Label illegible | Image model weak at text | Route label-critical work to a text-strong model such as `openai/gpt-image-2` (see `../../krea-generate/references/models/gpt-image-2.md`) |
| Colors shifted | Lighting biased palette | Use a clearer reference, neutral lighting, and color-fidelity constraint without naming a conflicting color |
| Background dominates | Composition too busy | Return to clean hero prompt |
| Recolored logo | Product flattened into a tinted graphic instead of a photo subject | Retake with cleaner photo reference and photo-first prompt |
| Prompt-text override | Output follows prompt product words instead of the reference | Remove product descriptors; prompt only surface, light, camera, copy, and placement |
