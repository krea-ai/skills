# Image To Video Animate

## Trigger

User says "animate this image", "make this picture move", "image-to-video", "bring this still to life", or provides a still frame as the anchor for a short motion clip. When in doubt between this workflow and `narrative-video-long.md`, pick this if there is one source still and one output clip.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Motion**: camera move, subject action, atmosphere, product reveal.
- **Duration**: 4-5s draft or 8-10s polished, if supported.
- **Aspect**: keep source, 9:16, 16:9, 1:1.
- **Audio**: none unless the model supports and user requests it.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the still image with vision; identify what must remain stable.
2. **Cost-preflight** if estimated >100 CU or any premium video model is used.
3. Resolve `image-to-video / start frame anchored` from live `list_models`. If the resolved video model is a `seedance-2` variant, load `../../krea-generate/references/models/seedance-2.md` for prompt structure, media-path rules, `end_image` destination behavior, shadow-fail recovery, and pacing guardrails.
4. Inspect schema for `start_image`, `end_image`, duration, aspect, audio, and resolution fields.
5. Upload local still to Krea; use hosted URL.
6. Write a motion-only prompt. The still already defines the scene; prompt the movement.
7. Submit one async video job.
8. Poll with `../../krea-generate/references/progress-reporting.md`.
9. Download, sample frames, and check that the anchor subject did not drift.
10. **Deliver** with a one-line summary and QA notes.

### CLI

```bash
START=$(krea upload ./still.png --json | jq -r .url)
krea generate video -m "<image-to-video-model>" \
  --aspect 9:16 \
  --duration 5 \
  --start-image "$START" \
  -p "Camera slowly pushes in, hair and fabric move naturally, background light flickers subtly" \
  --json
```

### MCP fallback

```
upload_asset(filename, mimeType, fileData)
list_models()
get_model_schema(model="<image-to-video-model>")
generate_video(model="<image-to-video-model>", input={start_image, prompt, aspect_ratio, duration}, sync=false)
get_job(jobId=<id>)
```

## Banned

- Do not describe a totally different scene; animate what is in the still.
- Do not use social storyboard rules for a single still unless the user asks for a social sequence.
- Do not silently poll.
- Do not promise exact identity preservation through large motion.

## Cost & time

- Per-job: usually >100 CU for premium video; 3-15 minutes by model and duration.
- Typical full workflow: 1 still upload plus 1 video job.
- Hard caps the user should know about: duration and aspect options are model-specific; source aspect can bias output.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Subject morphs | Motion too aggressive | Use smaller motion and stronger preservation language |
| Output wrong aspect | Source aspect bias or missing field | Pad/crop source or pass accepted aspect field |
| Job exceeds timeout | Long video queue | Manual poll and report progress |
| User wants multiple cuts | Scope changed | Route to `narrative-video-long.md` |
