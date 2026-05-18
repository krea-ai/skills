# Narrative Video Long

## Trigger

User asks for a video longer than 15 seconds, a multi-scene story, montage, launch reel, explainer, music video, event recap, or a piece with intentional hard cuts. When in doubt between this workflow and `social-video-short.md`, pick this if the user needs separate scenes with different locations, subjects, or title cards.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Runtime**: target total duration and per-scene length.
- **Aspect**: 9:16, 16:9, 1:1, or platform-specific.
- **Scene list**: 4-8 scenes, each with subject/action/location.
- **References**: faces, products, brand, locations, music.
- **Audio**: silent, music bed, generated audio, or user-supplied track.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. **Cost-preflight** (mandatory - see `../references/cost-preflight.md`). Estimate number of still frames, number of video clips, and total wall-clock.
2. Plan a shot list before generation. Include title cards, scene order, aspect, duration, and refs per scene.
3. Resolve live archetypes: `high-fidelity image` or `image-to-image / face reference` for frames, `text in image` for titles, and `image-to-video / start frame anchored` for clips.
4. Generate still frames one scene at a time. Show each frame and wait for approval. Cheap still approval comes before expensive animation.
5. Regenerate weak frames until all scenes are approved.
6. Submit approved image-to-video jobs async, preferably in parallel after approval.
7. Poll with `../references/progress-reporting.md`; report aggregate status for multiple jobs.
8. Download clips and normalize every clip to the same resolution, FPS, codec, SAR, and no audio.
9. Concatenate with ffmpeg. Add one cohesive audio track at the end if requested.
10. Sample frames across the final edit and read with vision before delivery.
11. **Deliver** with final file path/URL, scene count, runtime, and QA notes.

### CLI

```bash
krea generate image -m "<high-fidelity-image>" \
  --aspect 9:16 \
  -p "<scene 1 frame prompt>" \
  --wait -o ./scene-01.png

FRAME=$(krea upload ./scene-01.png --json | jq -r .url)
krea generate video -m "<image-to-video-model>" \
  --aspect 9:16 \
  --duration 5 \
  --start-image "$FRAME" \
  -p "<motion-only prompt for scene 1>" \
  --json

ffmpeg -y -i scene-01.mp4 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libx264 -preset fast -crf 18 -r 24 -an scene-01-norm.mp4
```

### MCP fallback

```
list_models()
get_model_schema(model="<frame-model>")
generate_image(..., sync=true)
upload_asset(...)
get_model_schema(model="<image-to-video-model>")
generate_video(..., sync=false)
get_job(jobId=<id>)  # poll all jobs with progress pings
```

## Banned

- Do not animate unapproved frames.
- Do not submit all scenes before the user has seen the first frame.
- Do not concatenate clips without normalization.
- Do not keep random AI clip audio when assembling; strip and add one track.
- Do not call this workflow for a <=15s single social clip; use `social-video-short.md`.

## Cost & time

- Per-job: each video clip can be hundreds to 1500+ CU and 5-15 minutes.
- Typical full workflow: 4-8 stills plus 4-8 video clips; 30-90 minutes depending on approvals and queue.
- Hard caps the user should know about: long stories are many short jobs assembled; one huge continuous clip is not the default.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Scenes feel incoherent | No approved shot list | Re-plan and regenerate frames before animation |
| Clip specs mismatch | Different model outputs | Normalize with ffmpeg before concat |
| Audio is chaotic | Per-clip generated audio kept | Strip audio and add one bed |
| User dislikes scene after animation | Approval happened too late | Revert to still-frame approval gate |
