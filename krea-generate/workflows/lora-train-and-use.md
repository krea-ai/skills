# LoRA Train And Use

## Trigger

User asks to train a LoRA, fine-tune a style, keep a brand/person/product consistent, create a reusable style ID, or generate samples from a custom style. When in doubt between this workflow and `portrait-with-refs.md`, pick this if repeatability or exact identity across many outputs matters.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Type**: Style, Object, Character, or Default.
- **Training set**: 15-20 images preferred, hosted URLs or local files to upload.
- **Name and trigger word**: unique, short, brand-safe.
- **Sample outputs**: what to generate after training completes.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. **Cost-preflight** (mandatory - see `../references/cost-preflight.md`). Training can take 15-45 minutes.
2. Read a sample of training images with vision; reject blurry, tiny, duplicated, or off-style inputs.
3. If local, upload or ensure each training image has a reachable HTTPS URL.
4. Validate URL reachability through MCP when that capability is available; otherwise rely on MCP upload/training errors.
5. Discover or verify the current supported training base models through Krea MCP before submitting. Do not use a remembered training model id.
6. Submit training through Krea MCP only. If MCP does not expose LoRA training, stop and tell the user this capability is not available in the connected Krea MCP server yet.
7. Poll every 30-60 seconds using `../references/progress-reporting.md`.
8. On completion, capture `style_id` and trigger word.
9. Resolve a style-aware image model from live `list_models` and inspect schema for the exact style field, such as `style_id`, MCP `styleId`, or `styles`.
10. Generate 3-5 samples using the new style at strength ~0.85.
11. **Deliver** style ID, trigger word, sample outputs, and QA notes.

### MCP training

Verify the current MCP tool schema for LoRA/style training before use. Use only fields exposed by the connected MCP server. Do not use non-MCP endpoints or assume training payload fields from memory.

### Generate samples after training

```
# Use MCP after completion for style-aware image generation:
list_models()
get_model_schema(model="<style-aware-image-model>")
generate_image(model="<style-aware-image-model>", input={prompt, <schema-style-field>, <schema-strength-field>}, sync=true)
```

## Banned

- Do not train on fewer than 10 weak images unless the user accepts poor results.
- Do not skip cost-preflight or long-running progress pings.
- Do not assume the schema field is always `styleId` or `style_id`; inspect the model.
- Do not persist style IDs into project files without explicit user approval.

## Cost & time

- Per-job: training cost varies; 15-45 minutes typical.
- Typical full workflow: one training job plus 3-5 sample generations.
- Hard caps the user should know about: URL count, image quality, type, and base model are API-specific.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Training fails mid-run | Bad URL or inaccessible asset | HEAD-check URLs and resubmit |
| Samples ignore style | Underfit or missing trigger | Use trigger word and style strength; retrain with better set |
| Samples all look same | Overfit | Lower style strength or retrain with more varied images |
| User wants one portrait only | LoRA is overkill | Route to `portrait-with-refs.md` |
