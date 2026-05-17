# Video Production — Multi-Scene Storytelling

Create multi-scene videos with AI-generated visuals using the Krea CLI (or MCP fallback) for generation and `ffmpeg` for post-production. Works for short films, product launches, team intros, promo reels, music videos, explainers, event recaps — anywhere you need **multiple distinct cuts** stitched together.

> Requires: the Krea CLI (`krea`) or the Krea MCP (`mcp__krea-public-api__*`), plus `ffmpeg`.

## Pick the right workflow first

| Brief                                                  | Use |
|---|---|
| ≤15s vertical/square social short (GRWM, ad, UGC, "day in the life") | `storyboard-method.md` — **default for social** |
| One character, one location, single continuous video    | `storyboard-method.md` |
| >15s with multiple distinct cuts / locations / subjects | **this file** |
| Narrative short film, multi-scene product launch, promo reel with hard cuts between disparate scenes | **this file** |

If unsure, default to the single-storyboard-sheet method (`storyboard-method.md`). It produces a more coherent result for almost every social brief, and avoids the "varis videos enganxats" (stitched snippets) feel that multi-scene concatenation can have when overused.

## The golden rule

**Never generate video directly. Always generate frames first.**

Video generation is expensive and slow. Image generation is cheap and fast. Get the visuals right as stills, get user approval, **then** animate.

```
Clarify brief → Plan shot list → Generate frames → User reviews each frame → Animate approved frames → Normalize → Concat → Add audio
```

Generating all videos before the user has even seen the first frame is a bad workflow. Approval comes first.

## Before any frame: clarify

Same single-batched ask as in `storyboard-method.md`. Don't skip it:

- Aspect (9:16 / 16:9 / 1:1)
- Target total duration
- Concept / mood
- Identity refs needed (face photos / brand assets / mascot)
- Style notes (palette, brand, references)
- Beat list (the shot list you'll work from)

---

## The workflow

### Step 1: Plan the shot list

Before generating anything, collaborate with the user on a shot list. Define scenes, subjects, shot types, and mood.

```
PROJECT — SHOT LIST

1. TITLE: "Company Name" — 3D typography, dark background, 1.5s
2. OPENER: Wide establishing shot — setting the scene — ~5s
3. SCENE: [Subject A] solo — specific action/emotion — ~5s
4. SCENE: [Subject B + C] together — interaction — ~5s
5. SCENE: Detail/product close-up — ~5s
6. SCENE: Full group — ensemble action — ~5s
7. FINALE: Closing shot / call to action — ~5s
```

**Shot type variety matters.** Mix wide shots, close-ups, low angles, detail shots. All same framing = amateur.

**Give every subject their moment.** If the project features people, assign each person at least one scene with their face reference.

### Step 2: Pick the model archetypes you'll need

Call `list_models()` once. From the result, identify:

- **A high-fidelity image model with face/reference support.** Likely something with `nano-banana-pro`-style multi-reference (`imageUrls`) for scenes with people. Confirm via `get_model_schema`.
- **A text-friendly image model** for title cards. Look for models whose description mentions typography or on-image text.
- **A fast image-to-video model** for animating approved frames. Should accept a `startImage` (or equivalent).

Capture the chosen IDs once; reuse for all scenes in the project.

### Step 3: Generate frames (one at a time, show the user each)

For each shot in the list, generate the frame and show the user.

```
# Upload references first
ceo_face = upload_asset(filename="ceo.png", mimeType="image/png", fileData=base64(...))
eng1 = upload_asset(filename="eng1.png", mimeType="image/png", fileData=base64(...))
eng2 = upload_asset(filename="eng2.png", mimeType="image/png", fileData=base64(...))

# Title card (text-friendly model)
title_frame = generate_image(
    model="<text-friendly image model id>",
    input={
        prompt: "3D chrome text 'LAUNCH DAY' floating in dark smoky space, volumetric lighting, luxury",
        width: 720, height: 1280,  # OR aspectRatio: "9:16" per get_model_schema
    },
    sync=true, timeoutSeconds=60,
)
# Download, Read with vision, verify, send URL to user, wait for approval.

# Scene with face references (multi-reference model)
keynote_frame = generate_image(
    model="<multi-reference image model id>",
    input={
        prompt: "CEO on stage, spotlight, massive screen behind, keynote energy, low angle",
        imageUrls: [ceo_face.url],
        width: 720, height: 1280,
    },
    sync=true, timeoutSeconds=60,
)
# Show to user, get approval.

# Group scene (multiple face references)
team_frame = generate_image(
    model="<multi-reference image model id>",
    input={
        prompt: "Engineering team walking toward camera in modern office, golden hour, editorial",
        imageUrls: [eng1.url, eng2.url],
        width: 720, height: 1280,
    },
    sync=true, timeoutSeconds=60,
)
```

### Step 4: User approval gate

**This is hard-mandatory.** Show every frame, wait for the user to approve. Regenerate any that don't work. Only proceed to video once all frames are approved.

Do **not** batch-animate all frames hoping they'll be fine. Each animation is expensive and slow — wasting that on unapproved visuals is brutal.

### Step 5: Animate approved frames

For each approved frame, submit an image-to-video job. **Video is always async** — submit, then poll `get_job` until terminal.

```
# Animate the title card
title_job = generate_video(
    model="<fast image-to-video model id>",
    input={
        prompt: "Chrome text emerges from darkness, dramatic light sweep, metallic shimmer",
        startImage: title_frame.url,
        duration: 5,
        aspectRatio: "9:16",
    },
    sync=false,
)

# Animate the keynote
keynote_job = generate_video(
    model="<fast image-to-video model id>",
    input={
        prompt: "CEO walks across stage, gestures to screen, audience applauds, lights shift",
        startImage: keynote_frame.url,
        duration: 5,
        aspectRatio: "9:16",
    },
    sync=false,
)

# ...etc, submit all in quick succession, then poll each.
```

**Submit all video jobs first**, then poll each. They run in parallel server-side; serial polling is fine. See `async-polling.md` for the loop pattern.

**Animation prompts describe MOTION, not the static scene.** The model already sees the frame — tell it what should happen next.

### Step 6: Download all clips

Once each job completes, download the result MP4 locally for ffmpeg work. Save with clear names: `vid-title.mp4`, `vid-keynote.mp4`, etc.

### Step 7: Normalize all clips

Every clip MUST be normalized before concatenation. Different models output different resolutions, framerates, and codecs.

```bash
# Standard normalization (720x1280 portrait, 24fps, h264, no audio)
ffmpeg -y -i vid-keynote.mp4 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -preset fast -crf 18 -r 24 -an \
  vid-keynote-norm.mp4
```

For landscape (16:9), swap to `1280:720`.

Trim the title card to ~1.5–2s (videos default to 5s; titles should be short):

```bash
ffmpeg -y -i vid-title.mp4 -t 1.5 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -preset fast -crf 18 -r 24 -an \
  vid-title-short.mp4
```

Verify specs after normalization:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name -of csv=p=0 vid-keynote-norm.mp4
# Expected: h264,720,1280,24/1
```

### Step 8: Concatenate

```bash
cat > concat.txt << 'EOF'
file 'vid-title-short.mp4'
file 'vid-opener-norm.mp4'
file 'vid-keynote-norm.mp4'
file 'vid-product-norm.mp4'
file 'vid-finale-norm.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i concat.txt -an -c:v copy output-muted.mp4
```

### Step 9: Add a single audio track

**Critical.** Strip audio from ALL clips during normalization (`-an`). Each AI clip generates its own random audio that sounds terrible when concatenated. Overlay one cohesive track at the end.

```bash
VID_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 output-muted.mp4)
FADE_START=$(python3 -c "print(float('${VID_DUR}') - 2)")

