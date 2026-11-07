# Video prompts

Ready-to-use prompts for the AI video tool. Each video is 6 clips of
10 seconds, chained: clip 1 starts fresh, each next clip continues from
the previous clip's last frame (`resume_from_snapshot_id`).

Rules that were learned the hard way:
- Keep each prompt SHORT (under ~60 words). Long prompts fail with
  `invalid_args`. Say the same thing in fewer words.
- Describe the same person the same way in every clip (clothes, colors,
  backpack) so the character stays the same.
- One action per clip. A new clip = the next small step of the story.
- Natural sounds only, no music, no talking, no text on screen —
  unless the video needs a voice.
- The tool makes at most 6 videos per request (6 x 10s = 60s).

---

## Master prompt — script generation

`master-prompt-script-generation.txt` is a 17-section prompt that
turns one topic into a high-retention YouTube script (dark psychology
for success). Feed it a topic, get a full script back.

---

## Blank template — make your own 60-second video

Copy this, fill in the brackets, keep every clip under ~60 words.
Use the same character line in all 6 clips so the person stays
the same.

Character (use in every clip):
"[age], [shirt], [trousers], [shoes], [backpack or item].
Realistic handheld phone footage."

1. Opening — the character arrives / the story starts:
   "Realistic handheld footage, filmed on a phone. [CHARACTER],
   [what he does first, where he is]. [2-3 details of the place].
   Camera [follows him from behind / stays close]. Natural sounds
   only: [birds, footsteps, ...]. No music, no talking, no text."

2. Look around — he takes in the place:
   "Continue the same scene: the same [CHARACTER], [what he does
   next, one action]. [2 details of the place]. Camera [follows /
   stays close], handheld phone footage. Natural sounds only: [...].
   No music, no talking, no text."

3. First task — he does something with his hands:
   "Continue the same scene: the same [CHARACTER], [one clear
   action with his hands]. [1-2 details]. Handheld phone footage,
   close on his hands. Natural sounds only: [...]. No music, no
   talking, no text."

4. Turning point — something changes:
   "Continue the same scene: the same [CHARACTER], [the change:
   he finds something / finishes something / the light changes].
   [1-2 details]. Handheld phone footage. Natural sounds only:
   [...]. No music, no talking, no text."

5. Wide shot — the full picture:
   "Continue the same scene: wide shot of the same [CHARACTER],
   [what the wide shot shows]. [2 details of the place]. Handheld
   phone footage. Natural sounds only: [...]. No music, no talking,
   no text."

6. Ending — he walks on / the story closes:
   "Continue the same scene: the same [CHARACTER], [final action:
   he walks on / looks back / smiles]. [1 detail]. Camera follows
   from behind, handheld phone footage. Natural sounds only: [...].
   No music, no talking, no text."

## Tips

- One action per clip. If a clip tries to do two things, split it.
- Say the place in 2-3 details only (trees, light, ground).
  More detail makes the tool change the scene.
- End every prompt with the same sound line:
  "Natural sounds only: [...]. No music, no talking, no text."
- If a clip comes out wrong, do not fix it by editing — make a new
  clip from the last good frame with a shorter prompt.
