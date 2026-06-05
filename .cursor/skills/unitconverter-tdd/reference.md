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

| ID | FR | Layer | 파일(예) | Given → Then |
|----|-----|-------|----------|--------------|
| D-PARSE-01 | FR-01 | control | `tests/control/test_d_parse_01.py` | `meter:2.5` → value=2.5, unit=meter |
| D-CONV-01 | FR-02 | entity | `tests/entity/test_d_conv_01.py` | meter 2.5 → feet ≈ 8.2021 (3.28084) |
| D-CONV-02 | FR-02 | entity | `tests/entity/test_d_conv_02.py` | meter 2.5 → yard ≈ 2.7340 (1.09361) |
| D-CONV-03 | FR-02 | entity | `tests/entity/test_d_conv_03.py` | feet → meter (meter 경유) |
| D-CONV-04 | FR-02 | entity | `tests/entity/test_d_conv_04.py` | yard → meter (meter 경유) |
| D-CONV-05 | FR-02 | entity | `tests/entity/test_d_conv_05.py` | 입력 단위 → 3단위 값 일관 |
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

## 후속 (P1 — 테스트 ID 미할당)

| Req | 비고 |
|-----|------|
| NFR-01 | `inch` 추가 시 기존 Converter 비수정 회귀 |
| EXT-01~03 | `units.json`, 동적 등록, `--format` |
