# Storyboard-Sheet Method — Short Social-Format Videos

For 5–15s vertical or square videos (social shorts, GRWM, ad creative, "day in the life", quick explainers), the cleanest path is **one editorial storyboard sheet + one timeline-driven `seedance-2` job**. Not per-scene frame generation concatenated with `ffmpeg`.

This is the canonical pattern for Krea Agent–style social shorts. For longer narrative work with hard cuts across distinct subjects or locations, use `video-production.md` instead.

## When to use this vs `video-production.md`

| Use storyboard-sheet method (this doc) | Use multi-scene production (`video-production.md`) |
|---|---|
| Output ≤ 15s, single continuous video | Output > 15s, multiple distinct cuts |
| Editorial / social / GRWM / ad-vibe | Narrative short film, product launch reel |
| One character, one location/world | Multiple subjects, multiple locations, hard cuts |
| Vertical 9:16 or square 1:1 | Any aspect, often 16:9 |
| Want a coherent "single shoot" feel | Want intentional jump cuts and montage |

If unsure, ask the user which one they want.

## Hard rule: confirm before burning video credits

Video jobs are slow (8–15 min each) and expensive (≥1000 CU). Never start one without:

1. **Aspect confirmed** — 9:16 vertical, 16:9 horizontal, or 1:1 square. Ask if not stated.
2. **Duration confirmed** — 5s, 10s, or 15s. Default 15s for social shorts unless told otherwise.
3. **Storyboard approved by the user** — show 1, or 2–3 variations if the brief is loose, and wait for the pick before kicking off `generate video`.

Skipping any of these is how you ship videos the user didn't pre-approve and burn credits without earning trust.

## Step-by-step workflow

### 1. Clarify the brief (one short message, not five)

Before any generation, gather — skip whatever the user already volunteered:

- **Format / aspect**: 9:16 (TikTok / Reels / Shorts), 16:9 (YouTube / landscape), 1:1 (feed).
- **Duration**: typically 5, 10, or 15 seconds.
- **Concept / mood**: one line — "GRWM gym edition", "Hogwarts birthday", "product unboxing", etc.
- **Subject / identity refs**: real person (need face photos)? generic model? mascot?
- **Style notes**: palette, brand, aesthetic references.
- **Key beats**: 4–6 things that need to happen in the video.

Ask everything missing in one message. Don't drip the questions out one at a time.

### 2. Compose the storyboard prompt

Editorial storyboard layouts work well. Template (adapt freely):

```
Aesthetic "<TITLE>" storyboard layout, minimal neutral-toned design,
soft <palette> color palette, clean editorial grid.

Top header text:
  "<TITLE>"
  subtitle: "<subtitle>" in elegant script font
  subheading: "<one-line description>"

The layout is divided into <N> blocks, each showing a sequence
(1–<M> steps per row), featuring the same <subject> throughout
with consistent face, <styling notes>.

BLOCK 1 – <NAME> (1–M)
  1–2: <short verb-phrase action>
  3–4: <short verb-phrase action>
  ...
BLOCK 2 – <NAME> (M+1–2M)
  ...

Side icons representing categories: <list>.

<lighting / style / framing notes>, consistent framing across all panels.

Footer text:
  "<closing line>"
```

**Good annotations on a storyboard:**

- Tiny panel numbers.
- Short verb-phrase action labels under each cell ("Put on jacket", "Adjust fit").
- Left-side category column with line icons + names.
- Editorial header / subtitle / footer in elegant serif or script.

**Bad annotations on a storyboard** (strip these — they eat visual area and confuse the video model):

- Large technical fiches per panel ("camera: 50mm / light: warm / style: editorial / notes: ...").
- Per-panel duration tags ("1.5s").
- Info bars below the grid.

**Layout heuristic:** 4–8 cells works for a 5–10s clip. 16–32 cells works for a 15s clip with denser micro-beats. Seedance-2 will only realize ~5–8 distinct beats in 15s anyway — extra panels reinforce style / character / outfit continuity, they don't add new cuts.

### 3. Generate the storyboard (cheap, fast)

Use `openai/gpt-image-2` (or current best editorial-text-friendly image model — confirm via `list_models`) at `quality=high`.

Storyboard canvas aspect can differ from final video aspect. Pick whatever fits the grid: landscape canvas for wide 4×8 grids, portrait canvas for 3×2 grids, etc.

