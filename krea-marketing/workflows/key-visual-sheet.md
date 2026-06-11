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

1. **Cost-preflight** (see `../../krea-generate/references/cost-preflight.md`). A key-visual sheet is cheap compared with video, but it is still an approval gate for campaign work.
2. Load `../references/marketing-creative-anatomy.md` if the user has not already locked the static format family.
3. Upload product and style/layout references to Krea. If a reference is an external URL, download it first and upload the downloaded file.
4. Resolve a `text-friendly image model` from the marketing image set in `../SKILL.md`; prefer `openai/gpt-image-2` only if live discovery confirms it and schema supports the needed refs, aspect, and quality. If it is unavailable, use live Nano Banana 2 if available, then Nano Banana Pro. Slow models like `openai/gpt-image-2` must be submitted asynchronously and polled through the available Krea surface; synchronous waits can hit gateway timeouts and lose the job id.
5. Generate one sheet first, or 2-3 variants if the brief is loose. Do not generate downstream finals or videos yet.
6. Prompt with mandatory sections:
   - **LAYOUT**: grid shape, gutters, headline placement, footer placement, and aspect.
   - **HEADLINE**: exact copy, lettering style, and brand color.
   - **PANELS**: concrete shot description per cell.
   - **BRAND GRAPHICS**: brushwork, shapes, stickers, crops, paper texture, or other brand devices.
   - **FOOTER**: exact caption treatment.
   - **FIDELITY**: preserve product identity, label details, packaging color, and factual claims.
7. Read the generated sheet with vision against the product and style refs. Reject if it is film pre-vis, vertically stacked action panels, or missing the product identity.
8. Offer variations by moving one lever at a time:
   - Same layout, different headlines.
   - Same headline, different grid shape.
   - Same content, different palette or graphic device.
9. On approval, use the sheet as the brief for `social-video-short.md`, `../../krea-generate/workflows/image-final-render.md`, or `product-photo-lifestyle.md`.

### CLI path

When using CLI, verify the surface with `../../krea-generate/references/cli-or-mcp.md`, discover current command syntax from the installed CLI help, inspect the selected model schema, then submit using only live-supported fields. Treat command shapes from memory or old transcripts as stale.

### MCP path

When using MCP, use the available Krea tools to upload product/layout references, list models, inspect the selected model schema, then call image generation with schema-verified prompt, reference, text, aspect, and quality fields.

## Banned

- Do not generate without a style/layout reference unless the user explicitly asks you to invent the format.
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
