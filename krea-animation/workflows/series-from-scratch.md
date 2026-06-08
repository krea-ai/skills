# Series From Scratch

## Trigger

Use when the user has only an idea, premise, character, genre, or rough story and wants an anime/animated episode, pilot, trailer, or sequence.

## Goal

Create the minimum studio package needed before any expensive video job: brief, story spine, style bible, asset list, storyboard, shot list, keyframe plan, approvals, and only then generated clips.

## Recipe

1. Clarify once: target runtime, audience, aspect, style references, language/dialogue, delivery format, and whether this is a proof of concept or final sequence.
2. Scaffold a project with `scripts/scaffold_project.py`.
3. Write `00_brief/brief.md`: logline, audience, runtime, tone, constraints, approval owner.
4. Write `02_story/beat-sheet.md`: beginning, obstacle, turn, resolution, final feeling.
5. Write `01_bible/style/style-guide.md`: line quality, palette, lighting, camera, animation density, banned looks.
6. Plan required assets before image generation: characters, expressions, hands, props, environments, FX, signage, typography.
7. Generate or collect asset sheets. Use cheap draft models first, then high quality only after the style is approved.
8. Write `02_story/storyboard.md` with shot-by-shot panels in text if image boards do not exist yet.
9. Create shot folders under `03_shots/SC###/SH###/shot.md`. Every shot must include duration, action, camera, start keyframe, end keyframe or references, dialogue, SFX, continuity hook, status.
10. Stop for user approval before video generation. No storyboard approval means no animation.
11. Continue with `shotlist-to-sequence.md` after approval.

## Banned

- Do not create a long prompt and submit a single long video.
- Do not invent a full asset library after video generation has begun.
- Do not skip style and character approvals.
- Do not use famous studio or franchise styles as direct imitation targets. Use production adjectives instead.

## Output

Deliver a project folder path plus a brief status:

- story package ready
- asset list ready
- storyboard ready
- shot list ready
- approved for generation or waiting on approval
