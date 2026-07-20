# Cinematic Product Ad

## Trigger

User asks for a premium product commercial with no dialogue and no on-screen type: "cinematic product ad", "product film", "make it look like this ad" with a reference video, an ice/macro/studio treatment, "b-roll style ad", or an ingredient-story spot for food/CPG. Disambiguate from siblings: a designed film with typography, beat-synced cuts, and music routes to `launch-teaser.md`; anything creator-native routes to `social-video-short.md`; anything with a spoken script routes to `ugc-video-ad.md`. When in doubt: if the deliverable is clean product cinematography cut from multiple shots, route here.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Product reference**: a sharp, well-lit product shot where every word of the label is legible. This is a gate, not a nice-to-have — the start image is the quality ceiling (see Recipe step 2). Real printed packaging is welcome; it survives this pipeline.
- **Reference video**: does the user have an ad whose look/structure to replicate? If yes, get the file - the recipe measures it instead of guessing.
- **Scene concept**: ONE environment for the whole piece (ice + black glass, white marble, bright citrus splash, dark velvet...). The premium feel comes from scene consistency, not scene variety. Lean on the brand's own story when it has one (a "-196°C freeze crush" brand wants frost and shattering ice; a protein bar wants its ingredients).
- **Energy**: premium-calm (slow orbits, held beats) or ad-kinetic (fast cuts, action physics, hits on every cut). Default ad-kinetic for social placements.
- **Duration + aspect**: 12-15s default, 9:16 or 16:9.
- **End card**: none by default; minimal brand card only if asked.

## Recipe

Hard prescription. Follow in order. The primary path is ONE structured multi-shot timeline prompt on an audio-capable video model (live-verified on Seedance-2: fully-staged shots land as real cuts, not morphs). The stills-first pipeline (step 8) is the fallback and retake path.

1. **Measure the reference, if one exists.** Do not eyeball it. Detect cuts with `ffmpeg -i REF -filter:v "select='gt(scene,0.35)',showinfo" -f null -` and read the `pts_time` list; extract a frame at each cut plus midpoints; tile them into a contact sheet and inspect it with vision. Write down the structure as data: shot list, per-beat duration, and what alternates (verified reference pattern: product shots of 2-2.5s intercut with 1-1.5s ingredient cutaways, one consistent scene). Copy the structure, never the pixels or the other brand's assets.
2. **Gate the product image.** The start image is the quality ceiling — no prompt recovers a bad input. Verified back-to-back: a cropped video frame with a half-visible logo produced a garbled logo in every downstream generation regardless of prompt quality, while a clean retailer-grade shot of a text-dense bilingual can held every word crisp through six beats, including the last frame. Reject cropped video frames, blurry photos, and partial crops; if the user has none, generate a clean hero still first (marketing image model, i2i, preserve-packaging language) and vision-QA its text before any video spend.
3. **Lock one scene concept** and a palette. Every shot shares the same environment, lighting direction, and grade; only the subject of the beat changes (product / ingredient / texture / splash). Mixing scene concepts reads as a mood board, not a commercial - this is the verified failure that made an earlier cut feel scattered.
4. **Plan the beat sheet before writing the prompt.** 4-6 beats, every beat <=2.5s, alternating product beats with action/texture beats. Two verified pacing laws: (a) the model reliably commits to about 3 strongly distinct beats per generation on its own - more beats only land when each one is short and fully staged; (b) if any late beat is given 3s+ of hold, the back half coasts into one slow rotation and the ad dies (verified failure at 15s). If a shot needs to breathe longer, split it with a cutaway instead.
5. **Write the timeline prompt with this architecture.** Length must come from structure - more staged shots - never from stacking adjectives on one shot (50-90 words for a single-motion clip; ~250-400 for a staged multi-shot timeline). Describe motion as verbs with physical consequences ("frost races across the surface", "a rim of light travels along the top edge", "shards burst toward camera"), never static image-model adjectives ("cinematic", "beautiful", "4K"). Skeleton, every section load-bearing:

   ```text
   Format: <energy> product video ad, <N> fast cuts in one take, <duration>s,
     <aspect>, <look/grade>.
   References: @Image1 as the first frame and hero product — <name it>; keep
     <list every logo and printed line worth protecting> exactly as shown,
     do not warp or re-letter any text.
   Consistent world across all shots: <one scene concept, palette, light>.
   Motion split: <what moves with real physical weight at realtime speed>;
     camera moves are <fast, snappy | slow, deliberate>, never slow-motion,
     never floating.
   SHOT 1 — <NAME> (0–2.5s), <shot size>, <lens>. <One camera move + one
     physical event with consequences>. <Named transition>.
   SHOT 2 — ... (each beat: time range, shot size, lens, one move, one event)
   ...
   Audio: <beat/energy> with a hard hit on every cut; <per-shot diegetic SFX
     list>. No voiceover.
   Constraints (reassert): <N> hard cuts, not morphs; no long static holds,
     keep cutting; one consistent world; <product/logo/text> locked exactly
     as @Image1; realtime motion; no on-screen text, no captions, no added
     graphics, no 3D, no cartoon, no distorted or re-lettered text.
   ```

   The `@Image1` role must be stated inline in the prompt AND the file passed through the schema `start_image` field - the model does not reliably infer an asset's role from the attachment alone. The constraints tail is not decoration: long prompts decay over the generation, and the tail is what keeps the last beats from drifting back to defaults.
