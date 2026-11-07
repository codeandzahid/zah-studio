#!/bin/bash
# Zah Studio helper.
#   bash zah.sh check    — check the tools you need are installed
#   bash zah.sh prompts  — list every prompt set in the repo
#   bash zah.sh help     — show this help
set -e
cd "$(dirname "$0")"

cmd="${1:-help}"
case "$cmd" in
  check)
    echo "Checking tools..."
    if command -v ffmpeg >/dev/null 2>&1; then
      echo "ffmpeg: OK ($(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}'))"
    else
      echo "ffmpeg: MISSING — install it to join clips (https://ffmpeg.org)"
    fi
    if command -v blender >/dev/null 2>&1; then
      echo "blender: OK ($(blender --version 2>/dev/null | head -1))"
    else
      echo "blender: not found (only needed for Blender scenes, https://www.blender.org/download/)"
    fi
    ;;
  prompts)
    echo "Prompt sets in prompts/video-prompts.md:"
    grep -E '^## ' prompts/video-prompts.md
    echo ""
    echo "Open the file to copy a prompt set."
    ;;
  help|*)
    echo "Zah Studio helper"
    echo "  bash zah.sh check    — check ffmpeg (and blender) are installed"
    echo "  bash zah.sh prompts  — list every prompt set in the repo"
    echo "  bash zah.sh help     — show this help"
    ;;
esac
