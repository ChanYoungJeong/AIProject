# Higgsfield Prompt Construction & Revision Strategy v1

Source: synthesized from 3 real Higgsfield test cases in
`experiments/raw/higgsfield_case_package_v1.1b/` (job IDs, seeds, and full prompts preserved
there verbatim), plus this project's own live master-build iteration in `Image Generation/
2026-08-16_마스터 이미지 생성/` (Test1 → Test2, QC handoffs preserved in each Test folder). This
document is the analysis; the case package and Test folders are the evidence. Updated as each
new Test round adds real evidence — this is a living document, not a one-time writeup.

**Status:** candidate methodology, not a locked preset. It does not modify `NAT_v1.4.3` or any
other locked artifact — it's a separate prompt lineage (character-master build → SNS-photo
expansion) that hasn't gone through Optimization Audit comparison against the locked lane
(Architecture §8.2, §13.1). Treat everything here as a technique to test, not an adopted rule,
until real results validate it.

## 0. The three cases, in one line each

- **Case 01 (Master Reference Build)** — 7 references (1 primary face + 2 secondary face + 3
  body + 1 outfit) → one clean master photo. Identity/body/outfit assembly worked well; worst
  problem was chest/bust physics (figurine-like, poor gravity/soft-tissue behavior).
- **Case 02 (SNS Expansion + Physics, Seedream 4.5)** — master → new candid SNS photo with a
  dedicated PHYSICS paragraph. Pose/expression varied naturally (not frozen); user's own
  hypothesis: the master's AI-look propagates downstream.
- **Case 03 (Strict Daily Reference, Seedream 5 Lite)** — master + a strict pose/scene
  reference → new photo matching that scene closely. Revealed a real model-level trade-off
  between pose fidelity and natural variation (§4 below).

## 1. Core finding: fix leverage is not evenly distributed

Case 02's own diagnostic is the single most important finding in the package: *"The master
itself already looks AI-generated, so downstream artificial skin/body/chest traits may be
inherited. If upstream master quality improves, downstream realism may improve too."* This
lines up exactly with Case 01's own worst flaw being chest/bust physics in the master.

**Implication:** don't spend correction effort re-fighting the same skin/body-physics battle
in every downstream SNS-expansion prompt. Fix it once, upstream, in the master — then every
downstream generation inherits the fix for free. This is the highest-leverage single change
available from this evidence.

## 1.1 Core finding: elaborating a reference image in prose can override the image itself

This project's own Test1 → Test2 round is the clearest evidence for this yet, and it's
important enough to state as a standalone principle, not bury in a pitfalls list.

**What happened:** Test1's OUTFIT paragraph was short and categorical (`"Use Image 8 only for
garment type, neckline, straps, seams, fabric, texture, color, length"` — one sentence,
matching Case 01's original register). Test1's QC flagged imperfect-but-recognizable outfit
transfer. To fix it, Test2 *expanded* the OUTFIT paragraph: an explicit "not inspiration, copy
precisely" framing sentence, an itemized "match exactly: neckline shape, strap/upper-chest
construction, torso panel shaping, waist/leg-opening geometry, shorts rise/placement/
silhouette" checklist, and a closing "same garment, different body, not redesigned" sentence.

