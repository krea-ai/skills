# Narrative Video Long

## Trigger

User asks for a video longer than 15 seconds, a multi-scene story, montage, launch reel, explainer, music video, event recap, or a piece with intentional hard cuts. When in doubt between this workflow and `social-video-short.md`, pick this if the user needs separate scenes with different locations, subjects, or title cards.

## Concept shotgun (thin briefs only)

If the user's brief is thin on *creative* content — no named hero, no setting list, no story beats (e.g. "1-minute video, a hero fights across different planets") — do not Clarify first. Propose **3 distinct concept variants** in a single batched message, each one a one-line pitch plus the implied 6–8 scene list. Move on meaningful axes: tone (somber / kinetic / playful), setting palette (lush / industrial / alien), hero archetype (ronin / engineer / drifter). Let the user pick or remix.

If the brief is thin only on *logistical* fields (aspect, runtime, audio, refs), skip the shotgun and go to Clarify. If rich on both, skip both and go to Recipe.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Runtime**: target total duration and per-scene length.
- **Aspect**: 9:16, 16:9, 1:1, or platform-specific.
- **Scene list**: 4-8 scenes, each with subject/action/location.
- **References**: faces, products, brand, locations, music.
- **Audio**: silent, music bed, generated audio, or user-supplied track.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. **Cost-preflight** (mandatory - see `../references/cost-preflight.md`). Estimate number of still frames, number of video clips, and total wall-clock. Initialize the session CU tracker — see `../references/budget-tracking.md`.
2. **Asset sheet (mandatory for narrative).** Before any scene composition, generate in one parallel batch:
   - **Character turnaround** per protagonist — front / three-quarter / action pose. One sheet or three separate refs.
   - **Prop sheet** for any recurring hero items (weapons, devices, signature accessories) on a neutral studio backdrop.
   - **Location plate** per distinct scene location, no characters.

   Show the sheet, wait for approval, regenerate any drifting elements before composing scenes. Asset-sheet stills are cheap (~17-35 CU each on `krea/krea-2/large` or `google/imagen-4-ultra`); the parallel batch finishes in ~30-60s. Skipping this step is the single biggest cause of character drift across a long video — every scene re-rolls the hero from text alone, and the spirit-creature / mask / hair-color drifts that look catastrophic on the assembled cut originate here.
3. Plan a shot list. Include title cards, scene order, aspect, duration, and per-scene refs (which turnaround / prop / location plate each scene consumes).
4. Resolve live archetypes: `high-fidelity image` or `image-to-image / face reference` for frames, `text in image` for titles, and `image-to-video / start frame anchored` for clips. If the resolved video model is a `seedance-2` variant, load `../references/models/seedance-2.md` for engine-specific prompt structure, archetypes, cut rules, the positional-travel rule for combat, and banned phrases.
5. **Scene-by-scene chain** (this is the cohesion gate; do not batch). For each scene N from 1 to M:
   a. Compose scene N still — 1-2 variations, image-to-image with the relevant character turnaround + location plate + prop sheet as references. Show, wait for approval.
   b. Plan scene N's **end frame** as the visual anchor for scene N+1's start. Either generate it as a separate still and approve, or note "same as scene N+1 start" if the cut is a hard match.
   c. Submit the image-to-video job with `startImage=<approved still>`, `endImage=<scene N+1 start or planned end>`, `referenceImages=[<character turnaround + prop>]`, `generateAudio=true`, `resolution=720p`, `aspectRatio=<target>`. Use `-i field=value` raw input — named CLI flags drop most of these fields silently (see `../references/cli-or-mcp.md`).
   d. Show the resulting clip. Approve or re-roll with adjusted motion prompt.
   e. Use scene N's `endImage` (or extract the last frame of the resulting clip) as scene N+1's `startImage`. This is the continuity hook that makes the assembled cut read as one piece rather than random concat.

   Surface the running CU spend after each clip; warn early if approaching the session budget.
6. After the final scene clip is approved, normalize every clip to identical resolution, FPS, codec, SAR, and strip per-clip audio.
7. Concatenate with ffmpeg. Add one cohesive audio track at the end if requested.
8. Sample frames across the final edit and read with vision before delivery.
9. **Deliver** with final file path/URL, scene count, runtime, asset-sheet references, and QA notes.

### CLI

Lead with the `-i` raw-input pattern for video — the named flags cover only `--start-image`, `--duration`, `--aspect`, `--prompt` and silently drop `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`. See `../references/cli-or-mcp.md` for the full syntax.

