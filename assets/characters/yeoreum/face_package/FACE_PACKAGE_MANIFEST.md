# HAN YEOREUM — FACE PACKAGE v1.1

**Status:** QC / SUPPORT LIBRARY — NOT ENABLED FOR NAT_v1.4.3 PRODUCTION

Canonical identity: `00_CANONICAL/YR_FACE_00_ID_MASTER.jpg`

## 0. Canonical-use rule

`YR_FACE_00_ID_MASTER` remains the highest facial-identity authority.

The current locked `NAT_v1.4.3` production architecture remains:

```text
@image1 = FACE ID MASTER
@image2 = CHARACTER MASTER
@image3 = BODY MASTER
@image4 = FACE-MASKED DAILY REFERENCE
```

This Face Package does **not** modify that order and must not be auto-inserted into production. A Face Package selector may be tested only in an explicit A/B experiment or after a newer canonical Workflow Master / locked preset promotes it.

Do not blend all package images together as equal identity references.

Candidate-QC priority:

```text
identity geometry > functional viewpoint/expression utility > character fit > render quality
```

## 1. 00_CANONICAL

### `YR_FACE_00_ID_MASTER.jpg`
- TYPE: `CANONICAL_IDENTITY`
- AUTHORITY: `HIGHEST`
- VIEW: `FRONT`
- EXPRESSION: `SOFT_NEUTRAL`
- GAZE: `CAMERA`
- STATUS: `LOCKED`
- SOURCE: `01_FACE_ID_MASTER.jpg`
- USE: identity comparison/QC; current NAT production face reference

## 2. 10_LIBRARY_CORE_APPROVED

These images are approved as **library/QC coverage**, not as automatic production replacements for the Face ID Master.

### `YR_FACE_11_3Q_NEUTRAL_VIEWER_LEFT.jpg`
- TYPE: `CORE_VIEW`
- VIEW: `THREE_QUARTER_VIEWER_LEFT`
- EXPRESSION: `SOFT_NEUTRAL`
- GAZE: `CAMERA_OR_NEAR_CAMERA`
- STATUS: `LIBRARY_APPROVED`
- USE: 3/4 identity comparison; future selector/A-B candidate

### `YR_FACE_12_SIDE_GLANCE_VIEWER_RIGHT.jpg`
- TYPE: `CORE_VIEW / GAZE_SUPPORT`
- VIEW: `FRONT_TO_MILD_3Q`
- EXPRESSION: `NEUTRAL`
- GAZE: `OFF_CAMERA_VIEWER_RIGHT`
- STATUS: `LIBRARY_APPROVED`
- USE: side-glance/candid identity comparison; future selector/A-B candidate

### `YR_FACE_13_HEAD_TILT_NEUTRAL.jpg`
- TYPE: `ANGLE_SUPPORT`
- VIEW: `NEAR_FRONT`
- HEAD: `SMALL_LATERAL_TILT`
- EXPRESSION: `SOFT_NEUTRAL`
- STATUS: `LIBRARY_APPROVED`
- USE: head-tilt identity comparison; do not treat as `SHY_CHIN_DOWN`

## 3. 20_LIBRARY_EXPRESSION_APPROVED

### `YR_FACE_20_TINY_SMILE.jpg`
- TYPE: `EXPRESSION_SUPPORT`
- VIEW: `FRONT`
- EXPRESSION: `TINY_SMILE`
- INTENSITY: `LOW`
- STATUS: `LIBRARY_APPROVED`
- USE: restrained positive-expression coverage

## 4. 30_EXPERIMENTAL_NOT_FOR_PRODUCTION

These images were generated to test missing angle coverage. They are retained as experimental evidence only and are **not eligible for automatic selection** because identity fidelity is weaker than the canonical master / uploaded approved library.

### `YR_FACE_30_OPPOSITE_3Q_GENERATED_REVIEW.png`
- TYPE: `ANGLE_SUPPORT`
- TARGET_ROLE: `OPPOSITE_THREE_QUARTER`
- STATUS: `EXPERIMENTAL_ID_DRIFT`
- ISSUE: useful direction coverage, but visible identity drift
- ACTION: regenerate only if opposite 3/4 becomes operationally necessary

### `YR_FACE_31_NEAR_PROFILE_GENERATED_REVIEW.png`
- TYPE: `ANGLE_SUPPORT`
- TARGET_ROLE: `NEAR_PROFILE_60_75`
- STATUS: `EXPERIMENTAL_LOW_UTILITY_ID_DRIFT`
- ISSUE: current Character Bible gives this angle low production value; identity drift also present
- ACTION: do not regenerate unless real Daily References repeatedly require it

### `YR_FACE_32_LOW_ANGLE_GENERATED_REVIEW.png`
- TYPE: `ANGLE_SUPPORT`
- TARGET_ROLE: `LOW_ANGLE`
- STATUS: `EXPERIMENTAL_ID_DRIFT`
- ISSUE: angle coverage useful in theory, but face geometry drifts
- ACTION: regenerate only if repeated Daily References justify the slot

## 5. 90_ARCHIVE_EXCLUDED

These are historical examples only. Never use them in production or automatic selection.

### `YR_REJECT_90_STRONG_SMILE.jpg`
- REASON: excessive/redundant smile intensity relative to Tiny Smile

### `YR_REJECT_91_POUT_KISS.jpg`
- REASON: character-tone mismatch; not a canonical default expression for Han Yeoreum

### `YR_REJECT_92_CHIN_DOWN_MOOD_ID_DRIFT.jpg`
- REASON: concept is useful, but the candidate has identity drift / mood-styling contamination

## 6. Missing roles — do not fill speculatively

### High-value missing role
- `YR_FACE_21_SHY_CHIN_DOWN`
  - Build only when an identity-faithful candidate exists.
  - This is different from lateral head tilt.

### Conditional roles
- `YR_FACE_30_3Q_OPPOSITE`
  - Useful only if a genuinely identity-faithful opposite 3/4 can be produced.
- `YR_FACE_31_HIGH_ANGLE`
- `YR_FACE_32_LOW_ANGLE`
  - Build only if real Daily References repeatedly require these viewpoints.

Near-profile/full-profile coverage is currently low priority for Han Yeoreum's Character Bible and should not be generated merely to complete a generic turnaround set.

## 7. Current-use rule

### Current locked production (`NAT_v1.4.3`)
Use only the canonical face master in the locked four-reference architecture. Face Package members are not substituted automatically.

### QC / reference analysis
Face Package members may be used to:
- compare whether identity survives a viewpoint/expression,
- detect missing viewpoint coverage,
- review a candidate Face Package image,
- design a future controlled A/B test.

### Future selector experiment
Only when explicitly requested:
1. Define the test and baseline before generation.
2. Select at most one package candidate for the tested facial state.
3. Compare against the unchanged canonical `NAT_v1.4.3` baseline.
4. Keep `YR_FACE_00_ID_MASTER` as the identity-QC authority.
5. Do not promote the experiment without measured benefit and a canonical source update.

## 8. Naming rule

Use viewer-relative directions in filenames to avoid mirror-selfie ambiguity:

```text
VIEWER_LEFT
VIEWER_RIGHT
```

Do not use bare `LEFT` / `RIGHT` without specifying the frame of reference.
