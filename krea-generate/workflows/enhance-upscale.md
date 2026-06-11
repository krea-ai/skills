# Enhance Upscale

## Trigger

User says "upscale", "make sharper", "4K", "increase resolution", "enhance but keep the same", "clean up", or asks for faithful improvement of an existing image. When in doubt between this workflow and `enhance-creative.md`, pick this if preserving the image is more important than inventing new detail.

## Clarify

Usually skip Clarify. Ask once only if the target size or preservation level is unclear.

- **Target size**: 2K, 4K, width/height, or platform.
- **Preservation**: faithful default, denoise, sharpen, face cleanup.
- **Use**: web, print, presentation, social.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the input image with vision.
2. Resolve `faithful upscale` archetype from live `list_models`.
3. Inspect schema for width, height, scale, denoise, sharpen, and face enhancement fields.
4. Cost-preflight if 4K/premium estimate exceeds 100 CU.
5. Upload local input to Krea.
6. Submit faithful enhance/upscale with target dimensions.
7. Download and read output with vision; compare for preservation and artifacts.
8. If artifacts appear, retry with lower creativity or fewer enhancement extras.
9. **Deliver** with dimensions and QA notes.

### CLI path

When using CLI, verify the surface with `../references/cli-or-mcp.md`, discover current command syntax from the installed CLI help, inspect the selected model schema, then submit using only live-supported fields. Treat command shapes from memory or old transcripts as stale.

### MCP path

When using MCP, use the available Krea tools to upload local inputs, list models, inspect the selected model schema, then call enhancement with schema-verified image and size fields.

## Banned

- Do not use creative enhance when the user asked to preserve exactly.
- Do not invent missing labels, faces, or product details.
- Do not ignore aspect ratio when setting target dimensions.
- Do not deliver without checking for hallucinated detail.

## Cost & time

- Per-job: low to medium for standard upscale; 1-3 minutes.
- Typical full workflow: 1 faithful upscale plus optional retry.
- Hard caps the user should know about: huge dimensions may be capped by model schema.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| New details invented | Creative model or high creativity | Switch to faithful archetype |
| Face looks waxy | Over-strong face enhancement | Disable or reduce face cleanup |
| Dimensions wrong | Schema/crop mismatch | Pass exact accepted width and height |
| User wants restyle | Wrong intent | Route to `enhance-creative.md` |
