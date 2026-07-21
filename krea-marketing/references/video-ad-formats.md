# Video Ad Formats

The video analog of `dtc-ad-formats.md`: a named library of short-video ad formats,
adapted from studying Higgsfield's Marketing Studio format taxonomy without copying
preset prompts, slugs, or parameters. Each entry is a brand-agnostic **structure +
treatment** spec written Seedance-native — templates follow the prompt rules in
`../../krea-generate/references/models/seedance-2.md` and assume that doc is loaded
when a `seedance-2` variant is the resolved video model.

This is a **variation menu, not a routing table**. The executing workflow stays the
one the router picked (`ugc-video-ad.md`, `social-video-short.md`, or
`cinematic-product-ad.md`); formats are consumed at the storyboard/prompt step to
name the creative direction, and as axes for A/B/C variants per
`storyboard-variations.md`.

Two layers per format, mirroring the static library:

- **Structural device** — the beat structure that makes it *that* format (a
  setup→reveal, two labeled states, a locked POV). The QA target: if the device
  isn't legible in the output video, the clip is off-type and must be retaken.
- **Treatment** — camera, light, energy, and audio recipe.

## A. How to use

1. The workflow's Clarify step is running; the brief names a product, platform,
   aspect, and duration. Offer formats from the registry (section D) that fit the
   product type and route — or match the format the user named ("crush test",
   "ASMR unboxing").
2. Loose brief → pick 3 formats from different families as the A/B/C storyboard
   variants (this satisfies the two-axis rule in `storyboard-variations.md`).
3. Fill the chosen template's `{{placeholders}}` and append the universal tail
   `<VTAIL>` (section C).
4. Real-product evidence rules apply unchanged: inspect the reference with vision
   first, keep `{{product}}` category-level ("the referenced water blaster"), and
   keep material/color/garment descriptors out of the prompt — `@Image1` carries
   the product. Attach it through the schema field (`reference_images`, or
   `start_image` when the product shot opens the clip), never prompt text alone.
5. Dialogue formats obey the script gate and 2-4 words/second law in
   `ugc-scripts.md` before any generation. Captions, CTA cards, and logos are
   burned in post per `video-ad-post.md` — never asked of the video model.

## B. Cross-format prompt checklist

Every filled template must pass this before submission:

- Subject + action land in the first ~15 words.
- Exactly **one primary camera instruction** (fixed, slow push-in, slow orbit,
  slow pull-out, handheld tier, or locked POV). Named cuts only via fully staged
  beats per the seedance-2 beat budget (≤2.5s per beat).
- A lighting phrase is present.
- Any spoken line is in quotes, 5-10 words per beat, tagged to one clear speaker;
  two speakers are always labeled.
- Never stack "fast" on more than one of: camera / subject motion / cut pace.
  One element carries the energy; the others hold steady.
- Pacing vocabulary rules hold: never `slow`, `gentle`, `soft`, `slow motion` —
  use `smooth`, `steady`, `natural realtime`; deliberate ramps use the
  `RAMPS TO SLOW MOTION` / `SNAPS BACK` syntax from the seedance-2 doc.
- Total prompt roughly 60-120 words for single-shot formats; multi-beat formats
  follow the staged-timeline architecture instead.

## C. Universal tail `<VTAIL>`

Append to every filled template. Preservation instruction, not permission to name
product colors/materials:

> Natural realtime motion, smooth and steady. Keep the referenced product
> (@Image1) true to the provided image in shape, color, label, and proportion —
> no warped text, no logo distortion. No on-screen text, captions, or added
> graphics. Avoid jitter beyond the format's stated handheld level, bent limbs,
> extra fingers, and identity drift.

## D. Format registry

`route`: U = `ugc-video-ad.md` (spoken), S = `social-video-short.md`,
C = `cinematic-product-ad.md`.

