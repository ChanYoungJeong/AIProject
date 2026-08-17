# Test7 - changes from Test6

Source: direct visual comparison the user ran - `Test6/Result.png` vs `Test6/Reference.webp`
(a swapped-in outfit reference, not the production bodysuit asset), cross-checked by Claude
against the actual body reference (`references/05_PRIMARY_BODY.png`).

References unchanged - same 8 images, same order, same roles.

## What the comparison showed

Outfit fidelity was good - collar, buttons, chest pocket, jean rivets/stitching all matched the
swapped reference closely. This confirms Test6's OUTFIT revert (back to Case 01's proven short
register, §1.2) is working.

Body shape did not match the character. Direct comparison against `05_PRIMARY_BODY.png` (which
shows a full bust, narrow waist, and pronounced hourglass under a fitted tank top) showed the
result's silhouette was noticeably flatter/more generic under the loose black shirt used in this
test.

## Why the production outfit reference can't diagnose this (the user's own point)

The user flagged something important before agreeing to a fix: testing this with the actual
production outfit reference (`08_OUTFIT_BODYSUIT_DENIM_FISHNET.png`) wouldn't be a clean test,
because that reference's own model already has a similar body shape to the character. If body
shape leaked from Image 8 instead of correctly coming from Images 5-7, the output would look
right either way - the two failure modes are indistinguishable with that reference. Swapping in
an outfit reference with a visibly different body (and a loose fit that reveals nothing about
the wearer's real shape) removes that confound: any body-shape drift under that reference can
only have come from the text instruction failing, not from image-based leakage, because there's
no strong body signal in that reference image to leak from.

This means the swapped-reference test the user ran is the more informative one for this specific
question, not a secondary "just in case" check - see the recommended validation approach below.

## Diagnosis

BODY's proportion clause was comparative and negative-framed: "Do not make the body slimmer or
more generic... no stronger bust projection, no narrower waist, no more pronounced hourglass
than Image 5 shows." With the original fitted bodysuit reference, Image 8 itself visually
reinforces the body shape, so this text only has to do part of the job. With a loose reference
that shows no body silhouette at all, this text has to carry the entire weight of keeping body
shape correct - and a comparative negative ("no more than X") is a weaker signal than a direct
positive statement of what the shape actually is (§8.1, applied here for the first time to BODY
rather than OUTFIT).

## What changed this round

**BODY only** - added one positive, concrete sentence naming the actual shape from Image 5,
kept short and categorical (not descriptive/argumentative, consistent with §1.1): "Image 5 shows
a full bust, a narrow waist, and a pronounced hourglass silhouette - reproduce this exact shape
even where Image 8 is loose-fitting or its own model has a different figure." The existing
comparative-negative sentence was kept, not replaced - per §8.1, the pattern is positive
statement first, negative as reinforcement, not a substitution of one for the other. The
anti-exaggeration half of that sentence stays too, since Test1-3's real QC history shows
over-exaggerated proportions was a genuine separate problem to guard against, not something to
drop just because under-shooting is this round's issue.

**Everything else unchanged from Test6** - OUTFIT (just confirmed working), PHYSICS/hair
addition (not yet evaluated by this comparison), SKIN, `quality: basic` all stay as-is. This
round isolates the one clause that was actually implicated.

## How to validate this fix properly

**Use `Test6/Reference.webp` as Image 8 for this run, not the production bodysuit** - per the
diagnosis above, the production reference can't tell us whether the fix worked. Once body shape
holds up under the diagnostic (loose, different-body) reference, that's real evidence the text
fix works; re-confirm with the actual production bodysuit reference afterward as a final check,
not as the primary test.

## Length

2869 / 3000 characters, pure ASCII, `scripts/prompt_check.py` PASS, no WARN, no duplicate
phrases.

## Judge Test7 on

1. **Primary:** with the diagnostic (loose/different-body) outfit reference, does the body now
   show Image 5's actual proportions (full bust, narrow waist, hourglass), not a generic/flatter
   figure
2. Outfit fidelity - should stay as good as Test6's result (this round didn't touch OUTFIT)
3. Hair physics, skin, chest physics - not this round's focus, should be consistent with Test6
