# Changelog

## Unreleased

- Added `krea-ai/references/models/` as the home for per-model prompting playbooks loaded after model resolution. First entry: `seedance-2.md` covering engine constraints (named-technique action beats, exit-frame implicit cut, no reflections), the action/general/dialogue archetype router, double-contrast cut rules, the age-blind character rule, image-reference legend, bilingual EN+ZH output, and the antislop/pacing banned-phrase lists.
- Wired the new reference into `social-video-short.md`, `narrative-video-long.md`, and `image-to-video-animate.md` so it loads only when the resolved video model is a `seedance-2` variant.
- **narrative-video-long.md: added mandatory asset-sheet pre-production step** (character turnaround + prop sheet + location plate, parallel batch) before scene composition. Closes #30. The 3-track anime test on this branch confirmed identity drift across every track when the asset sheet is skipped.
- **narrative-video-long.md: replaced "batch-animate after still approval" with a scene-by-scene chain** using `endImage` as the continuity hook (scene N's `endImage` = scene N+1's `startImage`). One decision point per scene, lower total CU on failure, no "random concat" boundaries. Closes #34.
- **narrative-video-long.md: added "Concept shotgun" step** for thin briefs — propose 3 distinct concept variants up front instead of asking the user to author the creative subject matter. Closes #27.
- **seedance-2.md: added positional-travel rule for combat motion** — direction + distance + duration must be named, or the engine renders the attack *state* not the *trajectory*. Worked Gear-3 example. Closes #36.
- **seedance-2.md + cli-or-mcp.md: lead with `-i` raw-input pattern** for video. Named CLI flags cover ~4 of 12+ Seedance 2.0 schema fields and silently drop `endImage`, `referenceImages`, `generateAudio`, `resolution`, `seed`. Workflows now show the `-i` syntax for arrays, booleans, and numbers as primary. Closes #33.
- **Added `references/budget-tracking.md`** — session CU tracker protocol covering the gap between cost-preflight (gates a single upcoming op) and 402 Payment Required (catches accumulated spend too late). Surfaces running total at logical breakpoints and gives the user a clear top-up / profile-switch path on first 402. Wired into `SKILL.md` UX rule 4. Closes #32.

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
