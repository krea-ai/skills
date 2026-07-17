---
name: seedance-2-prompting
description: Prompting playbook for Seedance 2.0 / Seedance 2 Fast video models, focused on multimodal references, shot sequencing, action/camera control, audio/text, video editing, extension, and Krea operating rules.
---

# Seedance 2.0 Prompting Guide

Load this file only after the selected model is Seedance 2.0, Seedance 2 Fast, `bytedance/seedance-2`, or a closely related Seedance video model.

Use the rules in this file as the controlling guidance for Seedance 2.0 prompting. Example patterns in the appendix are optional support material and should not override the main rules.

Always verify the live Krea model schema before submitting. Use only fields exposed by the selected model. Prompt examples describe intent; schema controls such as duration, aspect, resolution, references, audio, `start_image`, `end_image`, and reference arrays must come from the live schema.

## Examples Appendix

For concrete prompt examples, search `seedance-2-examples.md` by heading and read only the matching section:

```bash
rg -n "^##|^###" seedance-2-examples.md
rg -n "Multimodal Reference|Video Editing|Shot Storyboard" seedance-2-examples.md
```

Do not load the full examples appendix unless the relevant section cannot be identified.

## When To Load Examples

| Task | Search terms |
|---|---|
| image/video/audio references | `Multimodal Reference|Asset Role` |
| subject identity from references | `Subject Definition|Multi-Subject Reference` |
| multi-shot story or drama | `Shot Storyboard|Dialogue Short Drama` |
| action/fight/chase | `Action Scene|Wuxia Confrontation|Transformation Arc` |
| video edit, add/remove/replace | `Video Editing|Object Removal|Replace Product` |
| video extension or track connection | `Video Extension|Track Completion` |
| text, subtitles, speech bubbles | `Text Generation|Subtitles|Speech Bubble` |
| video/camera/effects reference | `Video Motion Reference|Special Effects Reference` |
| voice, dialogue, audio reference | `Voice Timbre|Dialogue Audio` |
| product ad or commercial | `Product Commercial` |
| stylized animation | `Stylized Animation` |
| failure/retake | `Retake Examples|Troubleshooting` |

## Core Formula

Seedance is a multimodal video model that uses text, images, video, and audio together. Write prompts as engineering-style shot instructions, not copywriting.

Advanced formula:

```text
precise subject + action details + scene/environment + lighting/color tone
+ camera movement + visual style + image quality + constraints
```

For complex videos, use a storyboard:

```text
References: <asset roles>
Global style: <visual tone, quality, constraints>
Shot 1: <camera/transition> + <subject action/expression> + <position/space> + <audio>
Shot 2: <camera/transition> + <subject action/expression> + <position/space> + <audio>
Constraints: <identity, motion stability, no subtitles/logos/watermarks, style locks>
```

## Reference Roles

Name what each asset contributes. Do not assume the model knows why an asset was uploaded.

| Asset role | Prompt pattern |
|---|---|
| Image subject | `Use the <2-3 stable traits> in @Image1 as <Subject_A>.` |
| Image scene/style | `Use @Image2 as the scene/style reference, not as a subject.` |
| Video action | `Reference the <action/motion> in @Video1.` |
| Video camera | `Reference the <camera movement/shot language> in @Video1.` |
| Video effects | `Reference the <effect form and motion logic> in @Video1.` |
| Audio timbre | `Use the <voice traits> timbre from @Audio1 for <speaker>.` |
| Audio rhythm | `Use @Audio1 for background rhythm / atmosphere.` |

Subject definitions should be concise and stable: 2-3 clear visual traits, no contradictions. If an asset has multiple people/props, label the intended subject explicitly. Even when using Krea asset IDs, prompt with `@ImageN`, `@VideoN`, or `@AudioN` labels because those are what the model understands in the prompt.

Recommended asset strategy: use the fewest assets that carry the job, usually 4-5 total: 1-2 character images, 1 scene image, 1 camera/action video, and 1 audio clip. Too many assets can confuse priority, blur subject identification, and cause style conflicts.

## Task Formulas

### Multimodal Reference

Use when extracting subject, style, scene, action, camera movement, sound effect, or voice from references to make a new video.

```text
Reference <dimension> from @ImageN/@VideoN/@AudioN to generate <new scene>.
Keep <specific traits> consistent. Change <new action/environment/story>.
```

### Video Editing

Use when modifying an existing video. Parts not mentioned should remain unchanged.

```text
Strictly edit @Video1. Change only <target>.
Add: <element features> + <timing> + <location>.
Remove: <element>, keeping all other video content unchanged.
Replace: <old element> with <new element/reference>, preserving motion and camera work.
```

### Video Extension

Use when continuing or prepending a single coherent scene.

```text
Extend @Video1 forward/backward: <what happens before/after>.
Preserve continuity of <characters, lighting, camera, action path, audio tone>.
```

