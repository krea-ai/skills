---
version: 2.1.0
name: krea-marketing
description: "Commercial creative workflows with Krea — product photography (hero, lifestyle, white-background, social-square), video ads (UGC, talking head, product showcase, before/after, demo), brand-consistent batch generation via LoRA training, and click-to-ad pipelines (URL → product info → hero image → social variants). Use when the user asks for a product photo, ad, commercial creative, social media content, marketing campaign, brand assets, UGC video, or anything DTC-flavored. NOT for architectural visualization (use krea-archviz) or generic image generation (use krea-ai)."
license: MIT
---

# Krea Marketing — Commercial Creative

A vertical skill for product photography, video ads, and brand creative. Built on top of `krea-ai`'s MCP-first generation, with marketing-specific workflows, model routing, and format playbook.

## Bootstrap

Requires the Krea MCP server (`mcp__krea-public-api__*` tools). Inherits all bootstrap and UX rules from `../krea-ai/SKILL.md`. For click-to-ad workflows, also requires `WebFetch` to be available.

## When to use this skill

- "Hero product shot of my new perfume bottle"
- "Make me a TikTok ad for this product"
- "Generate a UGC-style video — someone unboxing this"
- "Lifestyle shots — this product in a kitchen, in a bathroom, on a desk"
- "Build me a 4-image carousel for Instagram"
- "Train a brand LoRA on these 15 images, then make 10 on-brand product shots"
- "Take this product URL and give me a hero image plus 3 social variants"

## When NOT to use this skill

- Architectural / interior / facade rendering → `krea-archviz`
- Developer integration patterns → `krea-build`
- Generic image gen with no commercial brief → stay in `krea-ai`

## The four core workflows

### 1. Product photography

Static product imagery across the most common DTC use cases: hero shots, lifestyle / context, white-background ecommerce, social-square posts.

```
1. Get the product reference (uploaded image or URL)
2. Read it with vision to understand the product's actual shape, color, surface
3. Pick the workflow: hero / lifestyle / white-bg / social
4. Route to a high-fidelity image archetype (see ../krea-ai/references/model-catalog.md)
5. Submit with image-to-image — the product reference anchors what the brand looks like
6. Vision-verify the result still reads as the same product
```

See `references/product-photography.md` for the full workflow + prompt templates for each sub-type.

### 2. Video ads

Five ad-type recipes covering most DTC commercial creative:

- **UGC-style** — selfie POV, casual presenter, social-native feel
- **Product showcase** — product centered, rotation, lighting changes, polished
- **Talking head** — presenter explaining the product, more produced
- **Before/after** — transformation reveals, split-frame or transition
- **Demo** — product in use, action, function-forward

Each has model archetype, prompt template, duration, aspect, audio flag in `references/video-ads.md`. All video generations follow `../krea-ai/references/async-polling.md` — `sync=false` then poll `get_job`.

### 3. Brand-consistent batch generation

For repeat campaigns where the brand look should hold across many generations.

```
1. Train a brand LoRA via ../krea-ai/scripts/train_style.py with 15-20 brand images
2. Pin the resulting style_id in KREA_PREFERENCES.md (see `../krea-ai/references/preferences.md`)
3. For each subsequent generation, include the style_id with strength ~0.8-1.0
4. Iterate strength based on how dominant the brand style should be
```

See `references/brand-consistency.md` for the training workflow + style-strength tuning.

### 4. Click-to-ad (URL → product → social variants)

User pastes a product URL; agent fetches the page, extracts product info, generates a hero shot + social variants in one orchestrated flow.

```
1. WebFetch the URL with extraction prompt: "extract product name, key visual features,
   target audience cues, color palette, hero product image URL"
2. Read the hero product image with vision (download via Bash + Read, or use the URL directly
   as imageUrl in the next step if it's HTTPS-accessible)
3. Confirm the extracted brief with the user in one line — "Generating a hero shot of
   [product] for [TikTok 9:16 / IG 1:1 / hero 16:9]. Confirm?"
4. Generate the hero shot (image-to-image with the product reference)
5. Generate the social variants (4-5 derivative shots in different formats / contexts)
6. Deliver: 1 hero + N variants with platform labels
```

See `references/product-photography.md` (Click-to-Ad section) for the orchestration details.

## Workflow shape (common to all 4)

