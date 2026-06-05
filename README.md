# UnitConverter_Agroup

> Mom Test · ECB(BCE) · Dual-Track TDD · IBAC/BCE/RBS  
> 상세: [docs/PRD.md](./docs/PRD.md) · [docs/IBAC-BCE-RBS.md](./docs/IBAC-BCE-RBS.md) · [Report/01](./Report/01.UnitConvert_ProblemDefinition_Report.md)

**원격:** https://github.com/miplkkd/UnitConverter_A_group.git

---

## 이번 README 안내

- **현재 유효:** 아래 「세션 개요」~「관련 문서」
- **레거시:** 맨 아래 **「기존 README (Original — 레거시)」** — 원본 6시간 Activities·추가 요구 전체

---

## 세션 개요

### 주제 (한 문장)

**과제 첫날에 변환 결과를 재현 가능하게 확인하고, import 막힘 없이 Dual-Track pytest가 돌아가게 만든다.**

### 진짜 문제

`main()` starter + 테스트·마감이 겹치면 import 막힘·손계산·실패 테스트 제거로 이어진다.

### 개발 3축

| 축 | 의미 |
|----|------|
| **BCE** | `boundary → control → entity` (ECB와 동일) |
| **IBAC** | Input → Boundary → Application(control) → Core(entity) |
| **RBS** | RED → Green → Stabilize + FR↔`D-*`/`U-*` 추적 |

### P0 범위 / Out of Scope

| Must (P0) | Out of Scope (P1) |
|-----------|-------------------|
| `meter`/`feet`/`yard` 변환·검증 | JSON/YAML 설정 (`D-CFG-01`) |
| `unit:value` 파싱·E001~E004 | 동적 단위 등록 (`D-REG-01`) |
| Dual-Track pytest RED→GREEN | `pip install -e .`, conftest, CI |
| ECB 골격 `src/{boundary,control,entity}` | 실패 assert 주석 처리 |

---

## R-G-I-O

| | 내용 |
|---|---|
| **Role** | 부분 단위변환 과제 학생 |
| **Goal** | FR-02 재현 + pytest green + FR-03~06 검증 통과 |
| **Input** | `unit:value`, README 비율, `UnitConverter.py` |
| **Output** | Track pytest PASS, 주석·skip·xfail 0 |

---

## 프로젝트 구조

```
UnitConverter_Agroup/
├── UnitConverter.py              # 레거시 starter (점진 이전)
├── pyproject.toml                # pythonpath = ["src"]
├── src/
│   ├── boundary/app.py           # CLI · E001~E005 emit
│   ├── control/                  # (GREEN) 파싱·판정
│   └── entity/
│       ├── convert.py            # to_meter · convert_all
│       ├── registry.py           # P1 동적 등록
│       └── config.py             # P1 JSON 로드
├── tests/
│   ├── boundary/                 # Track A — UI (U-*)
│   │   ├── test_u_in_01.py       # U-IN-01  "" → 형식 오류
│   │   ├── test_u_in_02.py       # U-IN-02  meter → 형식 오류
│   │   ├── test_u_in_03.py       # U-IN-03  meter:-1 → 음수 거부
│   │   └── test_u_out_01.py      # U-OUT-01 meter:2.5 → 3줄
│   └── entity/                   # Track B — Logic (D-*)
│       ├── test_d_cnv_01.py      # D-CNV-01 to_meter
│       ├── test_d_cnv_02.py      # D-CNV-02 convert_all
│       ├── test_d_cnv_03.py      # D-CNV-03 meter 경유 일치
│       ├── test_d_reg_01.py      # D-REG-01 (P1)
│       └── test_d_cfg_01.py      # D-CFG-01 (P1)
├── docs/PRD.md
├── Report/01~03
├── prompting/01~05
└── .cursorrules · .cursor/skills · .cursor/commands
```

---

## 도메인 계약

| 항목 | 규칙 |
|------|------|
| 입력 | `unit:value` (예 `meter:2.5`) |
| 비율 SSOT | 1 m = **3.28084** ft, 1 m = **1.09361** yd |
| 변환 | `feet`↔`yard`는 **meter 경유**만 |
| 성공 출력 | meter / feet / yard **3줄** (boundary SSOT) |
| 오류 | E001 형식 · E002 숫자 · E003 unknown · E004 음수 — **boundary만 emit** |

테스트 ID 전체: [.cursor/skills/unitconverter-tdd/reference.md](./.cursor/skills/unitconverter-tdd/reference.md)

