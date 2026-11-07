# Jungle Walk — Blender demo

A low-poly man with a safari hat walks a dirt path through a procedural
jungle. 60 seconds, 24 fps, 1440 frames. Built with Blender's Workbench
renderer (fast, runs on any computer, no GPU needed).

## What it makes

- A man walking forward on a jungle path, camera following from behind
- 130 trees, bushes, rocks, a dirt path, sun light, shadows
- Soft wind sound added at assembly

## Run it

```bash
# 1. Test one frame first (fast, checks the look)
blender -b --python build_jungle_walk.py -- --test

# 2. Render all frames (4 chunks in parallel, ~10-15 min on 4 CPUs)
bash render.sh

# 3. Join frames + wind sound into the video
bash assemble.sh
```

Result: `man-walking-jungle-60s.mp4` (960x540, 60s).

## Notes

- Blender 5.x: `read_factory_settings(use_empty=True)` creates NO world,
  so the script creates one. Motion uses drivers, not keyframes
  (`action.fcurves` was removed in Blender 5.x).
- Headless Linux needs the EGL libraries or Workbench fails:
  `sudo apt install libegl1 libgl1 libgl1-mesa-dri`
  (re-install after a cloud VM is rebuilt — system packages do not survive).
- If chunks save the same `.blend` at once, one can fail with
  "Cannot change old file" — just re-run that chunk alone.
