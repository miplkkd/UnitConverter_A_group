# UnitConverter_Agroup

> Mom Test 인터뷰 기반 문제 정의 · 세션 범위 README  
> 상세: [Report/01.UnitConvert_ProblemDefinition_Report.md](./Report/01.UnitConvert_ProblemDefinition_Report.md) · [docs/PRD.md](./docs/PRD.md)

---

## 이번 README 안내

**이 파일은 Mom Test 워크북·문제 정의 보고서·PRD 작업 이후 갱신된 README입니다.**

- **현재 유효한 안내:** 아래 「세션 개요」부터 「관련 문서」까지
- **기존 과제 안내 (레거시):** 맨 아래 **「기존 README (Original — 레거시)」** 섹션 — 원본 과제 PDF/README 수준의 전체 요구사항. 이번 세션 범위와 다를 수 있음

---

## 세션 개요

### 주제 (한 문장)

**과제 첫날에 변환 결과를 재현 가능하게 확인하고, import 막힘 없이 테스트가 돌아가게 만드는 것까지가 목표다.**

### 진짜 문제

main()만 있는 시작 코드에 테스트·설계·제출 마감이 동시에 걸리면, 학생은 첫날 import·환경 막힘에 시간을 쓰고 변환은 손계산으로 대신하며, 마감 직전에는 실패한 테스트를 고치기보다 빼서 제출 판정만 맞추려 한다.

### 표면 문제 (이번 세션에서 하지 않을 것)

| 금지 / Out of Scope | 이유 |
|---------------------|------|
| 「OCP·SRP 완성형 단위 변환 프로그램 + pytest」만을 목표로 삼기 | 제품 정의가 실제 막힘(import·재현·제출)과 어긋남 |
| JSON / CSV / 표 출력, 동적 단위 등록 | 인터뷰: 「시간 남으면」→ 미착수 |
| `pip install -e .`, conftest, coverage, CI | 1일차를 환경 셋업이 잡아먹음 |
| 실패 assert 주석 처리 후 제출 | 인터뷰: 검증 미구현 시 테스트 제거 패턴 |

---

## R-G-I-O

| | 내용 |
|---|---|
| **Role** | 프로그래밍 수업, 부분 단위변환 과제를 받은 학생 |
| **Goal** | 변환 숫자 재현 + 루트에서 pytest 실행 성공 + 실패 테스트를 주석 처리하지 않고 통과 |
| **Input** | `UnitConverter.py`, README 비율·검증 요구, CLI 입력 (`meter:2.5`, 오입력 등) |
| **Output** | `python -m pytest tests/` 초록, 변환·검증 assert 통과, 주석 처리 테스트 0개 |

---

## 성공 기준 (Mom Test 증거 연결)

| # | 기준 | 연결 증거 |
|---|------|-----------|
| 1 | **첫 세션 30분 내** 루트에서 `python -m pytest tests/` import 에러 없이 실행 | ModuleNotFoundError 후 파일 닫음; TA 후 40분~1시간 만에 초록 |
| 2 | 정상 변환 + 오입력 + 음수 테스트 통과, README 비율(3.28084 / 1.09361) 일치 | 손계산 대체; 실패 테스트 주석 처리 제출 |
| 3 | 제출 시 실패·주석 assert **0개** | 「이 assert 빼고 제출해도 되냐」 패턴 차단 |

---

## 이번 세션 범위 (Must Have)

### 변환

- 단위: `meter`, `feet`, `yard`
- 비율: `1 meter = 3.28084 feet`, `1 meter = 1.09361 yard`
- 변환·검증 로직은 **import 가능한 함수/클래스**로 분리 (`main()`은 입출력만)

### 입력 검증

- 형식 (`:` 없음), 숫자 (`meter:hello`), unknown unit, **음수** — 테스트로 고정, 주석 처리 금지

### 테스트 구조

```
UnitConverter_Agroup/
├── UnitConverter.py
├── tests/
│   ├── __init__.py
│   └── test_convert.py
├── Report/
│   └── 01.UnitConvert_ProblemDefinition_Report.md
├── docs/
│   └── PRD.md
└── prompting/
    ├── 01.step1-mom-test-prompt.md
    └── 02.transcript-export.md
```

---

## 빠른 시작

```bash
# 가상환경 (선택)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 프로그램 실행 (프로젝트 루트)
python UnitConverter.py

# 테스트 (프로젝트 루트 — cwd 중요)
python -m pytest tests/
python -m pytest tests/ --collect-only   # import·수집만 확인
```

**import 에러 시 우선 확인:** (1) cwd가 `UnitConverter.py`와 `tests/` 있는 루트인지 (2) `tests/__init__.py` 존재 (3) 테스트 대상이 `main()`이 아닌 분리된 함수/클래스인지

---

## 세션 Command (권장 순서)

1. README·PRD 범위 확인 → **기본 3단위 + 검증**만
2. `UnitConverter.py` 실행 → `meter:2.5`, `abc:1`, `meter:hello`, 음수 동작 기록
3. 변환·검증 로직 분리
4. `tests/__init__.py`, `tests/test_convert.py` 작성
5. `python -m pytest tests/` → import OK
6. assert: 정상 2~3 + 오입력 + 음수 → 전부 green
7. 제출 게이트: 주석 assert 0, pytest green

---

## Test Loop (품질 게이트)

| Loop | 내용 | Pass |
|------|------|------|
| **A — 재현** | meter/feet/yard 변환 | README 비율·assert 일치 |
| **B — import** | `python -m pytest tests/ --collect-only` | 수집 OK, ModuleNotFoundError 없음 |
| **C — 검증** | abc:1, meter:hello, 음수, unknown unit | assert 전부 통과, 주석 0 |

**세션 종료:** A + B + C 동시 Pass.

---

## Mom Test 증거 (요약)

- 「`sys.path` … **더 읽기 싫어졌어요**. **일단 변환부터** 하고 파일 닫음」
- 「**pytest는 환경/경로 문제**, README 숫자만 맞으면 발표 때 덜 당황」
- 「음수 테스트 실패 → **주석 처리하고 제출**」

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [Report/01.UnitConvert_ProblemDefinition_Report.md](./Report/01.UnitConvert_ProblemDefinition_Report.md) | Mom Test 인터뷰·문제 정의·Rule/Command/Test Loop |
| [docs/PRD.md](./docs/PRD.md) | 세션 범위 PRD (FR, Non-Goals, Test Loop) |
| [prompting/01.step1-mom-test-prompt.md](./prompting/01.step1-mom-test-prompt.md) | STEP 1 Mom Test 인터뷰 프롬프트·규칙·종료 지시 |
| [prompting/02.transcript-export.md](./prompting/02.transcript-export.md) | 유효 세션(2개) 통합 트랜스크립트 |

---

## 후속 세션 (Not This Session)

- 설정 외부화 (JSON/YAML)
- 동적 단위 등록
- 출력 포맷 (JSON / CSV / table)
- OCP/SRP 완성형 리팩터링

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
