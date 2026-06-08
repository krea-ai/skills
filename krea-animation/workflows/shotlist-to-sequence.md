# Shotlist To Sequence

## Trigger

Use when a storyboard and shot list are approved and the user wants to generate multi-shot animation clips and assemble an edit.

## Recipe

1. Run `scripts/validate_project.py <project>`. Fix blocking errors before spending credits.
2. Run cost preflight. Estimate approved shot count, seconds per shot, model family, resolution, and retry budget.
3. Run `scripts/build_manifests.py <project>` to produce video job and edit manifests.
4. Dry-run submission:
   ```bash
   python3 krea-animation/scripts/submit_video_jobs.py <project> --dry-run
   ```
5. Submit only approved shots. For the first pass, submit 1-3 representative shots before the whole sequence.
6. Poll jobs with progress updates:
   ```bash
   python3 krea-animation/scripts/poll_video_jobs.py <project> --download
   ```
7. Normalize and assemble:
   ```bash
   python3 krea-animation/scripts/assemble_edit.py <project> --fps 24 --size 1280x720
   ```
8. Sample QA frames:
   ```bash
   python3 krea-animation/scripts/sample_qa_frames.py <project>
   ```
9. Review against storyboard, style bible, and asset bible. Log retakes in `06_qa/retakes.csv`.
10. Repeat generation only for failed shots. Keep passed clips locked.

## Continuity Checks

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
