#!/bin/bash
# Assemble rendered frames + game sounds into the 4K video.
# Game sounds (jump boings, coin dings, finish fanfare) are synthesized
# by gen_sfx.py — no sound files needed.
set -e
cd "$(dirname "$0")"

python3 gen_sfx.py

ffmpeg -y -v error -framerate 24 -i frames/frame_%04d.png -i /tmp/roblox-sfx.wav \
  -vf scale=3840:2160:flags=lanczos,unsharp=5:5:0.6 \
  -c:v libx264 -pix_fmt yuv420p -crf 23 -c:a aac -b:a 128k -shortest \
  -movflags +faststart roblox-obby-4k-60s.mp4

ffprobe -v error -show_entries format=duration,size \
  -of default=noprint_wrappers=1 roblox-obby-4k-60s.mp4
echo ASSEMBLY_DONE
