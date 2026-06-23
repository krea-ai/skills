# Image Text Poster

## Trigger

User asks for a poster, flyer, banner, packaging mockup, signage, ad with readable copy, title card, or any typography-heavy image. When in doubt between this workflow and `image-final-render.md`, pick this if legible text is central to success.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Exact text**: headline, subhead, date, CTA, legal line.
- **Format**: poster, story, banner, square, print.
- **Brand/style**: palette, type mood, references.
- **Text hierarchy**: what must be largest.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Extract exact copy. Do not paraphrase text that should appear in the image.
2. Resolve `text in image / typography` archetype from live `list_models`.
3. Inspect schema for prompt, text, aspect, and quality fields.
4. If references are supplied, read them with vision and upload local assets.
5. Write a layout prompt with explicit hierarchy: headline, subhead, body, CTA.
6. Generate one candidate at the requested aspect.
7. Download and read with vision, checking text legibility and spelling.
8. If text is wrong, retry with shorter text blocks or split into design-first image plus external typography recommendation.
9. Deliver with spelling QA notes.

### MCP path

Use the available Krea MCP tools to list models, inspect the selected model schema, then call image generation with schema-verified prompt, aspect, text, quality, and resolution fields.

## Banned

- Do not use a generic art model when readable text is the core requirement.
- Do not invent or rewrite the user's exact text.
- Do not promise perfect small legal copy; tiny text is fragile.
- Do not deliver before vision-checking spelling.

## Cost & time

- Per-job: medium to high CU, 1-3 minutes depending on model.
- Typical full workflow: 1-4 text-correction attempts.
- Hard caps the user should know about: long copy is unreliable; keep image text short.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Garbled headline | Text too long or wrong archetype | Shorten copy and use typography model |
| Wrong hierarchy | Prompt did not define scale | Specify largest/middle/smallest text |
| Nice image, bad copy | Model hit visual but failed text | Regenerate or recommend external type overlay |
| Cropped text | Aspect/layout mismatch | Add margins and safe area language |
