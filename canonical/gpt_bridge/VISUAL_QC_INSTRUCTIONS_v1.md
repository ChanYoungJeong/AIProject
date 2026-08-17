# Visual QC Instructions — Claude ↔ GPT Bridge (v1)

Source: migrated from real project sources (`00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt` §4,
`NAT_v1.4.3_LOCKED_PROMPT.txt`, `CHARACTER_BIBLE_YEOREUM_v1.1.txt`) and
`AI_Influencer_Studio_System_Architecture_v0.2.2.md` §18, §32, §34.

## Purpose

Automatic GPT vision calls are **off by default** (Architecture §32.1). The default QC path
is `MANUAL_EXTERNAL`: you upload the relevant images to GPT yourself, along with the template
in **Section 7**, and paste GPT's reply back to Claude. This file exists so GPT gets the same
reference-role rules Claude already operates under — without it, GPT has no way to know that
`CHARACTER_MASTER`'s pose isn't supposed to be copied, or that a face-masked Daily Reference's
face shouldn't be scored for identity.

Claude reads this file too (via `canonical/manifest.yaml` → not yet wired to a manifest field;
reference it directly by path). Keep Sections 2–5 in sync with the real canonical sources if
they ever change — this file restates them for GPT, it doesn't redefine them.

## 1. What images to attach

For a generated-result QC task, attach in this order and label them exactly as shown — GPT's
reply should refer back to these labels:

```text
1. FACE_ID_MASTER      — canonical/... via asset FACE_YEOREUM_V1
2. CHARACTER_MASTER    — asset CHARACTER_YEOREUM_V1
3. BODY_MASTER         — asset BODY_YEOREUM_V1
4. DAILY_REFERENCE     — the face-masked derivative actually used for this generation
5. RESULT              — the generated candidate being reviewed
```

Only attach what the task needs. A reference-selection sanity check may need just 1–4; a
result QC needs all five.

## 2. Character identity ground rules

The character is a **clearly adult (19-year-old) virtual influencer**
(한여름 / Han Yeoreum, `canonical/characters/yeoreum/character_profile.yaml`). Per Workflow
Master §3.7:

- Never flag or describe her as younger than her stated age, and never suggest age-ambiguous
  styling as acceptable.
- If a reference or result reads as age-ambiguous, that itself is a QC failure to report, not
  something to quietly work around.

## 3. Reference role definitions (Workflow Master §4)

| Reference | Authority for | Must NOT be used for |
|---|---|---|
| **FACE_ID_MASTER** | Facial identity: overall impression, face shape, eye shape/spacing, nose, lips, jawline, recognizable traits. Highest authority for identity. | Forcing its exact expression, gaze, mouth position, or head angle onto every result — those should adapt naturally to the scene. |
| **CHARACTER_MASTER** | Hairstyle/color, hair silhouette, base skin tone, neck/shoulder relationship, upper-body continuity. | Pose, expression, clothing (its clothing is not canonical wardrobe), or its studio lighting. |
| **BODY_MASTER** | Canonical body proportions: shoulder/torso ratio, bust/waist/hip relationship, pelvis/leg proportions, overall silhouette. Aspirational/idealized is acceptable as long as anatomy stays internally coherent. | Overriding the Daily Reference's pose. Its clothing is not canonical wardrobe either. |
| **DAILY_REFERENCE** (face-masked for this lane) | Pose, body orientation, camera position/height/distance, crop, framing, environment, lighting direction, color mood, expression *direction*. | Identity or body shape — those must still come from the masters, never from this image. Its clothing is ignored unless the task explicitly says `COPY DAILY OUTFIT`. |
| **OUTFIT_REFERENCE** (if present) | Garment type, neckline, straps/sleeves, seams, fabric, texture, color, length, design details only. | Face, identity, body proportions, pose, camera, or environment. |

## 4. Priority hierarchy

General (Workflow Master §7):

```text
1. FACE ID MASTER identity
2. Daily Reference pose and composition
3. BODY MASTER proportion consistency
4. CHARACTER MASTER hair / upper-body continuity
5. Outfit correctness
6. Correct anatomy and hand count
7. Camera / framing realism
8. Lighting and color
9. Skin micro-detail
10. Decorative details
```

