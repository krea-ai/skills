# Still To Motion

## Trigger

Use when the user provides one still image, one keyframe, one character pose, one illustration, one background plate, or one product/render frame and asks to animate it.

## Recipe

1. Read the image with vision and list what must remain stable.
2. Ask only for missing high-impact choices: duration, aspect, motion, audio, and final vs test.
3. Run cost preflight before video.
4. Upload the still if it is local. Store the URL in the project or response.
5. List live models and inspect the selected video model schema through the available Krea surface.
6. Write a motion-only prompt:
   - The still defines the subject and composition.
   - The prompt defines camera, subject motion, atmosphere, timing, and what must not drift.
7. Generate one test clip first.
8. Download, sample frames, and compare first/mid/last frames against the source still.
9. If accepted, deliver the clip path. If not, log a concrete retake prompt.

## Motion Prompt Shape

```text
Camera: locked / slow push / pan / dolly / handheld.
Subject motion: small, specific movement over N seconds.
Secondary motion: hair, cloth, steam, rain, light, particles.
Preservation: keep character design, costume, palette, composition, and background stable.
Timing: 0-1s, 1-3s, final beat.
Avoid: morphing, new subjects, extra limbs, text changes, camera over-movement.
```

## Banned

- Do not describe a different scene from the still.
- Do not promise perfect identity preservation through aggressive action.
- Do not submit many variants before inspecting the first result.
