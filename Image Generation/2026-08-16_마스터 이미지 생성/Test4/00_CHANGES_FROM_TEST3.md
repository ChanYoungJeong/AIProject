# Test4 - changes from Test3

Source: `Test3/CLAUDE_QC_NEW_BATCH_UPDATED_2026-08-16.md` (supersedes the original
`CLAUDE_QC_NEW_BATCH_2026-08-16.md` for the same batch).

References unchanged - same 8 images, same order, same roles.

## Why Test4 instead of continuing the staged-correction chain

After the updated QC came in, the plan was originally two chained i2i correction passes
(`Correction1_Outfit/` then `Correction2_Skin/`, staged per `canonical/prompt_lab/
HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` §2-§3.4). The user put both on hold and asked for
this to go through a new master-build round (Test4) instead. Those two folders are left in
place, marked on hold, in case Test4 does not fully resolve the outfit issue and a narrower
follow-up pass is still useful.

## What changed this round (revised - see below)

**First draft of this round** added an outcome constraint ("left and right sides must match
exactly...") and a reference-conflict precedence rule to OUTFIT, on the theory that a third
reword needed to state something genuinely new (§1.1 escalation rule) rather than repeat Test3's
guard. That draft is preserved in git history / conversation log but was superseded before being
run - see next section.

**Final version - removed outfit description text entirely, not just reworded it.** The user
flagged, independently of the above, that the garment still comes out slightly different from
Image 8 even with a short categorical description, and asked for all outfit description to be
removed from the prompt so the image reference alone controls it. This is the same §1.1 theory
taken to its logical endpoint: even Test1's original "short and categorical" register (`"garment
type, neckline, straps, seams, fabric, texture, color, length"`) still got only "imperfect but
recognizable" transfer, and every version since (including this round's first draft) kept
itemizing some property of the garment in words. Removing the itemization entirely is an
untested, more extreme point on the same axis, not a new mechanism.

**Removed from OUTFIT:** the itemized property list (garment type, neckline, straps, seams,
fabric, texture, color), the left/right-match outcome sentence, the reference-conflict
precedence rule, and the separate "Three pieces, all required, none merged" numbered list
(itself a text description of the garment's composition - the most literal form of "describing
the outfit"). Also dropped "uneven garment sides" from the Avoid list since it restated the
now-removed symmetry sentence.

**Kept in OUTFIT:** only role assignment and boundary-setting, neither of which describes what
the garment looks like: "Image 8 is the exact garment reference. Reproduce it exactly and
unchanged, with no redesign, simplification, or reinterpretation. Do not copy Image 8's body,
pose, or silhouette - only the garment. Do not let Images 5-7 alter the garment in any way;
transfer it exactly onto the body from Images 5-7." "No extra accessories or props." stayed as
its own short line - a boundary, not a description.

**Known risk of this change:** the removed three-piece list existed specifically because Test1-3
QC never complained about missing pieces while it was present - there's no equivalent evidence
yet for whether Image 8 alone reliably keeps all three pieces (bodysuit + shorts + stockings)
without that reinforcement. Watch Test4's result specifically for a dropped or merged piece, not
just left/right fidelity; if a piece goes missing, the fix is to reintroduce a bare piece-count
fact ("three pieces, base layer plus two more"), not full itemized descriptions again.

**Word choice note (still applies to the surviving text):** avoided the word "symmetrical"
anywhere near OUTFIT, since PHYSICS uses that exact word for the opposite intent ("mild
asymmetry - not perfectly round, symmetrical, or molded" for the chest) - using one word for a
wanted trait in one clause and an avoided trait in another risks its own text-conditioning
ambiguity, independent of §1.1's dilution finding.

**Everything else - left untouched.** SKIN's genre-anchoring register (Test3's own change) had
only one real trial so far and wasn't diagnosed as a systematic failure this round - Result 2's
speckling was classified "likely single-seed anomaly," and Result 3's only remaining note was
"residual AI-beauty smoothness," not a hard failure. No escalation trigger for SKIN yet, so
rewording it again this round would just add dilution risk (per §1.1's corollary) without
evidence it's needed. PHYSICS, BODY, FACE, POSE, and SCENE are all unchanged - none were
flagged as regressed in the updated QC.

## If Test4's outfit fix still doesn't hold

Per the escalation rule, the next lever is not a fourth version of the OUTFIT paragraph.
Options, in order of how contained the change is:
1. Model swap for the master-build step (Seedream 5 Lite) - untested for this specific
   contamination mechanism, but it's the structural lever the project already has evidence for
   in a related dimension (§4).
2. Drop Images 6-7 (secondary body angle references) from this call entirely, keeping only
   Image 5 for body shape - reduces how many body-shape signals compete with the outfit
   reference. Test3's own changes doc assumed source selection wasn't the problem, but that was
   carried over from Test2 as an assumption, never actually tested in isolation.
3. Fall back to the staged-correction chain that's currently on hold (`Correction1_Outfit/` →
   `Correction2_Skin/`) - image-to-image, re-attaching the actual outfit reference image
   directly, rather than relying on text to prevent contamination during from-scratch
   generation at all.

## Length

2655 / 3000 characters, pure ASCII, `scripts/prompt_check.py` PASS, no WARN, no duplicate
phrases - checked before this file was presented. Shorter than Test3 (2792) and the first draft
of this round (2999) despite this being the fourth master-build attempt, because removing the
OUTFIT itemization freed more room than any of this round's additions used.

## Judge Test4 on

1. Outfit: does the garment now match Image 8 closely (not just left/right symmetry, but overall
   fidelity to the specific reference) - this is the primary thing this round is testing, and
   the user's own stated bar ("정확하게 복사해와야해")
2. Whether all three pieces (bodysuit, denim shorts, fishnet stockings) are still present and
   distinct without the itemized list - the specific risk this round's change introduces
3. Whether removing the OUTFIT text costs PHYSICS or SKIN any quality, the way Test2's expansion
   cost PHYSICS last time in the opposite direction (§1.1 corollary) - compare against Test3
4. Skin: should be no worse than Test3 (not the focus of this round's changes)
5. Chest physics: should be no worse than Test3 (preserve)
6. Face/hair/anatomy stability: unchanged from Test1-3 (must not regress)
