# Retakes And Delivery

## Trigger

Use after clips are generated, when the user asks to improve quality, fix continuity, assemble final, compare shots, or prepare delivery.

## Recipe

1. Read `06_qa/retakes.csv`, current final edit, sampled frames, and shot manifests.
2. Classify each issue:
   - prompt fix
   - missing asset reference
   - wrong model or schema
   - editing/normalization issue
   - audio/subtitle issue
   - unavoidable model limitation
3. Lock passed shots. Only regenerate failed shots.
4. For each retake, write a short retake note tied to the shot ID and source issue. Diagnose prompt failures against the failure table in `../references/seedance-prompt-architecture.md` and change **one** block per retake with the seed pinned.
5. Regenerate the smallest necessary unit: keyframe first if the still is wrong, video only if the still is right. The start image is the quality ceiling — a soft or badly cropped still cannot be rescued by prompt changes.
6. Reassemble and sample QA frames again.
7. Deliver only after `06_qa/delivery-checklist.md` is complete.

## Delivery Checklist

- final runtime matches target or variance is explained
- all clips normalized to same FPS, resolution, codec, SAR, and pixel format
- no raw clip audio remains unless approved
- subtitles are legible and timed
- final edit has no missing shots or black frames
- sampled frames pass identity, style, background, and action checks
- retake log contains no open `blocking` items

## Banned

- Do not overwrite failed versions; keep versioned files.
- Do not regenerate a complete sequence for a local retake.
- Do not ignore continuity notes because the video is visually impressive.
