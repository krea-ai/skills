# Model Catalog — Intent → Archetype

Krea's model lineup changes faster than this skill ships. So this document does not list specific model IDs. Instead, it describes **archetypes** — the kinds of jobs Krea supports — and tells you what to scan for in the live `list_models()` output to find a current match.

## How to use this file

1. Call `krea models list --json` by default, or MCP `list_models()` when the CLI is unavailable. You get back an array of `{id, category, name, description}` per model.
2. Identify the intent (the user's brief or your interpretation of it).
3. Match the intent to an **archetype** below.
4. Scan the `name` and `description` fields of the `list_models` result for the **keyword hints** under that archetype.
5. Call `krea models show <id> --json` or `get_model_schema(model=<id>)` for the candidate to confirm it accepts the inputs you have.
6. Submit.

When in doubt, prefer the model whose `description` most closely echoes the user's brief.

**Current flagship note.** As of the 0.2.1 skill release, `krea/krea-2/large` is the CLI's default image model and `krea/krea-2/medium` is its faster sibling. Treat them as current flagship examples when they appear in live `list_models()` output, but still inspect the live schema before submitting.

---

## Image archetypes

### Fast image draft (cheap, iterative)

**Intent.** The user is iterating quickly. They will refine the prompt several times. They have not asked for "high quality" or "final".

**Keywords in `list_models`.** Scan `name` for `flux`, `dev`, `z-image`, `fast`, `mini`. Scan `description` for "fast", "draft", "cheap", "iterate", "quick".

**Schema hints (via `get_model_schema`).** Most accept `prompt`, `width`/`height`, `seed`. Some accept `steps` and `guidance` for finer control.

**Don't use this archetype when** the user explicitly says "final", "production", "for delivery", or the brief is detailed and specific (>50 words, clear vision).

---

### High-fidelity image (photoreal, hero shots)

**Intent.** Polished result. Production. The user has already iterated and wants the best output Krea offers, or the brief is unambiguously high-stakes.

**Keywords.** Scan `name` for `krea-2`, `nano-banana-pro`, `gpt-image`, `imagen`, `seedream`, `pro`, `ultra`, `flagship`. Scan `description` for "photoreal", "high-fidelity", "premium", "production-quality".

**Schema hints.** Often supports `resolution` (e.g. `1K`/`2K`/`4K`), `quality` (`high`/`auto`), and `aspect_ratio` or MCP `aspectRatio`.

**Krea 2 public shape.** `krea/krea-2/*` image endpoints use `aspect_ratio` + `resolution` (for example `1:1` + `1K`) instead of `width`/`height`. Do not pass `quality` or `steps` to Krea 2 unless the live schema explicitly adds them.

**Don't use this archetype when** the user is just exploring or hasn't committed to a direction.

---

### Text in image / typography

**Intent.** The image needs readable text — a poster, a brand banner, packaging mockup, UI screenshot, signage.

**Keywords.** Scan `name` for `ideogram`, `gpt-image`. Scan `description` for "text", "typography", "letters", "signage".

**Schema hints.** Worth checking whether the model accepts a `text` parameter explicitly or expects text inside the prompt.

**Don't use this archetype** for general images that happen to have a tiny bit of text — the cost premium isn't worth it. Most flagship general models render some text passably.

---

### Stylized / illustrated / character

**Intent.** Anime, cartoon, painted look, character design, expressive illustration. Not photoreal.

**Keywords.** Scan `name` for `nano-banana`, `flux-kontext`, `grok-imagine`. Scan `description` for "stylized", "character", "anime", "illustration", "expressive".

**Schema hints.** Some support LoRA styles (`styleId`) — useful when the user has a trained Krea style they want to apply.

---

### Image-to-image / face reference

**Intent.** The user provided an existing image and wants it transformed (style swap, edit), or wants their face/subject referenced.

**Keywords.** Scan `description` for "image prompt", "reference", "face", "edit".

**Schema hints.** Check whether the schema uses `image_url`/MCP `imageUrl` (singular) or `image_urls`/MCP `imageUrls` (array). Multi-reference models use the array form for face injection from several photos.

**Pattern.**
- One reference, simple edit → most image models work
- Multiple face references → look for models accepting `image_urls` or MCP `imageUrls` as an array
- Faithful subject preservation across edits → look for models with "character ref" or similar in description

---

### Vector illustrations

**Intent.** Logos, icons, flat illustrations with clean geometric shapes — output meant to be vectorized or already vector-like.

**Keywords.** Scan `name`/`description` for `vector`, `seedream`, `flat`.

---

## Video archetypes

### Fast video draft

**Intent.** Quick motion test. The user is exploring how a still might animate.

**Keywords.** Scan `name` for `hailuo`, `fast`, `lite`, `mini`. Scan `description` for "fast", "draft", "budget".

**Schema hints.** Most support `prompt`, `duration` (4-8s typical), and `aspect_ratio` or MCP `aspectRatio`.

---

### Cinematic video (high-fidelity)

**Intent.** Production-grade clip, multi-shot, consistent identity, motion-heavy. The user is making something polished.

**Keywords.** Scan `name` for `veo`, `seedance`, `kling-pro`. Scan `description` for "cinematic", "high-fidelity", "multi-shot", "consistent".

**Schema hints.** Check for `resolution` (`720p`/`1080p`), `mode` (`std`/`pro`), and `generate_audio` or MCP `generateAudio`.

**Don't use this archetype** for quick tests — these models are slow and expensive.

---

### Image-to-video / start frame anchored

**Intent.** Animate a still. The first frame is given.

**Keywords.** Scan `description` for "start frame", "image to video", "anchor", "first frame".

**Schema hints.** The schema will name the start-frame param - current CLI schemas commonly use `start_image`; MCP may expose `startImage`. Some models also accept `end_image` / MCP `endImage` for a transition. Check the live schema for the exact field name and whether multiple references are allowed.

**Workflow.** First call `krea upload` or MCP `upload_asset` to register the local/non-Krea frame, then pass the returned Krea-hosted URL into the video model's start-frame field.

---

### Video with audio

**Intent.** Final clip needs synced audio (ambient, music, or speech).

**Keywords.** Scan `description` for "audio", "sound", "with audio", "lip sync".

**Schema hints.** Some models expose `generate_audio` or MCP `generateAudio` as a boolean. Others accept a reference audio file via an `audio` media input.

---

## Image enhancement archetypes

### Faithful upscale

**Intent.** Make the existing image larger without changing what's in it.

**Keywords.** Scan `name` for `topaz-standard`, `topaz`. Scan `description` for "faithful", "upscale", "preserve".

**Schema hints.** `width` and `height` are required. Some accept `sharpen`/`denoise` fine-tuning.

---

### Creative enhance

**Intent.** Upscale and let the model add detail / refinement (more aggressive than faithful).

**Keywords.** Scan `name` for `topaz-generative`, `creative`. Scan `description` for "creative", "generative", "add detail".

**Schema hints.** Often accepts `creativity` (1–6 typical), `face_enhancement`.

---

### Bloom / creative detail injection

**Intent.** Heavy creative pass — invent texture, depth, embellishment.

**Keywords.** Scan `name` for `bloom`. Scan `description` for "bloom", "embellish", "invent detail".

---

## Picking flow — intent first, model second

When the user says something, classify into one of these intent buckets first:

1. **"Make me a quick image of X"** → fast image draft
2. **"Final image for production"** → high-fidelity image
3. **"Poster / banner / packaging with text"** → text-in-image
4. **"Illustration / anime / cartoon of X"** → stylized
5. **"Edit this photo into Y"** → image-to-image
6. **"Make a video of X"** → fast video draft (default) OR cinematic if the brief is detailed
7. **"Animate this still"** → image-to-video
8. **"Add sound"** → video-with-audio
9. **"Upscale this"** → faithful upscale (default)
10. **"Enhance this"** (ambiguous) → ask one quick question: faithful or creative?

Then resolve the archetype → candidate model via `list_models` keywords. Then `get_model_schema` to check inputs. Then submit.

## Things to keep in mind

- **Never hardcode a model ID** based on what you remember. Always pull from `list_models`. Names change, models retire.
- **`get_model_schema` is the source of truth for inputs.** Don't guess parameter names; ask.
- **If the user names a specific model** (e.g. "use nano-banana-pro"), use it — skip the archetype routing.
- **`KREA_PREFERENCES.md` overrides the defaults.** If a project pins specific models for specific intents, honor that.
- **When two archetypes could apply**, prefer the one matching the user's stated word ("fast" → fast draft; "cinematic" → cinematic video).
- **Model name keywords are hints, not guarantees.** Always confirm the choice by reading the model's `description` from `list_models`.
