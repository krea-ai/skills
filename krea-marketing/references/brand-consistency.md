# Brand Consistency via LoRA

When a brand needs visual consistency across many generations — same palette, same compositional language, same vibe — train a brand LoRA once and apply the resulting `style_id` to every subsequent generation. The difference between "looks AI-generated" and "looks on-brand."

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

### Step 2: Train via the Krea API

LoRA training is exposed as a direct API call (no CLI subcommand yet, no shipping Python script). The full API surface is documented in `../../krea-ai/references/lora-training.md` with curl, Python, and TypeScript examples.

**One-off**: agent runs curl inline.

```bash
KEY="$KREA_API_KEY"
JOB=$(curl -sf -X POST https://api.krea.ai/styles/train \
  -H "Authorization: Key $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux_dev",
    "type": "Style",
    "name": "acmebrand-2026q2",
    "urls": ["https://cdn/brand-01.jpg", "https://cdn/brand-02.jpg", "..."],
    "trigger_word": "acmebrand",
    "max_train_steps": 1000
  }' | jq -r .job_id)

# Poll every 60s until terminal
while :; do
  STATUS=$(curl -sf "https://api.krea.ai/jobs/$JOB" -H "Authorization: Key $KEY" | jq -r .status)
  case "$STATUS" in completed) break ;; failed|cancelled) exit 1 ;; esac
  sleep 60
done

# Extract style_id
STYLE_ID=$(curl -sf "https://api.krea.ai/jobs/$JOB" -H "Authorization: Key $KEY" | jq -r '.result.id')
echo "Style ID: $STYLE_ID"
```

**Repeatable**: the agent generates a training script in the user's stack via `krea-build`. If the project is Python → `train.py`. If TypeScript → `train.ts`. If bash-only → `train.sh`. The user owns the script; the skill doesn't ship one.

Training takes 15-45 minutes.

### Step 3: Pin the style ID

Add to the project's `KREA_PREFERENCES.md` (or the user-level `~/.claude/CLAUDE.md` `## Krea preferences` section):

```markdown
## Krea preferences

- Brand style ID: style_abc123 (trigger: acmebrand, trained 2026-05-17)
- Default style strength: 0.85
```

Future agent invocations read this and apply the style automatically.

### Step 4: Apply in generations

Include the style in every product / marketing generation. Different models accept the style field with different names — check the schema first via `mcp__krea-public-api__get_model_schema(model=<id>)` (or `krea models show <id>`).

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

Or via CLI:

```bash
krea generate image -m <id> \
  -p "acmebrand premium product hero shot of [PRODUCT]" \
  -i styleId=style_abc123 \
  -i styleStrength=0.85 \
  --aspect 1:1 --wait
```

The trigger word (`acmebrand`) in the prompt activates the style.

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

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Training never completes | Bad training URLs (404) | HEAD-check each URL (`curl -sfI <url>`) before submitting |
| Trained style ignores trigger word | LoRA underfit (too few or too inconsistent training images) | Retrain with more / better images, or `max_train_steps: 1500` |
| Style overwhelms every generation | LoRA overfit | Use strength 0.5-0.7 at generation time, or retrain with `max_train_steps: 600` |
| `style_id` not accepted by chosen model | That model doesn't support style input | Check `get_model_schema` for a `styleId` or `styles` field; pick a model that has it |
| Style applies but product accuracy drops | Style is dominating the image-to-image reference | Decrease style strength, OR include the product reference at higher weight (model-specific) |

For full API field reference and additional language examples (Python, TypeScript), see `../../krea-ai/references/lora-training.md`.
