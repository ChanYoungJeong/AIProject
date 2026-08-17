import pytest
from pydantic import ValidationError

from app.schemas import AssetMetadata, AssetType, CanonicalState, CharacterProfile, LanePolicy, Manifest, Preset
from app.schemas.manifest import (
    CharacterMasters,
    ManifestCharacterEntry,
    ManifestLaneEntry,
    ManifestPresetEntry,
)


def test_face_package_candidate_accepts_and_defaults_extra_fields():
    minimal = AssetMetadata(
        asset_id="YR_FACE_20_TINY_SMILE",
        file_path="assets/characters/yeoreum/face_package/20_library_expression_approved/YR_FACE_20_TINY_SMILE.jpg",
        asset_type=AssetType.FACE_PACKAGE_CANDIDATE,
    )
    assert minimal.support_category is None
    assert minimal.support_status is None
    assert minimal.functional_role is None

    populated = AssetMetadata(
        asset_id="YR_FACE_20_TINY_SMILE",
        file_path=minimal.file_path,
        asset_type=AssetType.FACE_PACKAGE_CANDIDATE,
        character_id="yeoreum",
        support_category="EXPRESSION_SUPPORT",
        support_status="LIBRARY_APPROVED",
        functional_role="TINY_SMILE",
        approved=True,
    )
    assert populated.support_category == "EXPRESSION_SUPPORT"
    assert populated.canonical is False  # never defaults to canonical


def test_body_master_support_accepts_and_a_candidate_master_stays_noncanonical():
    support = AssetMetadata(
        asset_id="BODY_3Q_STANDING_V2",
        file_path="assets/characters/yeoreum/masters/body/body_master_package_v2.0/02_core_view_support/BODY_3Q_STANDING_v2.png",
        asset_type=AssetType.BODY_MASTER_SUPPORT,
        character_id="yeoreum",
        support_category="CORE_VIEW_SUPPORT",
        support_status="ACCEPTED_SUPPORT",
        functional_role="3Q_STANDING_DEPTH",
        approved=True,
    )
    assert support.canonical is False

    # A genuine candidate *replacement* master still uses asset_type=BODY_MASTER,
    # just canonical=False — distinct from the pure-support BODY_MASTER_SUPPORT type.
    candidate = AssetMetadata(
        asset_id="BODY_YEOREUM_V2_CANDIDATE",
        file_path="assets/characters/yeoreum/masters/body/body_master_package_v2.0/01_primary/02_BODY_MASTER_v2_PRIMARY.png",
        asset_type=AssetType.BODY_MASTER,
        character_id="yeoreum",
        approved=True,
    )
    assert candidate.asset_type == AssetType.BODY_MASTER
    assert candidate.canonical is False


def test_character_profile_parses_yeoreum_example():
    profile = CharacterProfile(
        id="yeoreum",
        display_name="Han Yeoreum",
        adult=True,
        age=19,
        core_persona=["quiet", "introverted"],
        visual_formula=["soft_face", "curvy_silhouette"],
        expression_range=["soft_neutral", "tiny_smile"],
        primary_content_pillars={"home_just_outside": 45, "outfit_fitting_mirror": 20},
    )
    assert profile.id == "yeoreum"
    assert profile.primary_content_pillars["home_just_outside"] == 45


def test_lane_policy_parses_natural_mirror_example():
    policy = LanePolicy(
        lane="natural_mirror",
        canonical_preset="NAT_v1.4.3",
        status="locked",
        model={"provider": "higgsfield", "model": "seedream_4_5", "max_prompt_length": 3000},
        reference_order={
            "image1": "FACE_ID_MASTER",
            "image2": "CHARACTER_MASTER",
            "image3": "BODY_MASTER",
            "image4": "DAILY_REFERENCE_FACE_MASKED",
        },
        priority=["face_identity", "daily_pose_composition"],
        pose_policy={"reference_led": True, "invent_new_pose": False},
        face_policy={
            "preserve_identity": True,
            "copy_master_expression": False,
            "adapt_gaze_head_angle_perspective": True,
        },
        outfit_policy="preset_defined",
        refinement_policy={"mandatory_second_pass": False},
    )
    assert policy.status == CanonicalState.LOCKED
    assert policy.reference_order.image4 == "DAILY_REFERENCE_FACE_MASKED"


def _valid_preset_kwargs(**overrides):
    kwargs = dict(
        preset_id="NAT_v1.4.3",
        status="locked",
        lane="natural_mirror",
        model={"provider": "higgsfield", "model": "seedream_4_5"},
        reference_profile="NAT_MIRROR_FOUR_REF_V1",
        max_prompt_length=3000,
        prompt_snapshot_path="canonical/presets/natural_mirror/NAT_v1.4.3_LOCKED_PROMPT.txt",
        prompt_hash="abc123",
        outfit_policy="preset_defined",
        revision_policy="derive_new_version",
    )
    kwargs.update(overrides)
    return kwargs


def test_preset_parses_valid_example():
    preset = Preset(**_valid_preset_kwargs())
    assert preset.status == CanonicalState.LOCKED
    assert preset.prompt_snapshot_path is not None


def test_locked_preset_without_snapshot_path_is_rejected():
    with pytest.raises(ValidationError):
        Preset(**_valid_preset_kwargs(prompt_snapshot_path=None))


def test_preset_rejects_unknown_status():
    with pytest.raises(ValidationError):
        Preset(**_valid_preset_kwargs(status="not_a_real_status"))


def test_manifest_parses_valid_example():
    manifest = Manifest(
        project="AI_Influencer_Studio",
        workflow_master="canonical/workflow/00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt",
        characters={
            "yeoreum": ManifestCharacterEntry(
                bible="canonical/characters/yeoreum/CHARACTER_BIBLE_YEOREUM_v1.1.txt",
                profile="canonical/characters/yeoreum/character_profile.yaml",
                masters=CharacterMasters(),
            )
        },
        lanes={
            "natural_mirror": ManifestLaneEntry(
                preset="NAT_v1.4.3",
                policy="canonical/presets/natural_mirror/lane_policy.yaml",
            )
        },
        presets={
            "NAT_v1.4.3": ManifestPresetEntry(
                status="locked",
                prompt="canonical/presets/natural_mirror/NAT_v1.4.3_LOCKED_PROMPT.txt",
                metadata="canonical/presets/natural_mirror/preset.yaml",
            )
        },
    )
    assert manifest.characters["yeoreum"].masters.face_id is None
    assert manifest.presets["NAT_v1.4.3"].status == CanonicalState.LOCKED
