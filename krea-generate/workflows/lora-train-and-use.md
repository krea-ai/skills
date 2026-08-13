# LoRA Train And Use

## Trigger

User asks to train a LoRA, fine-tune a style, keep a brand/person/product consistent, create a reusable style ID, or generate samples from a custom style. Use this when repeatability or exact identity across many outputs matters.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Type**: Style, Object, Character, or Default.
- **Training set**: 15-20 images preferred, hosted URLs or local files to upload.
- **Name and trigger word**: unique, short, brand-safe.
- **Sample outputs**: what to generate after training completes.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. Read a sample of training images with vision; reject blurry, tiny, duplicated, or off-style inputs.
2. If local, upload or ensure each training image has a reachable HTTPS URL.
3. Validate URL reachability when that capability is available; otherwise rely on upload/training errors.
4. Discover or verify the current supported training base models through live Krea tools before submitting. Do not use a remembered training model id.
5. Submit training only if the current tools expose LoRA/style training. If not, tell the user this capability is not available in this session.
6. Wait for completion with the available job tool, reporting progress per `../references/progress-reporting.md`.
7. On completion, capture `style_id` and trigger word.
8. Resolve a style-aware image model from live `list_models` and inspect schema for the exact style field, such as `style_id`, `styleId`, or `styles`.
9. Generate 3-5 samples using the new style at strength ~0.85.
10. **Deliver** style ID, trigger word, sample outputs, and QA notes.

### Training

Verify the current tool schema for LoRA/style training before use. Use only fields exposed in this session. Do not assume training payload fields from memory.

### Generate samples after training

```
list_models()
get_model_schema(model="<style-aware-image-model>")
generate_image(model="<style-aware-image-model>", input={prompt, <schema-style-field>, <schema-strength-field>}, sync=true)
```

## Banned

- Do not train on fewer than 10 weak images unless the user accepts poor results.
- Do not skip long-running progress pings.
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
| User wants one portrait only | LoRA is overkill | Generate directly using the model-selection guidance in `../SKILL.md` |
