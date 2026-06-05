---
name: unitconverter-tdd
description: >-
  Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. UnitConverter_Agroup에서
  RED/GREEN/REFACTOR, Logic/UI Track, Loop A/B/C pytest, E001~E007·Mock 규칙을
  적용할 때 사용. TDD, ECB, test_d_*, test_u_*, D-*, U-* 요청 시.
---

# UnitConverter — Dual-Track TDD · ECB

> 헌법: `.cursorrules` · 범위: `docs/PRD.md` · D-* ID: [reference.md](reference.md)

## 언제 이 Skill을 켜는지

| 트리거 | 예 |
|--------|-----|
| 사용자가 TDD·RED/GREEN/REFACTOR·Dual-Track·ECB 개발을 요청 | 「D-CONV-01 RED」, 「entity 변환 테스트」 |
| `test_d_*` / `test_u_*` / `D-*` / `U-*` 작성·수정·실행 | Logic/UI Track 테스트 추가 |
| `src/entity` · `src/control` · `src/boundary` 구현·리팩터 | ECB 레이어별 작업 |
| Test Loop A/B/C·세션 Exit·제출 게이트 점검 | Loop B `--collect-only`, 검증 assert |
| import·ModuleNotFoundError 해소 후 테스트 사이클 재개 | RED 스켈레톤부터 |

**켜지 않을 때:** Rule/PRD 리뷰만, 문서만, git commit(사용자 미요청), Golden Master 갱신, JSON/동적 단위/conftest/`pip install -e .` 제안.

**매 턴 선언 (한 줄):** `Phase`(RED|GREEN|REFACTOR) · `Layer`(entity|control|boundary) · `Track`(Logic|UI)

---

## RED — 7단계 (한 번에 한 테스트)

1. **대상 확정** — `reference.md`에서 D-* ID 선택, Layer·Track·파일 경로 결정 (`tests/entity|control`, `test_d_*`).
2. **Phase 선언** — `Phase=RED` · `Layer=…` · `Track=Logic`.
3. **테스트만 작성** — `tests/`에 `test_d_*` 추가; 함수 docstring·이름에 `D-*` 포함; SSOT 상수는 구현 SSOT에서 import(리터럴 산재 금지).
4. **구현 금지** — 이 단계에서 `src/`·`UnitConverter.py` **로직 수정 금지** (import 경로용 `__init__.py`·빈 스텁만 예외).
5. **RED 수용 기준** — `ModuleNotFoundError`(미구현 import) 또는 `pytest.fail("RED: D-* …")` 또는 AssertionError(의도된 미구현).
6. **pytest 실행** — 프로젝트 루트 cwd, 대상 노드만:
   `python -m pytest tests/<layer>/test_d_<id>.py::<함수명> -v`
7. **FAIL 확인·보고** — exit ≠ 0, 실패 유형·D-* ID 기록. FAIL 없이 GREEN으로 넘어가지 않음.

---

## GREEN — 6단계

1. **대상 확정** — RED에서 FAIL 확인한 동일 D-* / 동일 테스트 함수.
2. **Phase 선언** — `Phase=GREEN` · `Layer=…` · `Track=Logic`.
3. **최소 구현** — 해당 Layer의 `src/`만 수정; ECB import 방향 준수; MagicConstant SSOT 한 곳만.
4. **금지** — assert 완화·주석·삭제·`skip`·`xfail`로 green 만들기 금지.
5. **Track pytest** — Logic Track 전체:
   `python -m pytest tests/entity tests/control -v`
6. **PASS 확인** — Track 전부 green 후에만 REFACTOR. 실패 시 구현/검증 수정으로 통과.

---

## REFACTOR — 6단계

1. **전제** — 해당 Track pytest **전부 PASS** (GREEN 완료).
2. **Phase 선언** — `Phase=REFACTOR` · `Layer=…` · `Track=Logic|UI`.
3. **범위** — 냄새·중복·이름·SSOT 정리만; **동작·공개 계약·테스트 assert 변경 없음**.
4. **ECB 유지** — `entity` 순수 로직, `control` 판정·오케스트레이션, `boundary` I/O·emit; 역방향 import 금지.
5. **회귀 pytest** — 수정한 Track:
   - Logic: `python -m pytest tests/entity tests/control -v`
   - UI: `python -m pytest tests/boundary -v`
6. **완료** — 회귀 PASS 후 다음 RED(다른 D-* 1개) 또는 Test Loop 점검.

---

## Logic Track vs UI Track

| 항목 | Logic Track | UI Track |
|------|-------------|----------|
| **레이어** | `entity`, `control` | `boundary` |
| **디렉터리** | `tests/entity`, `tests/control` | `tests/boundary` |
| **파일명** | `test_d_*` | `test_u_*` |
| **테스트 ID** | `D-*` (변환·판정 로직) | `U-*` (FR-04~07 CLI·출력·에러 emit) |
| **Mock** | **금지** — entity/control `@patch`·Domain Mock 없음 | **I/O만 허용** — stdin/stdout/`capsys`/`monkeypatch`/`StringIO`; **control은 real** |
| **검증 대상** | meter 기준 변환, E001~E004 **판정** (코드/결과만, emit 없음) | 3줄 출력 형식, E001~E004 **메시지·exit** |
| **RED pytest 예** | `python -m pytest tests/entity/test_d_conv_01.py::… -v` | `python -m pytest tests/boundary/test_u_err_01.py::… -v` |
| **GREEN 회귀** | `python -m pytest tests/entity tests/control -v` | `python -m pytest tests/boundary -v` |

