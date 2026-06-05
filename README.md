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

**P0 변환·검증에 P1 확장(units.json · register CLI · `--format`)을 ECB Dual-Track pytest로 GREEN하고, Golden Master·PyQt GUI까지 수동·자동 확인 가능하게 만든다.**

### 진짜 문제

`main()` starter + 테스트·마감이 겹치면 import 막힘·손계산·실패 테스트 제거로 이어진다.

### 개발 3축

| 축 | 의미 |
|----|------|
| **BCE** | `boundary → control → entity` (ECB와 동일) |
| **IBAC** | Input → Boundary → Application(control) → Core(entity) |
| **RBS** | RED → Green → Stabilize + FR↔`D-*`/`U-*` 추적 |

### P0 범위 / P1 (Session 14 GREEN)

| Must (P0) | P1 (EXT-01~03) — ✅ GREEN |
|-----------|---------------------------|
| `meter`/`feet`/`yard` 변환·검증 | **`units.json` 로드** (`load_units_config` · `--config`) |
| `unit:value` 파싱·E001~E004 (U-IN/U-OUT) | **동적 등록 CLI** (`register:unit:ratio`) |
| Dual-Track pytest RED→GREEN | **`--format table \| json \| csv`** (legacy 3줄 유지) |
| ECB `src/{boundary,control,entity}` | table Golden `u_fmt_01_table_meter_25` |
| Golden Master (boundary 4건) | |
| PyQt GUI + pytest-qt (U-GUI) | |
| Out of Scope | E002/E003 emit · GUI format/config · CI |

---

## R-G-I-O

| | 내용 |
|---|---|
| **Role** | 부분 단위변환 과제 학생 |
| **Goal** | FR-02 재현 + pytest green + FR-03~06 검증 통과 |
| **Input** | `unit:value`, README 비율, CLI/GUI |
| **Output** | Track pytest PASS (23), Golden Master 5/5, skip/xfail 0 |

---

## 프로젝트 구조

```
UnitConverter_Agroup/
├── UnitConverter.py              # 레거시 starter (점진 이전)
├── units.json                    # P1 EXT-01 샘플 (meter 기준 배율)
├── run_gui.py                    # PyQt GUI 실행 (src 경로 자동 추가)
├── pyproject.toml                # pythonpath = ["src"], optional [gui]
├── src/
│   ├── boundary/
│   │   ├── app.py                # CLI · process_input · register · format/config
│   │   ├── format.py             # legacy 3줄 · table · json · csv SSOT
│   │   ├── messages.py           # E001~E004 메시지 SSOT
│   │   └── gui_app.py            # PyQt6 GUI (control 경유)
│   ├── control/
│   │   ├── parse.py              # unit:value 파싱 SSOT
│   │   ├── convert_service.py    # 파싱·변환 오케스트레이션
│   │   ├── register_service.py   # D-REG-02 register:unit:ratio 파싱
│   │   └── validation.py         # E001/E004 판정 (emit 없음)
│   └── entity/
│       ├── constants.py          # 비율 SSOT (기본값)
│       ├── convert.py            # to_meter · convert_all (config-aware)
│       ├── registry.py           # D-REG-01 동적 등록
│       └── config.py             # D-CFG-01~03 JSON · units.json
├── tests/
│   ├── _approval.py              # GM · assert_cli_golden · assert_matches_golden
│   ├── fixtures/units.json       # P1 테스트 fixture
│   ├── golden/                   # boundary stdout SSOT (*.approved.txt)
│   ├── boundary/                 # Track A — UI (U-*)
│   │   ├── test_u_in_01~03.py    # U-IN E001/E004
│   │   ├── test_u_out_01.py      # U-OUT 성공 3줄
│   │   ├── test_u_cfg_01.py      # U-CFG-01 --config + table
│   │   ├── test_u_fmt_01.py      # U-FMT-01~03 table/json/csv
│   │   ├── test_u_reg_01~02.py   # U-REG register CLI
│   │   ├── test_u_gui_01.py      # U-GUI-01 PyQt 성공
│   │   └── test_u_gui_errors.py  # U-GUI-02~04 PyQt 오류
│   ├── control/
│   │   └── test_d_reg_02.py      # D-REG-02 parse_register
│   └── entity/                   # Track B — Logic (D-*)
│       ├── test_d_cnv_01~03.py
│       ├── test_d_reg_01.py
│       └── test_d_cfg_01~03.py
├── docs/PRD.md · docs/P1_NEW_FEATURES_TODO.md
├── Report/01~12
├── prompting/01~14
└── .cursorrules · .cursor/skills · .cursor/commands
```

