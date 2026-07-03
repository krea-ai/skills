# Full Ad Campaign

## Trigger

User gives a product URL or product brief and asks for a campaign, ad set, launch assets, social variants, product URL to creative, or "give me ads for this". When in doubt between this workflow and `product-photo-hero.md`, pick this if the user wants multiple formats or angles.

## Clarify

Ask the user once, in a single batched message. Skip whichever the user already volunteered.

- **Source**: product URL, product images, or written brief.
- **First deliverable shape**: key-visual sheet, static ad set, or social video storyboard.
- **Creative anatomy**: mode, format, hook, setting, talent/identity, reference path, CTA.
- **Deliverables**: hero, lifestyle, TikTok, IG, YouTube, Pinterest, posters.
- **Angles**: lifestyle, feature, social proof, comparison, offer, UGC.
- **Approval level**: drafts only, final renders, or draft-to-final winners.

If the user gave a tight, complete brief, skip Clarify entirely and proceed to Recipe.

## Recipe

Hard prescription. Follow in order.

1. **Identify first deliverable shape**. For CPG/FMCG/agency-style campaign asks, route to `key-visual-sheet.md` first. For a static ad set built around one product photo, route to `dtc-ad-templates.md`. For other digital static sets, start with cheap image drafts. For UGC/social video sets, route to `social-video-short.md`; if the videos need a spoken script, captions, or a CTA card (scripted UGC ads, talking-head/testimonial ads, narrated demos), route to `ugc-video-ad.md` instead.
2. If the user chose Meta Ads context, run `meta-ads-performance.md` first and incorporate the performance read into the creative brief.
3. Load `../references/marketing-creative-anatomy.md` and decompose the campaign into mode, product/facts, brand system, format, hook, setting, talent/identity, reference path, and CTA.
4. **Cost-preflight** (mandatory - see `../../krea-generate/references/cost-preflight.md`). Campaigns are batches.
5. Extract text facts from the URL or user brief for claims/copy only. Do not treat PDP copy, alt text, filenames, or scraped descriptions as visual product truth.
6. Read product images with vision and identify only visible product facts. For apparel, name silhouette, texture, colorway, trim, hardware, pattern, closures, logo/pin/embroidery, and proportion. If a URL does not expose usable product images, stop and ask for product refs before promising faithful product creative.
7. If a URL or scraped source was used, confirm the visual brief in one line before generating: visible product facts + supported claims/copy + deliverable shape. Do not confirm PDP text facts as if they were seen.
8. Resolve live marketing image candidates using the marketing image set in `../SKILL.md`: default `openai/gpt-image-2` (always first for copy-heavy images and real-product scene composites); for product/final stills, offer live Nano Banana 2 / Nano Banana Pro as alternatives and let the user choose. If Nano Banana is chosen with a real product ref, use stricter scene-only prompting because prompt words can override the reference.
9. Write real-product prompts around scene, pose/use, light, camera, composition, platform copy, and placement. Do not include product color, material, silhouette, trim, hardware, label, or garment descriptors in the generation prompt; keep those facts in the visual confirmation and QA checklist only.
10. Generate lightweight drafts by angle and format first, unless step 1 routed to a key-visual sheet or social storyboard gate.
11. **Blocking draft QA gate**: read every draft with vision, compare it to the visible brief, and record pass/fail before any finals, upscale, animation, or delivery claim. Reject outputs with wrong product identity, wrong claims, Recolored logo, Prompt-text override, or generic product drift. If none pass, retake one lever at a time or ask for clearer refs.
12. Show a contact sheet or labeled list only after the gate, with pass/fail notes; let the user pick winners for final render/upscale.
13. Generate final winners through `product-photo-hero.md`, `product-photo-lifestyle.md`, `dtc-ad-templates.md`, `../../krea-generate/workflows/image-text-poster.md`, `key-visual-sheet.md`, `social-video-short.md`, or `ugc-video-ad.md` as needed.
14. **Deliver** organized outputs by platform, with QA notes and any unsupported claims removed.

### MCP path

Use the available Krea MCP tools to list models, inspect schema for draft and final image models, then call image generation with schema-verified campaign prompt, reference, aspect, quality, and resolution fields.

## Banned

- Do not invent product claims, certifications, pricing, or performance promises.
- Do not build prompts from PDP copy alone when product images exist or can be fetched.
- Do not re-describe real product material, color, silhouette, trim, or hardware in the prompt; let the reference carry product facts.
- Do not skip the draft QA gate or present a set as on-brand/product-faithful without recorded inspection.
- Do not upscale every draft; only upscale user-approved winners.
- Do not start with premium renders for every angle.
- Do not assume "storyboard" means film pre-vis in CPG/FMCG/agency campaign work; check `../references/artifact-taxonomy.md`.
- Do not treat "make ads" as one prompt. Use `../references/marketing-creative-anatomy.md` to separate mode, format, hook, setting, talent, product, brand, reference path, and CTA.
- Do not generate social video without routing into `social-video-short.md` (continuous clip) or `ugc-video-ad.md` (scripted ad).

## Cost & time

- Per-job: drafts are low to medium CU; finals and videos vary widely.
- Typical full workflow: 6-18 drafts plus 2-6 finals; 10-45 minutes without video, longer with video.
- Hard caps the user should know about: URL extraction may be thin; ask for product refs when page imagery is poor.

## On failure

| Symptom | Cause | Fix |
|---|---|---|
| Product facts wrong | URL extraction hallucinated or was thin | Re-read source and ask user to confirm facts |
| Too many weak variants | No approval gate | Draft first, contact sheet, final only winners |
| Output makes unsupported claims | Prompt included invented copy | Remove claims and regenerate visual-only |
| Recolored logo | Model flattened the product photo into a tinted graphic/logo-like mark | Retake with cleaner photo reference, photo-first settings, and scene-only prompt |
| Prompt-text override | Output follows prompt words instead of the attached product reference | Remove product descriptors from the prompt; keep scene, pose, light, copy, and placement only |
| User asks for UGC video | Expensive sub-workflow | Route to `social-video-short.md` (continuous) or `ugc-video-ad.md` (scripted) with cost-preflight |
| User expected a key-visual sheet | Ambiguous "storyboard" or "ad" vocabulary | Route to `key-visual-sheet.md` before downstream assets |
