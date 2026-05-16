# Media Inputs

How to pass reference images, start frames, and audio files to Krea models through the MCP.

## Two paths: URL or upload

Krea generation tools accept media references as **URLs**. A local file becomes a URL via `upload_asset`.

### URL (when the user gave a hosted image)

If the user pasted a URL, pass it straight into the model's input:

```
generate_image(
    model="<id>",
    input={
        prompt: "transform to watercolor",
        imageUrl: "https://example.com/photo.jpg",
    },
    sync=true,
)
```

### Local file (use `upload_asset`)

When the user has a file on their machine:

```
import base64
with open("/path/to/photo.png", "rb") as f:
    data = base64.b64encode(f.read()).decode()

upload = upload_asset(
    filename="photo.png",
    mimeType="image/png",
    fileData=data,
)
# upload contains a URL. Pass it into the next call:

generate_image(
    model="<id>",
    input={prompt: "...", imageUrl: upload.url},
    sync=true,
)
```

**Important distinction:** `upload_asset` puts a file on Krea's servers so Krea models can use it as a reference. This is **not** the same as the agent reading an image. The agent reads images with its built-in vision (the `Read` tool on a local file path). Use both, for different jobs:

| What you need | How |
|---|---|
| The agent understands what's in the user's image | `Read` the local file (the agent's vision) |
| Krea uses the image as a generation reference | `upload_asset` → pass the returned URL into the model's input |

Often you do both: `Read` the file first to know the brief better, then `upload_asset` to actually pass it to the model.

## Single image vs multiple images

Each model declares which input shape it accepts. Use `get_model_schema(model=<id>)` to confirm — but the two common shapes are:

- **`imageUrl`** (string, singular) — one reference. Most models.
- **`imageUrls`** (array of strings) — multiple references. Models like the nano-banana-pro family use this for face injection from several photos.

## Reference image quality

Reference images that are too small (< 512px on the long side) often fail to anchor the generation well, even when the call succeeds. The model can fall back to a fresh text-to-image pass that ignores the reference. For best results:

- Use references ≥ 1024px on the long side
- For face injection, use clear front-facing photos at ≥ 1024px
- If you must use a smaller image, expect noisy results — and verify with vision before delivering

Example with multiple face references for a generated scene:

```
# Upload three face photos
face1 = upload_asset(filename="face1.png", mimeType="image/png", fileData=base64(...))
face2 = upload_asset(filename="face2.png", mimeType="image/png", fileData=base64(...))
face3 = upload_asset(filename="face3.png", mimeType="image/png", fileData=base64(...))

generate_image(
    model="<a model that accepts imageUrls>",
    input={
        prompt: "Three colleagues presenting at a conference, dramatic stage lighting",
        imageUrls: [face1.url, face2.url, face3.url],
        width: 1080,
        height: 1920,
    },
    sync=true,
)
```

## Video-specific media

Image-to-video models commonly accept:

- **`startImage`** — the first frame the video animates from
- **`endImage`** — an optional last frame (some Kling-family models)
- **`audio`** — a reference audio track for lipsync or soundtrack matching (model-dependent)

Use `get_model_schema(model=<id>)` to confirm the exact field names — different models name these differently.

Example: image-to-video on a model that accepts `startImage`:

```
upload = upload_asset(filename="hero.png", mimeType="image/png", fileData=base64(...))

job = generate_video(
    model="<id>",
    input={
        prompt: "camera slowly pushes in, fabric ripples",
        startImage: upload.url,
        duration: 6,
        aspectRatio: "16:9",
    },
    sync=false,
)
# then poll get_job(jobId=job.id) — see async-polling.md
```

## Audio reference

For models that support an `audio` input (lipsync, music-driven motion):

```
audio = upload_asset(
    filename="track.mp3",
    mimeType="audio/mpeg",
    fileData=base64(...),
)

job = generate_video(
    model="<id>",
    input={
        prompt: "person speaking",
        startImage: portrait.url,
        audio: audio.url,
    },
    sync=false,
)
```

Don't pass `generateAudio: true` to a model that takes a reference audio file — those are different mechanisms. Confirm with the schema.

## Common upload mistakes

- **Wrong mimeType.** `image/jpg` is invalid; use `image/jpeg`. For video, use `video/mp4`. For audio, `audio/mpeg` for mp3 and `audio/wav` for wav.
- **Passing a local path directly into `input.imageUrl`.** Krea doesn't fetch from the user's machine. Upload first, then use the returned URL.
- **Forgetting `Read` on the user's attached file.** If you upload without looking at the content, you might miss what the user actually wants done.

## File size and format

Krea accepts standard formats:

- **Images:** `image/png`, `image/jpeg`, `image/webp`
- **Video:** `video/mp4`, `video/quicktime`, `video/webm`
- **Audio:** `audio/mpeg`, `audio/wav`, `audio/ogg`, `audio/mp4`

Files >50 MB may fail to upload — re-encode at lower bitrate first if needed.
