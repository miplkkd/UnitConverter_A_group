# P1 New Features — Todo (branch: `new_features`)

> 요구: EXT-01 설정 파일 · EXT-02 동적 등록 CLI · EXT-03 `--format`  
> 원칙: BCE `boundary → control → entity` · Dual-Track TDD · TC 1개씩 RED→GREEN

---

## 외부 계약 SSOT (워크북 그림)

### `units.json` — meter 기준 배율 (1 m 대비)

```json
{
  "meter": 1.0,
  "feet": 3.28084,
  "yard": 1.09361
}
```

| 항목 | 규칙 |
|------|------|
| 파일 | 프로젝트 루트 `units.json` · 테스트 `tests/fixtures/units.json` |
| 의미 | **1 meter → N target** (README `METER_TO_FEET` / `METER_TO_YARD` 와 동일) |
| 로드 | entity `load_units_config` → `apply_units_config` → boundary `--config` |

### `--format table` — `meter:2.5` 출력 (4자리 반올림)

```
| unit  | input | result |
|-------|-------|--------|
| meter | 2.5   | 2.5    |
| feet  | 2.5   | 8.2021 |
| yard  | 2.5   | 2.7340 |
```

| 항목 | 규칙 |
|------|------|
| `input` | 원 입력 value (2.5) — **모든 행 동일** |
| `result` | 해당 unit으로 변환된 값 · **소수 4자리** |
| Golden | `tests/golden/u_fmt_01_table_meter_25.approved.txt` |
| legacy | 기존 3줄 텍스트(`U-OUT-01`)는 `format=legacy` 또는 default 유지 검토 |

### `--format json` / `csv` (확장 TC)

| format | 스키마 |
|--------|--------|
| **json** | `[{"unit":"meter","input":2.5,"result":2.5}, ...]` |
| **csv** | `unit,input,result` + 3 data rows |

---

## Feature 1 — EXT-01 · `units.json` 로드

| # | Phase | Layer | Test ID | 작업 | 상태 |
|---|-------|-------|---------|------|:----:|
| 1.1 | RED | entity | **D-CFG-02** | `load_units_config` — flat JSON → `{meter,feet,yard}` | ✅ |
| 1.2 | GREEN | entity | D-CFG-02 | `tests/fixtures/units.json` 파싱 | ✅ |
| 1.3 | RED | entity | **D-CFG-03** | `apply_units_config` — convert feet=8.2021, yard=2.7340 | ✅ |
| 1.4 | GREEN | entity | D-CFG-03 | registry/constants 연동 | ✅ |
| 1.5 | RED | boundary | **U-CFG-01** | `--config units.json` + `format=table` → GM table | ✅ |
| 1.6 | GREEN | boundary | U-CFG-01 | `run_cli_with_config(...)` | ✅ |
| 1.7 | REFACTOR | entity | — | `constants.py` ↔ config 단일 SSOT (OCP) | ✅ |

**Fixture:** `units.json` · `tests/fixtures/units.json`

---

## Feature 2 — EXT-02 · 동적 단위 등록 CLI

| # | Phase | Layer | Test ID | 작업 | 상태 |
|---|-------|-------|---------|------|:----:|
| 2.1 | — | entity | D-REG-01 | cubit `register()` — **GREEN 완료** | ✅ |
| 2.2 | RED | control | **D-REG-02** | `parse_register` — `register:cubit:0.4572` | ✅ |
| 2.3 | GREEN | control | D-REG-02 | unit + meters_per_unit | ✅ |
| 2.4 | RED | boundary | **U-REG-01** | register → `cubit:1` table/json 출력 | ✅ |
| 2.5 | GREEN | boundary | U-REG-01 | `run_cli` register 경로 | ✅ |
| 2.6 | RED | boundary | **U-REG-02** | `register:cubit` → E001 | ✅ |
| 2.7 | REFACTOR | control | — | register 오케스트레이션 SSOT | ✅ |

**입력 계약:** `register:unit:ratio` (ratio = **1 unit → N meter**, cubit 0.4572)

---

## Feature 3 — EXT-03 · `--format json | csv | table`

| # | Phase | Layer | Test ID | 작업 | 상태 |
|---|-------|-------|---------|------|:----:|
| 3.1 | RED | boundary | **U-FMT-01** | `format=table` → pipe table GM | ✅ |
| 3.2 | RED | boundary | **U-FMT-01b** | table 헤더·3 rows 구조 assert | ✅ |
| 3.3 | GREEN | boundary | U-FMT-01 | `format_table_lines()` in `boundary/format.py` | ✅ |
| 3.4 | RED | boundary | **U-FMT-02** | `format=json` → `[{unit,input,result}]` | ✅ |
| 3.5 | GREEN | boundary | U-FMT-02 | `format_json()` | ✅ |
| 3.6 | RED | boundary | **U-FMT-03** | `format=csv` → `unit,input,result` | ✅ |
| 3.7 | GREEN | boundary | U-FMT-03 | `format_csv()` | ✅ |
| 3.8 | REFACTOR | boundary | — | Printer Strategy OCP | ✅ |

**Golden:** `u_fmt_01_table_meter_25.approved.txt` · legacy 3줄 GM(`u_out_01_*`) 유지

---

## 권장 RED 순서 (한 번에 1 TC)

```
D-CFG-02 → D-CFG-03 → U-CFG-01
→ D-REG-02 → U-REG-01 → U-REG-02
→ U-FMT-01 → U-FMT-01b → U-FMT-02 → U-FMT-03
```

## Exit Gate

- [x] `python -m pytest tests/ -v` — **36 passed**
- [x] Loop B `--collect-only` OK
- [x] skip / xfail 0

## P1 후속 (Session 15+)

| # | 작업 | Test ID | 상태 |
|---|------|---------|:----:|
| F-01 | E002/E003 boundary emit + GM | D-VAL-02/03, U-ERR-02/03 | ✅ |
| F-02 | argparse `--format` / `--config` | U-CLI-01 | ✅ |
| F-03 | `UnitConverter.py` ECB wrapper | `cli_main.py` | ✅ |

## GUI Smoke Test (후속 — Session 15)

| # | GUI 반영 | pytest smoke | 상태 |
|---|----------|--------------|:----:|
| G-01 | Output format 콤보 (legacy/table/json/csv) | U-GUI-05 table GM | ✅ |
| G-02 | `units.json` Load 버튼 | U-GUI-06 config+table | ✅ |
| G-03 | register 입력 (`register:unit:ratio`) | U-GUI-07 register→cubit:1 | ✅ |
| G-04 | register 성공 시 짧은 확인 메시지 | U-GUI-07 assert | ✅ |
| G-05 | json/csv format smoke | U-GUI-08 / U-GUI-09 | ✅ |
| G-06 | E002 `meter:hello` | U-GUI-10 → `u_err_02` GM | ✅ |
| G-07 | E003 `furlong:1` | U-GUI-11 → `u_err_03` GM | ✅ |
