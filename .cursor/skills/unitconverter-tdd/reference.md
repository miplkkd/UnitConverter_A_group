# D-* 테스트 ID (Logic Track)

| ID | Layer | 파일(예) | 범위 |
|----|-------|----------|------|
| D-CONV-01 | entity | `tests/entity/test_d_conv_01.py` | meter → feet (README 3.28084) |
| D-CONV-02 | entity | `tests/entity/test_d_conv_02.py` | meter → yard (1.09361) |
| D-CONV-03 | entity | `tests/entity/test_d_conv_03.py` | feet → meter |
| D-CONV-04 | entity | `tests/entity/test_d_conv_04.py` | yard → meter |
| D-CONV-05 | entity | `tests/entity/test_d_conv_05.py` | 입력 단위→meter 기준 3단위 값 일관 |
| D-VAL-01 | control | `tests/control/test_d_val_01.py` | `:` 없음 판정 (E001 조건, emit 없음) |
| D-VAL-02 | control | `tests/control/test_d_val_02.py` | 숫자 아님 (E002 조건) |
| D-VAL-03 | control | `tests/control/test_d_val_03.py` | unknown unit (E003 조건) |
| D-VAL-04 | control | `tests/control/test_d_val_04.py` | 음수 (E004 조건) |
