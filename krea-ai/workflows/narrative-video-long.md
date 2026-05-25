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
2. **Concept + storyboard (mandatory before any image generation).** Write three short docs in the project directory and get explicit user approval **at each gate** before composing a single frame:
   - **`CONCEPT.md`** — one-paragraph logline; **`## Story spine`** section with the six fields from `../references/story-spine.md` (PROTAGONIST, WANT, OBSTACLE, STAKES, TURN, NEW NORMAL); a `## Dialogue posture` line (lines per scene, language, or explicit justification if silent); a `## Final-5-seconds feeling` line (one concrete sentence on what the audience feels at fade-out); arc-curve summary; tone reference; visual palette; story motif; reference touchstones.

     **Approval gate 1 — story spine.** Surface CONCEPT.md and wait. Push once: "Can you say back the protagonist's want in your own words?" — if the user can articulate it, proceed; if not, the brief is not yet a story.

   - **`STORYBOARD.md`** — beat-by-beat doc, one section per scene. Each section names: (a) **function in the arc** (one sentence tying back to the story spine — which spine field does this scene advance?), (b) **beats** with local timecodes (`[0–3s]` etc.) describing on-screen action, (c) **dialogue** (verbatim, in original language — write the actual lines now; "TBD" is not acceptable; if silent, justify in CONCEPT.md), (d) **camera** behavior, (e) **lighting**, (f) **sound** intent, (g) **why this works** tying back to spine + arc.

   - **`SHOTLIST.md`** (mandatory; this is the file the previous workflow was missing). Explode every scene into **3–6 individual shots of 2–3s each** per `../references/shot-grammar.md`. A 60s narrative is 20–30 shots, not 6. For each shot write: `id`, `duration`, `frame` (WS/MS/CU/ECU/OTS/POV/INSERT/MACRO/LOW/HIGH/DUTCH/TWO-SHOT/RACK), `action` (one sentence with camera move), `subject`, `startImage` (keyframe file), `endImage` (next keyframe or "none"), `dialogue` (verbatim line if any), `sfx/foley`, `continuity hook` (match cut / hard cut / J-cut / L-cut). Plan at least 2–3 explicit match cuts across the 60s — name them in the continuity-hook field.

     **Approval gate 2 — shot list.** Surface STORYBOARD.md + SHOTLIST.md and wait. Until the user OKs the shot count and the dialogue lines verbatim, no keyframe generation.

   The 2026-05-21 Inkfall delivery shipped with one 10s clip per scene, no dialogue, and no match cuts — the user verdict was "transitions suck, story makes no sense, people don't speak." That outcome traces directly back to skipping the SHOTLIST.md and spine gates. Do not repeat it.

   A scene is a *story beat*, not a *time slot*. A shot is one camera setup. Most scenes are 3–6 shots.

3. **Asset sheet (mandatory for narrative).** Before any scene composition, generate in one parallel batch:
   - **Character turnaround** per protagonist — front / three-quarter / action pose. One sheet or three separate refs.
   - **Prop sheet** for any recurring hero items (weapons, devices, signature accessories) on a neutral studio backdrop.
   - **Location plate** per distinct scene location, no characters.

   When each still lands, **Read every file individually and run a critical vision pass per `../references/vision-qa.md`** — one observation per still, grade each (✓ / ✗), regenerate the weak ones before showing the user. Do not summarize a batch as "all four look great"; that is the failure mode that produces broken endImages and Seedance refusals downstream. Asset-sheet stills are cheap (~17-35 CU each on `google/imagen-4-ultra` or `google/nano-banana-pro` for the CLI/MCP path; `krea/krea-2/large` exists only via direct HTTP — see `../references/models/`); the parallel batch finishes in ~30-60s. Skipping this step is the single biggest cause of character drift across a long video — every scene re-rolls the hero from text alone, and the spirit-creature / mask / hair-color drifts that look catastrophic on the assembled cut originate here.
4. Resolve live archetypes: `high-fidelity image` or `image-to-image / face reference` for frames, `text in image` for titles, and `image-to-video / start frame anchored` for clips. If the resolved video model is a `seedance-2` variant, load `../references/models/seedance-2.md` for engine-specific prompt structure, archetypes, cut rules, the positional-travel rule for combat, and banned phrases.

5. **Compose one keyframe per shot, not per scene.** From SHOTLIST.md, each shot has a `startImage`. Generate every distinct keyframe (a shot whose startImage is "extracted from previous shot's last frame" does not need its own generation). Use image-to-image with the character turnaround + location plate + prop sheet as references. Run keyframe generation in parallel batches of 4–6.

   **Read every keyframe individually** per `../references/vision-qa.md` — grade each shot's keyframe ✓/✗ with one critique line, regenerate any ✗ before video generation. The cost of regenerating a still is seconds; the cost of a bad startImage propagating into a video clip is minutes plus the CU.

