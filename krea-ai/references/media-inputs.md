# Media Inputs

How to pass reference images, start frames, and audio files to Krea models through the CLI or MCP.

## Asset rule: upload before generation

Krea generation tools accept media references as **URLs**, but model input validators intentionally restrict which asset hosts can be used. Treat local files and arbitrary external URLs as source material, not as final model inputs. Before passing a media URL into fields such as `imageUrl`, `image_url`, `imageUrls`, `image_urls`, `referenceImages`, `reference_images`, `startImage`, `start_image`, `endImage`, `end_image`, `styleImages[].url`, `style_images[].url`, `image_style_references[].url`, or audio/video reference fields, first make sure it is a Krea-hosted or explicitly approved asset URL.

If the URL is not already a Krea asset URL, download it to a local temp file, upload it with `krea upload` or MCP `upload_asset`, then pass the returned Krea URL to the generation model. This is the skill-level fix for `Invalid asset URL` failures.

### Hosted URL from the user

When the user pasted an image/video/audio URL, do not pass it straight into generation unless it is already a Krea/approved asset host. Rehost it through Krea first:

```bash
curl -L "https://example.com/photo.jpg" -o /tmp/krea-reference.jpg
REF_URL=$(krea upload /tmp/krea-reference.jpg --json | jq -r .url)

krea generate image -m "<image-to-image-model>" \
  -i imageUrl="$REF_URL" \
  -p "transform to watercolor" \
  --wait -o ./out.png
```

Use the field name accepted by the selected model schema. For example, Kontext uses a singular `imageUrl`, Seedance-style video models may use `referenceImages`, Seedream-style references may use `styleImages[].url` or `style_images[].url`, and Krea 2 style references use `image_style_references[].url`.

### Local file (use upload)

When the user has a file on their machine:

```python
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
| Krea uses the image as a generation reference | `krea upload` or `upload_asset` -> pass the returned Krea URL into the model's input |

Often you do both: `Read` the file first to know the brief better, then `upload_asset` to actually pass it to the model.

## CLI reference pattern

The CLI is the default surface. For local files or downloaded external URLs, upload once, resolve the Krea-hosted URL, then pass that URL using the field accepted by the selected model schema.

```bash
REF_URL=$(krea upload ./reference.png --json | jq -r .url)

krea models show "<model-id>" --json

# Singular reference field, when schema supports imageUrl/image:
krea generate image -m "<model-id>" \
  -i imageUrl="$REF_URL" \
  -p "<prompt>" \
  --wait -o ./out.png

# Multi-reference field, when schema supports imageUrls/imageUrls-like arrays:
krea generate image -m "<model-id>" \
  -i imageUrls="[\"$REF_URL\"]" \
  -p "<prompt>" \
  --wait -o ./out.png

# Start-frame video, when schema supports startImage/start-image:
krea generate video -m "<model-id>" \
  --aspect 9:16 \
  -i startImage="$REF_URL" \
  -p "<motion prompt>" \
  --json

# Krea 2 style reference, when schema supports image_style_references:
krea generate image -m krea/krea-2/large \
  --aspect 1:1 \
  -i image_style_references='[{"url":"'"$REF_URL"'","strength":0.5}]' \
  -p "<prompt>" \
  --wait -o ./out.png
```

Do not guess field names. Always inspect the live model schema first; different models use different reference fields.

Krea 2 image endpoints use `aspect_ratio` + `resolution` in the public API. The CLI maps `--aspect` for the default Krea 2 flow and supplies the default `resolution=1K`; raw MCP or `--input` calls should use those public names directly. Krea 2 style references use `image_style_references` items shaped as `{ "url": "...", "strength": 0.5 }`.

## Field-name crosswalk

The hosting rule applies regardless of naming convention. Always inspect the live schema, then put Krea-hosted URLs into whichever field it declares:

| Field family | Common shapes |
|---|---|
| Single image reference | `imageUrl`, `image_url` |
| Multiple image references | `imageUrls`, `image_urls`, `referenceImages`, `reference_images` |
| Video frame anchors | `startImage`, `start_image`, `endImage`, `end_image` |
| Style/reference objects | `styleImages[].url`, `style_images[].url`, `image_style_references[].url` |
| Audio/video references | Schema-specific URL fields such as `referenceAudios`, `referenceVideos`, or snake_case equivalents |

## Which URLs can be passed directly?

Pass direct URLs only when they are already Krea-hosted or an explicitly approved Krea asset host. Otherwise, use the upload step above. Product pages, CDN images, GitHub raw images, S3 links you do not control, and ordinary `https://example.com/photo.jpg` references are not safe to pass directly into generation inputs; many models return HTTP 422 `Invalid asset URL`.

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
- **Passing an arbitrary external URL directly into generation.** Download it, upload it to Krea, then use the Krea-hosted URL.
- **Forgetting `Read` on the user's attached file.** If you upload without looking at the content, you might miss what the user actually wants done.

## File size and format

Krea accepts standard formats:

- **Images:** `image/png`, `image/jpeg`, `image/webp`
- **Video:** `video/mp4`, `video/quicktime`, `video/webm`
- **Audio:** `audio/mpeg`, `audio/wav`, `audio/ogg`, `audio/mp4`

Files >50 MB may fail to upload — re-encode at lower bitrate first if needed.
