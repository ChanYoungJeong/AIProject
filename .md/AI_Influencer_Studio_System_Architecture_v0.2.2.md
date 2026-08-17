# AI Influencer Studio — System Architecture & Automation Design
Version: 0.2.2  
Status: Claude-First Local Integration Draft — Token-Aware Vision / Manual GPT Bridge Revision

---

# 1. Purpose

This document defines the system architecture for an AI-assisted image production workflow built around:

- reusable character masters,
- reference-image selection,
- prompt management,
- Higgsfield image generation,
- generation-result QC,
- iterative prompt correction,
- user-feedback memory,
- experiment logging,
- and future MCP-based automation.

The system must allow the user to give a natural-language production request such as:

> “회사에서 찍은 것 같은 자연스러운 반신 셀카를 만들고 싶어.”

and automatically determine:

1. which canonical character and master set applies,
2. which lane / current production baseline applies,
3. which Daily Reference or other production reference is appropriate,
4. whether Daily Reference preprocessing such as face masking is required,
5. whether an Outfit Reference or other optional reference is needed,
6. which exact reference order should be supplied,
7. whether to retrieve the current baseline, construct a revision, or enter an explicit optimization audit,
8. how the final generation plan should be validated,
9. whether a returned candidate should be accepted, rejected, or minimally revised,
10. what validated lessons should be stored for future generations.

The system should reduce unnecessary Higgsfield generations and minimize repeated mistakes.

---

# 2. Relationship to Existing Workflow

The latest approved `00_WORKFLOW_MASTER` remains the canonical source for creative and generation rules. At the time of this architecture revision, the integrated workflow source is `00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2`.

The System Architecture does **not** replace the creative workflow. It defines how Claude, local files, metadata, SQLite, vision analysis, QC, memory, and optional MCP tools execute that workflow.

The following approved sources must be treated as separate canonical layers:

- `00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2` — global creative/workflow rules
- `CHARACTER_BIBLE_YEOREUM_v1.1` — canonical character concept and content logic
- `NAT_v1.4.3_LOCKED_PROMPT` — locked production preset for the completed Natural / Mirror Selfie lane
- canonical master images — FACE ID MASTER, CHARACTER MASTER, BODY MASTER

A locked lane preset is immutable **as a benchmark artifact**, not immune from future optimization. It records the best approved configuration at the time it was locked. Claude may explicitly re-evaluate its prompt structure, reference count/order, masking policy, or other generation strategy. Any improved strategy must be saved as a derived candidate/new version and compared against the locked baseline rather than silently overwriting it.

Creative source priority at runtime:

```text
1. Current user instruction
2. Latest WORKFLOW_MASTER
3. Explicitly selected locked lane preset / canonical asset within its declared scope
4. Canonical Character Bible / character metadata
5. Validated memory
6. Historical experiments
7. Old chats
```

Infrastructure rules in this System Architecture govern storage, retrieval, versioning, automation, and execution, but must not silently change an approved creative preset.

The system therefore distinguishes **production stability** from **optimization freedom**:

- production uses the latest approved baseline predictably,
- optimization may challenge any prompt/reference implementation choice when explicitly invoked,
- canonical promotion happens only after comparison and approval.

---

# 3. Core Design Principle

The local system should have **one primary controller** and multiple replaceable capabilities.

## Claude / Claude Code — Primary Controller

Primary responsibilities:

- workflow orchestration,
- production-request interpretation,
- canonical-state resolution,
- reference-role planning,
- prompt construction and revision,
- experiment reasoning,
- long-term rule management,
- local file and database interaction,
- MCP / CLI tool use,
- system development and maintenance.

Claude acts as:

**Production Director + Prompt Engineer + System Orchestrator**

## Vision Analyzer — Pluggable, Cost-Aware Capability

Visual reasoning should be exposed through a stable internal interface rather than hard-wired to one model.

Possible backends:

- manual external GPT review performed by the user,
- GPT vision through an explicitly enabled API/connector adapter,
- Claude vision only when Claude itself genuinely needs to inspect pixels,
- a future local or hosted vision model,
- deterministic local image utilities for simple preprocessing.

Typical responsibilities:

- reference comparison,
- pose/composition analysis,
- identity drift assessment,
- candidate ranking,
- QC,
- visible AI-artifact detection.

### Visual Context Isolation Rule

The Claude orchestrator should **not ingest image pixels merely because it manages an image workflow**. It should normally manage:

```text
asset IDs
file paths
reference roles
metadata
prompt state
normalized visual-analysis results
```

A selected visual worker receives only the images required for its task and returns a compact structured result. Claude then reasons over that result rather than re-reading the same images.

Default rule:

> Do not send the same visual context to Claude and GPT by default. Duplicate visual processing must be an explicit diagnostic or comparison choice.

For the MVP, automatic GPT visual calls are **disabled by default**. Manual external GPT review is a first-class supported path so the user can upload images to GPT directly and return only the QC/reference-analysis result to the local Claude system.

The rest of the system should not care whether the structured analysis came from a manual GPT session, an API worker, Claude vision, or a future local model.

## Higgsfield / Generation Provider

The generation provider performs image/video generation only. It is not the system brain.

The architecture must support provider adapters so a future model can be added without rewriting the workflow.

---

# 4. High-Level Architecture

```text
USER REQUEST
     │
     ▼
CLAUDE ORCHESTRATOR
(metadata / rules / prompts by default; no image pixels)
     │
     ├───────────────┬────────────────┐
     ▼               ▼                ▼
CANONICAL STATE   ASSET SEARCH    MEMORY SEARCH
     │               │                │
     └───────────────┴────────┬───────┘
                              ▼
                    REFERENCE / LANE PLANNER
                              │
                              ▼
                       PROMPT ENGINE
                              │
                              ▼
                       GENERATION PLAN
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             MANUAL HIGGSFIELD    EXPLICIT PROVIDER TOOL
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    GENERATED CANDIDATES
                              │
                              ▼
                       QC MODE ROUTER
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
       MANUAL GPT BRIDGE   AUTO VISION      CLAUDE VISION
          (default)         (opt-in)         (on-demand)
              │               │                │
              └───────────────┴────────┬───────┘
                                      ▼
                           NORMALIZED QC REPORT
                                      │
                                      ▼
                               CLAUDE DECISION
                           ACCEPT / REVISE / REJECT
                                      │
                                      ▼
                            EXPERIMENT + MEMORY
```

