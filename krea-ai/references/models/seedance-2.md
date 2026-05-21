# Seedance 2.0 - Prompting Reference

Load this when the resolved video model is `bytedance/seedance-2` (or any `seedance-2` variant). It captures the engine's quirks, the prompt structure it responds to, and the banned-move list. Use alongside the active workflow (`social-video-short.md`, `narrative-video-long.md`, `image-to-video-animate.md`), not instead of it.

For generic camera/motion vocabulary that applies to all video models, see `../prompt-engineering.md`. This file only documents Seedance-specific behavior.

## Prompt structure that works

Write the prompt as one continuous string with inline section labels. Seedance responds to labeled sections better than to flat prose.

1. **Style & Mood** - palette, lighting, lens, atmosphere. Never skip.
2. **Narrative Summary** - one sentence. Optional; trim first if the prompt is getting long.
3. **Dynamic Description** - shot-by-shot in prose. Camera, movement, action. Present tense.
4. **Static Description** - location, props, ambient details. Establish anything `Dynamic` references.
5. **Audio** - (dialogue scenes only) spoken lines plus SFX/BGM. Keep dialogue in its original language - never translate user-supplied lines.

Do not include shot labels (`Shot 1:`) or per-shot timestamps. Rhythm is implied by description density.

## Immersive prompting pattern (alternative to section labels)

The labeled-sections structure above is the safest default. But high-density atmospheric scenes also respond very well to **immersive concept-stacked prose** — one continuous descriptive paragraph that layers era anchor, character, environment, motion, camera, lighting, image artifacts, and mood without separator labels. See the worked example at the end of this file.

Pick immersive prose when:

- The medium itself is the aesthetic (analog film, anime broadcast print, comic, retro game, archive footage).
- The scene is dense or crowded and the prompt itself needs to feel saturated.
- Mood is the content — atmosphere over plot.

Stay with labeled sections when:

- Multi-character dialogue scenes (clean Audio block matters).
- Multi-shot sequences where rhythm is implied by per-block density.
- Bilingual EN+ZH delivery (labels translate cleanly).

### Six anchors of an immersive prompt

In whichever order serves the scene, hit all six:

1. **Era / medium / format anchor.** One sentence at the top locks the entire aesthetic. `Shot on 35mm in 1978 and transferred to worn analog tape.` `Cel-animated 1990s shonen anime broadcast print.` `Captured on early Bolex 16mm with hand-cranked exposure variation.` Every downstream detail inherits this.
2. **Character with sensory specificity.** Not `a young man with a beard`; `a man in his mid-thirties, neatly trimmed auburn-brown beard, blue-green eyes, fair skin with a ruddy flush, sweat-damp hair with confetti stuck in it`. Specific physical detail plus embodied state (sweat, dust, paint smears, breath fog) is the single biggest quality unlock.
3. **Environment as collaborator.** Props with material (`plywood maze of distorted mirror panels`, `yellowed rubber teeth`, `ruffled collars in lemon-yellow`), not abstract nouns. Name lighting fixtures, floor surface, atmospheric particles (fog-machine puffs, talc dust, neon haze).
4. **Camera as co-actor.** The camera does physical things in the world. `Handheld and tight, lurching with each swing, briefly losing focus as a clown's face presses against the lens.` Not just `handheld` — what the handheld camera is doing this second. Camera reactions are part of the action.
5. **Image artifacts as content.** For any stylized medium, name the artifacts the medium produces: film grain, gate weave, color bleed, chromatic aberration, halation, scan lines, VHS smear, anime smear-frames, ink-bleed lineart, jpeg banding. These read as authenticity, not flaws.
6. **Density / negative-space statement.** Explicit one-liner about how full the frame is. `Frame is dense with grinning faces crowding from every angle, almost no negative space.` `Empty corridor, a single figure dwarfed by the architecture.` Without this, Seedance defaults to medium density and crowded scenes feel underpopulated.

End with a **mood summary line** (`Overall feeling: garish, disorienting, and crowded — a carnival horror grounded in animatronics, greasepaint, and dense, popping motion.`) that gives the engine one emotional target.

### Sensory grounding rule (applies to both patterns)

