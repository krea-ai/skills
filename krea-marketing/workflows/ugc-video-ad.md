# UGC Video Ad

## Trigger

User asks for a scripted UGC ad: "UGC ad with a script", "talking-head ad", "testimonial ad", "creator ad", "founder-style ad", "make her say...", "narrated demo", "app demo ad", or any social video ad where someone SPEAKS lines, or that needs burned captions and a CTA card. Disambiguate from siblings: a continuous non-scripted social clip (GRWM, aesthetic b-roll, product-in-use vibe piece) stays in `social-video-short.md`; a designed launch film with typography and music routes to `launch-teaser.md`. When in doubt: if there is a written script to be spoken, route here.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Product + claims**: product reference (image/URL), required claims/copy, CTA destination.
- **Platform + aspect**: 9:16 TikTok/Reels/Shorts (default) or 1:1 feed.
- **Duration**: 15s default (the maximum allowed for this format; completion drops hard past 15s) — use 10s only if the user wants a tighter cut, longer only if the script demands it and the user accepts the completion tradeoff.
- **Talent**: text persona (one-off face), face reference image(s), or a reused campaign character/LoRA for consistency.
- **Structure**: pure talking head, or talking head intercut with demo/b-roll cutaways. For app/software demos, ask for real screen recordings.
- **Hook family**: let them pick from `../references/ugc-scripts.md` families or say "surprise me".
- **Captions**: yes/no, and style (bold-emphasis, flowing, minimal) - opt-in, but recommend them; most social video plays muted.

## Recipe

Hard prescription. Follow in order. The script gate and storyboard gate exist because words and panels are free; video jobs are not.

1. **Lock the tuple** from `../references/marketing-creative-anatomy.md` (mode = UGC review/testimonial/demo, hook, setting, talent, CTA). Load `../references/ugc-social-video.md` and `../references/ugc-scripts.md`.
2. **Script gate (blocking).** Write the spoken script with a hook family from `../references/ugc-scripts.md`. Enforce the 2-4 words/second law by word count (5s=10-20, 10s=20-40, 15s=30-60) before anything is generated. Hook in the first 1-3 seconds, one CTA at the end. Run the compliance check: no personal-attribute "your X" phrasing, no unsupported claims. Show the script (plus overlay-text hook if any) and get an explicit yes. Iterate here freely.
3. **Product evidence.** Inspect product references with vision before prompt writing; the attached reference, not prompt words, carries product facts. Keep product descriptors out of generation prompts and in the QA checklist.
4. **Storyboard.** Build one six-panel UGC storyboard sheet per `../references/ugc-social-video.md`, applying the realism rubric (texture, asymmetry, phone framing) and look preset. Loose brief -> 3 variants per `../references/storyboard-variations.md` (vary hook family + one other axis), A/B/C labels, wait for a pick. Resolve the storyboard image model from the marketing image set in `../SKILL.md`.
5. **Cost-preflight** (mandatory - `../../krea-generate/references/cost-preflight.md`). A 10-15s clip with audio is the expensive step; batches multiply it. Show the estimate, get yes.
6. **Resolve a dialogue/audio-capable video model** from live `list_models` + `get_model_schema`; do not use a remembered default. Verify the live schema exposes spoken-audio generation (dialogue in prompt, `generate_audio`-style fields). If the resolved model is a `seedance-2` variant, load `../../krea-generate/references/models/seedance-2.md` for dialogue formatting, reference roles, and pacing guardrails. If no live model supports speech, say so and offer the silent-clip + captions fallback instead of faking it.
7. **Generate the takes.** One job for a script that fits the model's max duration. Longer scripts: chunk at sentence boundaries into takes that each obey 2-4 wps, SAME face reference(s) on every take for identity lock (a text persona alone will drift between takes - require a face ref or generate one portrait first and reuse it). Timeline prompt carries the spoken lines, realism cues, and look preset; aspect-trap and pacing-word rules from `social-video-short.md` apply (no landscape refs for 9:16; never `slow`/`gentle`/`soft`). Upload all refs to Krea first; submit jobs and wait with the available job tool.
8. **Demo/b-roll cutaways** (if the structure calls for them): trim from user-provided footage per the placement table in `../references/ugc-scripts.md` (input moment early, money shot second). Never generate app/software UI with a model - real screen recordings only.
9. **Assemble** per `../references/video-ad-post.md`: normalize segments, stitch takes/cutaways, burn captions in the chosen style, add the CTA card in the final ~4s, optional music bed under the dialogue. All text inside the green zones. HyperFrames only if the user wants designed caption motion.
10. **Virality QA gate (blocking).** Sample the first frame + 4-6 beat frames, inspect with vision, and score against the 7-criterion scorecard in `../references/video-ad-qa.md`. Below 70: apply the per-criterion fix and rework before delivering. Also run the adversarial UGC question - does it read as real creator content? Record pass/fail.
11. **Deliver** with the scorecard summary, QA notes, and the delivery spec from `../references/video-ad-post.md`. For variant batches: change ONE tuple axis per variant (hook family, persona, setting, format hook), and produce/test 3-5 before any larger batch. Posting/scheduling is out of scope - hand off platform-ready files.

