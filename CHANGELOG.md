# Changelog

## 0.5.2

- Documented public moodboard discovery in `krea-generate/references/models/krea-2.md`: the preset moodboard gallery at `GET https://www.krea.ai/api/preset-moodboards` answers unauthenticated (verified live 2026-06-11, ~3549 boards) and supports `limit`, `seed` (stable shuffle order), `search` (keyword filter the agent can query directly), and `cursor` pagination. Recorded the observed response shape (`items[].id` as the K2 moodboard UUID, `styleName`, `styleDescription`, `styleKeywords`, `isStaffPick`, Krea-hosted `previewImages`/`images`), a preset discovery recipe (search → shortlist → vision-check previews → pass the UUID into `moodboards: [{id, strength}]`), and kept the authenticated `/api/moodboards` rules for personal boards. The `image_style_references` fallback now names preset preview URLs as valid Krea-hosted style references.
- `krea-generate/SKILL.md`: the `references/models/` pointer now routes all moodboard work - discovery, preset-gallery search, and moodboard-driven generation - to `references/models/krea-2.md`.
- Added `krea-marketing/workflows/launch-teaser.md`: premium launch teasers, brand films, and kinetic-type product videos built by separating AI footage from designed motion - video models generate raw textless cinematic shots (i2i stills from the product reference, start_image clips, one steady camera move each); all typography, beat-synced cuts, flashes, HUD overlays, and the end card are composed deterministically through the external `hyperframes` skill. The recipe locks the beat grid first, generates ElevenLabs music against explicit cut timestamps (with the free-tier `/v1/sound-generation` fallback documented), and gates delivery on lint/validate/inspect/render plus frame-level vision QA.
- `krea-marketing/SKILL.md` routes launch video / brand film / teaser / product reveal / kinetic type video to the new workflow and notes the `hyperframes` handoff for designed motion-graphics composition; `workflows/social-video-short.md` disambiguates designed launch films from UGC in its trigger.
- Bumped synced package, plugin, marketplace, codex/cursor manifest, and skill versions to `0.5.2`.

## 0.5.1

- Added a Marketing Image Model Policy to `krea-marketing/SKILL.md`: the marketing image set is `openai/gpt-image-2` (default), live Nano Banana 2, and live Nano Banana Pro. `gpt-image-2` always comes first for text-heavy work (ad templates, key visuals, posters, exact copy, storyboard sheets); for product hero, lifestyle, marketplace, and final stills the agent names `gpt-image-2` as the default alongside the live Nano Banana option and lets the user choose. All marketing workflows now resolve image models through this policy.
- Rewrote `krea-generate` model selection around pure live discovery: `model-catalog.md` archetypes no longer name model IDs or keyword-match on remembered names; `preferences.md` became a model-selection boundary (`KREA_PREFERENCES.md`/`CLAUDE.md` pins no longer override live discovery; explicit per-request user model picks are verified live); `cli-or-mcp.md` is now a surface availability gate with CLI and MCP as peers instead of a CLI-first command reference.
- Replaced hardcoded CLI command examples across `krea-generate` and `krea-marketing` workflows with surface-agnostic CLI/MCP path guidance: discover command syntax from the installed CLI help or connected MCP tool schemas, and treat command shapes from memory or old transcripts as stale.
- Added `krea-generate/references/models/krea-2.md`: Krea 2 live-schema field notes (aspect_ratio, resolution, creativity, intensity, complexity, image_style_references, styles, moodboards), authenticated moodboard discovery rules, moodboard strength guidance, and QA notes. Wired from `SKILL.md`, `model-catalog.md`, and `troubleshooting.md`.
- `krea-animation`: switched skill rules and `references/krea-model-strategy.md` to live model discovery; `scripts/submit_video_jobs.py` now resolves draft/final video models from the live catalog by capability keywords instead of hardcoded model lists, and exits with an explicit error when no live model matches.
- `lora-train-and-use.md`: the training base model must be verified against Krea's live training API/docs instead of a hardcoded `flux_dev`; dropped the `KREA_PREFERENCES.md` style-pin suggestion.
- README: prerequisites now present the authenticated CLI and connected MCP as peer surfaces; fixed the stale version badge.
- Bumped synced package, plugin, marketplace, codex/cursor manifest, and skill versions to `0.5.1`.

## 0.5.0

