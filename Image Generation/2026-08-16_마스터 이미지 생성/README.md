# 마스터 이미지 생성 — 2026-08-16

Test1, Test2, ... 순서로 반복하는 마스터 후보 빌드 루프. 각 Test 폴더는
`experiments/raw/higgsfield_case_package_v1.1b/`의 실제 케이스 기록과 같은 형식을 따릅니다.

## 각 Test 폴더 구성

Claude가 미리 채워두는 것:
- `references/` — 실제 업로드용 이미지 파일, 순서대로 번호 매김 (예: `01_PRIMARY_FACE.jpg`)
- `00_PROMPT.txt` — 힉스필드에 그대로 붙여넣을 순수 텍스트 프롬프트
- `HOW_TO_RUN.md` — 업로드 순서표 + 모델/화면비/퀄리티 설정 + 실행 후 할 일, 한 파일에 정리

사용자가 실행 후 채우는 것:
- 결과 이미지 (파일명 자유, 예: `RESULT_01.png`)
- `USER_FEEDBACK.txt` — 본인 판단 (뭐가 좋았고 뭐가 안 좋았는지)
- `GPT_FEEDBACK.txt` (또는 `.md`) — GPT QC 판단 (`canonical/gpt_bridge/VISUAL_QC_INSTRUCTIONS_v1.2.md` 활용 가능)

## Claude가 매 Test마다 반드시 지킬 것

**`00_PROMPT.txt`를 사용자에게 제시하기 전에 반드시 실행:**
```bash
py scripts/prompt_check.py "Image Generation/.../TestN/00_PROMPT.txt" --max-length 3000
```
`WARN`/`FAIL` 없이 `PASS`가 나올 때까지 다듬은 뒤에만 제시할 것. 특히 `WARN`(non-ASCII 문자
발견)이 뜨면 em dash(—)나 스마트 따옴표 같은 걸 전부 일반 ASCII(`-`, `'`)로 바꿀 것 — 문자수는
3000자 이하로 통과해도, 바이트 수나 붙여넣기 과정에서 실제로는 더 길게 카운트될 수 있음.

이미 두 번 겪은 실수: Test1에서 4449자짜리 프롬프트를 검증 없이 제시했었고, Test2에서는
문자수는 통과(2983자)했지만 em dash 6개 때문에 실제로는 사용자 쪽에서 3000자 초과로
표시됐음. 원인과 수정 내역은 `canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md`
§5.1–5.2 참고 — 같은 실수 반복 금지.

## 진행 방식

1. Test1 실행 → 결과 + 두 피드백을 Test1에 채워넣기
2. Claude가 확인 후:
   - 후보 전체가 구조적으로 문제 있으면 (identity/body/outfit 자체가 틀림) → 원인 진단 + 수정된
     프롬프트로 Test2 생성 (프롬프트 길이 재확인 포함), 반복
   - 후보 중 하나는 이미 구조적으로 괜찮고 딱 한 차원만 약하면 (스킨, 가슴 physics, 표정 등) →
     처음부터 다시 만들지 말고 **보정 패스**(`Correction1_...` 형식 폴더, image-to-image, 그
     한 차원만 수정)로 전환. 근거와 템플릿은 `canonical/prompt_lab/
     HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` §2-§3 (실제 첫 적용 사례: `Correction1_Outfit/`
     → `Correction2_Skin/`, Test3와 같은 레벨의 별도 폴더, 두 단계 체인 - 폴더 번호는 실제 실행
     순서).
     보정이 두 차원 이상 필요해 보여도 한 프롬프트에 합치지 말고 §3의
     경고대로 따로따로 돌릴 것
   - 괜찮으면 → 여기서 종료, 해당 프롬프트를 검증된 것으로 기록 (`canonical/prompt_lab/`에 승격 여부는 별도 논의)
3. 각 Test/Correction은 독립 기록으로 남음 — 나중에 "무엇을 바꿔서 무엇이 좋아졌는지" 추적 가능
