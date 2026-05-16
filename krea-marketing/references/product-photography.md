# Product Photography

Four sub-workflows for the most common DTC product imagery needs, plus the click-to-ad orchestrated pipeline.

## Sub-workflows

### Hero shot

The flagship product image. Dramatic lighting, clean background or carefully-staged context, product as the unambiguous subject.

**When**: homepage hero, PDP hero, ad creative anchor, press release.

**Prompt template**:
> Photoreal hero product shot of [PRODUCT], [BACKGROUND — gradient / marble / fabric / dramatic neutral], [LIGHTING — soft directional from upper-left / studio softbox / golden window light], [CAMERA — 50mm at slight downward angle / 85mm head-on], [SURFACE INTERACTIONS — soft reflection on the polished plinth / subtle contact shadow / water droplets catching highlights], premium product photography, sharp detail, shallow depth of field on the foreground while preserving full product clarity

**Worked example** (perfume bottle):
> Photoreal hero product shot of a minimal frosted glass perfume bottle with brushed gold cap, soft gradient marble surface in cream-and-warm-grey, soft directional lighting from upper-left creating a long contact shadow, polished plinth showing subtle reflection beneath the bottle, single water droplet caught in highlight on the shoulder of the bottle, shot on 85mm at slight downward angle, premium fragrance photography, sharp detail with shallow depth of field

**Model**: resolve a high-fidelity image archetype via `../../krea-ai/references/model-catalog.md`. Call `list_models()` then `get_model_schema(model=<id>)` to confirm the actual ID and input shape — don't hardcode.

### Lifestyle / in-context shot

Product placed in a real-world context that suggests the use case and target audience.

**When**: secondary PDP images, social media posts that aren't hard-sell, ad creative with emotional appeal.

**Prompt template**:
> Lifestyle product photograph of [PRODUCT] in [CONTEXT — kitchen counter / bathroom vanity / desk / gym bag / outdoor café], [TIME / LIGHTING — morning light through window / evening warm lamp / midday natural], [SCENE DETAILS — coffee mug nearby / open notebook / linen napkin / plants in soft focus], suggesting [TARGET AUDIENCE LIFESTYLE — minimalist creative / busy professional / wellness routine], natural product placement, candid feel

**Worked example** (skincare serum):
> Lifestyle product photograph of a small amber dropper bottle of skincare serum on a clean marble bathroom vanity, soft morning light through a frosted window casting diffused light, folded white linen washcloth nearby, single fresh-cut eucalyptus stem in a small ceramic vessel, suggesting a minimalist wellness routine, natural product placement, candid feel, shot on 50mm

**Model**: image-to-image with the product as reference. The reference anchors the product's specific design.

### White-background ecommerce shot

Clean catalog-style image for marketplace listings, ecommerce PDPs, ad creative testing.

**When**: Amazon listings, Shopify product gallery, marketplace cards, A/B test variants.

**Prompt template**:
> Clean white-background product photograph of [PRODUCT], pure white seamless background, soft even lighting from front and slightly above eliminating harsh shadows, subtle contact shadow beneath product for grounding, sharp focus across the entire product, true colors, catalog photography style, no creative flourishes, product centered in frame

**Worked example** (running shoe):
> Clean white-background product photograph of a sleek black-and-white running shoe, pure white seamless background, soft even lighting from front and slightly above, subtle contact shadow beneath the shoe, sharp focus across all surfaces, true colors as in the reference, catalog photography style, shoe positioned at a slight 3/4 angle showing the medial side

**Model**: high-fidelity image-to-image. The product reference is critical here — accuracy of the shoe's actual design beats aesthetic embellishment.

### Social-square shot

Product image cropped or composed for social-media native aspects (square / portrait / story).

**When**: Instagram feed, TikTok still posts, story / reel cover frames, Pinterest pins.

**Prompt template**:
> Social-media product shot of [PRODUCT], [ASPECT — 1:1 square / 4:5 portrait / 9:16 vertical], [STYLE — clean minimal / lifestyle context / bold graphic], [COLOR PALETTE — brand-aligned colors named explicitly], composition optimized for [PLATFORM CROP — Instagram feed / TikTok / Reels], product as the focal point with room for overlay text in the upper third / lower third / one side

**Model**: high-fidelity image with platform-appropriate `aspectRatio`.

## Click-to-Ad workflow

The orchestrated pipeline: user pastes a product URL, agent extracts product info, confirms in one line, then ships a hero shot plus social variants. "Click-to-ad" isn't fully autonomous — there's exactly one confirmation gate (so the user can correct the extracted brief before 5 generations run).

### Pattern

