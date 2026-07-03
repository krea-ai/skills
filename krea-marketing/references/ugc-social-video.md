# UGC Social Video

Use this when the user asks for UGC, creator content, GRWM, TikTok-native review, selfie ad, casual testimonial, or "make it feel real". For scripted talking-head ads, this pairs with `ugc-scripts.md` and `../workflows/ugc-video-ad.md`.

## Realism Rubric

These clauses are mandatory for UGC generation prompts, not optional flavor. Outputs built from bare prompts read as AI-perfect and are unusable as creator content.

**Skin and face** (the #1 authenticity signal):

- natural skin texture, visible pores, subtle freckles or fine facial hair
- no plastic shine, no airbrushed smoothing
- subtle facial asymmetry - perfect symmetry screams AI
- micro-expressions, not a frozen smile
- genuine eye catchlights from the room's actual light

**Framing and grain**:

- vertical phone framing, selfie POV or phone-on-table POV
- slight handheld micro-shake and tilt, imperfect composition - real people don't nail the rule of thirds
- mild digital noise/grain, warm phone color grade, shallow phone-portrait depth of field
- framed waist-up, hands free; the subject must NOT hold a phone unless the user asks for it
- creator glances at screen, not a perfect lens lock

**Setting**:

- natural daylight or room light only
- casual clutter in frame; unpolished room, car, bathroom, kitchen, gym, or desk
- product enters imperfectly, not like a studio reveal
- quick cutaway to product in ordinary use
- caption sticker or native social text overlay

**Prompt-word trap**: do not write "selfie" in generation prompts - video models carry a strong selfie=subject-holding-phone-with-both-hands prior. Use "talking-head close-up", "vertical front-camera video", or "phone-framed close-up" to get the composition without the phone.

## Look Presets

Pick one per piece and keep it consistent across takes:

- **natural**: soft window daylight, gentle wrap shadows, ambient room reflections in the eyes. Default.
- **commercial-casual**: clean soft key light, tidier backdrop, skin texture still preserved - polished creator, not a studio ad.
- **raw phone**: unedited front-camera energy, raw HDR, slight handheld breathing, mild low-light grain, imperfect exposure. Most authentic; best for confession/problem hooks.

## Banned Vocabulary

Avoid commercial-polish words for UGC:

- cinematic
- editorial
- commercial
- studio
- professional
- crane shot
- dolly
- push-in
- key light
- cinematic grading
- luxury product film

## Talent Consistency

For a campaign or multi-take script, the creator must be the same person in every clip:

- lock 2-3 varied face reference images and reuse the exact same set on every take and every variant
- a text-only persona description regenerates a new face each job - fine for one-off single takes, never for multi-take or campaigns
- for a recurring brand creator, train a face LoRA via `../../krea-generate/workflows/lora-train-and-use.md`
- keep the look preset, wardrobe, and setting family stable across a batch so variants read as one creator's feed

## Six-Panel UGC Storyboard Template

1. **Hook**: surprised reaction or caption sticker; product partly visible.
2. **Reveal**: product near face or hand, label readable.
3. **Action**: opening, using, applying, pouring, wearing, or trying the product.
4. **Human beat**: sip, reaction, aside to camera, side-eye, smile, doubt, or tiny mistake.
5. **Proof point**: one supported benefit or product detail, shown casually.
6. **Outro**: product lands in everyday context with CTA/caption; no polished end card unless requested.

## Adversarial QA

After generating a UGC storyboard or clip, inspect it with a skeptical question:

```text
Would a TikTok/Reels viewer read this as real creator content, or does it look like a brand ad pretending to be UGC? Be blunt. Name the giveaways.
```

If the answer points to polished lighting, perfect camera movement, sterile space, product-hero framing, AI-perfect skin, or generic creator behavior, revise the storyboard before animating. For assembled ads, follow with the full scorecard in `video-ad-qa.md`.
