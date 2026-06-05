# 테스트 ID — PRD §4 추적성 (1:1)

> 요구: [docs/PRD.md](../../docs/PRD.md) §3~§4 · Logic `D-*` / UI `U-*` / 에러 E001~E004

## Req → Test (요약)

| Req | Logic `D-*` | UI `U-*` | Error |
|-----|---------------|----------|-------|
| FR-01 | D-PARSE-01 | U-PARSE-01 | — |
| FR-02 | D-CONV-01~05 | U-OUT-01 | — |
| FR-03 | D-VAL-03 | U-ERR-03 | E003 |
| FR-04 | D-VAL-04 | U-ERR-04 | E004 |
| FR-05 | D-VAL-01 | U-ERR-01 | E001 |
| FR-06 | D-VAL-02 | U-ERR-02 | E002 |

---

## Logic Track — `D-*`

> **도메인:** 길이 단위 변환 (`meter`/`feet`/`yard`). MagicSquare·격자·`find_blank_coords`·`D-LOC-*` **사용 안 함**.

| ID | FR | Layer | 대상 함수(목표) | 파일(예) | Given → Then |
|----|-----|-------|----------------|----------|--------------|
| D-PARSE-01 | FR-01 | control | `parse_input` | `tests/control/test_d_parse_01.py` | `meter:2.5` → value=2.5, unit=meter |
| D-CONV-01 | FR-02 | entity | `convert_all` | `tests/entity/test_d_conv_01.py` | `2.5 m` → feet **8.20210** (5자리, 3.28084) |
| D-CONV-02 | FR-02 | entity | `convert_all` | `tests/entity/test_d_conv_02.py` | `2.5 m` → yard **2.73403** (1.09361) |
| D-CONV-03 | FR-02 | entity | `to_meter` | `tests/entity/test_d_conv_03.py` | `1 feet` → **0.3048 m** (±ε) |
| D-CONV-04 | FR-02 | entity | `to_meter` | `tests/entity/test_d_conv_04.py` | `1 yard` → meter (1/1.09361) |
| D-CONV-05 | FR-02 | entity | `convert_all` | `tests/entity/test_d_conv_05.py` | feet→yard, **meter 경유** 일치 (직접 비율 금지) |
| D-VAL-01 | FR-05 | control | `tests/control/test_d_val_01.py` | `meter` / `abc:1` → 형식 판정 (E001 조건, emit 없음) |
| D-VAL-02 | FR-06 | control | `tests/control/test_d_val_02.py` | `meter:hello` → 숫자 판정 (E002) |
| D-VAL-03 | FR-03 | control | `tests/control/test_d_val_03.py` | `cubit:1` → unknown 판정 (E003) |
| D-VAL-04 | FR-04 | control | `tests/control/test_d_val_04.py` | `meter:-1` → 음수 판정 (E004) |

---

## UI Track — `U-*`

| ID | FR | Layer | 파일(예) | Given → Then |
|----|-----|-------|----------|--------------|
| U-PARSE-01 | FR-01 | boundary | `tests/boundary/test_u_parse_01.py` | CLI `meter:2.5` → control 경유 파싱 성공 |
| U-OUT-01 | FR-02 | boundary | `tests/boundary/test_u_out_01.py` | `meter:2.5` → meter/feet/yard **3줄** SSOT 형식 |
| U-ERR-01 | FR-05 | boundary | `tests/boundary/test_u_err_01.py` | `meter`, `abc:1` → E001 메시지 emit |
| U-ERR-02 | FR-06 | boundary | `tests/boundary/test_u_err_02.py` | `meter:hello` → E002 emit |
| U-ERR-03 | FR-03 | boundary | `tests/boundary/test_u_err_03.py` | `cubit:1` → E003 emit |
| U-ERR-04 | FR-04 | boundary | `tests/boundary/test_u_err_04.py` | `meter:-1` → E004 emit |

---

## 후속 (P1 — EXT · NFR)

| ID | Req | Layer | 대상 함수(목표) | Given → Then |
|----|-----|-------|----------------|--------------|
| D-REG-01 | EXT-02 | entity | `register` | `cubit` 0.4572 m 등록 → 변환 가능 |
| D-CFG-01 | EXT-01 | entity | `load_config` | 깨진 JSON → `ConfigError` |
| — | NFR-01 | entity | — | `inch` 추가 시 기존 Converter 비수정 회귀 |
| — | EXT-03 | boundary | — | `--format json \| csv \| table` |

---

## RED 묶음 권장 순서 (Track B · entity)

| 순서 | Test ID | pytest 예시 |
|------|---------|-------------|
| 1 | **D-CONV-01** | `tests/entity/test_d_conv_01.py::test_d_conv_01_meter_to_feet` |
| 2 | D-CONV-03 | `tests/entity/test_d_conv_03.py::test_d_conv_03_feet_to_meter` |
| 3 | D-CONV-05 | `tests/entity/test_d_conv_05.py::test_d_conv_05_feet_yard_via_meter` |