Every character description should answer at least three of: *what is on their body that wasn't there an hour ago, what is wet / dry / dusty about them, what are they touching, what are they about to touch.* Generic appearance (`a brave warrior with a sword`) produces generic output. Embodied appearance (`sword grip slick with rain, knuckles white, breath fogging in the cold`) produces dense output.

### Dialogue inside action

When dialogue is part of the shot, write it inline as part of the action description rather than a separate Audio block:

> Wiping greasepaint off his cheek with his shoulder, he turns to camera and says casually, "Don't forget to like and subscribe." [...] Knocking a puppet back through a cutout, he adds with a small smirk, "Let me know in the comments if you hate clowns."

The labeled Audio block still applies to ambient SFX and score. Inline dialogue keeps performance and action tethered.

## Default duration and camera

- Default to 10 seconds unless the user specifies. Hard cap 15 seconds for one continuous prompt.
- If the user names a specific camera move or angle, it MUST appear verbatim in the final prompt. User camera direction overrides any default the workflow would have chosen.

## Submitting jobs — lead with `-i` raw input

`krea generate video`'s named flags (`--start-image`, `--duration`, `--aspect`, `--prompt`) cover roughly four of Seedance 2.0's twelve+ schema fields. The named flags silently drop:

- `endImage` — the continuity hook that chains scene N's end to scene N+1's start.
- `referenceImages` (up to 9) — character / prop / style refs that lock identity across scenes.
- `referenceVideos`, `referenceAudios` — motion + audio style transfer.
- `generateAudio` — single-boolean toggle that turns Seedance 2 into a sound-on engine.
- `resolution` — 480p / 720p / 1080p; default 720p balances cost and delivery.
- `seed` — reproducibility for re-rolls.
- `effects[]` — preset effect router.

Pass these via `-i field=value` (or `-i "field=[\"a\",\"b\"]"` for arrays). Example:

```bash
krea generate video -m bytedance/seedance-2 \
  --start-image "$START" --duration 10 --aspect 16:9 \
  -i endImage="$END" \
  -i "referenceImages=[\"$HERO\",\"$PROP\"]" \
  -i generateAudio=true \
  -i resolution=720p \
  -i seed=42 \
  -p "<prompt>" \
  --json
```

See `../cli-or-mcp.md` for the full `-i` syntax with arrays, booleans, and numbers.

## Engine constraints (violation = broken output)

These are rendering quirks of Seedance 2.0. Each has bitten previously.

- **Action beats = intent plus named technique, not biomechanics.** Write `spinning back kick connects`, not `left forearm rotates 45 degrees to deflect`. If the user names a specific move, preserve it; if they describe joint mechanics, compress to the move name.
- **Positional travel must be named for combat motion.** Seedance defaults to rendering attack *states* (jaws open, fist clenched, beam visible) rather than attack *trajectories* (fist drives across frame, body knocked back three paces). For any clash, punch, swing, knockback, or chase, write the path explicitly with **direction** (`screen-left to screen-right`), **distance** (`a body-length`, `three paces back`, `to the right edge of the frame`), and **duration** (`over two seconds`). Without all three the engine holds the pose. Anti-pattern: `Luffy mid-Gear-3 attack, his right arm grotesquely inflated, fist driven forward at the camera`. Pattern that travels: `Luffy's Gear-3 fist drives from screen-left across the frame to screen-right over two seconds, the inflated arm extending another body-length as it travels; on impact Kaido's body lifts from the tiles and is driven back three paces toward the right edge of the frame`.
- **Describe force and direction, not the destruction sequence.** Write `driven into the car, metal buckling`, not `thrown into door, glass shatters, uses rebound to sweep leg`.
- **Exit-frame = implicit cut.** A character who leaves frame is gone for the rest of that shot. Never choreograph exit-then-re-entry inside one continuous shot.
- **Off-screen = nonexistent.** State changes must be shown on camera before being referenced.
- **Spatial continuity breaks on cuts.** After every cut, re-anchor who is where and which direction they face.
- **<=3 characters tracked across cuts.** Name the acting pair and interaction vector per shot.
- **Avoid reflection shots** (in blades, puddles, mirrors). Seedance breaks scene geography when rendering reflections.
- **Only describe what can be seen or heard.** No smells, no thoughts. Render `pine needles on the ground, wind moving through branches`, not `the air smells of pine`.
- **Micro-expressions work when written as physics.** `Jaw clenches, nostrils flare`, not `looks angry`.
- **Generic appearance equals generic output.** `A young warrior with a sword` produces a stock asset. `A young warrior, knuckles cracked and bleeding, breath fogging in the cold, sword grip slick with rain` produces a character. Always include sensory grounding — see the immersive prompting pattern.
- **Lock the medium up front for styled looks.** When the aesthetic is the content (analog film, anime, comic, archive footage), commit to era / format in the first sentence rather than scattering style hints throughout.
- **Name image artifacts for styled media.** Grain, gate weave, color bleed, halation, scan lines, smear-frames, ink bleed. Present absence reads as generic AI; explicit presence reads as period / medium authenticity.
- **State frame density explicitly.** Without `dense / crowded / empty / sparse` called out, Seedance defaults to medium density and crowded shots feel underpopulated.

