# Video Ad QA

Delivery gate for UGC and social video ads. Run it on the assembled piece before calling anything ready: sample the first frame plus 4-6 beat frames with ffmpeg, inspect them with vision, and score. This extends, not replaces, the recorded vision inspections required by `../SKILL.md` and `../../krea-generate/references/vision-qa.md`.

## Virality Scorecard

Score the piece 0-100 on each criterion, then take the overall as a judgment call weighted toward hook and scroll-stop (not a mean). Score honestly; the point is to catch weak ads before the user pays attention to them.

| Criterion | Question |
|---|---|
| hook_strength | Do the opening 1-3 seconds stop the scroll? Visual impact plus emotional charge. |
| emotional_impact | Does it trigger relatability, shock, humor, or empathy? |
| pacing_flow | Tight, snappy, no dead time? Does anything drag? |
| text_readability | Overlay text clear, well-positioned, high-contrast, scannable? |
| scroll_stop_power | Would someone stop mid-scroll on the FIRST frame alone? |
| completion_likelihood | Will viewers reach the end? Shorter scores higher. |
| shareability | Would someone send this to a friend? Is the hook universal? |

Self-scoring prompt (adapt in place):

```text
You are a short-form video ads expert. Score this ad 0-100 overall and per criterion
(hook_strength, emotional_impact, pacing_flow, text_readability, scroll_stop_power,
completion_likelihood, shareability). For each: score + one-sentence reason.
Then name the top strength, the top weakness, and one concrete improvement.
Be blunt; do not grade on a curve.
```

## Thresholds

| Overall | Action |
|---|---|
| 85-100 | Deliver; flag as the lead variant |
| 70-84 | Deliver; note optional tweaks |
| 55-69 | Rework hook or pacing before delivering |
| <55 | Re-edit significantly or discard; do not deliver as-is |

## Per-Criterion Fixes

| Weak criterion | Fix |
|---|---|
| hook_strength | Change the opening beat or overlay hook; needs emotional punch in 1-3s |
| emotional_impact | Reaction/delivery does not match the script's emotion; re-storyboard the human beat |
| pacing_flow | Dead time or slow cuts; tighten takes, trim to a shorter duration |
| text_readability | Text too small, off green-zone, or low contrast; fix per `video-ad-post.md` |
| scroll_stop_power | Weak first frame; open on the expressive face or bolder overlay text |
| completion_likelihood | Too long or sags mid-piece; trim toward 10-15s |
| shareability | Hook too niche; pick a more universal angle from `ugc-scripts.md` |

Combine with the existing adversarial UGC question from `ugc-social-video.md`: "Would a TikTok/Reels viewer read this as real creator content, or a brand ad pretending?"

## Green Zones (Text Safe Areas)

At 1080x1920, platform UI eats the edges: top bar (username, sound), right rail (engagement buttons), bottom (caption, CTA). Keep ALL burned text inside the safe zone.

- **Universal safe zone** (safe on TikTok, Reels, Shorts): x 60-960, y 210-1480.
- TikTok: x 60-960, y 150-1480.
- Instagram Reels: x 44-996, y 210-1610.
- YouTube Shorts: x 60-984, y 170-1530.

Placement presets:

- Hook text: upper zone, y ~280-340.
- Running captions: mid-lower, y ~0.60 x height.
- CTA card: lower zone, y ~1380 (still above the platform caption area).
- Horizontal: center within x 60-960.

Scale proportionally for other resolutions.

## Duration Sweet Spot

Completion rates fall off hard with length: 7-10s very high, 10-15s high, 15-30s medium, 30s+ low. Default UGC ads to 15s (the format maximum); drop to 10s for a tighter cut, and only go longer when the script genuinely needs it and the user accepts the completion tradeoff.

## Performance Heuristics (Post-Publish)

Only relevant when the user brings real platform metrics (e.g. via the Meta Ads read path in `meta-ads-mcp.md`). Never invent these numbers; without real data, label everything a creative hypothesis.

Rough 24-48h winner bands used by short-form operators:

| Metric | Good | Great | Viral |
|---|---|---|---|
| Views | 10K+ | 100K+ | 1M+ |
| Like ratio | 5%+ | 10%+ | 15%+ |
| Comment ratio | 0.5%+ | 1%+ | 2%+ |
| Share ratio | 0.3%+ | 1%+ | 3%+ |

Use winners to pick which variant axes to double down on (hook family, persona, setting), one axis at a time.
