# Brand Consistency via LoRA

When a brand needs visual consistency across many generations — same color treatment, same compositional language, same vibe — train a brand LoRA once and apply the resulting `style_id` to every subsequent generation. This is the difference between "looks AI-generated" and "looks on-brand."

## When to use this

- Generating 50+ marketing assets per quarter for the same brand
- Brand has a recognizable visual signature that generic models don't reproduce well
- Stakeholders push back with "this looks like AI, not us"
- Multiple agents / sessions need to produce consistent output without re-explaining the brand each time

## When NOT to use this

- One-off generations where consistency across a series doesn't matter
- Brands that don't have a strong visual signature yet (LoRA needs 15-20 images of consistent style; if the brand visual is still evolving, train later)
- When the brand is happy with generic high-fidelity output

## Workflow

### Step 1: Collect 15-20 brand images

Quality matters more than quantity. The training set should:

- All share the same visual signature (color, composition, lighting, mood)
- Vary in subject so the LoRA learns the *style*, not the *content*
- Be high-resolution (≥1024px on the long side)
- Avoid heavy text overlays (LoRA learns those as part of the style — usually unwanted)

If the brand has fewer than 15 strong images, the LoRA will underfit. Train on what you have but expect 0.6-0.7 style strength to feel right rather than 1.0.

### Step 2: Train

Use the `train_style.py` script that ships with `krea-ai`. Resolve its absolute path first — agents typically run from the user's working directory, not the skill directory:

```bash
# Find the script in the installed skill location
SKILL_TRAIN=$(find ~/.claude/skills ~/.cursor/plugins ~/.codex/plugins 2>/dev/null \
  -name 'train_style.py' -path '*krea-ai*' | head -1)
[ -z "$SKILL_TRAIN" ] && { echo "krea-ai/scripts/train_style.py not found"; exit 1; }

uv run "$SKILL_TRAIN" \
  --name "acmebrand-2026q2" \
  --model flux_dev \
  --type Style \
  --trigger-word "acmebrand" \
  --urls-file acmebrand-references.txt \
  --max-train-steps 1000 \
  --output-dir output/acmebrand-2026q2
```

`acmebrand-references.txt` is one URL per line, in the user's working directory. Local files work too — the script uploads them automatically.

For training options including `--type Object` (specific product) and `--type Character` (face / person consistency), see `../../krea-ai/references/lora-training.md`.

Training takes 15-45 minutes. The script saves a `training-manifest.json` and prints the `style_id` on stdout.

### Step 3: Pin the style ID

Add to the project's `KREA_PREFERENCES.md` (or the user-level `~/.claude/CLAUDE.md` `## Krea preferences` section):

```markdown
## Krea preferences

- Brand style ID: style_abc123 (trigger: acmebrand, trained 2026-05-16)
- Default style strength: 0.85
- Skip cost confirmation under 100 CU
```

Future agent invocations read this and apply the style automatically.

### Step 4: Apply in generations

Include the style in every product / marketing generation:

```
result = generate_image(
  model=<style-aware image model from list_models>,
  input={
    prompt: "acmebrand premium product hero shot of [PRODUCT], [DESCRIPTION]",
    imageUrl: <product reference>,
    styleId: "style_abc123",
    styleStrength: 0.85,
    aspectRatio: "1:1"
  },
  sync=true
)
```

Notes:

- The trigger word ("acmebrand") in the prompt is what activates the style — include it
- `styleStrength` is the dial. 0.5 = subtle hint. 0.85 = balanced. 1.0+ = the style dominates
- Different models accept the style field with different names — check the schema via `get_model_schema`

## Tuning style strength

Start at 0.85 and adjust:

| Symptom | Strength change |
|---|---|
| Output looks generic, not on-brand | Increase to 1.0-1.2 |
| Output is too stylized, loses product accuracy | Decrease to 0.6-0.7 |
| Product is recognizable but composition is wrong | Strength is fine, adjust the prompt |
| Output looks identical regardless of prompt | LoRA is overfitting — retrain with more diverse subjects, or reduce strength to 0.5 |

For multi-image briefs (product + style + scene), the LoRA competes with other references. Often you'll want strength 0.7-0.8 in those cases to let the other references contribute.

## When the brand changes

LoRAs are versioned implicitly by training date. When the brand redesigns:

1. Train a new LoRA on the new reference set
2. Update `KREA_PREFERENCES.md` with the new style_id and trigger
3. Keep the old style_id documented in a "## Legacy" section for back-catalog work

Don't try to retrain the same `style_id` — train a new one. LoRAs are cheap to spin up.

## Comparison with higgsfield's Soul-ID

Higgsfield offers Soul-ID — a faster face-embedding-based training (5-20 images, ~5 min) for character / face consistency. Krea's LoRA approach is slower but more general:

- Krea LoRA: any visual signature (style, mood, palette, composition). 15-45 min train. Works across models that support style input.
- Higgsfield Soul-ID: face / character identity specifically. ~5 min train. Locked to higgsfield's Soul models.

For brand-style consistency (palette, composition, mood across products), Krea LoRA is the right tool. For face / character continuity in a campaign (same model across many ads), neither perfectly fits today — Krea LoRA can be trained on a person but it's overkill for face-only.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Training never completes | Bad training URLs (404) | The script HEAD-checks URLs; fix the bad ones or use `--skip-validation` if you know they're fine |
| Trained style ignores trigger word | LoRA underfit (too few or too inconsistent training images) | Retrain with more / better images, or with `--max-train-steps 1500` |
| Style overwhelms every generation | LoRA overfit | Use strength 0.5-0.7 at generation time, or retrain with `--max-train-steps 600` |
| `style_id` not accepted by chosen model | That model doesn't support style input | Check `get_model_schema` for a `styleId` or `styles` field; pick a model that has it |
| Style applies but product accuracy drops | Style is dominating the image-to-image reference | Decrease style strength, OR include the product reference at higher weight (model-specific) |
