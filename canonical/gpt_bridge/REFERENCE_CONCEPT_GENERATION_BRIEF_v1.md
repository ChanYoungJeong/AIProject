# Reference & Selfie Concept Generation Brief — Claude ↔ GPT Bridge (v1)

Source: migrated from real project sources (`CHARACTER_BIBLE_YEOREUM_v1.1.txt`,
`00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt` §8) and
`AI_Influencer_Studio_System_Architecture_v0.2.2.md` §6, §7, §9.

## 0. Purpose and scope

This bridge is for **generating new candidate concept/reference images** with GPT when
building out Han Yeoreum's reference library — mirror-selfie concepts, outfit-fitting shots,
daily-life scene ideas. It is **not** the production path: real generation still goes through
Higgsfield manually with the locked `NAT_v1.4.3` prompt (`canonical/presets/natural_mirror/`).
Anything GPT produces here is a **candidate** for human review — never auto-registered as a
canonical asset, never fed into a `GenerationPlan` without going through
`app/services/asset_registry.py`'s explicit `set_approval_state` step.

## 1. Character brief (Character Bible §1–2, §11)

Han Yeoreum, 19, adult. Quiet, introverted homebody — more comfortable at home than in
crowded places. Nerdy interests: games, manga/anime, books, online shopping. Shy in person,
noticeably more confident online than offline. Aware her figure draws attention; used to avoid
fitted clothes because of it, but always liked pretty clothes/styling itself — gradually
accepting her appearance through solo Instagram fitting photos. **She is not someone who
suddenly became bold — she is gradually becoming bolder.**

Visual formula: `Soft face × Curvy silhouette × Ordinary adult life × Slightly daring styling`

Content pillars to draw concepts from (Character Bible §11 — match this mix, don't invent a
generic influencer mix):

```text
45% Home / Just Outside — home, entrance, elevator, hallway, laundry room, convenience store
20% Outfit Fitting / Mirror — trying new clothes/styles, package-unboxing → fitting → mirror photo
15% University / Quiet Day — class, study, bookstore; more modest, realistic student styling
10% Nerd Lifestyle — games, books, anime goods, hobby space
10% Cosplay / Special — rare, needs an in-story reason (see §5)
```

## 2. Identity & body lock — hard constraints

Attach `FACE_ID_MASTER`, `CHARACTER_MASTER`, and `BODY_MASTER` (the real registered assets:
`FACE_YEOREUM_V1`, `CHARACTER_YEOREUM_V1`, `BODY_YEOREUM_V1`) as the only identity/body source.
GPT must match these, not invent a new person who merely fits the persona description.

**Do not generate, under any circumstance:**

- underweight / visibly thin proportions that don't match `BODY_MASTER`
- overweight proportions that don't match `BODY_MASTER`
- unnaturally elongated limbs/torso or fashion-illustration proportions (exaggerated leg
  length, stretched waist-to-hip ratio) — Architecture §9.1: body proportions come from
  `BODY_MASTER` and must stay internally coherent and visually believable, not stylized
- a different face shape, jawline, or eye spacing than `FACE_ID_MASTER`
- a different hair color/style or skin tone than `CHARACTER_MASTER`
- an exaggerated hourglass or waxy/synthetic "AI-beauty" body that reads as generic rather
  than as this specific character

If GPT cannot see or match the attached body/face proportions closely enough to be confident,
it should say so rather than guess.

## 3. Identity/likeness safeguard

Draw on the **genre conventions** of natural Instagram / mirror-selfie photography (see §4) —
never attempt to replicate any specific real individual's face, body, or identity. All
identity/body must come from the three attached master images only. Do not name, describe, or
imitate any real public figure or influencer as a reference.

## 4. Adult-character safeguard (Workflow Master §3.7, Character Bible §3)

Han Yeoreum is a clearly adult 19-year-old. Every generated concept must:

- read as clearly adult in framing, styling, and context — never age-ambiguous or minor-coded
- use university/adult-education framing for any school-adjacent content, never school-uniform
  or under-18 cues
