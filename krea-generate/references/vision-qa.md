# Vision QA — read every frame before approving it

Every image and video frame this skill generates **must be read back with vision** before being approved, shown to the user, or used as input to a downstream model. Looking at the URL coming back from the API and trusting the prompt is not a review. Render output drifts from prompt intent constantly; the only way to catch that is to look.

A blind director ships bad cuts.

## When this applies

- Asset-sheet stills (character turnarounds, prop sheets, location plates)
- Scene-composition stills in any narrative workflow (`narrative-video-long.md`, `key-visual-sheet.md`, `full-ad-campaign.md`)
- Any frame that will be passed as `start_image`, `end_image`, or `reference_images` to a video model
- Last-frame extracts pulled with ffmpeg for chain continuity
- Final concatenated outputs (sample several frames spaced across the timeline)

## How to QA a still

After the file is on disk, open it with the `Read` tool — that's what gives the vision pipeline the pixels. Then write a short critique pass, **one observation per line**, covering:

1. **Subject legibility.** Does the named subject read clearly at thumbnail size? If you have to squint to find the protagonist, the next clip will lose them.
2. **Named action present.** If the prompt called for "a stretched rubber arm with the fist three meters past the body", is the arm actually visible and connected? Or is the fist a disembodied blob? If the model dropped or fudged the named action, the next clip won't be able to animate it.
3. **Identifying details.** Hat, scar, weapon, horns, costume hardware, signature aura — each named identifier should be visible. Missing details mean character drift in the next scene.
4. **Lighting and color temperature.** Does it match the brief? Does it match adjacent scenes' palette? Drift here is what makes assembled cuts feel like random concat.
5. **Composition energy.** Is the subject framed with intent (rule-of-thirds, leading lines, deliberate negative space) or shoved into a corner with empty middle?
6. **Continuity hook for the next clip.** If this is an `end_image`, can a video model plausibly interpolate motion from the previous `start_image` to here? The spatial story between the two frames must be clear — fist moving left-to-right, character walking forward, eye opening. If the two frames have no shared motion vector, the clip in between will either fail or produce visual mush.

## What to do when a still is weak

State the weakness in one direct sentence, then offer a fix. **Do not bury weak stills under generic praise.** "Three of these are solid; B is weak because the rubber arm isn't connected to the body — want me to regenerate B with a sharper composition?" is the right shape.

Never approve based on the prompt alone ("I asked for X so it must be X"). Look at what the model actually produced.

## Batch reviews

When a workflow generates a batch of stills in parallel (asset sheet, chain keyframes), Read every one individually and grade each on its own line:

> A (Luffy turnaround) — clean, scar visible, hat shadow as briefed. ✓
> B (Gear-3 first touch) — fist reads as a disembodied black blob, no visible arm trail. Composition shoved to the left. ✗ regenerate.
> C (Gear-5 + Azure Dragon) — silver hair and golden aura present, dragon clearly serpentine, golden eye on subject. ✓
> ...

If three of four pass and one fails, regenerate the failing one immediately — don't proceed to the video step with a weak link in the chain. The cost of regenerating a still is a few seconds and a handful of CU; the cost of a Seedance clip refusing or producing mush because its end_image was unclear is minutes of wall-clock and a confused user.

## Video frame sampling

For the final concatenated cut, extract frames spaced across the timeline (every ~2s) with ffmpeg and Read them. Catch:

- Identity drift between scenes (character looks different in scene 3 vs scene 5)
- Hard cuts that aren't intentional cuts
- Color-temperature jumps that weren't planned in the storyboard
- Last-frame-of-N → first-frame-of-N+1 mismatch when the chain hook didn't take

## Why this matters

Generative models hallucinate, drop details, soften prompted actions into ambiguity, and occasionally invent things the prompt didn't ask for. None of that is visible from the job-status response. The only signal is the pixels. Skipping the vision pass is a guaranteed way to ship a bad cut and then discover the problem only after the user pushes back.
