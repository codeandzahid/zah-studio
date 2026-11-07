# Roblox Obby — Blender viral gameplay

A classic blocky Roblox noob (yellow head/arms, blue torso, green legs)
runs and jumps across a 60-platform rainbow obby course over lava, past
spinning gold coins and checkpoint flags, to a gold finish arch.
60 seconds, 24 fps, 1440 frames. Delivered as a 4K file.

## What it makes

- Roblox-style gameplay: run + jump every second, one platform per second
- Colorful obby platforms, lava floor, coins, flags, finish arch
- Game sounds made by `gen_sfx.py` (jump boings, coin dings, fanfare)
- Final video upscaled to 3840x2160 (4K) with ffmpeg

## Run it

```bash
# 1. Test one frame first (fast, checks the look)
blender -b --python build_roblox_obby.py -- --test

# 2. Render all frames (4 chunks in parallel, ~10-15 min on 4 CPUs)
bash render.sh

# 3. Join frames + sounds, upscale to 4K
bash assemble.sh
```

Result: `roblox-obby-4k-60s.mp4` (3840x2160, 60s).

## Notes

- Rendered at 960x540, then upscaled to 4K. True 4K rendering in
  Blender is far too slow on a normal computer — upscaling is the
  practical way to get a 4K file.
- Eevee was tested and is ~68 seconds per frame on a CPU-only machine
  (software rendering) — unusable for a full minute. Workbench is the
  fast engine here (~1 second per frame).
- Workbench shows material colors from `diffuse_color`, NOT from the
  Principled BSDF node color — the script sets both.
- Blender 5.2: the Eevee engine enum is `BLENDER_EEVEE` (not
  `BLENDER_EEVEE_NEXT`), and the setting is `use_shadows`
  (not `use_soft_shadows`).
- If chunks save the same `.blend` at once, one can fail with
  "Cannot change old file" — just re-run that chunk alone.
