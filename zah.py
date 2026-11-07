#!/usr/bin/env python3
"""Zah Studio — working software for making 60-second videos.

A small command-line tool. It needs only Python 3 (no extra installs)
and ffmpeg (for joining clips). Everything works offline.

Commands:
    python3 zah.py check              check ffmpeg is installed
    python3 zah.py prompts            list the prompt sets in the repo
    python3 zah.py list               list your video projects
    python3 zah.py new <name> <idea>  start a new video project
    python3 zah.py join <name>        join the 6 clips into a 60s video

How a video is made:
    1. `new` makes a project folder with a prompts file.
    2. You make 6 clips of 10 seconds with your AI video tool,
       one prompt per clip, each continuing from the last clip.
    3. Put the clips in the project's clips/ folder as
       clip1.mp4 ... clip6.mp4 (or any 6 .mp4 files).
    4. `join` makes the finished 60-second video.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS_FILE = ROOT / "prompts" / "video-prompts.md"
VIDEOS_DIR = ROOT / "videos"

TEMPLATE = """# {name} — prompts

Idea: {idea}

Character (use the same line in every clip):
{character}

Keep every clip under ~60 words. One action per clip.
Natural sounds only, no music, no talking, no text on screen.

## Clip 1 — opening
Realistic handheld footage, filmed on a phone. {character}, {beat1}.
Natural sounds only. No music, no talking, no text.

## Clip 2 — look around
Continue the same scene: the same {character_short}, {beat2}.
Natural sounds only. No music, no talking, no text.

## Clip 3 — first task
Continue the same scene: the same {character_short}, {beat3}.
Natural sounds only. No music, no talking, no text.

## Clip 4 — turning point
Continue the same scene: the same {character_short}, {beat4}.
Natural sounds only. No music, no talking, no text.

## Clip 5 — wide shot
Continue the same scene: wide shot of the same {character_short}, {beat5}.
Natural sounds only. No music, no talking, no text.

## Clip 6 — ending
Continue the same scene: the same {character_short}, {beat6}.
Natural sounds only. No music, no talking, no text.
"""

DEFAULT_CHARACTER = ("a man in his early 30s, khaki shirt, dark trousers, "
                     "brown boots and a canvas backpack")


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    return 1


def run(cmd):
    """Run a command, return (ok, output)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        return proc.returncode == 0, (proc.stdout + proc.stderr).strip()
    except FileNotFoundError:
        return False, ""


def cmd_check(_args):
    ok, out = run(["ffmpeg", "-version"])
    if ok:
        print("ffmpeg: OK (" + out.splitlines()[0] + ")")
    else:
        print("ffmpeg: MISSING — install it to join clips (https://ffmpeg.org)")
        return 1
    ok, out = run(["ffprobe", "-version"])
    print("ffprobe: " + ("OK" if ok else "MISSING (duration check skipped)"))
    ok, out = run(["blender", "--version"])
    if ok:
        print("blender: OK (" + out.splitlines()[0] + ")")
    else:
        print("blender: not found (only needed for Blender scenes)")
    return 0


def prompt_sets():
    if not PROMPTS_FILE.exists():
        return []
    text = PROMPTS_FILE.read_text(encoding="utf-8")
    return re.findall(r"^## (.+)$", text, flags=re.M)


def cmd_prompts(_args):
    sets = prompt_sets()
    if not sets:
        return fail("no prompts found in prompts/video-prompts.md")
    print("Prompt sets in prompts/video-prompts.md:")
    for name in sets:
        print(f"  - {name}")
    print("\nOpen the file to copy a prompt set.")
    return 0


def cmd_list(_args):
    print("Video projects:")
    if VIDEOS_DIR.exists():
        projects = sorted(p for p in VIDEOS_DIR.iterdir() if p.is_dir())
    else:
        projects = []
    if not projects:
        print("  (none yet — make one with: python3 zah.py new <name> <idea>)")
    for proj in projects:
        clips = sorted((proj / "clips").glob("*.mp4")) if (proj / "clips").exists() else []
        done = proj.glob("*-60s.mp4")
        status = "done" if any(done) else f"{len(clips)}/6 clips"
        print(f"  - {proj.name} ({status})")
    return 0


def cmd_new(args):
    if len(args) < 2:
        return fail("usage: python3 zah.py new <name> <idea>\n"
                    "example: python3 zah.py new jungle-house "
                    "\"a man buys jungle land and builds a wooden house\"")
    name = args[0]
    idea = " ".join(args[1:])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
        return fail("name must use only letters, numbers, - and _")
    proj = VIDEOS_DIR / name
    if proj.exists():
        return fail(f"project '{name}' already exists")
    (proj / "clips").mkdir(parents=True)
    character = DEFAULT_CHARACTER
    short = "the same man"
    prompts = TEMPLATE.format(
        name=name, idea=idea, character=character, character_short=short,
        beat1="walks into the scene and the story starts",
        beat2="stops and looks around the place",
        beat3="does something with his hands",
        beat4="something changes",
        beat5="the full place is shown",
        beat6="walks on and the story closes",
    )
    (proj / "prompts.md").write_text(prompts, encoding="utf-8")
    print(f"Created project '{name}' in {proj}")
    print("Next steps:")
    print("  1. Open prompts.md and fill in the 6 clips.")
    print("  2. Make 6 clips of 10 seconds with your AI video tool.")
    print("  3. Put them in clips/ as clip1.mp4 ... clip6.mp4.")
    print(f"  4. Run: python3 zah.py join {name}")
    return 0


def cmd_join(args):
    if len(args) < 1:
        return fail("usage: python3 zah.py join <name>")
    name = args[0]
    proj = VIDEOS_DIR / name
    if not proj.exists():
        return fail(f"no project named '{name}' (see: python3 zah.py list)")
    clips_dir = proj / "clips"
    if not clips_dir.exists():
        return fail(f"no clips folder in {proj}")
    clips = sorted(clips_dir.glob("*.mp4"))
    if len(clips) != 6:
        found = ", ".join(c.name for c in clips) or "(none)"
        return fail(f"need exactly 6 clips, found {len(clips)}: {found}")
    out = proj / f"{name}-60s.mp4"
    concat_file = proj / "clips.txt"
    concat_file.write_text(
        "".join(f"file '{c.resolve()}'\n" for c in clips), encoding="utf-8")
    ok, err = run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
        str(out),
    ])
    if not ok:
        return fail("ffmpeg failed to join the clips:\n" + err)
    duration = None
    ok, probe = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(out),
    ])
    if ok:
        try:
            duration = float(probe.strip())
        except ValueError:
            duration = None
    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"Done: {out}")
    print(f"Duration: {duration:.2f}s" if duration else "Duration: unknown")
    print(f"Size: {size_mb:.1f} MB")
    if duration and abs(duration - 60.0) > 1.0:
        print("Note: not 60 seconds — check that every clip is 10 seconds.")
    return 0


COMMANDS = {
    "check": (cmd_check, "check ffmpeg is installed"),
    "prompts": (cmd_prompts, "list the prompt sets in the repo"),
    "list": (cmd_list, "list your video projects"),
    "new": (cmd_new, "start a new video project"),
    "join": (cmd_join, "join the 6 clips into a 60s video"),
}


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__.strip())
        print("\nCommands:")
        for name, (_, desc) in COMMANDS.items():
            print(f"  {name:<8} {desc}")
        return 0
    func, _ = COMMANDS.get(argv[1], (None, None))
    if func is None:
        print(f"Unknown command: {argv[1]}", file=sys.stderr)
        return 1
    return func(argv[2:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
