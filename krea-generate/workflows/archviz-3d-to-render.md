# Archviz 3D To Render

## Trigger

User asks to turn a SketchUp, Rhino, Revit, Blender, CAD, clay, viewport, or 3D screenshot into a photoreal architectural render, interior render, facade study, material variant, or time-of-day render. When in doubt between this workflow and generic image edit, pick this if preserving architectural structure is the main requirement.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Scene type**: exterior, interior, facade, urban, landscape, detail.
- **Target mood**: golden hour, overcast, midday, twilight, night, editorial.
- **Materials**: preserve, change, or specify important surfaces.
- **Output**: draft, client presentation, final hero, print.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read the 3D screenshot with vision and identify camera angle, scene type, massing, openings, visible materials, and missing context.
2. Default to `google/nano-banana-pro` at 4K for archviz renders. Confirm that named model exists in the live catalog, then inspect its schema. Consider alternatives only if this default is unavailable or the schema cannot accept the source image and target size.
3. Keep `openai/gpt-image-2` at 4K as the premium backup for particularly complex options, or requests that also need substantial text overlay. It is potentially better, but slower and more expensive; name that tradeoff before using it.
4. Inspect schema for the exact source image field, aspect, 4K size/resolution, strength/preservation controls, and optional prompt/style fields. Do not copy field names from memory or stale examples.
5. Upload the screenshot to Krea; use a source at least 1024px on the long side when possible.
6. Prompt structure: preserve exact camera, massing, window/door rhythm, proportions, and perspective; then specify scene type, target realism, time of day, lighting, material details, atmosphere, permitted additions, and camera/lens.
7. Generate one structural render first; do not batch variants until the model preserves the architecture.
8. Read output with vision; verify massing, openings, material intent, perspective, and camera against the source.
9. If structure drifts, retry once with lower edit/creativity strength if available, stronger preservation language, or the premium backup when appropriate.
10. **Deliver** with one-line summary and suggested next variants only if useful.

### Tool path

Use the available Krea tools to upload local references when needed, verify the named default model, inspect its schema, then call image generation with schema-verified reference and aspect/size fields. Do not copy field names from memory.

## Banned

- Do not treat architectural screenshots as generic inspiration; preserve structure.
- Do not change massing, window rhythm, or camera unless asked.
- Do not create 6 variants before the first structural pass is accepted.
- Do not route product or marketing images here.

## Cost & time

- Per-job: draft 1K is moderate; 2K/4K final renders are higher CU and 1-4 minutes.
- Typical full workflow: 1 structural pass plus 2-4 mood/material variants.
- Hard caps the user should know about: exact CAD fidelity is not guaranteed.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Massing changed | Prompt too generative | Emphasize exact structure and lower edit strength |
| Materials wrong | Vague descriptors | Use concrete material language |
| Render too stylized | Wrong archetype | Re-route to photoreal high-fidelity image |
| Reference ignored | Source too small or wrong schema | Upload larger source and verify image input field |
