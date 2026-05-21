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
2. **Concept + storyboard (mandatory before any image generation).** Write two short docs in the project directory and get explicit user approval on both before composing a single frame:
   - **`CONCEPT.md`** — one-paragraph logline; arc-curve summary (set-up → conflict → escalation → climax → resolution); tone reference; visual palette; story motif (the recurring object / gesture / image the fight is *actually* about — e.g. a hat, a watch, a name); reference touchstones.
   - **`STORYBOARD.md`** — beat-by-beat doc, one section per scene. Each section names: (a) **function in the arc** (one sentence — what this scene does for the story), (b) **beats** with local timecodes (`[0–3s]` etc.) describing on-screen action, (c) **dialogue** (verbatim, in original language — keep it sparse, 0–2 lines per scene), (d) **camera** behavior (push-in, orbit, smash-cut etc.), (e) **lighting** changes within the scene, (f) **sound** intent (silence beats matter as much as cues), and (g) one-line **why this works** rationale tying it back to the arc curve. Close with a production-notes section: asset map per scene, model assignment, continuity primitives, approval gates.

   Surface both docs in chat and **wait for the user to approve** before moving on. This is the cheapest course-correction point in the whole pipeline — once a frame is composed against a vague brief, every later iteration just renders the same incoherence at higher resolution. The skill author's 2026-05-21 live session burned six failed scene-2 video re-rolls because the underlying brief was "Gear-3 vs Boro-Breath collision" instead of "the beat after Luffy says his line." Don't repeat that.

   A scene is a *story beat*, not a *time slot*. If you can't write one sentence on what this scene does for the arc, the scene shouldn't exist.

3. **Asset sheet (mandatory for narrative).** Before any scene composition, generate in one parallel batch:
   - **Character turnaround** per protagonist — front / three-quarter / action pose. One sheet or three separate refs.
   - **Prop sheet** for any recurring hero items (weapons, devices, signature accessories) on a neutral studio backdrop.
   - **Location plate** per distinct scene location, no characters.

   Show the sheet, wait for approval, regenerate any drifting elements before composing scenes. Asset-sheet stills are cheap (~17-35 CU each on `krea/krea-2/large` or `google/imagen-4-ultra`); the parallel batch finishes in ~30-60s. Skipping this step is the single biggest cause of character drift across a long video — every scene re-rolls the hero from text alone, and the spirit-creature / mask / hair-color drifts that look catastrophic on the assembled cut originate here.
4. Plan a shot list. Include title cards, scene order, aspect, duration, and per-scene refs (which turnaround / prop / location plate each scene consumes). The shot list is the table that maps STORYBOARD.md beats to concrete model calls; it should not introduce new beats not in the storyboard.
5. Resolve live archetypes: `high-fidelity image` or `image-to-image / face reference` for frames, `text in image` for titles, and `image-to-video / start frame anchored` for clips. If the resolved video model is a `seedance-2` variant, load `../references/models/seedance-2.md` for engine-specific prompt structure, archetypes, cut rules, the positional-travel rule for combat, and banned phrases.
6. **Scene-by-scene chain** (this is the cohesion gate; do not batch). For each scene N from 1 to M:
   a. Compose scene N still — 1-2 variations, image-to-image with the relevant character turnaround + location plate + prop sheet as references. The prompt for this still is the STORYBOARD.md beat for scene N, not a freshly imagined description. Show, wait for approval.
   b. Plan scene N's **end frame** as the visual anchor for scene N+1's start. Either generate it as a separate still and approve, or note "same as scene N+1 start" if the cut is a hard match.
   c. Submit the image-to-video job. **Seedance 2 rejects `endImage` and `referenceImages` in the same call (HTTP 422)** — pick one path:
      - **Chained scenes (have a next scene)**: `startImage=<approved still>`, `endImage=<scene N+1 still>`, `generateAudio=true`, `resolution=720p`, `aspectRatio=<target>`. **Omit `referenceImages`.** Identity rides forward because scene N+1's `startImage` is the still you composed with the asset-sheet refs at step 6a — the identity lock happens at still-compose time, not at video time.
      - **Terminal scene (last in the chain)**: `startImage=<approved still>`, `referenceImages=[<character turnaround + prop>]`, `generateAudio=true`, `resolution=720p`, `aspectRatio=<target>`. **Omit `endImage`.** Reference images reinforce fine character details (signature mask elements, costume hardware) that the still-compose pass may have softened.

      Use `-i field=value` raw input — named CLI flags drop most of these fields silently (see `../references/cli-or-mcp.md`).
   d. Show the resulting clip. Approve or re-roll with adjusted motion prompt.
   e. Use scene N's `endImage` (or extract the last frame of the resulting clip) as scene N+1's `startImage`. This is the continuity hook that makes the assembled cut read as one piece rather than random concat.

   Surface the running CU spend after each clip; warn early if approaching the session budget.
7. After the final scene clip is approved, normalize every clip to identical resolution, FPS, codec, SAR, and strip per-clip audio.
8. Concatenate with ffmpeg. Add one cohesive audio track at the end if requested.
9. Sample frames across the final edit and read with vision before delivery.
10. **Deliver** with final file path/URL, scene count, runtime, asset-sheet references, and QA notes.

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
# NOTE: field name is per-model. nano-banana-pro uses `imageUrls`; seedance-2 uses `referenceImages`.
# Run `krea models show <id> --json` and read the schema before guessing.
krea generate image -m "google/nano-banana-pro" --aspect 16:9 \
  -i "imageUrls=[\"$HERO\",\"$LOC\"]" \
  -p "scene 1 still — hero standing in the ruined street, low-angle wide" \
  --wait -o ./scene-01-still.png

