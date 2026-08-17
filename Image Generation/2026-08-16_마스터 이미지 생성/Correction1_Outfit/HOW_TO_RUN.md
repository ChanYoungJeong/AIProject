# Correction1_Outfit - Test3 Result 1 의상 구조 보정 (staged pass, 1/2)

**보류 (2026-08-16):** 사용자 지시로 이 보정 패스 체인 전체를 보류하고, 대신 마스터를 처음부터
다시 만드는 `../Test4/`로 진행 중. Test4가 의상 좌우 비대칭을 완전히 해결하지 못하면 이 폴더로
돌아올 수 있음 - 그 전까지는 실행하지 말 것.

`../Test3/CLAUDE_QC_NEW_BATCH_UPDATED_2026-08-16.md` 반영 (원래 작성 배경, 아래 내용은 보류
중에도 유효한 진단이니 참고용으로 남겨둠). 이 문서가 Test3의 원래 QC
(`CLAUDE_QC_NEW_BATCH_2026-08-16.md`)를 대체하는 최신 판단입니다.

## 새로 확인된 문제

Result 1, 2, 3 전체에 걸쳐 탱크/바디수트가 하나의 안정된 의상으로 유지되지 않음 - 좌우 넥라인/
스트랩 구조가 다르고, 몸매 정보가 의상 구조를 오염시키는 것으로 진단됨 (HIGH priority, 반복/
시스템적 문제). Test2에서 처음 지적된 것과 같은 종류의 body-outfit blending이며, Test3에서 추가한
명시적 방지 문구("do not let Images 5-7 change the outfit's cut, fit, or construction")로도
완전히 해결되지 않았음이 이번에 확인됨.

## 왜 프롬프트를 세 번째로 다시 고치지 않고 보정 패스로 가는가

Outfit 차원에 대한 텍스트 수정은 이미 두 라운드 시도됐고 둘 다 실패:
1. Test2 - 장문의 해석적 문구("not inspiration", 항목별 체크리스트, "same garment... not
   redesigned") 추가 -> 오히려 악화
2. Test3 - 그 반대로 짧고 사실적인 문구 한 줄로 단순화 -> 이번 배치 3개 전부에서 여전히 발생

전략 문서 §1.1의 에스컬레이션 규칙("같은 차원에 대한 텍스트 교정이 두 라운드 연속 실패하면,
그 차원에 단어를 더 추가하지 말고 구조적 변수를 바꿔라")이 정확히 이 상황입니다. 다음 시도는
OUTFIT 문구를 세 번째로 고쳐 쓰는 게 아니라, 이미 스킨/physics에 쓴 것과 같은 방식 - 실제 후보
이미지에 대한 좁은 범위의 i2i 보정 패스 - 를 의상에도 적용하는 것입니다. 새 템플릿은
`canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` §3.4에 기록.

## 왜 Result 3이 아니라 Result 1인가

UPDATED QC의 "overall visual usability" 기준 순위: 1. Result 1, 2. Result 3, 3. Result 2.
Result 1은 의상 비대칭이 "less distracting"으로 상대적으로 약하고, 렌더링 아티팩트도 Result 2보다
적음. Result 3은 "significant outfit-fidelity failure"로 더 심하게 지적됨. 더 약한 결함을 가진
후보를 고치는 게 더 심한 결함을 가진 후보를 고치는 것보다 성공 확률이 높다고 판단.

## 1. 입력 (i2i, 이미지 2장)

1. **Result 1** 이미지 (원본 생성 세션에서 가져올 것 - 이 폴더에 저장되어 있지 않음)
2. **`../Test3/references/08_OUTFIT_BODYSUIT_DENIM_FISHNET.png`** (Test3에서 이미 쓴 의상
   레퍼런스, 그대로 재사용)

프롬프트의 "first attached image" = 1번(Result 1), "second attached image" = 2번(의상 레퍼런스)
순서를 반드시 지킬 것.

## 2. 설정

| 항목 | 값 |
|---|---|
| 모드 | Image-to-image (2개 이미지 입력) |
| 모델 | Seedream 4.5 (Test3와 동일 - 모델을 동시에 바꾸지 않고 한 번에 한 변수만 테스트) |
| 화면비 | 원본과 동일 (9:16) |
| 퀄리티 | high (Test3와 동일 유지) |

## 3. 프롬프트

`00_PROMPT.txt` 그대로 사용 (877/3000자, 순수 ASCII, `prompt_check.py` PASS 확인 완료).

## 4. 확인할 것

- 탱크/바디수트 좌우가 이제 하나의 일관된 구조로 보이는지 (넥라인/스트랩이 양쪽 대칭)
- 의상이 여전히 몸매에 맞춰 재해석된 것처럼 보이지 않는지
- 얼굴/포즈/몸/피부/반바지/스타킹/배경/조명이 Result 1 원본과 동일하게 유지됐는지 (이 패스는
  바디수트 구조 외엔 아무것도 안 바뀌어야 정상)

## 5. 실행 후

성공하면: 이 결과 이미지를 `Correction2_Skin/`의 입력으로 넘겨 스킨 보정을 이어서 진행하세요
(그 폴더의 "1. 입력" 항목 참고 - 이미 이 순서로 안내되어 있음). 결과와 판단은 이 폴더에 추가.

실패하면 (좌우 비대칭이 남아있거나 다른 요소가 바뀌면): §3.4 템플릿 자체를 개선해야 할 신호.
이 경우 다음으로 시도할 것 - 두 번째 이미지(의상 레퍼런스)의 role 문구를 더 강하게("second image
is the only source of garment shape") 명시하거나, 마스터 빌드 자체를 참조 이미지 수를 줄여
재구성하는 더 큰 변경을 검토. `HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md`에 결과를 기록해서
다음 판단에 반영할 것.