| id | family | route | structural device (QA target) | notes |
|---|---|---|---|---|
| `ugc-native` | talking | U | one creator, talking-head close-up, one quoted hook line + one natural gesture | the default; never the word "selfie" |
| `selfie-testimonial` | talking | U | arm's-length phone framing, one specific claim line, small proud reaction | the one format where the selfie=phone prior is wanted |
| `direct-to-camera` | talking | U | centered composed address, fixed or slow push-in, no handheld | reads intentional, not grabbed |
| `problem-relief` | talking | U | visible struggle → product picked up → relief line naming the solved problem | relief must be acted, not stated |
| `hack-reveal` | talking | U | old/annoying way → pause → product reveal on a push-in + "hack" line | two beats, one camera move |
| `obsession-loop` | talking | U | immediate repeat use, can't-stop energy, one confession line | one clean loopable beat, not crammed repeats |
| `couple-share` | talking | U | two people, shared activity, labeled A-line + B-reaction | label both speakers; simple motion only |
| `tutorial-steps` | talking | U | ordered first/then/finally demo, one short spoken cue per step | each step its own 5-10 word beat |
| `unboxing-spoken` | talking | U | box open → lift out → quoted reaction on the reveal | budget the line for the reveal beat |
| `tv-spot` | talking | U | narrative mini-commercial, one deliberate camera move, BGM under dialogue | the only talking format allowed polish vocabulary |
| `asmr-unboxing` | sensory | S | extreme close-up hands unboxing; named crisp sound cues; no dialogue | SFX list is the format |
| `reboxing` | sensory | S | deliberate precise placement back into molded slots, settling sounds | precision, not fumbling |
| `crush-test` | sensory | S | product under one stress event, fixed camera, impact SFX | never pair with camera movement |
| `giant-scale` | spectacle | S | house-sized product over an ordinary scene, slow pull-out reveals scale | lives or dies on stated scale contrast |
| `hyper-motion` | spectacle | S | one fast subject action, camera fixed or slow-tracking | the one format where fast is earned — subject only |
| `pov-immersive` | spectacle | S | camera IS the eyes, hands in frame, perspective locked | requires the negation lock from the seedance-2 doc |
| `mystery-reveal` | spectacle | S | approach → hesitate → open → reveal, one slow push-in throughout | lighting shifts moody→bright on the reveal |
| `style-blend` | spectacle | S | treatment shifts between two named concrete aesthetics across one move | name both anchors precisely, never "classic"/"modern" |
| `before-after` | two-state | S | two labeled states, product the only changed variable | environment/light identical across states |
| `mess-to-fresh` | two-state | S | chaotic state → resolved state after product use | staged as two beats, not a dissolve |
| `product-showcase` | product-led | C/S | product centered, slow orbit or push-in, studio light, label locked | closest to pure image-to-video; multi-beat versions route C |
| `unbox-and-use` | product-led | S | unbox then immediately use/wear in one continuous take | two actions, one slow push-in carries both |
| `ugc-try-on` | product-led | U | product worn/used on-body with UGC realism cues + one opinion line | wearables/apparel only — flag mismatch otherwise |
| `pro-try-on` | product-led | S | composed try-on, fixed or slow camera, designed light, dialogue optional | polished variant of `ugc-try-on`; same wearables flag |

A "wild card" concept that maps to none of these is not a format — build it from
the executing workflow's own recipe and the seedance-2 prompt skeleton directly.

## E. Templates

Talking-format templates carry dialogue placeholders that must already have passed
the script gate. `{{light}}` is a natural-light phrase for UGC-family formats and
a designed-light phrase for composed ones.

**`ugc-native`** — Vertical front-camera video, {{duration}}s, {{aspect}}. A {{persona}} in {{setting}}, talking-head close-up, {{energy}} energy, holding the referenced product (@Image1). Says: "{{hook_line}}". One small natural gesture. Slightly handheld — gentle living handheld that barely breathes — {{light}}, warm phone-camera look, no studio polish. `<VTAIL>`

**`selfie-testimonial`** — Selfie-style framing, {{duration}}s, {{aspect}}: a {{persona}} holds the phone at arm's length in {{setting}}, holds up the referenced product (@Image1). Says: "{{claim_line}}". {{small_reaction}}. Slight handheld selfie sway — natural, not stabilized — {{light}}. `<VTAIL>`

**`direct-to-camera`** — A {{persona}} sits centered against {{backdrop}}, {{duration}}s, {{aspect}}, addressing camera directly with the referenced product (@Image1) in hand. Says: "{{composed_line}}". Camera fixed with one smooth steady push-in. Clean {{light}}. Intentional framing, no handheld. `<VTAIL>`

