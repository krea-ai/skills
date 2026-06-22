# Asset Bible

The asset bible is the source of truth for visual consistency. Build it before generating clips.

## Required Asset Classes

- Characters: turnaround, front, side, 3/4, back if needed.
- Expressions: neutral, happy, angry, afraid, tired, speaking.
- Hands and props: common hand poses, held props, signature objects.
- Mouth shapes: closed, open, wide, narrow, smile, grimace for dialogue-heavy work.
- Costume and color: palette swatches, materials, markings, damage, alternate outfits.
- Backgrounds: clean plates with no characters, lighting variants if story demands it.
- FX: smoke, steam, aura, rain, magic, debris, graphic marks.
- Typography/signage: exact text rendered separately and approved if important.

## Model Sheet Prompt Pattern

```text
Production model sheet for animation.
Consistent character across all poses.
Views: front, 3/4, side, back.
Neutral studio background, full body visible, no props unless specified.
Line quality, palette, costume, proportions, and facial features exactly described.
No extra characters, no scene background, no text labels unless requested.
```

## Approval Gate

Do not move to shot keyframes until:

- main characters have approved sheets
- recurring props and locations are approved
- style guide and palette are approved
- a naming convention exists for asset versions

## Versioning

Never overwrite approved assets. Use:

```text
character-name_turnaround_v001.png
character-name_expression_happy_v001.png
world-shop-interior_plate_warm_v001.png
```

## Common Failures

| Symptom | Fix |
|---|---|
| character changes shot to shot | add turnaround and expression refs to keyframe prompts |
| costumes drift | promote costume sheet into `assets.csv` |
| backgrounds mutate | use clean background plates and reference images |
| action breaks design | reduce motion and generate clearer start/end keyframes |
