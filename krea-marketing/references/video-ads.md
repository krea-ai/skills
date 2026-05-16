# Video Ads — Five Recipes

Five canonical video-ad shapes with full templates. Every video workflow uses the async + poll pattern from `../../krea-ai/references/async-polling.md` — `sync=false` then `get_job(jobId=...)` until terminal.

## Pre-flight (every video)

1. `Read` any user-uploaded reference (product photo, person photo, brand image) with vision
2. Confirm duration and aspect with the user — videos are expensive, get this right before submitting
3. Resolve model archetype from `../../krea-ai/references/model-catalog.md`:
   - **Cinematic / production-quality** → cinematic video archetype
   - **Fast / testing / volume** → fast video draft archetype
4. `get_model_schema(model=<id>)` to confirm the exact input shape (`startImage`, `aspectRatio`, `duration`, audio flag if any). Don't hardcode model names; resolve via `list_models()`.
5. Upload reference via `upload_asset` if needed
6. Submit async, poll, deliver

## Audio: visuals first, voiceover separate

Video models generate **ambient / atmospheric audio** when their schema supports `generateAudio: true` (or equivalent) — engine sound, room tone, contextual noise. They do NOT generate scripted speech with lip-sync that a brand would actually ship.

For UGC, talking-head, and demo recipes that involve speaking:

- **Generate visuals first.** Use `generateAudio: false` so the model doesn't produce muffled gibberish speech that has to be stripped out anyway.
- **Add voiceover separately.** Use a TTS or human voice-over to record the script, then overlay it in post-production (ffmpeg, video editor).
- **Lip-sync.** If lip-sync to the spoken script is required, check whether the chosen model supports a lip-sync input (some Krea video models do; verify via `get_model_schema`). If not, lip-sync needs a separate downstream tool — out of scope for this skill.
- **Get the script from the user.** Don't write ad copy speculatively for the model to "say". The user owns the brand voice and the claims; you generate the visuals around the script they give you.

Bottom line: the agent's job in this skill is **visual generation**. Voiceover, lip-sync, and post-production are downstream of what this skill ships.

## Recipe 1: UGC-style

Casual, selfie-POV, social-media-native. Looks like a real person filmed on phone. Default for TikTok / Reels.

**Prompt template (with start frame of person + product):**
> A casual UGC-style video, [PERSON DESCRIPTION] holds the [PRODUCT] up to the camera in a [SETTING — bedroom / bathroom / kitchen / outdoor café], natural selfie framing on phone camera, [ACTION — they unbox the package / they spray and pose / they take a sip / they apply and react], soft natural light, slight handheld camera shake, candid not polished, social-native feel

**Defaults**: duration 5-8s, aspectRatio 9:16, generateAudio true (model-dependent — verify via schema), resolution 720p for testing / 1080p for final.

**Worked example** (skincare serum unboxing):
> A casual UGC-style video, a young woman in a soft cream sweater holds the small amber dropper bottle of serum up to the camera in a sunlit bathroom, natural selfie framing on phone camera, she unboxes the small kraft paper packaging and lifts the bottle into view with a small genuine smile, soft morning light through frosted window, slight handheld camera shake, candid not polished

**Common failures**: looks too produced. Fix: add explicit "phone camera quality", "candid not polished", "natural micro-expressions" cues.

## Recipe 2: Product showcase

Product-centered, rotation or movement, polished lighting, no person. Default for hard-sell ads, hero video assets.

**Prompt template (with start frame of product on staged background):**
> Polished product showcase video of [PRODUCT] centered on [BACKGROUND], slow camera rotation around the product / slow pull-back from extreme close-up / subtle lighting shifts revealing different surfaces, premium product photography in motion, soft studio lighting, sharp focus, [DURATION] seconds

**Defaults**: duration 5-8s, aspectRatio 16:9 (or 1:1 for IG square ads), generateAudio false (music added later), resolution 1080p.

**Worked example** (perfume bottle):
> Polished product showcase video of a frosted glass perfume bottle centered on a warm marble pedestal, slow 30-degree camera rotation around the bottle revealing the brushed gold cap from multiple angles, subtle warm lighting shifts catching the bottle's facets, soft cream gradient background, premium fragrance photography in motion, 6 seconds

**Common failures**: feels static. Fix: name specific motion ("slow 30-degree rotation", "pull-back from extreme close-up to full view") rather than generic "rotate" or "move".

## Recipe 3: Talking head

Presenter explains the product. More produced than UGC. Suitable for tutorials, founder pitches, expert endorsements.

**Prompt template (with start frame of presenter + product):**
> Polished talking-head video, [PRESENTER DESCRIPTION] holds the [PRODUCT] in [SETTING — clean modern home interior / minimalist studio / branded kitchen], natural presenting gestures and micro-expressions, eyes engaging the camera, [SPECIFIC ACTION — points to a feature / demonstrates a function / takes a small bite / sniffs and reacts], soft three-point lighting, slight rack focus between product and face, clean professional ad-spot quality

