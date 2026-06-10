# Series From Scratch

## Trigger

Use when the user has only an idea, premise, character, genre, or rough story and wants an anime/animated episode, pilot, trailer, or sequence.

## Goal

Create the minimum studio package needed before any expensive video job: brief, story spine, style bible, asset list, storyboard, shot list, keyframe plan, approvals, and only then generated clips.

## Concept Development

If the user only gives a logline or broad premise, propose 3 distinct concepts before asking them to fill in production details. Each concept should include:

- one-line title and pitch
- protagonist, want, obstacle, stakes, turn, and new normal
- implied 6-8 beat scene list
- dialogue posture
- final-5-seconds feeling

Let the user pick or remix one concept, then proceed to the production package.

## Recipe

1. Clarify once: target runtime, audience, aspect, style references, language/dialogue, delivery format, and whether this is a proof of concept or final sequence.
2. If the premise is creatively thin, run the concept development step above and wait for a chosen direction.
3. Scaffold a project with `scripts/scaffold_project.py`.
4. Write `00_brief/brief.md`: logline, audience, runtime, tone, constraints, approval owner.
5. Write `02_story/beat-sheet.md` with story spine fields from `../references/story-spine.md`: protagonist, want, obstacle, stakes, turn, new normal, dialogue posture, and final feeling.
6. Stop for story-spine approval before storyboard or keyframe generation.
7. Write `01_bible/style/style-guide.md`: line quality, palette, lighting, camera, animation density, banned looks.
8. Plan required assets before image generation: characters, expressions, hands, props, environments, FX, signage, typography.
9. Generate or collect asset sheets. Use cheap draft models first, then high quality only after the style is approved.
10. Write `02_story/storyboard.md` with shot-by-shot panels in text if image boards do not exist yet.
11. Create shot folders under `03_shots/SC###/SH###/shot.md`. Every shot must include duration, action, camera, start keyframe, end keyframe or references, dialogue, SFX, continuity hook, status.
12. Stop for user approval before video generation. No storyboard and shot-list approval means no animation.
13. Continue with `shotlist-to-sequence.md` after approval.

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
