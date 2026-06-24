# Image

## Trigger

User asks for image generation with references, image editing, restyling, a final/high-quality asset, multiple options, or preservation constraints. For a simple no-reference image draft, use the Quick Image Shortcut in `../SKILL.md` instead of loading this workflow.

## Route

| Request | Mode |
|---|---|
| Loose concept, options, or exploration | Fast draft |
| Final, hero, production-quality, client-ready, detailed brief, or references | High fidelity |
| "Edit this", "turn this into", "restyle", background/object change, or source image preservation | Image-to-image |
| Poster, flyer, signage, packaging copy, or readable typography | Use `image-text-poster.md` |
| Repeatable identity/style across many outputs | Use `lora-train-and-use.md` |

## Clarify

Ask once, in a single batched message, only for missing details that block a useful result. Skip anything the user already gave.

- **Goal**: draft, final render, edit, restyle, or options.
- **Subject and use**: what the image is for.
- **Aspect and resolution**: 1:1, 4:5, 16:9, 9:16; 1K, 2K, or 4K.
- **References and preservation**: product, face, pose, layout, colors, text, or non-negotiables.
- **Edit strength**: subtle edit, balanced transformation, or full restyle.

If the brief is complete, skip Clarify and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read every attached/source/reference image with vision before routing.
2. If the run is >100 CU, 4K, a premium batch, or otherwise expensive, run `../references/cost-preflight.md`.
3. Load `../references/model-catalog.md` and resolve the right live archetype:
   - Fast draft: `fast image draft`.
   - High fidelity: `high-fidelity image`.
   - Edit/restyle/preservation: `image-to-image / face reference`.
4. Inspect the selected model schema through Krea MCP. Confirm exact prompt, reference, aspect, size, quality, resolution, strength, mask, and style fields before submitting.
5. Upload local files and arbitrary external media URLs to Krea first. Pass already-Krea asset URLs directly.
6. Write the prompt for the selected mode:
   - Fast draft: concrete subject, setting, camera/style, and aspect.
   - High fidelity: subject, composition, lighting, material, style, and preservation constraints.
   - Image-to-image: describe the change, then list what must stay the same.
7. Generate one candidate first. If the user asked for options, keep the first batch cheap unless cost-preflight approved a premium batch.
8. Download and read outputs with vision. Compare against source images and non-negotiables.
9. If the result clearly misses the subject or preservation target, retry once with a more literal prompt, stronger preservation language, lower edit strength, or a better live model archetype.
10. Deliver with the saved path or URL plus one concise QA note.

### MCP path

Use available Krea MCP tools to upload inputs, list models, inspect schemas, generate images, and poll jobs. Do not hardcode model IDs or input fields.

## Banned

- Do not force simple no-reference image drafts through this workflow.
- Do not skip vision reading for source or reference images.
- Do not describe a source image as if generating from scratch when the user asked for an edit.
- Do not use external URLs as generation references without uploading them to Krea first.
- Do not produce a large or premium batch before one candidate proves the model is following the brief.
- Do not upscale a bad image just because it is high resolution; fix composition first, then enhance if needed.

## Cost & time

- Fast drafts: usually low CU, about 20-90 seconds.
- High-fidelity or image-to-image: medium to high CU, usually 1-3 minutes.
- Typical workflow: 1 candidate plus 1-3 refinements.
- Hard caps the user should know about: aspect, resolution, edit strength, masks, and multi-reference support vary by model schema.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Generic output | Prompt too loose | Add concrete subject, setting, camera, and style |
| Wrong aspect | Aspect field omitted or unsupported | Check schema and pass an accepted aspect |
| Reference ignored | Wrong model or weak input | Switch to image-to-image archetype and re-upload reference |
| Source changed too much | Edit strength too high or prompt too broad | Lower strength and name preserved details |
| Product/face drifted | Prompt overemphasized style | Add preservation language and use clearer refs |
| Low detail after good composition | Needs enhance step | Route output through `enhance.md` |
| Text is garbled | Wrong archetype | Route to `image-text-poster.md` |
