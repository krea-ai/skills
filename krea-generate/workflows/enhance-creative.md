# Enhance Creative

## Trigger

User says "make this more cinematic", "re-light", "add detail", "creative enhance", "restyle while improving", "make it premium", or wants the image improved with some invention. When in doubt between this workflow and `enhance-upscale.md`, pick this if creative change is welcome.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Creative direction**: cinematic, editorial, luxury, painterly, gritty, bright, etc.
- **Preserve**: subject, face, product, composition, text.
- **Strength**: subtle, balanced, bold.
- **Target size**: same size, 2K, 4K.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the source image with vision.
2. Resolve `creative enhance` or `bloom / creative detail injection` from live `list_models`.
3. Inspect schema for creativity, face enhancement, width/height, and prompt fields.
4. Cost-preflight for >100 CU or large output.
5. Upload local image to Krea.
6. Prompt the desired enhancement and list preserved elements.
7. Generate one balanced creative pass first.
8. Read output with vision and compare against preservation list.
9. **Deliver** with QA notes and mention if anything drifted.

### CLI

```bash
IMG=$(krea upload ./input.png --json | jq -r .url)
krea generate enhance -m "<creative-enhance-model>" "$IMG" \
  --width 2048 --height 2048 \
  -i creativity=3 \
  -p "<creative direction while preserving subject/composition>" \
  --wait -o ./creative-enhance.png
```

### MCP fallback

```
upload_asset(...)
list_models()
get_model_schema(model="<creative-enhance-model>")
enhance_image(model="<creative-enhance-model>", input={imageUrl, width, height, creativity, prompt}, sync=true)
```

## Banned

- Do not use this for faithful archival upscale.
- Do not change product or face identity unless the user permits it.
- Do not crank creativity to max on the first pass.
- Do not hide drift; call it out in QA.

## Cost & time

- Per-job: medium CU, 1-4 minutes.
- Typical full workflow: 1 balanced pass plus 1 strength adjustment.
- Hard caps the user should know about: creative models may change details by design.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Too much changed | Creativity too high | Lower creativity and strengthen preserve list |
| Not improved enough | Conservative settings | Increase creativity one step |
| Product/face drift | Creative pass overrode identity | Switch to faithful upscale or image edit workflow |
| Text degraded | Enhance model weak at text | Keep original or route to text workflow |