## Cut rules

### Double contrast (mandatory)

Every cut changes both shot size and camera character.

- Shot-size scale: `extreme wide -> wide -> medium -> medium close-up -> close-up -> ECU`.
- Camera modes: handheld, static/locked-off, stabilized tracking, crane/vertical, aerial/drone. Never repeat across a cut.

### Re-anchor after cuts

If a character moves left-to-right before the cut, keep that direction after. State movement direction explicitly. Respect the 180-degree rule.

### Inserts

Sub-second (0.3-0.5s) dramatic punctuation. Any shot size. Rules:

- No story beats inside an insert - static moments only.
- Causally motivated: the viewer must understand why this detail. A hand gripping the hood right after a slam works; a generic boot in a puddle does not.
- Name the subject: `his hand`, `her boot`. Unattributed inserts render wrong content.
- Inserts still obey double contrast.

## Scene archetype router

Identify the archetype before writing. It controls camera behavior and what changes over time.

### Action archetypes

| Archetype | Camera focus | Space dynamic |
|---|---|---|
| Pursuit | Distance closing/opening. Pursued ahead, pursuer behind | Path narrows or opens |
| Duel | Camera lower on the dominant side; dominance alternates | Fighters trade position |
| Impact | Build-up slow -> hit fast -> aftermath slow | Point of contact is center frame |

Decision tree: chase -> Pursuit. Alternating advantage -> Duel. Single decisive contact -> Impact. None of the above -> default Duel.

Duel rule: neither side dominates more than one consecutive beat. If one fighter dominates the whole clip, describe it as a one-sided assault, not a duel.

### General archetypes

| Archetype | What changes | Camera signature |
|---|---|---|
| Journey | Position in space - road, flight, walking | Tracking, aerial, traveling alongside |
| Atmosphere | Nothing - mood is the content | Minimal movement, slow push-in or static hold |
| Reveal | Hidden becomes visible | Pan, crane, dolly reveal |

Decision tree: moves through space -> Journey. Hidden becomes visible -> Reveal. Nothing changes -> Atmosphere. Default -> Atmosphere.

### Dialogue archetypes

| Archetype | Power dynamic | Camera signature |
|---|---|---|
| Confrontation | Both push, dominance trades per exchange | Tight OTS, axis crosses on power shift |
| Interrogation | One extracts, one resists | Low-angle on questioner, push-in on silence |
| Negotiation | Both need something, balanced | Symmetrical framing, matching shot sizes |

Decision tree: both pushing -> Confrontation. Extract/resist -> Interrogation. Balanced need -> Negotiation. Default -> Confrontation.

Dialogue word budget: ~25-30 spoken words fit in 15 seconds. If the user provides more, keep the power-shift line (where dominance flips or truth emerges) plus one line before and one after. Convert the rest to physical behavior.

## Age-blind character rule

Never describe characters by age in either language. Trigger words to avoid: `boy, girl, child, kid, young, teen, little`, and in Chinese `男孩, 女孩, 孩子, 少年, 少女, 小孩, 年轻`.

- With image input: describe by role (`rider`, `figure`, `traveler`, `speaker`), clothing, and action. Label what they do, not who they are.
- Without image input: use functional labels like `a figure in a wool cloak`, `a silhouette against the horizon`.

## Inventory discipline

Before writing, silently catalog every asset the user provided: characters (names, wardrobe, distinguishing features), location (interior/exterior, architecture, lighting), props (only what is explicitly mentioned or shown), and style/atmosphere (palette, contrast, weather, time of day).