---

## 도메인 계약

| 항목 | 규칙 |
|------|------|
| 입력 | `unit:value` (예 `meter:2.5`) |
| 비율 SSOT | 1 m = **3.28084** ft, 1 m = **1.09361** yd |
| 변환 | `feet`↔`yard`는 **meter 경유**만 |
| 성공 출력 | meter / feet / yard **3줄** (legacy) · **table/json/csv** (P1 `--format`) |
| `units.json` | flat JSON · meter=1.0, feet=3.28084, yard=1.09361 (1 m → N target) |
| register | `register:unit:ratio` (ratio = 1 unit → N meter, 예 `register:cubit:0.4572`) |
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

# 레거시 CLI (starter)
python UnitConverter.py

# ECB CLI (boundary SSOT) — legacy 3줄
python -c "from boundary.app import run_cli; run_cli('meter:2.5')"

# P1 — table / json / csv
python -c "from boundary.app import run_cli_with_format; run_cli_with_format('meter:2.5', 'table')"
python -c "from boundary.app import run_cli_with_config; run_cli_with_config('meter:2.5', 'units.json', 'table')"

# register → convert
python -c "from boundary.app import run_cli; run_cli('register:cubit:0.4572'); run_cli('cubit:1')"

# 전체 테스트 (23)
python -m pytest tests/ -v

# Track별
python -m pytest tests/boundary -v    # UI — U-IN / U-OUT / U-GUI / U-CFG / U-FMT / U-REG
python -m pytest tests/entity tests/control -v   # Logic — D-CNV / D-REG / D-CFG

# Golden Master (boundary만)
python -m pytest tests/boundary/test_u_in_01.py tests/boundary/test_u_in_02.py tests/boundary/test_u_in_03.py tests/boundary/test_u_out_01.py -v

# Golden 갱신 (의도적 출력 변경 시만)
$env:UPDATE_GOLDEN="1"; python -m pytest tests/boundary/ -v   # PowerShell
# UPDATE_GOLDEN=1 python -m pytest tests/boundary/ -v         # bash

# PyQt GUI (수동 확인)
pip install -e ".[gui]"    # PyQt6 + pytest-qt
python run_gui.py

# PyQt GUI 자동 테스트
python -m pytest tests/boundary/test_u_gui_01.py tests/boundary/test_u_gui_errors.py -v

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
| **B — import** | `python -m pytest tests/ --collect-only` | 수집 OK (23 tests) |
| **C — 검증** | `python -m pytest tests/boundary -v` | U-IN/U-OUT/U-GUI PASS |
| **D — Golden** | `python -m pytest tests/boundary/test_u_*.py -v` | GM 5/5 matched |

**세션 Exit:** A + B + C + D 동시 Pass, skip/xfail 0.

---

## Golden Master (boundary)

| Test ID | golden 파일 | 내용 |
|---------|-------------|------|
| U-OUT-01 | `tests/golden/u_out_01_meter_25.approved.txt` | `meter:2.5` 성공 3줄 (legacy) |
| U-FMT-01 | `tests/golden/u_fmt_01_table_meter_25.approved.txt` | `meter:2.5` pipe table |
| U-IN-01 | `tests/golden/u_in_01_empty.approved.txt` | 빈 입력 E001 |
| U-IN-02 | `tests/golden/u_in_02_no_colon.approved.txt` | 콜론 없음 E001 |
| U-IN-03 | `tests/golden/u_in_03_negative.approved.txt` | 음수 E004 |

헬퍼: `tests/_approval.py` — `assert_cli_golden` · `run_gui_output` · `assert_matches_golden`

---

## PyQt GUI

