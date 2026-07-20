# Product Photo Lifestyle

## Trigger

User asks for lifestyle product shots, product in context, model wearing or using a product, UGC stills, desk/kitchen/bathroom/gym scenes, or social product imagery. When in doubt between this workflow and `product-photo-hero.md`, pick this if the environment or human use case matters as much as the product.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Product reference**: local file, external URL to download/upload, or existing Krea asset.
- **Context**: where the product appears and who uses it.
- **Platform/aspect**: TikTok cover, IG feed, Pinterest, PDP secondary.
- **Audience and mood**: premium, playful, wellness, technical, everyday.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Load `../references/product-photoshoot.md` and classify the request into lifestyle, closeup/person, Pinterest, carousel, ad pack, virtual try-on, conceptual product, or restyle.
2. Read product and optional people/location refs with vision. For apparel, confirm only visible silhouette, texture, colorway, trim, hardware, pattern, closures, logo/pin/embroidery, and proportion. Use URL/PDP copy only for supported claims or copy, not visual truth.
3. Resolve a final still model from the marketing image set in `../SKILL.md`: default `openai/gpt-image-2`, offering live Nano Banana 2 / Nano Banana Pro as alternatives the user can pick; require multi-reference support if people or rooms are involved. If Nano Banana is chosen for a real product ref, keep the prompt scene-only because prompt words can override the reference.
4. Inspect schema for image-reference fields, aspect, and resolution.
5. Cost-preflight for batches, 4K, or >100 CU.
6. Upload local or external/non-Krea refs to Krea.
7. Prompt environment, pose/use, lighting, audience cue, camera, composition, copy, product placement, and value-free fidelity to the reference. When a real reference exists, do not include product material, color, silhouette, trim, hardware, label, or garment descriptors in the generation prompt; keep those facts in the confirmation and QA checklist only.
8. Generate 1-2 candidates in the primary platform aspect.
9. Vision-check that the product is recognizable and plausibly placed. This inspection is blocking before variants, upscale, animation, or delivery.
10. **Deliver** with platform labels and QA notes.

### Tool path

Use the available Krea tools to upload product, model, and brand references when needed, list models, inspect the selected model schema, then call image generation with schema-verified multi-reference, prompt, and aspect fields.

## Banned

- Do not let the product become a generic prop.
- Do not build faithful product prompts from PDP copy alone.
- Do not let prompt text fight the reference image; remove product material/color/garment words from real-product generation prompts.
- Do not invent claims or use cases not supported by the user brief.
- Do not generate people wearing products without enough product detail for accuracy.
- Do not upscale or animate a lifestyle shot before vision QA.

## Cost & time

- Per-job: medium to high CU, 1-3 minutes.
- Typical full workflow: 2-6 lifestyle candidates, then optional final upscale.
- Hard caps the user should know about: complex human-product interaction can distort product geometry.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Product not visible | Context prompt overpowered subject | Specify product size, placement, and focal priority |
| Product changed | Weak reference anchoring | Use clearer product reference and preservation language |
| Human hand/use looks wrong | Interaction too complex | Simplify pose or generate product-only lifestyle |
| Recolored logo | Product flattened into a tinted graphic instead of a placed photo subject | Retake with cleaner photo reference and photo-first prompt |
| Prompt-text override | Output follows prompt product words instead of the reference | Remove product descriptors; prompt only scene, pose, light, camera, copy, and placement |
| User wants video ad | Scope changed | Route to `social-video-short.md` with product refs |
