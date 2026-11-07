#!/bin/bash
# Join the Theseus frames into a vertical 1080x1920 Short with
# big word captions and the voiceover.
# Usage: bash assemble.sh
set -e
cd "$(dirname "$0")"

# The narration, one word at a time, spread over the 22 seconds.
WORDS="If you take out your eyeballs and then your skin you will definitely still be the same person And if you keep removing parts of your body until only the skeleton left you still technically be the same person But what if you take all of these parts and assemble them together on Jeffrey Epstein skeleton Would you still be you or you might start cracking kid"
N=$(echo "$WORDS" | wc -w)
START=0.5
END=21.0
DUR=$(python3 -c "print(($END-$START)/$N)")

# Build the drawtext filter chain: one word at a time, white with
# a black border, bottom center.
FILTER=""
i=0
for w in $WORDS; do
    t0=$(python3 -c "print($START + $i*$DUR)")
    t1=$(python3 -c "print($START + ($i+1)*$DUR)")
    FILTER="$FILTER,drawtext=text='$w':fontsize=96:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=h-260:enable='between(t,$t0,$t1)'"
    i=$((i + 1))
done
FILTER="${FILTER#,}"

# 1. Frames -> silent 540x960 video.
ffmpeg -y -v error -framerate 24 -i frames/frame_%04d.png \
    -c:v libx264 -pix_fmt yuv420p -crf 20 -preset veryfast \
    /tmp/theseus-540.mp4

# 2. Upscale to 1080x1920 + captions.
ffmpeg -y -v error -i /tmp/theseus-540.mp4 -vf \
    "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,$FILTER" \
    -c:v libx264 -pix_fmt yuv420p -crf 20 -preset veryfast \
    /tmp/theseus-1080.mp4

# 3. Voiceover (if narration.mp3 exists) + soft bed, else bed only.
if [ -f narration.mp3 ]; then
    # Narration is 23.4s; speed it a touch to fit the 22s video.
    ffmpeg -y -v error -i /tmp/theseus-1080.mp4 -i narration.mp3 \
        -filter_complex "[1:a]atempo=1.066[voice]" \
        -map 0:v -map "[voice]" -c:v copy -c:a aac -shortest \
        theseus-22s.mp4
else
    ffmpeg -y -v error -i /tmp/theseus-1080.mp4 \
        -f lavfi -i "anoisesrc=color=brown:duration=22:amplitude=0.04" \
        -map 0:v -map 1:a -c:v copy -c:a aac -shortest theseus-22s.mp4
fi
ffprobe -v error -show_entries format=duration -of csv=p=0 theseus-22s.mp4
ls -la theseus-22s.mp4
