---
name: krea-ai
description: "Generate images, videos, upscale/enhance images, and train LoRA styles using the Krea.ai API. Supports 20+ image models (Flux, Imagen, GPT Image, Ideogram, Seedream), 7 video models (Kling, Veo, Hailuo, Wan), and 3 upscalers (Topaz up to 22K). Use when the user wants to generate images, create videos, upscale images, train custom LoRA styles, or run multi-step creative pipelines."
license: MIT
---

# Krea AI — Image, Video & Enhancement Generation

Generate images, videos, upscale/enhance images, and train LoRA styles using the Krea.ai API. Supports 20+ image models (Flux, Imagen, GPT Image, Ideogram, Seedream...), 7 video models (Kling, Veo, Hailuo, Wan), and 3 upscalers (Topaz up to 22K).

**IMPORTANT:** Do NOT invent model names. Run `list_models.py` to get the **live** list of models, CU costs, and accepted parameters from the Krea API's OpenAPI spec. All scripts resolve models dynamically from the spec — there are no hardcoded endpoint tables. Scripts also accept full endpoint paths from `list_models.py --json` output (e.g. `--model /generate/image/google/imagen-4-ultra`).

## Usage

Scripts are in the `scripts/` directory alongside this file. Run them with `uv run` from the user's working directory so output files are saved where the user expects.

**Generate image:**
```bash
uv run scripts/generate_image.py --prompt "your description" --filename "output.png" [--model nano-banana-2] [--width 1024] [--height 1024] [--api-key KEY]
```

**Generate video:**
```bash
uv run scripts/generate_video.py --prompt "your description" --filename "output.mp4" [--model veo-3.1-fast] [--duration 5] [--aspect-ratio 16:9] [--api-key KEY]
```

**Enhance/upscale image:**
```bash
uv run scripts/enhance_image.py --image-url "https://..." --filename "upscaled.png" --width 4096 --height 4096 [--enhancer topaz-standard-enhance] [--api-key KEY]
```

**Train a LoRA style:**
```bash
uv run scripts/train_style.py --name "my-style" --urls-file images.txt [--model flux_dev] [--type Style] [--trigger-word "mystyle"] [--api-key KEY]
```

**List available models:**
```bash
uv run scripts/list_models.py [--type image|video|enhance]
```

**Run a multi-step pipeline:**
```bash
uv run scripts/pipeline.py --pipeline pipeline.json [--api-key KEY]
```

**Check job status:**
```bash
uv run scripts/get_job.py --job-id "uuid" [--api-key KEY]
```

**Important:** Always run from the user's current working directory so files are saved where the user is working.

## Default Workflow (draft → iterate → final)

Goal: fast iteration without burning CU on expensive models until the prompt is right.

- **Draft (cheap/fast):** use `--model z-image` or `--model flux-1-dev` (3-5 CU, ~5s) for quick iteration
  ```bash
  uv run scripts/generate_image.py --prompt "<draft prompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --model flux-1-dev
  ```

- **Iterate:** adjust prompt, keep trying with cheap models

- **Final (high quality):** switch to `--model gpt-image` or `--model nano-banana-pro`
  ```bash
  uv run scripts/generate_image.py --prompt "<final prompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --model nano-banana-pro
  ```

## Available Models

Models, CU costs, and accepted body fields are fetched **live** from the Krea API's OpenAPI spec (`/openapi.json`). Run `list_models.py` to see what's currently available:

```bash
uv run scripts/list_models.py                     # all models with params
uv run scripts/list_models.py --type image         # image models only
uv run scripts/list_models.py --json               # machine-readable
```

Short aliases (e.g. `flux` for `flux-1-dev`) are maintained for convenience. The scripts resolve them automatically via the spec. If a model isn't in the alias list, pass the full OpenAPI model ID or endpoint path.

### Model selection guidance

Map user requests for **images**:
- "fast", "quick", "cheap" → `flux-1-dev` or `z-image`
- "high quality", "best" → `nano-banana-pro` or `gpt-image`
- "text in image", "typography" → `ideogram-3`
- "photorealistic" → `seedream-4` or `nano-banana-pro`
- No preference → `nano-banana-2`

