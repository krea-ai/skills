# Image Final Render

## Trigger

User says "final", "production quality", "hero asset", "for delivery", "client-ready", "high quality", or gives a detailed brief with references. When in doubt between this workflow and `image-fast-iterate.md`, pick this if a wrong output would waste user review time.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Use**: web hero, print, ad, presentation, product page, social.
- **Aspect and resolution**: 16:9, 4:5, 1:1, 9:16; 1K, 2K, or 4K.
- **References**: product, face, style, brand, or previous draft.
- **Non-negotiables**: details that must be preserved.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read all attached/generated references with vision.
2. If the run is >100 CU or 4K premium, run cost-preflight via `../references/cost-preflight.md`.
3. Resolve a `high-fidelity image` or `image-to-image / face reference` archetype from live `list_models`.
4. Inspect schema for exact fields: `imageUrl`, `imageUrls`, `aspectRatio`, `resolution`, `quality`, `styleId`.
5. Upload local references to Krea first; use Krea-hosted URLs for generation.
6. Write one prompt that states subject, composition, lighting, material, style, and preservation constraints.
7. Generate 1 final candidate first; only batch variants after the first passes vision QA.
8. Download and read the output with vision; verify against non-negotiables.
9. Deliver with one-line summary and any QA notes.

### CLI

```bash
REF=$(krea upload ./reference.png --json | jq -r '.url // empty')
krea models list --json
krea models show "<high-fidelity-image>" --json
krea generate image -m "<high-fidelity-image>" \
  --aspect 16:9 \
  -i quality=high \
  -i imageUrls="[\"$REF\"]" \
  -p "<final render prompt>" \
  --wait -o ./final-render.png
```

### MCP fallback

```
upload_asset(filename, mimeType, fileData)
list_models()
get_model_schema(model="<high-fidelity-image>")
generate_image(model="<high-fidelity-image>", input={prompt, imageUrls, aspectRatio, quality}, sync=true, timeoutSeconds=120)
```

## Banned

- Do not skip reference vision reading; final work depends on real visual details.
- Do not produce a large batch before one candidate proves the model is following the brief.
- Do not upscale a bad image just because it is high resolution.
- Do not invent product claims, labels, logos, or legally sensitive details.

## Cost & time

- Per-job: medium to high CU depending on live model and resolution; 1-3 minutes typical.
- Typical full workflow: 1 premium candidate plus 1-3 refinements.
- Hard caps the user should know about: 4K and multi-reference support vary by model schema.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Reference ignored | Wrong model or weak input | Switch to image-to-image archetype and re-upload reference |
| Product shape drifted | Prompt overemphasized style | Add preservation language and use clearer product ref |
| Low detail | Draft model selected | Re-resolve to high-fidelity archetype |
| Good composition but low resolution | Need enhance step | Route output through `enhance-upscale.md` |
