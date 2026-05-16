# Cookbook

Five end-to-end recipes that combine Krea generation with agent reasoning. Each recipe shows what to say to the agent, the pattern of MCP calls it produces, and tips.

All recipes assume model IDs are resolved live via `list_models()` and matched against the archetypes in `model-catalog.md`. Concrete IDs are shown as `<archetype>` placeholders.

---

## Recipe 1 — Full ad campaign from a product URL

**What it does.** Give the agent a product URL. It fetches the page, extracts value props and audience signals, then generates 30+ creatives across TikTok (9:16), Instagram (1:1), YouTube (16:9), with several creative angles — lifestyle, feature, social proof, comparison.

**Why this is powerful.** Replaces the first sprint of a creative agency: one URL in, full campaign out.

**Prompt to the agent:**
```
Generate a full ad campaign for [URL]. Make TikTok (9:16), Instagram (1:1), and YouTube (16:9) formats. Cover lifestyle, feature highlight, social proof, and comparison angles. Draft cheap first, then upscale the best ones to 4K.
```

**Pattern.**

```
# 1. Fetch URL with WebFetch to extract product info
brief = WebFetch(url=..., prompt="extract product name, key features, target audience, visual style cues")

# 2. Pick a fast draft image model and a high-fidelity model once
models = list_models()
draft_id = <choose fast image draft archetype from model-catalog.md>
final_id = <choose high-fidelity image archetype>
upscaler_id = <choose faithful upscale archetype>

# 3. For each (angle, format), generate a draft
for angle in ["lifestyle", "feature", "social-proof", "comparison"]:
    for aspect in ["9:16", "1:1", "16:9"]:
        draft = generate_image(
            model=draft_id,
            input={
                prompt: f"{brief.product} — {angle} angle, {aspect} format, social media ad, clean background, professional photography",
                aspectRatio: aspect,
            },
            sync=true, timeoutSeconds=60,
        )
        # Download, Read with vision, score subjectively
        # Save URL with metadata for later

# 4. Show all drafts to user; let them pick which to upscale

# 5. Upscale picks to 4K
for winner in user_picks:
    enhance_image(
        model=upscaler_id,
        input={imageUrl: winner.url, width: 4096, height: 4096},
        sync=true, timeoutSeconds=120,
    )
```

**Tips.**
- Generate 9:16 drafts first (cheapest), only upscale the formats you'd actually run.
- For ads that overlay text/copy on the image, prefer a text-friendly image archetype (see `model-catalog.md`).
- Use the agent's vision to filter out drafts where the product didn't render correctly — don't waste upscale CU on broken drafts.

---

## Recipe 2 — Train a brand style → generate infinite on-brand content

**What it does.** Feed 10–20 brand images → train a custom LoRA → use the style ID to generate unlimited new content that matches your aesthetic. Solves visual consistency.

**Why this is powerful.** One training run, then every future generation references the style ID and stays on-brand.

**Prompt to the agent:**
```
Train a LoRA on these brand images: [URLs or local paths]. Call it "acme-brand". Then generate 5 sample images using the trained style: product on white background, lifestyle shot, hero banner, social square, email header.
```

**Pattern.**

LoRA training is **not** exposed through the MCP. Use the `scripts/train_style.py` companion script:

```bash
uv run scripts/train_style.py \
  --name "acme-brand" \
  --model flux_dev \
  --type Style \
  --trigger-word "acmestyle" \
  --urls-file brand-images.txt \
  --max-train-steps 1000 \
  --output-dir output/acme-brand
```

`brand-images.txt` — one URL per line:
```
https://your-cdn.com/brand-photo-01.jpg
https://your-cdn.com/brand-photo-02.jpg
...
```

Training takes 15–45 minutes. The script saves `training-manifest.json` with the resulting `style_id`.

Then use the style ID with MCP generation:

