# PRD — UnitConverter_Agroup

> Product Requirements Document  
> 기준: [Report/01.UnitConvert_ProblemDefinition_Report.md](../Report/01.UnitConvert_ProblemDefinition_Report.md) · 워크북 요구 매트릭스  
> 테스트 ID: [.cursor/skills/unitconverter-tdd/reference.md](../.cursor/skills/unitconverter-tdd/reference.md)

**추적 원칙:** 모든 FR / NFR / EXT 에 테스트 ID를 **1:1** 매핑한다 — 개념(PRD)에서 코드(Test)까지 추적 가능하게.

---

## 1. Overview

### 1.1 Product Statement (Problem-First)

**과제 첫날에 변환 결과를 재현 가능하게 확인하고, import 막힘 없이 테스트가 돌아가게 만든다.**

본 PRD는 README·워크북 전체 요구를 **우선순위(P0/P1)** 로 정리한다. **현재 세션(Implementation Gate)** 은 P0 FR·검증·pytest Loop 달성에 집중하고, P1 EXT·OCP 완성형은 후속으로 미룬다.

### 1.2 Background

| 구분 | 내용 |
|------|------|
| 페르소나 | 프로그래밍 수업, 부분 단위변환 과제, 6시간 실습 |
| 표면 문제 (금지) | 「OCP·SRP 단위 변환 프로그램 + pytest 테스트 작성」만을 목표로 삼기 |
| 진짜 문제 | main() starter + 테스트·마감이 겹치면 import 막힘·손계산·실패 테스트 제거로 이어짐 |

---

## 2. Domain Contract (입력 · 단위 · 비율 · 품질)

### 2.1 입력

| 항목 | 규칙 |
|------|------|
| 형식 | `unit:value` (예: `meter:2.5`) |
| 파싱 | `:` 기준 분리 → `unit` 문자열 + `value` 숫자 |

### 2.2 기본 단위 (P0)

| 단위 | 세션 범위 |
|------|-----------|
| `meter` | ✅ Must |
| `feet` | ✅ Must |
| `yard` | ✅ Must |

### 2.3 변환 비율 (meter 기준 SSOT)

| 비율 | 값 |
|------|-----|
| 1 m → ft | **3.28084** |
| 1 m → yd | **1.09361** |

**규칙:** `feet` ↔ `yard` 는 **meter 경유**만 허용 (직접 비율 하드코딩 금지 — entity 순수 로직).

### 2.4 성공 출력

- 입력 `unit:value` → **meter / feet / yard 세 줄** 출력 (형식·반올림·단위 표기는 boundary SSOT 한 곳).
- 예: `meter:2.5` → feet ≈ **8.2021**, yard ≈ **2.7340** (README 비율 기준).

### 2.5 품질·검증 (P0)

