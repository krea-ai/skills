# Social Video Short

## Trigger

User says "make a short video", "TikTok", "Reels", "Shorts", "GRWM", "UGC", "Ori-style video", "social ad", or asks for a vertical/square clip of 15 seconds or less. Pick this if the target is one continuous social-native piece rather than many hard cuts. If the piece needs a written SPOKEN script, burned captions, a CTA card, or a multi-take talking head, route to `ugc-video-ad.md` - that workflow owns scripted UGC ads. Requests for designed launch films, brand teasers, or kinetic-type videos route to `launch-teaser.md` - UGC realism rules do not apply there.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Aspect**: 9:16 TikTok/Reels/Shorts, 1:1 feed, or 16:9.
- **Duration**: 5, 10, or 15 seconds.
- **Concept and beats**: one-line concept plus 4-6 actions that must happen.
- **Identity refs**: face, product, brand, outfit, mascot, or none.
- **Ad anatomy**: for ads/UGC, mode, hook, setting, talent/identity, product proof, CTA, and reference path.
- **Style**: palette, setting, mood, reference videos, text overlays.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. **Cost-preflight** (mandatory before video - see `../../krea-generate/references/cost-preflight.md`). Default estimate for 15s Seedance-2 720p is ~1564 CU and 10-15 minutes. Show estimate, get yes.
2. For ad/UGC work, load `../references/marketing-creative-anatomy.md` and lock the tuple before storyboarding. For UGC, also load `../references/ugc-social-video.md`. For ad work, offer a format from `../references/video-ad-formats.md` (sensory, spectacle, two-state, and product-led families route here) and structure the storyboard on its device; the format's Seedance-native template seeds the timeline prompt in step 9.
3. Resolve the storyboard image model from the marketing image set in `../SKILL.md`; prefer `openai/gpt-image-2` for storyboard sheets when live discovery confirms it and the schema fits. Resolve the animation model separately from live `list_models` as a cinematic video model; do not use a remembered video default. If the resolved video model is a `seedance-2` variant, load `../../krea-generate/references/models/seedance-2.md` for prompt structure, reference roles, media-path rules, failure recovery, and pacing guardrails.
4. Build one editorial storyboard sheet, not separate panels. Use 4-8 cells for 5-10s; 16-32 cells for dense 15s micro-beats. Use tiny panel numbers and short action labels; no technical fiches. For UGC, use the six-panel UGC template from `../references/ugc-social-video.md`.
5. Decide whether the brief is locked or loose. If locked, generate one storyboard. If loose, load `../references/storyboard-variations.md` and default to 3 parallel storyboard variants that vary on at least two axes.
6. Show storyboard variants together with `A/B/C` labels and one-line captions. Wait for an explicit user pick or merge request before animating. Iterate cheaply here before burning video credits.
7. Upload the chosen storyboard and any local/non-Krea refs to Krea. Use the returned Krea-hosted URLs in generation inputs.
8. Avoid the Seedance aspect trap (issue #11): do not pass a landscape start image for vertical output. If the storyboard sheet is landscape and final output must be 9:16, pad the sheet to portrait before upload or drop the sheet from `reference_images` and rely on face refs plus a detailed timeline prompt.
9. Compose a timestamped timeline prompt. Use `TIMELINE`, `STYLE`, `CAMERA`, `TRANSITIONS`, and `OUTPUT` sections. Strip the words `slow`, `gentle`, `soft`, and `slow motion`; use `smooth`, `steady`, `fluid`, or `natural realtime` instead.
10. Submit one video job async. Use `reference_images` for storyboard/refs, not per-panel concatenation.
11. Poll with `../../krea-generate/references/progress-reporting.md`: ping on status changes and every 25-35 seconds while unchanged.
12. Download, normalize to the requested delivery frame with ffmpeg, sample 4-6 frames, and vision-check continuity/identity before delivering.
13. **Deliver** with a one-line summary and QA notes.

### MCP path

Use the available Krea MCP tools to list models, inspect schema for both storyboard and video models, upload the approved storyboard, then call video generation with schema-verified prompt, reference, aspect, duration, and resolution fields. Poll with the available job-status tool and progress pings.

## Banned

- Do not submit video before storyboard approval - this is the #11 fix and the 2026-05-17 lesson. The storyboard gate is a creative gate and is not skipped by a session-level cost-preflight override.
- Do not generate panels separately and ffmpeg-concatenate - it creates stitched snippets, not a coherent social video.
- Do not pass a landscape start image into Seedance for vertical output - issue #11.
- Do not put a landscape storyboard first in `reference_images` for 9:16 unless padded to portrait - issue #11.
- Do not use `slow`, `gentle`, `soft`, or `slow motion` in prompts - Seedance often literalizes them.
- Do not rely on synchronous video generation waits; they can cap before the job finishes. Submit asynchronously, then poll through the available Krea surface.
- Do not use non-Krea-hosted refs as generation inputs - issue #7.
- Do not silently poll - issue #17; progress pings are mandatory.
- For UGC, do not use commercial-polish words or camera moves banned in `../references/ugc-social-video.md`.

## Cost & time

- Per-job: storyboard is cheap; Seedance-style 15s 720p video is ~1564 CU and 8-15 minutes.
- Typical full workflow: 1-3 storyboards plus 1 approved video job; ~10-20 minutes.
- Hard caps the user should know about: 15 seconds max for this workflow; face-reference likeness is moderate; storyboard aspect can bias video aspect.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Output horizontal despite `aspect_ratio="9:16"` | Landscape `start_image` or `reference_images[0]` bias, issue #11 | Drop start image; pad sheet to portrait; or use face refs plus timeline only |
| Output is slow motion | Prompt contained banned pacing words, issue #14 | Rewrite with natural realtime, smooth, steady, fluid |
| Video feels stitched | Per-panel generation was used, issue #15 | Use one storyboard sheet and one timeline-driven video job |
| Upload URL empty | Upload response missing a URL | Retry upload through MCP; if it still fails, stop and surface the asset error |
| Job times out | Sync generation wait cap | Submit async, then poll with MCP `get_job` |
| External URL rejected | Public API asset validation, issue #7 | Download the asset if needed, upload it to Krea, then use the returned Krea URL |
| Identity drifts | Face refs weak, issue #16 | Use 2-3 varied refs or route to `../../krea-generate/workflows/lora-train-and-use.md` |
| User lost trust during wait | Silent polling, issue #17 | Follow `../../krea-generate/references/progress-reporting.md` every 25-35 seconds |
| UGC looks like a brand commercial | Storyboard lacks creator-native realism cues | Load `../references/ugc-social-video.md`, rebuild the storyboard, and QA adversarially before animating |
