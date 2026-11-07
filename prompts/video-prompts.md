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

## Realistic jungle walk (60s)

The same man throughout: early 30s, khaki shirt, dark trousers,
brown boots, canvas backpack. Realistic handheld phone footage.

1. "Realistic handheld footage, filmed on a phone. A man in his early 30s, khaki shirt, dark trousers, brown boots and a canvas backpack, walks away from the camera along a narrow dirt path through dense tropical jungle. Tall trees, thick green leaves, vines and ferns on both sides. Soft morning sunlight comes through the leaves in patches. The camera follows him from behind at walking pace, steady. He walks at a normal pace, arms swinging naturally. Natural jungle sounds only: birds singing, leaves rustling, his footsteps on dry leaves. No music, no talking, no text on screen."

2. "Continue the same walk: the same man, khaki shirt, dark trousers, brown boots and canvas backpack, keeps walking away from the camera along the same dirt path through dense tropical jungle. The path bends gently left. He steps over a small fallen branch. Tall trees, green leaves, vines and ferns. Morning sunlight through the leaves. Camera follows from behind at walking pace, handheld phone footage. Natural jungle sounds only: birds, rustling leaves, footsteps on dry leaves. No music, no talking, no text."

3. "Continue the same walk: the same man, khaki shirt, dark trousers, brown boots and canvas backpack, keeps walking away from the camera along the same dirt path through dense tropical jungle. The path reaches a small shallow stream. He steps across it carefully on flat stones, then walks on. Tall trees, green leaves, vines and ferns. Morning sunlight through the leaves. Camera follows from behind at walking pace, handheld phone footage. Natural jungle sounds only: birds, rustling leaves, footsteps, gentle water. No music, no talking, no text."

4. "Continue the same walk: the same man, khaki shirt, dark trousers, brown boots and canvas backpack, keeps walking away from the camera along the same dirt path through dense tropical jungle. The path opens into a small clearing where bright sunbeams cut through the trees, then narrows back into shade. Tall trees, green leaves, vines and ferns. Camera follows from behind at walking pace, handheld phone footage. Natural jungle sounds only: birds, rustling leaves, footsteps on dry leaves. No music, no talking, no text."

5. "Continue the same walk: the same man, khaki shirt, dark trousers, brown boots and canvas backpack, keeps walking away from the camera along the same dirt path through dense tropical jungle. The path climbs a gentle slope with thick tree roots across it. He steps over the roots and keeps walking. Tall trees, green leaves, vines and ferns, denser shade. Camera follows from behind at walking pace, handheld phone footage. Natural jungle sounds only: birds, rustling leaves, footsteps on dry leaves and roots. No music, no talking, no text."

6. "Continue the same walk: the same man, khaki shirt, dark trousers, brown boots and canvas backpack, keeps walking away from the camera along the same dirt path through dense tropical jungle. The trees open ahead to a wide view of a green valley far below. He slows, looks at the view for a moment, then keeps walking on. Tall trees, green leaves, vines and ferns. Camera follows from behind at walking pace, handheld phone footage. Natural jungle sounds only: birds, rustling leaves, footsteps on dry leaves. No music, no talking, no text."

Join the 6 clips in order (plain cuts — each starts where the last
ended), 60 seconds total.

---

## Jungle property series — Episode 1: Buying the Land (60s)

Same man as the jungle walk. A series about buying jungle property,
building a wooden house on it, upgrading it, and making paths.
Planned episodes: 1. Buying the land, 2. Clearing the land,
3. Building the wooden house, 4. Upgrades, 5. Making paths.

1. "Realistic handheld footage, filmed on a phone. A man in his early 30s, khaki shirt, dark trousers, brown boots and a canvas backpack, walks into dense tropical jungle on a faint trail, pushing leaves aside. Tall trees, thick green leaves, vines and ferns. Morning sunlight through the leaves. Camera follows him from behind at walking pace. Natural jungle sounds only: birds, rustling leaves, footsteps. No music, no talking, no text."

2. "Continue the same scene: the same man stops in a small open space in the jungle and looks around the wild land, turning slowly. He touches a big tree trunk with one hand. Tall trees, green leaves, vines and ferns. Morning sunlight. Camera stays close, handheld phone footage. Natural jungle sounds only: birds, rustling leaves. No music, no talking, no text."

3. "Continue the same scene: the same man kneels on the jungle ground and checks the soil with his hands, picking up a handful of dark earth and letting it fall. Tall trees and ferns around him. Morning sunlight. Handheld phone footage, close on his hands. Natural jungle sounds only: birds, rustling leaves. No music, no talking, no text."

4. "Continue the same scene: the same man hammers a small wooden sign into the jungle ground with a rock, then steps back and looks at it. The sign marks his new land. Tall trees, green leaves, ferns. Morning sunlight. Handheld phone footage. Natural jungle sounds only: birds, hammering, rustling leaves. No music, no talking, no text."

5. "Continue the same scene: wide shot of the same man standing on his jungle land as sun breaks through the trees, hands on hips, looking over the wild ground he now owns. Tall trees, green leaves, vines and ferns. Handheld phone footage. Natural jungle sounds only: birds, rustling leaves. No music, no talking, no text."

6. "Continue the same scene: the same man walks deeper into his jungle land with a smile, a new beginning, pushing leaves aside as the trail opens ahead. Tall trees, green leaves, vines and ferns. Morning sunlight. Camera follows from behind, handheld phone footage. Natural jungle sounds only: birds, rustling leaves, footsteps. No music, no talking, no text."

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
