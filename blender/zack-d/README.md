# Zack D.-style 3D video — the growing money tree

A Blender scene that makes a video like Zack D. Films: a money
tree grows on green ground, gold coins appear on its branches one
by one, a man stands watching, and the camera slowly moves around
the tree. The finance idea, shown in 3D, not flat bars.

## Run it

```bash
bash render.sh     # 240 frames = 10 seconds (about 1 minute)
bash assemble.sh   # makes money-tree-10s.mp4
```

For a full 60 second video:

```bash
DEMO_FRAMES=1440 bash render.sh
DEMO_FRAMES=1440 bash assemble.sh   # makes money-tree-60s.mp4
```

Or from the repo root:

```bash
bash zah zackd          # 10 second version
bash zah zackd 1440     # 60 second version
```

You need Blender (free, blender.org) and ffmpeg. Set `BLENDER`
to your Blender file if it is not on your PATH.

## What it is, plainly

- The tree grows from half size to full size.
- Leaves pop in one by one. Coins pop in one by one and spin.
- The man fades in at the start and watches the tree.
- The camera turns around the tree while it grows.

## Honest limit

This is the simple 3D version. Zack D. Films uses a team of 50+
people, Cascadeur for character movement, EmberGen for smoke and
fire, and After Effects to finish. This scene is Blender only, so
the man is simple and the tree is low-poly. It looks like his
idea, not his full quality.