```
1. Receive brief (text + optional uploaded image, or URL for click-to-ad)
2. Read any user images with vision
3. Identify which of the 4 workflows above fits
4. Resolve model archetype via ../krea-ai/references/model-catalog.md
5. get_model_schema(model=<id>) — confirm input field names
6. upload_asset(...) for any local references; or pass URL directly if HTTPS
7. Generate (sync=true for image, sync=false + poll for video)
8. Read output with vision, verify it matches the brief
9. Deliver URL + suggest one upgrade path (variation, format, etc.)
```

## UX rules (extends krea-ai)

Inherits all from `../krea-ai/SKILL.md`. Marketing-specific additions:

- **Aspect ratio routing.** When the user names a platform, route by it:
  - TikTok / IG Reels / IG Story / YT Shorts → 9:16
  - IG square / IG carousel → 1:1
  - IG portrait → 4:5
  - YouTube / web hero / LinkedIn / X → 16:9
  - Pinterest → 2:3
  - Default to 1:1 when no platform is named (most flexible).
- **For ad video, default duration is short.** 4-5s for testing, 8-15s for production. Always ask before generating > 10s clips — they're expensive.
- **Always offer 3 variations on hero shots** — same product, different lighting / composition / background. Conversion-rate testing requires options.
- **Confirm cost before any of these operations:** ≥ 5 images in one brief, any video generation, any 4K resolution image, or any batch larger than 1 variant of a hero shot. Surface estimated CU and the model archetype in one line, then proceed on confirmation.
- **Product accuracy matters more than aesthetic perfection.** If the agent renders a slightly-different bottle shape, the brand notices. Vision-verify shape, color, label every time before delivering.

## Reference docs

Load on demand:

- `references/product-photography.md` — hero / lifestyle / white-bg / social workflows + click-to-ad orchestration
- `references/video-ads.md` — 5 ad-type recipes with full prompt templates
- `references/brand-consistency.md` — LoRA training + style application workflow
- `references/ad-formats.md` — format taxonomy + aspect ratios per platform
- `references/marketing-prompts.md` — prompt patterns + power keywords + things to avoid

## Model selection (defer to krea-ai)

This skill does NOT maintain its own model catalog. Always resolve via:

```
list_models()
get_model_schema(model=<id>)
```

Use `../krea-ai/references/model-catalog.md` for archetypes. Most relevant to marketing:

- **High-fidelity image (photoreal, hero shots)** — hero product shots, lifestyle
- **Text-in-image / typography** — ads with overlay text, banners with copy
- **Image-to-image / face reference** — product placement, lifestyle with the actual product
- **Cinematic video (high-fidelity)** — polished video ads (Veo, Seedance, Kling families)
- **Fast video draft** — test-and-iterate ad video
- **Image enhancement** — upscaling final hero shots to 4K for print / large-format display

## Project preferences

Honor `KREA_PREFERENCES.md` per `../krea-ai/references/preferences.md`. Useful overrides for marketing teams:

```markdown
## Krea preferences

- Brand style ID: style_xyz123 (apply with strength 0.85 to all product shots)
- Trigger word: acmebrand
- Default platform: TikTok 9:16 unless otherwise specified
- For hero shots, prefer nano-banana-pro at 2K
- For draft / volume exploration, use flux-1-dev
- Skip cost confirmation under 100 CU
- Always generate 3 variants on hero shots
```

A "champion" on the marketing team owns this file; the rest of the team's agent invocations honor it automatically.

## Things this skill doesn't do

Be honest about the gaps so the user knows when the skill is the wrong tool:

- **Pre-built avatar / talent library.** No curated face library server-side. For UGC or talking-head video with a specific presenter, the user uploads photos as references — or trains a character LoRA via `../krea-ai/scripts/train_style.py` if the schema supports `Character` type. Identity drift is real; vision-verify after every generation.
- **URL-based brand-kit extraction.** No automatic logo / palette / font scraping from a brand website beyond what `WebFetch` returns as text. The user provides those explicitly.
- **Pre-composed ad-format layouts.** No template gallery for "headline format", "carousel slide 1", etc. The user describes the layout intent in the prompt and we render it.
- **In-platform performance data.** No CTR / engagement integration. The user runs ads externally and feeds winners back as references for the next batch.

These gaps are real. Don't pretend the skill does something it can't.