Manual Higgsfield remains the default execution path. A connected generation provider is an explicit action, not an automatic consequence of creating a GenerationPlan.

---

# 5. Production Request

Every natural-language request is normalized into a structured `ProductionRequest`, but the user is never required to fill every field manually.

Example:

```yaml
production_request:
  character_id: yeoreum
  lane: natural_mirror
  content_type: mirror_selfie
  framing: half_body
  environment: bedroom
  mood: natural
  outfit_mode: inherit
  preset_id: auto
  daily_reference_id: null
  daily_reference_face_policy: auto
  identity_priority: maximum
  realism_priority: high
  pose_change: low
  generation_provider: higgsfield
  generation_mode: manual_unlimited
  generation_model: auto
  requested_output_count: null

  visual_reasoning_mode: manual_external
  auto_external_vision: false
  allow_duplicate_visual_review: false
```

Resolution order for missing fields:

1. current user request,
2. explicitly selected preset,
3. canonical lane policy,
4. Workflow Master,
5. Character Bible / character metadata,
6. asset metadata,
7. validated successful recipes,
8. timestamped user preferences.

`requested_output_count` should remain unset unless the user or selected preset specifies it. The architecture should not hard-code a universal test batch size.

---

# 6. Asset Management System

Assets must not be treated as anonymous image files. Every important image receives an ID, metadata, provenance, and approval state.

## Primary Image Asset Types

```text
FACE_ID_MASTER
CHARACTER_MASTER
BODY_MASTER
DAILY_REFERENCE
OUTFIT_REFERENCE
STYLE_REFERENCE
ENVIRONMENT_REFERENCE
GENERATED_RESULT
APPROVED_RESULT
REJECTED_RESULT
```

Derived assets use the same primary type plus provenance metadata. Example: a face-masked Daily Reference remains a `DAILY_REFERENCE` with `derived_from` and `face_masked: true`.

The system should avoid inventing additional master categories unless a real production need is validated. The current canonical character architecture is exactly:

```text
FACE ID MASTER
+ CHARACTER MASTER
+ BODY MASTER
```

with the Daily Reference acting as the production-time pose/composition source.

---

# 7. Asset Metadata

Recommended core metadata:

```yaml
asset_id:
file_path:
asset_type:

character_id:
lane:

shot_type:
view_angle:
pose_type:
camera_angle:
camera_distance:
body_visibility:

environment:
lighting:
mood:
content_pillar:

outfit_id:

source:
created_at:
derived_from:
face_masked: false

quality_score:
identity_score:
realism_score:
pose_readability_score:

approved: false
canonical: false
locked: false
```

Useful computed/search metadata can later include:

```text
pose_similarity
camera_similarity
framing_similarity
environment_similarity
identity_conflict_risk
character_fit
previous_success_rate
```

Metadata should describe the asset; it should not silently promote the asset to canonical state.

---

# 8. Reference Selection Engine

Reference selection has two operating modes: **Production Mode** and **Optimization Audit Mode**.

## 8.1 Production Mode

Resolution order:

```text
1. If the selected approved preset declares exact reference roles/order, use them as the current baseline.
2. Else if the lane has a validated reference profile, use that profile.
3. Else run generic reference planning.
```

For a new or unvalidated lane, the generic planner should optimize:

> the smallest reference set that reliably controls the required attributes.

For an already validated lane, production runs should not casually remove references merely to satisfy a minimum-reference heuristic. This protects reproducibility and prevents accidental regression.

## 8.2 Optimization Audit Mode

When the user explicitly asks Claude to re-check or optimize the workflow, **all implementation choices may be challenged**, including an already-validated lane:

```text
reference count
reference role split
reference order
FACE / CHARACTER / BODY necessity
Daily Reference masking policy
prompt wording and section order
prompt length / redundancy
negative constraints
preset modularity
```

The existing approved configuration becomes the **control/baseline**, not a constraint on the search space.

Claude may propose fewer references, more references, different role assignment, or a different prompt architecture if there is a plausible reason it could improve Seedream output.

However:

- never mutate the baseline during the audit,
- compare candidate strategies against the baseline under comparable conditions,
- preserve successful character/pose/realism behavior unless the test intentionally targets it,
- promote a new configuration only after evidence and user approval.

This gives Claude freedom to improve the workflow without losing the reproducibility of previously approved results.

---

# 9. Reference Strategy

## 9.1 Canonical Three-Master Character Structure

Current canonical character references:

```text
FACE ID MASTER
  → facial identity authority

CHARACTER MASTER
  → hair, base skin tone, neck/shoulder and upper-body continuity

BODY MASTER
  → canonical body proportions and silhouette
```

The Daily Reference controls pose/composition and must not redefine identity or body proportions.

## 9.2 Current Natural / Mirror Selfie Baseline

For `NAT_v1.4.3`, reference order is deterministic:

```text
@image1 = FACE ID MASTER
@image2 = CHARACTER MASTER
@image3 = BODY MASTER
@image4 = FACE-MASKED DAILY REFERENCE
```

Priority:

```text
FACE identity
> DAILY pose/composition
> BODY proportions
> CHARACTER continuity
> outfit
> anatomy
> smartphone realism
> lighting/skin
```

For this lane, the four-reference structure is the **current validated production baseline**. Production Mode should use it unchanged unless another approved version supersedes it.

Optimization Audit Mode may re-test whether four references are actually optimal. The system must treat the existing four-reference result as the control configuration and retain it for comparison.

## 9.3 Daily Reference Face Policy

External Daily References can introduce identity conflict. The system should support:

```text
none
mask
blur_or_obscure
manual_review
auto
```