START=$(krea upload ./scene-01-still.png --json | jq -r .url)
END=$(krea upload ./scene-02-still.png --json | jq -r .url)   # planned next-scene start

# Scene N (chained) video — endImage chain. Do NOT pass referenceImages (HTTP 422).
krea generate video -m "bytedance/seedance-2" \
  --start-image "$START" --duration 10 --aspect 16:9 \
  -i endImage="$END" \
  -i generateAudio=true \
  -i resolution=720p \
  -p "<positional-travel prompt for scene N>" \
  --json

# Terminal scene (last in the chain) — referenceImages for fine-detail anchor. No endImage.
krea generate video -m "bytedance/seedance-2" \
  --start-image "$FINAL_START" --duration 10 --aspect 16:9 \
  -i "referenceImages=[\"$HERO\",\"$PROP\"]" \
  -i generateAudio=true \
  -i resolution=720p \
  -p "<positional-travel prompt for terminal scene>" \
  --json
```

### MCP fallback

```
list_models()
get_model_schema(model="<frame-model>")
generate_image(..., sync=true)
upload_asset(...)
get_model_schema(model="<image-to-video-model>")
# Chained scene — endImage only, no referenceImages:
generate_video(input={startImage, endImage, generateAudio: true, resolution: "720p", duration, aspectRatio, prompt}, sync=false)
# Terminal scene — referenceImages only, no endImage:
generate_video(input={startImage, referenceImages, generateAudio: true, resolution: "720p", duration, aspectRatio, prompt}, sync=false)
get_job(jobId=<id>)  # poll all jobs with progress pings
```

## Banned

- Do not skip `CONCEPT.md` + `STORYBOARD.md`. Composing keyframes against a vague verbal brief produces incoherent scenes that the user can't articulate fixes for, which forces expensive re-rolls at the video step. The 60-second skill author session on 2026-05-21 burned six failed scene-2 video re-rolls because of this exact omission.
- Do not skip the asset sheet for narrative video. Without locked turnarounds, character / creature / prop drift across scenes is guaranteed.
- Do not batch all scene videos in parallel after still approval. Chain scene-by-scene with `endImage` so the user can steer continuity at the cheapest decision point.
- Do not animate unapproved frames.
- Do not submit all scenes before the user has seen the first frame.
- Do not concatenate clips without normalization.
- Do not keep random AI clip audio when assembling; strip and add one track.
- Do not rely on named CLI flags for Seedance 2.0; use `-i` for `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`.
- Do not pass `endImage` and `referenceImages` in the same Seedance 2 call — the API returns HTTP 422. Pick one per scene (chained → endImage; terminal → referenceImages).
- Do not call this workflow for a <=15s single social clip; use `social-video-short.md`.

## Cost & time

- Asset sheet: 3-6 stills × ~17-35 CU each, parallel batch, ~30-60s wall-clock.
- Scene stills: ~60 CU each on `google/nano-banana-pro` 1K with reference images.
- Per scene clip: Seedance 2.0 at 720p / 10s without video refs is **~1,738 CU per clip** (live billing, 2026-05-21). With video refs the rate is lower (~830 CU) but most chain workflows can't use video refs simultaneously with endImage. Wall-clock 5-15 min per clip; queue varies.
- Typical full workflow: asset sheet (~150 CU) + 6-8 chained scene stills (~400 CU) + 6-8 chained scene clips (~10-14k CU). Budget **~11-15k CU end-to-end for a 60-80s narrative video** at 720p with audio. 40-100 minutes wall-clock depending on approvals and queue.
- Sequential scene-by-scene chain is **not slower in wall-clock** for a 60s short — user decision time was already the bottleneck — and total CU is lower because failed scenes are caught immediately, not after all 6 have been rendered.
- Hard caps the user should know about: long stories are many short clips assembled with `endImage` continuity, not one huge continuous clip.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Hero/villain look different between scenes | No asset sheet, or turnaround not passed as refs at the still-compose step | Re-compose the failing scene's still with the turnaround as refs (image-to-image). Identity locks at still-compose time, not video time — chained clips ride on the still |
| HTTP 422 "Seedance 2 does not support mixing end frames with reference images" | Passed `endImage` and `referenceImages` together | Pick one. Chained scenes drop `referenceImages`; terminal scenes drop `endImage` |
| Fine character details soften across clips (signature mask elements, costume hardware) | Identity rides via composed still only; video model rerolls fine detail | Acceptable on chained clips. For the terminal scene, switch to `referenceImages` path to reinforce details |
| Cuts feel like random concat | Scenes animated without `endImage` chaining | Re-render scene N+1 with N's `endImage` (or last-frame extract) as its `startImage` |
| Scenes feel incoherent | No approved shot list | Re-plan and regenerate frames before animation |
| Action scene reads as "held pose" instead of motion | Prompt described attack *state*, not *trajectory* | See positional-travel rule in `../references/models/seedance-2.md` — name direction + distance + duration |
| Clip specs mismatch | Different model outputs | Normalize with ffmpeg before concat |
| Audio is chaotic | Per-clip generated audio kept | Strip audio and add one bed |
| User dislikes scene after animation | Approval happened too late | Revert to still-frame approval gate |
| 402 Payment Required mid-batch | Session CU exhausted | See `../references/budget-tracking.md` — surface running spend earlier; switch profile or top up |
