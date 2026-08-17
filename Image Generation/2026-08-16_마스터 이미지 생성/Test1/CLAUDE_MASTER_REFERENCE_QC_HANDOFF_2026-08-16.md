# Claude Prompt-Direction QC Handoff

## Overall
Current test is **not ready to lock as the final Master Reference prompt**.

The generation is structurally stable across seeds, but two repeated failures are significant enough to require another revision.

## Priority Findings

### 1. Skin / Rendering — High Priority
Across all three outputs, skin is too uniform and polished.

Observed tendency:
- reduced local tonal variation
- overly clean face/neck/body transitions
- smooth cosmetic finish
- slight doll-like / generic AI-beauty impression

This is not primarily a geometry failure. The character remains recognizable, but the rendering style weakens character-specific realism.

**Direction for Claude:** preserve identity stability while reducing Seedream's beauty-normalization tendency. Target attractive photographic skin rather than polished virtual-model skin.

### 2. Outfit Reference Fidelity — High Priority
The model understands the outfit category but does not preserve the exact garment design closely enough.

It reproduces:
- black sleeveless bodysuit-like garment
- denim shorts
- fishnet stockings

But it reinterprets:
- neckline
- strap / upper-chest construction
- torso shaping
- waist / leg-opening geometry
- shorts rise, placement, silhouette, and construction

The result behaves more like **"an outfit inspired by the reference"** than **"the same garment transferred onto the character."**

**Direction for Claude:** increase garment-design preservation and reduce model-side fashion reinterpretation.

## Secondary Finding
Body proportions show some drift toward stronger bust projection, narrower waist, and a more exaggerated hourglass silhouette.

This should remain a secondary correction target for the next iteration. Do not let body correction destabilize the currently strong identity/anatomy consistency.

## What Already Works — Preserve
- strong seed-to-seed character consistency
- stable facial family
- stable long black hairstyle
- clean anatomy
- neutral master-reference presentation
- simple background
- useful frontal and 3/4 angle readability
- correct recognition of the outfit as multiple separate garment layers

## Next Test Should Be Judged On
1. More natural skin and tonal variation
2. Higher exact Outfit Reference fidelity
3. Same or better facial consistency
4. Same anatomical stability
5. No worsening of body drift

## Decision
**REVISE — DO NOT LOCK YET**

Summary:
**Structural success, but rendering and Outfit Reference fidelity are not yet Master-level.**
