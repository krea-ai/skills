# Product Photo Hero

## Trigger

User asks for a product hero shot, ecommerce hero, PDP lead image, white-background catalog shot, premium product render, or commercial product still. When in doubt between this workflow and `product-photo-lifestyle.md`, pick this if the product should be the unambiguous subject.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Product reference**: upload, URL, or existing asset.
- **Use and aspect**: PDP, ad hero, web banner, marketplace, print.
- **Background**: white, gradient, plinth, fabric, marble, contextual.
- **Accuracy constraints**: label, color, shape, material, logo.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the product reference with vision; note shape, label, material, and colors.
2. Resolve `high-fidelity image` with image-to-image support from live `list_models`.
3. Inspect schema for reference fields and resolution.
4. Run cost-preflight if generating a batch, 4K, or >100 CU.
5. Upload product refs to Krea if local.
6. Prompt as a hero product photograph: product, surface, lighting, lens, contact shadow/reflection, accuracy constraints.
7. Generate one hero candidate first. Offer variants only after the product reads correctly.
8. Read output with vision; verify product identity, proportions, label, and color.
9. **Deliver** with a one-line summary and QA notes.

### CLI

```bash
PRODUCT=$(krea upload ./product.png --json | jq -r .url)
krea generate image -m "<high-fidelity-image-to-image>" \
  --aspect 16:9 \
  -i imageUrl="$PRODUCT" \
  -i quality=high \
  -p "Photoreal hero product shot of the referenced product, preserving exact shape, label, color, and material; <background, lighting, camera>" \
  --wait -o ./product-hero.png
```

### MCP fallback

```
upload_asset(...)
list_models()
get_model_schema(model="<high-fidelity-image-to-image>")
generate_image(model="<high-fidelity-image-to-image>", input={prompt, imageUrl, aspectRatio, quality}, sync=true)
```

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
| Label illegible | Image model weak at text | Route label-critical work to `image-text-poster.md` |
| Colors shifted | Lighting biased palette | Add exact color preservation or hex values |
| Background dominates | Composition too busy | Return to clean hero prompt |
