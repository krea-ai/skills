# Meta Ads MCP

Use this reference when a marketing user wants performance-informed creative planning, campaign analysis, catalog context, or Meta Ads activation.

The connected Meta Ads MCP tools are the source of truth. Meta Ads is a fast-moving authenticated ads-ops surface, so verify tool names, schemas, and permissions live before using them.

## Role In This Skill

Meta Ads is optional. It improves creative strategy and activation, but Krea marketing creative must still work without it.

Use Meta Ads before creative when connected:

- Identify winning and weak creative formats.
- Detect fatigue, spend concentration, and underperforming campaigns.
- Inspect placement, objective, CTA, product/catalog, and audience signals.
- Turn performance patterns into creative hypotheses.

Use Meta Ads after creative only with approval:

- Draft campaigns, ad sets, ads, or catalog associations.
- Upload/use approved creative.
- Change budgets, status, or launch state.

## Entry Prompt

Ask this in the marketing intake when relevant:

```text
Do you want me to connect Meta Ads MCP for performance context before creative planning? If yes, I will read account/campaign/catalog signals first. If not, I will proceed Krea-only from your product refs, brand refs, and goals.
```

## Discovery

Before any Meta call:

1. Check whether a Meta Ads MCP connector is available.
2. Read the exposed tool descriptions and schemas.
3. Confirm the selected ad account before reads or writes.

Do not guess tool names from memory. If Meta MCP is not connected, continue Krea-only.

## Read-First Analysis

For performance-informed creative briefs, collect only what is needed:

- Account and campaign names relevant to the request.
- Recent spend, CPA/ROAS/CTR/CVR, or the user's chosen KPI.
- Best and worst ads by creative, hook, placement, objective, and CTA.
- Fatigue signals such as declining CTR/CVR, rising CPA, or repeated creatives.
- Product/catalog performance when the request is product-led.

Translate findings into a creative brief:

```text
Performance read:
- Winning pattern:
- Weak pattern:
- Fatigue risk:
- Product / placement signal:
- Creative implication:
```

## Write Gates

Paused/draft is the default. Before any write, show:

- Account.
- Campaign/ad set/ad/catalog entity.
- Action.
- Budget or status impact.
- Creative asset IDs/URLs.
- Whether the result will be paused/draft or live.

Live launch, budget edits, status changes, publishing, and catalog mutations require explicit approval. If the approval does not name the live/published state, create paused/draft or stop.

## Banned

- Do not require Meta Ads to generate Krea creative.
- Do not invent account performance data.
- Do not change budgets, statuses, catalogs, or live campaigns from a vague "go ahead".
- Do not use Meta performance data to make unsupported product claims in creative.
