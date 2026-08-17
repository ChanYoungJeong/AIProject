# Test3 — changes from Test2

Source: `Test2/CLAUDE_QC_CANDIDATE_2_2026-08-16.md`
Decision: **REVISE (current best base, not locked)**

References unchanged - same 8 images, same order. The problem is transfer/rendering, not
source selection.

## The actual diagnosis this round (not just "add more correction text")

Test2 made outfit fidelity *worse*, not better, despite adding more explicit correction
language ("not inspiration," itemized construction checklist, "same garment... not
redesigned"). Candidate #2's own QC: *"the system is reproducing the outfit concept, not
reliably preserving the specific garment design"* and *"BODY reference + OUTFIT reference +
model styling prior were blended together."* Skin/glamour also didn't improve on the second,
more forceful attempt either - "Excessive AI-Glamour Direction" is now the #1 HIGH finding.

This matches what the user flagged directly: adding more *text description* of what an image
reference already shows can compete with the image itself instead of reinforcing it, and for a
prompt meant for general master-building, over-describing the garment risks conflicting with
the fact that a real Outfit Reference image is already doing that job. Full writeup:
`canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` §1.1 (new, elevated to a core
principle, not just a pitfall).

## What changed this round

**OUTFIT - simplified back toward Case01's proven register, not expanded further.** Removed
the "not inspiration," itemized-construction-checklist, and "same garment... not redesigned"
sentences entirely - all interpretive/conceptual prose, not categorical fact. Kept a single
categorical sentence (garment type, neckline, straps, seams, fabric, texture, color - matches
Case01's original wording almost exactly) plus the numbered 3-piece list (proven to work in
both Test1 and Test2 - QC never complained about missing pieces, only about construction
fidelity within them, so it stayed).

**New: explicit cross-contamination guard.** Added "do not let Images 5-7 change the outfit's
cut, fit, or construction" as a plain fact, addressing Candidate #2's new finding that body
information was visibly leaking into the garment's shape. (prompt_lab §5.3, new)

**SKIN - rewritten with a different mechanism, not more of the same one.** Two rounds of
"describe photographic skin / argue against beauty-normalization" both failed on this exact
dimension. Escalation rule (prompt_lab §1.1): stop adding words to a dimension that's failed
twice, try something structurally different. This round uses genre-anchoring language
("amateur candid phone-camera quality, not a beauty campaign or glamour shoot") instead of
descriptive/argumentative language - a different lever, matching the register Case02/03's real
validated prompts actually used ("restrained vintage-digicam influence," not abstract
concepts). Added "glamour-shoot polish" and "symmetrical" to the Avoid list, matching
Candidate #2's own wording ("excessive symmetry").

**PHYSICS - left untouched**, but likely regains effectiveness anyway: it wasn't flagged as a
problem in Test1, only became a problem in Test2 after two other sections got much longer
(prompt_lab §1.1 dilution corollary - not that PHYSICS broke, but that it lost "share of
voice" in a denser prompt). Shortening OUTFIT and SKIN should restore its relative weight
without rewriting it.

**BODY - anti-exaggeration clause kept unchanged.** Candidate #2 doesn't call out body
proportion drift as its own separate failure anymore (folded into the general glamour finding,
not flagged as independently worse) - no evidence it needs more work this round.

## If Test3's skin/glamour still doesn't improve

Per the escalation rule, the next lever is **not** more skin text. Try, in order:
1. `quality: basic` instead of `high` for the master (untested hypothesis: higher
   quality/refinement settings may correlate with more aggressive smoothing/idealization -
   worth isolating as its own variable).
2. Seedream 5 Lite instead of 4.5 for this master-build step specifically (Case 03's
   variation-vs-fidelity trade-off, tested there for pose freezing - untested whether it also
   reduces general over-polish, but the mechanism is plausible).
3. Generate a small batch on Test3's prompt and hand-pick the least-glamorous result rather
   than expecting single-shot correction (Case 02: batch generation already proven useful when
   some individual generations fail).

## Length

2792 / 3000 characters, pure ASCII, `scripts/prompt_check.py` PASS, no WARN, no duplicate
phrases - checked before this file was presented. Notably *shorter* than Test2 (2943) despite
adding the new cross-contamination clause, because removing the interpretive OUTFIT/SKIN prose
freed up more room than the new additions used.

## Judge Test3 on

1. Outfit: does it now read as the same garment transferred, not "inspired by" - especially
   neckline/strap/torso construction and shorts rise/placement (Candidate #2's specific list)
2. Skin: less "AI-glamour," more amateur-photo quality - genuinely different from Test1/Test2,
   not just a smaller version of the same look
3. Chest physics: less symmetrical/orderly, now that PHYSICS has more relative weight
4. Face/hair/anatomy stability: unchanged from Test1/Test2 (must not regress)
5. Body proportions: no worse than Test2
