---
version: 0.3.0
name: krea-animation
description: "Professional AI animation and anime production workflows with Krea. Use for long-form animation, anime series, storyboard-to-video, shotlist-to-sequence, asset bibles, model sheets, keyframes, animatics, AI video clips, edit assembly, QA, retakes, and studio productivity workflows. For one-off generic image/video generation use krea-ai; for app/API integration use krea-build."
license: MIT
---

# Krea Animation - Studio Animation Production

Use this skill when the user wants to produce animation, not just generate a clip. Treat Krea as the production engine inside an animation pipeline: premise -> bible -> storyboard -> shot list -> assets -> keyframes -> approved video jobs -> edit -> QA -> retakes -> delivery.

This skill is anime-first by default, but applies to any character, narrative, product, or studio animation workflow that needs continuity and shot discipline.

## Hard Rules

1. Do not jump from idea to long video. First create or inspect the project bible, storyboard, and shot list.
2. Do not animate unapproved characters, locations, keyframes, or shot prompts.
3. Run cost preflight before any video, LoRA training, or large batch. Use `../krea-ai/references/cost-preflight.md`.
4. Use the Krea CLI first. Run `krea doctor`, then `krea models list --json`, then `krea models show <model> --json` before relying on a model schema.
5. Prefer live model archetypes over memory. Current defaults can prefer GPT Image 2 or Krea 2 for model sheets/keyframes and Seedance 2 for approved animation, but the live catalog is authoritative.
6. Upload local references before generation. Keep Krea asset URLs in manifests.
7. Video jobs are async. Poll and report progress using `../krea-ai/references/progress-reporting.md`.
8. Normalize clips before assembly. Strip random per-clip audio unless the workflow explicitly asks to keep it.
9. Sample frames and review continuity before delivery. If a shot fails, log a retake instead of pretending it is acceptable.
10. Do not commit copyrighted references or generated run media into this skills repo.

## Route

| User intent | Workflow |
|---|---|
| "I have an idea for an anime/animated series" or novice from scratch | `workflows/series-from-scratch.md` |
| Studio/pro team has script, boards, style guide, layouts, or shot turnover | `workflows/studio-shot-production.md` |
| Approved storyboard/shot list -> clips -> final sequence | `workflows/shotlist-to-sequence.md` |
| Animate one still, one illustration, one model sheet pose, or one keyframe | `workflows/still-to-motion.md` |
| Improve failed clips, manage retakes, final assembly, delivery checks | `workflows/retakes-and-delivery.md` |

If the user asks to build a web app or internal tool around this pipeline, use `../krea-build/SKILL.md` for implementation and this skill only for the creative workflow contract.

## Project Scaffold

For new projects, create the folder structure before creative work:

```bash
python3 krea-animation/scripts/scaffold_project.py \
  --project ./runs/my-animation \
  --title "My Animation" \
  --runtime 60 \
  --aspect 16:9 \
  --fps 24
```

Then validate and generate manifests:

```bash
python3 krea-animation/scripts/validate_project.py ./runs/my-animation
python3 krea-animation/scripts/build_manifests.py ./runs/my-animation
python3 krea-animation/scripts/submit_video_jobs.py ./runs/my-animation --dry-run
```

Use the scripts from the user's project directory when possible so outputs land with the project, not inside this skill.

## References

Load only what the active workflow needs:

- `references/production-pipeline.md` - studio/anime production stages and Japanese pipeline terms.
- `references/project-structure.md` - canonical folders, approval statuses, manifests.
- `references/asset-bible.md` - model sheets, turnarounds, expression sheets, props, colors, backgrounds.
- `references/storyboard-shotlist.md` - shot IDs, duration planning, camera language, continuity hooks.
- `references/krea-model-strategy.md` - live Krea model selection and schema checking.
- `references/motion-prompting.md` - start/end frames, reference images, motion-only prompts, drift control.
- `references/edit-qa-retakes.md` - normalization, assembly, QA frame sampling, retake logs.

Reuse sibling Krea references instead of duplicating them:

- `../krea-ai/references/cli-or-mcp.md`
- `../krea-ai/references/media-inputs.md`
- `../krea-ai/references/async-polling.md`
- `../krea-ai/references/progress-reporting.md`
- `../krea-ai/references/troubleshooting.md`

## Scripts

- `scripts/scaffold_project.py` - create the production folder structure and starter templates.
- `scripts/validate_project.py` - check required files, shot metadata, approvals, and media references.
- `scripts/build_manifests.py` - compile asset, keyframe, video job, duration, and concat manifests.
- `scripts/submit_video_jobs.py` - submit approved video jobs or print dry-run Krea commands.
- `scripts/poll_video_jobs.py` - poll Krea jobs, write results, and optionally download raw clips.
- `scripts/assemble_edit.py` - normalize, concatenate, and optionally smooth transitions.
- `scripts/sample_qa_frames.py` - extract frames for continuity and retake review.
