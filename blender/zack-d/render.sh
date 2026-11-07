#!/bin/bash
# Render the Zack D.-style money tree scene (Blender, Workbench).
#   bash render.sh            — 240 frames (10 seconds)
#   DEMO_FRAMES=1440 bash render.sh   — 1440 frames (60 seconds)
# Renders in 4 chunks at once. Needs Blender: set BLENDER or put
# blender on your PATH (https://www.blender.org/download/).
set -e
cd "$(dirname "$0")"
BLENDER="${BLENDER:-blender}"
FRAMES="${DEMO_FRAMES:-240}"
mkdir -p frames
CHUNK=$(( (FRAMES + 3) / 4 ))
pids=()
i=0
while [ $i -lt 4 ]; do
  START=$(( i * CHUNK + 1 ))
  END=$(( (i + 1) * CHUNK ))
  [ "$END" -gt "$FRAMES" ] && END="$FRAMES"
  [ "$START" -gt "$FRAMES" ] && break
  FRAME_START="$START" FRAME_END="$END" DEMO_FRAMES="$FRAMES" \
    "$BLENDER" -b --python build_money_tree.py \
    > "render-chunk$((i+1)).log" 2>&1 &
  pids+=($!)
  i=$((i + 1))
done
for pid in "${pids[@]}"; do wait "$pid"; done
echo "Rendered $FRAMES frames into frames/"
