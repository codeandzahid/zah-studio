# Video Studio

One repo with everything used to make the videos: Blender scenes that
render fully offline, and the prompts for the realistic AI videos.
Clone it on any computer — laptop or cloud — and make videos.

## What's inside

| Folder | What it is |
|---|---|
| `blender/jungle-walk/` | Blender: a man walks a jungle path. 60s, Workbench render. |
| `blender/roblox-obby/` | Blender: Roblox noob runs a rainbow obby over lava. 60s, 4K file. |
| `prompts/video-prompts.md` | Ready prompts for realistic videos (jungle walk, jungle property series Ep 1). |
| `prompts/master-prompt-script-generation.txt` | 17-section prompt that turns a topic into a high-retention YouTube script. |
| `docs/zack-d-style.md` | The Zack D. Films 3D-simulation style guide (Blender + After Effects + Cascadeur + EmberGen). |

## Use it on a local or cloud computer

```bash
# 1. Get the repo
git clone https://github.com/codeandzahid/video-studio.git
cd video-studio

# 2. Install Blender (free) — https://www.blender.org/download/
#    Blender 5.2 or newer. No other install needed.

# 3. Make a video, for example the Roblox obby:
cd blender/roblox-obby
blender -b --python build_roblox_obby.py -- --test   # one test frame
bash render.sh                                        # all 1440 frames
bash assemble.sh                                      # 4K video with sounds
```

## Offline?

- **Blender scenes: fully offline.** Once Blender is installed, the
  scripts need no internet at all. They build the scene, render the
  frames, and ffmpeg joins them into a video.
- **AI video prompts: need an online video tool.** The prompts in
  `prompts/` are text — paste them into any AI video generator that
  supports continuing from a previous clip. The Blender parts do not
  need this.
- **Cloud computers:** system packages (like the EGL libraries Blender
  needs for headless rendering) do NOT survive a VM rebuild. If a
  render fails with `libEGL.so.1: cannot open shared object file`,
  re-install them: `sudo apt install libegl1 libgl1 libgl1-mesa-dri`

## How the videos are made

- **Blender videos:** a Python script builds the whole 3D scene
  (character, world, camera, walk/run animation) and renders 1440
  frames at 960x540. Four chunks run in parallel. ffmpeg joins the
  frames, adds sound, and upscales to 4K where asked.
- **Realistic videos:** 6 clips of 10 seconds from the AI video tool,
  each continuing from the previous clip's last frame, joined into
  60 seconds. Prompts stay short — long prompts fail.

## Notes

- True 4K rendering in Blender is far too slow on a normal computer.
  The practical way to a 4K file is: render small, upscale with ffmpeg.
- Blender 5.x notes are in each scene's README (world creation,
  drivers instead of keyframes, Workbench colors, Eevee limits).