If real-person identity matters, pass face refs in `imageUrls` (per the model's schema). 1–3 face refs from varied angles work best.

For loose briefs, run **2–3 storyboard variations** with slightly different palette / mood / composition. Show all to the user side-by-side.

### 4. Show the user, get the pick

Send the storyboard image(s) with a one-line ask: which storyboard, or OK to animate. **Wait for the user.** Iterate on the storyboard until they approve. This is the cheap iteration loop — use it.

### 5. Upload the chosen storyboard to Krea

```bash
ID=$(krea upload ./storyboard-chosen.png --json | jq -r .id)
# Resolve the hosted URL:
SHEET=$(curl -sS -H "Authorization: Bearer $KREA_API_KEY" \
  "https://api.krea.ai/assets/$ID" | jq -r .image_url)
```

`krea upload --json` returns an empty `url` field at the time of writing — use the asset endpoint to resolve the hosted URL. (See issue #6 in `krea-ai/skills`.)

Kontext / Seedream-4 and similar models reject non-Krea-hosted URLs in `imageUrls`. Always upload local assets to Krea first; pass the resolved `image_url` into the next call. (See issue #7.)

### 6. Compose the video timeline prompt

The video prompt has two halves: (a) tell seedance to use the storyboard as reference, and (b) lay out the timeline as a cut script with absolute timestamps.

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
<close-up + mid shots, focus, framing notes>

TRANSITIONS:
<match cuts, fabric-motion cuts, jump cuts...>

OUTPUT:
Loopable, smooth pacing, vertical 9:16 (or whatever aspect was confirmed).
```

**Avoid these words in seedance prompts**: "slow", "gentle", "soft", "slow motion". Seedance-2 interprets them literally and emits slow-motion footage. Use "smooth", "steady", "fluid" instead — they get the same energy without the speed penalty.

### 7. Submit the video job

Default to `bytedance/seedance-2` at 720p. `seedance-2-fast` exists but is lower quality — prefer `seedance-2` unless the user explicitly asks for speed.

```bash
krea generate video -m bytedance/seedance-2 \
  --aspect 9:16 \
  --duration 15 \
  -i resolution=720p \
  -i referenceImages='["<storyboard-url>", "<face-ref-url-optional>"]' \
  -p "<timeline-prompt>" \
  --json
```

**Critical — `--start-image` aspect lock:** do NOT pass `--start-image` if you want the output aspect to follow `--aspect`. A `startImage` forces the output aspect to match the source image dimensions. If you pass a landscape storyboard cell as the start image with `--aspect 9:16`, the output still comes out landscape.

For 9:16 vertical output, leave `--start-image` empty and let `referenceImages` carry the visual context.

### 8. Poll and download

Seedance-2 15s 720p jobs run 8–15 minutes. Use either:

```bash
# Server-blocking wait (preferred if your CLI version handles it):
krea jobs wait <job-id> --timeout 1200 --json

# Or manual polling loop with 15–25s sleep:
krea jobs show <job-id> --json
```

Some CLI versions silently cap `--timeout` to 300s (see issue #9 in `krea-ai/skills`); manual `jobs show` polling is the safe fallback.

### 9. Post-process for delivery

Raw output is usually 720×1280. Scale + pad to 1080×1920 for social delivery:

```bash
ffmpeg -y -i out.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  final.mp4
```

Sample 4–6 frames for QA before sending:

```bash
ffmpeg -i final.mp4 -vf "select='not(mod(n\,60))'" -vsync vfr frame-%d.jpg
```

## Honest expectations

- Seedance-2 resolves ~5–8 distinct beats per 15s, regardless of how many panels are in the storyboard. The storyboard transfers **aesthetic / palette / character / outfit / world** — the timeline prompt does the actual choreographic work. Don't promise "32 panels = 32 cuts".
- Identity preservation with face refs is moderate (5–7/10 on average). Don't promise photo-accurate likeness. For real-person work where likeness matters, manage expectations up front or use a LoRA (see `lora-training.md`).
- Hair / styling continuity drifts across cuts. Lock it in the timeline prompt ("hair tied in a tight bun throughout", "same jacket every beat").
- A 15s `seedance-2` 720p job costs roughly 1500–1600 CU and runs 8–15 minutes. Budget accordingly.

## Failure recovery

| Problem | Cause | Fix |
|---|---|---|
| Output is horizontal despite `--aspect 9:16` | Passed a landscape `--start-image` | Drop `--start-image`, rely on `referenceImages` only |
| Output is slow motion | Prompt contained "slow", "gentle", "soft", "slow motion" | Strip those words, rewrite with "smooth", "steady", "fluid" |
| Video feels like jump-cut snippets stitched together | You generated panels separately and `ffmpeg`-concatenated | Generate ONE storyboard sheet, ONE `seedance` job with a timeline prompt |
| Storyboard has technical fiches confusing the model | On-panel "camera / light / style / notes" annotations | Strip to: tiny panel num + short action label + category icon only |
| `krea upload --json` returns empty `url` field | Known issue #6 | Resolve `id` via `GET https://api.krea.ai/assets/<id>` and use `.image_url` |
| Job times out after 300s | CLI `--timeout` silently capped (issue #9) | Switch to manual `jobs show` polling loop |
| External (non-Krea) URL rejected by Kontext / Seedream-4 | Known issue #7 | Always upload local assets to Krea first; use the Krea-hosted URL |
