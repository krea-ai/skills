# Krea AI Skill

Generate images, videos, upscale/enhance with 20+ AI models through the [Krea.ai](https://krea.ai) API. Works with Claude Code, Cursor, Copilot, Codex, Windsurf, and other AI agents.

## Install

### Agent Skills (recommended)

```bash
npx skills add krea-ai/skills
```

Works with Claude Code, Cursor, Copilot, Codex, Windsurf, and [many other agents](https://skills.sh).

### Manual

```bash
git clone https://github.com/krea-ai/skills.git
export KREA_API_TOKEN="your-token-here"
```

Then ask your agent: *"Generate an image of a cyberpunk city at night"*

## Setup

1. Get your API token at [krea.ai/settings/api-tokens](https://krea.ai/settings/api-tokens)
2. Set `KREA_API_TOKEN` environment variable (or pass `--api-key` to any script)
3. Ensure `uv` is installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Available Scripts

| Script | Description |
|--------|-------------|
| `scripts/generate_image.py` | Generate images with 20+ models (Flux, Imagen, GPT Image, etc.) |
| `scripts/generate_video.py` | Generate videos with Veo, Kling, Hailuo, Wan, Sora |
| `scripts/enhance_image.py` | Upscale/enhance with Topaz (up to 22K resolution) |
| `scripts/list_models.py` | List all models live from the API |
| `scripts/pipeline.py` | Multi-step workflows with fan_out, templates, parallel execution |
| `scripts/train_style.py` | Train custom LoRA styles on brand images |
| `scripts/get_job.py` | Check job status |
| `scripts/krea_helpers.py` | Shared helpers (retry, polling, error handling) |

All scripts use `uv run` (inline dependencies, no install needed).

## Documentation

- **[SKILL.md](SKILL.md)** — Full reference: models, parameters, LoRA training, error handling
- **[PIPELINES.md](PIPELINES.md)** — Pipeline reference: JSON format, examples, advanced features
- **[COOKBOOK.md](COOKBOOK.md)** — Real-world recipes: ad campaigns, brand LoRA training, product-to-video pipelines, storyboard production, creative iteration

## Quick Examples

```bash
# Generate an image
uv run scripts/generate_image.py --prompt "A cyberpunk cat" --filename "cat.png"

# Generate a video with audio
uv run scripts/generate_video.py --prompt "Ocean waves at sunset" --filename "waves.mp4" --generate-audio

# Upscale to 4K
uv run scripts/enhance_image.py --image-url "https://..." --filename "upscaled.png" --width 4096 --height 4096

# List available models (live from API)
uv run scripts/list_models.py

# Run a multi-step pipeline
uv run scripts/pipeline.py --pipeline pipeline.json --dry-run
```

## API Key

Get your token at [krea.ai/settings/api-tokens](https://krea.ai/settings/api-tokens). Set as `KREA_API_TOKEN` environment variable or pass `--api-key` to any script.

## License

MIT
