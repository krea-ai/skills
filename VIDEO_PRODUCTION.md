# Video Production — Multi-Scene Storytelling

Create multi-scene videos with AI-generated visuals using Krea AI for image/video generation and ffmpeg for post-production. Works for any format: short films, product launches, team intros, promo reels, music videos, explainers, event recaps.

> Requires: Krea AI skill (this repo), `ffmpeg`, `uv`

## The Golden Rule

**Never generate video directly. Always generate frames first.**

Video generation is expensive (39+ CU per clip, 12s+ processing). Image generation is cheap and fast (~5 CU, ~5s). Get the visuals right in 2D, get user approval, THEN animate.

```
Plan shot list → Generate frames → User reviews each frame → Animate approved frames → Normalize → Concat → Add audio
```

**A bad workflow** is generating all videos before the user has even seen the first frame. The user must approve visuals before any animation starts.

---

## The Workflow

### Step 1: Plan the Shot List

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

**Shot type variety is critical**: Mix wide shots, close-ups, low angles, detail shots. All same framing = amateur.

**Give every subject their moment**: If featuring people, assign each person at least one scene with their face reference.

### Step 2: Generate Frames

Generate frames one at a time or in small batches. **Show each frame to the user before proceeding.**

```bash
# Title card (nano-banana-2 renders text well)
uv run scripts/generate_image.py \
  --prompt "3D chrome text 'Company Name' floating in dark smoky space, volumetric lighting, cinematic" \
  --model nano-banana-2 --filename "frame-title.png" --width 720 --height 1280

# Scene with face references (nano-banana-pro supports multiple imageUrls)
uv run scripts/generate_image.py \
  --prompt "Two colleagues presenting at a conference, dramatic stage lighting, professional" \
  --image-url face1.png face2.png \
  --model nano-banana-pro --filename "frame-presenters.png" --width 720 --height 1280

# Scene with style/composition reference (single image-url)
uv run scripts/generate_image.py \
  --prompt "Aerial view of modern office building at sunset, cinematic drone shot" \
  --image-url reference-photo.jpg \
  --model nano-banana-2 --filename "frame-building.png" --width 720 --height 1280
```

### Step 3: User Reviews Frames

**This is an approval gate.** Show each frame in chat. The user approves, rejects, or requests changes. Regenerate any frames that don't work. Only proceed to video once all frames are approved.

Do NOT batch-animate all frames hoping they'll be fine. Each frame costs 39+ CU to animate — wasting that on unapproved visuals is expensive and slow.

### Step 4: Animate Approved Frames

Convert approved frames to video clips using image-to-video.

```bash
uv run scripts/generate_video.py \
  --prompt "The presenters gesture confidently, camera slowly pushes in, stage lights shift" \
  --start-image "frame-presenters.png" \
  --model seedance-2-fast \
  --filename "vid-presenters.mp4" \
  --aspect-ratio 9:16
```

**Animation prompts describe MOTION, not the static scene.** The model already sees the frame — tell it what should happen next.

Run multiple animations in parallel to save time (they're independent).

### Step 5: Normalize All Clips

Every clip MUST be normalized before concatenation. Different models output different resolutions, framerates, and codecs.

```bash
# Standard normalization (720x1280 portrait, 24fps, h264, no audio)
ffmpeg -y -i INPUT.mp4 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -preset fast -crf 18 -r 24 -an \
  OUTPUT-norm.mp4
```

For landscape (16:9), swap to `1280:720`.

**Title cards — also trim duration** (1.5-2s, not the default 5s):
```bash
ffmpeg -y -i title.mp4 -t 1.5 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -preset fast -crf 18 -r 24 -an \
  title-short.mp4
```

Verify specs after normalization:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,codec_name -of csv=p=0 clip-norm.mp4
# Expected: h264,720,1280,24/1
```

### Step 6: Concatenate

```bash
# Create concat list (order = final video sequence)
cat > concat.txt << 'EOF'
file 'vid-title-short.mp4'
file 'vid-opener-norm.mp4'
file 'vid-presenters-norm.mp4'
file 'vid-product-norm.mp4'
file 'vid-finale-norm.mp4'
EOF

# Concat (copy codec — all clips already normalized to same spec)
ffmpeg -y -f concat -safe 0 -i concat.txt -an -c:v copy output-muted.mp4
```

### Step 7: Add Audio Track

**Critical**: Strip audio from ALL clips during normalization (`-an`). Each AI video model generates random audio that sounds terrible when concatenated. Overlay a single cohesive track.

```bash
# Get video duration
VID_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 output-muted.mp4)

# Calculate fade-out start (2 seconds before end)
FADE_START=$(python3 -c "print(float('${VID_DUR}') - 2)")

# Overlay music with fade out
ffmpeg -y -i output-muted.mp4 -i music-track.mp3 \
  -c:v copy \
  -c:a aac -b:a 192k \
  -af "atrim=0:${VID_DUR},afade=t=out:st=${FADE_START}:d=2" \
  -map 0:v:0 -map 1:a:0 \
  final-video.mp4
