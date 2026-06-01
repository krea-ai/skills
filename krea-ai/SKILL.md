---
version: 0.2.1
name: krea-ai
description: "Generate images, videos, enhance/upscale, train LoRAs, and run campaign workflows through Krea. Intent-first workflow prefabs route common asks to hard recipes for social video, key visuals, image generation, product photography, archviz, enhancement, LoRA training, and ad campaigns."
license: MIT
---

# Krea AI - Generation, animation, enhancement

Use Krea through the CLI by default, with the Krea MCP server as fallback. This skill is organized around intent-first workflow prefabs: classify the user's verb + modality + flavor, load the matching `workflows/*.md`, and follow that recipe instead of improvising from a model menu.

For developers building apps that call Krea programmatically, use the sibling `krea-build/` skill instead.

## Bootstrap

Prefer the Krea CLI whenever it is installed and authenticated:

```bash
which krea && krea doctor 2>&1 | head -5
```

A healthy CLI prints `api auth` success for `list_models`. If the CLI is missing:

```bash
npm install -g @krea-ai/cli
krea auth login
# or export KREA_API_KEY=...
```

Use MCP only when the CLI is unavailable and Krea tools such as `list_models`, `get_model_schema`, `generate_image`, `generate_video`, `enhance_image`, `get_job`, and `upload_asset` are connected. If neither surface is available, stop and ask the user to install the CLI or connect MCP. Do not use direct HTTP for normal generation except documented flows such as LoRA training.

Before the first generation in a session, optionally run the passive update check only if this skill directory contains `scripts/update-check.sh`:

```bash
bash /path/to/krea-ai/scripts/update-check.sh 2>/dev/null || true
```

It never blocks generation. Surface `UPGRADE_AVAILABLE` or `JUST_UPGRADED` once; otherwise stay quiet.

## Universal UX rules

1. Concise output. Send result path/URL plus one useful sentence. No raw IDs or JSON dumps.
2. Detect the user's language from their first message and reply in it. Technical params stay English.
3. Vision-first. Read attached images before generating, and read every generated still/frame with the Read tool before approving it, showing the user, or feeding it to a downstream model. Critique each output on its own line per `references/vision-qa.md` — composition, named action present, identifying details, lighting, continuity hook for the next clip. Never approve a batch with a one-line "all of them look great"; that is the rubber-stamp failure mode that produces broken endImages and Seedance refusals downstream.
4. No premature questions for cheap ops. For cheap images/enhance, pick sane defaults. For expensive ops, do not answer prematurely: run campaign brief intake when it applies, clarify once, run `references/cost-preflight.md` for upcoming spend, and maintain `references/budget-tracking.md` for the session's running total so 402 Payment Required is never the first signal that credits ran out.
5. Progress reporting is mandatory for async polling over 30 seconds. Use `references/progress-reporting.md`.
6. Always call `list_models` before choosing a model. Use `references/model-catalog.md` to resolve archetypes to live IDs.
7. Always inspect the model schema before submitting. Do not guess field names such as `imageUrl`, `imageUrls`, `startImage`, `duration`, or `resolution`.
8. Upload local references to Krea before generation. Some models reject non-Krea-hosted URLs.
9. Honor `KREA_PREFERENCES.md` or a `## Krea preferences` section in project docs when present.
10. Do not pretend bad outputs are fine. Name the mismatch and offer a concrete retry path.
11. Reference before prose. If the user uses a term with multiple legitimate visual meanings (`storyboard`, `mood board`, `key visual`, `hero shot`, `mockup`, `tearsheet`, `look book`), ask for a reference image before interpreting it in your own visual language.
12. Taste gate, not just fidelity gate. Before delivering campaign-tier output, write one sentence to yourself answering: is this recognizably premium creative, or is it category-cliche? If cliche, iterate before shipping.
13. No default anchoring in routing questions. If asking image-vs-video, draft-vs-final, or similar, present options neutrally without "default if you say go" phrasing.

## Campaign brief intake

Mandatory before routing when the request involves a product, brand, campaign, ads, shorts, social pack, or more than 3 deliverables. Skip only for one-shot quick generations.

Ask once, in a single compact message, for any missing items:

1. **Vocabulary**: restate loaded terms (`storyboard`, `ad`, `short`, `campaign`, `draft`, `hero`) in the user's likely industry context. Use `references/artifact-taxonomy.md` when terms are ambiguous.
2. **References**: ask for layout, style, tone, or format references before generating any planning artifact.
3. **Brand voice**: infer one sentence from the product, packaging, refs, and user brief; confirm if uncertain.
4. **Success criteria**: one line per deliverable covering audience, platform, and intended action.
5. **Levers**: keep format, content, palette, and voice separate when responding to feedback such as "boring", "meh", or "surprise me". For ad/campaign work, load `references/marketing-creative-anatomy.md` and separate mode, format, hook, setting, talent, product, brand, reference path, and CTA.

Output a 5-line confirmed brief, then route.

## Routing - intent -> workflow