```
style_id = "style_abc123"  # from training-manifest.json

# Each generation can reference the style via the appropriate input field for the model.
# Check get_model_schema(model=...) for the exact field name (typically `styleId` or
# `styles: [{id, strength}]`).

for prompt in [
    "acmestyle product on clean white background, studio lighting",
    "acmestyle lifestyle photo, person using product outdoors, golden hour",
    "acmestyle hero banner for homepage, wide aspect",
    "acmestyle social square for Instagram, vibrant",
    "acmestyle email header, subtle texture, on-brand",
]:
    generate_image(
        model="<style-aware image model>",  # confirm via get_model_schema
        input={
            prompt: prompt,
            styleId: style_id,
            styleStrength: 1.0,
        },
        sync=true, timeoutSeconds=60,
    )
```

**Tips.**
- 15–20 training images works better than 10 for style consistency.
- `--type Object` is for training on a specific product; `--type Style` for a visual aesthetic.
- `style_strength=0.7` is a softer influence; `1.5` is very strong (often overdriven).
- Store the style ID in `KREA_PREFERENCES.md` so every future session reuses it.

---

## Recipe 3 — Product photo → lifestyle scenes → 4K videos

**What it does.** One product photo in → 10 lifestyle scene images → best ones animated to video → upscaled to 4K. Plain product photo → campaign-ready video content.

**Prompt to the agent:**
```
Take this product image [URL or local path] and generate 10 lifestyle scenes around it, animate the best 4 into 5-second videos, then upscale all videos to 4K. Save everything to output/campaign/.
```

**Pattern.**

```
# 1. Upload the product image if local
if local_path:
    product = upload_asset(filename, mimeType, fileData=base64(...))
    product_url = product.url
else:
    product_url = "<URL given by user>"

# 2. Generate 10 lifestyle scenes referencing the product
scenes = ["morning coffee setup on marble", "desk workspace with plants",
          "outdoor café table", "gym bag with accessories", "bookshelf home office",
          "kitchen counter at golden hour", "luxury hotel room", "beach picnic",
          "modern living room", "rooftop bar at dusk"]

scene_urls = []
for i, scene in enumerate(scenes, 1):
    result = generate_image(
        model="<image-to-image high-fidelity model>",  # accepts imageUrl input
        input={
            prompt: f"{scene}, product visible in scene, lifestyle photography, natural lighting",
            imageUrl: product_url,
            aspectRatio: "1:1",
        },
        sync=true, timeoutSeconds=60,
    )
    scene_urls.append(result.url)

# 3. Show all to user, get their top 4 picks

# 4. Animate the picks (parallel submission)
video_jobs = []
for url in user_top_4:
    job = generate_video(
        model="<image-to-video model>",
        input={
            prompt: "subtle product reveal, camera slowly pulls back, natural ambient motion",
            startImage: url,
            duration: 5,
            aspectRatio: "1:1",
        },
        sync=false,
    )
    video_jobs.append(job)

# 5. Poll each until terminal — see async-polling.md

# 6. Download all .mp4 results. Upscaling video to 4K isn't currently supported
#    via the standard enhance models, so this step typically applies to stills, not videos.
#    If the user wanted 4K stills of each scene, run enhance_image on scene_urls instead.
```

**Tips.**
- For repeatable batch runs (do this for every new product launch), wrap it as `scripts/pipeline.py` JSON with `fan_out + parallel`. See `pipelines.md`.
- Add audio to videos with `generateAudio: true` if the model schema supports it.
- Validate the first 2 scenes before kicking off all 10 — if the product doesn't carry over well, regenerate with stronger reference language in the prompt.

---

## Recipe 4 — Storyboard to produced ad

**What it does.** Write a 6-scene script → each scene becomes a frame → each frame becomes an animated clip → assemble with `ffmpeg`. A produced ad without a camera or crew.

**Prompt to the agent:**
```
Produce a 30-second ad for [product] with this script: [your script]. Each scene should be ~5 seconds. Generate images for each scene, animate them, add audio, give me the assembled clip.
```

**Pattern.** This is the canonical `video-production.md` workflow. The short version:

