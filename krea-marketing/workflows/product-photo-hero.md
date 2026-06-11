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
2. Read the product reference with vision; note shape, label, material, and colors.
3. Resolve a final still model from the marketing image set in `../SKILL.md`: default `openai/gpt-image-2`, offering live Nano Banana 2 / Nano Banana Pro as alternatives the user can pick; require image-to-image support from the live schema.
4. Inspect schema for reference fields and resolution.
5. Run cost-preflight if generating a batch, 4K, or >100 CU.
6. Upload product refs to Krea if local or external/non-Krea.
7. Prompt as a hero product photograph: product, surface, lighting, lens, contact shadow/reflection, accuracy constraints.
8. Generate one hero candidate first. Offer variants only after the product reads correctly.
9. Read output with vision; verify product identity, proportions, label, and color.
10. **Deliver** with a one-line summary and QA notes.

### CLI path

When using CLI, verify the surface with `../../krea-generate/references/cli-or-mcp.md`, discover current command syntax from the installed CLI help, inspect the selected model schema, then submit using only live-supported fields. Treat command shapes from memory or old transcripts as stale.

### MCP path

When using MCP, use the available Krea tools to upload product references, list models, inspect the selected model schema, then call image generation with schema-verified product reference, prompt, aspect, and quality fields.

## Banned

- Do not generate from text alone when the real product reference exists.
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
| Label illegible | Image model weak at text | Route label-critical work to `../../krea-generate/workflows/image-text-poster.md` |
| Colors shifted | Lighting biased palette | Add exact color preservation or hex values |
| Background dominates | Composition too busy | Return to clean hero prompt |
