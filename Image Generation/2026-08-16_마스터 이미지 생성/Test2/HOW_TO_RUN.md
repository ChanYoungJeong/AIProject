# Test2 — 마스터 이미지 생성 (Test1 수정본)

Test1 QC 핸드오프(`../Test1/CLAUDE_MASTER_REFERENCE_QC_HANDOFF_2026-08-16.md`) 반영. 뭘 왜
바꿨는지는 `00_CHANGES_FROM_TEST1.md` 참고.

## 1. 이미지 업로드 순서 (Test1과 동일)

| 순서 | 파일 | 역할 |
|---|---|---|
| 1 | `01_PRIMARY_FACE.jpg` | 얼굴 정체성 |
| 2 | `02_SECONDARY_FACE_3Q.jpg` | 얼굴 보조 — 3/4 각도 |
| 3 | `03_SECONDARY_FACE_TILT.jpg` | 얼굴 보조 — 머리 기울임 각도 |
| 4 | `04_HAIR_CONTINUITY.jpg` | 헤어스타일·피부톤·목/어깨 연결부 전용 |
| 5 | `05_PRIMARY_BODY.png` | 몸매 기준 |
| 6 | `06_SECONDARY_BODY_3Q.png` | 몸매 보조 — 3/4 각도 |
| 7 | `07_SECONDARY_BODY_SIDE.png` | 몸매 보조 — 측면 각도 |
| 8 | `08_OUTFIT_BODYSUIT_DENIM_FISHNET.png` | 의상 — 이번엔 "정확히 이 디자인 그대로" 강조 |

## 2. 설정 (Test1과 동일)

| 항목 | 값 |
|---|---|
| 모델 | Seedream 4.5 |
| 화면비 | 9:16 |
| 퀄리티 | high |
| 생성 방식 | Unlimited / 웹 플랜 (수동) |
| 시드 | 랜덤 |

## 3. 프롬프트

`00_PROMPT.txt` 그대로 복사 (2943/3000자, 순수 ASCII, `prompt_check.py` PASS 확인 완료 — WARN 없음).

## 4. 이번엔 특히 확인해주세요

- 피부가 Test1보다 덜 매끈하고 덜 인형같은지 (질감·톤 편차가 자연스러운지)
- 의상이 "영감을 받은 비슷한 옷"이 아니라 레퍼런스와 거의 동일한 디자인인지 (넥라인/스트랩/허리·다리 트임 구성)
- 얼굴/헤어/anatomy는 Test1만큼 안정적인지 (이건 유지되어야 함, 나빠지면 안 됨)
- 가슴/허리 비율이 Test1보다 과장 안 됐는지

## 5. 실행 후

`Test1`과 동일하게: 결과 이미지 + `USER_FEEDBACK.txt` + GPT QC 핸드오프를 이 폴더에 추가해주세요.
확인 후 괜찮으면 종료하고 검증된 프롬프트로 기록, 아니면 Test3로 계속 갑니다.
