# Prompt Engineering

Krea models reward concrete, sensory prompts. Keep them under ~200 tokens — very long prompts hurt more than help.

## Structure that works

`Subject + setting + style + camera + lighting`

Examples:

- "A red fox curled in a snowy pine forest, golden hour, 35mm, soft rim light"
- "Cyberpunk cat DJ on a neon rooftop, low angle, tilt-shift, dramatic backlight, cinematic"
- "Watercolor painting of a Japanese garden, cherry blossoms, soft pastels, morning haze"

Concrete > abstract. "A cat looking sad" is weaker than "An orange tabby sitting in a rainy window, head down, dim light".

## Camera and lighting vocabulary

Adding camera and lighting language helps most models lock onto a coherent visual:

- **Camera:** lens (35mm, 50mm, 85mm), angle (low, overhead, tilt-shift), motion (dolly in, tracking shot)
- **Lighting:** rim light, neon glow, golden hour, moody backlight, soft daylight, dramatic contrast
- **Medium:** oil painting, watercolor, photograph, 3D render, anime, vector illustration

## Image-to-image prompts

When you're passing an `imageUrl`, the prompt should describe **what changes**, not redescribe the source.

- ❌ "a man with brown hair in a leather jacket holding coffee, made into anime"
- ✅ "transform into anime style, vibrant cel shading"

The image already encodes the subject. The prompt is the transformation.

## Image-to-video prompts

When you're passing a `startImage`, the prompt describes **motion**, not the static frame.

- ❌ "a dancer in a red dress on stage" (the frame already has this)
- ✅ "the dancer spins slowly, fabric flowing, camera pushes in"

Motion vocabulary:

- **Camera moves:** dolly in, dolly out, pan left, pan right, tilt up, sweeping pan, slow push, whip pan, tracking shot
- **Subject motion:** "the X turns slowly", "smoke rises", "leaves fall", "water splashes"
- **Energy:** slow, gentle, gradual, sudden, frantic

## Negative prompting (when not supported)

Most Krea models don't expose `negative_prompt`. Phrase what you want **positively** instead:

- Instead of "no blur" → "tack sharp"
- Instead of "no people" → "uninhabited landscape"
- Instead of "no text" → describe the scene without referring to text

## Aspect ratio hints

- `16:9` — landscape, cinematic, hero shots
- `9:16` — vertical, social, mobile
- `1:1` — square, profile pics, icons
- `4:3`, `3:4`, `21:9` — model-dependent; check `get_model_schema(model=<id>)` for the exact accepted enum

If the model accepts `aspectRatio`, prefer it. If it doesn't, set `width` and `height` directly.

## Style consistency across multiple images

When generating a series (storyboard, character sheet, brand pack):

- Reuse the same `seed` across images for similar prompt structure.
- Reuse the same model — switching mid-series changes the look.
- Use a Krea LoRA `styleId` if you've trained one for the project (see `../workflows/lora-train-and-use.md`).
- Use multi-image reference (`imageUrls`) on supporting models to lock the subject across compositions.

## Safety

Models will reject prompts with `nsfw` or `ip_detected` terminal status. Avoid:

- Real public figures (politicians, celebrities) — use generic descriptors
- Sexual content
- Trademarked characters
- Violence against identifiable individuals

If a job fails with content moderation, surface it to the user without judgment and suggest a rephrasing.