| 항목 | 내용 |
|------|------|
| 실행 | `python run_gui.py` (프로젝트 루트) |
| 구현 | `src/boundary/gui_app.py` — `process_input()` SSOT (CLI와 동일) |
| 자동 테스트 | `test_u_gui_01.py`, `test_u_gui_errors.py` (pytest-qt) |
| 의존성 | `pip install -e ".[gui]"` → PyQt6, pytest-qt |

---

## REFACTOR (`refactoring` 브랜치 · `/refactor-safe`)

| # | 대상 | 파일 | GM diff |
|---|------|------|:-------:|
| 1 | `parse_unit_value` Extract | `control/parse.py` | 0 |
| 2 | `assert_cli_golden` Extract | `tests/_approval.py` | 0 |
| 3 | CLI Golden 4/4 헬퍼 통일 | `test_u_in_01~03`, `test_u_out_01` | 0 |
| 4 | `run_gui_output` Extract | `tests/_approval.py` | 0 |
| 5 | GUI Golden 4/4 헬퍼 통일 | `test_u_gui_01`, `test_u_gui_errors` | 0 |
| 6 | entity Magic Number → SSOT | `test_d_cnv_01`, `test_d_cnv_02` | N/A |

**원칙:** 외부 계약(출력·메시지) 변경 금지 · 매 커밋 pytest PASS + GM matched.

**PR:** [#4](https://github.com/miplkkd/UnitConverter_A_group/pull/4) (`refactoring` → `main`)

---

## P1 New Features (`new_features` 브랜치 · Session 14)

| EXT | 기능 | Test ID | 상태 |
|-----|------|---------|:----:|
| EXT-01 | `units.json` 로드 · apply | D-CFG-02/03, U-CFG-01 | ✅ |
| EXT-02 | `register:unit:ratio` CLI | D-REG-02, U-REG-01/02 | ✅ |
| EXT-03 | `--format table\|json\|csv` | U-FMT-01~03 | ✅ |

**table 출력 예 (`meter:2.5`):**

```
| unit  | input | result |
|-------|-------|--------|
| meter | 2.5   | 2.5    |
| feet  | 2.5   | 8.2021 |
| yard  | 2.5   | 2.7340 |
```

상세 Todo: [docs/P1_NEW_FEATURES_TODO.md](./docs/P1_NEW_FEATURES_TODO.md)

---

## 현재 진행 상태 (2026-06-05)

| 구분 | 상태 |
|------|------|
| Logic Track (D-CNV, D-REG, D-CFG) | ✅ GREEN 8/8 |
| UI Track CLI (U-IN/U-OUT/U-CFG/U-FMT/U-REG) | ✅ GREEN 10/10 |
| PyQt GUI (U-GUI-01~04) | ✅ GREEN 4/4 |
| Golden Master (boundary) | ✅ 5/5 matched |
| REFACTOR (Session 11~13) | ✅ 6건 · GM diff 0 |
| P1 EXT-01~03 (`new_features`) | ✅ GREEN 10 TC |
| **전체 pytest** | ✅ **23 passed** |
| E002/E003 boundary emit | ❌ 후속 |
| GUI `--format` / `--config` | ❌ 후속 |
| Report / Transcript | ✅ 01~12 / 01~14 |

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
| [Report/04~12](./Report/) | RED · GREEN · Golden Master · PyQt · Refactor · P1 |
| [Report/12](./Report/12.UnitConverter_Session14_P1_NewFeatures_GREEN_Report.md) | Session 14 P1 GREEN |
| [docs/P1_NEW_FEATURES_TODO.md](./docs/P1_NEW_FEATURES_TODO.md) | P1 Todo · SSOT |
| [reference.md](./.cursor/skills/unitconverter-tdd/reference.md) | `D-*` / `U-*` SSOT |
| [prompting/](./prompting/) | 세션별 Transcript export (01~14) |

---

## 후속

- E002/E003 boundary emit (`meter:hello`, unknown unit) + GM
- GUI `--format` / `--config` 연동 (`gui_app.py`)
- REFACTOR Printer Strategy OCP · `constants` ↔ config 단일 SSOT
- `registry.register` 파라미터 rename · `UnitConverter.py` ECB wrapper (P2)

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
