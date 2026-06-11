# Portrait With Refs

## Trigger

User asks for a portrait, headshot, character image, avatar, or stylized likeness and provides one or more face references. When in doubt between this workflow and `image-edit-i2i.md`, pick this if the desired output is a new portrait rather than an edit of one source image.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Likeness target**: realistic, stylized, loose inspiration, or exact as possible.
- **Output style**: studio headshot, cinematic, editorial, avatar, illustration.
- **References**: best 2-3 face photos from varied angles.
- **Constraints**: age, hair, glasses, wardrobe, background.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read all face references with vision and pick the clearest frontal image as primary.
2. Set expectation: face-reference likeness is moderate; exact identity may require `lora-train-and-use.md`.
3. Resolve `image-to-image / face reference` or high-fidelity portrait model from live `list_models`.
4. Inspect schema for `image_urls` or MCP `imageUrls` array support; prefer multi-reference support.
5. Upload local references to Krea; duplicate the strongest ref in the array only when the model tolerates repeated URLs.
6. Prompt style, wardrobe, lighting, and background while explicitly preserving face identity.
7. Generate one portrait first.
8. Read output with vision; compare likeness, age, hair, and key features.
9. Deliver with QA notes or route to LoRA if identity is insufficient.

### CLI path

When using CLI, verify the surface with `../references/cli-or-mcp.md`, discover current command syntax from the installed CLI help, inspect the selected model schema, then submit using only live-supported fields. Treat command shapes from memory or old transcripts as stale.

### MCP path

When using MCP, use the available Krea tools to upload local face references, list models, inspect the selected model schema, then call image generation with schema-verified multi-reference, prompt, and aspect fields.

## Banned

- Do not promise exact likeness from face refs alone.
- Do not use a single blurry selfie if the user can provide better refs.
- Do not alter age, ethnicity, or distinctive facial features unless asked.
- Do not skip vision comparison before delivery.

## Cost & time

- Per-job: medium to high CU, 1-3 minutes.
- Typical full workflow: 1-4 attempts; LoRA training is a separate 15-45 minute workflow.
- Hard caps the user should know about: identity preservation depends on model and reference quality.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Likeness weak | Too few or poor refs | Add 2-3 clearer references or train LoRA |
| Face changed across variants | No identity anchor | Reuse same `image_urls`/MCP `imageUrls` and stronger preservation prompt |
| Style overwhelms identity | Prompt overweights aesthetic | Reduce style language and emphasize face |
| User needs brand-critical identity | Face refs insufficient | Route to `lora-train-and-use.md` |
