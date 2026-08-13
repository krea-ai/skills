---
name: seedance-2-examples
description: Searchable concrete prompt examples for the Seedance video family (Seedance 2.5, 2.0, Fast, Mini). Load only the section matching the active workflow.
---

# Seedance Examples

Use only after reading `seedance-2.md`. Search by heading and read the smallest matching section:

```bash
rg -n "^##|^###" seedance-2-examples.md
```

Examples are adapted prompt cards, not API payloads. Apply live Krea schema fields for references, duration, aspect, resolution, audio, and start/end frames.

## Official-Style Core Examples

### Multimodal Reference

Use when different assets each supply one role.

```text
References:
Use the woman with short black hair and red raincoat in @Image1 as Hero_A.
Use @Image2 only as the rain-soaked alley scene reference.
Reference the slow lateral tracking camera movement in @Video1.
Use @Audio1 only for low rainy ambience and distant traffic.

Shot 1: Smooth lateral tracking medium shot. Hero_A walks through the alley,
holding a paper lantern close to her chest. Neon signs reflect in puddles.
Her pace is slow and steady; the lantern swings slightly with each step.

Shot 2: Camera cuts to a close-up. Hero_A stops under an awning, lowers her
head slightly, and exhales. Raindrops slide down the lantern frame.

Style: cinematic night rain, cool blue-magenta palette, soft reflected light.
Constraints: keep Hero_A's face, coat, and proportions stable; no subtitles,
no logo, no watermark.
```

### Subject Definition

Use when one asset contains multiple subjects.

```text
Define the boy in @Image1 wearing the yellow hoodie and round glasses as
Boy_A. Define the small white dog with the blue collar in @Image1 as Dog_B.

Generate a warm living-room scene where Boy_A kneels beside Dog_B and gently
clips the blue collar into place. Keep Boy_A and Dog_B visually distinct and
do not duplicate either subject.
```

### Shot Storyboard

Use for complex story clips. Prefer shot numbers over exact time ranges.

```text
Global style: high-definition cinematic documentary, soft natural colors,
warm interior light, stable faces and natural motion.

Shot 1: Fixed medium shot of a young chef standing at a small restaurant
counter before opening. She wipes the counter twice with her right hand,
then pauses and looks toward the front door. Quiet kitchen ambience.

Shot 2: Cut to a close-up of her hands setting three ceramic bowls in a row.
She adjusts the middle bowl slightly, takes a slow breath, and smiles with
nervous anticipation.

Shot 3: Smooth pullback to a wider view as the front door opens and morning
light enters the room. She straightens her shoulders and says {Welcome in}.

Constraints: one camera movement per shot; no subtitles unless requested;
no logo, no watermark, no flicker, no duplicate people.
```

### Dialogue Short Drama

Use for a single-scene dialogue/emotion progression.

```text
References:
Use @Image1 as the main character's face and clothing reference.
Use @Image2 as the small dorm room environment reference.
Use @Audio1 as soft indoor ambience.

Shot 1: Medium follow shot. The main character walks to the dorm-room door
at dusk, clutching a notebook with both hands. She slows at the threshold,
inhales, and glances down.

Shot 2: Cut inside the dorm room. Two roommates look up from their desks.
One roommate smiles and asks {How did the exam go?}. The camera stays in a
gentle medium shot with warm window light.

Shot 3: Close-up on the main character. Her shoulders drop, then she looks
up, breaks into a small grin, and says {I passed}. Room ambience rises into
soft laughter.

Constraints: keep faces and body proportions stable; dialogue language is
consistent; no subtitles unless requested.
```

### Wuxia Confrontation

Use for action/atmosphere-focused scenes with references.

```text
References:
Use the red-robed swordswoman in @Image1 as Fighter_Red.
Use the black-clad swordswoman in @Image2 as Fighter_Black.
Use @Image3 as the cliff and bamboo forest environment.
Reference @Video1 for restrained martial-arts camera rhythm.
Use @Audio1 for sparse drum hits and wind.

Shot 1: Side medium shot. Fighter_Red stands near the cliff edge and slowly
raises a flask with her right hand. Wind moves her sleeves and robe hem.
The camera makes one slow half-circle move, revealing Fighter_Black as a
dark shape in the bamboo.

Shot 2: Cut to a high wide shot overlooking the cliff and forest. The two
fighters stand far apart. Wind lifts dust and robe hems; the drum rhythm
becomes tighter.

Shot 3: Ground-level close shot. Both fighters draw swords slowly. Fighter_Red
shifts from careless calm to cold focus; Fighter_Black steadies her blade.
The camera tracks them as they circle, ending on the moment before impact.

Style: misty rain wuxia, cool low-saturation palette, film grain, layered
light and shadow. Constraints: natural continuous motion, no clipping, no
stutter, stable faces and proportions.
```

