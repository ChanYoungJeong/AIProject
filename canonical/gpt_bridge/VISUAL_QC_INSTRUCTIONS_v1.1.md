# Visual QC Instructions — Claude ↔ GPT Bridge (v1.1)

**Status:** Candidate canonical bridge instruction  
**Project:** AI Influencer Studio  
**Character:** 한여름 / Han Yeoreum — clearly adult, age 19  
**Primary purpose:** Manual external visual QC between Claude and GPT  

## 0. Source-of-truth rule

This file is a **bridge/restatement**, not a new canonical workflow.

When anything conflicts, use this order:

1. User's current instruction
2. Latest `00_WORKFLOW_MASTER_AI_INFLUENCER_*`
3. Latest locked lane preset, e.g. `NAT_v1.4.3_LOCKED_PROMPT.txt`
4. Latest `CHARACTER_BIBLE_YEOREUM_*`
5. Canonical master assets
6. This bridge file
7. Historical chats / old QC reports

Do **not** let this file silently redefine a locked lane.

Current production fact for `NAT_v1.4.3`:

```text
@image1 = 01_FACE_ID_MASTER.jpg
@image2 = 01_CHARACTER_MASTER.jpg
@image3 = 02_BODY_MASTER.jpg
@image4 = FACE-MASKED DAILY REFERENCE
```

The newer Face Package is currently a **QC/support library unless and until the Workflow Master or locked preset explicitly promotes a face-selector workflow to canonical production**.

---

## 1. Purpose and operating mode

Automatic GPT vision calls are **off by default**. The default path is:

```text
MANUAL_EXTERNAL
Claude prepares context / user uploads images to GPT
→ GPT returns structured VISUAL_QC_V1
→ user pastes result back to Claude
→ Claude normalizes and uses it as a decision input
```

This bridge exists so GPT evaluates each reference only for the role that reference is authorized to control.

Example: do not penalize RESULT because it does not copy `CHARACTER_MASTER` pose; pose is not `CHARACTER_MASTER` authority.

---

## 2. Character identity ground rules

Han Yeoreum is a **clearly adult 19-year-old virtual influencer**.

QC rules:

- Never reinterpret or describe her as younger than her stated age.
- Never recommend age-ambiguous or minor-coded styling as an acceptable fix.
- If a reference or result visually reads age-ambiguous, report that as a **character-fit / age-clarity failure**.
- University/adult-education context is acceptable; school-age framing, minor-coded uniforms, or under-18 cues are not.

Character-fit shorthand:

```text
quiet / introverted / homebody / slightly nerdy / feminine / self-aware
ordinary adult life + fashion experimentation + gradual confidence
```

Avoid rewarding a result merely for looking more glamorous if it breaks this identity.

---

## 3. Reference roles

| Reference | Authority for | Must NOT be used for |
|---|---|---|
| **FACE_ID_MASTER** | Facial identity: overall facial impression, face shape/width, eye shape and spacing, nose, lips, jawline, recognizable traits. Highest authority for identity. | Forcing exact expression, gaze, mouth position, head angle, or facial pose onto every result. |
| **CHARACTER_MASTER** | Hair style/color/length, hair silhouette, base skin tone, neck/shoulder relationship, upper-body continuity. | Pose, expression, wardrobe, or studio lighting. |
| **BODY_MASTER** | Canonical shoulder/torso ratio, bust/waist/hip relationship, pelvis/leg proportions, overall body silhouette. | Overriding Daily pose/composition; wardrobe authority. |
| **DAILY_REFERENCE** | Pose, body orientation, camera position/height/distance, crop, framing, environment, lighting direction, color mood, casual SNS mood. | Identity, body shape, canonical wardrobe. |
| **OUTFIT_REFERENCE** (if present) | Garment type, neckline, straps/sleeves, seams, fabric, texture, color, length, design details only. | Face, body proportions, pose, camera, environment. |

### 3.1 Face-masked Daily Reference caveat

For the current `natural_mirror` lane, the Daily Reference is face-masked.

Therefore:

- Judge **head orientation / head angle** if still visible.
- Judge **expression direction only if it remains genuinely visible despite masking or is separately supplied**.
- Do **not** invent or infer an expression-match score from an obscured face.
- The masked Daily face is never identity evidence.

### 3.2 Outfit scoring caveat

Score `outfit` only when there is a real target to compare against, such as:

- an `OUTFIT_REFERENCE`,
- an explicit wardrobe instruction,
- or a locked preset with a specified outfit.

If no outfit target exists, omit the outfit score rather than inventing one.

---

## 4. Face Package rules

The Face Package is a **selector/support library**, not a multi-image identity blend.

### 4.1 Canonical authority

