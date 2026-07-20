# Krea Model Strategy

Use live model discovery. Do not rely on remembered model IDs.

## Required Checks

1. Verify the needed Krea tools are available in the current session.
2. List live models.
3. Inspect the selected model schema.
4. Submit using only fields exposed by the live schema.

## Selection Policy

Use live model discovery. Do not maintain animation defaults here. Pick candidates by matching the approved animation task to live model descriptions and schemas:

- Draft character/style exploration: fast image model capability.
- Production model sheets and keyframes: text fidelity, reference handling, and high-fidelity still capability.
- Approved shot animation: cinematic video capability with required frame/reference controls.
- Draft animation tests: faster video capability when available.
- Final/highest-fidelity alternatives: evaluate live video models by schema and brief.

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

Use `../../krea-generate/references/cost-preflight.md` before any video, batch, or final-quality run. Show the user:

- number of shots
- seconds per shot
- model family
- rough retry budget
- expected wall-clock range

## App Work

If the user asks to build a UI, API, or production integration, use the app-integration skill if it is installed. This skill defines the creative and production contract.