## Reference Control Examples

### Multi-Subject Reference

```text
Use the orange cat from @Image1 as Cat_A and the tan dog from @Image2 as
Dog_B. In a cozy apartment, Dog_B lies on the floor eating from a bowl.
Cat_A approaches from frame left, gently taps Dog_B's shoulder with one paw,
then curls up beside Dog_B. Warm afternoon light, calm domestic tone.
Preserve both animals' colors, proportions, and identities.
```

### Multi-Element Reference

```text
Use @Image1 for the barista's face and hairstyle.
Use @Image2 for the green apron outfit.
Use @Image3 for the customer character.
Use @Image4 for the cafe interior.
Use @Image5 for the small logo placement only.

Generate a cafe counter scene. The barista arranges cups on the counter,
the customer approaches and asks a question, and the small logo remains in
the lower-right corner. Preserve asset roles; do not blend the subjects.
```

### Video Motion Reference

```text
Reference the running gait and leg rhythm from @Video1.
Generate a golden horse running across a wide grassland at sunrise. The
horse's movement should follow the same stride cadence and body mechanics,
then settle into a proud still pose as the camera pulls back.
```

### Camera Motion Reference

```text
Reference only the camera movement from @Video1: a smooth push-in that
begins wide, lowers slightly, and ends in a close-up.

Generate a scene of a glass perfume bottle on wet black stone. The camera
movement follows @Video1, while the subject, lighting, and environment come
from this prompt.
```

### Special Effects Reference

```text
Reference the wing-formation effect from @Video1: the exact growth path,
particle direction, and timing of the light trails.

Apply that effect to the girl in @Image1. Keep her face, outfit, pose, and
body proportions stable while the luminous wings form behind her.
```

## Video Edit Examples

### Object Removal

```text
Strictly edit @Video1. Remove everything on the desk except office supplies.
Keep the desk, camera movement, lighting, background, hands, and all remaining
objects unchanged. Reconstruct occluded desk areas naturally.
```

### Replace Product

```text
Strictly edit @Video1. Replace only the perfume bottle in the original video
with the face cream jar from @Image1.

Preserve all original motions, hand positions, camera work, background,
lighting, reflections, and pacing. Do not change anything except the product.
```

### Add Element

```text
Strictly edit @Video1. At the moment the person opens the notebook, add a
small glowing blue paper crane on the right side of the desk.

The crane should appear already folded, cast a soft blue reflection on the
desk, and stay still. Keep all original people, camera movement, lighting,
and background unchanged.
```

### Video Extension

```text
Extend @Video1 forward.

After the original clip, the two late friends run into frame from the street,
slow down, and greet the waiting group. The five people gather in a loose
circle and begin chatting naturally. Preserve the original scene lighting,
camera height, clothing, and friendly tone.
```

### Backward Extension

```text
Extend @Video1 backward.

Before the original clip begins, create an over-the-shoulder shot of the man
in the hoodie standing near the window. He turns slightly toward the other
person and says {It's not that bad. You're just exhausted. Let's take it one
step at a time}. Then transition naturally into the first frame of @Video1.
```

### Track Completion

```text
Connect @Video1 to @Video2.

At the end of @Video1, a leaf lands on the ground and releases a brief swirl
of golden particles. A gust of wind carries those particles across frame,
creating the transition into @Video2. Preserve visual continuity and make
the transition feel motivated by the wind.
```

## Text And Audio Examples

### Text Generation

```text
Hand-drawn comic style. Three friends sit around a table sharing crispy
fried chicken, laughing and passing plates.

The frame gradually softens, then three words appear one after another in
the center: "Bite", "Laugh", "Share". Use playful rounded lettering, warm
yellow color, and a gentle pop-in entrance. No other text.
```

### Subtitles

```text
I2V: A mountain landscape transitions from a wide starry night to pale dawn.
Voiceover: a calm deep male voice says {In the quiet before sunrise, every
path begins again}.

Text Integration: render the narration as subtitles at bottom-center.
Subtitles should synchronize with the voice pacing and remain readable.
```

