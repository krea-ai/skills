# Storyboard-sheet method (short social-format videos)

For 5–15s vertical or square videos — social shorts, GRWM, ad creative, "day in the life", explainers — the cleanest path is **one editorial storyboard sheet + one timeline-driven video job**. NOT per-scene frame generation concatenated together.

This is the canonical Krea Agent pattern and the one users mean when they ask for "an Ori-style video" or "a GRWM storyboard".

## When to use this vs `video-production.md`

| Use storyboard-sheet method (this doc)         | Use multi-scene production (`video-production.md`) |
|---|---|
| Output ≤ 15s, single continuous video          | Output > 15s, multiple distinct cuts |
| Editorial / social / GRWM / ad / UGC vibe      | Narrative short film, product launch reel, montage |
| One character, one location/world              | Multiple subjects, multiple locations, hard cuts |
| Vertical 9:16 or square 1:1                    | Any aspect, often 16:9 |
| Want a coherent "single shoot" feel            | Want intentional jump cuts between disparate scenes |

If unsure, ask the user. The single-storyboard-sheet method is the right default for almost every social brief.

## Hard rule: confirm before burning video credits

**Video jobs are slow (10–12 min each) and expensive (~1564 CU per 15s seedance-2 720p job). Never start one without:**

1. **Aspect confirmed** — 9:16 vertical, 16:9 horizontal, 1:1 square? Ask if not stated.
2. **Duration confirmed** — 5s, 10s, 15s? Default 15s for social shorts unless told otherwise.
3. **Storyboard approved by the user** — show 1 (or 2–3 variations if the brief is loose) and wait for the pick before kicking off `generate video`.

Showing video output the user didn't pre-approve a storyboard for is how you burn credits and end up with *"videos random que no tenen sentit"* — disconnected output that wastes both credits and trust.

## Step-by-step workflow

### 1. Clarify the brief (single batched ask)

Before any generation, gather in **one short message** (not five back-and-forths):

- **Format / aspect**: 9:16 (TikTok/Reels/Shorts), 16:9 (YouTube/landscape), 1:1 (feed).
- **Duration**: typically 5, 10, or 15 seconds.
- **Concept / mood**: one line — "GRWM gym edition", "Hogwarts birthday for X", "product unboxing", etc.
- **Subject / identity refs**: real person (need face photos)? generic model? mascot?
- **Style notes**: palette, brand, aesthetic references.
- **Key beats**: 4–6 things that need to happen in the video.

Skip whichever the user already volunteered. Don't ask twice.

### 2. Compose the storyboard prompt

Editorial storyboard layouts work. The Krea Agent canonical reference (GRWM Gym Edition: 4 blocks × 8 cells, 32 cells total, side category icons, header/subtitle/footer in elegant script/serif) follows this skeleton:

```
Aesthetic "<TITLE>" storyboard layout, minimal neutral-toned design, soft <palette> color palette, clean editorial grid.
Top header text:
"<TITLE>"
subtitle: "<subtitle>" in elegant script font
subheading: "<one-line description>"
The layout is divided into <N> blocks, each showing a sequence (1–<M> steps per row), featuring the same <subject> throughout with consistent face, <styling notes>.
BLOCK 1 – <NAME> (1–M)
1–2: <action>
3–4: <action>
...
BLOCK 2 – <NAME> (M+1–2M)
...
Side icons representing categories: <list>.
<lighting / style / framing notes>, consistent framing across all panels.
Footer text:
"<closing line>"
```

**Good annotations on a storyboard**: tiny panel numbers, short verb-phrase action labels under each cell ("Put on sports bra", "Adjust fit"), left-side category column with line icons, editorial header / subtitle / footer.

**Bad annotations on a storyboard**: large technical fiches per panel ("camera: 50mm / light: warm / style: editorial / notes: ..."), duration tags ("1.5s"), info bars below the grid. These eat visual area and confuse the video model — the first Valeryia/Hogwarts attempt failed because of this.

**Layout heuristic**: 4–8 cells works for a 5–10s clip. 16–32 cells works for a 15s clip with denser micro-beats. The video model will only realize ~5–8 distinct beats in 15s anyway — extra panels reinforce style/character/world continuity, they don't add new cuts.

### 3. Generate the storyboard (cheap, fast)

