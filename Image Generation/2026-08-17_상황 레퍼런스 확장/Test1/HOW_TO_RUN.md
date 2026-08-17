# Test1 - 상황 레퍼런스 확장 (Daily Reference 방식, 새 Trial)

마스터 제작(`../../2026-08-16_마스터 이미지 생성/`)은 Test8에서 일단락하고, 이제 그 결과물을
가지고 다른 상황/배경 사진을 만드는 새 단계입니다. 이 폴더는 그 새 Trial의 Test1입니다 - 마스터
제작 때와 번호를 공유하지 않고 새로 시작합니다.

## 이 방식의 근거

`experiments/raw/higgsfield_case_package_v1.1b/CASE_02_SNS_EXPANSION_PHYSICS/`와
`CASE_03_STRICT_DAILY_REFERENCE_5LITE/`가 정확히 이 작업(마스터 + 상황 레퍼런스 → 새 사진)의
실제 테스트 기록입니다. 거기서 확인된 것:
- 마스터 하나(identity+몸매+의상 다 포함)를 Image1로, 상황 사진을 Image2로 - 2장이면 충분함
- Image2는 배경/조명/포즈를 강하게 따라가게 하고, Image1의 얼굴 표정을 그대로 붙여넣지 않게
  명시해야 함 (안 그러면 표정이 "붙여넣은 것처럼" 굳어버림 - Workflow Master §10에도 있는 문제)
- Seedream 4.5가 포즈 재현은 5 Lite보다 정확함 (5 Lite는 변주는 좋지만 정확한 포즈 재현엔 약함)

이번 상황 레퍼런스(엎드려 자는 포즈, 특정 소품 배치)는 포즈가 꽤 구체적이라 정확한 재현이
중요하다고 판단해서 Seedream 4.5로 갑니다 (`canonical/prompt_lab/
HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` §4의 모델 선택 기준과도 일치).

`canonical/workflow/00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt`의 공식 구조(FACE ID MASTER +
CHARACTER MASTER + BODY MASTER + Daily Reference + Outfit Reference, 5장 분리)도 검토했지만,
이번엔 CASE_02/03에서 이미 검증된 2장짜리(Master + Daily Reference) 구조로 갑니다 - Test8 결과물
자체가 이미 identity+몸매+의상이 다 검증된 상태라, 그걸 다시 3개로 쪼개는 것보다 그대로 Image1로
쓰는 게 더 안전하고 단순합니다.

## 1. 이미지 업로드 순서

| 순서 | 파일 | 역할 |
|---|---|---|
| 1 | `01_MASTER.png` (Test8 Result.png - 흰 티+회색 반바지) | identity + 몸매 + 의상 전체 |
| 2 | `02_DAILY_REFERENCE.jpeg` (공부하다 책상에 엎드린 사진) | 배경/조명/포즈/카메라 앵글 - STRICT |

## 2. 설정

| 항목 | 값 |
|---|---|
| 모델 | Seedream 4.5 |
| 화면비 | 4:5 (Daily Reference 원본이 750x936 = 4:5 비율과 거의 일치) |
| 퀄리티 | basic (마스터와 동일 - 업스트림에서 이미 확인된 설정 유지) |
| 생성 방식 | Unlimited / 웹 플랜 (수동) |
| 시드 | 랜덤, 배치로 여러 장 뽑아서 고르는 걸 추천 (CASE_02: "batch generation can yield usable images") |

## 3. 프롬프트

`00_PROMPT.txt` 그대로 복사 (2679/3000자, 순수 ASCII, PASS 확인 완료).

## 4. 이번엔 특히 확인해주세요

- **배경이 레퍼런스와 실제로 거의 동일하게 나오는지** (책상, 노트, 펜, 배경의 둥근 소품, 조명
  톤) - 사용자가 명시적으로 요청한 핵심 조건
- **표정이 마스터 사진(정면 무표정)을 그대로 붙여넣은 것처럼 안 보이는지** - 엎드린 포즈에 맞는
  자연스럽고 살짝 나른한 표정인지
- 포즈가 레퍼런스와 가깝게 나오는지 (엎드려서 책상에 기댄 자세, 팔 위치)
- 의상(흰 티+회색 반바지)과 몸매가 마스터와 일치하는지, 레퍼런스 인물의 옷(후드집업)이나 몸매가
  안 새어 들어왔는지

## 5. 실행 후

결과 이미지 + `USER_FEEDBACK.txt` + GPT QC 핸드오프를 이 폴더에 추가해주세요.