---

## 빠른 시작

```bash
# 프로젝트 루트로 이동 (필수)
cd UnitConverter_Agroup

# 가상환경 (선택)
python -m venv venv
venv\Scripts\activate          # Windows

# 레거시 CLI
python UnitConverter.py

# 전체 테스트
python -m pytest tests/ -v

# Track별
python -m pytest tests/boundary -v    # UI — U-IN / U-OUT
python -m pytest tests/entity -v      # Logic — D-CNV / D-REG / D-CFG

# 단일 RED 예시
python -m pytest tests/entity/test_d_cnv_02.py::test_d_cnv_02_meter_to_feet -v
python -m pytest tests/boundary/test_u_in_02.py::test_u_in_02_meter_no_colon_format_error -v

# import·수집만 (Loop B)
python -m pytest tests/ --collect-only
```

**cwd:** `UnitConverter.py`와 `tests/`가 있는 **프로젝트 루트**. `pyproject.toml`의 `pythonpath = ["src"]`로 `entity`·`boundary` import.

---

## TDD — RED / GREEN

| Phase | 할 일 | 금지 |
|-------|--------|------|
| **RED** | `tests/`만 작성·실행, **FAIL 확인** | `src/` 로직 선행, skip/xfail |
| **GREEN** | 해당 Layer `src/` 최소 구현 | assert 완화·삭제 |
| **REFACTOR** | SSOT·이름·중복 정리 | 공개 계약 변경 |

**RED 기대 실패:** `ModuleNotFoundError` 대신 워크북 **Then** 기준 `AssertionError` (예 `RED: U-IN-01 — format error`). import 스텁은 `src/`에만 둠.

Cursor: `/tdd-red` · `/review-ecb` · `/kdreport`

---

## Test Loop (품질 게이트)

| Loop | 명령 | Pass |
|------|------|------|
| **A — 재현** | `python -m pytest tests/entity -k cnv -v` | README 비율·D-CNV PASS |
| **B — import** | `python -m pytest tests/ --collect-only` | 수집 OK |
| **C — 검증** | `python -m pytest tests/boundary -v` | U-IN/U-OUT PASS |

**세션 Exit:** A + B + C 동시 Pass, skip/xfail 0.

---

## 현재 진행 상태 (2026-06-05)

| 구분 | 상태 |
|------|------|
| RED 스켈레톤 (9 tests) | ✅ 수집·의미 있는 FAIL |
| `src/` 스텁 | ✅ import 경로 (미구현) |
| GREEN (`convert_all`, `run_cli` 등) | ❌ 다음 단계 |
| `src/control/` | ❌ 미생성 |

---

## Mom Test 증거 (요약)

- 「**일단 변환부터** 하고 파일 닫음」— import 막힘
- 「README 숫자만 맞으면」— 손계산 대체
- 「**주석 처리하고 제출**」— 검증 미구현

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](./docs/PRD.md) | FR-01~06 · INF · 1:1 Test ID (v0.2) |
| [docs/IBAC-BCE-RBS.md](./docs/IBAC-BCE-RBS.md) | IBAC · BCE · RBS 가이드 |
| [Report/01](./Report/01.UnitConvert_ProblemDefinition_Report.md) | Mom Test 문제 정의 |
| [Report/02](./Report/02.UnitConverter_Session4_CursorDesign_Report.md) | Cursor 8계층 설계 |
| [Report/03](./Report/03.UnitConverter_Session5_IBAC_RED_KDReport_Report.md) | IBAC·RED·kdreport |
| [reference.md](./.cursor/skills/unitconverter-tdd/reference.md) | `D-*` / `U-*` SSOT |
| [prompting/](./prompting/) | 세션별 Transcript export |

---

## 후속 (P1)

- `D-REG-01` 동적 단위 · `D-CFG-01` JSON
- `src/control/` 판정·파싱
- OCP/SRP 완성형 · `--format json|csv|table`

---

---

# 기존 README (Original — 레거시)

> **아래는 Mom Test 작업 이전의 원본 과제 README입니다.**  
> 전체 6시간 Activities·추가 요구사항·OCP/SRP 풀 스펙이 포함되어 있습니다.  
> **이번 세션의 실행 범위는 위 「세션 개요」~「Test Loop」를 따릅니다.**

<details>
<summary>기존 README 전문 펼치기</summary>

## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점

</details>
