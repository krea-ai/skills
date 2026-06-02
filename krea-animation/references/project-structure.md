# Project Structure

Every production project should be file-based and inspectable. Generated media belongs in the project, not in the skill repo.

## Canonical Tree

```text
project/
  00_brief/
    brief.md
  01_bible/
    style/style-guide.md
    characters/characters.csv
    props/props.csv
    worlds/worlds.csv
  02_story/
    script.md
    beat-sheet.md
    storyboard.md
  03_shots/
    SC001/SH010/shot.md
  04_generation/
    manifests/assets.csv
    manifests/keyframes.csv
    manifests/video_jobs.csv
    manifests/durations.tsv
    manifests/concat-list.txt
    jobs/jobs.tsv
    jobs/results.tsv
  05_edit/
    audio/
    subtitles/
    shots_raw/
    shots_norm/
    final/
  06_qa/
    frame-samples/
    retakes.csv
    delivery-checklist.md
```

## Shot Statuses

Use these exact status values:

- `draft`
- `needs_assets`
- `needs_keyframes`
- `approved_for_video`
- `submitted`
- `complete`
- `retake`
- `approved_final`

Only `approved_for_video` and `retake` shots should be submitted. `retake` should include a `Retake note`.

## Per-Shot Required Fields

Each `shot.md` must include:

- `Shot ID`
- `Scene`
- `Duration`
- `Status`
- `Start image`
- `End image` or `Reference images`
- `Prompt`
- `Camera`
- `Action`
- `Continuity`
- `Audio`

The scripts parse simple Markdown fields shaped as `Field: value`. Keep one field per line for machine readability.

## Manifest Policy

- `assets.csv`: character, prop, world, style reference, URL/path, status.
- `keyframes.csv`: shot ID, keyframe path/URL, frame role, status.
- `video_jobs.csv`: shot ID, duration, model, aspect, start image, end image, reference images, prompt, status.
- `durations.tsv`: shot ID and duration for edit normalization.
- `retakes.csv`: shot ID, priority, issue, fix type, status, note.