**`problem-relief`** — A {{persona}} in {{setting}} visibly {{struggle_action}}, then picks up the referenced product (@Image1), relief breaking across their face. Says: "{{relief_line}}". Camera fixed, {{light}}, casual handheld UGC look. {{duration}}s, {{aspect}}. `<VTAIL>`

**`hack-reveal`** — Beat 1 (0-{{t1}}s): a {{persona}} in {{setting}} demonstrates {{old_way}}, sighs. Beat 2 ({{t1}}-{{duration}}s): they hold up the referenced product (@Image1) as the camera makes one smooth push-in. Says: "{{hack_line}}". {{light}}. {{aspect}}. `<VTAIL>`

**`obsession-loop`** — A {{persona}} in {{setting}} uses the referenced product (@Image1) again the moment it's ready, restless can't-stop energy. Says: "{{confession_line}}". Camera fixed. {{light}}. One clean loopable beat, {{duration}}s, {{aspect}}. `<VTAIL>`

**`couple-share`** — {{person_a}} and {{person_b}} in {{setting}}, {{shared_activity}} with the referenced product (@Image1). {{person_a}} says: "{{a_line}}". {{person_b}} {{b_reaction}}. Camera gentle handheld, held on a two-shot. {{light}}. {{duration}}s, {{aspect}}. `<VTAIL>`

**`tutorial-steps`** — A {{persona}} demonstrates the referenced product (@Image1) step by step in {{setting}}: first {{step_1}}, then {{step_2}}, finally {{step_3}}. One short spoken cue lands on each step, e.g. says: "{{instruction_line}}". Camera fixed, clear even {{light}}. Steady unhurried pacing, {{duration}}s, {{aspect}}. `<VTAIL>`

**`unboxing-spoken`** — A {{persona}} opens the product box on {{surface}} in {{setting}}, lifts out the referenced product (@Image1). On the reveal, says: "{{reaction_line}}". Camera one smooth push-in timed to the reveal. {{light}}. {{duration}}s, {{aspect}}. `<VTAIL>`

**`tv-spot`** — A {{persona}} in {{aspirational_setting}}, {{narrative_action}} with the referenced product (@Image1). Says: "{{polished_line}}". Camera: one deliberate {{camera_move}}. Cinematic {{light}}, polished commercial style. Audio: warm understated music under the dialogue, natural diegetic sound. {{duration}}s, {{aspect}}. `<VTAIL>`

**`asmr-unboxing`** — Extreme close-up, {{duration}}s, {{aspect}}: hands steadily peel the tape and lift the lid of the product box on {{textured_surface}}, revealing the referenced product (@Image1). Audio: crisp tape peel, cardboard flex, {{product_sound_cues}}. No dialogue, no music. Camera fixed, one soft directional {{light}} emphasizing texture. Deliberate unhurried hands. `<VTAIL>`

**`reboxing`** — Close-up, {{duration}}s, {{aspect}}: hands deliberately place the referenced product (@Image1) and its accessories back into their molded packaging slots on {{surface}}, each piece clicking and settling precisely. Audio: soft precise placement sounds, a final lid press. No dialogue. Camera fixed, soft {{light}}. `<VTAIL>`

**`crush-test`** — Medium close shot, {{duration}}s, {{aspect}}: the referenced product (@Image1) under {{stress_event}} in {{setting}}, physical consequences rendered precisely — {{physics_detail}}. Audio: {{impact_cues}}. No dialogue. Camera locked and fixed — no camera movement of any kind. {{light}}. `<VTAIL>`

**`giant-scale`** — A giant referenced product (@Image1) the size of {{scale_anchor}} looms over {{ordinary_environment}}, ordinary-sized {{scale_figures}} for contrast, {{light}}. Camera: one smooth steady pull-out revealing the full scale. Surreal advertising style, hyperreal product detail, photorealistic grounding. {{duration}}s, {{aspect}}. Avoid distorted product shape, avoid chaotic composition. `<VTAIL>`

**`hyper-motion`** — The referenced product (@Image1) in one fast {{single_action}} with real physical weight — {{physics_detail}} — in {{dynamic_environment}}. Camera fixed or slow-tracking only, never fast. Punchy {{light}}, high-energy commercial style. Audio: {{action_sfx}}. {{duration}}s, {{aspect}}. Fast subject, steady camera — never both. `<VTAIL>`

