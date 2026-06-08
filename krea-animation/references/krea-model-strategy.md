# Krea Model Strategy

Use live model discovery. Do not rely on remembered model IDs.

## Required Checks

```bash
krea doctor
krea models list --json
krea models show <model-id> --json
```

Inspect schemas for exact field names. Current Krea CLI fields may use snake_case in schema, while CLI convenience flags expose `--start-image`, `--aspect`, and raw `-i key=value` inputs.

## Current Defaults

These are defaults, not permanent promises:

- Draft character/style exploration: fast image model from live catalog.
- Production model sheets and keyframes: prefer `openai/gpt-image-2`, `krea/krea-2/medium`, or `krea/krea-2/large` when present and suitable.
- Approved shot animation: prefer `bytedance/seedance-2` for flagship video when present.
- Draft animation tests: prefer `bytedance/seedance-2-fast` or another fast video model when present.
- Final/highest-fidelity alternatives: evaluate live Veo, Kling, Runway, or other video models by schema and brief.

## Seedance-Style Schema Needs

For shot animation, prefer a model that supports:

- `prompt`
- `start_image`
- optional `end_image`
- `reference_images`
- `duration`
- `aspect_ratio`
- `resolution`
- `generate_audio`

If a model does not support an end frame, convert the plan to start-frame plus reference-image prompting or choose another model.

## Cost Discipline

Use `../krea-ai/references/cost-preflight.md` before any video, batch, or final-quality run. Show the user:

- number of shots
- seconds per shot
- model family
- rough retry budget
- expected wall-clock range

## App Work

If the user asks to build a UI, API, or production integration, route implementation to `../krea-build/SKILL.md`. This skill defines the creative and production contract.
