# Studio Shot Production

## Trigger

Use when the user already has studio materials: a script, boards, animatic, style guide, character sheets, background plates, shot spreadsheet, rough cut, existing assets, or production notes.

## Goal

Ingest existing production materials without flattening them into a generic prompt. Preserve the studio's naming, continuity, approval statuses, and shot ownership.

## Recipe

1. Inspect provided files first. Identify script, boards, style guides, model sheets, palettes, backgrounds, shot lists, audio, and edit references.
2. Scaffold a project only if no production folder exists. Otherwise adapt the existing folder without renaming user assets.
3. Map studio inputs to the canonical structure in `references/project-structure.md`.
4. Build or update `assets.csv`, `keyframes.csv`, and per-shot `shot.md` files.
5. Mark every imported shot as one of: `draft`, `needs_assets`, `needs_keyframes`, `approved_for_video`, `submitted`, `complete`, `retake`, `approved_final`.
6. Create a gap report before generation:
   - missing model sheets or turnarounds
   - missing background plates
   - missing start/end keyframes
   - unclear duration or camera
   - unresolved dialogue/audio
   - inconsistent aspect or FPS
7. If gaps exist, fill only the missing production artifacts. Do not rewrite approved materials.
8. For approved shots, continue with `shotlist-to-sequence.md`.

## Professional Defaults

- Preserve shot IDs from the source production.
- Keep retakes as new versions, not overwritten media.
- Keep source boards and style guides separate from generated keyframes.
- Treat the user's materials as higher authority than generic model defaults.

## Banned

- Do not discard existing naming conventions.
- Do not regenerate approved assets unless the user asks.
- Do not batch-submit all shots before the first approved test shot succeeds.