```
# 1. Plan shot list with user

# 2. Generate each frame (high-fidelity image archetype with face refs where needed).
#    Show each frame, wait for approval before moving on.

frames = []
for scene in shot_list:
    frame = generate_image(
        model="<multi-reference image model>",
        input={
            prompt: scene.frame_prompt,
            imageUrls: scene.face_refs,  # if any
            aspectRatio: "16:9",
        },
        sync=true, timeoutSeconds=60,
    )
    # Show to user; if approved, frames.append(frame)
    # if rejected, regenerate before continuing

# 3. Animate approved frames in parallel (submit all, then poll)
video_jobs = [
    generate_video(
        model="<image-to-video model with audio support>",
        input={
            prompt: scene.motion_prompt,
            startImage: frame.url,
            duration: 5,
            aspectRatio: "16:9",
            generateAudio: true,  # if supported by schema
        },
        sync=false,
    )
    for scene, frame in zip(shot_list, frames)
]

# 4. Poll each, download all clips

# 5. Normalize + concat + add audio with ffmpeg — see video-production.md
```

**Tips.**
- The single most common failure: animating frames the user hasn't approved. Don't skip the approval gate.
- Keep scene prompts consistent (same character description, same lighting cues, same color grading) for cross-scene cohesion.
- See `video-production.md` for the full ffmpeg post-production pipeline.

---

## Recipe 5 — Data-driven creative iteration

**What it does.** Generate 50 ad variants → measure performance externally → regenerate winners with targeted variations. Programmatic creative optimization.

**Prompt to the agent (phase 1):**
```
Generate 50 ad variants for [product] across these dimensions: 5 model archetypes × 2 angles × 5 formats. Save with a manifest tying file → (model_id, angle, format) for later analysis.
```

**Pattern.**

```
# 1. Pick model archetypes once
models = list_models()
chosen_archetypes = ["fast draft", "high-fidelity general", "high-fidelity character",
                     "stylized", "text-friendly"]
chosen_ids = [<resolve each archetype from model-catalog.md>]

# 2. Generate the matrix
manifest = {"product": "...", "run": "2026-05-13", "variants": []}
for archetype, model_id in zip(chosen_archetypes, chosen_ids):
    for angle in ["lifestyle", "feature"]:
        for aspect in ["9:16", "1:1", "16:9", "4:5", "21:9"]:
            result = generate_image(
                model=model_id,
                input={
                    prompt: f"product — {angle} angle, social media ad, clean background, professional photography",
                    aspectRatio: aspect,
                },
                sync=true, timeoutSeconds=60,
            )
            manifest["variants"].append({
                "url": result.url,
                "archetype": archetype,
                "model_id": model_id,
                "angle": angle,
                "aspect": aspect,
                "ctr": None,  # to be filled in later
            })

# 3. Save manifest.json. User runs the ads externally, fills in CTR.
```

**Prompt to the agent (phase 2, after data):**
```
Variants 3, 7, and 12 had 2.3× the CTR. Generate 20 new variants that keep their composition but vary lighting (5), color temperature (5), background (5), and model/talent (5).
```

**Pattern (phase 2).**

```
winners = [v for v in manifest["variants"] if v["id"] in user_winner_list]

new_variants = []
for w in winners:
    # 5 lighting variations
    for lighting in ["warm golden hour", "high contrast studio", "soft morning blue",
                     "neon accent backlight", "dramatic rim light"]:
        result = generate_image(
            model=w["model_id"],
            input={
                prompt: f"same composition as reference, {lighting}",
                imageUrl: w["url"],
            },
            sync=true, timeoutSeconds=60,
        )
        new_variants.append({...})

# Repeat for color temp, background, talent
```

**Tips.**
- Start with cheap models to explore the space; only invoke high-fidelity archetypes on promising directions.
- The most impactful variable is usually the **angle / hook** (the story), not the model.
- Save `seed` values when the model schema exposes them — lets you reproduce a winner exactly and vary one parameter at a time.

---

## Which recipe for what

| Goal | Recipe | Best matches in `model-catalog.md` |
|---|---|---|
| Launch a campaign fast | #1 Full Ad Campaign | fast draft → high-fidelity → faithful upscale |
| Keep all content on-brand | #2 LoRA Training | train via `scripts/train_style.py`, then any style-aware archetype |
| Turn a product photo into lifestyle scenes | #3 Product Pipeline | image-to-image high-fidelity → image-to-video |
| Produce a narrative video ad | #4 Storyboard | multi-reference high-fidelity → image-to-video with audio |
| Find what creative works | #5 Iteration | fast draft (volume) → high-fidelity (winners) |
