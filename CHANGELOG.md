# Changelog

## 0.2.1

- Added campaign brief intake, reference-first disambiguation, taste gates, and no-default-anchoring rules for campaign work.
- Added key-visual sheet routing/workflow and visual artifact taxonomy to prevent CPG storyboard requests from routing to film pre-vis or premature video generation.
- Added marketing creative anatomy guidance for decomposing ads into mode, product, brand, format, hook, setting, talent, reference path, and CTA.
- Added UGC/social storyboard variation guidance so loose briefs default to cheap A/B/C directions before animation.
- Documented CLI media-reference upload patterns, silent empty-result video failures, and raw REST job-inspection pitfalls.
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
