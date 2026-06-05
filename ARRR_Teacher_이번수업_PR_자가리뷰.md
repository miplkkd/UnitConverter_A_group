# ARRR teacher persona를 이용한 이번 수업의 PR 자가리뷰

**작성:** ARRR(RBS) 감독 teacher persona  
**대상 저장소:** [miplkkd/UnitConverter_A_group](https://github.com/miplkkd/UnitConverter_A_group/pulls)  
**작성일:** 2026-06-05  
**리뷰 범위:** PR #1 ~ #5 (prompting·Transcript 중심, `src/`·`tests/` 코드 심층 리뷰 제외)

---

## 리뷰 기준

| 항목 | 내용 |
|------|------|
| 1순위 | 학생 User 프롬pt·`prompting/*-Transcript.md` |
| 참고 | `Report/` (맥락용) |
| PR당 형식 | 잘한 점 / 보완점 / 다음 액션 (각 1줄) |
| 필수 표기 | 해당 PR에서 prompt 파일 신규·수정 여부 |
| 금지 | Transcript 본문에 이모지·아이콘 사용 |

---

## PR별 리뷰

### [PR #1](https://github.com/miplkkd/UnitConverter_A_group/pull/1) — spec: Cursor TDD harness, PRD v0.2

**prompt 변화:** `prompting/02.transcript-export.md`, `03.UnitConverter_Session3_CursorRulesReview-Transcript.md`, `04.UnitConverter_Session4_CursorDesign-Transcript.md` **신규**.

세션 3~4 Transcript가 Session ID·제외 세션(마방진 페르소나) 표와 User 프롬pt 원문을 잘 보존했고, Skill·`/tdd-red`·`/review-ecb`·hooks 설계 흐름이 Report/02와 1:1로 맞습니다.  
다만 Session 4 User 턴에 `Phase · Layer · Track` 선언이 없고, Assistant 요약 표에 이모지(⚠️·❌)가 남아 있어 이후 export 규칙과 어긋납니다.  
다음 세션부터 User 프롬pt 첫 줄에 Phase 선언을 고정하고, Transcript는 텍스트만 쓰도록 정리하세요.

---

### [PR #2](https://github.com/miplkkd/UnitConverter_A_group/pull/2) — Session 5: IBAC/BCE/RBS, D-CONV-01 RED

**prompt 변화:** `prompting/05.UnitConverter_Session5_IBAC_RED_KDReport-Transcript.md` **신규** (이전 PR 대비 +1).

IBAC 피드백→always-apply rule→MagicSquare 정리→D-CONV-01 RED의 인과가 Transcript에 남아 있고, RED 실행 프롬pt에 `Phase: red | Layer: entity | Track: Logic`이 명시된 점이 좋습니다.  
초기 `/red-test-plan`(D-LOC-01)이 도메인 오류였고, IBAC 반영·브랜치 전환·`/kdreport` 턴은 Phase 선언 없이 진행되어 “왜 red로 갔는가” 복기가 약합니다.  
도메인 수정 전후를 User 턴에 한 줄씩 남기고, `/kdreport` 이전에도 Phase·Track을 붙이세요.

---

### [PR #3](https://github.com/miplkkd/UnitConverter_A_group/pull/3) — Session 7–10: Full GREEN + Golden Master

**prompt 변화:** `prompting/06~10` **신규 6건** (`06`이 GREEN·RED_Skeletons로 **번호 중복**, 이전 PR 대비 +6).

Session 6 RED 스켈레톤(워크북 이미지·의미 있는 FAIL 전환)과 Session 10 Golden Master 개념 Q&A가 RBS 복기에 유용하고, `/next-green` 반복 패턴이 Report 05~08과 연결됩니다.  
Session 9에서 U-OUT/D-REG/D-CFG를 한 Transcript에 연속 GREEN했고, User 턴이 대부분 `/next-green`만 있어 FR 단위·Phase 경계가 흐려집니다; `06` 파일명 충돌도 혼동을 줍니다.  
ID마다 Transcript를 분리하거나 User 프롬pt에 대상 ID·예상 FAIL·pytest 명령을 매 턴 적고, `06` 번호를 세션별로 재정렬하세요.

---

### [PR #4](https://github.com/miplkkd/UnitConverter_A_group/pull/4) — Session 11: PyQt GUI, refactor-safe

**prompt 변화:** `prompting/11~13` **신규 3건** (이전 PR 대비 +3).

Session 11에서 GUI 요청→`process_input` 분리→`/refactor-smell`→`/refactor-safe`×2→pytest/GM 검증까지 흐름이 Report 09~11과 맞고, refactor-safe를 12·13에서 CLI/GUI/entity로 쪼갠 기록이 있습니다.  
첫 GUI 프롬pt가 “pyqt? GUI test” 수준으로 짧고 Phase·Track이 없으며, 12·13은 `/refactor-safe`·`/kdreport` 위주라 의사결정 문장이 거의 없습니다.  
GUI·REFACTOR User 턴에 `Phase: green/refactor | Layer: boundary | Track: UI`를 넣고, smell 결과(P0/P1)를 다음 `/refactor-safe` 프롬pt에 그대로 인용하세요.

---

### [PR #5](https://github.com/miplkkd/UnitConverter_A_group/pull/5) — Session 14~15: P1 features, GUI smoke

**prompt 변화:** `prompting/14~15` **신규 2건** (이전 PR 대비 +2).

Session 14는 OCP/SRP 질의→`new_features` 브랜치→이미지 SSOT→P1 GREEN까지 User 의도가 단계별로 남아 있고, Session 15는 P1 잔여·GUI smoke·E002/E003를 체크리스트 형태로 정리했습니다.  
Session 14 “진행 하자” 한 턴에 9+ GREEN이 묶였고, Session 15 GUI smoke User 문장이 `…`로 축약되어 원문 프롬pt 복기가 불가합니다.  
대량 GREEN은 ID·pytest 명령을 나열한 User 턴으로 쪼개고, smoke 목록·컨펌 문장은 export 시 생략 없이 전문을 남기세요.

---

## 전체 소견

이 저장소는 `prompting/NN.*-Transcript.md` + `/kdreport` 워크플로가 가장 잘 정착된 편입니다.

공통 보완점은 다음과 같습니다.

1. User 프롬pt 첫 줄 `Phase · Layer · Track` 선언의 일관성
2. 한 Transcript에 여러 ID GREEN을 묶지 않기 (FR 단위 RBS 원칙)
3. `prompting/06`처럼 동일 번호 파일 충돌 해소
4. Transcript export 시 User 문장 생략·축약 금지

---

## prompt 파일 누적 현황 (PR #5 기준)

| 번호 | 파일 | 최초 등장 PR |
|------|------|-------------|
| 02 | `02.transcript-export.md` | #1 |
| 03 | `03.UnitConverter_Session3_CursorRulesReview-Transcript.md` | #1 |
| 04 | `04.UnitConverter_Session4_CursorDesign-Transcript.md` | #1 |
| 05 | `05.UnitConverter_Session5_IBAC_RED_KDReport-Transcript.md` | #2 |
| 06 | `06.UnitConverter_Session6_D-CONV-01_GREEN-Transcript.md` | #3 |
| 06 | `06.UnitConverter_Session6_RED_Skeletons-Transcript.md` | #3 (번호 중복) |
| 07 | `07.UnitConverter_Session7_GREEN_Merge_U-IN-01-Transcript.md` | #3 |
| 08 | `08.UnitConverter_Session8_U-IN-02-03_GREEN-Transcript.md` | #3 |
| 09 | `09.UnitConverter_Session9_Full_GREEN-Transcript.md` | #3 |
| 10 | `10.UnitConverter_Session10_GoldenMaster-Transcript.md` | #3 |
| 11 | `11.UnitConverter_Session11_PyQtGUI_Refactor-Transcript.md` | #4 |
| 12 | `12.UnitConverter_Session12_RefactorSafe_CLI-Transcript.md` | #4 |
| 13 | `13.UnitConverter_Session13_RefactorSafe_GUI_Entity-Transcript.md` | #4 |
| 14 | `14.UnitConverter_Session14_P1_NewFeatures_GREEN-Transcript.md` | #5 |
| 15 | `15.UnitConverter_Session15_P1_Followup_GUI_Smoke-Transcript.md` | #5 |

---

*End of ARRR teacher PR self-review*
