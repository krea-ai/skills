# Generic Short Video

## Trigger

User asks for a simple generated clip, text-to-video, ambient motion, nature/product-neutral scene, abstract motion, or short video that is not a paid-social ad and not a professional animation sequence.

Route away from this workflow when:

- The brief mentions product, ad, UGC, campaign, social creative, CTA, marketplace, or Meta Ads -> `../../krea-marketing/SKILL.md`.
- The brief needs characters across shots, storyboard approval, shotlists, or retakes -> `../../krea-animation/SKILL.md`.

## Clarify

Ask once only when missing:

- **Duration**: usually 4-8s, sometimes going up to 15s.
- **Aspect**: 16:9, 9:16, 1:1, or source aspect.
- **Motion**: camera move, subject action, atmosphere.
- **Audio**: none unless the model supports and user requests it.

## Recipe

1. Run `../references/cost-preflight.md`; video is expensive and async.
2. Resolve the video model from live `list_models`: default Seedance-2-fast for generic video; use Seedance-2 for high-end video requests.
3. Inspect schema for duration, aspect, resolution, audio, and reference fields.
4. If the prompt includes local/non-Krea references, upload them first.
5. Prompt visible motion, camera, subject, atmosphere, and timing. Keep it one coherent clip.
6. Submit one async job.
7. Poll with `../references/progress-reporting.md`.
8. Download or surface the result URL. Sample frames when local media is available and check the visible action matches the brief.

### MCP path

Use the available Krea MCP tools to upload local references, list models, inspect the selected model schema, then call video generation with schema-verified prompt, reference, duration, aspect, resolution, and audio fields.

## Banned

- Do not use this for UGC/social ads; route to `krea-marketing`.
- Do not use this for long-form/narrative/character continuity; route to `krea-animation` or ask whether to simplify to one clip.
- Do not silently poll.
- Do not promise exact identity or product fidelity from a text-only video prompt.

## On Failure

| Symptom | Cause | Fix |
|---|---|---|
| Output feels like an ad | Marketing language leaked in | Route to `krea-marketing` and build a campaign brief |
| Multiple cuts needed | Workflow too simple | Route to `krea-animation` or ask whether to simplify to one clip |
| Motion is too slow or static | Prompt lacked specific action | Add concrete motion, direction, and timing |
| Job times out | Video queue or sync timeout cap | Poll manually and report progress |
