# CASE_03_STRICT_DAILY_REFERENCE_5LITE

## Generation metadata
```json
{
  "job_id": "ae053be5-933e-4c95-ad68-432db90bea20",
  "model": "seedream_v5_lite",
  "seed": 179015,
  "quality": "high",
  "aspect_ratio": "9:16",
  "width": 2304,
  "height": 4096
}
```

## Reference roles
- @Image1: PRIMARY identity + hairstyle + body proportions + chest volume + waist/hips + exact outfit
- @Image2: STRICT background + lighting + color tone + exposure + depth + atmosphere + pose + composition

## Reference image manifest
- `01_MASTER_IMAGE.png` — https://d8j0ntlcm91z4.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/hf_20260812_022154_7764fb92-8abc-427e-b838-e3076929f67e.png
- `02_DAILY_SCENE_POSE.jpg` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/c67091cc-ce89-42c6-8a3f-64d3721cef44.jpg

- Output — https://d8j0ntlcm91z4.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/hf_20260815_043936_ae053be5-933e-4c95-ad68-432db90bea20.png

## Original prompt
```text
Use @Image1 as the PRIMARY reference for the clearly adult woman’s identity, hairstyle, body proportions, chest volume, waist, hips, and exact outfit.

Use @Image2 as the STRICT reference for background, lighting, color tone, exposure, depth, overall photo atmosphere, pose, and composition. Do not copy @Image2’s person, face, body shape, hairstyle, or clothing.

Create one NEW realistic 4:5 vertical Instagram phone-camera photo. Output the photograph itself, not a phone screen, mockup, UI, or screenshot.

IDENTITY:
Keep her clearly recognizable as the same woman from @Image1. Preserve core facial structure, proportions, skin tone, bangs, hairstyle, and hair color. Do not copy @Image1’s exact expression, gaze, head angle, eye openness, or mouth position. Adapt the same identity naturally to the new setting so the face does not look pasted or frozen.

EXPRESSION:
Give her a fresh natural expression that fits @Image2’s environment and mood. Keep relaxed brows and jaw, soft eyes, natural lips, and a subtle candid feeling. Identity stays from @Image1; expression may change naturally.

BODY / OUTFIT:
Preserve @Image1’s shoulder-to-torso ratio, chest-to-torso ratio, waist, hips, legs, and overall silhouette. Do not make her slimmer, flatter, smaller, or more generic.
Recreate @Image1’s outfit faithfully: same design, neckline, shoulder coverage, sleeves/straps, fabric, texture, color, fit, and length. Do not borrow clothing from @Image2.

PHYSICS:
Preserve @Image1’s original chest volume. Make it physically believable with natural gravity, softer lower fullness, less artificial upper lift, mild natural asymmetry, and realistic attachment to the torso. Avoid perfectly round, rigid, identical, or molded shapes. Let the outfit show slight stretch, uneven tension, soft drape, small irregular folds, and subtle compression.

POSE / COMPOSITION:
Stay very close to @Image2’s pose and composition. Keep the same general body arrangement, camera direction, framing, subject scale, and pose mood. Allow only minor natural variation needed to fit @Image1’s body and outfit. Do not dramatically change the pose or invent a new one. Keep hands and limbs simple, visible, and anatomically clear.

SKIN:
Keep skin clean and attractive but realistically photographed: fine pores, subtle microtexture, and natural highlight breakup. Do not add freckles, moles, acne, scars, blemishes, or redness. No waxy/plastic skin, heavy smoothing, HDR, glossy CGI finish, or commercial retouching.

PRIORITY:
@Image2 controls background, lighting, atmosphere, pose, and composition.
@Image1 controls identity, body, and outfit.

Exactly one woman. Natural anatomy. No duplicate limbs, malformed hands, broken legs, body morphing, text, watermark, phone frame, UI, or collage.
```

## User feedback
What worked:
- The master character was transferred into Image2's photographed environment/background well.
- Image2's overall scene and photographic context were followed well.

Model trade-off observed by user:
- Seedream 5 Lite often does NOT follow the reference pose closely enough.
- That looser adherence can be useful when avoiding duplicated-looking images, but is a weakness when exact pose replication is desired.
- Seedream 4.5 follows the reference pose very well.
- However, Seedream 4.5 can freeze the face too strongly and make facial/skin characteristics excessively consistent, to the point of looking copied-and-pasted.

Claude note:
- This is not a simple '5 Lite good / 4.5 bad' comparison.
- 5 Lite advantage: more variation / less duplication.
- 5 Lite weakness: weaker pose fidelity when exact matching is required.
- 4.5 advantage: high pose fidelity.
- 4.5 weakness: over-fixed face and over-consistent skin/rendering.
- Future prompt/model routing should distinguish 'exact pose replication' from 'reference-inspired variation' as separate generation intents.
