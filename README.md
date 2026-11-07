# Zah Studio

One repo with everything used to make the videos: ready prompts
and a script writer. Clone it on any computer —
laptop or cloud — and start making videos.

## What's inside

| Folder | What it is |
|---|---|
| `prompts/video-prompts.md` | Ready prompts for realistic 60-second videos, plus a blank template to make your own. |
| `prompts/master-prompt-script-generation.txt` | A 17-section prompt that turns one topic into a high-retention YouTube script. |
| `zah.sh` | Small helper: checks your tools and lists the prompts. |

## Quick start

```bash
git clone https://github.com/codeandzahid/zah-studio.git
cd zah-studio
bash zah.sh check     # makes sure ffmpeg is installed
bash zah.sh prompts   # lists every prompt set in the repo
```

## Make a realistic 60-second video

Every video is 6 clips of 10 seconds, chained together:

1. Pick a prompt set from `prompts/video-prompts.md`
   (jungle walk, or jungle property series Episode 1),
   or write your own with the blank template in the same file.
2. Make clip 1 from its prompt in your AI video tool.
3. Make clips 2-6 the same way, each one continuing from the
   previous clip's last frame (`resume_from_snapshot_id`).
   Keep each prompt short — under ~60 words — or the tool rejects it.
4. Join the 6 clips in order with ffmpeg:

```bash
ffmpeg -y -f concat -safe 0 -i clips.txt \
  -c:v libx264 -pix_fmt yuv420p -crf 20 \
  -c:a aac -b:a 128k -movflags +faststart my-video-60s.mp4
```

(`clips.txt` lists the 6 clip files, one `file 'clip1.mp4'` line each.)

## Write a script

Feed a topic to the master prompt:

1. Open `prompts/master-prompt-script-generation.txt`.
2. Give it your topic (for example: "dark psychology for success").
3. It returns a full high-retention YouTube script in 17 sections.

## Rules that were learned the hard way

- Keep prompts SHORT. Long prompts fail.
- Describe the same person the same way in every clip
  (clothes, colors, backpack) so the character stays the same.
- One action per clip. A new clip = the next small step of the story.
- Natural sounds only — no music, no talking, no text on screen —
  unless the video needs a voice.
- The AI video tool makes at most 6 videos per request
  (6 x 10s = 60s). A longer video needs a new request.

## Offline?

The prompts, the script prompt, and the style guide are plain text —
they work anywhere, no internet needed to read and use them.
The AI video tool itself needs an internet connection to generate clips.
