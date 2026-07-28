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
3. Write the brief: logline, audience, runtime, tone, constraints, approval owner.
4. Write the beat sheet with story spine fields from `references/story-spine.md`: protagonist, want, obstacle, stakes, turn, new normal, dialogue posture, and final feeling.
5. Stop for story-spine approval before storyboard or keyframe generation.
6. Write the style guide: line quality, palette, lighting, camera, animation density, banned looks.
7. Plan required assets before image generation: characters, expressions, hands, props, environments, FX, signage, typography.
8. Generate or collect asset sheets. Use cheap draft models first, then high quality only after the style is approved.
9. Write the storyboard as shot-by-shot panels in text if image boards do not exist yet.
10. Break the storyboard into a numbered shot list. Every shot must include duration, action, camera, start keyframe, end keyframe or references, dialogue, SFX, continuity hook, status.
11. Stop for user approval before video generation. No storyboard and shot-list approval means no animation.
12. Continue with `workflows/shotlist-to-sequence.md` after approval.

## Seedance Notes

Shots animate on Seedance. Resolve the live variant with `references/seedance-routing.md`, write shot prompts with `references/seedance-prompt-architecture.md`, and pull camera and reveal moves from `references/reveal-recipes.md`. For a single hero shot outside the series pipeline, use `workflows/cinematic-shot.md`.

## Banned

- Do not create a long prompt and submit a single long video.
- Do not invent a full asset library after video generation has begun.
- Do not skip style and character approvals.
- Do not use famous studio or franchise styles as direct imitation targets. Use production adjectives instead.

## Output

Deliver the production package in the conversation plus a brief status:

- story package ready
- asset list ready
- storyboard ready
- shot list ready
- approved for generation or waiting on approval