For the current `NAT_v1.4.3` production baseline, use a face-masked Daily Reference. In Optimization Audit Mode, Claude may test unmasked, masked, blurred/obscured, or other preprocessing strategies against that baseline. For other lanes, `auto` may choose masking when identity conflict risk is material.

## 9.4 Generic / Future Lanes

For new or unvalidated lanes, reference count is an open optimization problem by default.

For validated lanes, reference count is stable in Production Mode but becomes an open optimization variable again when Optimization Audit Mode is explicitly invoked.

---

# 10. Reference Scoring

Candidate references should be ranked against the production request.

Suggested scoring dimensions:

```text
pose_similarity
camera_similarity
framing_similarity
environment_similarity
lighting_similarity
identity_compatibility
outfit_compatibility
reference_conflict_risk
previous_success_rate
```

Conceptually:

```text
Reference Score =
Intent Match
+ Structural Compatibility
+ Historical Success
- Conflict Risk
```

The exact numerical formula does not need to be finalized during MVP.

---

# 11. Prompt Library

Prompts may be modular, but **locked production presets must also store an immutable rendered prompt snapshot**.

Recommended structure:

```text
prompts/
  modules/
    identity/
    body/
    pose/
    camera/
    lighting/
    realism/
    outfit/
    avoidance/

  presets/
    natural_mirror/
    future_lanes/

  snapshots/
    locked/
```

Modules are useful for building or revising presets. They are not a substitute for preserving the exact text of a proven locked preset.

This avoids a reproducibility failure where module changes silently alter an old preset.

---

# 12. Prompt Preset

A preset represents a tested production configuration and should store both its structure and its rendered prompt.

Example:

```yaml
preset_id: NAT_v1.4.3
status: locked
lane: natural_mirror

model:
  provider: higgsfield
  model: seedream_4_5

reference_profile: NAT_MIRROR_FOUR_REF_V1
max_prompt_length: 3000

prompt_snapshot_path: prompts/snapshots/locked/NAT_v1.4.3.txt
prompt_hash: <computed>

modules:
  identity: optional_module_id
  camera: optional_module_id
  realism: optional_module_id

outfit_policy: preset_defined
revision_policy: derive_new_version
```

Rules:

- A `locked` preset is read-only.
- A revision creates a new version; it never mutates the locked snapshot.
- Prompt length validation happens against the final rendered text.
- The system stores model, reference order, and any preset-owned outfit rules with the snapshot.
- Generic Workflow Master defaults apply only where the preset does not explicitly define a behavior.

---

# 13. Prompt Engine

The Prompt Engine receives:

```text
ProductionRequest
+
Canonical State
+
Selected Assets
+
Selected / Locked Preset
+
Relevant Validated Memory
```

and outputs a `GenerationPlan`.

```yaml
provider:
model:
generation_mode:

references:
  image1:
    asset_id:
    role:
  image2:
    asset_id:
    role:

prompt:
prompt_length:
prompt_hash:

expected_behavior:
high_risk_points:
qc_targets:
```

In Production Mode, if an approved preset applies and the user has not requested a change, the engine should prefer **retrieval over reconstruction**: load the exact approved prompt snapshot and fill only the permitted production-time inputs.

In Optimization Audit Mode, Claude should instead load the approved snapshot as the control, inspect it for redundancy/conflict, construct one or more explicit candidate variants, and record exactly which dimensions differ.

---

# 13.1 Optimization Audit Protocol

An optimization audit must be reproducible rather than conversationally ad hoc.

Minimum audit record:

```yaml
audit_id:
baseline_preset:
baseline_reference_profile:
target_dimension:
hypothesis:
candidate_id:
changed_variables:
held_constant:
test_daily_references:
result_scores:
qualitative_findings:
user_decision:
promotion_status:
```

Recommended principle:

> change as few variables as possible per comparison.

Examples:

- 4 refs vs 3 refs while prompt and Daily Reference stay constant,
- masked vs unmasked Daily Reference while reference count stays constant,
- existing NAT_v1.4.3 wording vs Claude-simplified wording with identical references,
- different reference order with all other variables held constant.

The audit should test whether simplification improves or preserves:

```text
identity
pose/composition adherence
body consistency
anatomy
camera realism
skin/lighting realism
postability
variance across repeated generations
```

A candidate should not replace the baseline merely because one image looks better. Prefer repeated evidence across several suitable Daily References or repeated generations when generation budget allows.

---

# 14. Prompt Construction

For new or revised Seedream prompts, use the current canonical order:

```text
1. Reference-role assignment
2. Output format
3. FACE ID / facial identity
4. CHARACTER continuity / hair / upper body
5. BODY MASTER proportions
6. Outfit mode / garment
7. Daily Reference pose / composition
8. Expression
9. Camera
10. Lighting / color
11. Skin / rendering
12. Important avoidance constraints
```

For Seedream 4.5 production presets, keep the final prompt under 3,000 characters.

Critical behavior:

- identity preservation must not freeze the master expression,
- expression, gaze, head angle, and facial perspective should adapt naturally,
- Daily Reference pose should be followed rather than reinvented in text,
- Master clothing is not canonical wardrobe,
- Daily Reference clothing is ignored unless explicitly requested,
- avoid repeated constraints that create prompt conflict.

---

# 15. Prompt Conflict Detection

Before approving a prompt, check for conflicts such as:

```text
Character Master pose
vs.
Daily Reference pose

Character Master outfit
vs.
Outfit Reference

Style Reference identity
vs.
Character identity

Fixed head angle
vs.
New camera viewpoint

Cinematic lighting
vs.
Casual smartphone requirement
```

If conflict risk is high, simplify the prompt rather than adding more instructions.

---

# 16. Higgsfield Safety / Cost-Control Principle

The default path remains **manual generation on the Higgsfield website / Unlimited workflow**.

Claude prepares and validates the plan and prompt, but should not submit a connected Higgsfield generation unless the user explicitly requests that action.

This is both a cost-control and execution-control boundary.

Default:

```text
PLAN
→ VALIDATE REFERENCES
→ VALIDATE PROMPT
→ USER RUNS HIGGSFIELD MANUALLY
→ IMPORT RESULTS
→ QC
→ MINIMAL REVISION OR ACCEPT
```

