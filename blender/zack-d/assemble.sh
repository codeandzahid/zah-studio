#!/bin/bash
# Join the rendered frames into a video with a soft sound bed.
#   bash assemble.sh            — joins 240 frames (10s)
#   DEMO_FRAMES=1440 bash assemble.sh   — joins 1440 frames (60s)
set -e
cd "$(dirname "$0")"
FRAMES="${DEMO_FRAMES:-240}"
DUR=$(( FRAMES / 24 ))
ffmpeg -y -v error -framerate 24 -i frames/frame_%04d.png \
  -f lavfi -i "anoisesrc=color=brown:duration=${DUR}:amplitude=0.15" \
  -filter:a "lowpass=f=300,volume=0.12" -shortest \
  -c:v libx264 -pix_fmt yuv420p -crf 20 \
  -c:a aac -b:a 128k -movflags +faststart \
  "money-tree-${DUR}s.mp4"
echo "Done: money-tree-${DUR}s.mp4"