For the locked `natural_mirror` / `NAT_v1.4.3` lane specifically, this collapses to (identical
ordering, just the short form used in that lane's prompt):

```text
FACE identity > DAILY pose/composition > BODY proportions > CHARACTER continuity
> outfit > anatomy > smartphone realism > lighting/skin
```

If two findings conflict, the higher-priority one determines whether this is a P0/P1 issue
(Architecture §19) — a P0 identity failure matters more than a P2 lighting quibble even if the
lighting issue is more visually obvious.

## 5. QC dimensions to evaluate (Architecture §18)

```text
identity, body_proportions, pose, framing, outfit, anatomy_hands,
skin, lighting, camera_realism, ai_artifacts, instagram_believability, character_fit
```

Report the **2–3 highest-impact failures first**, explicitly state what already works (don't
just list problems), and end with one recommendation:

```text
ACCEPT | REVISE_MINIMALLY | REJECT_SEED
```

`REJECT_SEED` applies to structural failures (wrong identity, major pose failure, extra/missing
limbs, impossible reflection, severe body distortion, completely wrong outfit) — prefer
rejecting a broken seed over asking for a repair prompt.

## 6. Required output format (Architecture §34 — `VISUAL_QC_V1`)

Ask GPT to answer in this shape so Claude can parse it without guessing. Missing dimensions
should be omitted, never invented — a dimension GPT didn't actually judge should not get a
score.

```yaml
visual_analysis:
  schema_version: VISUAL_QC_V1
  task_type: generated_result_qc        # or reference_selection_check, etc.
  source_mode: manual_external
  source_model: user_reported_gpt

  compared_assets:
    face_master: FACE_YEOREUM_V1
    character_master: CHARACTER_YEOREUM_V1
    body_master: BODY_YEOREUM_V1
    daily_reference: <asset_id of the face-masked derivative actually used>
    result: <asset_id or filename of the candidate>

  scores:               # 0-10, only dimensions actually judged
    identity: 8.7
    body_proportions: 9.1
    pose: 7.4

  major_failures:
    - <short, specific, in order of impact>

  preserve:
    - <what already works and should not be touched in a revision>

  recommended_changes:
    - <specific, minimal — not a rewrite>

  decision_hint: ACCEPT | REVISE_MINIMALLY | REJECT_SEED
```

## 7. Copy-paste template for GPT

Everything between the `---` lines is meant to be pasted into GPT as-is, with the bracketed
placeholders filled in and the labeled images (Section 1) attached.

---

You are doing visual QC for an AI-influencer image production pipeline. The character is a
clearly adult (19-year-old) virtual influencer named Han Yeoreum — never describe or treat her
as younger than that.

I'm attaching up to five images, each labeled:
1. FACE_ID_MASTER — facial identity authority only. Don't expect its exact expression/gaze/head
   angle to be copied; that should adapt naturally.
2. CHARACTER_MASTER — hair, base skin tone, neck/shoulder/upper-body continuity only. Not a
   pose, expression, or wardrobe reference.
3. BODY_MASTER — canonical body proportions/silhouette only. Not a pose reference.
4. DAILY_REFERENCE (face-masked) — authority for pose, camera, framing, environment, lighting,
   and expression direction only. Not identity or body shape.
5. RESULT — the generated image to evaluate against the above.

Compare RESULT against references 1–4 using their roles above (don't penalize RESULT for
differing from a reference outside that reference's role — e.g. don't dock pose points because
it differs from CHARACTER_MASTER's pose, since CHARACTER_MASTER isn't a pose reference).

Evaluate: identity, body_proportions, pose, framing, outfit, anatomy_hands, skin, lighting,
camera_realism, ai_artifacts, instagram_believability, character_fit. Score only the
dimensions you can actually judge from what's attached — 0–10 each.

State the 2–3 highest-impact problems first. Explicitly say what already works and should be
preserved in any revision. Then give minimal, specific recommended changes — not a full
rewrite. End with exactly one of: ACCEPT, REVISE_MINIMALLY, REJECT_SEED (use REJECT_SEED for
wrong identity, major pose failure, extra/missing limbs, impossible reflection, severe body
distortion, or completely wrong outfit — don't try to prompt-fix a structurally broken image).

Please answer in this YAML shape:

```yaml
visual_analysis:
  schema_version: VISUAL_QC_V1
  task_type: generated_result_qc
  source_mode: manual_external
  source_model: [which GPT model/version you are]
  compared_assets:
    face_master: [label 1]
    character_master: [label 2]
    body_master: [label 3]
    daily_reference: [label 4]
    result: [label 5]
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

## 8. Notes for Claude when the reply comes back

- Treat the pasted reply as `source_mode: manual_external`, `source_model: user_reported_gpt`
  regardless of what GPT claims about itself, unless the user says otherwise.
- If GPT's reply isn't valid YAML, normalize it locally into the shape above before storing —
  never store free-form prose as if it were the structured report (Architecture §34).
- Don't re-derive scores GPT didn't give; a missing dimension stays missing, not zero.
- This normalized report is not yet wired into a database table — Architecture §46 item 14
  (QC schema + result import) is still pending. For now, treat the parsed result as an
  in-conversation decision input only.
