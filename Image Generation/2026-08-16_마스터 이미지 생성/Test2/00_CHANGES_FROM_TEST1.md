# Test2 — changes from Test1

Source: `Test1/CLAUDE_MASTER_REFERENCE_QC_HANDOFF_2026-08-16.md`
Decision: **REVISE — DO NOT LOCK YET** (Test1's own verdict)

References are **unchanged** — same 8 images, same order. Test1's findings were about
rendering/transfer, not about which source images were chosen, so there's no reason to touch
them (Architecture §20 minimum-change principle).

## What Test1 confirmed already works — left alone

- Face/identity stability across seeds, stable facial family
- Stable long black hairstyle (Image 4's role)
- Clean anatomy, no structural/pose failures
- Neutral master-reference presentation, simple background
- Outfit correctly recognized as 3 separate layers (the numbered-list instruction worked)

Kept as-is or only lightly trimmed to make room for the fixes below — not because they're
unimportant, but because touching working language risks breaking what's already working.

## High priority fixes

**1. Skin/rendering** — Test1: "too uniform and polished... doll-like / generic AI-beauty
impression," explicitly *not* a geometry failure. The old SKIN line only asked for "natural
pore detail and tonal variation," which wasn't forceful enough against Seedream's default
beauty-normalization. New SKIN paragraph names the failure mode directly ("resist
beauty-normalization... not a generic doll-like finish") instead of only describing the
desired positive outcome — and the Avoid list now says "doll-like AI-beauty finish" and
"overly clean/uniform skin" explicitly, matching Test1's own wording.

**2. Outfit fidelity** — Test1: category recognition was correct (bodysuit + shorts +
fishnet, correctly layered) but construction was reinterpreted — neckline, strap/upper-chest
construction, torso shaping, waist/leg-opening geometry, shorts rise/placement/silhouette all
drifted. The old OUTFIT paragraph said only "garment details," which is exactly the vagueness
that let this happen. New OUTFIT paragraph enumerates precisely those failure points as
explicit match targets, and adds "not inspiration... not one redesigned to fit it more
conventionally" to directly counter the "inspired by" framing Test1 used to describe the
failure.

## Secondary fix

**3. Body proportion drift** — Test1: stronger bust projection, narrower waist, more
exaggerated hourglass than the reference, flagged as secondary and explicitly *not* to be
fixed at the cost of the (working) identity/anatomy stability. Added one clause to BODY
covering both directions of drift (too generic *and* too exaggerated) rather than rewriting
the section.

## Trimmed to make room (not flagged as problems, just lower-priority this round)

STYLE section removed; POSE and SCENE shortened; FACE's negative list shortened. None of these
were named as failures in Test1 — cut for length budget, not because they need fixing. If
Test2 regresses on pose/background/style, that's a signal these needed to stay, not that the
skin/outfit fixes were wrong.

## Length

2943 / 3000 characters, pure ASCII (`scripts/prompt_check.py --max-length 3000`, PASS, no
`WARN`, no duplicate phrases) — checked before this file was presented, not after.

First pass at this revision was 2983 characters but included 6 em dashes; character count and
UTF-8 byte count disagree whenever non-ASCII characters are present, and something in the
user's own check counted it as over 3,000. Converted to plain ASCII (`-` instead of `—`) so
character count and byte count are now identical (2943 = 2943) — see `canonical/prompt_lab/
HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` §5.2.

## Judge Test2 on (same as Test1's own "next test should be judged on" list)

1. More natural skin and tonal variation
2. Higher exact Outfit Reference fidelity (neckline/straps/torso/waist/shorts construction)
3. Same or better facial consistency
4. Same anatomical stability
5. No worsening of body drift (and check the new anti-exaggeration clause actually helped)
