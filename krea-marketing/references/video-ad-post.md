# Video Ad Post-Production

Assembly layer for UGC/social video ads: captions, CTA card, multi-take stitching, and music beds. Text is NEVER asked from the video model - models render text unreliably; burned text is pixel-perfect on every render. Default path is local ffmpeg; route to the `hyperframes` skill only for designed caption styles.

All coordinates below assume 1080x1920; scale proportionally. All text must live inside the green zones in `video-ad-qa.md`.

## Captions (ffmpeg drawtext)

Caption discipline:

- Captions are opt-in: ask the user once (yes/no + style) before burning. Recommend them - most social video plays muted.
- 2-3 words per phrase, max ~1.1s on screen per phrase. Break on punctuation.
- One caption position for the whole piece: centered, mid-lower (`x=(w-text_w)/2`, `y=h*0.60`).
- White text with a heavy dark border for contrast (`borderw=8:bordercolor=black`); ONE emphasis color (e.g. brand yellow) for key words only.
- Font size ~78 for short phrases (<=14 chars), ~66 for longer; wrap anything >18 chars into 2 balanced lines.
- A bold rounded sans in the platform's native energy; verify the font file exists locally before building the filter.
- Sync caption timing to the actual audio, not to guessed timestamps: extract or estimate word timing from the generated take (listen/inspect), then assign phrase windows. Mis-timed captions read as fake instantly.
- Stop captions before the CTA window so they never overlap the card.

Each phrase is one drawtext filter gated by time:

```bash
drawtext=fontfile=FONT:text='king of hooks':fontsize=78:fontcolor=white:\
borderw=8:bordercolor=black:x=(w-text_w)/2:y=h*0.60:\
enable='between(t,2.10,3.15)'
```

Chain all phrases plus the CTA card in a single `-vf` pass.

Caption styles to offer:

- **bold-emphasis**: large type, key words in the emphasis color, brief holds - high energy.
- **flowing**: smaller phrases in steady rhythm - conversational, storytelling.
- **minimal**: only the load-bearing phrases, lots of air - clean/premium-casual.

## CTA Card

Reserve the final ~4 seconds. Bigger type (fontsize ~92), emphasis/brand color, heavier border (`borderw=10`), centered slightly lower (`y=h*0.65`), enabled from `cta_start` to end:

```bash
drawtext=fontfile=FONT:text='APPNAME - App Store':fontsize=92:fontcolor=0xFFE600:\
borderw=10:bordercolor=black:x=(w-text_w)/2:y=h*0.65:enable='between(t,11.0,15.0)'
```

Keep it native: a type card, not a polished brand end-slate, unless the user asks.

## Segment Assembly (Multi-Take / Cutaways)

Normalize every segment to the delivery frame before stitching:

```bash
ffmpeg -i IN -ss START -t DUR \
  -vf "scale=w=1080:h=1920:force_original_aspect_ratio=decrease,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=30" \
  -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p seg_00.mp4
```

Then concat without re-encoding:

```bash
printf "file 'seg_00.mp4'\nfile 'seg_01.mp4'\n" > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy stitched.mp4
```

This stitching is for takes of ONE continuous scripted piece (talking-head takes + demo cutaways with the same identity refs). It does not license the banned per-storyboard-panel generation pattern from `../workflows/social-video-short.md` - a UGC ad's cut structure is designed in the script/storyboard, not improvised in ffmpeg.

Preserve generated dialogue audio through the video chain (`-an` only on video-only segments whose audio you're replacing; keep the talking take's audio track).

## Music Bed (Optional)

When adding music under model-generated audio or silent footage:

```bash
# Pre-bake the bed: loop, normalize to -16 LUFS, fade in
ffmpeg -y -stream_loop -1 -i SOURCE.mp3 -t 17 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.4" -c:a libmp3lame -q:a 2 bed.mp3

# Mix: dialogue full, music ~50%, fade out, limiter; don't renormalize the mix
ffmpeg -y -i video.mp4 -i bed.mp3 -filter_complex \
  "[1:a]atrim=0:DUR,asetpts=PTS-STARTPTS,volume=0.5,afade=t=out:st=DUR-1.5:d=1.5[m];\
[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.97[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart final.mp4
```

Dialogue stays fully intelligible; if the music fights the voice, drop it to 0.3-0.4, don't raise the voice.

## Delivery Spec

1080x1920 (9:16), 30fps, H.264 `yuv420p`, AAC 192k, `-movflags +faststart`. Square deliveries: 1080x1080, same encode.

## When to Use HyperFrames Instead

Route composition to the `hyperframes` skill (as `../workflows/launch-teaser.md` does) when the user wants designed caption animation, beat-synced type, brand-styled cards, or a polished end sequence. That is designed motion, not native UGC - do not mix the two vocabularies in one piece. For a UGC ad that should read as creator content, burned drawtext captions are the default.