**레거시:** PRD FR-08 `tests/test_convert.py` — Loop B import·수집 통과용; **신규 테스트는 Track 디렉터리에만** 추가.

---

## ECB · Mock · E001~E007

### ECB (의존 방향)

```
boundary → control → entity
```

| 레이어 | 역할 | import·호출 |
|--------|------|-------------|
| **entity** | meter 기준 변환·순수 계산 | stdlib·`entity` 내부만; `control`/`boundary` import **금지** |
| **control** | 형식·숫자·단위·음수 **판정**, 오케스트레이션 | `entity`만 import; `boundary` import **금지** |
| **boundary** | CLI/I/O, 3줄 출력, **E001~E004 emit** | `control`만 호출; `entity` 직접 import·호출 **금지** |

### Mock

| 허용 | 금지 |
|------|------|
| UI Track: stdin/stdout/capsys/monkeypatch/StringIO | Logic Track: entity/control `@patch`·Mock |
| UI Track: control **real** 사용 | boundary에서 entity 직접 호출 |
| | Domain 로직을 Mock으로 대체해 green 만들기 |

### E001~E007 (emit 주체 · 세션 범위)

| 코드 | 의미 | emit |
|------|------|------|
| E001 | `:` 없음 (형식) | **boundary만** |
| E002 | 숫자 아님 | **boundary만** |
| E003 | unknown unit | **boundary만** |
| E004 | 음수 | **boundary만** |
| E005 | 출력 형식/계약 위반 | boundary (본 세션 계약 확정 시) |
| E006~E007 | 예약 | 본 세션 범위 밖 |

**금지:** `entity`/`control`에서 E001~E004를 raise/return/print. 판정은 control, emit은 boundary.

**Golden Master:** `tests/golden/*.approved.txt` — 본 세션 **미사용**; 후속 도입 시 사용자 명시 승인 없이 AI 갱신 금지.

### MagicConstant SSOT

`3.28084`, `1.09361`, `meter`/`feet`/`yard`, 오류 키·메시지 — **한 곳**만. 테스트·구현에 리터럴 산재 금지.

---

## Test / Review Loop — pytest 언제 돌리는지

프로젝트 루트에서 실행 (`pyproject.toml` `pythonpath = ["src"]`).

| 시점 | 명령 | Pass 조건 |
|------|------|-----------|
| **RED** (사이클 1개) | `python -m pytest tests/<layer>/test_d_*.py::<함수> -v` | exit ≠ 0 (의도된 FAIL) |
| **GREEN** (Logic) | `python -m pytest tests/entity tests/control -v` | 전부 PASS |
| **GREEN** (UI) | `python -m pytest tests/boundary -v` | 전부 PASS |
| **REFACTOR** | 위와 동일 Track 전체 | PASS 유지 |
| **Loop A — 재현** | `python -m pytest tests/ -k "convert or conv" -v` (또는 `tests/test_convert.py` + `test_d_*`) | meter/feet/yard, README 비율 일치 |
| **Loop B — import·수집** | `python -m pytest tests/ --collect-only` | ModuleNotFoundError 없음 |
| **Loop C — 검증·판정** | `python -m pytest tests/ -v` | `abc:1`, `meter:hello`, 음수, unknown unit assert 통과 |
| **세션 Exit** | Loop A + B + C 연속 Pass | 주석·`skip`·`xfail` assert **0개** |

**import 막힘 시 (Loop B 실패):** cwd=루트 → `--collect-only` → 함수 분리 → `tests/__init__.py`. `pip install -e .`·conftest 이번 세션 제안 금지.

**전체 회귀 (Exit 직전):** `python -m pytest tests/ -v`

---

## 완료 보고 항목

작업 턴·세션 종료 시 아래를 짧게 보고한다.

| # | 항목 |
|---|------|
| 1 | `Phase` · `Layer` · `Track` |
| 2 | 테스트 ID (`D-*` / `U-*`) 및 파일·함수명 |
| 3 | 실행한 pytest 명령과 결과 (PASS/FAIL, 실패 1줄 요약) |
| 4 | 변경 파일 목록 (`tests/` vs `src/` vs `UnitConverter.py`) |
| 5 | ECB 위반 여부 (없음 / 수정함) |
| 6 | Mock 사용 여부 (Logic: 없어야 함 / UI: I/O만) |
| 7 | Loop A/B/C 상태 (해당 시 Pass/Fail) |
| 8 | 다음 권장 단계 (예: 다음 `D-*` RED, UI `U-*`, Loop C) |

---

## 금지 요약 (Quick)

- RED 중 `src/` 로직 선행 수정
- Logic Track Domain Mock · entity/control patch
- entity/control에서 E001~E004 emit · boundary→entity 직접 호출
- 실패 테스트 제거·약화·skip·xfail로 제출 판정만 맞추기
- OCP 풀 세트 선행 리팩터로 변환·테스트 미루기
- Golden Master / snapshot 사용자 승인 없이 갱신
