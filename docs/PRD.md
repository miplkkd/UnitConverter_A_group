# PRD — UnitConverter_Agroup (Session Scope)

> Product Requirements Document  
> 기준: [Report/01.UnitConvert_ProblemDefinition_Report.md](../Report/01.UnitConvert_ProblemDefinition_Report.md)  
> Mom Test 인터뷰 기반 초안

---

## 1. Overview

### 1.1 Product Statement (Problem-First)

**과제 첫날에 변환 결과를 재현 가능하게 확인하고, import 막힘 없이 테스트가 돌아가게 만든다.**

본 PRD는 README 전체 요구사항 중 **이번 세션에서 반드시 달성할 범위**만 정의한다. OCP/SRP 완성형 아키텍처·추가 요구(JSON, 동적 단위)는 후속 세션으로 미룬다.

### 1.2 Background

| 구분 | 내용 |
|------|------|
| 페르소나 | 프로그래밍 수업, 부분 단위변환 과제, 6시간 실습 |
| 표면 문제 (금지) | 「OCP·SRP 단위 변환 프로그램 + pytest 테스트 작성」 |
| 진짜 문제 | main()만 있는 starter에 테스트·설계·마감이 겹치면 import 막힘·손계산·실패 테스트 주석 처리로 이어짐 |

---

## 2. Goals & Non-Goals

### 2.1 Goals

1. meter / feet / yard 변환 결과를 README 비율과 일치하게 **재현**.
2. 프로젝트 루트에서 `python -m pytest tests/` **import 에러 없이 실행**.
3. 정상 변환·오입력·음수에 대한 assert **전부 통과** (주석 처리 0개).

### 2.2 Non-Goals (Out of Scope)

- JSON / CSV / 표 형태 출력
- 동적 단위 등록 (`1 cubit = 0.4572 meter` 등)
- OCP/SRP **완성형** 인터페이스·클래스 풀 설계
- `pip install -e .`, conftest, coverage, CI
- 실패 테스트 **주석 처리 후 제출** (명시적 금지)

---

## 3. User & Context

### 3.1 Primary User

부분 단위변환 과제를 받은 **프로그래밍 수업 학생**.

- pytest/import 경험은 있으나 프로젝트 구조·분리는 미숙
- 마감·실습 시간 압박 하에서 「변환 먼저, 테스트 나중」으로 우선순위가 어긋날 수 있음

### 3.2 R-G-I-O

| | 내용 |
|---|---|
| **Role** | 부분 단위변환 과제 학생 |
| **Goal** | 변환 재현 + pytest 실행 성공 + 실패 테스트 미제거·통과 |
| **Input** | `UnitConverter.py`, README, CLI 입력 (`unit:value`) |
| **Output** | pytest 초록, 검증 포함 assert 통과, 주석 처리 테스트 0개 |

---

## 4. Functional Requirements

### 4.1 Conversion (Must Have)

| ID | Requirement | Acceptance |
|----|-------------|------------|
| FR-01 | `meter`, `feet`, `yard` 입력 단위 지원 | `meter:2.5` 등 정상 입력 시 세 단위 모두 출력 |
| FR-02 | README 비율 준수 | 1m = 3.28084ft, 1m = 1.09361yd 기준 |
| FR-03 | 변환 로직 테스트 가능 | main() 외 import 가능한 함수/클래스로 분리 |

### 4.2 Input Validation (Must Have)

| ID | Requirement | Acceptance |
|----|-------------|------------|
| FR-04 | 형식 검증 | `:` 없음 → 오류 처리 |
| FR-05 | 숫자 검증 | `meter:hello` → 오류 처리 |
| FR-06 | 단위 검증 | unknown unit → 오류 처리 |
| FR-07 | 음수 검증 | 음수 값 → 오류 처리 (테스트 통과, **주석 처리 금지**) |

### 4.3 Test Infrastructure (Must Have)

