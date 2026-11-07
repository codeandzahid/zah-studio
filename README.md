# Zah Studio

Working software for making 60-second videos. One tool, one repo.
Clone it on any computer — laptop or cloud — and start.

## What's inside

| File | What it is |
|---|---|
| `zah.py` | The tool. Makes video projects, joins clips, and renders the Zack D.-style 3D video. |
| `zah` | Short way to run the tool: `bash zah <command>`. |
| `blender/zack-d/` | The Zack D.-style 3D scene: a money tree that grows, with gold coins. Blender only. |
| `prompts/video-prompts.md` | Ready prompts for realistic 60-second videos, plus a blank template. |
| `prompts/master-prompt-script-generation.txt` | A 17-section prompt that turns one topic into a high-retention YouTube script. |

## How to use it

You need Python 3 and ffmpeg. Check first:

```bash
bash zah check
```

### 1. Start a new video

```bash
bash zah new my-first-video "a man walks through the city"
```

This makes a folder `videos/my-first-video/` with a `prompts.md`
file (6 clip prompts, already filled in) and an empty `clips/` folder.

### 2. Make the clips

Open `videos/my-first-video/prompts.md` and change the 6 prompts
if you want. Then make 6 clips of 10 seconds with your AI video
tool — one prompt per clip, each clip continuing from the last one.
Put them in `videos/my-first-video/clips/` as `clip1.mp4` to `clip6.mp4`.

### 3. Join them into one video

```bash
bash zah join my-first-video
```

You get `videos/my-first-video/my-first-video-60s.mp4` — 60 seconds,
ready to watch and upload.

## Make a Zack D.-style 3D video

A Blender scene that makes a video like Zack D. Films: a money
tree grows, gold coins appear on its branches one by one, a man
stands watching, and the camera slowly moves around the tree.
The finance idea, shown in 3D, not flat bars.

```bash
bash zah zackd         # 10 second version (240 frames)
bash zah zackd 1440    # 60 second version
```

You need Blender (free, blender.org) and ffmpeg. The video comes
out in `blender/zack-d/` as `money-tree-10s.mp4` or
`money-tree-60s.mp4`.

Honest limit: this is the simple 3D version. Zack D. Films uses
a team of 50+ people, Cascadeur for character movement, EmberGen
for smoke and fire, and After Effects to finish. This scene is
Blender only, so the man is simple and the tree is low-poly. It
looks like his idea, not his full quality.

## Other commands

```bash
bash zah prompts   # list every prompt set in the repo
bash zah list      # list your video projects and how many clips each has
bash zah check     # check ffmpeg is installed
```

## How a 60-second video works

Every video is 6 clips of 10 seconds, chained together.
Keep each prompt short — under ~60 words — or the tool rejects it.
Describe the same person the same way in every clip (clothes,
colors, backpack) so he stays the same. One action per clip.
Natural sounds only — no music, no talking, no text on screen —
unless the video needs a voice.

## Write a script

Feed a topic to the master prompt in
`prompts/master-prompt-script-generation.txt`.
You give it a topic (for example: "dark psychology for success")
and it writes a full high-retention YouTube script in 17 parts.

## Offline?

The tool, the prompts, and the script prompt are plain files —
they work anywhere, no internet needed. Joining clips needs only
ffmpeg on your computer. The AI video tool itself needs an
internet connection to make the clips.
