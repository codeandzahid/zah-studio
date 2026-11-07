#!/bin/bash
# Render the Theseus video in 2 parallel chunks (never 4 — RAM).
# Usage: bash render.sh [frames]   (default 528 = 22s at 24fps)
set -e
cd "$(dirname "$0")"
FRAMES="${1:-528}"
BLENDER=~/workspace/blender/blender-5.2.3-linux-x64/blender
HALF=$((FRAMES / 2))
mkdir -p frames
# Chunk 1: frames 1..HALF, chunk 2: HALF+1..FRAMES. Each chunk
# renders only its missing frames (re-runnable after a restart).
DEMO_FRAMES=$FRAMES FRAME_START=1 FRAME_END=$HALF \
    "$BLENDER" -b --python build_theseus.py > /tmp/theseus-chunk1.log 2>&1 &
P1=$!
DEMO_FRAMES=$FRAMES FRAME_START=$((HALF + 1)) FRAME_END=$FRAMES \
    "$BLENDER" -b --python build_theseus.py > /tmp/theseus-chunk2.log 2>&1 &
P2=$!
wait $P1 $P2
echo "Done. Frames in frames/: $(ls frames/*.png 2>/dev/null | wc -l) / $FRAMES"
