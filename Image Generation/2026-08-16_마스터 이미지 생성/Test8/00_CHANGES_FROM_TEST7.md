# Test8 - changes from Test7

Source: user's review of `Test7/result1.png` (ref1: cropped sports-bra photo with visible toned
abs) and `Test7/result2.png` (ref2: open blazer, no visible abs but a leaner overall build) -
"저 복근이나 저런걸 가져오는 걸 없애는 수정" (remove the thing where it brings over the abs/that
kind of thing).

References unchanged - same 8 images, same order, same roles.

## Distinguishing this from the exposure finding (§5.5) - not a reversal of it

This is a narrower, different fix from the exposure/coverage discussion in the previous round.
The user explicitly confirmed exposure level (how much skin shows, e.g. crop tops) should keep
transferring faithfully from the outfit reference - that stays unchanged in Test8. What should
**not** transfer is the reference model's own body *tone/definition* (visible abs, muscle
definition) when it differs from the character's own established physique. Concretely:

- Keep: if Image 8 is a crop top or low-cut design, the result should show that same amount of
  skin - unchanged from Test7.
- Fix: if Image 8's own model happens to have visible abs/muscle tone, that muscle definition
  should not appear on the character - the skin that shows should still read as Image 5's soft,
  non-muscular tone, not Image 8's.

Test7's BODY paragraph never separated these two things - "body shape" language (waist, hips,
bust) doesn't obviously cover skin/muscle *tone*, so there was nothing telling the model to keep
tone from Image 5 specifically when the outfit reference showed a toned physique underneath a
revealing cut.

## What changed this round

**BODY** - added tone alongside shape: "Image 5 shows ... soft, non-muscular skin - reproduce
this shape and tone even where Image 8 is more revealing or shows a different figure or visible
muscle definition." And extended the closing guard: "Image 8 must not change body shape **or
skin tone**" (was just "body shape" in Test7).

**OUTFIT** - two small, targeted additions, both following the same positive-then-negative
pattern already validated in this project (§8.1):
1. Positive: "...design details, including how much skin it reveals" - makes explicit that
   exposure/coverage is still meant to transfer (protects §5.5's settled decision from being
   accidentally undone by the new muscle-tone guard).
2. Negative: "Do not copy Image 8's body, pose, silhouette, **or muscle tone**" (was just "body,
   pose, or silhouette" in Test7).

**Avoid list** - added "visible abs or muscle definition" as the short negative reinforcement,
matching the same pattern used for hair (Test6) and outfit sides (earlier rounds).

**Everything else unchanged** - PHYSICS, SKIN, FACE, HAIR, POSE, SCENE, `quality: basic` all
stay as Test6/7 had them. This round isolates muscle tone/definition specifically.

## Length

2996 / 3000 characters, pure ASCII, `scripts/prompt_check.py` PASS, no WARN, no duplicate
phrases. Very little headroom left - trimmed several existing sentences (removed "either" after
"exaggerate...", shortened "the design itself reveals" to "it reveals", dropped a redundant "no
visible abs" clause already covered by the Avoid list) to make room for the new content instead
of just appending.

## Judge Test8 on

1. **Primary:** with a revealing/high-exposure outfit reference whose own model shows visible
   abs (like Test7's ref1), does the result still show Image 5's soft, non-muscular tone instead
   - this is what this round targets specifically.
2. **Confirm exposure/coverage still transfers as before** - a crop top or low-cut design should
   still show that same skin exposure (§5.5's settled behavior). If exposure suddenly drops back
   to conservative, the new BODY/OUTFIT wording overcorrected and needs rebalancing.
3. Everything else (outfit fidelity, body proportions/shape, hair, skin, chest physics) should
   be consistent with Test7 - not this round's target.
