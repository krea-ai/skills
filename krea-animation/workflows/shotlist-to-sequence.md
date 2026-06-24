# Shotlist To Sequence

## Trigger

Use when a storyboard and shot list are approved and the user wants to generate multi-shot animation clips and assemble an edit.

## Recipe

1. Run `scripts/validate_project.py <project>`. Fix blocking errors before spending credits.
2. Run cost preflight. Estimate approved shot count, seconds per shot, model family, resolution, and retry budget.
3. Resolve the live model with `../references/krea-model-strategy.md`. If the chosen model is Seedance-style, also load `../../krea-generate/references/models/seedance-2.md`.
4. Run `scripts/build_manifests.py <project>` to produce video job and edit manifests.
5. Dry-run submission:
   ```bash
   VERIFIED_MODEL_ID="bytedance/seedance-2-fast"
   python3 krea-animation/scripts/submit_video_jobs.py <project> --dry-run --model "$VERIFIED_MODEL_ID"
   ```
6. Inspect the dry-run. Confirm every approved shot has a Krea-hosted `start_image` and that Seedance-style shots use only one of `end_image` or `reference_images`.
7. Submit only approved payloads from `04_generation/jobs/mcp-video-jobs.jsonl` through the connected Krea MCP `generate_video` tool. For the first pass, submit 1-3 representative shots before the whole sequence. Write returned job IDs to `04_generation/jobs/jobs.tsv`.
8. Prepare MCP job-status checks:
   ```bash
   python3 krea-animation/scripts/poll_video_jobs.py <project>
   ```
9. Call Krea MCP `get_job` for each row in `04_generation/jobs/mcp-status-checks.jsonl`, save the responses as JSONL, then merge and optionally download completed clips:
   ```bash
   python3 krea-animation/scripts/poll_video_jobs.py <project> --results-jsonl <project>/04_generation/jobs/mcp-results.jsonl --download
   ```
10. Sample mid/end frames for the test shots. Log concrete retakes before submitting the rest of the sequence.
11. Continue in batches. Keep in-scene continuity serialized when a shot depends on the previous shot's last frame; batch independent hard-cut shots in parallel within live model limits.
12. Normalize and assemble:
   ```bash
   python3 krea-animation/scripts/assemble_edit.py <project> --fps 24 --size 1280x720
   ```
13. Sample QA frames:
   ```bash
   python3 krea-animation/scripts/sample_qa_frames.py <project>
   ```
14. Review against storyboard, style bible, and asset bible. Log retakes in `06_qa/retakes.csv`.
15. Repeat generation only for failed shots. Keep passed clips locked.

## Shot Generation Rules

- A scene is not one clip. Use shot grammar from `../references/shot-grammar.md`: most scenes become 3-6 shots of 2-4 seconds each.
- Use approved keyframes only. If the shot starts from the previous shot's extracted last frame, generate the predecessor first and update the manifest before submitting the dependent shot.
- For Seedance-style models, `end_image` and `reference_images` are mutually exclusive. Chained shots use `start_image` + `end_image`; terminal or hard-cut shots use `start_image` + `reference_images`.
- Discover submit fields from Krea MCP and use only fields present in the selected model schema. Do not copy MCP field names from memory.
- Keep native generated audio only when the shot plan explicitly calls for it. Otherwise default to no generated clip audio and assemble the final audio bed separately.
- Treat a completed job with no result URL as a failed shot. Retry once with a simpler prompt, then log a retake.

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
