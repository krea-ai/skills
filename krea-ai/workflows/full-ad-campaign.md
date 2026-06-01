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

1. **Identify first deliverable shape**. For CPG/FMCG/agency-style campaign asks, route to `key-visual-sheet.md` first. For digital static ad sets, start with cheap image drafts. For UGC/social video sets, route to `social-video-short.md`.
2. Load `../references/marketing-creative-anatomy.md` and decompose the campaign into mode, product/facts, brand system, format, hook, setting, talent/identity, reference path, and CTA.
3. **Cost-preflight** (mandatory - see `../references/cost-preflight.md`). Campaigns are batches.
4. Extract product facts from the URL or user brief. Do not invent claims.
5. Read product images with vision and identify product shape, materials, label, and brand palette.
6. Confirm the extracted brief in one line before generating if a URL was used.
7. Resolve live archetypes: `fast image draft`, `high-fidelity image`, `text in image / typography` if copy appears in image, and `faithful upscale` for winners.
8. Generate cheap drafts by angle and format first, unless step 1 routed to a key-visual sheet or social storyboard gate.
9. Read drafts with vision and reject outputs where product identity or claims are wrong.
10. Show a contact sheet or labeled list; let the user pick winners for final render/upscale.
11. Generate final winners through `product-photo-hero.md`, `product-photo-lifestyle.md`, `image-text-poster.md`, `key-visual-sheet.md`, or `social-video-short.md` as needed.
12. **Deliver** organized outputs by platform, with QA notes and any unsupported claims removed.

### CLI

```bash
# After extracting and confirming brief:
krea generate image -m "<fast-image-draft>" \
  --aspect 9:16 \
  -p "<product> TikTok draft, <angle>, preserving factual claims only" \
  --wait -o ./draft-tiktok.png

krea generate image -m "<high-fidelity-image>" \
  --aspect 16:9 \
  -i imageUrl="<product-ref-url>" \
  -p "<approved hero angle final prompt>" \
  --wait -o ./hero-final.png
```

### MCP fallback

```
list_models()
get_model_schema(model="<fast-image-draft>")
generate_image(...drafts..., sync=true)
get_model_schema(model="<high-fidelity-image>")
generate_image(...finals..., sync=true)
```

## Banned

- Do not invent product claims, certifications, pricing, or performance promises.
- Do not upscale every draft; only upscale user-approved winners.
- Do not start with premium renders for every angle.
- Do not assume "storyboard" means film pre-vis in CPG/FMCG/agency campaign work; check `../references/artifact-taxonomy.md`.
- Do not treat "make ads" as one prompt. Use `../references/marketing-creative-anatomy.md` to separate mode, format, hook, setting, talent, product, brand, reference path, and CTA.
- Do not generate social video without routing into `social-video-short.md`.

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
| User asks for UGC video | Expensive sub-workflow | Route to `social-video-short.md` with cost-preflight |
| User expected a key-visual sheet | Ambiguous "storyboard" or "ad" vocabulary | Route to `key-visual-sheet.md` before downstream assets |