**Defaults**: duration 8-15s (talking head needs room for the pitch), aspectRatio 9:16 or 16:9 depending on placement, generateAudio true, resolution 1080p.

**Worked example** (founder for a kitchen tool):
> Polished talking-head video, the founder in his late 30s wearing a chef's apron holds the precision kitchen knife in a clean modern home kitchen, natural presenting gestures with genuine confidence, eyes engaging the camera, he angles the blade to catch the light and points to the wave-pattern Damascus steel, soft three-point lighting with warm fill, slight rack focus between the knife and his face, professional ad-spot quality, 10 seconds

**Common failures**: presenter looks unnatural / robotic. Fix: emphasize "natural micro-expressions", "genuine confidence", "specific gesture" rather than generic "explains the product".

## Recipe 4: Before / after

Transformation reveal. Split-frame or transition. Default for skincare, cleaning, home improvement, fitness.

**Prompt template (with start frame showing 'before' state):**
> A before-and-after reveal video, opens on [BEFORE STATE — dull skin / cluttered countertop / unkempt before-state], smooth transition (camera wipe / quick cut / dissolve) to [AFTER STATE — radiant skin / clean countertop / polished after-state], the [PRODUCT] visible in the middle of the transformation, clean editorial style, [DURATION] seconds

**Defaults**: duration 5-8s, aspectRatio 9:16 (most before/after lives on TikTok / Reels), generateAudio true, resolution 1080p.

**Worked example** (skincare):
> A before-and-after reveal video, opens on a close-up of skin with visible dullness and uneven texture under cool morning light, smooth dissolve transition to the same skin appearing radiant and even under warm golden light, the small amber dropper bottle of serum visible briefly in the middle of the transformation in the model's hand, clean editorial close-up framing, 6 seconds

**Common failures**: transition feels jumpy / unconvincing. Fix: name the specific transition type ("smooth dissolve", "camera wipe right-to-left", "quick cut with light flash") and ensure the before and after are visually distinct enough that the transition reads.

## Recipe 5: Demo / product-in-use

Action-forward. Shows the product doing its thing. Default for tools, gadgets, kitchenware, cleaning products.

**Prompt template (with start frame of product mid-use):**
> Action demonstration video of [PRODUCT] in active use, [SPECIFIC ACTION — slicing through a ripe tomato / spraying onto a fogged mirror and clearing it / kneading dough on a butcher block], close-up on the moment of action, clean clear function-forward framing, soft directional lighting emphasizing the action, [DURATION] seconds, satisfying mechanical quality

**Defaults**: duration 4-8s, aspectRatio 9:16 or 16:9 depending on placement, generateAudio true (action sounds add a lot here), resolution 1080p.

**Worked example** (precision knife):
> Action demonstration video of the precision Damascus kitchen knife slicing through a ripe heirloom tomato on a wooden butcher block, close-up on the moment of contact and clean cut, the blade visibly catching the light as it moves, the tomato falling cleanly into two halves with visible juice, soft directional lighting from upper-left, satisfying mechanical quality, 5 seconds, slight slow-motion on the moment of cut

**Common failures**: action looks fake / floaty. Fix: name specific mechanical details ("tomato falling cleanly into two halves", "blade visibly catching the light"), use models with strong physics (Hailuo, Seedance) over models with weak physics for action shots.

## Cost-aware defaults

| Phase | Duration | Resolution | Model archetype |
|---|---|---|---|
| Exploratory / testing | 4-5s | 720p | Fast video draft |
| Client iteration | 5-8s | 1080p | Cinematic video |
| Final production | 8-15s | 1080p (4K rarely worth it) | Cinematic video |

Always preflight cost for any video > 10s. For batch generation of multiple variants, confirm explicitly before submitting.

## Audio handling

- Most models support `generateAudio: true` as a boolean — but the schema differs per model. Always check via `get_model_schema`.
- UGC, talking head, and demo recipes benefit from audio. Product showcase and before/after typically have music added in post and don't need generated audio.
- If the user has a specific soundtrack in mind, generate audio off OFF and overlay later — generated audio is generic.

## Polling pattern (every video)

```
job = generate_video(
  model=<chosen>,
  input={prompt: "...", startImage: <upload_url>, duration: 5, aspectRatio: "9:16", ...},
  sync=false
)
# job.id is available immediately

# Then poll every 10s:
loop:
  status = get_job(jobId=job.id)
  if status.status in ("completed", "failed", "cancelled"): break
  sleep 10

# On completed: download, Read with vision, verify, deliver
# On failed: surface the reason, offer retry with adjustments
```

See `../../krea-ai/references/async-polling.md` for full details.
