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
2. Read product and optional people/location refs with vision.
3. Resolve a final still model from the marketing image set in `../SKILL.md`: default `openai/gpt-image-2`, offering live Nano Banana 2 / Nano Banana Pro as alternatives the user can pick; require multi-reference support if people or rooms are involved.
4. Inspect schema for `image_url`/`image_urls` or MCP equivalents, aspect, and resolution.
5. Cost-preflight for batches, 4K, or >100 CU.
6. Upload local or external/non-Krea refs to Krea.
7. Prompt product placement, environment, lighting, audience cue, and product preservation.
8. Generate 1-2 candidates in the primary platform aspect.
9. Vision-check that the product is recognizable and plausibly placed.
10. **Deliver** with platform labels and QA notes.

### CLI path

When using CLI, verify the surface with `../../krea-generate/references/cli-or-mcp.md`, discover current command syntax from the installed CLI help, inspect the selected model schema, then submit using only live-supported fields. Treat command shapes from memory or old transcripts as stale.

### MCP path

When using MCP, use the available Krea tools to upload product, model, and brand references, list models, inspect the selected model schema, then call image generation with schema-verified multi-reference, prompt, and aspect fields.

## Banned

- Do not let the product become a generic prop.
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
| User wants video ad | Scope changed | Route to `social-video-short.md` with product refs |