6. **Shot-by-shot video generation** (chain primitive operates at shot level, not scene level). For each shot `S{n}.{m}` in SHOTLIST.md:
   a. Submit the image-to-video job. **Seedance 2 rejects `endImage` and `referenceImages` in the same call (HTTP 422)** — pick one path:
      - **Chained shot (has a next shot, continuity hook is match / J-cut / L-cut)**: `startImage=<this shot's keyframe>`, `endImage=<next shot's keyframe>`, `generateAudio=true`, `resolution=720p`, `aspectRatio=<target>`. **Omit `referenceImages`.**
      - **Terminal shot (hard cut to next, or last in cut)**: `startImage=<this shot's keyframe>`, `referenceImages=[<turnaround + prop>]`, `generateAudio=true`, `resolution=720p`, `aspectRatio=<target>`. **Omit `endImage`.**
      - **For Seedance: native audio is the default audio path.** Include each shot's dialogue and SFX/foley directly in the prompt's `Audio:` block (per `../references/models/seedance-2.md` prompt structure). Seedance renders lip-synced dialogue + ambient + score per-clip natively. Do NOT default to external TTS + ffmpeg mux — that's the fallback for video models without native audio (Kling, etc.). The external mux pattern in step 7-8 below applies only when the chosen video model returns silent video.
      - **Duration**: Seedance-2 minimum is **4 seconds** (per `../references/models/seedance-2.md`). Shot-grammar shots are typically 2-3s. **Always submit `duration=4` and trim down in ffmpeg at step 8.** Do not pass duration<4 — the job fails with a schema error.

      Use `-i field=value` raw input — named CLI flags drop most fields silently (see `../references/cli-or-mcp.md`).
   b. **Chain-from-last-frame for in-scene continuity** (per `../references/models/seedance-2.md` "Chain-from-last-frame"). Within a scene, shots are SERIAL: submit shot N+1 only after shot N has completed, then extract shot N's actual last frame with `ffmpeg -sseof -0.1 -i shot-N-raw.mp4 -frames:v 1` and use that as shot N+1's `startImage` (overriding the pre-planned keyframe). This carries motion, lighting, costume, and expression smoothly into the next shot. Across scenes (hard scene boundaries), keep the pre-planned keyframe and fire in parallel. Net effect: serial within ~3-5 shots of a scene, parallel between scenes, **respecting the 12-concurrent-job cap** on Seedance-2 videoV2 (HTTP 429 `CONCURRENCY_LIMIT_REACHED` on the 13th).

   If you skip the chain-from-last-frame step, every clip will start cold from a freshly-rendered still and the assembled cut will feel like a slideshow of independent clips. This is the single biggest difference between a 1/10 narrative and a 7/10 narrative.

   **Shadow-fail detection (mandatory)**: a Seedance-2 job can return `status:"completed"` with `result:{}` empty — that is a silent content-filter refusal, not a successful render. Treat any completed job with no `result.urls[]` as a refusal. Retry once with a sanitized prompt (drop proper nouns and role descriptors per `../references/models/seedance-2.md` "Content-filter shadow-fail"); if still empty, drop `endImage` and retry with `startImage` only; if still empty, mark the shot and continue.
   c. As each clip lands, sample its mid and end frame with ffmpeg, Read both, write a ✓/✗ critique. Re-roll weak shots immediately — do not assemble around a known-bad shot hoping the cut will hide it. It won't.

   Surface running CU spend after each batch.

7. **Audio strategy — branch by model.**
   - **If using Seedance-2 (native audio)**: nothing extra to do in this step. Per shot in step 6, you already included dialogue + SFX/foley in the prompt's `Audio:` block; Seedance renders it natively (lip-sync, ambient, score). Keep Seedance's per-clip audio when normalizing in step 8 — do NOT strip. Optionally add a thin continuous music bed under the whole assembly to bridge cuts (see `../references/dialogue-and-audio.md` "thin overlay bed pattern"), but the per-clip native audio is the primary track.
   - **If using a silent-video model (Kling, etc.)**: run the external-mux pipeline per `../references/dialogue-and-audio.md`:
     a. Generate the continuous music/ambient bed via the chosen audio model (`list_models` for audio/voice; prefer Krea if available, else ElevenLabs, else stock).
     b. Generate one TTS file per dialogue line in SHOTLIST.md.
     c. Listen to every file before assembly; re-generate any that sounds wrong.

8. **Assemble.** **Trim each raw clip to its SHOTLIST.md duration first** (Seedance was submitted at duration=4 per the 4s minimum — your 2.5s shot needs `ffmpeg -i raw.mp4 -t 2.5 -c:v libx264 -c:a aac -b:a 192k trim.mp4`). Then normalize every trimmed clip to identical resolution, FPS, codec, SAR.
   - **Seedance path (native audio)**: KEEP per-clip audio through trim and normalize. Concatenate with `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4` so both video and audio carry through. Optionally overlay a thin continuous music bed underneath (see "thin overlay bed pattern" in `../references/dialogue-and-audio.md`).
   - **Silent-video-model path**: strip per-clip audio (`-an`), concat video-only, then mux the external bed + TTS lines per `../references/dialogue-and-audio.md` in a single ffmpeg invocation:
   - Input 0: video-only concat
   - Input 1: ambient bed (full duration, `volume=0.35`)
   - Inputs 2..N: dialogue TTS lines, each positioned with `adelay=<ms>|<ms>` at its shot's start timestamp
   - Filter graph: `amix=inputs=N:duration=longest:normalize=0`
   - `-c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2`

   If subtitles are needed for non-English dialogue, burn them in with `subtitles=subs.srt` at the configured style.

