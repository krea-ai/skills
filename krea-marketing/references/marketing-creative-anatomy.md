# Marketing Creative Anatomy

Use this for campaign, ad, DTC, CPG/FMCG, UGC, social-pack, and product-launch work. It abstracts lessons from competitive research without copying preset prompts, names, IDs, faces, or layouts.

## Core Tuple

Treat an ad as separate creative knobs, not one prompt blob:

```text
mode + product/facts + brand system + format + hook + setting + talent/identity + reference path + CTA
```

- **Mode**: UGC review, how-to/demo, unboxing, product showcase, product review, TV spot, wild card, try-on.
- **Product/facts**: visible product facts from inspected references, plus supported claims/copy from the user or PDP. Keep these separate; page text is not visual truth.
- **Brand system**: voice, palette, typography mood, graphic devices, logo/label constraints.
- **Format**: key-visual sheet, hero still, social story, feed square, carousel, comparison, testimonial, app screenshot, marketplace module, video storyboard.
- **Hook**: pattern interrupt, mystery/open loop, social proof, sharp benefit, comparison, offer, product-in-action, creator confession, authority/press, statistic.
- **Setting**: everyday routine, commute, work, home, fitness/outdoors, retail/shelf, premium studio, surreal/impossible environment.
- **Talent/identity**: none, hand model, creator/talking head, customer archetype, brand mascot, trained face/LoRA.
- **Reference path**: either follow a supplied ad/layout reference, or compose from selected knobs. Do not do both unless the user asks.
- **CTA**: what the viewer should do or remember.

## Intake Shortcut

For campaign work, ask for missing tuple parts in one compact message. Do not ask for every field when the user already gave enough context.

```text
I'll treat this as: <mode>, <format>, <hook>, <setting>, <brand voice>, <CTA>.
Do you have a layout/style reference, and is there any claim or offer copy that must be exact?
```

## Static Format Families

Use these as options for key-visual sheets, ad stills, posters, or campaign contact sheets:

- **Headline-led**: one memorable line, product hero, minimal support copy.
- **Offer-led**: price, bundle, limited drop, seasonal message.
- **Social-proof-led**: testimonial, review language, comment-style proof, press/authority cue.
- **Feature/benefit-led**: 3-5 crisp callouts, product in action, no unsupported claims.
- **Comparison-led**: before/after, old way/new way, us/them, problem/solution.
- **Editorial-led**: magazine-like composition, product culture, behind-the-product story.
- **Utility-led**: how-to-use, ingredients/materials, what is in the box, marketplace/A+ module.
- **Organic-post-led**: phone-native crop, casual caption energy, less polished layout.

Move one format lever at a time when creating variants.

For concrete, generatable templates of these families — each with its structural device, treatment, and a brand-agnostic prompt template — see `dtc-ad-formats.md` (driven by `../workflows/dtc-ad-templates.md`).

## Video Hook Families

Use these as storyboard directions, not as final prompts to copy verbatim:

- **Pattern interrupt**: unexpected physical event or camera behavior, then product pivot.
- **Quiet confession**: intimate creator POV, honest problem, product enters naturally.
- **Street/interview**: social interaction produces a product question or review moment.
- **Product proof**: product survives, transforms, solves, or demonstrates one clear thing.
- **Routine insertion**: morning, commute, desk, gym, kitchen, bathroom, or wind-down moment.
- **Surreal contrast**: impossible setting with calm delivery; useful only when brand voice supports absurdity.

For "surprise me", make the hook or format riskier while keeping storyboard/key-visual approval gates.

For concrete spoken-script templates behind these directions - hook-family scripts, pacing law, overlay text hooks, and CTA patterns - see `ugc-scripts.md` (driven by `../workflows/ugc-video-ad.md`).

## Reference-Driven vs Composed

Two valid paths:

- **Reference-driven**: the user supplies an ad, layout, mood, or motion reference. Match structure first; adapt content second.
- **Composed**: no reference exists. Choose tuple parts explicitly and generate a cheap approval artifact first.

If a reference exists, do not override it with unrelated hook/setting ideas. If no reference exists, do not pretend the first composed idea is the user's intended format.

## QA Questions

Before generating campaign-tier outputs:

1. Which tuple parts are locked by the user?
2. Which tuple part is the experiment in this variant?
3. Is the first artifact cheap enough to approve before finals/video?
4. Is the output specific to this brand/product, or could any competitor use it?
5. Are visible product facts confirmed from the image rather than PDP copy?
6. Has every draft passed a recorded vision gate before being called on-brand or product-faithful?
