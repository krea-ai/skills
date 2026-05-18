# Social Video Short

## Trigger

User says "make a short video", "TikTok", "Reels", "Shorts", "GRWM", "UGC", "Ori-style video", "social ad", or asks for a vertical/square clip of 15 seconds or less. When in doubt between this workflow and `narrative-video-long.md`, pick this if the target is one continuous social-native piece rather than many hard cuts.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Aspect**: 9:16 TikTok/Reels/Shorts, 1:1 feed, or 16:9.
- **Duration**: 5, 10, or 15 seconds.
- **Concept and beats**: one-line concept plus 4-6 actions that must happen.
- **Identity refs**: face, product, brand, outfit, mascot, or none.
- **Style**: palette, setting, mood, reference videos, text overlays.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. **Cost-preflight** (mandatory before video - see `../references/cost-preflight.md`). Default estimate for 15s Seedance-2 720p is ~1564 CU and 10-15 minutes. Show estimate, get yes.
2. Resolve a `text-friendly image model` for storyboard generation and a `cinematic video` model for animation from live `list_models`; defaults can be `openai/gpt-image-2` and `bytedance/seedance-2` only if live discovery confirms them.
3. Build one editorial storyboard sheet, not separate panels. Use 4-8 cells for 5-10s; 16-32 cells for dense 15s micro-beats. Use tiny panel numbers and short action labels; no technical fiches.
4. Generate 1 storyboard sheet, or 2-3 variations if the brief is loose. Include face/product refs in the image call when identity matters.
5. Show the storyboard(s) and wait for approval. Iterate cheaply here before burning video credits.
6. Upload the chosen storyboard to Krea. If `krea upload --json` returns an empty URL (issue #6), resolve `image_url` via `GET https://api.krea.ai/assets/<id>`.
7. Avoid the seedance aspect trap (issue #11): do not pass `--start-image` for vertical output. If the storyboard sheet is landscape and final output must be 9:16, pad the sheet to portrait before upload or drop the sheet from `referenceImages` and rely on face refs plus a detailed timeline prompt.
8. Compose a timestamped timeline prompt. Use `TIMELINE`, `STYLE`, `CAMERA`, `TRANSITIONS`, and `OUTPUT` sections. Strip the words `slow`, `gentle`, `soft`, and `slow motion`; use `smooth`, `steady`, `fluid`, or `natural realtime` instead.
9. Submit one video job async. Use `referenceImages` for storyboard/refs, not per-panel concatenation.
10. Poll with `../references/progress-reporting.md`: ping on status changes and every 25-35 seconds while unchanged.
11. Download, normalize to the requested delivery frame with ffmpeg, sample 4-6 frames, and vision-check continuity/identity before delivering.
12. **Deliver** with a one-line summary and QA notes.

### CLI

```bash
krea generate image -m "<text-friendly-image-model>" \
  --aspect 16:9 \
  -i quality=high \
  -i imageUrls='["<face-or-product-ref-url>"]' \
  -p "<editorial storyboard sheet prompt>" \
  --wait -o ./storyboard.png

ID=$(krea upload ./storyboard.png --json | jq -r .id)
SHEET=$(curl -sS -H "Authorization: Bearer $KREA_API_KEY" \
  "https://api.krea.ai/assets/$ID" | jq -r .image_url)

krea generate video -m "<cinematic-video-model>" \
  --aspect 9:16 \
  --duration 15 \
  -i resolution=720p \
  -i referenceImages="[\"$SHEET\"]" \
  -p "<timestamped timeline prompt>" \
  --json
```

### MCP fallback

```
list_models()
get_model_schema(model="<text-friendly-image-model>")
generate_image(model="<text-friendly-image-model>", input={prompt, imageUrls, aspectRatio, quality}, sync=true)
upload_asset(filename="storyboard.png", mimeType="image/png", fileData=<base64>)
get_model_schema(model="<cinematic-video-model>")
generate_video(model="<cinematic-video-model>", input={prompt, referenceImages, aspectRatio, duration, resolution}, sync=false)
get_job(jobId=<id>)  # poll with progress pings
```

## Banned

- Do not submit video before storyboard approval - this is the #11 fix and the 2026-05-17 lesson.
- Do not generate panels separately and ffmpeg-concatenate - it creates stitched snippets, not a coherent social video.
- Do not pass landscape `--start-image` into Seedance for vertical output - issue #11.
- Do not put a landscape storyboard first in `referenceImages` for 9:16 unless padded to portrait - issue #11.
- Do not use `slow`, `gentle`, `soft`, or `slow motion` in prompts - Seedance often literalizes them.
- Do not rely on `krea jobs wait --timeout 600` if the CLI caps at 300s - issue #9; use manual polling.
- Do not use non-Krea-hosted refs for models that reject them - issue #7.
- Do not silently poll - issue #17; progress pings are mandatory.

## Cost & time

- Per-job: storyboard is cheap; Seedance-style 15s 720p video is ~1564 CU and 8-15 minutes.
- Typical full workflow: 1-3 storyboards plus 1 approved video job; ~10-20 minutes.
- Hard caps the user should know about: 15 seconds max for this workflow; face-reference likeness is moderate; storyboard aspect can bias video aspect.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Output horizontal despite `--aspect 9:16` | Landscape `--start-image` or `referenceImages[0]` bias, issue #11 | Drop start image; pad sheet to portrait; or use face refs plus timeline only |
| Output is slow motion | Prompt contained banned pacing words, issue #14 | Rewrite with natural realtime, smooth, steady, fluid |
| Video feels stitched | Per-panel generation was used, issue #15 | Use one storyboard sheet and one timeline-driven video job |
| Upload URL empty | CLI upload issue #6 | Resolve asset by ID through the assets endpoint |
| Job times out | CLI timeout cap issue #9 | Manual `krea jobs show` loop |
| External URL rejected | Kontext/Seedream URL issue #7 | Upload local assets to Krea first |
| Identity drifts | Face refs weak, issue #16 | Use 2-3 varied refs or route to `lora-train-and-use.md` |
| User lost trust during wait | Silent polling, issue #17 | Follow `../references/progress-reporting.md` every 25-35 seconds |
