# Wardrobe - outfit masters

Each subfolder is one finished "outfit master": the character's canonical identity/body
(FACE ID MASTER + CHARACTER MASTER + BODY MASTER) combined with one specific, locked outfit,
generated with the recipe validated in `Image Generation/2026-08-16_마스터 이미지 생성/Test8/`
(`00_PROMPT.txt`, quality: basic, Seedream 4.5).

This is distinct from the three identity masters in `../masters/` - per
`canonical/workflow/00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt` §4, "clothing visible in any
master is never canonical wardrobe." A wardrobe entry is the opposite: identity/body stays fixed,
the outfit is the whole point. Downstream generations that need this specific outfit reference
`MASTER.png` directly (per Workflow Master's Outfit Policy, `WARDROBE` mode or the simpler
CASE_02/03-style single-master pattern) rather than re-deriving the outfit from scratch.

## Entries

### 01_casual_white_tee_gray_shorts
- `MASTER.png` - white scoop-neck fitted tee + gray athletic shorts. Picked from Test8's
  validation batch (`Test8/Result/Result.png`) as the result to carry forward.
- First used in: `Image Generation/2026-08-17_상황 레퍼런스 확장/Test1/` (studying-at-desk Daily
  Reference scene).

## Adding a new entry

1. Run the Test8 recipe (`Image Generation/2026-08-16_마스터 이미지 생성/Test8/00_PROMPT.txt`)
   with the new outfit reference in Image 8's slot.
2. Pick the best result from the batch.
3. New subfolder here, numbered next in sequence, named for the outfit in plain English.
4. Copy the chosen image in as `MASTER.png`, add an entry to this list.

## Known gap

The original production outfit (bodysuit + denim shorts + fishnet stockings,
`assets/outfit/OUTFIT_BODYSUIT_DENIM_FISHNET_v1.png` - the whole reason Test1-8 exist) does not
have a picked wardrobe entry yet. Every Test7/Test8 comparison shown so far used swapped
diagnostic outfit references (sports bra, blazer, henley, black shirt, white tee) to stress-test
fidelity, not the actual production asset. Run the Test8 recipe against
`OUTFIT_BODYSUIT_DENIM_FISHNET_v1.png` and add `00_bodysuit_denim_fishnet/` once there's a picked
result.
