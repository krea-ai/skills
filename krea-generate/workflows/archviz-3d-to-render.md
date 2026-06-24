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

1. Read the 3D screenshot with vision and identify camera angle, scene type, visible materials, and missing context.
2. Resolve `image-to-image / face reference` or `high-fidelity image` with structural reference support from live `list_models`.
3. Inspect schema for image input, aspect, resolution, and strength controls.
4. Cost-preflight for 4K, batches, or >100 CU.
5. Upload the screenshot to Krea; use a source at least 1024px on the long side when possible.
6. Prompt structure: scene type, target style, time of day, lighting, material details, atmosphere, additions, camera.
7. Generate one render first; do not batch variants until structure preservation works.
8. Read output with vision; verify massing, openings, materials, and camera.
9. **Deliver** with one-line summary and suggested next variant only if useful.

### MCP path

Use the available Krea MCP tools to upload local references, list models, inspect the selected model schema, then call image generation with schema-verified reference and aspect fields. Do not copy field names from memory.

## Banned

- Do not treat architectural screenshots as generic inspiration; preserve structure.
- Do not change massing, window rhythm, or camera unless asked.
- Do not create 6 variants before the first structural pass is accepted.
- Do not route product or marketing images here.

## Cost & time

- Per-job: draft 1K is moderate; 2K/4K final renders are higher CU and 1-4 minutes.
- Typical full workflow: 1 structural pass plus 2-4 mood/material variants.
- Hard caps the user should know about: exact CAD fidelity is not guaranteed; use vision QA.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Massing changed | Prompt too generative | Emphasize exact structure and lower edit strength |
| Materials wrong | Vague descriptors | Use concrete material language |
| Render too stylized | Wrong archetype | Re-route to photoreal high-fidelity image |
| Reference ignored | Source too small or wrong schema | Upload larger source and verify image input field |