### Speech Bubble

```text
In a sunlit apple orchard, the girl picks a red apple, takes one bite, smiles,
and says {This is the real deal}.

A speech bubble appears beside her containing exactly: "This is the real deal".
Keep the bubble clean, rounded, and readable.
```

### Voice Timbre

```text
Use the low, warm, slightly grainy middle-aged male voice from @Audio1 for
the narrator.

The narrator says {The old station wakes before the city does}. Keep the
delivery calm, measured, and close to the microphone, with soft room tone.
```

## Production-Format Examples

These examples use production-style formatting for creator and commercial workflows. Do not let them override the main rules about reference roles, shot order, one camera move per shot, or avoiding strict timing over-control.

### Transformation Arc

```text
Format: transformation comedy-horror, 5 shots.
References: @Image1 is the relaxed hero, @Image2 is the truck, @Image3 is
the underpass location, @Image4 is the approaching creature.

Shot 1: Medium shot. The hero sits on the truck hood eating noodles calmly
under the dusk overpass. Camera has a slight handheld sway.

Shot 2: Wide shot. The creature runs from the river channel toward the truck.
Camera tracks the threat with controlled shake.

Shot 3: Close-up. The hero notices the creature, pauses mid-bite, and looks
annoyed rather than afraid.

Shot 4: Medium low angle. The hero transforms into a huge pale creature,
limbs stretching and jaw opening, while the truck stays fixed behind her.

Shot 5: Wide shot. The creature is defeated; the hero returns to normal,
sits back on the hood, and resumes eating as if nothing happened.

Constraints: transformation arc calm -> threat -> transformation -> aftermath;
faces and body proportions stable before/after transformation; no subtitles,
no logo, no watermark.
```

### Product Commercial

```text
Format: premium product video, 4 strongly staged beats.
Reference: @Image1 is the hero product. Preserve product shape, label text,
cap, materials, and proportions exactly.

Shot 1: Macro close-up. Condensation beads slide down the product surface.
Camera makes one slow push-in; cold studio light catches the label.

Shot 2: Medium product shot. A splash of clear water arcs behind the product,
never covering the label. Camera stays fixed.

Shot 3: Extreme macro. Light travels across the cap texture and printed logo.
The product remains still and sharp.

Shot 4: Hero close-up. Camera settles on the full product centered against a
clean premium background. Subtle audio hit, no voiceover.

Constraints: no extra text, no subtitles, no label warping, no added logos,
product locked exactly as @Image1.
```

### Stylized Animation

```text
@Image1 is the first keyframe and style reference.
Style: cinematic stylized 3D animation with realistic desert environment,
high-detail particle physics, and expressive character motion.

Shot 1: Wide shot from @Image1. The small hero sprints across red desert
sand toward a huge glowing entity. Dust lifts around her feet.

Shot 2: The entity strikes downward with one tentacle. The hero slides under
it; the impact throws a ring of dust and debris outward.

Shot 3: Medium shot. The hero touches the glowing surface, recoils, and sees
rainbow energy flickering around her hand.

Shot 4: Wide shot. She uses the energy to redirect the entity's own force.
Dust and colored particles swirl, then settle into a calm final frame.

Constraints: preserve the style and hero design from @Image1; motion remains
continuous, no flicker, no subtitles.
```

## Retake Examples

### Unwanted Subtitles

```text
Retake: keep the same scene, camera, actions, lighting, and audio. Remove all
generated subtitles and on-screen text. Keep it subtitle-free; avoid generating
any text, captions, logos, or watermarks.
```

### Duplicate Character

```text
Retake: keep only one instance of each referenced character in the same frame.
Do not create duplicates, twins, mirrored copies, or extra avatars. Preserve
the original character identities and simplify the action.
```

### Style Drift

```text
Retake: preserve the same shots and actions, but lock the video to 3D Chinese
animation CG xianxia style. Do not drift into live-action realism. Keep cool
misty lighting, stylized robes, and animation-style faces.
```

### Motion Instability

```text
Retake: simplify the movement. Use one smooth lateral tracking camera move
only. The subject walks slowly, turns her head slightly, and stops. No running,
jumping, spinning camera, stutter, flicker, or clipping.
```

### Special Effect Miss

```text
Retake: reference @Video1 only for the countdown effect's motion logic and
appearance timing. Recreate that effect form exactly, while preserving the
new scene, subject, camera angle, and background from the current prompt.
```