```

**Note**: `bc` may not be available — always use `python3 -c "print(...)"` for float math.

---

## Model Selection

| Task | Model | Cost | Why |
|------|-------|------|-----|
| Face-conditioned scenes | `nano-banana-pro` via multiple `--image-url` | 119 CU | Supports multiple face/reference images via `imageUrls` |
| Title cards / 3D typography | `nano-banana-2` | ~5 CU | Good at rendering text, cheap |
| Scene from reference (no faces) | `nano-banana-2` + single `--image-url` | ~5 CU | Style/scene transfer without face injection |
| Quick draft (iteration) | `flux-1-dev` or `z-image` | 3-5 CU | Cheap, fast, good for prompt tuning |
| Video animation | `seedance-2-fast` | 39 CU | Fast (~12s), cheap, good motion quality |
| Premium video (budget allows) | `veo-3.1-fast` or `kling-2.5` | 275-307 CU | Higher quality motion |

### When to use which image model

- **Need specific faces in the scene** → `nano-banana-pro` with multiple `--image-url` values
- **Need text/typography** → `nano-banana-2` (renders text well)
- **Need scene based on reference photo** → `nano-banana-2` with single `--image-url`
- **Pure text-to-image, no reference** → `nano-banana-2` (balanced) or `flux-1-dev` (cheap drafts)

---

## Prompt Engineering

### Frame Prompts

**What FAILS** (generic, vague):
- "People in a room, cinematic"
- "A man standing in a hallway"
- "Product on a table"

**What WORKS** (specific, compositional):

```
# Conference keynote
"Two speakers on stage presenting to a packed auditorium, dramatic overhead spotlights, giant screen behind them showing data visualizations, professional photography, wide shot"

# Product hero
"Sleek smartphone floating at an angle above a marble surface, soft studio lighting with rim highlight, water droplets on screen, product photography, close-up"

# Team portrait
"Five engineers standing in V-formation in a modern glass office, arms crossed, confident expressions, dramatic golden hour light from floor-to-ceiling windows, corporate editorial"

# Action/energy
"Drone shot of electric car drifting around mountain hairpin turn, dust cloud trailing, sunset backlighting, aerial wide angle, cinematic"

# Emotional moment
"Founder working alone at desk at 3am, single desk lamp illuminating her face, city lights blurred through the window behind, intimate close-up, documentary style"
```

### Prompt Formula

```
[Subject doing specific action] + [setting details] + [lighting/mood] + [camera angle] + [genre/style reference] + [quality keywords]
```

**Power keywords**: "cinematic", "dramatic lighting", "editorial photography", "volumetric light", "documentary style", "slow motion", "professional", "studio lighting"

### Animation Prompts (from start frame)

The animation prompt describes what HAPPENS — motion, not the static scene. The model already sees the frame.

```
# Keynote
"The speakers gesture toward the screen, camera slowly pushes in, audience applauds, spotlights shift"

# Product reveal
"The phone slowly rotates, water droplets slide off the screen, light catches the edges, subtle reflection shift"

# Team
"The team uncrosses arms and walks toward camera in unison, golden light shifts across their faces, confident slow motion"

# Car
"The car accelerates out of the turn, dust cloud expands, camera follows the motion, sunlight flares through the dust"

# Title reveal
"The text slowly emerges from darkness with a dramatic light sweep, volumetric smoke drifts behind, subtle metallic shimmer"
```

### Title Card Prompts

```
# Chrome/minimal
"The word 'LAUNCH' in sleek 3D chrome metallic typography floating in dark smoky space, volumetric lighting, cinematic, minimal, luxury aesthetic, dark background"

# Bold/colorful
"The text 'BEHIND THE SCENES' in bold 3D typography with gradient colors, floating above clouds, dramatic lighting, modern design, dark background"
```

---

## Scene Replacement

When the user wants to replace a single scene in an already-assembled video:

1. Generate new frame → show to user for approval
2. Animate once approved
3. Normalize new clip (same specs as all other clips)
4. Update the concat list file (swap the filename)
5. Re-concat everything
6. Re-overlay the audio track

---

## Failure Patterns

| Problem | Cause | Fix |
|---------|-------|-----|
| Video job fails with `{}` | Content moderation or bad start image | Tone down prompt; use full scene image not tight headshot |
| Tight headshot rejected as start image | Not enough visual context for animation | Use full scene compositions as start images |
| No job ID returned | Rate limiting | Wait and retry |
| All scenes look the same | Same start image or same prompt structure | Generate unique frames for each scene with varied composition |
| Concatenated audio sounds terrible | Each AI clip has random generated audio | Strip all audio (`-an`), overlay single cohesive track |
| Faces don't appear in image | Used single `--image-url` with wrong model | Use `nano-banana-pro` with multiple `--image-url` values for face injection |
| Concat produces glitches | Mixed resolutions/codecs/framerates | Normalize ALL clips to identical specs before concat |
| Title cards too long | Default 5s duration | Trim to 1.5-2s with ffmpeg `-t` |
| `bc: command not found` | bc not installed | Use `python3 -c "print(...)"` for float math |

---

## Shot Vocabulary

| Type | Framing | When to Use |
|------|---------|-------------|
| **ECU** (Extreme Close-Up) | Eyes/detail only | Intense emotion, product detail, texture |
| **CU** (Close-Up) | Face fills frame | Reaction shots, solo spotlight, intimacy |
| **MS** (Medium Shot) | Waist up | Dialogue, general action, presentations |
| **WS** (Wide Shot) | Full body + environment | Establishing, group shots, reveals |
| **Low Angle** | Camera looks up | Power, dominance, hero moments |
| **Dutch Angle** | Tilted frame | Tension, energy, action sequences |

**Vary your shots**: Mix CU, MS, WS, and different angles across scenes. Monotonous framing kills energy.

---

## Parallel Execution

Launch independent generation jobs simultaneously to save time:

```bash
# Generate multiple frames in parallel
uv run scripts/generate_image.py --prompt "..." --image-url face1.png --model nano-banana-pro --filename "scene-a.png" &
uv run scripts/generate_image.py --prompt "..." --image-url face2.png face3.png --model nano-banana-pro --filename "scene-b.png" &
uv run scripts/generate_image.py --prompt "..." --model nano-banana-2 --filename "scene-c.png" &
wait