**Result: fidelity got *worse*, not better.** Test2's own QC handoff (`Test2/
CLAUDE_QC_CANDIDATE_2_2026-08-16.md`) diagnosis: *"the system is reproducing the outfit
concept, not reliably preserving the specific garment design"* and *"result feels like BODY
reference + OUTFIT reference + model styling prior were blended together."* The same pattern
plausibly explains why the SKIN paragraph's parallel expansion (Test1's one-sentence texture
note → Test2's multi-sentence "actively resist beauty-normalization... generic doll-like
finish" framing) also failed to fix, and may have worsened, the "AI-glamour" rendering — flagged
as HIGH priority in *both* rounds, not just Test1's round.

**Working theory:** a reference image is a much stronger, more precise signal than text for
anything with fine visual detail. When the prompt spends multiple sentences *describing and
reasoning about* what a reference image shows — especially abstract/conceptual language
("not inspiration," "resist normalization," "the same garment... not redesigned") rather than
plain categorical facts — that prose competes with the image on the text-conditioning pathway,
and the model's generic learned prior (generic "AI-glamour" beauty, generic "outfit concept")
has more surface area to reassert itself instead of the specific reference. Case 01's simpler,
more categorical register didn't have this problem and got better fidelity feedback.

**Practical rule:** for any dimension a reference image already answers precisely (exact
outfit design, exact identity, exact pose from a Daily Reference), keep the prompt's role
assignment for that image short and categorical — *what* it controls, not paragraphs
*describing or arguing about* what it shows. Save elaborate prose for dimensions with no
reference image to lean on (mood, lighting genre, camera style) where text is the only signal
available anyway.

**Corollary — text-vs-text dilution:** this project's PHYSICS paragraph was unchanged,
word-for-word, between Test1 and Test2, and wasn't flagged as a problem in Test1's QC — but
Test2's QC flagged chest physics as HIGH priority ("excessive symmetry... insufficient natural
gravity"). The most likely explanation isn't that PHYSICS stopped working; it's that Test2
added so much more text elsewhere (the expanded OUTFIT and SKIN paragraphs) that PHYSICS lost
relative "share of voice" in an already-dense prompt. Adding correction language to one
dimension isn't free — it can visibly cost another, unrelated dimension. This is the §2
dilution risk made concrete with a real before/after.

**Escalation rule:** if two consecutive rounds of *textual* correction on the same dimension
both fail (skin/glamour here: Test1's fix didn't work, Test2's stronger fix didn't work either
and may have made a related dimension worse), stop adding more words to that dimension and
change a structural variable instead — model (§4), quality setting, or generate-a-batch-and-
select rather than expecting one perfect generation (Case 02: "batch generation can yield
usable images" even when some fail). More adjectives is not a third strategy if two rounds of
adjectives already failed.

**Recommendation:** before a master is used as `@Image1`/`PRIMARY` anywhere downstream, run it
through a dedicated, narrow **physics + skin realism correction pass** (§3.2) — image-to-image
on the master itself, not a from-scratch regeneration. Only promote a master to "used
downstream" status after that pass, similar in spirit to how `BODY_MASTER`/`FACE_ID_MASTER`
promotion in this project already requires an explicit step rather than happening by default.

## 2. Single comprehensive prompt vs. staged correction — decision rule

Both approaches are legitimate; the cases show when each one actually fits.

**Use one comprehensive prompt** (like all three original prompts in the package) when
building something new where the dimensions genuinely interact and can't be decided
independently: a new master (identity + body + outfit must resolve together), or a new scene
(pose + lighting + composition must resolve together as one photograph). This is why Case 01's
prompt legitimately needs ~60 lines across FACE/BODY/OUTFIT/POSE/SCENE/STYLE — those aren't
separable sub-problems for a from-scratch generation.

**Use a staged, single-dimension correction pass** (image-to-image on an already-mostly-good
candidate) when the base image is already structurally correct — identity, pose, and outfit
are all fine — and exactly one dimension is weak: skin texture, chest/body physics, or
expression. This is Architecture §20's minimum-change principle ("change only rendering/
camera/skin clauses... do not mutate a locked preset in place"), just executed as its own
generation call instead of folding the fix back into a re-run of the big prompt.

**Why staged is usually better for a narrow fix, not just equally valid:** Case 01's prompt
already carries 8+ simultaneous constraint blocks. Adding more physics/skin emphasis to one
clause among that many has diminishing returns and risks new conflicts elsewhere — Architecture
§15's own rule is "if conflict risk is high, simplify rather than add more instructions," and
Workflow Master §10 already warns against adding long negative lists after every failure. A
narrow, single-purpose correction prompt has no competing instructions to dilute it, so the
model has less to trade off.

**Practical rule of thumb:** if you can point at one QC dimension and say "everything else
about this image is fine," reach for a staged correction pass, not a bigger prompt.

## 3. Staged correction templates (ready to test)

Each is image-to-image on a specific candidate: attach the candidate itself as the primary
reference, lock everything else explicitly, change only the named dimension.

### 3.1 Skin-texture-only correction

```text
Use the attached image as the exact reference for identity, pose, body, outfit, framing,
background, and lighting. Change nothing except skin rendering.