Use `openai/gpt-image-2` (or current best editorial-text-friendly image model — pull live from `list_models`, don't hardcode) at `quality=high`. Match the storyboard's own aspect — wider canvas for 4×8 grids (landscape), taller for 3×2 portrait grids. Storyboard aspect does NOT have to match final video aspect.

If real-person identity matters, pass face refs in `imageUrls` (gpt-image-2 schema). 1–3 face refs from varied angles work best.

For loose briefs, run **2–3 storyboard variations** in parallel with slightly different palette/mood/composition seeds. Show all to the user side-by-side.

```bash
krea generate image -m openai/gpt-image-2 \
  --aspect 16:9 \
  -i quality=high \
  -i imageUrls='["<face-ref-url>"]' \
  -p "<storyboard prompt>" \
  --wait -o ./storyboard-A.png
```

### 4. Show the user, get the pick

Send the storyboard image(s) with one short line: *"storyboard A / B / C — which one?"* or *"storyboard ready, ok to animate?"*. Wait for the pick. Iterate on the storyboard (cheap, fast) before moving on — fixes at this stage cost cents, fixes at the video stage cost ~1564 CU each.

### 5. Upload the chosen storyboard to Krea

```bash
ID=$(krea upload ./storyboard-chosen.png --json | jq -r .id)
# CLI returns an empty `url` field — resolve hosted URL via the assets endpoint:
SHEET=$(curl -sS -H "Authorization: Bearer $KREA_API_KEY" \
  "https://api.krea.ai/assets/$ID" | jq -r .image_url)
```

(`krea upload --json` returns an empty `url` field — use the asset endpoint. Tracked as issue #6 in `krea-ai/skills`.)

Kontext and Seedream-4 also reject non-Krea-hosted URLs in `imageUrls` — always upload local assets to Krea first. (Issue #7.)

### 6. Compose the video timeline prompt

The video prompt has two halves: (a) tell seedance to use the storyboard as visual reference, and (b) lay out the timeline as a CUT script with absolute timestamps.

```
Use provided storyboard image as reference.

CONCEPT:
<one-line concept>

TIMELINE:
0:00–0:Xs
<beat 1, beat 2, beat 3...>
0:Xs–0:Ys
<beat 4, beat 5...>
...

STYLE:
<palette, lighting, environment, aesthetic>

CAMERA:
<close-up + mid shots, fluid focus, framing notes>

TRANSITIONS:
<match cuts, fabric-motion cuts, jump cuts...>

OUTPUT:
Loopable, smooth pacing, vertical 9:16 (or whatever)
```

**Banned words**: "slow", "gentle", "soft", "slow motion". Seedance literally interprets them as slow-motion playback. Use "smooth", "steady", "fluid" instead. (Today's first GRWM cut came back in slow-mo because the prompt used "soft, gentle pacing".)

### 7. Submit the video job

Default to **`bytedance/seedance-2`** at 720p. `seedance-2-fast` exists but produces lower quality — only use it if the user explicitly asks for speed.

```bash
krea generate video -m bytedance/seedance-2 \
  --aspect 9:16 \
  --duration 15 \
  -i resolution=720p \
  -i referenceImages='["<storyboard-url>", "<face-ref-url-optional>"]' \
  -p "<timeline-prompt>" \
  --json
```

**Critical**: do NOT pass `--start-image` if you want the output aspect to follow `--aspect`. A `startImage` forces the output aspect to match the source image dimensions — pass a landscape storyboard cell as start image and the output comes out landscape even with `--aspect 9:16`. (This caused multiple horizontal outputs today when the user asked for vertical.)

For 9:16 vertical, leave `--start-image` empty and let `referenceImages` carry the visual reference.

### 8. Poll and download

Seedance-2 15s 720p jobs run 8–15 minutes. Use `krea jobs wait <id> --json` if the CLI version supports long timeouts, otherwise fall back to manual `krea jobs show <id> --json` polling with a 15–25s sleep.

Watch out for the CLI's `--timeout` flag being silently capped on older versions (tracked as issue #9). Manual `jobs show` polling is the safer fallback.

### 9. Post-process for delivery

Raw seedance output is 720×1280. Scale + pad to 1080×1920 for social delivery:

```bash
ffmpeg -y -i out.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 128k -pix_fmt yuv420p -movflags +faststart \
  final.mp4
```

Sample 4–6 frames with `ffmpeg -vf "select='not(mod(n\,60))'" -vsync vfr frame-%d.jpg` for QA before sending.

## Honest expectations (set these with the user upfront)

- **Beats per 15s**: Seedance-2 resolves ~5–8 distinct beats per 15s, regardless of how many panels are in the storyboard. The storyboard mostly transfers **aesthetic / palette / character / outfit / world** — the timeline prompt does the actual choreographic work.
- **Identity preservation**: Face refs are moderate (5–7/10 average). Don't promise photo-accurate likeness. For real-person gifts or brand-critical work, manage expectations honestly or use a LoRA (see `lora-training.md`).
- **Continuity**: Hair/styling continuity can drift across cuts. Lock it in the timeline prompt (e.g. "hair tied in a tight bun throughout").
- **Cost**: ~1564 CU per 15s seedance-2 720p job. With unlimited-tier keys the bottleneck is the 8–15 min processing time, not credits.

## Failure recovery

| Problem                                            | Cause                                                | Fix |
|---|---|---|
| Output is horizontal despite `--aspect 9:16`       | Passed a landscape `--start-image`                   | Drop start-image, rely on `referenceImages` only |
| Output is slow motion                              | Prompt contained "slow", "gentle", "soft"            | Strip those words, rewrite with "smooth", "steady", "fluid" |
| Video feels like jump-cut snippets stitched        | Generated panels separately and ffmpeg-concatenated  | Generate ONE storyboard sheet, ONE seedance job with timeline prompt |
| Storyboard has technical fiches confusing the model | Used "01 ARRIVAL / 1.5s / icon" annotations         | Strip to: tiny panel num + short action label + category icon |
| `krea upload --json` returns empty `url`           | Known issue #6                                       | Resolve `id` via `GET https://api.krea.ai/assets/<id>`, use `.image_url` |
| Job times out before completion                    | CLI `--timeout` capped (issue #9)                    | Switch to manual `krea jobs show` polling loop |
| External (non-Krea) URL rejected by Kontext/Seedream-4 | Known issue #7                                   | Always upload local assets to Krea first; use Krea-hosted URLs |
| Identity drift across cuts                         | Single face ref, weak likeness model                 | Pass 2–3 face refs from varied angles; if still weak, train a LoRA |
