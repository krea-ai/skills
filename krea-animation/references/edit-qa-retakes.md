# Edit QA Retakes

## Normalization

Never concatenate raw clips straight from the generator — re-encode every clip to one
resolution, FPS, codec, pixel format and SAR (square pixels) first, dropping audio
unless it is explicitly retained:

```bash
# Set W and H to the deliverable's own aspect — 1920x1080 for 16:9, 1080x1920 for
# 9:16, 2560x1080 for 21:9. `-s` alone stretches a clip that does not match.
W=1080; H=1920
for f in shot-*.mp4; do
  ffmpeg -y -i "$f" -r 24 \
    -vf "scale=$W:$H:force_original_aspect_ratio=decrease,pad=$W:$H:(ow-iw)/2:(oh-ih)/2,setsar=1" \
    -c:v libx264 -pix_fmt yuv420p -an "norm-$f"
done
printf "file '%s'\n" norm-shot-*.mp4 > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy sequence.mp4
```

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