Extension is best for single-scene dialogue, emotional progression, or movement along one path. Use segmented stitching for plot turns, chases, fights, montages, or complex action.

### Track Completion / Stitching

Use when connecting multiple input clips:

```text
@Video1 + <transition description> + @Video2 + <transition description> + @Video3.
```

Respect the live schema. Official guidance notes a maximum of 3 input video clips and total input video duration not exceeding 15 seconds for track-completion style inputs.

## Shot Sequencing

Prefer `Shot 1`, `Shot 2`, `Shot 3` over strict second-by-second timing. Precise timing such as `0-3s` can be unstable. Use time ranges only as editorial staging when a workflow specifically requires them; do not expect frame-accurate timing.

Each shot should include:

1. camera movement or transition
2. subject action and expression
3. position or spatial relationship
4. audio, dialogue, ambience, or sound effect

For multi-shot creator-format prompts, put shot count, total duration, and aspect ratio near the top as metadata. Keep this as metadata, not a substitute for shot details.

## Action And Camera Rules

Actions need body-part specificity, degree, speed, force, and continuity:

- `she slowly raises her right hand`
- `he turns his head quickly toward the doorway`
- `the runner pushes hard off the wet pavement`
- `shoulders relax, breath releases, faint smile appears`

Prefer slow, gentle, coherent small movements for stability. Avoid stacking high-burst actions unless you split them into separate shots or clips.

Camera rules:

- Use standard terms: medium shot, close-up, wide shot, fixed shot, slow push-in, smooth lateral track.
- Specify only one primary camera movement per shot.
- Do not ask for push, pull, pan, orbit, and crane in the same shot.
- For action that travels, name direction, distance, start/end pose, and frame position.

## Text, Dialogue, And Audio

Seedance can generate common text such as slogans, subtitles, and speech bubbles. Use simple/common characters and avoid rare symbols unless needed.

Text prompt pattern:

```text
<Text content> + <timing> + <position> + <entrance/appearance> + <visual attributes>
```

Dialogue language should be consistent; avoid mixing languages except for proper nouns.

Special symbol conventions:

| Information type | Symbol style |
|---|---|
| Music | `(fast-paced drums in the background)` |
| Sound effect | `<dog barking in the distance>` |
| Dialogue | `{Hello, world}` |
| Dialogue in less common language | `says in Japanese {こんにちは}` |
| Subtitle text | `〖Chapter One: Departure〗` |

Voice matching improves when you describe voice traits, such as age, thickness, warmth, grain, pace, and emotion, rather than only saying "use @Audio1."

## Krea Operating Rules

These are Krea-specific rules for `bytedance/seedance-2`; live schema still wins.

- `@Image1` / `@Video1` / `@Audio1` are prompt labels. Also pass assets through the schema-confirmed fields.
- In Krea, `end_image` and `reference_images` are mutually exclusive for Seedance-2.
- Chained/destination shots use `start_image` + `end_image`, omitting `reference_images`.
- Terminal/detail-anchored shots use `start_image` + `reference_images`, omitting `end_image`.
- `end_image` is a visual destination, not a loose style reference. Keep it within plausible story-time from the start frame.
- Seedance-2 has a 4 second minimum duration. For shorter editorial cuts, generate 4s and trim if useful motion lands early.
- For in-scene continuity, extract the prior clip's actual last frame and use it as the next `start_image`.
- Treat completed jobs with no result URL as failure/refusal, not success.
- Submit video jobs in waves of 12 or fewer to avoid practical workspace concurrency limits.

Krea live test supplement: one-shot commercial timelines usually land about 3 strong beats reliably. More beats need full staging, short beats, and a constraints tail; unstaged "hard cuts" can morph instead of cutting.

## Constraints And Troubleshooting

Add constraints at the tail, especially for longer prompts:

- `keep it subtitle-free`
- `avoid generating any text or subtitles`
- `do not generate a logo`
- `do not generate a watermark`
- `faces and body proportions remain stable`
- `motion is continuous and natural, no stutter, no flicker, no clipping`
- `do not duplicate characters or create twin avatars`

Known fixes:

| Symptom | Fix |
|---|---|
| Unwanted subtitles | Add subtitle-free constraints, remove text from references, prefer landscape if feasible |
| Logo/watermark appears | Add explicit no-logo / no-watermark constraints |
| Style drifts to realism | State the target style; if needed, convert references to the target style before video generation |
| Extension join jumps | Repair in post by aligning keyframes; trim a few frames at joins when needed |
| Duplicate/twin character appears | Use single-person refs, simplify prompt, add anti-duplicate constraint |
| Extension quality degrades | Limit stacked continuations, use high-definition refs, consider a white-model intermediate for long continuation workflows |
| Special effect is wrong | Use a reference video that shows the effect form and motion logic |
| Voice match is weak | Describe voice traits explicitly in addition to attaching @Audio |
| Motion is unstable | Reduce action intensity, use one camera move, break action into shots |
