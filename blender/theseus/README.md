# Ship of Theseus — Zack D. style (original remake)

An original Blender remake of the Zack D. Films Short "The Ship Of
Theseus Paradox": a man on a bright blue background with a grid
floor. His layers come off one by one — skin, then muscle, then
skeleton — and at the end he is put back together. Vertical 9:16,
big word captions, close camera, voiceover.

## What it is

- `build_theseus.py` — builds the scene and renders frames.
  - 4 acts (24 fps): skin man close-up (1–130, eyeballs float out
    of the sockets above the forehead) → muscle man (131–300) →
    skeleton + a pile of the removed layers on the floor (301–460)
    → skin man back, whole again, name tag showing (461–528).
  - Blue world background, light-blue grid floor (brick texture),
    soft studio light aimed at the man (TRACK_TO), no cast shadows.
  - 540x960 Eevee, TAA 4. Bodies are joined into one mesh each
    (fast) — see the driver note below.
- `render.sh [frames]` — renders in 2 parallel chunks (never 4).
  Default 528 frames = 22 s.
- `assemble.sh` — joins frames, upscales to 1080x1920, adds the
  big white word captions (one word at a time, from the narration),
  mixes the voiceover (`narration.mp3`, sped to fit 22 s).
  Output: `theseus-22s.mp4`.
- `narration.mp3` — the narration, TTS voice avocado_v2:Twenty.

## Run it

```bash
bash render.sh        # ~35-50 min for 528 frames (2 chunks)
bash assemble.sh      # makes theseus-22s.mp4
```

## Lessons (do not repeat)

- `primitive_cube_add` makes a 2x2x2 cube — halve the scale in
  `add_box`, or every box comes out twice the intended size.
- `join_parts` bakes the parent empty's CURRENT scale into the
  geometry. Add the scale drivers AFTER the join, or a body whose
  driver is 0 at frame 1 collapses to a single point and renders
  invisible.
- Legs are 1.18 long from the hip at z 0.62, so the feet land at
  z -0.56 (under the floor). The body empties sit at z +0.56.
- A portrait render fits the sensor vertically, so a 50mm lens is
  very zoomed in — use 35mm for close-ups.
- Text facing the camera needs rotation (90, 0, 180) or it reads
  mirrored.
- The sun must TRACK_TO the man. A sun behind him lights his back
  and the blue world light turns his skin grey-blue.
