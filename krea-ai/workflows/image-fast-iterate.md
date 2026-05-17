# Image Fast Iterate

## Trigger

User says "make me an image", "generate a quick image", "try a concept", "show me options", or gives a loose visual idea with no production-quality bar. When in doubt between this workflow and `image-final-render.md`, pick this if the user is still exploring.

## Clarify

Usually skip Clarify. Ask once only if the brief is missing the subject or has an impossible constraint.

- **Subject**: what should be in the image.
- **Aspect**: 1:1, 9:16, 16:9, or "whatever fits".
- **Style**: photoreal, illustration, product, cinematic, etc.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read any attached image with vision before routing.
2. Load `references/model-catalog.md` and resolve the `fast image draft` archetype from live `list_models`.
3. Call `get_model_schema` or `krea models show` for the chosen model; confirm accepted aspect and prompt fields.
4. Submit one draft first. Do not ask cost-preflight unless the estimated total is >100 CU.
5. If the user asked for options, generate 2-4 cheap variations, not a premium batch.
6. Download outputs locally and read them with vision.
7. If the draft clearly misses the subject, retry once with a more literal prompt.
8. Deliver with a one-line summary and saved path or URL.

### CLI

```bash
krea models list --json
krea models show "<fast-image-draft>" --json
krea generate image -m "<fast-image-draft>" \
  --aspect 1:1 \
  -p "<user brief, lightly tightened only if needed>" \
  --wait -o ./draft.png
```

### MCP fallback

```
list_models()
get_model_schema(model="<fast-image-draft>")
generate_image(model="<fast-image-draft>", input={prompt, aspectRatio}, sync=true, timeoutSeconds=60)
```

## Banned

- Do not start with a premium render for a loose idea; use the cheap draft path first.
- Do not ask a long questionnaire for a cheap image; ambiguity is resolved by generating.
- Do not hardcode model IDs; resolve archetypes live.
- Do not deliver without vision-checking the generated image.

## Cost & time

- Per-job: usually low CU, about 20-90 seconds.
- Typical full workflow: 1-4 drafts, usually under 100 CU unless the live catalog says otherwise.
- Hard caps the user should know about: model-specific aspect and resolution limits from schema.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Generic output | Prompt too loose | Add concrete subject, setting, camera, and style |
| Wrong aspect | Aspect field omitted or unsupported | Check schema and pass an accepted aspect |
| Text is garbled | Wrong archetype | Route to `image-text-poster.md` |
| User wants final polish | Intent changed | Route to `image-final-render.md` |