ffmpeg -y -i output-muted.mp4 -i music-track.mp3 \
  -c:v copy \
  -c:a aac -b:a 192k \
  -af "atrim=0:${VID_DUR},afade=t=out:st=${FADE_START}:d=2" \
  -map 0:v:0 -map 1:a:0 \
  final-video.mp4
```

Use `python3 -c "print(...)"` for float math instead of `bc` — `bc` isn't installed everywhere.

---

## Prompt engineering for production

### Frame prompts — what works

**Fails (generic, vague):**
- "People in a room, cinematic"
- "A man standing in a hallway"
- "Product on a table"

**Works (specific, compositional):**

```
Conference keynote:
"Two speakers on stage presenting to a packed auditorium, dramatic overhead spotlights, giant screen behind them showing data visualizations, professional photography, wide shot"

Product hero:
"Sleek smartphone floating at an angle above a marble surface, soft studio lighting with rim highlight, water droplets on screen, product photography, close-up"

Team portrait:
"Five engineers standing in V-formation in a modern glass office, arms crossed, confident expressions, dramatic golden hour light from floor-to-ceiling windows, corporate editorial"

Action / energy:
"Drone shot of electric car drifting around mountain hairpin turn, dust cloud trailing, sunset backlighting, aerial wide angle, cinematic"

Emotional moment:
"Founder working alone at desk at 3am, single desk lamp illuminating her face, city lights blurred through the window behind, intimate close-up, documentary style"
```

### Prompt formula

```
[Subject doing specific action] + [setting details] + [lighting/mood] + [camera angle] + [genre/style reference] + [quality keywords]
```

Power keywords: "cinematic", "dramatic lighting", "editorial photography", "volumetric light", "documentary style", "slow motion", "professional", "studio lighting".

### Animation prompts (from a start frame)

Describe what HAPPENS — motion, not the static scene.

**Banned words for seedance**: "slow", "gentle", "soft", "slow motion" — seedance literally interprets these as slow-motion playback. Use "smooth", "steady", "fluid" instead unless slow-mo is the actual intent.

**Aspect-ratio trap**: if you pass a horizontal `startImage`, seedance forces a horizontal output even with `--aspect 9:16`. For vertical output, either use a vertical start frame, or omit `--start-image` and let `referenceImages` carry the visual reference.

**Cost note**: seedance-2 15s 720p ≈ 1564 CU and runs 8–15 min per job. Prefer `seedance-2` over `seedance-2-fast` for quality unless the user explicitly asks for speed.

```
Keynote:
"The speakers gesture toward the screen, camera slowly pushes in, audience applauds, spotlights shift"