Future API generation must remain behind an explicit tool/action boundary.

---

# 17. Generation Strategy

Do not hard-code `1–2 candidates` as a universal rule.

Use a preset- or provider-specific generation policy:

```yaml
generation_policy:
  mode: manual_unlimited
  initial_batch: user_or_preset_defined
  reject_early_on:
    - wrong identity
    - major pose failure
    - severe anatomy error
    - impossible reflection
    - severe body distortion
    - fundamentally wrong outfit
```

The system should prefer selecting a structurally correct seed over trying to repair a fundamentally broken result.

Once a result is already strong, do not automatically add a mandatory second refinement stage. Refinement should be used only when there is a specific, worthwhile correction.

---

# 18. QC Engine

QC conceptually compares the generated result against:

```text
ProductionRequest
FACE ID MASTER
CHARACTER MASTER
BODY MASTER
Daily Reference
Outfit Reference / outfit policy
Selected Preset
Character Bible constraints when relevant
```

This does **not** mean Claude must load all of those images. In the default token-aware path, a visual worker performs the image comparison and Claude receives only the normalized QC result plus asset IDs/provenance.

Visual QC execution modes:

```text
MANUAL_EXTERNAL
  user uploads the required images to GPT (or another visual tool)
  → returns structured QC
  → Claude imports and acts on the report

AUTO_EXTERNAL
  explicitly enabled visual API/connector receives required assets directly
  → returns structured QC
  → Claude does not re-read the images

CLAUDE_ON_DEMAND
  Claude inspects images only when its own visual judgment is specifically requested
  or when validating a disputed/ambiguous external QC result
```

`AUTO_EXTERNAL` must never be triggered merely because an image was imported.

Recommended dimensions:

```yaml
qc:
  identity:
  body_proportions:
  pose:
  framing:
  outfit:
  anatomy_hands:
  skin:
  lighting:
  camera_realism:
  ai_artifacts:
  instagram_believability:
  character_fit:
```

For commercial review, optional additional fields can include attraction / attention potential, but these must not override identity, realism, anatomy, or character coherence.

QC should report the **2–3 highest-impact failures first**, preserve what already works, and recommend one of:

```text
ACCEPT
REVISE_MINIMALLY
REJECT_SEED
```

---

# 19. QC Priority

Handle failures by impact.

```text
P0
- facial identity failure
- major anatomy failure
- fundamentally wrong pose structure
- wrong person / wrong character

P1
- Daily Reference pose/composition drift
- body proportion drift
- major framing/camera mismatch
- outfit failure
- reflection failure

P2
- skin / lighting / smartphone realism
- visible AI artifacts that do not require seed rejection
- expression integration

P3
- minor decorative details
```

Do not spend a new generation correcting P3 while P0/P1 failures remain.

For the current Natural / Mirror lane, identity is first, then Daily Reference pose/composition, then BODY and CHARACTER continuity.

---

# 20. Revision Engine

Revision follows the **minimum-change principle**.

Example:

```text
identity = good
pose = good
body = good
skin = weak
```

Change only rendering/camera/skin clauses.

Additional rules:

- Do not globally weaken identity to fix a frozen expression; instead release exact expression/gaze/head-angle copying.
- Do not invent a new pose to correct pose drift; strengthen the Daily Reference relationship and remove conflicting pose language.
- Do not add long negative lists after every failure.
- Do not mutate a locked preset in place; create a derived revision/version if prompt text must change.
- If a candidate is fundamentally broken, reject the seed instead of over-repairing the prompt.

---

# 21. Experiment Tracking

Every meaningful generation attempt should create an Experiment record.

```yaml
experiment_id:

production_request_id:
preset_version:
prompt_version:

references:
model:

output_images:

qc_scores:

user_feedback:

result:
  rejected
  revised
  approved

revision_from:
revision_reason:
```

---

# 22. Learning / Memory System

Chat history must **not** be the primary memory store.

Store explicit production knowledge in four categories.

## A. Canonical Rules

Stable approved rules, for example:

```text
FACE ID MASTER is facial identity authority.
Daily Reference is pose/composition authority after identity.
BODY MASTER controls canonical proportions.
CHARACTER MASTER controls hair and upper-body continuity.
Master expression/gaze/head angle are not fixed.
```

## B. User Preferences

Timestamped, revisable preferences.

## C. Failure Patterns

Only store reusable failure patterns with evidence and scope.

## D. Successful Recipes

Validated reference + preset + model combinations, including lane scope.

Current validated Natural / Mirror recipe should be seeded as structured memory rather than rediscovered from chat.

---

# 23. Memory Confidence

Do not convert one generation into a permanent rule.

Use explicit state:

```text
observation
hypothesis
tested
validated
canonical
```

Every memory should also carry scope:

```yaml
scope:
  character_id:
  lane:
  provider:
  model:
  preset_family:
```

A rule validated for `NAT_v1.4.3 / Seedream 4.5 / mirror_selfie` must not silently become a universal rule for every future lane.

Promotion to `canonical` requires explicit approval or inclusion in a canonical source file.

---

# 24. User Feedback Handling

User feedback should be converted into explicit diagnostics.

Example:

User:

> 얼굴은 괜찮은데 Image2 자세를 거의 안 따라갔어.

Stored as:

```yaml
feedback:
  identity: acceptable
  pose_reference_adherence: poor

action:
  strengthen_pose_reference_priority
  preserve_identity_prompt
```

Do not interpret this as:

```text
entire prompt failed
```

---

# 25. MCP / Local Tool Architecture

Recommended MVP tools:

```text
get_canonical_manifest
get_workflow_master
get_character_bible
get_lane_policy

search_assets
get_asset
get_canonical_master
prepare_daily_reference

search_presets
get_preset
validate_reference_order
validate_prompt_length

search_generation_history
search_successful_recipes
search_failure_patterns

create_generation_plan
save_generation_plan

export_visual_analysis_packet
import_external_visual_report
validate_visual_report

save_experiment
save_qc_result
save_user_feedback

promote_asset
promote_preset
archive_result
```