SKIN ONLY: replace any waxy, plastic, beauty-filter-smoothed, or overly uniform skin with
realistic photographed skin — fine natural pore texture, subtle tonal variation, natural
highlight breakup, visible micro-texture that holds up at close crop. Do not add freckles,
moles, acne, scars, or blemishes that weren't already there.

Do not change face shape, expression, gaze, pose, body proportions, outfit, background, or
lighting in any way. This is a texture-only correction of the same exact photograph.
```

### 3.2 Body / chest-physics-only correction

Seeded from the one paragraph the cases already show helping ("PHYSICS section seems somewhat
better than variants without it" — Case 02):

```text
Use the attached image as the exact reference for identity, face, pose, outfit, framing,
background, and lighting. Change nothing except body/chest physics realism.

PHYSICS ONLY: keep the same body proportions and chest volume, but make them physically
believable — natural gravity-driven distribution, softer lower fullness, less artificial
upper lift, mild natural asymmetry, and realistic attachment to the torso. Avoid perfectly
round, rigid, identical, or molded shapes. Let the outfit react with slight stretch, uneven
tension, soft drape, small irregular folds, and subtle compression against the body.

Do not change face, identity, pose, outfit design, background, or lighting. Do not make the
body smaller, larger, or differently proportioned — only correct how it physically renders.
```

### 3.3 Expression-only correction

For the specific, already-documented "pasted/frozen face" failure (Workflow Master §10; also
why Case 02/03 explicitly instruct against copying the master's exact expression):

```text
Use the attached image as the exact reference for identity, pose, body, outfit, framing,
background, and lighting. Change nothing except facial expression.

EXPRESSION ONLY: give her a natural expression that fits the existing pose and mood — relaxed
brows and jaw, soft eyes, natural lips. Do not copy a frozen or pasted-looking expression.
Identity (face shape, proportions, eyes, nose, lips, jawline, skin tone) must stay exactly the
same — only the expression itself changes.

Do not change face shape, identity, pose, body, outfit, background, or lighting.
```

Each of these is deliberately short and single-purpose — that's the point (§2). If a candidate
needs two of these, run them as two separate passes rather than merging the paragraphs; merging
reintroduces the multi-constraint dilution problem this approach is meant to avoid.

### 3.4 Outfit-structure-only correction

Added 2026-08-16 after Test3's updated QC (`Image Generation/2026-08-16_마스터 이미지 생성/
Test3/CLAUDE_QC_NEW_BATCH_UPDATED_2026-08-16.md`) found the same left/right garment-construction
failure across all three candidates in the batch — see §5.3. Two textual rounds on this exact
dimension had already failed (Test2's elaborate correction, Test3's simplified categorical
guard), triggering the §1.1 escalation rule. Unlike §3.1–3.3, this template needs a *second*
attached image (the original outfit reference) because the failure is specifically about one
reference role's content (body shape) overriding another (garment), so the garment reference
needs to be reasserted directly rather than described from memory:

```text
Use the first attached image as the exact reference for identity, face, pose, body, skin,
framing, background, and lighting. Use the second attached image only as the exact reference
for the garment design. Change nothing except the outfit's construction.