Product reveal:
"The phone slowly rotates, water droplets slide off the screen, light catches the edges, subtle reflection shift"

Team:
"The team uncrosses arms and walks toward camera in unison, golden light shifts across their faces, confident slow motion"

Car:
"The car accelerates out of the turn, dust cloud expands, camera follows the motion, sunlight flares through the dust"

Title reveal:
"The text slowly emerges from darkness with a dramatic light sweep, volumetric smoke drifts behind, subtle metallic shimmer"
```

### Title card prompts

```
Chrome / minimal:
"The word 'LAUNCH' in sleek 3D chrome metallic typography floating in dark smoky space, volumetric lighting, cinematic, minimal, luxury aesthetic, dark background"

Bold / colorful:
"The text 'BEHIND THE SCENES' in bold 3D typography with gradient colors, floating above clouds, dramatic lighting, modern design, dark background"
```

---

## Scene replacement

When the user wants to replace a single scene in an already-assembled video:

1. Generate new frame → show for approval
2. Animate once approved
3. Normalize the new clip (same specs as the others)
4. Update `concat.txt` (swap the filename)
5. Re-concat
6. Re-overlay audio

---

## Failure patterns

| Problem | Cause | Fix |
|---|---|---|
| Video job fails with empty result | Content moderation or bad start image | Soften prompt; use full scene image not tight headshot |
| Tight headshot rejected as start image | Not enough visual context for animation | Use full scene compositions as start images |
| No job ID returned | Rate limiting | Wait and retry |
| All scenes look the same | Same start image or same prompt structure | Generate unique frames for each scene with varied composition |
| Concatenated audio sounds terrible | Each AI clip has random generated audio | Strip all audio (`-an`), overlay single cohesive track |
| Faces don't appear in image | Used a single-reference model when you needed multi-reference | Switch to a model whose schema declares `imageUrls` (array) |
| Concat produces glitches | Mixed resolutions/codecs/framerates | Normalize ALL clips to identical specs before concat |
| Title cards too long | Default video duration is 5s | Trim to 1.5–2s with `ffmpeg -t` |
| `bc: command not found` | bc not installed | Use `python3 -c "print(...)"` for float math |
| Output is slow motion | Prompt contained "slow", "gentle", "soft" | Strip those words, rewrite with "smooth", "steady", "fluid" |
| Output is horizontal despite `--aspect 9:16` | Passed a landscape `--start-image` | Drop start-image, rely on `referenceImages`; or generate a vertical start frame |
| Video feels like "varis videos enganxats" (snippets stitched) | Multi-scene concat on a brief that wanted a single coherent video | Switch to the single-storyboard-sheet method in `storyboard-method.md` |
| `krea upload --json` returns empty `url` | Known issue #6 | Resolve `id` via `GET https://api.krea.ai/assets/<id>`, read `.image_url` |
| External (non-Krea) URL rejected by Kontext/Seedream-4 | Known issue #7 | Always upload local assets to Krea first; use Krea-hosted URLs |
| Identity drift across cuts | Single face ref / weak likeness | Pass 2–3 face refs from varied angles; if still weak, train a LoRA (`lora-training.md`) |

---

## Shot vocabulary

| Type | Framing | Use it for |
|---|---|---|
| **ECU** Extreme Close-Up | Eyes / detail only | Intense emotion, product detail, texture |
| **CU** Close-Up | Face fills the frame | Reaction shots, solo spotlight, intimacy |
| **MS** Medium Shot | Waist up | Dialogue, presentations |
| **WS** Wide Shot | Full body + environment | Establishing, group shots, reveals |
| **Low Angle** | Camera looks up | Power, dominance, hero moments |
| **Dutch Angle** | Tilted frame | Tension, energy, action |

Vary your shots. Monotonous framing kills energy.

---

## Parallel execution

Once approvals are in, you can submit multiple animation jobs back-to-back without waiting. They run in parallel server-side; you just poll each in turn.

```
# Submit all video jobs in quick succession
jobs = [
    generate_video(model="<id>", input={...startImage: title_frame.url, prompt: "..."}, sync=false),
    generate_video(model="<id>", input={...startImage: keynote_frame.url, prompt: "..."}, sync=false),
    generate_video(model="<id>", input={...startImage: product_frame.url, prompt: "..."}, sync=false),
    generate_video(model="<id>", input={...startImage: team_frame.url, prompt: "..."}, sync=false),
]

# Then poll each until terminal
for j in jobs:
    while True:
        s = get_job(jobId=j.id)
        if s.status in ("completed", "failed", "cancelled"): break
        sleep 10
```

For batch-style pipelines (the user wants a reusable workflow), the agent generates code in your stack via `krea-build`. See `pipelines.md`.