# After user approves all frames, animate in parallel
uv run scripts/generate_video.py --prompt "..." --start-image "scene-a.png" --model seedance-2-fast --filename "vid-a.mp4" --aspect-ratio 9:16 &
uv run scripts/generate_video.py --prompt "..." --start-image "scene-b.png" --model seedance-2-fast --filename "vid-b.mp4" --aspect-ratio 9:16 &
uv run scripts/generate_video.py --prompt "..." --start-image "scene-c.png" --model seedance-2-fast --filename "vid-c.mp4" --aspect-ratio 9:16 &
wait
```

---

## Example: Full Production

```bash
# === FRAMES (generate + show each to user) ===

# Title card
uv run scripts/generate_image.py \
  --prompt "3D chrome text 'LAUNCH DAY' floating in dark smoky space, volumetric lighting, luxury" \
  --model nano-banana-2 --filename "frame-title.png" --width 720 --height 1280

# Scene with face references
uv run scripts/generate_image.py \
  --prompt "CEO on stage, spotlight, massive screen behind, keynote energy, low angle" \
  --image-url ceo-headshot.png \
  --model nano-banana-pro --filename "frame-keynote.png" --width 720 --height 1280

# Product hero
uv run scripts/generate_image.py \
  --prompt "New product floating on dark background, dramatic rim lighting, studio photography" \
  --model nano-banana-2 --filename "frame-product.png" --width 720 --height 1280

# Team finale
uv run scripts/generate_image.py \
  --prompt "Engineering team walking toward camera in modern office, golden hour, editorial" \
  --image-url eng1.png eng2.png eng3.png \
  --model nano-banana-pro --filename "frame-team.png" --width 720 --height 1280

# === USER APPROVES ALL FRAMES ===

# === ANIMATE ===
uv run scripts/generate_video.py \
  --prompt "Chrome text emerges from darkness, dramatic light sweep, metallic shimmer" \
  --start-image "frame-title.png" --model seedance-2-fast \
  --filename "vid-title.mp4" --aspect-ratio 9:16

uv run scripts/generate_video.py \
  --prompt "CEO walks across stage, gestures to screen, audience applauds, lights shift" \
  --start-image "frame-keynote.png" --model seedance-2-fast \
  --filename "vid-keynote.mp4" --aspect-ratio 9:16

uv run scripts/generate_video.py \
  --prompt "Product slowly rotates, light catches edges, dramatic reveal" \
  --start-image "frame-product.png" --model seedance-2-fast \
  --filename "vid-product.mp4" --aspect-ratio 9:16

uv run scripts/generate_video.py \
  --prompt "Team walks forward in unison, golden light shifts, confident slow motion" \
  --start-image "frame-team.png" --model seedance-2-fast \
  --filename "vid-team.mp4" --aspect-ratio 9:16

# === POST-PRODUCTION ===

# Normalize all clips
for f in vid-*.mp4; do
  ffmpeg -y -i "$f" \
    -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
    -c:v libx264 -preset fast -crf 18 -r 24 -an "${f%.mp4}-norm.mp4"
done

# Trim title card
ffmpeg -y -i vid-title-norm.mp4 -t 2.0 -c:v copy vid-title-trim.mp4

# Concat
cat > concat.txt << 'EOF'
file 'vid-title-trim.mp4'
file 'vid-keynote-norm.mp4'
file 'vid-product-norm.mp4'
file 'vid-team-norm.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i concat.txt -an -c:v copy muted.mp4

# Add music
VID_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 muted.mp4)
FADE_START=$(python3 -c "print(float('${VID_DUR}') - 2)")
ffmpeg -y -i muted.mp4 -i soundtrack.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -af "atrim=0:${VID_DUR},afade=t=out:st=${FADE_START}:d=2" \
  -map 0:v:0 -map 1:a:0 final.mp4
```