- avoid childlike posing, expressions, or environments

## 5. Natural Instagram genre baseline (Workflow Master §8)

```text
Camera:  ordinary smartphone-photo perspective, mild phone-camera softness,
         minimal digital sharpening, mild compression, no CGI-clean finish
Lighting: soft indirect daylight (or one believable practical light at night),
          slightly imperfect exposure, low-to-moderate contrast
Skin:    clean healthy skin with subtle tonal variation, no exaggerated pores,
         no waxy/plastic finish, no heavy beauty-filter look
Color:   warm-neutral white balance, subdued-to-normal saturation
Mood:    candid Instagram post — natural asymmetric posture, relaxed body language,
         believable garment tension/folds, simple uncluttered background
```

Sensuality (Workflow Master §3.6, §3.9) should come from pose, crop, styling, gaze, and
context — not exaggerated anatomy. A more revealing pose/outfit is only acceptable if it still
looks like believable photography, not synthetic glamour art.

### 5.1 Photorealism target — it should read as a real photo, not an AI render

The specific quality to aim for: even labeled as an AI influencer, the image should still read
as an actual photo of an actual person. Five dimensions matter most:

```text
POSE     Natural, slightly imperfect weight distribution and asymmetry — not a symmetric,
         camera-aware "model pose." Should look like a candid mid-moment (as if she didn't
         perfectly time the shutter), not a held studio pose.

LOCATION Real, lived-in spaces with authentic small imperfections — a visible cord, a slightly
         messy shelf, real bathroom/bedroom clutter — not a swept, staged, magazine-clean room.
         Consistent with her actual life radius (home, elevator, convenience store, laundry
         room, campus).

GAZE     Vary it — not always a locked, camera-aware stare. Sometimes at her phone screen, at
         her own mirror reflection, slightly downward or to the side, a natural middle-
         distance look. When she does look at camera, it should read as a quick candid glance,
         not a held gaze.

LIGHTING Match the light sources actually present in that specific scene (a single overhead
         bulb, window daylight, phone-flash bounce, convenience-store fluorescent) rather than
         idealized multi-point studio lighting. Slight color-temperature inconsistency and
         imperfect exposure across the frame is correct, not a flaw.

SKIN     The single biggest AI tell. Visible natural pore texture, believable minor tonal
         unevenness, natural shine/matte variation — must hold up at close crop. Never flatten
         into a smooth, uniform "beauty filter" plane; never waxy or plastic.
```

General AI-artifact avoidance: no unnaturally perfect facial symmetry, no uniformly "flawless"
studio polish, no perfectly matched color grading across skin/hair/background, no hyper-sharp
fine detail that reads as upscaled or rendered rather than photographed.

## 6. Cosplay concepts (10% pillar) — needs a reason (Character Bible §9)

Only generate cosplay/themed concepts with an in-story reason attached (ordered because of a
favorite character, deciding whether to go to an event, game-character-inspired outfit,
seasonal event, streaming outfit, post-unboxing test) — not a standalone "costume shoot."
Preferred directions: fantasy, gothic, witch, cat-inspired, bunny-inspired, sci-fi,
game-character-inspired, dark feminine, themed lounge look. Confidence progression for staging:
room → entryway → elevator → parking lot → actual event.

## 7. Character breakers — do not generate (Character Bible §15)

```text
sudden party-girl energy                    luxury/celebrity lifestyle framing
the same expression in every concept        a permanently "seducing the camera" look
cosplay with no reason                      professional-studio-model repetition
content that reduces her to body-only       overly depressing/self-pity framing
```

Expression should vary across a set (Character Bible §13): soft neutral, tiny smile, side
glance, shy/chin-down, relaxed candid, slightly confident — same recognizable person underneath.

## 8. Copy-paste template — concept batch generation

Attach `FACE_ID_MASTER`, `CHARACTER_MASTER`, `BODY_MASTER` (and an `OUTFIT_REFERENCE` if you
have a specific garment in mind) before pasting.

---