```bash
# Asset sheet — parallel batch
krea generate image -m "krea/krea-2/large" --aspect 1:1 \
  -p "character turnaround sheet, hero front / three-quarter / action pose, single sheet, neutral studio gray, cel shaded anime style" \
  --wait -o ./asset-hero-turnaround.png &
krea generate image -m "krea/krea-2/large" --aspect 16:9 \
  -p "location plate, neon ruined street at night, no characters, anime BG plate" \
  --wait -o ./asset-loc-01.png &
wait

HERO=$(krea upload ./asset-hero-turnaround.png --json | jq -r .url)
LOC=$(krea upload ./asset-loc-01.png --json | jq -r .url)

# Scene N still — image-to-image with asset references
krea generate image -m "google/nano-banana-pro" --aspect 16:9 \
  -i "referenceImages=[\"$HERO\",\"$LOC\"]" \
  -p "scene 1 still — hero standing in the ruined street, low-angle wide" \
  --wait -o ./scene-01-still.png

START=$(krea upload ./scene-01-still.png --json | jq -r .url)
END=$(krea upload ./scene-02-still.png --json | jq -r .url)   # planned next-scene start, if available

# Scene N video — chain via endImage + character refs + audio
krea generate video -m "bytedance/seedance-2" \
  --start-image "$START" --duration 10 --aspect 16:9 \
  -i endImage="$END" \
  -i "referenceImages=[\"$HERO\"]" \
  -i generateAudio=true \
  -i resolution=720p \
  -p "<positional-travel prompt for scene 1>" \
  --json
```

### MCP fallback

```
list_models()
get_model_schema(model="<frame-model>")
generate_image(..., sync=true)
upload_asset(...)
get_model_schema(model="<image-to-video-model>")
generate_video(input={startImage, endImage, referenceImages, generateAudio: true, resolution: "720p", duration, aspectRatio, prompt}, sync=false)
get_job(jobId=<id>)  # poll all jobs with progress pings
```

## Banned

- Do not skip the asset sheet for narrative video. Without locked turnarounds, character / creature / prop drift across scenes is guaranteed.
- Do not batch all scene videos in parallel after still approval. Chain scene-by-scene with `endImage` so the user can steer continuity at the cheapest decision point.
- Do not animate unapproved frames.
- Do not submit all scenes before the user has seen the first frame.
- Do not concatenate clips without normalization.
- Do not keep random AI clip audio when assembling; strip and add one track.
- Do not rely on named CLI flags for Seedance 2.0; use `-i` for `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`.
- Do not call this workflow for a <=15s single social clip; use `social-video-short.md`.

## Cost & time

- Asset sheet: 3-6 stills × ~17-35 CU each, parallel batch, ~30-60s wall-clock.
- Per scene clip: each Seedance 2.0 clip is hundreds to 1500+ CU and 5-15 minutes.
- Typical full workflow: asset sheet + 6-8 chained scene stills + 6-8 chained scene clips; 40-100 minutes depending on approvals and queue.
- Sequential scene-by-scene chain is **not slower in wall-clock** for a 60s short — user decision time was already the bottleneck — and total CU is lower because failed scenes are caught immediately, not after all 6 have been rendered.
- Hard caps the user should know about: long stories are many short clips assembled with `endImage` continuity, not one huge continuous clip.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Hero/villain look different between scenes | No asset sheet, or turnaround not passed as `referenceImages` | Generate (or re-pass) the turnaround; resubmit clip with it in `referenceImages` |
| Cuts feel like random concat | Scenes animated without `endImage` chaining | Re-render scene N+1 with N's `endImage` (or last-frame extract) as its `startImage` |
| Scenes feel incoherent | No approved shot list | Re-plan and regenerate frames before animation |
| Action scene reads as "held pose" instead of motion | Prompt described attack *state*, not *trajectory* | See positional-travel rule in `../references/models/seedance-2.md` — name direction + distance + duration |
| Clip specs mismatch | Different model outputs | Normalize with ffmpeg before concat |
| Audio is chaotic | Per-clip generated audio kept | Strip audio and add one bed |
| User dislikes scene after animation | Approval happened too late | Revert to still-frame approval gate |
| 402 Payment Required mid-batch | Session CU exhausted | See `../references/budget-tracking.md` — surface running spend earlier; switch profile or top up |
