# Studio Shot Production

## Trigger

Use when the user already has studio materials: a script, boards, animatic, style guide, character sheets, background plates, shot spreadsheet, rough cut, existing assets, or production notes.

## Goal

Ingest existing production materials without flattening them into a generic prompt. Preserve the studio's naming, continuity, approval statuses, and shot ownership.

## Recipe

1. Inspect provided files first. Identify script, boards, style guides, model sheets, palettes, backgrounds, shot lists, audio, and edit references.
2. Adopt the studio's own naming and organization. Do not rename or restructure user assets.
3. Build a working index of what exists: assets, keyframes, and per-shot entries carrying the studio's own shot IDs.
4. Mark every imported shot as one of: `draft`, `needs_assets`, `needs_keyframes`, `approved_for_video`, `submitted`, `complete`, `retake`, `approved_final`.
5. Create a gap report before generation:
   - missing model sheets or turnarounds
   - missing background plates
   - missing start/end keyframes
   - unclear duration or camera
   - unresolved dialogue/audio
   - inconsistent aspect or FPS
6. If gaps exist, fill only the missing production artifacts. Do not rewrite approved materials.
7. For approved shots, continue with `../workflows/shotlist-to-sequence.md`. Shots animate on Seedance — resolve the live variant with `list_models` and write prompts with `../../krea-generate/references/models/seedance-2.md`.

## Professional Defaults

- Preserve shot IDs from the source production.
- Keep retakes as new versions, not overwritten media.
- Keep source boards and style guides separate from generated keyframes.
- Treat the user's materials as higher authority than generic model defaults.

## Banned

- Do not discard existing naming conventions.
- Do not regenerate approved assets unless the user asks.
- Do not batch-submit all shots before the first approved test shot succeeds.