```
1. WebFetch(url=USER_URL, prompt="Extract a structured product brief for ad creative:
   - product name + one-line description
   - key visual features (color, material, distinctive shape)
   - primary hero image URL
   - target audience cues (who's this for, based on copy and imagery)
   - brand palette if visible (hex codes if possible)
   - product category (beverage, skincare, electronics, apparel, etc.)
   - notable claims or selling points (premium, sustainable, organic, etc. — IF stated on page)
   - price tier if visible (budget, mid-range, premium)
   Return only what's actually on the page. Do not invent claims.")

2. Read the extracted hero image (via the URL passed into the next step, or download + Read locally)

3. One-line confirm with the user (then proceed unless they object):
   "Found: [product name]. Generating a 16:9 hero shot + 4 social variants
   (TikTok 9:16, IG 1:1, IG portrait 4:5, Pinterest 2:3)."

4. Generate hero shot:
   generate_image(
     model=<high-fidelity image-to-image>,
     input={
       prompt: "<hero shot prompt incorporating the extracted product features>",
       imageUrl: <extracted hero image URL>,
       aspectRatio: "16:9",
       resolution: "2k"
     },
     sync=true, timeoutSeconds=60
   )

5. Generate 4 social variants in parallel (or fast-sequential):
   - TikTok 9:16 — vertical, suggest motion / energy in the prompt
   - IG square 1:1 — clean, brand-forward
   - IG portrait 4:5 — lifestyle context
   - Pinterest 2:3 — discovery-style, "save-worthy"

6. Read all 5 outputs with vision, verify the product looks consistent across them

7. Deliver: 5 URLs labeled by platform + one-line summary
```

### Tips

- **Confirm before generating.** Even with a clear URL, the user may have wanted a different angle. One quick confirmation saves 5 wrong generations.
- **Preserve product accuracy across variants.** Reuse the same `imageUrl` reference in all 5 generations so the product reads as the same product. Models can drift on subtle product features (button shape, label position) across independent generations.
- **Brand palette extraction is best-effort.** WebFetch can pull obvious colors, but it's not as good as a human eye. If the user gives you palette info, use it. If not, let the model pick palette from the product reference.
- **Skip Click-to-Ad if the URL doesn't have a clear product image.** If WebFetch returns no hero image, ask the user to upload one — you can't reliably image-to-image without a reference.
- **Don't invent claims.** WebFetch returns what's actually on the page. If the extraction is missing claims, audience cues, or a clear pitch, generate the *photography* (hero + variants) but DO NOT write overlay text or copy that makes claims the page doesn't support — that's an FTC / compliance risk. Visual generation is fine; ad copy with unverified claims is not.
- **Degrade gracefully if extraction is thin.** If WebFetch can't extract a target audience or claims, treat this as product photography (visual only), not as full ad creative. Ship the hero + variants without overlaid copy, and tell the user "I couldn't extract enough from the page to write ad copy — generate visuals only."

### Worked example flow

User pastes: `https://example.com/shop/lemonade-can`

```
WebFetch → returns: { product: "Sparkling Peach Lemonade Can",
                      description: "12oz aluminum can, peach-blossom-pink with cream typography",
                      hero_image_url: "https://example.com/img/can.jpg",
                      palette: ["#F5C2C2", "#FFF5EE", "#3A2A1F"] }

Confirm: "Found: Sparkling Peach Lemonade Can. Generating a 16:9 hero + 4 social variants. OK?"

Hero (16:9):
generate_image(
  model=<flagship>,
  input={
    prompt: "Photoreal hero shot of a sparkling peach lemonade aluminum can,
             peach-blossom-pink can with cream typography, soft gradient
             surface in cream and warm peach, condensation droplets catching
             warm light, single peach blossom in soft focus background,
             premium beverage photography, shot on 85mm",
    imageUrl: "https://example.com/img/can.jpg",
    aspectRatio: "16:9",
    resolution: "2k"
  },
  sync=true
)

TikTok variant (9:16):
generate_image(
  model=<same flagship>,
  input={
    prompt: "Vertical product hero of a sparkling peach lemonade can,
             dynamic composition with motion lines suggesting freshness,
             splashes of ice and peach pieces frozen in motion around the
             can, vibrant social-media-native energy",
    imageUrl: "https://example.com/img/can.jpg",
    aspectRatio: "9:16",
    resolution: "2k"
  },
  sync=true
)

[+ IG square, IG portrait, Pinterest]

Deliver:
"Done. 5 variants for the Sparkling Peach Lemonade can:
 - Hero (16:9): <url>
 - TikTok (9:16): <url>
 - Instagram square (1:1): <url>
 - Instagram portrait (4:5): <url>
 - Pinterest (2:3): <url>
Want me to enhance the hero to 4K for print, or generate 3 more hero variants
with different backgrounds?"
```

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Product looks "like the brand but not the actual product" | Reference image was small / low-res, model interpolated | Re-upload at ≥1024px or use higher-quality WebFetch source image |
| Different products across variants | Each generation drifted from the reference | Always include the same `imageUrl` reference in every variant generation |
| Color shifted (e.g. brand pink reads as salmon) | Lighting in the prompt biased the color | Add explicit color anchoring: "preserving the exact brand peach-pink color" or include hex in prompt |
| Label / typography illegible | Model isn't strong at text rendering | Switch to the text-in-image archetype from `../../krea-ai/references/model-catalog.md` for shots where label legibility matters |
| Wrong aspect / orientation | aspectRatio param not passed or model defaulted | Always pass `aspectRatio` explicitly; verify via dimensions on download |