**`pov-immersive`** — One continuous first-person shot, {{duration}}s, {{aspect}} — the camera is the character's eyes, no cuts, no zoom, natural head movement, never breaking the viewpoint. Hands raise the referenced product (@Image1) into frame and {{pov_action}} in {{environment}}. Smooth gradual head motion, not chaotic. {{light}}. Audio: natural diegetic sound only. `<VTAIL>`

**`mystery-reveal`** — A {{persona}} approaches an unmarked box in {{setting}}, hesitates, hands resting on the lid, then opens it to reveal the referenced product (@Image1) — {{reaction}}. Camera: one slow push-in sustained across the entire beat, no cuts. Lighting shifts from moody {{light_before}} to bright {{light_after}} on the reveal. {{duration}}s, {{aspect}}. `<VTAIL>`

**`style-blend`** — The referenced product (@Image1) in {{setting}}; the visual treatment shifts from {{style_anchor_a}} to {{style_anchor_b}} as one smooth {{camera_move}} progresses across the frame. Lighting transitions coherently with the treatment. {{duration}}s, {{aspect}}. Avoid abrupt tonal jumps, avoid identity drift. `<VTAIL>`

**`before-after`** — Beat 1 (0-{{t1}}s), the "before" state: {{initial_condition}} in {{setting}}. Beat 2 ({{t1}}-{{duration}}s), fully staged cut to the "after" state: {{improved_condition}} with the referenced product (@Image1) present, same {{setting}} and same {{light}} — the product is the only variable that changed. {{aspect}}. Avoid inconsistent environment details between states. `<VTAIL>`

**`mess-to-fresh`** — Beat 1 (0-{{t1}}s): {{setting}} in a {{chaotic_state}}. Beat 2 ({{t1}}-{{duration}}s), fully staged cut: the same {{setting}}, now {{resolved_state}}, the referenced product (@Image1) in a {{persona}}'s hands. Consistent {{light}} across both beats. {{aspect}}. Avoid environment drift between states. `<VTAIL>`

**`product-showcase`** — The referenced product (@Image1) centered on {{clean_surface}}, {{duration}}s, {{aspect}}. Camera: one smooth steady orbit. Soft studio key light with a subtle rim light on the edge. Premium ecommerce style, shallow depth of field. No hands, no dialogue. Audio: quiet ambient tone. `<VTAIL>`

**`unbox-and-use`** — One continuous take, {{duration}}s, {{aspect}}: a {{persona}} opens the product box on {{surface}}, lifts out the referenced product (@Image1), and immediately {{use_action}} with {{reaction}}. Camera: one smooth push-in carrying both actions, no cuts. {{light}}. `<VTAIL>`

**`ugc-try-on`** — Vertical front-camera video, {{duration}}s, {{aspect}}: a {{persona}} in {{casual_setting}} puts on the referenced product (@Image1), checking the fit. Says: "{{opinion_line}}". Slightly handheld, {{light}}, phone-camera look. Keep the product's shape and fit on the body accurate. `<VTAIL>`

**`pro-try-on`** — A {{persona}} in {{composed_setting}} wears the referenced product (@Image1), moving with deliberate composed motion — {{movement}}. Camera fixed or one slow orbit at {{framing_height}}. Designed {{light}}, polished commercial style. Keep the product's shape and fit on the body accurate. {{duration}}s, {{aspect}}. `<VTAIL>`

## F. Worked example

Brief: pink motorized water blaster, real product reference uploaded as `@Image1`
(`reference_images`), format `problem-relief`, 9:16, 10s, warm late-afternoon
light. Because a real reference exists, the prompt names only the scene — no
color/material words:

> A dad in a sunlit backyard, breathing hard mid water-fight, strains at pumping
> an old hand-pump water gun, then picks up the referenced product (@Image1),
> relief breaking across his face. Says: "No more pumping — it just fires."
> Camera fixed, warm late-afternoon light, casual handheld UGC look. 10s, 9:16.
> Natural realtime motion, smooth and steady. Keep the referenced product
> (@Image1) true to the provided image in shape, color, label, and proportion —
> no warped text, no logo distortion. No on-screen text, captions, or added
> graphics. Avoid jitter beyond the format's stated handheld level, bent limbs,
> extra fingers, and identity drift.