`prepare_daily_reference` should be able to create a non-destructive derived reference, including a face-masked copy when the selected lane policy requires it.

The MVP can expose these capabilities through MCP, a local CLI, or both. Business logic should live in reusable Python services rather than only inside tool wrappers.

---

# 26. Future Tools

Later-stage tools may include:

```text
run_visual_qc_explicit
compare_identity_explicit
compare_pose_explicit
build_contact_sheet
recommend_references
recommend_revision

optional_generate_with_higgsfield
get_generation_status
download_generation_results

publish_experiment_report
```

Generation tools must remain explicitly invoked. The orchestrator must never auto-consume generation credits merely because a plan has been prepared.

---

# 27. Data Storage

MVP recommended stack:

```text
SQLite
+
local filesystem / NAS
```

SQLite stores:

```text
asset metadata
prompts
presets
experiments
QC
feedback
memory
```

Images remain normal files.

Do not store large image binaries inside SQLite.

---

# 28. Recommended Folder Structure

```text
AI_Influencer_Studio/

  canonical/
    manifest.yaml
    workflow/
      00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt
    characters/
      yeoreum/
        CHARACTER_BIBLE_YEOREUM_v1.1.txt
    presets/
      natural_mirror/
        NAT_v1.4.3_LOCKED_PROMPT.txt
        lane_policy.yaml

  assets/
    characters/
      yeoreum/
        masters/
          face_id/
          character/
          body/
    daily/
      raw/
      derived_masked/
    outfit/
    style/
    environment/

  prompts/
    modules/
    revisions/
    snapshots/
      locked/

  generations/
    raw/
    shortlisted/
    approved/
    rejected/

  qc/
    packets/
      outbound/
    imported/
      raw/
      normalized/

  experiments/

  memory/
    rules/
    preferences/
    failures/
    successes/

  database/
    studio.db

  app/
    services/
    cli/
    mcp/
    vision/
    providers/

  tests/
```

The canonical folder should remain small and human-readable. Historical experiments belong outside permanent runtime context.

---

# 29. Canonical State

The system must distinguish:

```text
working
approved
locked
canonical
archived
```

Rules:

- `working`: editable draft or candidate.
- `approved`: user accepted for use, but not necessarily the project default.
- `locked`: immutable versioned artifact.
- `canonical`: currently selected source of truth for its scope.
- `archived`: retained for history but excluded from normal retrieval.

A canonical update should create a new version and update `canonical/manifest.yaml`; it should not overwrite the prior locked artifact.

Old chats are not canonical. Old experiments are evidence. Canonical assets, character metadata, workflow sources, and locked presets are sources of truth.

---

# 30. Agent Behavior

When a generation request arrives, Claude should internally follow:

```text
1. Parse user intent
2. Resolve canonical manifest
3. Resolve character + lane
4. Check whether a locked preset applies
5. Load only the relevant canonical text/metadata sources
6. Resolve / search required asset IDs and file paths
7. Apply lane reference policy before generic reference optimization
8. Prepare Daily Reference derivative if required
9. Retrieve only relevant validated memories
10. Build or retrieve prompt
11. Validate prompt length, reference order, and conflicts
12. Produce GenerationPlan
13. Do not load image pixels into Claude unless a selected operation explicitly requires Claude vision
14. When QC/reference visual analysis is needed, choose MANUAL_EXTERNAL by default or another explicitly enabled visual mode
```

Important:

- If a locked preset applies, prefer exact retrieval over prompt reconstruction.
- Do not re-open validated reference-count decisions unless the user asks to redesign the lane.
- If a critical source is missing, stop before a generation action and report the missing dependency.
- Do not require the user to re-explain a canonical asset that exists locally.
- Asset management and visual interpretation are separate concerns: Claude can manage an image by ID/path without seeing its pixels.
- Do not automatically duplicate a visual review across Claude and GPT.

---

# 31. Generation Decision Output

Before manual generation, the system should be able to provide a compact plan:

```text
TARGET
What are we creating?

PRESET / LANE
Which canonical production policy applies?

REFERENCES
Which assets are selected, in what exact order, and for what roles?

PROMPT
What exact prompt snapshot or derived prompt will be used?

RISK
What are the 1–3 most likely structural failures?

RUN MODE
Manual Higgsfield / connected generation / other provider?

QC
What will be checked when results return?
```

For routine production using a locked preset, this explanation may be shortened; the system should not force verbose reasoning into every run.

---

# 32. Vision Analyzer Role

The Vision Analyzer is a **replaceable execution capability**, not a required always-on agent.

Typical tasks:

```text
reference comparison
image interpretation
pose comparison
identity drift assessment
candidate ranking
image QC
AI artifact detection
```

## 32.1 Default Vision Policy

Default MVP behavior:

```text
Claude visual ingestion: OFF by default
Automatic GPT/API visual calls: OFF by default
Manual external visual review: SUPPORTED / PREFERRED when QC is needed
Duplicate Claude + GPT review: OFF by default
```

The user may manually upload the selected images to GPT and return the result. This path must be treated as a normal production workflow, not as a workaround.

The local system should therefore be able to export a compact **Visual Analysis Packet** containing:

```yaml
task_type: generated_result_qc
character_id: yeoreum
lane: natural_mirror
preset_id: NAT_v1.4.3

assets:
  face_master: <asset_id + local path>
  character_master: <asset_id + local path>
  body_master: <asset_id + local path>
  daily_reference: <asset_id + local path>
  generated_result: <asset_id + local path>

check:
  - identity
  - body_proportions
  - pose
  - framing
  - anatomy_hands
  - camera_realism
  - ai_artifacts

return_schema: VISUAL_QC_V1
```

The packet can also contain a ready-to-copy GPT instruction so the user does not have to reconstruct the QC request manually.

## 32.2 Automatic Vision Policy

If automatic GPT or another hosted vision worker is enabled later:

1. Claude sends only asset IDs/task parameters to the local worker service.
2. The worker resolves local files and calls the visual backend directly.
3. The backend receives only the minimum required images.
4. The worker normalizes the response.
5. Claude receives the compact normalized result, not the original image payload.

