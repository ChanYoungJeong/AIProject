# 상황 레퍼런스 확장 - 2026-08-17

`../2026-08-16_마스터 이미지 생성/`에서 만든 캐릭터+의상 마스터를 가지고, 다른 배경/상황
사진(Daily Reference)을 만드는 새 작업 라인입니다. Test1, Test2, ... 마스터 제작 때와 별개로
번호를 새로 시작합니다.

## 이 폴더 vs 마스터 제작 폴더

| | 마스터 제작 (`2026-08-16_...`) | 상황 레퍼런스 확장 (여기) |
|---|---|---|
| 목적 | identity+몸매+의상을 하나의 이미지로 고정 | 그 마스터를 다른 배경/포즈에 넣기 |
| 레퍼런스 수 | 8장 (얼굴 3 + 헤어 1 + 몸매 3 + 의상 1) | 2장 (마스터 1 + Daily Reference 1) |
| 상태 | Test8에서 일단락, 프롬프트 확정 | 지금 시작 |
| 근거 문서 | `canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` | `experiments/raw/higgsfield_case_package_v1.1b/CASE_02_...`, `CASE_03_...` + `canonical/workflow/00_WORKFLOW_MASTER_AI_INFLUENCER_v1.2.txt` |

## 마스터(옷장) 관리

캐릭터가 여러 의상을 입은 마스터를 옷장처럼 여러 개 갖게 됩니다. 실제 파일은
`assets/characters/yeoreum/wardrobe/`에 정리되어 있고, 이 폴더의 각 Test는 어떤 옷장 항목을
어떤 Daily Reference에 넣었는지를 기록합니다.

## 진행 방식

마스터 제작 폴더와 동일: Test1 실행 → 결과 + 피드백 채우기 → 문제 있으면 원인 진단 + 수정된
프롬프트로 Test2, 반복. 괜찮으면 그 조합(마스터 + Daily Reference 스타일)을 검증된 것으로 기록.