`01_FACE_ID_MASTER.jpg` remains the canonical face authority unless a newer Workflow Master explicitly changes that rule.

### 4.2 Package categories

Use these labels when reviewing or organizing Face Package assets:

```text
CANONICAL_IDENTITY
CORE_VIEW
EXPRESSION_SUPPORT
ANGLE_SUPPORT
HELPER_ONLY
ARCHIVE_DUPLICATE
ARCHIVE_IDENTITY_DRIFT
ARCHIVE_OVER_STYLIZED
```

### 4.3 Production restriction

Until a future canonical workflow explicitly enables face selection:

- Do not silently replace `FACE_ID_MASTER` with a Face Package image in `NAT_v1.4.3`.
- Do not send the whole Face Package as simultaneous identity references.
- Face Package assets may be used for QC, comparison, angle coverage analysis, and future workflow testing.

### 4.4 Face Package candidate QC

For `face_package_candidate_qc`, compare the candidate primarily against `FACE_ID_MASTER`.

Priority:

```text
identity geometry > usefulness of viewpoint/expression > character fit > skin/render quality
```

Reject/archive a candidate if it becomes a prettier but visibly different person.

Common drift indicators:

- changed lower-face length or jaw width
- changed eye size/spacing
- sharper or significantly different nose
- changed lip architecture
- more mature/glamorous generic beauty face
- strong studio-beauty treatment that overwhelms identity

Mirrored images may be kept as `HELPER_ONLY`, but they are not new identity evidence.

---

## 5. Priority hierarchy

General priority:

```text
1. FACE_ID_MASTER identity
2. DAILY_REFERENCE pose and composition
3. BODY_MASTER proportion consistency
4. CHARACTER_MASTER hair / upper-body continuity
5. Outfit correctness
6. Correct anatomy and hand count
7. Camera / framing realism
8. Lighting and color
9. Skin micro-detail
10. Decorative details
```

For locked `natural_mirror / NAT_v1.4.3`:

```text
FACE identity > DAILY pose/composition > BODY proportions > CHARACTER continuity
> outfit > anatomy > smartphone realism > lighting/skin
```

When findings conflict, the higher-priority failure governs the decision.

A wrong identity should not be accepted because skin or lighting is excellent.

---

## 6. QC dimensions

For generated-result QC, evaluate only dimensions that can actually be judged from the attached inputs:

```text
identity
body_proportions
pose
framing
outfit
anatomy_hands
skin
lighting
camera_realism
ai_artifacts
instagram_believability
character_fit
```

### 6.1 Business/creative fit — optional but recommended when visible

The Workflow Master also treats attraction and believable sensuality as production concerns. When the image and task make these dimensions judgeable, add:

```text
attraction_fit
sensuality_naturalness
```

Definitions:

- `attraction_fit`: does the image remain visually compelling for the intended adult audience without sacrificing identity or realism?
- `sensuality_naturalness`: does sensuality arise believably from styling, pose, crop, gaze, and context rather than artificial anatomy or forced adult-shoot posing?

These are **lower authority than identity, pose, anatomy, and realism**. A sexier image is not automatically a better image.

### 6.2 Character-fit criteria

For Han Yeoreum, `character_fit` should reward:

- quiet / reserved rather than generic influencer-model energy
- ordinary adult settings and believable SNS behavior
- fashion experimentation / gradual confidence
- subtle contrast between calm personality and feminine silhouette
- expressions that can vary naturally without becoming a permanently seductive model face

Penalize:

- party-girl / celebrity-luxury persona drift
- aggressively seductive expression as the default
- age ambiguity
- overly staged glamour-shoot behavior
- character becoming only a body showcase with no Yeoreum personality

---

## 7. Decision rules

Report the **2–3 highest-impact failures first** and explicitly state what should be preserved.

End with exactly one:

```text
ACCEPT
REVISE_MINIMALLY
REJECT_SEED
```

### ACCEPT
Use when no high-impact failure remains and the result is production-usable.

### REVISE_MINIMALLY
Use when the seed is structurally sound and 1–3 targeted changes are likely to fix the result without rebuilding it.

### REJECT_SEED
Use for structural failures such as:

- wrong identity
- major pose/composition failure
- extra/missing limb or severe hand/anatomy failure
- impossible reflection
- severe body distortion
- completely wrong locked/explicit outfit
- age ambiguity significant enough to break the adult character

Prefer rejecting a broken seed over writing a large repair prompt.

---

## 8. Required output format — `VISUAL_QC_V1`

Missing dimensions must be omitted, not guessed and not set to zero.

