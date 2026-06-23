# Meta Ads Performance

## Trigger

User asks to use Meta Ads data, improve ad performance, analyze a campaign, inspect creative fatigue, understand what creative to make next, draft campaign structure, or activate approved Krea creative in Meta Ads.

## Clarify

Ask once, skipping what is already clear:

- **Mode**: performance read, creative brief, paused draft activation, or live change.
- **Account/campaign scope**: account, campaign, ad set, product/catalog, or time window.
- **KPI**: CPA, ROAS, CTR, CVR, spend, revenue, leads, purchases, or user-defined.
- **Creative goal**: what to make or improve.

## Recipe

1. Load `../references/meta-ads-mcp.md`.
2. Verify Meta Ads MCP availability and read tool descriptions. Do not guess tool names.
3. Confirm the selected ad account before reading data.
4. For creative planning, read relevant performance/campaign/catalog context and produce:
   - winning pattern
   - weak pattern
   - fatigue risk
   - product/placement signal
   - creative implication
5. Route creative production to `full-ad-campaign.md`, `key-visual-sheet.md`, `social-video-short.md`, `product-photo-hero.md`, or `marketplace-cards.md`.
6. For activation, show the exact proposed Meta action. Create paused/draft by default.
7. For live launch, budget/status edits, publishing, or catalog mutations, require explicit approval naming account, entity, action, budget/status, and live-vs-paused state.

## Banned

- Do not require Meta to proceed with creative.
- Do not invent performance data or infer private account facts.
- Do not write to Meta without an explicit proposal and approval.
- Do not create live entities by default.
- Do not use account performance data to create unsupported product claims.

## Output

For read-first creative planning:

```text
Meta performance read:
- Winning pattern:
- Weak pattern:
- Fatigue risk:
- Creative implication:
Next creative route: <workflow>
```

For writes:

```text
Proposed Meta action:
- Account:
- Entity:
- Action:
- Status: paused/draft unless explicitly approved live
- Budget/status impact:
- Creative assets:
```
