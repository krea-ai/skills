# LoRA Style Training

Train a custom style, object, or character from 15–20 reference images, then use the resulting `style_id` in generations to keep output on-brand or character-consistent.

The Krea CLI doesn't currently expose training as a subcommand, and the MCP doesn't either. Training is done by hitting the Krea HTTP API directly. The skill ships **no Python scripts** — the agent writes the training flow in the user's stack via `krea-build` if they want a reusable script, or runs it inline via curl for a one-off.

## API surface

| Operation | Method | Endpoint |
|---|---|---|
| Submit training job | `POST` | `/styles/train` |
| Poll job status | `GET` | `/jobs/{job_id}` |
| Use trained style | (per-model) | include `styleId` in `generate_image` input, per the model's schema |

Authentication: `Authorization: Key ${KREA_API_KEY}` header. Get a key at [krea.ai/settings/api-keys](https://www.krea.ai/settings/api-keys).

## Training request shape

```json
POST /styles/train
{
  "model": "flux_dev",
  "type": "Style",
  "name": "acmebrand-2026q2",
  "urls": [
    "https://your-cdn.com/brand-photo-01.jpg",
    "https://your-cdn.com/brand-photo-02.jpg",
    "..."
  ],
  "trigger_word": "acmebrand",
  "learning_rate": 0.0001,
  "max_train_steps": 1000,
  "batch_size": 1
}
```

### Fields

| Field | Required | Notes |
|---|---|---|
| `model` | yes | Base: `flux_dev`, `flux_schnell`, `wan`, `qwen`, `z-image` |
| `type` | yes | `Style` (aesthetic), `Object` (specific product), `Character` (face/person), or `Default` |
| `name` | yes | Human-readable identifier |
| `urls` | yes | 3–2000 hosted image URLs. Validate they're reachable before submitting. |
| `trigger_word` | no | Token to activate the style in prompts. Pick something unique like `acmestyle`. |
| `learning_rate` | no | Default 0.0001 |
| `max_train_steps` | no | Default 1000. Bump to 1500 for harder briefs. |
| `batch_size` | no | Default 1 |

### Response

```json
{ "job_id": "<uuid>", "status": "queued", ... }
```

Poll `GET /jobs/{job_id}` every 30–60s. Terminal status is `completed` or `failed`. On `completed`, the response includes `result.id` (or `result.style_id`) — that's your `style_id`.

Typical training time: 15–45 minutes.

## Worked examples (language-neutral, agent picks the user's stack)

### curl (one-off)

```bash
KEY="$KREA_API_KEY"

JOB=$(curl -sf -X POST https://api.krea.ai/styles/train \
  -H "Authorization: Key $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux_dev",
    "type": "Style",
    "name": "acmebrand-2026q2",
    "urls": ["https://cdn/brand-01.jpg", "https://cdn/brand-02.jpg"],
    "trigger_word": "acmebrand",
    "max_train_steps": 1000
  }' | jq -r .job_id)

# Poll
while :; do
  STATUS=$(curl -sf "https://api.krea.ai/jobs/$JOB" -H "Authorization: Key $KEY" | jq -r .status)
  echo "Status: $STATUS"
  case "$STATUS" in
    completed) break ;;
    failed|cancelled) echo "Training failed"; exit 1 ;;
  esac
  sleep 60
done

curl -sf "https://api.krea.ai/jobs/$JOB" -H "Authorization: Key $KEY" | jq -r '.result.id'
```

### Python (if the user's project is Python)

```python
import os, time, requests

KEY = os.environ["KREA_API_KEY"]
H = {"Authorization": f"Key {KEY}"}

r = requests.post("https://api.krea.ai/styles/train", headers=H, json={
    "model": "flux_dev",
    "type": "Style",
    "name": "acmebrand-2026q2",
    "urls": ["https://cdn/brand-01.jpg", "https://cdn/brand-02.jpg"],
    "trigger_word": "acmebrand",
    "max_train_steps": 1000,
})
r.raise_for_status()
job_id = r.json()["job_id"]

while True:
    s = requests.get(f"https://api.krea.ai/jobs/{job_id}", headers=H).json()
    if s["status"] == "completed":
        print(s["result"]["id"])
        break
    if s["status"] in ("failed", "cancelled"):
        raise RuntimeError(s.get("error") or s["status"])
    time.sleep(60)
```

### TypeScript (if the user's project is Node)

```typescript
const KEY = process.env.KREA_API_KEY!;
const H = { Authorization: `Key ${KEY}`, "Content-Type": "application/json" };

const start = await fetch("https://api.krea.ai/styles/train", {
  method: "POST",
  headers: H,
  body: JSON.stringify({
    model: "flux_dev",
    type: "Style",
    name: "acmebrand-2026q2",
    urls: ["https://cdn/brand-01.jpg", "https://cdn/brand-02.jpg"],
    trigger_word: "acmebrand",
    max_train_steps: 1000,
  }),
}).then(r => r.json());

let job;
while (true) {
  job = await fetch(`https://api.krea.ai/jobs/${start.job_id}`, { headers: H }).then(r => r.json());
  if (job.status === "completed") break;
  if (["failed", "cancelled"].includes(job.status)) throw new Error(job.status);
  await new Promise(r => setTimeout(r, 60_000));
}
console.log(job.result.id);
```

For a production-grade client (retries, validation, error handling), see `../../krea-build/references/api-client.md`.

## Type selection

- **`Style`** — visual aesthetic across varied subjects. 15–20 images.
- **`Object`** — specific product or item across angles and contexts. 10–20 photos.
- **`Character`** — specific person or character. 15–30 references with varied expressions / lighting / outfits.
- **`Default`** — model picks based on training data. Use only when none of the above clearly fits.

## Training-set guidance

- **Count**: 15–20 is the sweet spot. <10 underfits. >30 rarely improves.
- **Variety**: vary subjects for `Style` (keep aesthetic consistent), vary angles for `Object`, vary expressions for `Character`.
- **Quality**: ≥1024px on the long side. Blurry inputs propagate as visual noise.
- **Pre-flight**: HEAD-check every URL is reachable (`curl -sfI <url>`) before submitting. The API will fail mid-training on a bad URL.

## Using the trained style

The `style_id` is passed into compatible image-generation calls. Different models accept it under different field names — check `mcp__krea-public-api__get_model_schema(model=<id>)` (or `krea models show <id>`) for the exact shape. Common shapes:

- `styleId: "<id>"` and `styleStrength: 1.0`
- `styles: [{ id: "<id>", strength: 1.0 }]`

Include the trigger word in the prompt to activate the style.

### Strength tuning

- `0.5` — subtle hint
- `0.85` — balanced (good default)
- `1.0` — strong
- `≥1.5` — usually overdriven

If outputs ignore the trigger word, the LoRA underfit — retrain with more or better images, or with `max_train_steps: 1500`. If outputs look uniform regardless of prompt, it overfit — drop strength to 0.5–0.7 at generation time, or retrain with fewer steps.

## Pinning style IDs in the project

For repeat use, pin the resulting `style_id` in the project's `KREA_PREFERENCES.md` (or `## Krea preferences` section in `CLAUDE.md`) so future sessions automatically apply it:

```markdown
## Krea preferences

- Brand style ID: style_abc123 (trigger: acmebrand, trained 2026-05-17)
- Default style strength: 0.85
```

See `preferences.md` for the override mechanism.

## When to write training into a script

- **One-off**: curl inline or run a snippet in `python -c` / `node -e`. No script needed.
- **Repeatable** (re-train per quarter, per brand drop, etc.): the agent writes a training script in the user's stack via `krea-build`. Don't ship a Python script the user has to keep alive.

If/when the Krea CLI adds a `krea styles train` subcommand, this whole reference becomes simpler — but as of v1.0.0, the API surface above is the source of truth.
