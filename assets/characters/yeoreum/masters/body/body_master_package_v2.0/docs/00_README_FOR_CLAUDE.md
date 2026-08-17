# Han Yeoreum BODY MASTER PACKAGE v2.0

Status: candidate canonical body package approved through manual visual QC in ChatGPT.
Character: Han Yeoreum / 한여름, clearly adult age 19.

## Critical authority rule

`01_PRIMARY/02_BODY_MASTER.jpg` is the **only canonical body-dimension authority** in this package.
It defines the stable baseline for:
- shoulder / torso ratio
- torso length
- bust / waist / hip relationship
- pelvis width
- thigh volume
- leg proportions
- overall silhouette

All other images are **support views of the same body**, not separate body identities.
They must never redefine the canonical dimensions merely because a pose causes compression, spread, perspective, or gravity deformation.

## Priority inside this package

1. `02_BODY_MASTER.jpg` — canonical baseline geometry
2. Core-view support — angle/depth evidence
3. Pose support — deformation/physics evidence only

## Production compatibility

The current locked NAT_v1.4.3 lane still expects one BODY MASTER at `@image3`.
For that locked lane, replace the old canonical `02_BODY_MASTER.jpg` with this package's new `01_PRIMARY/02_BODY_MASTER.jpg` only after explicit approval.

Do **not** automatically add the whole support package to every NAT_v1.4.3 generation. The support images are intended for:
- body QC,
- pose-specific consistency checks,
- repair/reference selection,
- a future pose-aware body-selector workflow if explicitly promoted to canonical.

## Rejected material

The previously generated glamour-biased single quadruped/cat-like pose was intentionally excluded because it exaggerated lumbar arch, waist reduction, and glute projection relative to the baseline body.