| 항목 | 요구 |
|------|------|
| 설계 | **OCP**·**SRP** 지향 (완성형 풀 세트는 후속 — [§2.2 NFR](#22-non-functional-requirements-nfr)) |
| 음수 | 거부 (E004) |
| 형식 | `:` 없음·잘못된 형식 거부 (E001) |
| 숫자 | 비숫자 value 거부 (E002) |
| 미지 단위 | `cubit` 등 미등록 단위 거부 (E003) |

---

## 3. Requirements Matrix (FR · NFR · EXT)

### 3.1 Functional Requirements (FR)

| ID | 요구 | Given | Then | P | 현재 세션 |
|----|------|-------|------|---|-----------|
| **FR-01** | `unit:value` 파싱 | 유효 문자열 `meter:2.5` | `value=2.5`, `unit=meter` | P0 | ✅ Must |
| **FR-02** | 전 단위 출력 | `meter:2.5` | feet≈8.2021, yard≈2.7340 (+ meter 줄) | P0 | ✅ Must |
| **FR-03** | 미지 단위 | `cubit:1` (미등록) | 명확한 오류 (E003) | P0 | ✅ Must |
| **FR-04** | 음수 | `meter:-1` | 거부 / 예외 (E004) | P0 | ✅ Must |
| **FR-05** | 잘못된 형식 | `meter` (콜론 없음), `abc:1` | 형식 오류 (E001) | P0 | ✅ Must |
| **FR-06** | 비숫자 value | `meter:hello` | 숫자 오류 (E002) | P0 | ✅ Must |

> **Note:** 워크북 핵심 5항(FR-01~05)에 **FR-06**(숫자 검증)을 명시 추가 — Mom Test·Loop C 케이스와 일치.

### 3.2 Non-Functional Requirements (NFR)

| ID | 요구 | Given | Then | P | 현재 세션 |
|----|------|-------|------|---|-----------|
| **NFR-01** | OCP | `inch` 등 신규 단위 추가 | 기존 변환기 코드 **비수정** 확장 | P0 | ⚠️ 방향만 (ECB·Registry 후속) |
| **NFR-02** | SRP | — | Parser / Registry / Converter / Printer **분리** | P0 | ⚠️ ECB 매핑으로 부분 달성 |

**ECB ↔ SRP 매핑 (목표 구조):**

| SRP 역할 | ECB 레이어 | 책임 |
|----------|------------|------|
| Parser | `control` | `unit:value` 파싱·검증 판정 |
| Registry | `entity` (+ SSOT) | 단위·비율 등록 (P0: 3단위 고정) |
| Converter | `entity` | meter 기준 변환 순수 로직 |
| Printer | `boundary` | 3줄 출력·E001~E005 emit |

### 3.3 External / Extension Requirements (EXT) — P1

| ID | 요구 | Given | Then | P | 현재 세션 |
|----|------|-------|------|---|-----------|
| **EXT-01** | 설정 파일 | `units.json` / YAML | 비율·단위 로드 | P1 | ❌ Out of Scope |
| **EXT-02** | 동적 등록 | `1 cubit = 0.4572 m` | 즉시 변환 가능 | P1 | ❌ Out of Scope |
| **EXT-03** | 출력 포맷 | `--format json \| csv \| table` | 포맷별 검증 | P1 | ❌ Out of Scope |

---

## 4. Requirements Traceability (1:1 Test ID)

| Req ID | Layer | Logic `D-*` | UI `U-*` | Error | 비고 |
|--------|-------|---------------|----------|-------|------|
| FR-01 | control | `D-PARSE-01` | `U-PARSE-01` | — | 파싱 성공 경로 |
| FR-02 | entity | `D-CONV-01`~`05` | `U-OUT-01` | — | 3줄 출력·비율 |
| FR-03 | control | `D-VAL-03` | `U-ERR-03` | E003 | unknown unit |
| FR-04 | control | `D-VAL-04` | `U-ERR-04` | E004 | 음수 |
| FR-05 | control | `D-VAL-01` | `U-ERR-01` | E001 | `:` 없음·형식 |
| FR-06 | control | `D-VAL-02` | `U-ERR-02` | E002 | 비숫자 |
| NFR-01 | — | — | — | — | 후속: inch 추가 회귀 |
| NFR-02 | ECB | Track 전체 | Track 전체 | — | `/review-ecb` |
| EXT-01~03 | — | — | — | — | 후속 세션 |

**인프라 (테스트 실행 — Req 아님, Gate):**

| ID | 요구 | 검증 |
|----|------|------|
| **INF-01** | `tests/` 구조 | `tests/__init__.py`, 레거시 `tests/test_convert.py` (Loop B) |
| **INF-02** | 루트 pytest | `python -m pytest tests/` |
| **INF-03** | Dual-Track 디렉터리 | `tests/entity`, `tests/control`, `tests/boundary` |

---

## 5. Goals & Non-Goals

### 5.1 Goals (현재 세션)

1. **FR-01~06** (P0) — 파싱·3단위 출력·검증 시나리오 재현.
2. **INF-01~03** — 루트 pytest import·수집 성공.
3. **NFR-02** — ECB(SRP) 골격: `src/{entity,control,boundary}` + Track 테스트.
4. assert **전부 통과**, 주석·skip·xfail **0개**.

### 5.2 Non-Goals (Out of Scope)

- **EXT-01~03** (JSON/YAML, 동적 단위, `--format`)
- **NFR-01** 완성형 (신규 단위 추가 시 기존 코드 무변경 — 설계만)
- `pip install -e .`, conftest, coverage, CI
- 실패 테스트 **주석 처리 후 제출**
- Golden Master (`tests/golden/*.approved.txt`) — 후속·사용자 승인 후

---

## 6. User & Context

### 6.1 Primary User

부분 단위변환 과제를 받은 **프로그래밍 수업 학생**.

### 6.2 R-G-I-O

| | 내용 |
|---|---|
| **Role** | 부분 단위변환 과제 학생 |
| **Goal** | FR-02 재현 + pytest green + FR-03~06 검증 통과 |
| **Input** | `UnitConverter.py`, README, CLI `unit:value` |
| **Output** | pytest 초록, 추적 가능한 `D-*`/`U-*`, 주석 0 |

---

## 7. Success Criteria (Mom Test · Loop)

| # | Criterion | FR/NFR Link | Evidence |
|---|-----------|-------------|----------|
| SC-01 | 30분 내 pytest import OK | INF-02 | Loop B `--collect-only` |
| SC-02 | 변환·검증 assert 통과 | FR-02, FR-03~06 | Loop A + C |
| SC-03 | 제출 시 실패·주석 assert 0 | — | Exit gate |

---

## 8. User Flow (Session Command)

```
1. README·본 PRD → P0 범위 확정 (FR-01~06, EXT 제외)
2. UnitConverter.py 실행 → Given/Then 기록
3. ECB 분리 (Parser/control · Converter/entity · Printer/boundary)
4. tests/ Track 구조 + test_d_* / test_u_*
5. python -m pytest tests/ → INF-02
6. /tdd-red → D-* RED FAIL → GREEN → Loop A/B/C
7. /review-ecb → ECB 위반 0
8. 제출: 주석 assert 0, pytest green
```

---

## 9. Test Loop (Quality Gate)

### Loop A — Conversion (FR-02)

- **Input:** `meter:2.5`, `feet:1`, `yard:1`
- **Pass:** README 비율·FR-02 Then 일치
- **Command:** `python -m pytest tests/ -k "convert or conv" -v`

### Loop B — Import (INF-02)

- **Command:** `python -m pytest tests/ --collect-only`
- **Pass:** 수집 OK, `ModuleNotFoundError` 없음

### Loop C — Validation (FR-03~06)

- **Cases:** `cubit:1`, `meter:-1`, `meter:hello`, `abc:1`, `meter` (no colon)
- **Pass:** 모든 assert green, 주석 0
- **Command:** `python -m pytest tests/ -v`

**Session Exit:** Loop A + B + C 동시 Pass.

---

## 10. Technical Constraints

| Item | Constraint |
|------|------------|
| Starter | `UnitConverter.py` — main(), if-elif (점진 이전) |
| Architecture | ECB: `boundary → control → entity` |
| Test runner | `python -m pytest tests/` (루트, `pythonpath = ["src"]`) |
| Package setup | `pip install -e .` **사용 안 함** (현재 세션) |
| 비율 SSOT | 3.28084, 1.09361 — 단일 상수 모듈 |

---

## 11. Session Rules (Agent / AI)

1. 목표: **pytest green + FR P0 통과** (EXT P1 선행 구현 금지).
2. import 에러 → 함수 분리·루트 실행; conftest/coverage/`pip install -e .` 제안 금지.
3. 실패 assert → 로직/검증 수정; 주석·삭제·skip·xfail 금지.
4. TDD: `/tdd-red`, Skill `unitconverter-tdd`, 추적성 표(§4) 준수.

---

## 12. Future Scope (P1 — EXT · NFR 완성)

| ID | 내용 |
|----|------|
| EXT-01 | `units.json` / YAML 비율 로드 |
| EXT-02 | `1 cubit = 0.4572 m` 동적 등록 |
| EXT-03 | `--format json \| csv \| table` |
| NFR-01 | `inch` 추가 시 기존 Converter 비수정 (OCP) |

---

## 13. References

- [Report/01.UnitConvert_ProblemDefinition_Report.md](../Report/01.UnitConvert_ProblemDefinition_Report.md)
- [Report/02.UnitConverter_Session4_CursorDesign_Report.md](../Report/02.UnitConverter_Session4_CursorDesign_Report.md)
- [README.md](../README.md) — 전체 과제 (본 PRD는 P0 게이트 + P1 로드맵)
- `.cursorrules` — ECB·E001~E007·Dual-Track 헌법

---

## 14. Revision History

| Version | Date | Note |
|---------|------|------|
| 0.1 (draft) | 2026-06-05 | Mom Test 워크북 초안 |
| 0.2 | 2026-06-05 | FR-01~06 / NFR-01~02 / EXT-01~03 매트릭스, Given/Then/P, 1:1 Test ID 추적, 도메인 계약·ECB↔SRP |
