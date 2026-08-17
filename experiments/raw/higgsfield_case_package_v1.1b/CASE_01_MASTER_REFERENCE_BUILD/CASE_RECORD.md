# CASE_01_MASTER_REFERENCE_BUILD

## Generation metadata
```json
{
  "job_id": "15a63f5b-5d8b-48cb-8201-e6652a53d786",
  "model": "seedream_v4_5",
  "seed": 4694,
  "quality": "basic",
  "aspect_ratio": "9:16",
  "width": 1440,
  "height": 2560,
  "use_unlim": true
}
```

## Reference roles
- Image 1: PRIMARY FACE
- Images 2-3: SECONDARY FACE only
- Images 4-6: BODY only
- Image 7: OUTFIT only

## Reference image manifest
- `01_PRIMARY_FACE.png` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/de584799-32ed-4af9-a9c0-34ddc0696212.png
- `02_SECONDARY_FACE.png` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/71f7513a-8441-4a1f-9484-20eca75da3b2.png
- `03_SECONDARY_FACE.png` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/41cb318f-73b6-4c10-aa69-ff2c0b9d52fb.png
- `04_BODY.png` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/b124d771-78b7-484e-9d76-3c81da7aa71b.png
- `05_BODY.png` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/93585eca-9304-4974-a4a3-55e20bc7688a.png
- `06_BODY.png` — https://d8j0ntlcm91z4.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/hf_20260730_004316_bbb2751c-fd6d-400d-a45c-1c9c86465c16.png
- `07_OUTFIT.jpg` — https://d2ol7oe51mr4n9.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/7246604b-923e-4fcf-944e-f1fcab093bca.jpg

- Output — https://d8j0ntlcm91z4.cloudfront.net/user_3GsQORcAE7g4Hbm1E3wyT14lIUK/hf_20260812_022544_15a63f5b-5d8b-48cb-8201-e6652a53d786.png

## Original prompt
```text
Use Image 1 as the primary face reference.
Use Images 2-3 as secondary face references only.
Use Images 4-6 as the only body references.
Use Image 7 as the outfit reference only.

Create exactly one realistic 4:5 vertical master reference photo of the same clearly adult woman from Images 1-3.

Purpose: a clean master reference image. Face, hairstyle, body proportions, torso silhouette, waist, hips, legs, and full outfit must be clearly visible.

Show one woman only. No duplicates, multiple people, collage, split screen, contact sheet, multi-panel layout, or multiple poses.

FACE: Preserve the same identity from Images 1-3, prioritizing Image 1: face shape, proportions, eyes, brows, nose, lips, jawline, cheeks, forehead, skin tone, age, ethnicity, hairline, bangs, hair length, and hair color. Do not average, morph, redesign, beautify, or copy the portrait mood from the face references.

BODY: Images 4-6 are the only source of body shape. Preserve shoulder width, torso length, upper-body proportions, waist, hips, legs, and overall silhouette. Image 7 must not change body shape. Do not make the body slimmer, flatter, smaller, or more generic than Images 4-6.

OUTFIT: Use Image 7 only for garment type, neckline, straps, seams, fabric, texture, color, length, and design details. Do not copy Image 7's body, pose, or silhouette. Transfer the outfit onto the body defined by Images 4-6. Keep the outfit visible and unchanged. Do not add layers, accessories, bags, hats, jewelry, or props.

POSE: Use a simple neutral reference pose. The woman stands upright in a relaxed natural stance. Face, chest, waist, hips, and legs face mostly toward the camera. Use a front-facing or near-front-facing angle only, with at most a slight natural turn. Arms relaxed, visible, and not covering the torso or outfit. Do not use side profile, strong side turn, back-turned pose, seated pose, lying pose, leaning pose, crouching pose, selfie pose, mirror pose, hand-on-face pose, fashion pose, or special gesture.

SCENE: Use a clean, simple, natural indoor background with soft even lighting. The background should be plain, believable, and unobtrusive. Do not include a phone, mirror, camera, large furniture blocking the body, busy decorations, strange objects, dramatic lighting, cinematic mood, or stylized set.

STYLE: The image should look like a clear natural reference photo, not a selfie, ID photo, passport photo, studio portrait, beauty shoot, fashion editorial, magazine image, or cinematic image.

Maintain realistic skin texture, natural shadows, realistic fabric folds, subtle camera noise, and restrained processing.

Avoid waxy skin, beauty-filter smoothing, artificial glow, excessive sharpness, distorted anatomy, extra fingers, duplicated limbs, cropped body parts, covered face, covered torso, face change, hairstyle change, body change, outfit redesign, or multiple subjects.

Generate one complete 4:5 vertical single-subject photograph only.
```

## User feedback
What worked:
- Very good at combining the intended character identity, intended body shape, and desired outfit.
- Straight, stable, neutral pose is good enough for Character Reference / Master Reference use.
- Face/body/outfit role separation works well.

Weaknesses:
- Reference-heavy: 3 face refs + 3 body refs.
- Body and skin can look AI-generated.
- Biggest issue is chest/bust physics: figurine-like or molded appearance; poor gravity/soft-tissue behavior and weak garment interaction.

Claude note:
- Preserve the successful identity + body + outfit assembly and reference-friendly neutral pose.
- Optimize upstream realism, especially skin/body/chest physics.
- Investigate whether fewer references can retain the same control.
- Do not treat GPT's discarded revision proposal as part of this case.
