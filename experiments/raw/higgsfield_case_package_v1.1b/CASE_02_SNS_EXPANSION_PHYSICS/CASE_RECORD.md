# CASE_02_SNS_EXPANSION_PHYSICS

## Generation metadata
```json
{
  "job_id": "b6ee5760-ceb2-434d-b04b-c7c592723759",
  "model": "seedream_v4_5",
  "seed": 289996,
  "quality": "basic",
  "aspect_ratio": "9:16",
  "width": 1440,
  "height": 2560,
  "use_unlim": true
}
```

## Reference roles
- @Image1: PRIMARY identity + hairstyle + body proportions + chest volume + waist/hips + exact outfit
- @Image2: declared as background/lighting/color/depth/SNS mood only; NOT present as a stored input in the job record

## Reference image manifest
- `01_MASTER_IMAGE.png` — https://d8j0ntlcm91z4.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/hf_20260812_022154_7764fb92-8abc-427e-b838-e3076929f67e.png

- Output — https://d8j0ntlcm91z4.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/hf_20260815_032606_b6ee5760-ceb2-434d-b04b-c7c592723759.png

## Original prompt
```text
Use @Image1 as the PRIMARY reference for the clearly adult woman’s identity, hairstyle, body proportions, chest volume, waist, hips, and exact outfit.
Use @Image2 ONLY for background, lighting, color tone, depth, and SNS mood. Do not copy @Image2’s person, face, body, clothing, or pose.

Create one NEW realistic 4:5 vertical phone-camera photo for a contemporary Korean influencer Instagram feed. Output the photograph itself, not a phone screen, mockup, bezel, UI, or screenshot.

IDENTITY:
Keep her clearly recognizable as the same woman from @Image1, but naturally photographed in a new moment. Preserve core facial structure, proportions, skin tone, bangs, hairstyle, and hair color. Do NOT copy @Image1’s exact expression, gaze, head angle, eye openness, or mouth position. Adapt the same identity naturally to the new angle so the face does not look pasted or frozen.

BODY / OUTFIT:
Preserve @Image1’s shoulder-to-torso ratio, chest-to-torso ratio, waist, hips, legs, and silhouette. Recreate @Image1’s outfit faithfully: same design, neckline, sleeves/straps, fabric, texture, color, and length.

PHYSICS:
Keep @Image1’s original chest volume, but make it physically believable: gravity-driven distribution, softer lower fullness, less artificial upper lift, mild natural asymmetry, and realistic attachment to the torso. Avoid perfectly round, rigid, identical, or molded shapes. The outfit reacts with slight stretch, uneven tension, soft drape, small irregular folds, and subtle compression.

POSE:
Create a natural Korean-influencer-style candid pose, not either reference pose. Prefer a seated or slightly leaning three-quarter pose with relaxed asymmetric shoulders, one shoulder slightly closer to camera, natural waist line, and balanced hips. Keep arms simple: one hand resting beside the body, thigh, or seat; the other relaxed near the torso or lightly touching hair. No arm reaches toward the lens. Avoid extreme twisting, hidden hands, or difficult foreshortening.

EXPRESSION:
Relaxed brows and jaw, soft eyes, naturally relaxed lips, gaze near camera or slightly off-camera. Attractive and confident, but casual and unposed.

MOOD / LIGHTING:
Dim apartment or bedroom at night, one small warm lamp in the background, soft neutral light on the subject, darker simple background. Slightly imperfect exposure, subdued saturation, gentle low contrast, soft highlight roll-off, mild low-light grain, subtle compression, and slight optical softness. Restrained vintage-digicam influence.

SKIN:
Keep skin clean and attractive but photographed, not rendered: fine pores, subtle microtexture, natural highlight breakup. Do not add freckles, moles, acne, scars, blemishes, or redness. No waxy/plastic skin, beauty-filter smoothing, HDR, studio lighting, cinematic rim light, glossy CGI finish, or commercial retouching.

Exactly one woman. Natural anatomy. No duplicate limbs, malformed hands, broken legs, body morphing, text, watermark, phone frame, UI, or collage.
```

## User feedback
What worked:
- PHYSICS section seems somewhat better than variants without it.
- Pose and expression are not frozen to the master.
- Natural variation in pose/gaze/expression/angle is useful.
- Some generations fail, but batch generation can yield usable images.

Weaknesses / hypothesis:
- The master itself already looks AI-generated, so downstream artificial skin/body/chest traits may be inherited.
- If upstream master quality improves, downstream realism may improve too.
- Background atmosphere and lighting do not consistently fit the intended character concept.
- Preserve pose/expression freedom; revise environment/lighting direction later.

Diagnostic:
Pose/expression variation is working. Main bottlenecks are upstream master realism and downstream environment/lighting alignment.