OUTFIT ONLY: rebuild the garment so the left and right sides match as one symmetrical,
structurally coherent piece. Match neckline shape, strap width and placement, and torso panel
construction from the second image equally on both sides. Do not let body shape from the first
image reinterpret, redesign, or distort the garment — transfer it unchanged and structurally
consistent left to right.

Do not change face, identity, pose, body proportions, skin, other garments, background, or
lighting. This is a garment-construction-only correction of the same exact photograph.
```

First real test: `Correction1_Outfit/`, applied to Test3 Result 1. Report back whether this
closes the left/right asymmetry without the body reference re-contaminating the fix — if it
doesn't, the next lever isn't a third rewording of this template but a bigger structural change
(e.g. reducing how many images are attached in the same call, or splitting outfit assembly into
its own generation step entirely rather than folding it into the same master-build prompt).

## 4. Model routing: Seedream 4.5 vs. 5 Lite (Case 03 finding)

Real, empirically observed trade-off, not a simple "one model is better":

```text
Seedream 4.5    high pose fidelity to the reference        can over-freeze the face / make
                                                             skin excessively consistent —
                                                             reads as copy-pasted

Seedream 5 Lite more natural variation, less duplicate-     weaker pose fidelity — doesn't
                looking output                              follow the reference pose closely
```

**Decision rule:** pick the model by generation *intent*, not by default:
- Need to closely match a specific reference pose/composition (e.g. a strict Daily Reference
  match) → Seedream 4.5, and treat "expression not frozen" as its own explicit prompt
  instruction (already working per Case 02/03) rather than trying to also fix it by switching
  models.
- Want natural variation across a batch, or the 4.5 frozen-face problem persists despite
  prompt wording → Seedream 5 Lite, accepting looser pose adherence as the trade-off.

This is a genuine future lever worth testing formally, not just prompt wording. Note (not yet
implemented): `app/schemas/production_request.py`'s `ProductionRequest.pose_change` field is
already the natural home for this decision (`low` → prioritize pose fidelity → 4.5; `high` →
prioritize variation → 5 Lite) if this ever gets validated enough to wire into the Reference
Selection Engine. That would be a real code change requiring its own Optimization Audit
comparison against the locked lane first — out of scope for this document.

## 5. Operational pitfall found in the evidence: declared role without an attached image

Case 02's prompt describes `@Image2` as controlling background/lighting/mood — but the actual
job record shows no `@Image2` was ever attached. The instruction had nothing to reference, so
in practice background/mood came from text description alone, silently, without anyone
deciding that on purpose.

**Checklist before submitting any Higgsfield job:** every `@ImageN` referenced in the prompt
text must have a real uploaded reference in that exact slot. A role instruction with no
matching attachment doesn't error — it just quietly does nothing, which is a confusing failure
mode to debug after the fact.

## 5.1 Operational pitfall: a hand-written prompt exceeding max_prompt_length

Found in this project's own first attempt at a master-build prompt (`Image Generation/
2026-08-16_마스터 이미지 생성/Test1/`): a hand-written prompt was drafted, expanded to cover a
3-piece outfit correctly, and presented at 4449 characters — 48% over the 3,000-character
Seedream limit (Workflow Master §5) — without being run through `scripts/prompt_check.py`
first. All three real case prompts in the evidence package independently landed at 2789–2995
characters, so 3,000 is a real, consistently-respected ceiling in practice, not just a
documented rule.

**Checklist before presenting any hand-written Higgsfield prompt:** run
`scripts/prompt_check.py <file> --max-length 3000` (or the model's actual limit) and confirm
`PASS` before calling a prompt final — the same way `app/services/prompt_validation.py`
enforces this automatically inside `build_generation_plan()` for the locked pipeline. A
hand-written prompt built outside that pipeline (like a Test-folder master-build prompt) gets
no automatic check, so it has to be run by hand, every time, not just when asked.

## 5.2 Operational pitfall: character count vs. byte count on paste

Test2's revised prompt passed `scripts/prompt_check.py` at 2983 characters, but the user still
saw it reported as over 3,000 elsewhere. Root cause: the prompt used 6 em dashes ("—"), each 3
bytes in UTF-8 but 1 Python character — `len(text)` (character count) and
`len(text.encode("utf-8"))` (byte count) disagree whenever any non-ASCII character is present.
Whatever counted it "over 3000" was very likely counting bytes, or the em dashes got mangled in
copy-paste into something longer. Converting the file to pure ASCII (`—` → `-`) made the
character count and byte count identical (2943 = 2943), which removes the ambiguity outright
regardless of which counting method any given tool uses.

**Checklist addition:** prefer plain ASCII in any Higgsfield prompt — no em dashes, no smart
quotes, no other typographic Unicode. `scripts/prompt_check.py` now warns when it finds
non-ASCII characters and fails if the UTF-8 *byte* length exceeds `max_length` even when the
*character* length doesn't, but the simplest fix is not needing that check to save you: write
plain ASCII from the start.

## 5.3 Cross-contamination between reference roles

Test2's QC (`Candidate #2`) named a failure mode neither Test1 nor the original case package
called out explicitly: *"clothing appears influenced by body-shape information"* — the outfit's
cut/fit visibly adapted toward the body reference rather than transferring as-is. Assigning
each image a role (§ everywhere in this doc) stops the model from treating them as
interchangeable, but doesn't by itself stop one role's content from *leaking* into another's
output. Where fidelity to one specific image matters, say so explicitly as its own fact: e.g.
"do not let Images 5-7 change the outfit's cut, fit, or construction" — not just "Image 8 is
the outfit reference" and assuming that implies the rest.