| ID | Requirement | Acceptance |
|----|-------------|------------|
| FR-08 | tests/ 구조 | `tests/__init__.py`, `tests/test_convert.py` |
| FR-09 | 루트 실행 | `python -m pytest tests/` (프로젝트 루트 cwd) |
| FR-10 | 최소 테스트 세트 | 정상 변환 2~3 + 오입력 + 음수 |

---

## 5. Success Criteria (Mom Test Linked)

| # | Criterion | Evidence Link |
|---|-----------|---------------|
| SC-01 | 첫 세션 **30분 내** pytest import 에러 없이 실행 | ModuleNotFoundError → 파일 닫음; TA 후 40분~1시간 |
| SC-02 | 변환·검증 assert 통과, README 숫자 일치 | 손계산 대체; 주석 처리 제출 |
| SC-03 | 제출 시 실패·주석 assert **0개** | 「빼고 제출해도 되냐」 패턴 차단 |

---

## 6. User Flow (Session Command)

```
1. README 확인 → 범위 확정 (기본 3단위 + 검증)
2. UnitConverter.py 실행 → 정상/오입력/음수 동작 기록
3. 변환·검증 로직 분리 (main = I/O only)
4. tests/ 생성
5. python -m pytest tests/ → import OK
6. assert 추가 → 전부 green
7. 제출 게이트: 주석 assert 0, pytest green
```

---

## 7. Test Loop (Quality Gate)

### Loop A — Conversion Reproducibility

- **Input:** `meter:2.5`, `feet:1`, `yard:1`
- **Pass:** README 비율과 assert 일치
- **Fail:** 코드 수정 후 재실행

### Loop B — Import & Collection

- **Command:** `python -m pytest tests/ --collect-only`
- **Pass:** tests 수집, ModuleNotFoundError 없음
- **Fail:** 함수 분리·경로 점검 후 재실행

### Loop C — Validation & Submission Gate

- **Cases:** `abc:1`, `meter:hello`, `meter:-1`, unknown unit
- **Pass:** 모든 assert green, 주석 0
- **Fail:** 검증 로직 구현 (assert 삭제·주석 **금지**)

**Session Exit:** Loop A + B + C 동시 Pass.

---

## 8. Technical Constraints

| Item | Constraint |
|------|------------|
| Starter | `UnitConverter.py` — main(), if-elif 구조 |
| Test runner | `python -m pytest tests/` (루트) |
| Package setup | `pip install -e .` **사용 안 함** (이번 세션) |
| 비율 | meter 기준: feet 3.28084, yard 1.09361 |

---

## 9. Session Rules (Agent / AI Guidance)

1. 목표는 「앱 완성」이 아니라 「pytest green + 검증 통과」.
2. import 에러 시 **함수 분리·루트 실행** 먼저; conftest/coverage/editable install 제안 금지.
3. 실패 assert → **검증/로직 수정**; 주석 처리·삭제로 통과시키지 않음.
4. 추가 요구(JSON, 동적 단위)는 이번 PRD 범위 밖.

### Optional Skill: pytest-import-unblock

- **Trigger:** ModuleNotFoundError, import 실패
- **Steps:** cwd 루트 → `python -m pytest tests/` → `__init__.py` → 분리된 함수 import
- **Avoid:** pip install -e ., conftest, coverage 우선 제안

---

## 10. Future Scope (Not This Session)

- 설정 외부화 (JSON/YAML)
- 동적 단위 등록
- 출력 포맷 (JSON / CSV / table)
- OCP/SRP 완성형 리팩터링 및 확장 단위

---

## 11. References

- [Report/01.UnitConvert_ProblemDefinition_Report.md](../Report/01.UnitConvert_ProblemDefinition_Report.md)
- [README.md](../README.md) — 전체 과제 요구사항 (본 PRD는 부분 범위)

---

## 12. Revision History

| Version | Date | Note |
|---------|------|------|
| 0.1 (draft) | 2026-06-05 | Mom Test 워크북 초안 기반 PRD 생성 |