```yaml
visual_analysis:
  schema_version: VISUAL_QC_V1
  task_type: generated_result_qc
  source_mode: manual_external
  source_model: user_reported_gpt

  compared_assets:
    face_master: FACE_YEOREUM_V1
    character_master: CHARACTER_YEOREUM_V1
    body_master: BODY_YEOREUM_V1
    daily_reference: <asset_id or filename>
    outfit_reference: <asset_id or filename, omit if absent>
    result: <asset_id or filename>

  scores:
    identity: 8.7
    body_proportions: 9.1
    pose: 7.4

  major_failures:
    - <short, specific, highest impact first>

  preserve:
    - <successful element that should not be changed>

  recommended_changes:
    - <minimal, specific change>

  decision_hint: ACCEPT | REVISE_MINIMALLY | REJECT_SEED
```

**Important:** `source_model` is intentionally normalized to `user_reported_gpt` in this bridge. Do not ask GPT to dynamically insert a model name into that schema field.

---

## 9. Task-specific attachment sets

### 9.1 `generated_result_qc`

Attach, normally in this order:

```text
1. FACE_ID_MASTER
2. CHARACTER_MASTER
3. BODY_MASTER
4. DAILY_REFERENCE actually used
5. OUTFIT_REFERENCE if applicable
6. RESULT
```

### 9.2 `reference_selection_check`

Attach only the assets needed to judge whether a candidate reference is appropriate.

Typical:

```text
1. FACE_ID_MASTER
2. CHARACTER_MASTER
3. BODY_MASTER
4. CANDIDATE_DAILY_REFERENCE
```

Judge role compatibility, not final generated-image quality.

### 9.3 `face_package_candidate_qc`

Attach:

```text
1. FACE_ID_MASTER
2. FACE_PACKAGE_CANDIDATE
3. CHARACTER_MASTER (optional, for hair/overall continuity only)
```

Evaluate:

```text
identity
viewpoint_utility
expression_utility
character_fit
skin/render quality
```

Decision:

```text
APPROVE_CORE | APPROVE_SUPPORT | ARCHIVE_DUPLICATE | ARCHIVE_IDENTITY_DRIFT | REGENERATE
```

This Face Package decision vocabulary is separate from generated-result `ACCEPT / REVISE_MINIMALLY / REJECT_SEED`.

### 9.4 `candidate_comparison`

When comparing multiple generated seeds, attach the common references once and label candidates clearly:

```text
RESULT_A
RESULT_B
RESULT_C
```

Rank structural correctness first, not attractiveness alone.

---

## 10. Copy-paste template — generated result QC

Everything between the lines can be pasted into GPT with the labeled images attached.

---

You are doing visual QC for an AI-influencer production pipeline.

The character is Han Yeoreum, a clearly adult 19-year-old virtual influencer. Never reinterpret her as younger. If the result reads age-ambiguous, report that as a QC failure.

Reference roles:

1. FACE_ID_MASTER — facial identity authority only. Preserve recognizable facial structure, but do not expect its exact expression, gaze, mouth position, or head angle to be copied.
2. CHARACTER_MASTER — hair, base skin tone, neck/shoulder/upper-body continuity only. Not pose, expression, wardrobe, or lighting authority.
3. BODY_MASTER — canonical body proportions/silhouette only. Not pose or wardrobe authority.
4. DAILY_REFERENCE — pose, body orientation, camera, crop, framing, environment, lighting direction, color mood, and SNS mood. Not identity or body shape. If its face is masked, do not infer expression details that are not visible.
5. OUTFIT_REFERENCE — if attached, garment design only.
6. RESULT — generated candidate to evaluate.

Do not penalize RESULT for differing from any reference outside that reference's authorized role.

Priority:
FACE identity > DAILY pose/composition > BODY proportions > CHARACTER continuity > outfit > anatomy > camera realism > lighting/skin.

Evaluate only what can genuinely be judged from the attached images:
identity, body_proportions, pose, framing, outfit, anatomy_hands, skin, lighting, camera_realism, ai_artifacts, instagram_believability, character_fit. If clearly judgeable, you may also score attraction_fit and sensuality_naturalness, but these never override identity, anatomy, or realism.

For character_fit, remember Yeoreum is quiet, introverted, homebody/nerdy, feminine, self-aware, and gradually gaining confidence through fashion. Do not reward generic glamour-model or party-girl drift.

State the 2–3 highest-impact problems first. Explicitly say what already works and must be preserved. Recommend only minimal, specific changes. If the seed is structurally broken, reject the seed rather than proposing a large repair prompt.

Return valid YAML only:

