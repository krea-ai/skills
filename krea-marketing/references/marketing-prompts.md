# Marketing Prompt Patterns

The difference between AI-slop and commercial-grade output usually comes down to the prompt. Marketing creative has its own vocabulary and patterns that generic prompting doesn't capture.

## The marketing prompt formula

```
[Subject doing specific thing] +
[Setting / environment with specifics] +
[Lighting language] +
[Camera language] +
[Material / texture / surface details] +
[Mood / atmospheric quality] +
[Reference to commercial photography style or genre]
```

Five slots minimum. Skip none. Each adds specificity that anchors the model away from generic "professional photograph" output.

## Power keywords that work

Words that consistently improve output quality in commercial creative:

- **Camera language**: "shot on 35mm", "85mm portrait", "macro detail", "shallow depth of field", "tight framing", "wide aspect", "slight elevated angle", "eye-level", "low angle"
- **Lighting quality**: "soft directional", "studio softbox", "warm three-point", "rim light catching the edge", "golden hour", "diffuse overcast", "single key light", "ambient bounce"
- **Photography genre**: "editorial photography", "advertising photography", "lookbook photography", "lifestyle photography", "documentary style", "fashion photography", "premium product photography", "candid", "magazine-quality"
- **Atmospheric quality**: "soft atmospheric haze", "subtle bloom on highlights", "warm color cast", "cool clinical tone", "natural skin tones", "true-to-life colors", "saturated punchy palette"
- **Material specifics**: see `../../krea-archviz/references/materials.md` for the full vocabulary; marketing reuses it
- **Production quality**: "premium production quality", "advertising-grade", "magazine spread quality", "minimalist editorial polish"

## Words and phrases to avoid

Generic AI vocabulary that produces generic AI output:

- "professional" (anchors to nothing specific)
- "modern" (means too many things)
- "high quality" (vague — replace with specific quality cues)
- "beautiful" (zero information)
- "vibrant" (overused, produces saturated slop)
- "amazing" (zero information)
- "stunning" (zero information)
- "trendy" (anchors to nothing)
- "aesthetic" (every model overuses this)

Use specific cues instead:

| Generic | Specific |
|---|---|
| "professional product photo" | "premium advertising photography, shot on 85mm" |
| "modern minimalist look" | "Bauhaus-inspired composition, sans-serif type hierarchy, restrained palette of cream and charcoal" |
| "high quality" | "magazine-quality reproduction, true-to-life color, sharp detail across the product" |
| "beautiful lighting" | "soft directional key light from upper-left with warm fill" |
| "trendy social media style" | "TikTok-native vertical composition, dynamic energy, social-platform-native feel" |

## Specific patterns by use case

### Product hero shot

> Photoreal hero shot of [PRODUCT, specific descriptors], [BACKGROUND] in [PALETTE], [LIGHTING — specific direction and quality], [SURFACE INTERACTION — reflection, contact shadow, droplets, etc.], shot on [LENS], [DEPTH OF FIELD], premium [GENRE — fragrance / beverage / fashion / electronics] photography

### Lifestyle in-context

> Lifestyle photograph of [PRODUCT] in [CONTEXT with specifics], [TIME OF DAY] light from [DIRECTION], [SCENE PROPS — 2-3 specific items], suggesting [TARGET AUDIENCE — specific lifestyle], natural product placement, [GENRE] photography, [LENS], candid feel

### Social-square graphic

> [STYLE — clean minimal / bold graphic / lifestyle] product image of [PRODUCT], 1:1 square composition, [PALETTE — explicit named colors or hex], room for overlay text in the [POSITION], [PLATFORM-NATIVE FEEL], optimized for [Instagram feed / TikTok / etc.]

### Video — UGC style

> Casual UGC-style video, [PERSON] in [SETTING], [SPECIFIC ACTION], natural selfie framing on phone camera, soft natural light, slight handheld camera shake, candid not polished, social-native feel, [DURATION] seconds

### Video — product showcase

> Polished product showcase video of [PRODUCT] centered on [BACKGROUND], [SPECIFIC MOTION — rotation / pull-back / lighting shift], premium product photography in motion, soft studio lighting, sharp focus throughout, [DURATION] seconds

## Color anchoring

When brand colors matter, name them explicitly. Models honor named colors better than implicit ones.

- "Brand peach-pink (warm coral with a hint of orange)"
- "Brand cream (off-white with a warm tan undertone, not pure white)"
- "Brand charcoal (deep warm grey with subtle brown undertone, not black)"

For tight color matching, include hex if the model supports it (some do, some ignore it): "brand pink #F5C2C2".

If the brand has a trained LoRA, the LoRA does most of the color work — just include the trigger word and the brand palette comes through.

## Compositional anchoring

Models have weak spatial control. Give them strong cues:

- "Product centered in frame" / "product in the lower-right third" / "product offset to the left"
- "Eye-level" / "slight downward angle" / "low angle looking up" / "directly overhead"
- "Tight crop on the product" / "medium framing showing the product and one supporting element" / "wide environmental shot with the product as focal point"

## Anti-AI vocabulary

If you find your prompts using these, replace them:

- "highly detailed" (vague — what detail?)
- "ultra realistic" (replace with specific genre: "advertising photography" / "editorial photography")
- "best quality, masterpiece" (Stable Diffusion era prompt vocabulary, doesn't help modern models)
- "8k, 32k" (resolution is a parameter, not a prompt word)
- "trending on artstation" (dated Stable Diffusion prompt vocabulary)
- "in the style of [famous photographer]" (works inconsistently and raises IP / likeness concerns when the photographer is living)

## Genre vocabulary by product category

| Category | Genre / style language |
|---|---|
| Beverage | "premium beverage photography", "moody bar lighting", "condensation droplets", "ice and motion" |
| Skincare / cosmetics | "clean clinical photography", "spa-aesthetic", "soft natural light", "fresh wet textures" |
| Food | "editorial food photography", "natural daylight from window", "linen napkin", "shallow depth of field" |
| Fashion / apparel | "lookbook photography", "editorial fashion", "natural light", "candid posing", "minimalist studio" |
| Electronics | "advertising photography", "studio rig lighting", "specular highlights on glass and metal", "tight detail crops" |
| Furniture | "interior magazine photography", "lifestyle context with natural light", "scale figures", "natural materials" |
| Beauty / personal care | "bathroom-natural light", "soft mirror reflections", "fresh wet skin", "lifestyle vignette" |
| Wellness / supplements | "morning routine lifestyle", "natural light through window", "scattered props suggesting rituals" |

Pick the genre that matches your product. The vocabulary doesn't just describe what you want — it anchors the model to a body of training data tagged with that genre.

## Iteration vocabulary

Once a first generation lands, refine with specific deltas:

- "Same composition but [shift one variable]": "same composition but evening lighting instead of midday"
- "Same lighting but [shift one variable]": "same lighting but the product moved to the right third"
- "Keep [specific], change [specific]": "keep the marble background, change the bottle to amber glass"

Avoid "make it better", "make it more dynamic", "more aesthetic" — those produce drift, not improvement.
