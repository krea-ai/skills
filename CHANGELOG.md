# Changelog

## 0.2.0

- Restructured `krea-ai` around flat, intent-first workflow prefabs in `krea-ai/workflows/`.
- Added mandatory `cost-preflight.md` and `progress-reporting.md` primitives for expensive and long-running jobs.
- Promoted the storyboard-first short social video workflow as the canonical path for <=15s social video.
- Folded cookbook, video production, pipeline, and LoRA training recipes into workflow files.
- Extended troubleshooting with the 2026-05-17 video failure lessons and CLI/model issue workarounds.
- Breaking: `krea-marketing` and `krea-archviz` are now redirect stubs pointing at canonical `krea-ai/workflows/` recipes.
- Breaking: legacy reference files absorbed into workflows were removed.