Rule: never invent characters, named identities, or props the user did not provide. You may add environmental details (dust, sparks, atmospheric particles) and camera behavior.

Exception: if the user asks you to invent the scene (`come up with a fight scene`, vague `two guys fighting`), you may invent supporting elements - location, props, environmental features - to build an effective scene. Named characters and their core attributes still come only from the user.

## Image references

When the user attaches reference images:

1. Explicit references look like `<<<image_1>>>` and link an image to a specific scene role.
2. Implicit references are attachments without tags - infer which scene element each image describes.

In the prompt, prepend a short legend before the first section label, then use the descriptive label with `(<<<image_n>>>)` on first mention and the label alone after.

## Bilingual EN + ZH output

Seedance was developed by ByteDance and responds well to Chinese-native prompts. When the user asks for bilingual output, or the brief is for a Chinese-language audience, deliver both:

- Output as a JSON array `[{"lang":"en","prompt":"..."},{"lang":"zh","prompt":"..."}]` so the downstream code can route each one cleanly.
- The Chinese version is a native rewrite, not a translation. Use natural film-set syntax, four-character phrases, and Chinese cinematography jargon.
- ZH hard cap: 1,800 characters. If approaching the limit, trim in this order: Narrative Summary first, then Static Description, then Style & Mood (keep at least one sentence), and never cut Dynamic Description entirely.
- Heuristic: one ZH sentence is roughly 40-60 characters. If the EN Dynamic Description runs over 10 sentences, preemptively trim before writing ZH.

For single-language requests, follow the universal UX rule in `../../SKILL.md`: detect the user's language and respond in it.

## Banned phrases (antislop)

These phrases produce flat output. Strip on sight.

- English: `breathtaking, stunning, captivating, mesmerizing, awe-inspiring, masterfully, meticulously, exquisitely, beautifully crafted, cinematic masterpiece, visual feast, a symphony of, seamlessly, effortlessly, flawlessly, cutting-edge, state-of-the-art, next-level, rich tapestry, vibrant tapestry, kaleidoscope of, elevate, unlock, unleash, harness, groundbreaking, a testament to, speaks volumes, resonates deeply`.
- Chinese: `令人叹为观止, 令人惊叹, 令人着迷, 精心打造, 匠心独运, 独具匠心, 视觉盛宴, 光影交响, 完美呈现, 极致体验, 引人入胜, 震撼人心, 巧妙融合`.

Also banned for pacing (Seedance often literalizes these into actual slow motion): `slow, gentle, soft, slow motion`. Use `smooth, steady, fluid, natural realtime` instead. This is documented in `social-video-short.md` and the 2026-05-17 lesson.

## Camera vocabulary cheat sheet

- **Angles**: low-angle / 仰拍, high-angle / 俯拍, dutch / 荷兰角, bird's-eye / 鸟瞰, worm's-eye / 蚁视角, eye-level / 平视, over-the-shoulder / 过肩镜头.
- **Focal length**: wide 14-24mm / 广角, standard 35-50mm / 标准, telephoto 85-200mm / 长焦, macro / 微距.
- **Movement**: tracking / 跟拍, dolly-in / 推镜头, dolly-out / 拉镜头, crane / 摇臂升降, pan / 横摇, tilt / 纵摇, whip-pan / 甩镜头, orbit / 环绕, push-in / 推进, pull-back / 后拉, handheld / 手持摄影, Steadicam / 斯坦尼康, aerial / 航拍.
- **Time**: slow-motion / 升格, speed ramp / 变速, freeze frame / 定格.
- **Transitions**: smash cut / 硬切, match cut / 匹配剪辑, whip-pan transition / 甩镜转场, hard cut / 直切, L-cut / L型剪辑.

## Language rules

- Present tense, active voice.
- Vivid but economical. Concrete visual direction beats poetic padding.
- Consistent character names. Unnamed -> functional labels (`the figure` / `身影`).
- No dialogue or subtitles unless the user explicitly requests them.
- Default to in medias res - scene already in progress - unless the user says `starts with...` or `ends with...`.
- No metadata headers in the final prompt. Weave transitions into prose.

## Worked example — immersive prompt

A high-quality immersive prompt for a stylized, dense, dialogue-bearing shot. It hits every anchor: era / medium up front, embodied character, environment with material, camera-as-actor, inline dialogue, image artifacts, density statement, mood-summary closer.