Automatic vision calls must be explicit and auditable because they may incur separate model usage/cost.

---

# 33. Claude Role

Claude owns the production logic, but **not necessarily the pixels**.

Claude responsibilities:

```text
request interpretation
canonical-state resolution
context assembly
workflow execution
prompt retrieval/construction
reference-role decisions from known metadata/policies
history/memory retrieval
revision strategy
local tool use
MCP/CLI operation
system development
visual-report interpretation
```

Default restriction:

> Claude should reason from canonical files, asset metadata, prompt state, and normalized visual reports. It should inspect images itself only when the task specifically benefits from Claude vision.

Examples where Claude vision may be justified:

```text
user explicitly asks Claude to visually review the image
external QC is ambiguous or contradictory
optimization audit compares Claude-vs-GPT vision quality
no external/manual visual report is available and visual reasoning is necessary
```

Even then, the system should avoid sending the same full reference set to multiple vision models without a reason.

Claude should not rely on chat memory for canonical facts that exist in local files or the database.

---

# 34. Vision Analysis Contract

All visual-analysis paths — manual GPT, automatic GPT/API, Claude vision, or a future local model — should normalize into the same machine-readable contract.

Example QC result:

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
    daily_reference: DAILY_20260815_004_MASKED
    result: GEN_20260815_004_03

  scores:
    identity: 8.7
    body_proportions: 9.1
    pose: 7.4
    framing: 9.0
    anatomy_hands: 9.3
    camera_realism: 8.5

  major_failures:
    - daily reference보다 hip rotation이 강함
    - face가 master보다 약간 길어짐

  preserve:
    - lighting
    - outfit
    - phone placement
    - background

  recommended_changes:
    - increase daily pose adherence
    - preserve face width and jaw proportions

  decision_hint: REVISE_MINIMALLY
```

The importer should accept either:

- valid structured YAML/JSON directly, or
- human-readable GPT output that is normalized locally into the schema before storage.

Validation requirements:

```text
record which assets were actually compared
record source mode
record timestamp
do not treat missing dimensions as scored
do not silently invent scores from prose
preserve raw external report for audit
store normalized report separately
```

The contract should not expose model-specific prose as permanent system memory without normalization.

---

# 35. MVP Scope

Do **not** automate everything initially.

MVP should implement:

```text
Canonical Manifest
Canonical Source Loader
Asset Catalog
Asset Search
Character + Lane Resolution
Prompt Preset Storage
ProductionRequest
Reference Selection
Daily Reference Preparation
Prompt Retrieval / Creation
Manual Higgsfield Generation Handoff
Visual Analysis Packet Export
Manual External QC Import / Normalization
QC Decision
Minimal Revision
Experiment Logging
User Feedback Memory
```

Automatic Higgsfield generation and multi-provider orchestration come later.

---

# 36. MVP Workflow

```text
USER
natural-language request
        │
        ▼
CLAUDE / CLAUDE CODE
parse request + resolve canonical state
(text + metadata; no image pixels by default)
        │
        ├───────────────┐
        ▼               ▼
ASSET DB           CANONICAL FILES
        │               │
        └───────┬───────┘
                ▼
CLAUDE
select reference IDs + retrieve/build prompt
                │
                ▼
LOCAL VALIDATORS
reference order / prompt length / conflicts
                │
                ▼
USER / HIGGSFIELD
manual generation by default
                │
                ▼
IMPORT RESULTS
                │
                ▼
VISUAL QC NEEDED?
        │
        ├── no ───────────────→ CLAUDE DECISION
        │
        └── yes
             │
             ▼
    EXPORT QC PACKET
             │
      ┌──────┴─────────┐
      ▼                ▼
USER → GPT         EXPLICIT AUTO VISION
(default)              (opt-in)
      │                │
      └──────┬─────────┘
             ▼
IMPORT + NORMALIZE QC REPORT
             │
             ▼
CLAUDE
accept / reject seed / minimal revision
             │
             ▼
