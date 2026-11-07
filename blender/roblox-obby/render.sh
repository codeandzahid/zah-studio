#!/bin/bash
# Render the Roblox obby video: 1440 frames in 4 parallel chunks.
# Needs Blender on the PATH, or set BLENDER=/path/to/blender.
set -e
cd "$(dirname "$0")"
BL="${BLENDER:-blender}"

FRAME_START=1    FRAME_END=360  "$BL" -b --python build_roblox_obby.py > chunk1.log 2>&1 &
FRAME_START=361  FRAME_END=720  "$BL" -b --python build_roblox_obby.py > chunk2.log 2>&1 &
FRAME_START=721  FRAME_END=1080 "$BL" -b --python build_roblox_obby.py > chunk3.log 2>&1 &
FRAME_START=1081 FRAME_END=1440 "$BL" -b --python build_roblox_obby.py > chunk4.log 2>&1 &
wait
echo "RENDER CHUNKS DONE"
ls frames/ | wc -l