```yaml
visual_analysis:
  schema_version: VISUAL_QC_V1
  task_type: generated_result_qc
  source_mode: manual_external
  source_model: user_reported_gpt
  compared_assets:
    face_master: [label or asset id]
    character_master: [label or asset id]
    body_master: [label or asset id]
    daily_reference: [label or asset id]
    outfit_reference: [omit if absent]
    result: [label or filename]
  scores:
    [dimension]: [0-10]
  major_failures:
    - [...]
  preserve:
    - [...]
  recommended_changes:
    - [...]
  decision_hint: [ACCEPT | REVISE_MINIMALLY | REJECT_SEED]
```

---

## 11. Copy-paste template — Face Package candidate QC

---

You are reviewing a candidate image for Han Yeoreum's Face Package.

FACE_ID_MASTER is the canonical identity authority. The candidate must not redefine the face. A Face Package image exists only to provide a useful viewpoint or expression support while preserving the same recognizable person.

Compare primarily against FACE_ID_MASTER. If CHARACTER_MASTER is attached, use it only for hair and overall continuity.

Evaluate:
- identity fidelity
- viewpoint utility
- expression utility
- character fit
- skin/render quality
- whether the candidate duplicates an already-covered functional role

Priority:
identity geometry > viewpoint/expression usefulness > character fit > render quality.

Do not approve a candidate merely because it is prettier. If it looks like a similar but different person, archive it for identity drift.

Return valid YAML only:

```yaml
face_package_analysis:
  schema_version: FACE_PACKAGE_QC_V1
  task_type: face_package_candidate_qc
  source_mode: manual_external
  source_model: user_reported_gpt
  compared_assets:
    face_master: [label or asset id]
    candidate: [label or filename]
  scores:
    identity: [0-10]
    viewpoint_utility: [0-10]
    expression_utility: [0-10]
    character_fit: [0-10]
    render_quality: [0-10]
  functional_role: [FRONT_NEUTRAL | THREE_QUARTER | SIDE_GLANCE | TINY_SMILE | SHY_CHIN_DOWN | HIGH_ANGLE | LOW_ANGLE | OTHER]
  major_failures:
    - [...]
  preserve:
    - [...]
  decision_hint: [APPROVE_CORE | APPROVE_SUPPORT | ARCHIVE_DUPLICATE | ARCHIVE_IDENTITY_DRIFT | REGENERATE]
```

---

## 12. Notes for Claude when a GPT report comes back

- Treat pasted reports as `source_mode: manual_external` and `source_model: user_reported_gpt`.
- If GPT returns prose instead of valid YAML, normalize locally before storing/using it.
- Do not invent missing scores; missing means not judged.
- Do not convert a low score into a prompt change automatically. First decide whether the seed should be rejected.
- Preserve successful features in every minimal revision.
- The bridge report is a decision input; canonical source files still outrank it.
- Face Package reports do not automatically modify `NAT_v1.4.3` reference order.

---

## 13. Changelog — v1.0 → v1.1

1. Added explicit **source-of-truth hierarchy** so the bridge cannot override the Workflow Master or locked NAT preset.
2. Resolved the `source_model` inconsistency by fixing the schema value to `user_reported_gpt`.
3. Added a **face-masked Daily Reference caveat**: do not score/infer expression details that are hidden.
4. Added **outfit-score gating**: omit outfit when no target wardrobe exists.
5. Added the current **Face Package as non-canonical support/selector library** and separate Face Package QC task/schema.
6. Restored optional **attraction_fit / sensuality_naturalness** from the Workflow Master while keeping them subordinate to identity, anatomy, pose, and realism.
7. Expanded `character_fit` using the current Han Yeoreum Character Bible.
8. Added task-specific attachment sets for generated-result QC, reference selection, Face Package QC, and candidate comparison.
9. Clarified `REJECT_SEED` vs minimal revision behavior.
10. Kept the locked `NAT_v1.4.3` 4-reference production structure unchanged.

---

## 14. Note from Claude (this project's local system)

This bridge file is currently **not yet wired into `canonical/manifest.yaml`** or any automated
code path — Architecture §46 item 13 (Vision Analysis Contract) and item 14 (QC schema +
result import) are still unbuilt. Until then, treat both this file and its predecessor as
manually-referenced text: copy Section 10 or 11's template into GPT yourself, and paste the
reply back into the conversation for Claude to read and act on directly.

The **Face Package** referenced in Sections 0, 4, 9.3, and 11 has no corresponding assets in
this project yet — only the single `01_FACE_ID_MASTER.jpg` exists under
`assets/characters/yeoreum/masters/face_id/`. Its rules here are accepted as forward-looking
(per user confirmation this is prepared separately); nothing in this file is treated as
canonical production behavior for `NAT_v1.4.3` until real Face Package assets are registered
and a Workflow Master revision explicitly promotes it.
