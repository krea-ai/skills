# Enhance

## Trigger

User asks to upscale, make sharper, increase resolution, clean up, denoise, enhance, relight, add detail, make more cinematic/premium, or restyle while improving an existing image.

## Route

| Request | Mode |
|---|---|
| "Upscale", "4K", "make sharper", "clean up", "enhance but keep the same" | Precise upscale |
| "Creative enhance", "make cinematic", "relight", "add detail", "make premium", "restyle" | Creative enhance |

When in doubt, choose precise upscale if preservation matters more than invention. Choose creative enhance only when the user welcomes stylistic change or added detail.

## Model Priority

Always resolve these through live `list_models` and inspect the selected schema before use. Match by live id/name/description; do not assume exact IDs.

| Mode | Priority | Notes |
|---|---|---|
| Creative enhance | Topaz Bloom, `/topaz/bloom-enhance` | Default for creative detail injection, relight, polish, or premium-looking restyles. |
| Faithful / realistic enhance | Topaz Standard, `/topaz/standard-enhance` | Default for normal faithful enhancement, upscaling, sharpening, denoise, cleanup, and photography. |

If none of the named models are available or their schema cannot support the request, fall back to the closest live model by archetype and explain the substitution briefly.

## Clarify

Ask once only if target size, preservation level, or creative direction is unclear.

- **Mode**: precise upscale or creative enhance.
- **Target size**: same size, 2K, 4K, width/height, or platform.
- **Preserve**: subject, face, product, composition, text, colors.
- **Creative direction**: cinematic, editorial, luxury, painterly, gritty, bright, etc.
- **Strength**: subtle, balanced, or bold.

If the user gave a tight, complete brief, skip Clarify and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the input image with vision.
2. Pick the mode and model from Model Priority:
   - Precise upscale / faithful realistic: use Topaz Standard, `/topaz/standard-enhance`.
   - Creative enhance: use Topaz Bloom, `/topaz/bloom-enhance`.
3. Inspect the selected model schema for image, width, height, scale, denoise, sharpen, face enhancement, creativity, strength, and prompt fields.
4. Run `../references/cost-preflight.md` if the target is 4K, premium, or >100 CU.
5. Upload local or external input images to Krea first.
6. Submit one pass:
   - Precise upscale: use target dimensions and conservative denoise/sharpen/face cleanup fields if available.
   - Creative enhance: prompt the desired improvement, list preserved elements, and start with balanced creativity.
7. Download and read the output with vision. Compare preservation, artifacts, dimensions, and detail quality against the input.
8. If artifacts or drift appear, retry once:
   - Precise upscale: lower enhancement extras, disable/reduce face cleanup, or switch to a more faithful archetype.
   - Creative enhance: lower creativity and strengthen the preserve list.
9. Deliver with dimensions and one concise QA note. Mention meaningful drift instead of hiding it.

### MCP path

Use available Krea MCP tools to upload inputs, list models, inspect schemas, run enhancement/upscale jobs, and poll results. Do not skip live verification of model names or input fields.

## Banned

- Do not use creative enhance when the user asked to preserve exactly.
- Do not invent missing labels, faces, or product details.
- Do not ignore aspect ratio when setting target dimensions.
- Do not crank creativity to max on the first pass.
- Do not deliver without checking for hallucinated detail, waxy faces, text degradation, or warped products.

## Cost & time

- Precise upscale: low to medium CU, usually 1-3 minutes.
- Creative enhance: medium CU, usually 1-4 minutes.
- Typical workflow: 1 pass plus optional retry.
- Hard caps the user should know about: maximum dimensions and creative controls vary by model schema.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| New details invented | Creative model or high creativity | Switch to precise upscale or lower creativity |
| Too much changed | Creative settings too strong | Lower creativity and strengthen preserve list |
| Not improved enough | Conservative settings | Increase creativity or sharpen/denoise one step |
| Face looks waxy | Over-strong face enhancement | Disable or reduce face cleanup |
| Dimensions wrong | Schema/crop mismatch | Pass exact accepted width and height |
| Text degraded | Enhance model weak at text | Preserve original text or route to text workflow |
