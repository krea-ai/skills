# Launch Teaser

## Trigger

User says "launch video", "brand film", "teaser", "hype video", "product reveal", "kinetic type video", "make it cinematic", or "make it ultracool", or asks for a website-hero or YouTube pre-launch video. Disambiguate from `social-video-short.md`: that workflow is creator-native, single-continuous-clip social content; this one is a designed multi-beat film with typography and music. When in doubt: if the video needs on-screen type, beat-synced cuts, or "premium/agency" energy, route here.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Aspect + placement**: 16:9 website hero/YouTube, 9:16 Reels, or 16:9 master plus vertical cut.
- **Duration**: ~15s teaser (default) or ~30s film.
- **Footage**: generate fresh cinematic shots (default), reuse existing campaign stills with motion treatment, or typography-only.
- **Sound**: music-driven (default), music plus VO, or silent-first.
- **Brand name + tagline** for the end card. Ask explicitly - a launch film wants a name reveal; if there is none, stay product-led.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order - the order IS the deliverable. The quality comes from separating AI footage from designed motion: video models generate raw, textless, cinematic material; ALL typography, cuts, flashes, HUD overlays, and beat sync are built deterministically in an HTML composition layer on top. That layer is the `hyperframes` skill; if it is not installed, install it first: `npx skills add heygen-com/hyperframes --skill hyperframes` and `npx skills add heygen-com/hyperframes --skill hyperframes-cli`.

1. **Lock the beat grid first.** Pick a rhythm template from the `hyperframes` skill's beat-direction patterns before generating anything; for 10-20s teasers default to SLAM-proof-SLAM-hold. Write down exact cut timestamps (for 15s, e.g. 3.0 / 6.2 / 7.4 / 10.8 / 13.0). Everything downstream serves these numbers.
2. **Pick a visual style** from the `hyperframes` skill's visual-styles presets - Shadow Cut for dark/dramatic, Maximalist Type for loud hype. The product's own aesthetic decides.
3. **Generate music against the beat grid** with the ElevenLabs Music API (`music` skill). Write the cut timestamps INTO the prompt as explicit musical events: "hard drop hit at exactly 3 seconds", "final massive impact at 13 seconds that rings out until the end". Without explicit timestamped hits the API returns rhythmless wallpaper. Verify duration with ffprobe - the API may return ~1s extra; the composition's `data-duration` crops it.
   - **ElevenLabs tier fallback**: free-tier keys get 402 `paid_plan_required` on `/v1/music`, but `/v1/sound-generation` usually works - a degraded fallback for short atmospheric beds. Validate keys with GET `/v1/user`; a 401 `missing_permissions` for `user_read` still allows generation endpoints, so test the actual endpoint before declaring a key dead.
4. **Build start-frame stills, image-to-image from the product reference** - never text-only; product fidelity dies. Resolve the still model from the marketing image set in `../SKILL.md`. One still per footage beat; 3 shots is plenty for 15s. Hard prompt rules: "no text, no logos" in every still and every video prompt. Cinematic vocabulary is ENCOURAGED here - this is the opposite of the UGC workflow's banned-words list; do not cross-contaminate.
5. **Animate each still into a 4-5s clip** via the start_image path on a cinematic video model resolved from live `list_models`. Cost-preflight before submitting video (`../../krea-generate/references/cost-preflight.md`). One steady camera move per shot - push-in, orbit, or pull-back; the composition handles all dynamism. Pacing guardrail still applies: never `slow`, `gentle`, `soft` - models literalize them into slo-mo; use `natural realtime`, `smooth`, `steady`. Footage only needs to be slightly longer than its slot; trimming is free in composition.
6. **Compose in HyperFrames.** Route to the `hyperframes` skill for all authoring rules; do not improvise composition syntax here. The composition must contain:
   - type scenes between/over footage on the locked beat timestamps;
   - punch-in cuts: each footage clip enters at 1.15-1.25x scale, snaps to 1.0 on the beat, then slow-creeps;
   - flash frames (1 white default; at most one colored accent, used once) and optional glitch/RGB-split bursts, HUD brackets, or scanlines per the chosen visual style;
   - end card: name/tagline reveal on the final hit, fade to black.
   - **Known trap**: video elements must NOT be nested inside timed divs - that violates the frozen-video contract. Wrap each video in a NON-timed div for scale/punch animations and put `data-start` on the video itself.
7. **Gate the render**: lint → validate → inspect → render via the hyperframes CLI. No skipped gates.
8. **Vision-QA rendered frames**: extract 4-6 frames with ffmpeg at the beat timestamps; check type legibility, clipping, safe areas, and product fidelity. Fix and re-render once.
9. **Deliver** with a beat-map summary - what happens at each timestamp. Offer the vertical cut.

### CLI path

When using CLI, verify the Krea surface with `../../krea-generate/references/cli-or-mcp.md`, discover current command syntax from the installed CLI help, and inspect live model schemas before submitting. Treat command shapes from memory as stale. The `hyperframes` skill owns all composition details. Skeleton:

```text
1. Upload the product reference to Krea; use the returned Krea-hosted URL.
2. Batch start-frame stills: marketing image model, image-to-image from the
   reference, one per footage beat, "no text, no logos" in every prompt.
3. One video job per shot: cinematic video model, start_image=<still>,
   4-5s, one steady camera move, natural realtime.
4. curl -X POST https://api.elevenlabs.io/v1/music with the cut timestamps
   written into the prompt as explicit hits; ffprobe the returned file.
5. Compose, then: npx hyperframes lint && npx hyperframes validate &&
   npx hyperframes inspect && npx hyperframes render -o final/<name>.mp4
```

## Banned

- Do not ask the video model to render typography, logos, UI text, or exact timing - it does so unreliably; composited type is pixel-perfect on every render.
- Do not generate music before cut timestamps are locked.
- Do not generate stills text-only when a product reference exists.
- Do not let UGC realism vocabulary (handheld, amateur, phone-framing) leak into this workflow.
- Do not skip the composition layer and deliver raw concatenated AI clips as a "launch film".

## Cost & time

- Per-job: ~3 stills + ~3 short video clips + 1 music track + 1 composition render.
- Each 4-5s video-model shot is roughly half the credit cost of one 15s UGC clip.
- Wall-clock is dominated by footage (~10 minutes) and the composition render (2-8 minutes).

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Music has no hits, rhythmless wallpaper | Prompt lacked explicit timestamped events | Re-prompt with harder timestamp language: name every cut, "hard drop hit at exactly Ns" |
| 402 `paid_plan_required` on `/v1/music` | Free-tier ElevenLabs key | Fall back to `/v1/sound-generation` for a short atmospheric bed, or ask for a paid key |
| Video frozen in render | Video element nested inside a timed div | Wrap the video in a non-timed div for punch animations; put `data-start` on the video itself |
| Type clipped or illegible | Safe areas violated | Safe-area margins >= 100px; captions >= 26px at 1080p; re-inspect before re-render |
| Product drifts in stills | Weak i2i preservation language | Strengthen preservation language: exact same product, materials, proportions; keep the reference image primary |
| Footage is slow motion | Banned pacing words in prompt | Rewrite with `natural realtime`, `smooth`, `steady` |