Map user requests for **video**:
- "fast" → `hailuo-2.3`
- "cinematic", "high quality" → `veo-3.1`
- "with sound", "with audio" → `veo-3` with `--generate-audio`
- No preference → `veo-3.1-fast`

**Enhancers:** `topaz-standard-enhance` (faithful upscaling, default), `topaz-generative-enhance` (creative enhancement), `topaz-bloom-enhance` (adding creative details).

## Image Generation Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--model` | Model ID or alias (run list_models.py) | `nano-banana-2` |
| `--prompt` | Text description (required) | — |
| `--filename` | Output filename (required) | — |
| `--width` | Width in pixels (512-4096) | 1024 |
| `--height` | Height in pixels (512-4096) | 1024 |
| `--aspect-ratio` | Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:2, etc.) | — |
| `--resolution` | 1K, 2K, 4K (nano-banana models) | — |
| `--seed` | Seed for reproducibility | — |
| `--image-url` | Input image URL or local file path for image-to-image | — |
| `--style-id` | LoRA style ID to apply | — |
| `--style-strength` | LoRA strength (-2 to 2) | 1.0 |
| `--batch-size` | Number of images (1-4) | 1 |
| `--steps` | Inference steps, 1-100 (flux models) | 25 |
| `--guidance-scale` | Guidance scale, 0-24 (flux models) | 3 |
| `--quality` | low/medium/high/auto (gpt-image) | auto |
| `--output-dir` | Output directory | cwd |
| `--api-key` | Krea API token | — |

## Video Generation Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--model` | Model ID or alias (run list_models.py) | `veo-3.1-fast` |
| `--prompt` | Text description (required) | — |
| `--filename` | Output filename (required) | — |
| `--duration` | Duration in seconds | 5 |
| `--aspect-ratio` | 16:9, 9:16, 1:1 | 16:9 |
| `--start-image` | URL or local file path for image-to-video | — |
| `--end-image` | End frame URL (kling only) | — |
| `--resolution` | 720p, 1080p (veo only) | 720p |
| `--mode` | std, pro (kling only) | std |
| `--generate-audio` | Generate audio (veo-3 only) | false |
| `--output-dir` | Output directory | cwd |
| `--api-key` | Krea API token | — |

## Enhancement Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--enhancer` | Enhancer ID (run list_models.py --type enhance) | `topaz-standard-enhance` |
| `--image-url` | Source image URL or local file path (required) | — |
| `--filename` | Output filename (required) | — |
| `--width` | Target width (required) | — |
| `--height` | Target height (required) | — |
| `--enhancer-model` | Sub-model variant | Standard V2 |
| `--creativity` | 1-6 (generative) or 1-9 (bloom) | — |
| `--face-enhancement` | Enable face enhancement | false |
| `--sharpen` | Sharpening 0-1 | — |
| `--denoise` | Denoising 0-1 | — |
| `--scaling-factor` | Upscaling factor 1-32 | — |
| `--output-format` | png, jpg, webp | png |
| `--output-dir` | Output directory | cwd |
| `--api-key` | Krea API token | — |

## LoRA Training Parameters

| Param | Description | Default |
|-------|-------------|---------|
| `--name` | Style name (required) | — |
| `--model` | Base model: flux_dev, flux_schnell, wan, qwen, z-image | `flux_dev` |
| `--type` | LoRA type: Style, Object, Character, Default | `Style` |
| `--urls` | Training image URLs (space-separated) | — |
| `--urls-file` | Text file with one URL per line | — |
| `--trigger-word` | Trigger word to activate the LoRA in prompts | — |
| `--learning-rate` | Learning rate | 0.0001 |
| `--max-train-steps` | Max training steps | 1000 |
| `--batch-size` | Training batch size | 1 |
| `--timeout` | Polling timeout in seconds | 3600 |
| `--skip-validation` | Skip URL HEAD-check validation | false |
| `--output-dir` | Directory to save training manifest | — |
| `--api-key` | Krea API token | — |

Training requires 3-2000 images. The script validates all URLs before submitting. Training takes 15-45 minutes. On completion, the style ID is printed to stdout and a `training-manifest.json` is saved if `--output-dir` is set.

