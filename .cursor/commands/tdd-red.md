# TDD RED — 실패 테스트 먼저

UnitConverter_Agroup · Dual-Track TDD **RED 단계만**. 한 번에 **테스트 1개**. 상세 규칙: `.cursorrules` · D-* ID: `.cursor/skills/unitconverter-tdd/reference.md`

## 필수 선언

응답 **첫 줄**에 반드시 적는다:

```text
Phase: red | Layer: <entity|control|boundary> | Track: <Logic|UI>
```

| Track | Layer | 디렉터리 | 파일·ID |
|-------|-------|----------|---------|
| Logic | entity / control | `tests/entity`, `tests/control` | `test_d_*`, `D-*` |
| UI | boundary | `tests/boundary` | `test_u_*`, `U-*` |

## 절차

1. **ID 확인** — `reference.md`(Logic `D-*`) 또는 사용자 지정 `U-*`·Layer·`tests/<layer>/test_*` 경로 확정.
2. **AAA 테스트 작성** — `tests/`만 수정.
   - **Arrange** — 입력·기대값; 상수는 SSOT import(리터럴 산재 금지).
   - **Act** — 대상 함수/메서드 호출(미구현이면 import + `pytest.fail("RED: <ID> …")` 스켈레톤 허용).
   - **Assert** — 실패할 명확한 기대(완화·주석 처리 금지).
   - 함수 docstring·이름에 `D-*` 또는 `U-*` 포함.
3. **pytest FAIL** — 프로젝트 루트 cwd에서 대상 노드 1개 실행; **exit ≠ 0** 확인.
   - RED 수용: `ModuleNotFoundError` · `pytest.fail("RED: …")` · `AssertionError`(미구현).
4. **보고** — 아래 「보고」 섹션 형식으로 마무리. FAIL 없으면 GREEN으로 넘어가지 않음.

## pytest 예시 (bash)

```bash
# Logic — 단일 테스트 (entity 예)
python -m pytest tests/entity/test_d_conv_01.py::test_d_conv_01_meter_to_feet -v

# Logic — control 판정 예
python -m pytest tests/control/test_d_val_01.py::test_d_val_01_missing_colon -v

# Logic — 파일 전체 (RED 1개만 추가했을 때)
python -m pytest tests/entity/test_d_conv_01.py -v

# UI — boundary (I/O Mock만, control은 real)
python -m pytest tests/boundary/test_u_err_01.py::test_u_err_01_invalid_format -v
```

## 보고

| 항목 | 내용 |
|------|------|
| 테스트 ID | `D-*` 또는 `U-*` |
| FAIL 요약 | 실패 유형 1줄 (예: `ModuleNotFoundError`, `AssertionError: …`, `pytest.fail RED`) |
| 변경 파일 | **`tests/` 아래만** (경로 목록) |
| pytest | 실행한 명령 + exit code |

## 금지

- `src/` · `UnitConverter.py` **로직** 수정 (빈 `__init__.py`·import 경로용 스텁만 예외)
- Logic Track에서 entity/control **Domain Mock** · `@patch`
- assert 완화·주석 처리·삭제·`skip`·`xfail`로 FAIL 회피
- RED 미확인 상태에서 GREEN·구현 착수
- 신규 테스트를 `tests/test_convert.py`에만 추가 (Track 디렉터리 `test_d_*` / `test_u_*` 사용)
