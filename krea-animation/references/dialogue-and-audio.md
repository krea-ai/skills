# Dialogue and audio

Use this reference when a workflow has dialogue, subtitles, a continuous music bed, or a video model that returns silent clips.

## First choice by model

| Video model path | Primary audio path |
|---|---|
| Seedance (2.5 or the 2.0 family) with native audio | Prompt dialogue, foley, ambience, and score inside each clip. Keep the native audio. |
| Silent video model | Generate or source audio separately, then mux it after visual assembly. |
| User-supplied track | Upload or keep the track as the timing reference when the model supports audio input; otherwise use it as the final bed. |

For Seedance, do not default to external TTS. Native dialogue and foley are part of the model's value. External TTS is a fallback when the selected model returns silent video, when Seedance dialogue is unusable after one retry, or when the user specifically requests a known voice pipeline.

## Prompting native audio

For each shot, include an `Audio:` block with only the audio that should be present in that shot:

```text
Audio: low room tone, one ceramic cup click at the cut, protagonist whispers "I remember now" in Spanish, no music swell until the final half-second.
```

Keep dialogue lines short enough to fit the shot. If a line cannot be spoken naturally inside the planned duration, either split the line across shots or lengthen the shot before generation.

## Thin overlay bed pattern

Use this only when native per-clip audio needs glue across cuts. Keep the Seedance clip audio as the main track and mix a quiet bed underneath:

```bash
ffmpeg -y \
  -i assembled-with-native-audio.mp4 \
  -i bed.wav \
  -filter_complex "[1:a]volume=0.18,aloop=loop=-1:size=2e+09[bed];[0:a][bed]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 \
  final-with-bed.mp4
```

If the bed masks dialogue, lower `volume` before touching the dialogue track.

## Silent-video mux pattern

For models that return silent video, strip any accidental audio, concatenate normalized clips, then add the bed and dialogue lines in one pass:

```bash
ffmpeg -y \
  -i concat-video-only.mp4 \
  -i bed.wav \
  -i line-01.wav \
  -i line-02.wav \
  -filter_complex "\
    [1:a]volume=0.35[bed];\
    [2:a]adelay=1200|1200[l1];\
    [3:a]adelay=4700|4700[l2];\
    [bed][l1][l2]amix=inputs=3:duration=longest:normalize=0[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 \
  final.mp4
```

Take millisecond offsets from the shot list's own timings. Listen to each line before muxing and sample the final mix at every dialogue timestamp.

## Subtitles

If the local ffmpeg build supports libass, burn subtitles with:

```bash
ffmpeg -y -i final.mp4 -vf "subtitles=subs.srt" -c:a copy final-subbed.mp4
```

If `subtitles=` is unavailable, render subtitle PNGs and overlay them with `overlay` filters. Do not stop a delivery to rebuild ffmpeg when the PNG overlay path is available.

## Failure handling

| Symptom | Fix |
|---|---|
| Seedance dialogue missing | Retry once with shorter verbatim lines and clearer speaker labels in the `Audio:` block. |
| Seedance clip audio is chaotic | Reduce the prompt to dialogue + essential foley only; add continuous music later with the thin bed pattern. |
| Silent-model line lands late | Adjust `adelay` from the shot start timestamp and re-mux; do not regenerate video. |
| Dialogue is buried | Lower bed volume before boosting dialogue. |
| Clipping or distortion | Re-mux with lower source volumes and keep `normalize=0`; listen again before delivery. |