| Intent (verb + modality + flavor) | Workflow |
|---|---|
| make a short vertical / social / TikTok / Reels / Shorts / GRWM video, <=15s | `workflows/social-video-short.md` |
| ad storyboard / key visual / campaign sheet / social pack / agency-style product layout | `workflows/key-visual-sheet.md` |
| make a longer narrative video with hard cuts, >15s | `workflows/narrative-video-long.md` |
| animate a still / image-to-video / make this picture move | `workflows/image-to-video-animate.md` |
| make me an image (no quality bar stated, exploring) | `workflows/image-fast-iterate.md` |
| production-quality image / for delivery / hero asset | `workflows/image-final-render.md` |
| transform / edit / restyle this image | `workflows/image-edit-i2i.md` |
| poster / typography / text-heavy image | `workflows/image-text-poster.md` |
| portrait with face refs | `workflows/portrait-with-refs.md` |
| product hero photo / e-com hero shot | `workflows/product-photo-hero.md` |
| product lifestyle / model wearing / scene composition | `workflows/product-photo-lifestyle.md` |
| 3D screenshot -> photoreal render (archviz) | `workflows/archviz-3d-to-render.md` |
| upscale / 4K / enhance / make sharper | `workflows/enhance-upscale.md` |
| creative enhance / restyle / re-light | `workflows/enhance-creative.md` |
| train a LoRA / fine-tune on these images | `workflows/lora-train-and-use.md` |
| product URL -> full campaign | `workflows/full-ad-campaign.md` |

**Hard rule**: never call `generate video` without first loading a `workflows/*.md` file. Workflows enforce cost-preflight, clarify-once, storyboard approval for short video, progress pings, and banned-move lists. Bypassing them is what wasted ~5,000 CU on 2026-05-17.

## References

Load only what the active workflow needs:

- `references/cli-or-mcp.md` - side-by-side CLI and MCP operations.
- `references/model-catalog.md` - archetypes to resolve through live `list_models`.
- `references/media-inputs.md` - uploads, local files, image refs, start/end frames.
- `references/async-polling.md` - job lifecycle semantics.
- `references/prompt-engineering.md` - prompt handling by modality.
- `references/artifact-taxonomy.md` - disambiguate storyboard, key visual, mood board, hero shot, mockup, tearsheet, and look book.
- `references/marketing-creative-anatomy.md` - campaign/ad tuple, hook families, static format families, and reference-driven vs composed paths.
- `references/storyboard-variations.md` - axes and delivery pattern for cheap storyboard variants before video.
- `references/story-spine.md` - PROTAGONIST/WANT/OBSTACLE/STAKES/TURN/NEW-NORMAL gate. Mandatory before storyboarding any narrative >15s.
- `references/shot-grammar.md` - scene-vs-shot vocabulary, beat patterns, match cuts. A 60s narrative is 20–30 shots, not 6.
- `references/dialogue-and-audio.md` - TTS pipeline, ambient bed, ffmpeg audio mux with `adelay`/`amix`. Mandatory when SHOTLIST.md has dialogue.
- `references/ugc-social-video.md` - UGC realism cues, storyboard template, banned polish words, and adversarial QA.
- `references/troubleshooting.md` - known CLI/model issues and recovery.
- `references/preferences.md` - project-level overrides.
- `references/cost-preflight.md` - mandatory approval before >100 CU or video/training jobs.
- `references/progress-reporting.md` - mandatory pings during long async polling.
- `references/models/` - per-model prompting playbooks (engine quirks, archetypes, banned phrases). Load only when the active workflow has resolved that model. Today: `seedance-2.md`.

## Related skill

Use `krea-build/` for developer integration work: API clients, frontend snippets, validation, and repeatable app code.

Marketing, product, campaign, and architectural visualization requests stay in this skill and route to `krea-ai/workflows/`:

- Marketing/product work: `workflows/product-photo-hero.md`, `workflows/product-photo-lifestyle.md`, `workflows/key-visual-sheet.md`, `workflows/social-video-short.md`, `workflows/full-ad-campaign.md`.
- Architectural visualization: `workflows/archviz-3d-to-render.md`.

## Campaign pre-delivery self-eval

Before delivering campaign-tier work, answer these privately and fix any "no" or "not sure":

1. Artifact match: is this the shape the user asked for in their industry's vocabulary?
2. Reference adherence: if a style ref exists, would a viewer place both in the same campaign?
3. Fidelity: are brand assets, label details, palette, typography, and claims correct?
4. Taste: what is the one distinctive element that keeps this from feeling category-cliche?
5. Voice: does the copy/layout match the brand voice surfaced in intake?
6. Variation discipline: did each variation move a meaningful lever, not just wallpaper details?
7. Cost honesty: did this spend more than 2x the minimal CU path, and what intake question would have prevented that?
8. Next-step legibility: can the user approve, reject, or request a tweak without extra explanation?

## Filename pattern

For local outputs, use `yyyy-mm-dd-hh-mm-ss-short-name.ext` with `.png` for images and `.mp4` for videos. Keep short names lowercase and hyphenated.