Use the style ID with `--style-id` in `generate_image.py`:
```bash
uv run scripts/generate_image.py --prompt "mystyle product on white background" --style-id "style_abc123" --model flux-1-dev --filename "branded.png"
```

## API Key

Scripts check for API key in this order:
1. `--api-key` argument (use if user provided key in chat)
2. `KREA_API_TOKEN` environment variable

If neither is available, the script exits with an error message.

## Preflight + Common Failures

**Preflight:**
- `command -v uv` (must exist)
- `test -n "$KREA_API_TOKEN"` (or pass `--api-key`)

**Common failures:**
- `Error: No API key` → set `KREA_API_TOKEN` or pass `--api-key`
- `402 Insufficient credits` → top up compute units at https://krea.ai/settings/billing
- `402 This model requires a higher plan` → model needs a paid plan upgrade at https://krea.ai/settings/billing
- `429 Too many requests` → concurrent job limit reached; scripts auto-retry up to 3 times with backoff
- `Job failed` → check prompt for content moderation issues, try different wording

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.ext`

- Timestamp: current date/time in `yyyy-mm-dd-hh-mm-ss` (24h format)
- Name: descriptive lowercase text with hyphens (1-5 words)
- Extension: `.png` for images, `.mp4` for videos

**Examples:**
- Prompt "A cyberpunk cat" → `2026-03-31-14-23-05-cyberpunk-cat.png`
- Prompt "waves on a beach" → `2026-03-31-15-30-12-beach-waves.mp4`

## Prompt Handling

**For generation:** Pass user's description as-is to `--prompt`. Only rework if clearly insufficient.

**For image-to-image:** Use `--image-url` with the source image and describe the desired transformation in `--prompt`.

**For video from image:** Use `--start-image` with the source image and describe the desired motion/action in `--prompt`.

Preserve user's creative intent in all cases.

## Output

- Scripts download the result and save it to the current directory (or `--output-dir`)
- Script outputs the full path to the generated file
- **Do not read the image/video back** — just inform the user of the saved path
- If `--batch-size` > 1, files are saved as `name-1.png`, `name-2.png`, etc.

## Examples

**Quick draft image:**
```bash
uv run scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2026-03-31-14-23-05-japanese-garden.png"
```

**High quality final:**
```bash
uv run scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms, golden hour lighting" --filename "2026-03-31-14-25-30-japanese-garden-final.png" --model nano-banana-pro --resolution 4K
```

**Image-to-image edit:**
```bash
uv run scripts/generate_image.py --prompt "transform to watercolor painting style" --filename "2026-03-31-14-30-00-watercolor.png" --image-url "https://example.com/photo.jpg" --model nano-banana-pro
```

**Generate video:**
```bash
uv run scripts/generate_video.py --prompt "A majestic eagle soaring over snow-capped mountains at sunrise" --filename "2026-03-31-15-00-00-eagle-mountains.mp4" --model veo-3 --duration 8 --generate-audio
```

**Upscale image to 4K:**
```bash
uv run scripts/enhance_image.py --image-url "https://example.com/photo.jpg" --filename "2026-03-31-15-10-00-upscaled.png" --width 4096 --height 4096 --enhancer topaz
```

**Train a LoRA style:**
```bash
uv run scripts/train_style.py --name "acme-brand" --model flux_dev --type Style --trigger-word "acmestyle" --urls-file brand-images.txt --output-dir output/acme-brand
```

**List models:**
```bash
uv run scripts/list_models.py --type image
```

## Pipelines (Multi-Step Workflows)

For multi-step workflows (generate → enhance → animate, fan_out branching, template variables, parallel execution, resume, dry-run), see [PIPELINES.md](PIPELINES.md).

Quick example:
```bash
uv run scripts/pipeline.py --pipeline '{"steps":[{"action":"generate_image","prompt":"a cat astronaut","filename":"cat"},{"action":"enhance","use_previous":true,"enhancer":"topaz-standard-enhance","width":4096,"height":4096,"filename":"cat-4k"}]}'
```
