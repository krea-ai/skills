# Image Edit I2I

## Trigger

User says "edit this image", "turn this into", "restyle", "change the background", "keep the person/product but make it", or provides an image as the primary input. When in doubt between this workflow and `image-final-render.md`, pick this if preservation of the source image matters more than inventing a new composition.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Change**: what should be different.
- **Preserve**: subject, face, product, pose, layout, colors, text, etc.
- **Strength**: subtle edit, balanced transformation, or full restyle.
- **Aspect**: keep original or change crop.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the source image with vision and state the edit target internally.
2. Resolve the `image-to-image / face reference` archetype from live `list_models`.
3. Inspect schema for `imageUrl` versus `imageUrls`, edit strength, mask, or preservation fields.
4. Upload local input to Krea; if CLI returns empty URL, resolve via the asset endpoint as described in `references/troubleshooting.md`.
5. Prompt the change, not a full re-description of the source: "change X to Y, preserve A/B/C".
6. Generate one edited candidate.
7. Read output with vision and compare against the source.
8. If preservation failed, retry once with stronger preservation language or a lower edit strength.
9. Deliver with a one-line summary and QA notes.

### CLI

```bash
ID=$(krea upload ./source.png --json | jq -r .id)
SRC=$(curl -sS -H "Authorization: Bearer $KREA_API_KEY" \
  "https://api.krea.ai/assets/$ID" | jq -r .image_url)
krea generate image -m "<image-to-image-model>" \
  -i imageUrl="$SRC" \
  -p "Change <edit> while preserving <must-keep details>" \
  --wait -o ./edited.png
```

### MCP fallback

```
upload_asset(filename, mimeType, fileData)
list_models()
get_model_schema(model="<image-to-image-model>")
generate_image(model="<image-to-image-model>", input={prompt, imageUrl}, sync=true, timeoutSeconds=90)
```

## Banned

- Do not describe everything already in the image as if generating from scratch.
- Do not ignore face/product preservation when the user says "this".
- Do not use external URLs for models known to require Krea-hosted assets; upload first.
- Do not call a video model for an edit request.

## Cost & time

- Per-job: usually medium CU, 1-2 minutes.
- Typical full workflow: 1-3 edit attempts.
- Hard caps the user should know about: masks, edit strength, and multi-reference support are model-specific.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Subject changed too much | Edit strength too high or prompt too broad | Lower strength and name preserved details |
| Model rejects URL | Non-Krea URL or bad MIME | Upload to Krea and use hosted asset URL |
| Background changed but subject warped | Model weak at preservation | Try a stronger image-to-image archetype |
| User wants only upscale | Wrong workflow | Route to `enhance-upscale.md` |