### Tool path

Use the available Krea tools: list models, inspect the schema of both the storyboard image model and the dialogue-capable video model, upload product/face refs and the approved storyboard, then submit video generation with schema-verified prompt, references, aspect, duration, and audio fields. Wait with the available job tool. Captions, CTA card, stitching, and music run locally with ffmpeg per `../references/video-ad-post.md`.

## Banned

- Do not generate video before the script AND storyboard are explicitly approved.
- Do not submit scripts outside 2-4 words/second for their duration.
- Do not ask the video model to render captions, CTA text, or logos - all text is burned in post.
- Do not use the word "selfie" in generation prompts unless a phone in hand is wanted - models have a strong selfie=holding-phone prior; use "talking-head close-up" or "vertical front-camera video".
- Do not use commercial-polish vocabulary from the banned list in `../references/ugc-social-video.md`.
- Do not AI-generate app or product UI for demo cutaways - real screen recordings only.
- Do not use "your [personal attribute]" phrasing in scripts or overlays.
- Do not run multi-take scripts on a text persona without a locked face reference - identity will drift.
- Do not pass landscape references for 9:16 output, use banned pacing words, use non-Krea-hosted refs, or poll silently - all inherited from `social-video-short.md`.
- Do not deliver below a 70 virality score; tell the user the score, apply the weak-criterion fixes, and re-score before delivery.
- Do not invent post-publish performance numbers; the winner bands in `../references/video-ad-qa.md` apply only to real metrics.

## Cost & time

- Per-job: storyboard is cheap; a 10-15s clip with audio is comparable to `social-video-short.md`'s video step (~1500+ CU, 8-15 min for a Seedance-class 15s 720p job). Multi-take scripts multiply per-take cost.
- Typical full workflow: script iterations (free) + 1-3 storyboards + 1-3 video takes + local assembly; ~15-30 minutes wall clock.
- Hard caps the user should know: per-job max duration is model-dependent (check live schema); face likeness from refs is moderate - offer LoRA training for a recurring campaign creator; a variant batch of N ads costs ~N times the single-ad video spend.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Speech rushed or padded with dead air | Script outside 2-4 wps for the duration | Recount words, rewrite or resize the shot, regenerate |
| Lip-sync looks off | Line too long for its shot, or model weak at dialogue | Shorten the line or lengthen the shot; try another live audio-capable model |
| Subject holds a phone unprompted | "selfie" or phone words in prompt | Rewrite with "talking-head close-up" / "vertical front-camera video" |
| Face changes between takes | Text persona without a locked face ref | Reuse the same face ref(s) on every take, or train a LoRA |
| Looks like a brand commercial | Polish vocabulary or studio cues leaked in | Rebuild storyboard per the realism rubric in `../references/ugc-social-video.md` |
| Captions feel fake/mistimed | Timing guessed instead of synced to audio | Re-time phrases to actual audio per `../references/video-ad-post.md` |
| Captions/CTA clipped by platform UI | Text outside green zones | Reposition per `../references/video-ad-qa.md` safe areas |
| Virality score <70 | Weak hook, pacing, or first frame | Apply the per-criterion fix table in `../references/video-ad-qa.md`, rework, re-score |
| Output horizontal / slow motion / stitched feel / silent-poll trust loss | Shared traps | Same fixes as `social-video-short.md` On-failure table |
| No live model supports dialogue | Catalog gap at run time | Say so; offer silent clip + burned captions, or park until a speech-capable model is live |