You are generating candidate reference/concept photos for an AI-influencer character named
Han Yeoreum — a clearly adult 19-year-old, quiet/introverted homebody with nerdy interests
(games, manga, books, online shopping), gradually gaining confidence about her appearance
through solo Instagram fitting photos. Visual formula: soft face × curvy silhouette × ordinary
adult life × slightly daring styling.

Identity and body must match the attached FACE_ID_MASTER, CHARACTER_MASTER, and BODY_MASTER
images exactly — do not invent a different face, hair, skin tone, or body proportions. Do not
generate her underweight, overweight, or with unnaturally elongated/stylized limb or torso
proportions — proportions should look like the same coherent, believable person as the
attachments, not a fashion-illustration body. Do not reference or imitate any real public
figure; use only the attached images for identity.

She is clearly adult — never age-ambiguous, never school-uniform/minor-coded, even in
university-day content (use adult-education framing instead).

Generate [N] concept photos across this mix, matching her real content pillars — don't default
to a generic influencer mix:
- Home / just outside (elevator, hallway, convenience store, laundry room) — the largest share
- Outfit fitting / mirror selfie — trying on new clothes, package just arrived
- University / quiet day — modest, realistic student styling (cardigan, knit, jeans, hoodie),
  not the daring Instagram-experiment look
- Nerd lifestyle — games, books, anime goods, hobby space visible in frame
- (only if requested) cosplay/themed — only with an in-story reason, never a standalone shoot

Style: natural Instagram/mirror-selfie realism — ordinary smartphone-camera perspective, mild
phone softness, soft indirect daylight or one practical light at night, slightly imperfect
exposure, low-to-moderate contrast, clean skin with natural tonal variation, no beauty-filter
or studio-glamour look, simple uncluttered background. Vary expression and pose across the set
(soft neutral, tiny smile, side glance, shy/chin-down, relaxed candid, slightly confident) —
never the same expression twice, never a fixed "seducing the camera" look.

It should read as an actual photo of an actual person, not an AI render, even though it's
labeled AI-generated. Specifically:
- Pose: natural, slightly imperfect weight distribution, candid mid-moment — not a symmetric,
  camera-aware model pose.
- Location: a real, lived-in space with authentic small imperfections, not a staged, swept-
  clean room.
- Gaze: vary it — phone screen, mirror reflection, slightly off-camera, natural middle
  distance — not always a locked, camera-aware stare.
- Lighting tone: match the light actually present in that scene (one bulb, window daylight,
  fluorescent), with the slight color-temperature and exposure imperfection a real phone
  camera produces — not idealized studio lighting.
- Skin texture: visible natural pore texture and believable minor tonal unevenness that holds
  up at close crop — never a smooth, uniform "beauty filter" plane.

Avoid: party-girl energy, luxury/celebrity framing, professional-studio-model repetition,
content that reduces her to body only, self-pity framing, cosplay without a stated reason.

For each generated image, give a short caption with:
```text
content_pillar: [home_just_outside | outfit_fitting_mirror | university_quiet_day | nerd_lifestyle | cosplay_special]
pose_type / expression: [...]
environment: [...]
outfit_mode: [auto-designed | matches attached OUTFIT_REFERENCE]
one-line concept description
```

---

## 9. After generation — review, don't auto-adopt

Every candidate is reviewed before it becomes anything more than a suggestion:

```text
APPROVE_FOR_LIBRARY     — matches identity/body/character; register as a candidate
                          Daily/Outfit/Style reference via asset_registry.register_asset
                          (approved=False, canonical=False until explicitly promoted)
APPROVE_WITH_EDIT       — concept is right, but needs a redo (lighting, pose, crop)
REJECT_BODY_MISMATCH    — proportions drift from BODY_MASTER (too thin/heavy/elongated)
REJECT_IDENTITY_DRIFT   — face/hair/skin drifts from FACE_ID_MASTER / CHARACTER_MASTER
REJECT_CONCEPT_MISMATCH — reads as a character breaker (§7) or off-persona
```

None of these decisions promote anything to `canonical` automatically — that stays an explicit,
separate action (Architecture §29, §43), same as every other asset in this project.