9. **Final QA**. Sample frames across the assembled cut (every ~2s) and Read each per `../references/vision-qa.md` "Video frame sampling". Sample audio at each dialogue timestamp (`ffmpeg -ss <t> -t 2 -vn`) and listen — confirm dialogue sits above bed, no clipping, no late landing. Catch identity drift, unplanned hard cuts, color-temperature jumps, dialogue-audio mismatch.

10. **Deliver** with final file path/URL, shot count (not scene count), runtime, total CU spent, asset-sheet references, and QA notes including which match cuts landed and which didn't.

### CLI

Lead with the `-i` raw-input pattern for video — the named flags cover only `--start-image`, `--duration`, `--aspect`, `--prompt` and silently drop `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`. See `../references/cli-or-mcp.md` for the full syntax.

```bash
# Asset sheet — parallel batch
krea generate image -m "google/imagen-4-ultra" --aspect 1:1 \
  -p "character turnaround sheet, hero front / three-quarter / action pose, single sheet, neutral studio gray, cel shaded anime style" \
  --wait -o ./asset-hero-turnaround.png &
krea generate image -m "google/imagen-4-ultra" --aspect 16:9 \
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

- Do not skip `CONCEPT.md` + `STORYBOARD.md` + `SHOTLIST.md`. The three approval gates (story spine → storyboard → shot list) are the cheapest course-correction points in the pipeline. Skipping any of them produces footage the user has to articulate fixes for in pixels — at orders of magnitude more cost than re-writing a sentence.
- Do not plan one continuous 10s clip per scene. A scene is 3–6 shots of 2–3s each. The 2026-05-21 Inkfall delivery shipped 6 one-shot scenes; the user verdict was "transitions suck, story makes no sense." Cinema cuts inside scenes. See `../references/shot-grammar.md`.
- Do not generate a narrative >15s with dialogue listed in SHOTLIST.md but no dialogue in the final cut. Either render the dialogue via TTS and mux it (see `../references/dialogue-and-audio.md`) or rewrite the storyboard to be deliberately silent with `## Dialogue posture` documented in CONCEPT.md.
- Do not ship without at least 2–3 explicit match cuts named in SHOTLIST.md continuity-hook fields. Random hard cuts read as "footage stapled together."
- Do not skip the asset sheet. Without locked turnarounds, character / creature / prop drift across shots is guaranteed.
- Do not animate unapproved keyframes.
- Do not concatenate clips without normalization.
- Do not keep random AI per-clip audio when assembling; strip and replace with the bed + dialogue mux.
- Do not rely on named CLI flags for Seedance 2.0; use `-i` for `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`.
- Do not pass `endImage` and `referenceImages` in the same Seedance 2 call — the API returns HTTP 422. Pick one per shot (chained → endImage; terminal/hard-cut → referenceImages).
- Do not call this workflow for a <=15s single social clip; use `social-video-short.md`.

## Cost & time

A 60s narrative under this workflow is **20–30 shots of 2–3s each**, not 6 × 10s. Cost scales accordingly — surface this honestly in cost-preflight.

- Asset sheet: 3-6 stills × ~17-35 CU each, parallel batch, ~30-60s wall-clock.
- Per-shot keyframes: 20–30 × ~60 CU on `google/nano-banana-pro` 1K with reference images = **~1.2–1.8k CU**. Parallel in batches of 4–6.
- Per-shot video: Seedance 2.0 at 720p / 2–3s. **Per-shot CU is lower than per-scene** because duration is shorter, but the count is higher. Estimate **~600–900 CU per 2–3s clip** (verify with `get_model_schema` cost endpoint; rates change). 20–30 shots = **~12–27k CU**. Wall-clock 5–15 min per shot; jobs are independent so the bottleneck is parallel-batch size, not chain order.
- Audio: 1 ambient bed (~500 CU on Krea audio, or external) + 4–8 TTS dialogue lines (~50 CU each on Krea voice, or ElevenLabs cost). ~1k CU total.
- **Typical full workflow**: asset sheet (~150 CU) + 20–30 keyframes (~1.5k CU) + 20–30 video shots (~15–25k CU) + audio (~1k CU) = **~17–28k CU end-to-end for a 60s narrative video** with dialogue at 720p. 60–120 minutes wall-clock depending on approvals and queue.
- The cost honesty conversation: this is 2–3× the old 6-scene budget. The old plan produced a slideshow. The right comparison is "this costs more *and* produces actual cinema" vs. "the old plan was cheap *and* unwatchable." Surface this at cost-preflight and let the user choose.

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
