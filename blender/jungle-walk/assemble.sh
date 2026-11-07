#!/bin/bash
# Assemble rendered frames into the 60s video with a soft wind bed.
set -e
cd "$(dirname "$0")"

ffmpeg -y -v error -f lavfi -i "anoisesrc=color=brown:duration=60" \
  -af "lowpass=f=300,volume=0.12" /tmp/ambience.wav

ffmpeg -y -v error -framerate 24 -i frames/frame_%04d.png -i /tmp/ambience.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a aac -b:a 96k -shortest \
  -movflags +faststart man-walking-jungle-60s.mp4

ffprobe -v error -show_entries format=duration,size \
  -of default=noprint_wrappers=1 man-walking-jungle-60s.mp4
echo ASSEMBLY_DONE