**Update 2026-08-16 (Test3):** the guard sentence above (added specifically to fix this) did
not fully solve it. Test3's updated QC (`Image Generation/2026-08-16_마스터 이미지 생성/Test3/
CLAUDE_QC_NEW_BATCH_UPDATED_2026-08-16.md`) found the same failure mode — left/right
neckline/strap mismatch, garment reading as "partially body-generated" — in all three
candidates, i.e. systematic, not incidental. That makes two consecutive textual attempts on
this exact dimension that both failed (Test2's elaborate version, Test3's short categorical
guard), which triggers the §1.1 escalation rule: stop rewording this clause a third time and
change a structural variable instead. The lever being tried next is §3.4's staged
outfit-structure correction pass (image-to-image, re-attaching the actual outfit reference
image rather than describing it in text) — not a Test4 prompt rewrite.

## 6. What NOT to change based on this evidence

- Don't touch pose/expression freedom in SNS-expansion prompts — already working (Case 02: "not
  frozen to the master," "natural variation... is useful").
- Don't treat Seedream 5 Lite's looser pose-matching as a flat defect — it's a real trade-off
  (§4), useful specifically when avoiding duplicate-looking output matters.
- Don't keep adding more negative/avoid-language to the master-build prompt hoping physics
  improves — Case 01's prompt already has extensive avoid-language and still has the physics
  problem. The evidence points at a targeted corrective pass (§3.2) as the more promising fix,
  not more prohibitions inside the same already-dense prompt (Workflow Master §10: "do not add
  long negative lists after every failure").

## 7. Suggested next step

Run §3.2 (physics correction) on a real master image-to-image, and report the result back —
at that point a specific, evidence-based follow-up correction (or confirmation it worked) can
be proposed against the actual output, the same way QC corrections work everywhere else in
this project (Architecture §20).

**Update 2026-08-16 (Test3, first pass):** Test3's master-build prompt (the §1.1 fix applied)
initially looked like physics was no longer the weak dimension, with skin/rendering (an
artifact-like speckling failure on one candidate, plus residual AI-beauty smoothness on the
apparent best candidate) as the sole remaining weak dimension — so a §3.1 skin-only pass
(originally drafted as `Correction1_Skin/`, since renumbered `Correction2_Skin/` — see below)
was drafted first, targeting Result 3.

**Update 2026-08-16 (Test3, revised after updated QC):** a second QC pass on the same batch
(`CLAUDE_QC_NEW_BATCH_UPDATED_2026-08-16.md`) found a HIGH-priority outfit-structure failure —
left/right garment mismatch — in all three candidates, including Result 3, superseding the
"Result 3 = structurally fine, only skin is weak" read that the skin-only pass was built on.
Running a skin-only pass on Result 3 as originally planned would have locked in the broken
outfit (the template explicitly preserves "outfit... in any way"). Corrected plan: run §3.4
(outfit correction, new, see §3.4) first, on Result 1 (now the safer candidate per the updated
ranking) — see `Correction1_Outfit/` — then chain the skin pass (`Correction2_Skin/`, renamed
from `Correction1_Skin/` so folder numbering matches actual run order) onto *that* pass's
output rather than onto raw Result 3. Lesson for future rounds: before spending effort building
a correction pass off one QC handoff, check whether a newer/updated QC handoff exists for the
same batch — QC itself can be revised after a first look.

**Update 2026-08-16 (Test3 -> Test4, user overrode the staged-correction plan):** the user put
both `Correction1_Outfit/` and `Correction2_Skin/` on hold and asked for the outfit fix to go
through a new master-build round instead (`Test4/`). §2's decision rule would have recommended
staged correction here (only one dimension - outfit - was actually broken; identity/pose/body
were fine), but the staged-correction plan required manually re-fetching Result 1 from the
original generation session since result images aren't saved into the Test folders (only the
inputs are - see `Image Generation/2026-08-16_마스터 이미지 생성/README.md`). That operational
friction is a plausible reason to prefer a from-scratch round even when staged correction is
the "correct" lever on paper - worth remembering as a real trade-off, not just a theoretical
one, next time §2's rule points at staged correction.

Test4's first draft respected the §1.1 escalation rule inside the from-scratch prompt itself:
rather than a third reword of the OUTFIT "don't let body affect outfit" guard (Test2 and Test3
already tried two variants of that and both failed), it stated the desired output property
directly (left/right construction must match) plus an explicit precedence rule for reference
conflicts - two elements neither prior round stated. That draft kept the word-choice lesson too
(avoided "symmetrical" for the outfit fix since PHYSICS uses that exact word for the opposite
intent on the chest - reusing one word for a wanted trait in one clause and an avoided trait in
another is its own text-conditioning ambiguity risk, independent of §1.1's dilution finding).

**Update 2026-08-16 (Test4, revised again - outfit description removed entirely):** before
Test4 was even run, the user separately flagged that the garment still doesn't match Image 8
exactly and asked for all outfit *description* to be stripped from the prompt, leaving only role
assignment ("Image 8 is the exact garment reference, reproduce it exactly") and boundary-setting
("do not copy Image 8's pose," "do not let Images 5-7 alter the garment"). This removed the
itemized property list every prior round kept in some form (garment type/neckline/straps/seams/
fabric/texture/color), and the separate three-piece numbered list. This is the same §1.1 theory
taken further than any prior round tried it: even Test1's original "short categorical" register
- already the register §1.1 recommends over descriptive/argumentative prose - still itemized the
garment's properties in words and still got only "imperfect but recognizable" transfer. Whether
*zero* itemization outperforms *short categorical* itemization is a genuinely new, untested
question this makes possible to answer. Tradeoff accepted knowingly: the three-piece list
existed because Test1-3 QC never reported a missing piece while it was present, so Test4 is the
first round with no textual guarantee that count survives - watch for that specifically, not
just left/right fidelity, when QC comes back. See `Image Generation/2026-08-16_마스터 이미지
생성/Test4/00_CHANGES_FROM_TEST3.md` for the full before/after; report back once Test4 has real
QC so this section can record whether removing the description worked better than describing it
carefully.
