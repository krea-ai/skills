# Storyboard And Shot List

## Shot IDs

Use stable IDs:

```text
SC001_SH010
SC001_SH020
SC002_SH010
```

Use increments of 10 so inserts can fit between shots.

## Storyboard Requirements

Each storyboard beat needs:

- time range
- shot size
- action
- camera
- subject
- emotional function
- dialogue or no dialogue
- sound cue
- continuity hook

## Shot Size Vocabulary

- `EWS`: extreme wide shot
- `WS`: wide shot
- `MS`: medium shot
- `CU`: close-up
- `ECU`: extreme close-up
- `OTS`: over-the-shoulder
- `POV`: point of view
- `INSERT`: object or detail shot

## Camera Vocabulary

Prefer concrete camera language:

- locked
- slow push-in
- dolly left/right
- pan
- tilt
- rack focus
- handheld drift
- top-down
- low angle
- tracking side-on

## Continuity Hooks

Use hooks intentionally:

- hard cut
- match on action
- graphic match
- color match
- eyeline match
- J-cut
- L-cut
- dissolve
- fade to black

Every hook should serve story, rhythm, or clarity. Do not add transitions as decoration.

## Duration Planning

For AI video models, prefer 4-8 second shots unless the live schema supports longer and the action truly needs it. Long sequences are many controlled clips assembled in edit.

## Prompt Transfer

Each shot list entry should carry enough information to submit its video job:

- start image
- end image or reference images
- duration
- aspect
- prompt
- audio policy
- status
