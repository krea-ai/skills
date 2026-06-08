# Production Pipeline

Use this reference when deciding what artifact must exist next.

## Studio Spine

Professional animation production is a gated pipeline:

1. Planning: premise, audience, tone, schedule, budget, delivery format.
2. Script and beat sheet: story, dialogue, emotional turn, runtime target.
3. E-konte / storyboard: shot-by-shot visual plan with timing and camera notes.
4. Layout: camera, staging, background perspective, character placement.
5. Genga / key animation: main poses and movement extremes.
6. Douga / in-betweening: transition drawings between key poses.
7. Shiage / color: character paint, palettes, consistency.
8. Backgrounds: location plates, lighting, perspective, atmosphere.
9. Satsuei / compositing: layers, effects, camera moves, final photographed image.
10. Rush check: review shots in motion, identify retakes.
11. Edit and audio: assemble, timing, music, foley, dialogue, subtitles.
12. Retake and delivery: fix only failed shots, archive manifests.

Sources that shaped the workflow:

- Toei Animation production overview: <https://corp.toei-anim.co.jp/en/company/animation_production/animation_production-2.html>
- Kyoto Animation business overview: <https://www.kyotoanimation.co.jp/company/business/>
- Kyoto Animation animator curriculum: <https://www.kyotoanimation.co.jp/school/curriculum/animator-curriculum.pdf>
- Disney Animation layout process: <https://www.disneyanimation.com/process/layout/>
- Pixar pipeline education site: <https://sciencebehindpixar.org/explore>
- AJA production assistant manual summary: <https://gigazine.net/gsc_news/en/20200813-anime-production-assistant-manual/>

## AI Mapping

AI can replace or accelerate media creation, but it should not remove the gates:

| Traditional artifact | AI-assisted equivalent |
|---|---|
| model sheet | GPT Image 2 / Krea 2 generated turnaround, expression, hand, mouth, color sheets |
| layout | approved keyframe, background plate, camera note |
| genga | start/end keyframes and timing beats |
| douga | video model interpolation from start/end/reference frames |
| shiage | prompt and style bible enforcing palette and line rules |
| satsuei | generated video clip plus edit normalization/compositing |
| rush check | sampled frame review and retake log |

## Rule Of Replacement

Only replace a traditional stage when the adjacent stage can still review it. Example: Seedance may replace manual in-betweening for a shot, but the shot still needs approved keyframes before generation and a rush check after generation.

## Terms

- `e-konte`: Japanese storyboard with shot timing and camera/action notes.
- `layout`: staging drawing that locks composition, background perspective, camera, and character placement.
- `genga`: key animation drawings or poses.
- `douga`: in-between animation drawings.
- `shiage`: paint/color finishing.
- `satsuei`: compositing/photography.
- `rush check`: review of completed cuts before final approval.
- `retake`: a requested correction to a shot or production artifact.