DATABASE + FILES
experiment + feedback + validated memory
```

---

# 37. Phase 2 Automation

After the MVP is stable:

```text
MCP server
automatic asset queries
automatic prompt retrieval
automatic experiment creation
automatic QC packet generation
automatic external-report import/normalization
automatic QC logging
automatic reference recommendations from stored metadata/reports
```

---

# 38. Phase 3 Automation

Only after sufficient real usage data exists:

```text
Higgsfield API integration
automatic generation
automatic candidate download
automatic visual QC
automatic regeneration recommendations
batch experiment runner
performance analytics
```

Human approval should remain before expensive or large generation actions.

---

# 39. Important Non-Goals

Do not attempt initially to build:

```text
complex vector database
fully autonomous agent swarm
automatic Instagram publishing
large multi-agent architecture
automatic prompt self-training
heavy cloud infrastructure
```

These increase complexity before enough production data exists.

---

# 40. Recommended Technology Stack

Local-first MVP:

```text
Python
Pydantic
SQLite
local filesystem
Claude Code
MCP Python SDK and/or local CLI
FastAPI only where an HTTP boundary is useful
manual GPT bridge via files/clipboard
```

Recommended design rule:

> Keep domain logic in normal Python services. MCP, CLI, and HTTP layers should be thin adapters.

Optional later:

```text
PostgreSQL
image embeddings
vector search
background job queue
object storage
analytics dashboard
```

Do not add infrastructure until real production volume requires it.

---

# 41. Success Metrics

The automation is successful if it reduces:

```text
Higgsfield generations per approved image
repeated prompt mistakes
manual reference searching
manual prompt reconstruction
time spent comparing failed generations
external vision calls per approved image
duplicate visual processing across models
```

while increasing:

```text
identity consistency
first-test success rate
reference-selection quality
prompt reuse
production repeatability
```

---

# 42. Primary Optimization Target

The main optimization target is **not generation speed**.

It is:

> Approved images per generation attempt.

Secondary optimization:

> Time required to reproduce a successful visual style.

This directly aligns prompt quality, reference selection, QC, and cost efficiency.

---

# 43. Integration With Existing GPT Project Material

Existing project material should be **migrated into structured local sources**, not copied wholesale into a permanent prompt.

Classify each useful item as:

```text
CANONICAL_RULE
CHARACTER_BIBLE
MASTER_ASSET
LANE_POLICY
PROMPT_MODULE
LOCKED_PRESET
USER_PREFERENCE
FAILURE_PATTERN
SUCCESS_RECIPE
EXPERIMENT
DEPRECATED
```

Migration rule:

- approved current behavior → canonical file / preset / validated memory,
- useful but non-canonical learning → scoped success/failure memory,
- obsolete trials → experiment archive only,
- old chats → historical evidence, not runtime context.

The current migration should preserve conclusions that improved production and omit trial paths that were not adopted.

`PROJECT_INSTRUCTIONS_AI_INFLUENCER_v1` is useful as a migration source, but duplicated operational rules should not be loaded alongside the newer Workflow Master on every run. Where the Workflow Master already contains the approved behavior, keep one canonical rule instead of two redundant context sources.

---

# 44. Integration With Claude

Claude should not receive the entire project history on every request.

At runtime, assemble a small context pack from local sources.

Always resolve:

```text
canonical manifest
current user request
selected character
selected lane / preset
```

Then load only what is needed:

```text
relevant Workflow Master sections
Character Bible summary or relevant sections
selected master metadata
selected Daily / Outfit references
locked prompt snapshot or required prompt modules
relevant validated memories
```

Historical experiments are retrieved only when diagnosing a failure, comparing alternatives, or revisiting a prior decision.

This selective context assembly is a core reason for moving away from a monolithic Project-chat memory model.

Image files are not part of the normal Claude context pack. Claude normally receives their asset IDs, paths, metadata, and any existing normalized visual reports. Actual image pixels are attached only for an explicitly selected Claude-vision task.

---

# 45. Source-of-Truth Hierarchy

Runtime conflict resolution:

```text
1. Explicit current user instruction
2. Latest Workflow Master
3. Explicitly selected locked preset / canonical asset for its declared scope
4. Canonical Character Bible / character metadata
5. System Architecture for infrastructure behavior
6. Validated scoped memory
7. Historical experiment
8. Old chat
```

Scope matters. A locked Natural / Mirror preset is authoritative for that lane, but should not silently redefine a future Office or Night preset.

Historical chat must never silently override a newer approved rule.

---

# 46. Immediate Implementation Order

Implement in this order:

```text
01. Canonical manifest + versioned source folders
02. Character / lane / preset schemas
03. Asset metadata schema
04. SQLite database
05. Asset registration + search
06. Canonical source loader
07. ProductionRequest schema
08. Lane reference policies
09. Daily Reference preparation / face-mask derivative support
10. Locked preset retrieval + prompt snapshot validation
11. Generic reference selection logic for unvalidated lanes
12. GenerationPlan schema
13. Vision analysis contract
14. QC schema + result import
15. Experiment logging
16. Feedback + scoped memory
17. MCP / CLI wrappers
18. Optional provider integrations
```

Do not begin with automatic Higgsfield generation. The local control system becomes useful before generation APIs are connected.

---

# 47. Architecture Principle

The final system should behave less like:

> “AI야 프롬프트 만들어줘.”

and more like:

> “이 콘텐츠 목표를 달성하기 위해 현재 보유한 자산과 이전 실험을 분석하고, 가장 효율적인 reference + prompt + generation strategy를 만들어줘.”

The AI is therefore not merely a prompt generator.

It is the **production control layer** for the entire content-generation workflow.

---

# 48. Canonical Natural / Mirror Integration Profile

The completed Natural / Mirror Selfie lane should be migrated into the new local system as a validated profile, not as chat history.

```yaml
lane_policy:
  lane: natural_mirror
  canonical_preset: NAT_v1.4.3
  status: locked

  model:
    provider: higgsfield
    model: seedream_4_5
    max_prompt_length: 3000

  reference_order:
    image1: FACE_ID_MASTER
    image2: CHARACTER_MASTER
    image3: BODY_MASTER
    image4: DAILY_REFERENCE_FACE_MASKED

  priority:
    - face_identity
    - daily_pose_composition
    - body_proportions
    - character_continuity
    - outfit
    - anatomy
    - smartphone_realism
    - lighting_skin

  pose_policy:
    reference_led: true
    invent_new_pose: false

  face_policy:
    preserve_identity: true
    copy_master_expression: false
    adapt_gaze_head_angle_perspective: true

  outfit_policy: preset_defined

  refinement_policy:
    mandatory_second_pass: false
```

This profile captures the usable conclusions of the completed testing without importing the abandoned trial paths.

---

# 49. Character Bible Integration

`CHARACTER_BIBLE_YEOREUM_v1.1` is a canonical character source and should influence content planning, scene selection, wardrobe logic, expression range, and QC for character consistency.

Minimum structured character metadata:

```yaml
character:
  id: yeoreum
  display_name: Han Yeoreum
  adult: true
  age: 19

  core_persona:
    - quiet
    - introverted
    - homebody
    - nerd_interests
    - more_confident_online_than_offline

  visual_formula:
    - soft_face
    - curvy_silhouette
    - ordinary_adult_life
    - slightly_daring_styling

  expression_range:
    - soft_neutral
    - tiny_smile
    - side_glance
    - shy_chin_down
    - relaxed_candid
    - slightly_confident

  primary_content_pillars:
    home_just_outside: 45
    outfit_fitting_mirror: 20
    university_quiet_day: 15
    nerd_lifestyle: 10
    cosplay_special: 10
```

Important system constraints:

- maintain clearly adult presentation,
- do not lock one expression across all images,
- avoid turning the character into a generic party/luxury/studio-model persona,
- use ordinary-life locations and recurring habits when they support the requested content,
- content planning should reflect gradual confidence rather than sudden personality replacement.

The full Bible should be loaded only when narrative or content-planning details are needed; routine prompt generation can use a compact structured summary plus relevant sections.

---

# 50. Canonical Manifest

Use one small human-readable manifest to resolve the current project state deterministically.

Example:

```yaml
project: AI_Influencer_Studio

