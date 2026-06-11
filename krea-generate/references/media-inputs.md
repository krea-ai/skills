# Media Inputs

How to pass reference images, start frames, and audio files to Krea models through the CLI or MCP.

## Asset rule: upload before generation

Krea generation tools accept media references as **URLs**, but model input validators intentionally restrict which asset hosts can be used. Treat local files and arbitrary external URLs as source material, not as final model inputs. Before passing a media URL into fields such as `image_url`, `image_urls`, `reference_images`, `start_image`, `end_image`, `style_images[].url`, `image_style_references[].url`, or MCP-translated camelCase equivalents, first make sure it is a Krea-hosted or explicitly approved asset URL.

If the URL is not already a Krea asset URL, download it to a local temp file, upload it with `krea upload` or MCP `upload_asset`, then pass the returned Krea URL to the generation model. This is the skill-level fix for `Invalid asset URL` failures.

### Hosted URL from the user

When the user pasted an image/video/audio URL, do not pass it straight into generation unless it is already a Krea/approved asset host. Rehost it through Krea first:

1. Download the URL to a temporary local file.
2. Upload that file through the available Krea surface.
3. Pass the returned Krea-hosted URL into the reference field declared by the selected model schema.

Use the field name accepted by the selected model schema. CLI schemas commonly use snake_case, such as singular image-reference fields, array reference fields, frame-anchor fields, or structured style-reference arrays. MCP tools may expose camelCase equivalents; verify the connected tool schema before using MCP.

### Local file (use upload)

When the user has a file on their machine:

1. Read the file with the agent's vision if visual understanding matters.
2. Upload the file through the available Krea surface.
3. Use the returned Krea URL in the selected model's schema-confirmed media field.

**Important distinction:** `upload_asset` puts a file on Krea's servers so Krea models can use it as a reference. This is **not** the same as the agent reading an image. The agent reads images with its built-in vision (the `Read` tool on a local file path). Use both, for different jobs:

| What you need | How |
|---|---|
| The agent understands what's in the user's image | `Read` the local file (the agent's vision) |
| Krea uses the image as a generation reference | `krea upload` or `upload_asset` -> pass the returned Krea URL into the model's input |

Often you do both: read the file first to know the brief better, then upload it to Krea so the model can use it.

## CLI upload pattern

When using CLI, upload local files or downloaded external URLs once, resolve the Krea-hosted URL, then pass that URL using the field accepted by the selected model schema.

Do not guess field names or CLI flags. Discover upload and generation syntax from the installed CLI help, then inspect the live model schema first; different models use different reference fields.

## Field-name crosswalk

The hosting rule applies regardless of naming convention. Always inspect the live schema, then put Krea-hosted URLs into whichever field it declares:

| Field family | Common shapes |
|---|---|
| Single image reference | `image_url` or MCP-translated `imageUrl` |
| Multiple image references | `image_urls`, `reference_images`, or MCP-translated equivalents |
| Video frame anchors | `start_image`, `end_image`, or MCP-translated equivalents |
| Style/reference objects | `style_images[].url`, `image_style_references[].url`, or MCP-translated equivalents |
| Audio/video references | Schema-specific URL fields such as `reference_audios`, `reference_videos`, or MCP-translated equivalents |

## Which URLs can be passed directly?

Pass direct URLs only when they are already Krea-hosted or an explicitly approved Krea asset host. Otherwise, use the upload step above. Product pages, CDN images, GitHub raw images, S3 links you do not control, and ordinary `https://example.com/photo.jpg` references are not safe to pass directly into generation inputs; many models return HTTP 422 `Invalid asset URL`.

## Single image vs multiple images

Each model declares which input shape it accepts. Inspect the selected model schema through the available Krea surface to confirm. Common shapes are:

- **`image_url` / MCP `imageUrl`** (string, singular) - one reference.
- **`image_urls` / MCP `imageUrls`** (array of strings) - multiple references.
- **`reference_images`** (array of strings) - common for video reference images.

## Reference image quality

Reference images that are too small (< 512px on the long side) often fail to anchor the generation well, even when the call succeeds. The model can fall back to a fresh text-to-image pass that ignores the reference. For best results:

- Use references ≥ 1024px on the long side
- For face injection, use clear front-facing photos at ≥ 1024px
- If you must use a smaller image, expect noisy results — and verify with vision before delivering

Example with multiple face references for a generated scene:

1. Upload each face photo through the available Krea surface.
2. Select a live model whose schema supports multiple image references.
3. Pass the returned Krea URLs in the schema-confirmed multi-reference field.

## Video-specific media

Image-to-video models commonly accept:

- **`start_image` / MCP `startImage`** - the first frame the video animates from
- **`end_image` / MCP `endImage`** - an optional last frame
- **`audio` or reference-audio fields** - a reference audio track for lipsync or soundtrack matching, model-dependent

Inspect the selected model schema through the available surface to confirm exact field names; different models name these differently.

## Audio reference

For models that support an `audio` input (lipsync, music-driven motion):

1. Upload the audio file through the available Krea surface.
2. Confirm the selected model's audio-reference field from its schema.
3. Pass the returned Krea URL in that schema-confirmed field.

Don't pass `generate_audio=true` or MCP `generateAudio: true` to a model that takes a reference audio file - those are different mechanisms. Confirm with the schema.

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