6. **Cost-preflight, then submit** (`../../krea-generate/references/cost-preflight.md`): audio-capable video model resolved from live `list_models` (Seedance-2 rules in `../../krea-generate/references/models/seedance-2.md`), `start_image` = the gated product shot, 12-15s, native audio on. Output is stochastic - budget best-of-2 or 3 seeds for a hero deliverable and pick the strongest.
7. **QA the timeline, not just frames.** Run scene detection on the OUTPUT (`gt(scene,0.3)`) and check that cuts registered near the planned boundaries - detected cuts mean real cuts; an empty list means the shots morphed. Tile 8-11 frames across the full duration into a contact sheet and vision-inspect: label text legible on the first AND last hero beats (drift is progressive), one consistent world, no beat holding past ~2.5s, back half still moving.
8. **Fallback and retake path: stills-first.** When one beat needs a surgical retake, when label text must survive extreme scene-changing motion, or when the one-shot keeps morphing its cuts: generate that shot as a vision-QA'd still (marketing image model, i2i from the product reference, preserve-packaging language), animate it with ONE camera-only move and freeze language ("Nothing else changes: the product stays exactly as shown, completely static except for the camera"), QA the last frame, and cut it into the timeline with ffmpeg. Verified: dense printed packaging stays fully legible through a full orbit under camera-only motion. Cutaway stills (ingredients, textures) may be text-only prompts - no product in frame, same lighting/background family.
9. **Assemble and deliver.** If post is needed: normalize clips to the delivery frame, trim to the beat sheet, concat with the demuxer, short fade in/out at the ends only. No burned captions, no typography overlays - this format is clean cinematography, and drawtext captions on it read cheap (verified user feedback). Deliver with the beat sheet and the prompt so the user can request per-beat retakes cheaply.

### Tool path

Use the available Krea tools: upload the gated product shot (`get_upload_url`) when needed, verify the video model schema live (`get_model_schema`) before submitting, then one `generate_video` job with the timeline prompt, `start_image`, duration, aspect, and native audio enabled per the live schema. Wait with the available job tool; congestion can stretch completions. Scene detection, frame extraction, contact sheets, trimming, and concat run locally with ffmpeg.

## Banned

- Do not guess a reference video's structure - measure it with scene detection and a contact sheet.
- Do not start from a cropped video frame, blurry photo, or partial crop of the product - the start image is the quality ceiling and a garbled input garbles every output.
- Do not stretch a single-shot prompt with adjectives to justify a longer duration - added length must be added staged shots.
- Do not write "HARD CUT" between shots that have no time range, shot size, lens, and named move - unstaged cuts render as morphs.
- Do not give any beat more than ~2.5s, and do not leave the final beats as one long hero hold - that is the verified back-half coasting failure.
- Do not mix scene concepts across shots; one environment, many beats.
- Do not burn captions or typography onto this format by default; route designed type to `launch-teaser.md`.
- Do not avoid real packaging text or ask the model to re-letter it; preserve it via the reference and lock it in the constraints tail.
- Do not animate a fallback still that has not passed vision QA, and do not deliver a clip whose last frame was not inspected.
- Do not copy a competitor reference's product, brand assets, or footage - structure only.

## Cost & time

- Primary path: ONE 12-15s video job (native audio) per seed; best-of-2/3 for hero deliverables. Comparable total credits to the 3-5 separate clips it replaces, with one submit and no assembly unless retaking.
- Fallback retakes: one still (cheap) + one 4s camera-only clip per retaken beat.
- Wall-clock: a 15s job typically lands in 3-6 minutes; provider congestion occasionally stretches jobs to 15-25 minutes and they still complete.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Back half coasts on one slow hero rotation | Too many beats requested and/or final beats given long holds - the model front-loads ~3 strong beats then idles | Re-balance: every beat <=2.5s, "no long static holds, keep cutting" in the constraints tail; or drop to 12s / fewer beats |
| Shot boundaries render as soft morphs, scene detection finds no cuts | Shots not fully staged - "HARD CUT" alone is not a cut | Give every SHOT a time range, shot size, lens, one move, and a named transition; reassert "hard cuts, not morphs" in the tail; if it persists, build the offending beats stills-first (step 8) |
| A destruction/action beat renders soft (shatter becomes a gentle drop) | The model softens violent physics verbs, especially near product identity | Escalate the physics language ("explodes", "bursts", "shards flying toward camera") and give the beat no product identity to protect - pure ingredient/texture; or generate that beat as its own clip |
| Logo or label garbled in EVERY generation | Dirty start image - quality ceiling, not a prompt problem | Re-gate step 2: get a clean product shot or generate + vision-QA a clean hero still, then re-run |
| Label text garbled or product detail redesigned mid-clip only | Scene-changing motion on an identity-carrying beat or missing lock language | Lock text in the constraints tail; move destructive motion to cutaway beats; for surgical fixes use the stills-first fallback with camera-only motion and freeze language (`launch-teaser.md` identity-drift row) |
| First scene drags / piece feels slow | Product beats too long, no content alternation | Trim product beats to ~2-2.5s and intercut ingredient/texture beats per the beat sheet |
| Piece reads as a mood board, not one commercial | Scene concepts mixed across shots | Rewrite the "Consistent world" block and regenerate; keep lighting direction and grade constant |
| Cutaway looks pasted from another ad | Cutaway lighting/background does not match the scene concept | Name the same background and light direction as the product scene in that SHOT block |
| Video jobs stuck in `processing` far past normal | Provider-side congestion (observed: 15-25 min completions, both flagship and fast tiers) | Keep polling before assuming failure; cancel + resubmit on the fast tier only past ~25 min |
| Reference structure unclear from scene detection | Soft transitions below threshold | Lower the scene threshold (0.15) and diff adjacent frames on the contact sheet manually |
