# LoRA Training

LoRA (Low-Rank Adaptation) training lets you teach a model a custom **style**, **object**, or **character** from a handful of example images. Once trained, the resulting `style_id` can be plugged into compatible Krea generation calls to produce on-brand or character-consistent output.

LoRA training is **not** exposed through the MCP today. Use the `scripts/train_style.py` companion script.

## Quick start

```bash
uv run scripts/train_style.py \
  --name "acme-brand" \
  --model flux_dev \
  --type Style \
  --trigger-word "acmestyle" \
  --urls-file brand-images.txt \
  --output-dir output/acme-brand
```

`brand-images.txt` is a text file with one URL per line:

```
https://your-cdn.com/brand-photo-01.jpg
https://your-cdn.com/brand-photo-02.jpg
# ... 15-20 total
```

The script:

1. Loads the URLs (and/or local files passed via `--urls`).
2. If any are local file paths, uploads them via Krea's assets API to get hosted URLs.
3. HEAD-checks every URL to catch 404s before wasting compute.
4. Submits the training job and polls until done (15–45 minutes typical).
5. Prints the `style_id` to stdout and saves `training-manifest.json` to `--output-dir`.

## Parameters

| Flag | Description | Default |
|---|---|---|
| `--name` | Style name (required) | — |
| `--model` | Base model: `flux_dev`, `flux_schnell`, `wan`, `wan22`, `qwen`, `z-image` | `flux_dev` |
| `--type` | LoRA type: `Style`, `Object`, `Character`, `Default` | `Style` |
| `--urls` | Training image URLs (space-separated) | — |
| `--urls-file` | Text file with one URL per line | — |
| `--trigger-word` | Word to activate the LoRA in prompts | — |
| `--learning-rate` | Learning rate | 0.0001 |
| `--max-train-steps` | Max training steps | 1000 |
| `--batch-size` | Training batch size | 1 |
| `--timeout` | Polling timeout in seconds | 3600 |
| `--skip-validation` | Skip URL HEAD-check | false |
| `--output-dir` | Where to save `training-manifest.json` | — |
| `--api-key` | Krea API key | env `KREA_API_KEY` |

## Type selection

- **`Style`** — a visual aesthetic (color palette, lighting style, brand look). 15–20 varied images of that aesthetic across different subjects.
- **`Object`** — a specific product or item that should appear across new scenes. 10–20 photos of that object from multiple angles.
- **`Character`** — a specific person or character (face, body, clothing). 15–30 reference photos from varied angles, expressions, and lighting.
- **`Default`** — the model picks based on the training data. Use only when none of the above clearly applies.

## Training image guidance

- **Count.** 15–20 images is the sweet spot. Fewer than 10 often underfits; more than 30 is rarely worth the extra training time.
- **Variety.** For `Style`, vary subjects but keep the aesthetic consistent. For `Object`, vary angles and backgrounds. For `Character`, vary expressions, lighting, and outfits while keeping the face consistent.
- **Quality.** Sharp, high-resolution images (≥1024px on the long side). Blurry or low-res inputs propagate as visual noise into the LoRA.
- **Backgrounds.** Mix neutral and contextual backgrounds so the LoRA learns what's the subject and what's the scene.

## Trigger words

The trigger word is a token the model learns to associate with the LoRA. When included in a prompt at generation time, it activates the trained style.

- Pick something **unique and unambiguous** — avoid common English words.
- Examples: `acmestyle`, `brandxbrand`, `personcharacter`, `productitem01`.
- The trigger does not need to mean anything in English; the model learns the association.

## Using the trained style at generation time

The `style_id` is printed when training completes. Save it (the manifest does this automatically).

Pass it into compatible image-generation calls. The exact input field depends on the model — check `mcp__krea-public-api__get_model_schema(model=<id>)` to confirm. Common shapes:

- `styleId: "<id>"` and `styleStrength: 1.0`
- Or `styles: [{ id: "<id>", strength: 1.0 }]`

Include the trigger word in the prompt to activate the style:

```
generate_image(
  model="<style-aware image model>",
  input={
    prompt: "acmestyle product on clean white background, studio lighting",
    styleId: "style_abc123",
    styleStrength: 1.0,
  },
  sync=true,
)
```

**Strength tuning:**
- `0.5` — subtle hint of the style; mostly the base model's behavior
- `1.0` — balanced (default)
- `1.5` — strong; the LoRA dominates the look
- `2.0` — usually overdriven; outputs look uniform

## Saving the style_id for the project

After a successful training, pin the style ID in `KREA_PREFERENCES.md` so future sessions reuse it:

```markdown
## Krea preferences

- Brand style: `style_abc123` (trigger word: `acmestyle`, trained 2026-05-13)
- Default image archetype: high-fidelity with the brand style applied
```

## Troubleshooting

- **`Need at least 3 training images, got X`** — the API requires a minimum. 15+ recommended.
- **HEAD-check failures** — the script lists every bad URL. Fix the URLs or use `--skip-validation` if you know they're fine (e.g. signed URLs that reject HEAD).
- **Training timed out** — bump `--timeout`. Large datasets or `flux_dev` with high steps can run 30+ minutes.
- **Trained style ignores the trigger word** — usually a sign the LoRA underfit. Retrain with more images or `--max-train-steps 1500`.
- **Trained style overpowers everything** — overfit. Use `style_strength: 0.5–0.7` at generation time, or retrain with fewer steps (`--max-train-steps 600`).