workflow_master: canonical/workflow/00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt

characters:
  yeoreum:
    bible: canonical/characters/yeoreum/CHARACTER_BIBLE_YEOREUM_v1.1.txt
    masters:
      face_id: <asset_id>
      character: <asset_id>
      body: <asset_id>

lanes:
  natural_mirror:
    preset: NAT_v1.4.3
    policy: canonical/presets/natural_mirror/lane_policy.yaml

presets:
  NAT_v1.4.3:
    status: locked
    prompt: canonical/presets/natural_mirror/NAT_v1.4.3_LOCKED_PROMPT.txt
```

The manifest should be the first local source Claude reads when resolving a production request.

---

# 51. Daily Reference Preparation

Daily References should remain non-canonical production inputs, but preprocessing must be reproducible.

Recommended flow:

```text
raw Daily Reference
→ register asset
→ assess identity-conflict risk
→ create derived face-masked copy when required
→ retain raw + derived provenance
→ use derived asset in GenerationPlan
```

Never overwrite the raw reference.

Store:

```yaml
derived_from: <raw_asset_id>
transformation: face_mask
face_masked: true
created_at:
```

For `NAT_v1.4.3`, the GenerationPlan validator should fail if `@image4` is not the required face-masked Daily Reference derivative.

---

# 52. Context Assembly Rule

The local automation should solve the main limitation of chat-project systems by separating **canonical knowledge** from **retrieved working context**.

Per request, build a context bundle containing only:

```text
current request
canonical manifest resolution
relevant workflow rules
character summary
selected lane/preset
selected asset metadata
selected prompt snapshot/modules
relevant validated memories
```

Do not automatically inject:

```text
all old chats
all failed experiments
all prompt versions
all character-bible prose
all assets
```

The system should be retrieval-driven, not conversation-history-driven.

---

# 52.1 Visual Token / Cost Control Policy

The system should optimize visual-model usage independently from text-context usage.

Core rules:

```text
1. Store images once; reference them by asset ID/path.
2. Do not place master/reference images in persistent Claude context.
3. Do not automatically send the same images to both Claude and GPT.
4. Automatic external vision calls are opt-in.
5. Manual GPT review is a supported default QC path.
6. Return compact structured reports to Claude.
7. Deep multi-reference comparison is reserved for shortlisted candidates or disputed failures.
8. Reuse prior valid analyses when the underlying asset has not changed.
```

Recommended staged QC:

```text
Stage 0 — deterministic / metadata validation
  file exists, reference order, prompt length, preset compatibility

Stage 1 — cheap/manual candidate triage
  identify obviously broken candidates without repeated full-reference analysis

Stage 2 — deep visual compare
  only shortlisted candidate(s): FACE + BODY + DAILY + RESULT as needed

Stage 3 — second opinion
  Claude + GPT duplicate review only when ambiguity or optimization benchmarking justifies it
```

A manual GPT workflow should not require any OpenAI API integration. The local system merely exports the task packet and imports the returned analysis. If a future GPT API/connector is enabled, it must expose per-call logging so the user can distinguish automatic model usage from manual review.

---

# 53. Reproducibility & Audit Trail

Every generated candidate should be reproducible from a stored `GenerationPlan`.

Minimum provenance:

```yaml
generation_plan_id:
created_at:
character_id:
lane:
preset_id:
preset_prompt_hash:
model:
reference_asset_ids:
reference_order:
prompt_text:
user_overrides:
parent_experiment_id:
```

When a result is approved, the approval record should point back to this plan. This makes it possible to reproduce a successful style without relying on memory or reconstructing the prompt from chat.

---

# 54. v0.2 Integration Changelog

This revision integrates the current approved project state into the local Claude-first architecture:

- updated canonical workflow target to `00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2`,
- added canonical FACE ID + CHARACTER + BODY three-master architecture,
- encoded the validated four-reference Natural / Mirror profile,
- added face-masked Daily Reference preparation and provenance,
- added deterministic reference order and current priority hierarchy,
- preserved natural expression adaptation instead of fixed master-expression copying,
- made `NAT_v1.4.3` an immutable locked prompt snapshot,
- removed the assumption that every lane should minimize reference count after a lane has already been validated,
- removed the assumption of a mandatory second refinement pass,
- changed GPT from a required visual agent to an optional vision backend,
- made manual user-operated GPT QC a first-class path with no required automatic API integration,
- added visual-context isolation so Claude manages asset IDs/metadata without ingesting image pixels by default,
- prohibited duplicate Claude + GPT visual processing by default,
- added portable QC packet export/import and normalized visual-report contracts,
- made Claude / Claude Code the primary local orchestrator,
- added Character Bible integration and scoped character metadata,
- added canonical manifest, selective context assembly, and reproducible GenerationPlan provenance,
- kept Higgsfield generation manual by default and explicit when connected tools may consume credits,
- kept non-adopted experiments in history rather than promoting them into canonical runtime rules.



---

# Changelog

## v0.2.1

- Reframed `locked` presets as immutable benchmark artifacts rather than permanently unquestionable strategies.
- Added Production Mode vs Optimization Audit Mode.
- Kept NAT_v1.4.3 four-reference structure as the current validated production baseline.
- Explicitly allowed Claude to re-test reference count, reference order, masking policy, and prompt architecture.
- Added an optimization-audit record and controlled-comparison protocol.
- Prevented optimization from silently mutating the approved baseline.

## v0.2.2

- Added a token/cost-aware vision architecture.
- Changed Claude's default visual behavior to metadata/report orchestration rather than repeated pixel ingestion.
- Set automatic GPT/API visual analysis to OFF by default for the MVP.
- Made manual user-operated GPT image review a first-class supported workflow.
- Added Visual Analysis Packet export and external QC import/normalization.
- Added a normalized `VISUAL_QC_V1` contract so Claude can act on compact QC data.
- Added the rule that the same image set must not be sent to Claude and GPT by default.
- Added staged visual QC and explicit second-opinion escalation.
- Added cost-efficiency metrics for external vision calls and duplicate visual processing.

