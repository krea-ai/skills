# Motion Prompting

## Principle

Use images for identity and composition. Use prompt text for motion, timing, and constraints.

## Shot Prompt Template

```text
Style: <approved style guide in one sentence>.
Dynamic description: <camera and subject motion across the duration>.
Static description: <only what must remain visible and stable>.
Timing: 0-1s <beat>; 1-3s <beat>; final beat <exit or hold>.
References: preserve <characters/props/backgrounds>.
Avoid: morphing, extra characters, extra limbs, costume changes, text changes, camera over-movement.
Audio: <silent or exact desired foley/music/dialogue>.
```

## Start And End Frames

Use start and end frames when the action has a clear transition. The end frame should not be a completely different scene unless the model has enough duration and the cut is designed as a transition.

## Reference Images

Use reference images for:

- character identity
- costume
- background plate
- prop design
- color palette
- texture or line style

Do not overload references. Too many unrelated references can confuse the model.

## Avoiding Drift

- Keep motion smaller for identity-critical shots.
- Use stronger references for close-ups.
- Use clean background plates for location continuity.
- State "no new characters" when the frame should stay isolated.
- Use "camera continues drifting through final beat" when chaining clips to reduce end-frame freeze.
- For action, break one complex shot into multiple simple shots.

## Retake Prompting

A retake prompt should fix one failure at a time:

```text
Retake SC001_SH020. Preserve the approved start image exactly. Reduce camera motion to a slow push-in. Keep the red jacket unchanged. Remove the extra background figure. The hand should only lift the cup; no full body turn.
```
