# Zah Studio

Working software for making 60-second videos. One tool, one repo.
Clone it on any computer — laptop or cloud — and start.

## What's inside

| File | What it is |
|---|---|
| `zah.py` | The tool. Makes video projects and joins clips into a 60-second video. |
| `zah` | Short way to run the tool: `bash zah <command>`. |
| `prompts/video-prompts.md` | Ready prompts for realistic 60-second videos, plus a blank template. |
| `prompts/master-prompt-script-generation.txt` | A 17-section prompt that turns one topic into a high-retention YouTube script. |

## How to use it

You need Python 3 and ffmpeg. Check first:

```bash
bash zah check
```

### 1. Start a new video

```bash
bash zah new jungle-house "a man buys jungle land and builds a wooden house"
```

This makes a folder `videos/jungle-house/` with a `prompts.md`
file (6 clip prompts, already filled in) and an empty `clips/` folder.

### 2. Make the clips

Open `videos/jungle-house/prompts.md` and change the 6 prompts
if you want. Then make 6 clips of 10 seconds with your AI video
tool — one prompt per clip, each clip continuing from the last one.
Put them in `videos/jungle-house/clips/` as `clip1.mp4` to `clip6.mp4`.

### 3. Join them into one video

```bash
bash zah join jungle-house
```

You get `videos/jungle-house/jungle-house-60s.mp4` — 60 seconds,
ready to watch and upload.

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