> A late-1970s / early-1980s carnival horror scene, shot on 35mm film with practical effects and transferred to worn analog tape. The visual style is entirely pre-digital — every clown a costumed performer or animatronic puppet, every set a physical built funhouse interior. A lone man fights through a horde of grinning carnival clowns inside a tilting funhouse. He is in his mid-thirties with short brown hair styled back from a slightly high hairline, a full but neatly trimmed auburn-brown beard with a connected mustache, blue-green eyes, fair skin with a naturally ruddy flush on the cheeks, a strong brow, and a medium athletic build. Confetti is stuck to his sweat-damp hair and beard, a smear of red and white greasepaint streaks his neck where a clown grabbed him, his forearm dusted with talc. He wears a plain heather grey crew-neck t-shirt with smears of pastel paint across the chest, dark blue jeans flecked with glitter, and plain sneakers slipping slightly on the painted floor. The funhouse interior is a tilting plywood maze of distorted mirror panels reflecting fragmented bodies, painted cutouts of leering faces and giant grinning mouths, a spinning barrel doorway at one end, strings of bare incandescent bulbs flickering in candy colors, painted floorboards angled at false perspectives. The clowns are surreal in color — chalk-white painted faces with cracked greasepaint, oversized red rubber noses, ruffled collars in lemon-yellow and acid-mint, eyes ringed in candy-pink and electric-violet, mouths frozen in too-wide grins of yellowed rubber teeth, hair in candy pinks and acid greens sticking out at hard angles. They are a mix of costumed performers and animatronic puppets popping out from behind cutouts, their movement deliberately jerky and mechanical, joints visibly hinged. He swings a wooden carnival mallet, the head connecting with rubber faces and animatronic chests with hollow thuds, sending one clown's wig flying. Wiping greasepaint off his cheek with his shoulder, he turns to camera and says casually, "Don't forget to like and subscribe." The frame is dense with grinning faces crowding from every angle, mirror reflections multiplying the bodies, bulb strings hanging into the shot, almost no negative space. The camera is handheld and tight, lurching with each swing, briefly losing focus as a clown's face presses against the lens. Knocking a puppet back through a cutout, he adds with a small smirk, "Let me know in the comments if you hate clowns." Lighting is harsh and bright — overexposed studio fill with candy-colored gels from the bulb strings (hot pink, acid green, lemon yellow) washing across the painted walls. Image quality shows heavy analog artifacts: visible film grain, color bleed between pink and green, chromatic aberration on the mirror edges, gate weave, and soft focus falloff. Highlights bloom unevenly on painted faces, the bulb strings, and his sweat-slick brow. Overall feeling: garish, disorienting, and crowded — a carnival horror grounded in animatronics, greasepaint, and dense, popping motion.

### Anti-pattern — what to avoid

The same scene written generically:

> A man fights clowns in a funhouse. He swings a mallet. The camera is handheld. Style is retro. Vibe is scary.

The first prompt is roughly 8x longer and over 20x more useful to the engine because every clause specifies sensory, material, or camera information the engine can render. The second forces the engine to guess and produces stock output.

### Adapt the pattern to other media

The era / medium anchor pattern transfers cleanly across aesthetics:

- **Modern shonen anime fight.** `Cel-animated theatrical shonen anime production, late-2020s broadcast print at peak intensity. [character with embodied state — knuckles cracking, hair lashing in the wind, sweat catching the dawn light]. [environment with material]. [camera as actor — pushes in fast then orbits ninety degrees around the standoff, briefly catches a lens flare on the kanabō]. [anime artifacts — sharp white speed lines radiating from frame edges, smear-frames on impact, chromatic dispersion on the Haki shockwave, ink-bleed lineart]. [density statement]. [mood closer].`
- **Documentary archive footage.** `Captured on hand-cranked Bolex 16mm in 1964 and later scanned from a faded reel. [character with embodied state]. [...] [artifacts — visible splice cuts, vinegar-syndrome color shift toward magenta, frame skip, slight vertical flicker]. [...].`
- **VHS family video.** `Shot on Hi8 home camcorder in 1992, transferred and copied across multiple VHS tapes. [...] [artifacts — chroma smearing, head-switching noise at the bottom of frame, motion lag on quick pans, timestamp overlay top-right]. [...].`
