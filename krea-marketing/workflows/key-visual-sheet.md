# Key-Visual Sheet

## Trigger

User says "ad storyboard", "key visual", "campaign sheet", "social pack", "ad layout", "moodboard for an ad", or shares an agency-style campaign reference. Default here when CPG, FMCG, beverage, beauty, fashion, or agency context suggests the first approval artifact should be a finished campaign layout rather than film pre-vis.

## Clarify

Ask once, in a single batched message. References are mandatory unless the user has already supplied a strong visual format reference.

- **Brand voice**: one sentence from product, packaging, existing brand assets, and brief.
- **Headline copy**: hero line plus optional tagline.
- **Static format family**: headline-led, offer-led, social-proof-led, feature/benefit-led, comparison-led, editorial-led, utility-led, or organic-post-led.
- **Grid shape**: 2x3 typical, 3x3 dense, or 1x5 strip.
- **Aspect**: 9:16 social, 1:1 feed, 4:5 IG, 16:9 presentation.
- **Palette / graphics**: pull from packaging when unspecified.
- **Footer caption**: e.g. `15s / 9:16 / Brand Flavor`.
- **References**: product reference plus layout/style reference.

## Recipe

Hard prescription. Follow in order.

1. Load `../references/marketing-creative-anatomy.md` if the user has not already locked the static format family.
2. Read product references with vision before prompt writing. If a reference is an external URL/PDP, download usable product images first and use page text only for supported claims/copy.
3. Upload product and style/layout references to Krea. If a reference is an external URL, download it first and upload the downloaded file.
4. Resolve a `text-friendly image model` from the marketing image set in `../SKILL.md`; prefer `openai/gpt-image-2` only if live discovery confirms it and schema supports the needed refs, aspect, and quality. If it is unavailable, use live Nano Banana 2 if available, then Nano Banana Pro. Slow models like `openai/gpt-image-2` must be submitted as jobs and waited on with the available job tool.
5. Generate one sheet first, or 2-3 variants if the brief is loose. Do not generate downstream finals or videos yet.
6. Prompt with mandatory sections:
   - **LAYOUT**: grid shape, gutters, headline placement, footer placement, and aspect.
   - **HEADLINE**: exact copy, lettering style, and brand color.
   - **PANELS**: concrete shot description per cell.
   - **BRAND GRAPHICS**: brushwork, shapes, stickers, crops, paper texture, or other brand devices.
   - **FOOTER**: exact caption treatment.
   - **FIDELITY**: preserve product identity from the reference and factual claims. Do not include product material, color, silhouette, trim, hardware, label, or garment descriptors in the generation prompt; keep those facts in the confirmation and QA checklist only.
7. **Blocking sheet QA gate**: read the generated sheet with vision against the product and style refs. Reject if it is film pre-vis, vertically stacked action panels, missing product identity, Recolored logo, Prompt-text override, or unsupported claims. Do not use the sheet as a downstream brief until it passes.
8. Offer variations by moving one lever at a time:
   - Same layout, different headlines.
   - Same headline, different grid shape.
   - Same content, different palette or graphic device.
9. On approval, use the sheet as the brief for `social-video-short.md`, generic image generation via the model-selection guidance in `../../krea-generate/SKILL.md`, or `product-photo-lifestyle.md`.

### Tool path

Use the available Krea tools to upload product/layout references when needed, list models, inspect the selected model schema, then call image generation with schema-verified prompt, reference, text, aspect, and quality fields.

## Banned

- Do not generate without a style/layout reference unless the user explicitly asks you to invent the format.
- Do not build product facts from PDP copy alone or let prompt text fight the reference image.
- Do not produce film pre-vis with stacked temporal panels and action labels.
- Do not call this a storyboard without naming that it is a campaign key-visual sheet.
- Do not proceed to video generation before the user approves the sheet.

## Cost & time

- Per-job: usually one high-quality image generation; commonly around the same cost as a premium still image.
- Typical workflow: 1-3 sheets before approval; far cheaper than generating video directions blindly.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| User says "this is not a storyboard" | Wrong artifact taxonomy | Re-open `../references/artifact-taxonomy.md`, ask for/inspect a visual reference, and reroute |
| Looks like generic product collage | Missing brand voice or graphic devices | Rebuild prompt around packaging palette, copy voice, and one distinctive format lever |
| Product wrong or label distorted | Weak product reference or no fidelity pass | Use clearer product refs, increase fidelity wording, or route to product-photo workflow for per-cell finals |
| Recolored logo | Product photo became a tinted graphic element | Reject and retake with photo-first prompt and cleaner product ref |
| Prompt-text override | Sheet follows prompt product words instead of the reference | Remove product descriptors; keep layout, scene, copy, and placement |
