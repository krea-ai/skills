# Edit QA Retakes

## Normalization

Before concatenation, normalize every clip:

- same resolution
- same FPS
- same codec
- same pixel format
- square pixels / SAR 1:1
- no audio unless explicitly retained

Normalize in the sandbox with FFmpeg before concatenating — re-encode every clip to
one FPS, size, codec, pixel format and SAR, then concat the normalized copies. Never
concatenate raw clips straight from the generator.

## Transition Smoothing

For chained AI clips, visible stutter often comes from frozen end/start frames. Default fixes:

- trim a few frames at boundaries
- use a short dissolve only when it serves the cut
- use one continuous audio bed instead of generated per-clip audio

Do not hide major continuity failures with transitions.

## QA Frame Sampling

Sample:

- first frame
- midpoint
- last frame
- boundary frames between clips

Compare against the storyboard and asset bible.

## Retake Log

Keep a running retake log with these columns:

```text
shot_id,priority,issue,fix_type,status,note
```

Priority:

- `blocking`: cannot deliver
- `major`: visible quality problem
- `minor`: acceptable if budget is exhausted

Fix types:

- `prompt`
- `keyframe`
- `asset`
- `edit`
- `audio`
- `model`

Statuses:

- `open`
- `submitted`
- `resolved`
- `waived`

## Delivery

Deliver only after:

- no blocking retakes remain
- final edit exists
- QA frames exist
- runtime is checked
- subtitles/audio are checked if present
- final path is reported clearly
