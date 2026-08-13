# Shotlist To Sequence

## Trigger

Use when a storyboard and shot list are approved and the user wants to generate multi-shot animation clips and assemble an edit.

## Recipe

1. Restate the shot list back to the user: shot IDs, durations, start images, and approval status. Flag blocking gaps before spending credits.
2. Run cost preflight. Estimate approved shot count, seconds per shot, Seedance variant, resolution, and retry budget.
3. Resolve the live Seedance variant with `list_models`, and read `../../krea-generate/references/models/seedance-2.md` for the field-mapping rules.
   Write every shot prompt with the block architecture in `../../krea-generate/references/models/seedance-2.md`; pull camera and reveal moves from `../references/reveal-recipes.md` and `../references/dimensional-motion.md`.
4. Lay out the planned jobs in one table — shot ID, duration, model, aspect, start image, end image or references, prompt — so the user can approve before submission.
5. Check each planned job against the live model schema. Confirm every approved shot has a Krea-hosted `start_image` and that Seedance-style shots use only one of `end_image` or `reference_images`.
6. Submit only approved shots with `generate_video`. For the first pass, submit 1-3 representative shots before the whole sequence. Keep the returned job IDs alongside their shot IDs.
7. Poll each job to completion and report progress as you go.
8. Inspect mid/end frames for the test shots. Log concrete retakes before submitting the rest of the sequence.
9. Continue in batches. Keep in-scene continuity serialized when a shot depends on the previous shot's last frame; batch independent hard-cut shots in parallel within live model limits.
10. Review the finished clips against the storyboard, style bible, and asset bible. Track retakes as a running list with shot ID, priority, issue, fix type, and status.
11. Repeat generation only for failed shots. Keep passed clips locked.

## Shot Generation Rules

- A scene is not one clip. Use shot grammar from `../references/shot-grammar.md`: most scenes become 3-6 shots of 2-4 seconds each.
- Use approved keyframes only. If the shot starts from the previous shot's extracted last frame, generate the predecessor first and update the manifest before submitting the dependent shot.
- `end_image` and `reference_images` are mutually exclusive on Seedance. Chained shots use `start_image` + `end_image`; terminal or hard-cut shots use `start_image` + `reference_images`.
- Every shot prompt carries a motion split, a world lock, a light block with negatives, and a constraints tail. Quantify camera moves and state realtime physics — see `../../krea-generate/references/models/seedance-2.md`.
- Block shots on a fast Seedance variant, judge, then re-run approved prompts on the quality variant for delivery.
- Discover submit fields with `get_model_schema` and use only fields it exposes. Do not copy field names from memory.
- Keep native generated audio only when the shot plan explicitly calls for it. Otherwise default to no generated clip audio and assemble the final audio bed separately.
- Treat a completed job with no result URL as a failed shot. Retry once with a simpler prompt, then log a retake.

## Continuity Checks

Inspect the **last** frame of every clip, not just the middle — drift is progressive. For multi-beat prompts, verify the cuts landed with scene detection instead of eyeballing them:

```bash
ffmpeg -i shot-raw.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```

- character identity and proportions
- costume, props, colors, and marks
- eyelines and screen direction
- background continuity
- action starts and ends where intended
- no unintended text, logos, watermarks, or character drift
- clip duration and frame rate match the edit plan

## Banned

- Do not assemble clips without normalization.
- Do not keep inconsistent per-clip audio unless explicitly approved.
- Do not overwrite raw generated clips.
- Do not call a rough assembly final without QA frame review.