- Added a DTC static ad-format library to `krea-marketing`: `references/dtc-ad-formats.md` — 16 brand-agnostic, original ad-format templates (headline, offer, bundle, testimonial, press, UGC two-panel, spec callouts, benefits, comparison diptych, before/after, magazine, behind-the-product, manifesto, what's-in-the-box, organic, lifestyle-in-use), each with its required structural device, an art-direction treatment, and a placeholder prompt template organized by the existing static format families.
- Added `workflows/dtc-ad-templates.md`: turn one product reference photo into N on-brand static ad stills, with cost-preflight, model-aware generation (gpt-image-2 async + multiples-of-16; nano-banana-pro aspect_ratio), and per-format structural-device vision QA. Images-only delivery; no bundled scripts.
- Hardened sibling docs: `key-visual-sheet` now flags the gpt-image-2 async requirement, `full-ad-campaign` routes one-photo static ad sets to the new workflow, and the shared troubleshooting table documents the 524-on-sync and multiples-of-16 gotchas for slow image models.
- Moved the animation-domain references `story-spine.md`, `shot-grammar.md`, and `dialogue-and-audio.md` from `krea-generate` to `krea-animation` (their only consumers) and updated the cross-skill links, so `krea-generate` stays a pure generation-primitives skill.
- Bumped synced package, plugin, marketplace, codex/cursor manifest, and skill versions to `0.5.0`; added a DTC routing eval scenario.

## 0.4.0

- Breaking: renamed the canonical generation skill from `krea-ai` to `krea-generate` and removed the `/krea:ai` marketplace invocation. The new invocation is `/krea:generate`.
- Renamed the package metadata from `krea-ai-skill` to `krea-skills` and bumped synced package, plugin, skill, and CI versions to `0.4.0`.
- Added `krea-marketing`, a dedicated marketing creative skill for product photoshoots, marketplace image sets, key visuals, UGC/social ads, product URL creative, social storyboards, ad packs, and campaign workflows.
- Added Krea-native product photoshoot and marketplace-card workflows inspired by researched creative production patterns, without depending on Higgsfield tooling.
- Added optional Meta Ads CLI/MCP performance context for marketing work, including read-first creative intelligence and paused/draft defaults for any gated write operations.
- Moved long-form/narrative/studio animation, storyboards, shotlists, still-to-motion, retakes, and edit assembly material into `krea-animation`.
- Kept generic generation, enhancement, edit, LoRA, portrait, text-poster, archviz, and non-marketing/non-animation video primitives in `krea-generate`.
- Updated high-impact CLI examples to follow live `krea models show --json` `inputSchema` field names such as `image_urls`, `reference_images`, `end_image`, and `generate_audio`.
- Removed legacy `narrative-video-long.md` and `image-to-video-animate.md` entrypoints from `krea-animation`; their useful rules now live in the canonical series, still-to-motion, and shotlist-to-sequence workflows.
- Cleaned stale CLI/MCP and direct API guidance: `krea-build` now uses public API Bearer auth and snake_case fields, workflow-level MCP fallbacks defer to live schema inspection, and Meta Ads intake is limited to paid-social/performance/activation work.
- Updated README, plugin manifests, package contents, CI validation, cross-skill references, and eval scenarios for the four-skill taxonomy.

## 0.3.0

- Added `krea-animation`, a professional animation and anime production skill for asset bibles, model sheets, storyboards, shot lists, Krea video jobs, edit assembly, QA, and retakes.
- Added file-based animation project scaffolding, validation, manifest generation, Krea video job submission/polling, ffmpeg assembly, and QA frame sampling scripts.
- Updated `krea-ai` routing so studio animation, anime series, storyboard-to-video, and shotlist-to-sequence requests hand off to `krea-animation`.
- Updated package/plugin metadata, README, CI validation, package-content checks, and eval scenarios for the new third skill.
- Follow-up fixes after the 0.2.1 campaign workflow merge: added the missing `references/dialogue-and-audio.md`, filled in the Krea-specific Seedance-2 operating rules that workflows referenced, reconciled Seedance native-audio assembly, clarified `endImage` duration/trim behavior, and made narrative cost estimates consistent.
- Added `krea-ai/references/models/` as the home for per-model prompting playbooks loaded after model resolution. First entry: `seedance-2.md` covering multimodal reference roles, time-segmented prompt structure, Krea-specific Seedance media-path exclusions, `endImage` destination behavior, chain-from-last-frame continuity, positional-travel prompting, shadow-fail recovery, concurrency caps, and pacing guardrails.
- Wired the new reference into `social-video-short.md`, `narrative-video-long.md`, and `image-to-video-animate.md` so it loads only when the resolved video model is a `seedance-2` variant.
- **narrative-video-long.md: added mandatory asset-sheet pre-production step** (character turnaround + prop sheet + location plate, parallel batch) before scene composition. Closes #30. The 3-track anime test on this branch confirmed identity drift across every track when the asset sheet is skipped.
- **narrative-video-long.md: replaced "batch-animate after still approval" with a scene-by-scene chain** using `endImage` as the continuity hook (scene N's `endImage` = scene N+1's `startImage`). One decision point per scene, lower total CU on failure, no "random concat" boundaries. Closes #34.
- **narrative-video-long.md: added "Concept shotgun" step** for thin briefs — propose 3 distinct concept variants up front instead of asking the user to author the creative subject matter. Closes #27.
- **seedance-2.md: added positional-travel rule for combat motion** — direction + distance + duration must be named, or the engine renders the attack *state* not the *trajectory*. Worked Gear-3 example. Closes #36.
- **seedance-2.md + cli-or-mcp.md: lead with `-i` raw-input pattern** for video. Named CLI flags cover ~4 of 12+ Seedance 2.0 schema fields and silently drop `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`. Workflows now show the `-i` syntax for arrays, booleans, and numbers as primary. Closes #33.
- **Added `references/budget-tracking.md`** — session CU tracker protocol covering the gap between cost-preflight (gates a single upcoming op) and 402 Payment Required (catches accumulated spend too late). Surfaces running total at logical breakpoints and gives the user a clear top-up / profile-switch path on first 402. Wired into `SKILL.md` UX rule 4. Closes #32.
- **narrative-video-long.md + seedance-2.md + cli-or-mcp.md: documented the `endImage` ⊕ `referenceImages` exclusion.** Seedance 2 returns HTTP 422 when both are passed together; the prior commit's example unintentionally violated this. Recipe step 5c now splits chained-vs-terminal scene calls; banned list, On-failure table, and CLI worked example all updated. Identity rule clarified: locks at still-compose time (image-to-image with refs), so chained clips ride identity via the next clip's `startImage` and don't need `referenceImages`. Empirically validated by the 3-track anime chain-demo test on this branch (all 3 agents independently hit the 422).
- **cli-or-mcp.md: documented per-model reference-field variance.** `bytedance/seedance-2` uses `referenceImages`; `google/nano-banana-pro` uses `imageUrls`; `bfl/flux-1-kontext-dev` uses `imageUrl`; `google/imagen-4-ultra` has no reference field. The CLI's `-i` does not validate field names against the schema, so wrong field names silently no-op rather than erroring. Always read `krea models show <id> --json` before guessing.
- **narrative-video-long.md: corrected Seedance 2 720p / 10s pricing to ~1,738 CU/clip** (live billing 2026-05-21) and revised the end-to-end budget to ~11-15k CU for a 60-80s narrative video at 720p with audio. The prior estimate (~830 CU/clip) was the lower video-reference-eligible tier, which most chain workflows can't use simultaneously with `endImage`.

## 0.2.1

- Added campaign brief intake, reference-first disambiguation, taste gates, and no-default-anchoring rules for campaign work.
- Added key-visual sheet routing/workflow and visual artifact taxonomy to prevent CPG storyboard requests from routing to film pre-vis or premature video generation.
- Added marketing creative anatomy guidance for decomposing ads into mode, product, brand, format, hook, setting, talent, reference path, and CTA.
- Added UGC/social storyboard variation guidance so loose briefs default to cheap A/B/C directions before animation.
- Documented CLI media-reference upload patterns, silent empty-result video failures, and raw REST job-inspection pitfalls.
- Documented the Krea 2 Large CLI default, async `job_id` stdout contract, and Krea 2 public input shape (`aspect_ratio`/`resolution`, `image_style_references`).
- Embedded `VERSION` and `scripts/update-check.sh` inside `krea-ai/` so skill-directory installs keep the passive update checker.
- Tightened cost gates and troubleshooting around expensive campaign batches, "boring" feedback, and Seedance-style failure modes.
- Added an eval regression for CPG storyboard/key-visual routing.

## 0.2.0

- Restructured `krea-ai` around flat, intent-first workflow prefabs in `krea-ai/workflows/`.
- Added mandatory `cost-preflight.md` and `progress-reporting.md` primitives for expensive and long-running jobs.
- Promoted the storyboard-first short social video workflow as the canonical path for <=15s social video.
- Folded cookbook, video production, pipeline, and LoRA training recipes into workflow files.
- Extended troubleshooting with the 2026-05-17 video failure lessons and CLI/model issue workarounds.
- Breaking: legacy vertical skill entrypoints were removed; canonical marketing and archviz workflows now live under `krea-ai/workflows/`.
- Breaking: legacy reference files absorbed into workflows were removed.
