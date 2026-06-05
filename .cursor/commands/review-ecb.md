# BCE · ECB · 계약 리뷰 (코드 수정 금지)

UnitConverter_Agroup · **BCE**(=ECB) · **읽기·리뷰만**. `src/`·`tests/`·`UnitConverter.py` **수정 금지**. 헌법: `.cursorrules` · 3축: `docs/IBAC-BCE-RBS.md`

## 필수 선언

응답 **첫 줄**:

```text
Phase: review | Layer: — | Track: —
```

## 절차

1. 범위 확인 — 사용자가 지정한 경로(없으면 `src/`, `tests/`, `UnitConverter.py` 전체 **읽기만**).
2. 아래 **체크표 5항**을 파일·심볼 단위로 검사.
3. 위반만 표로 보고; 위반 0건이면 「위반 없음」+ 잔여 리스크 1~3줄(선택).
4. 구현 제안·리팩터·테스트 추가는 **하지 않음** (별도 `/tdd-red` 등으로 분리).

## 체크표 (5항)

| # | 체크 | Pass 기준 | 위반 예 |
|---|------|-----------|---------|
| 1 | **import 방향** | `boundary → control → entity`만. `entity`→`control`/`boundary` **없음**. `control`→`boundary` **없음**. `boundary`→`entity` 직접 import·호출 **없음** | `entity`가 `control` import; `boundary`가 `entity.convert` 직접 호출 |
| 2 | **entity · E001~E005** | `entity`는 변환·순수 계산만. **E001~E005**를 raise/return/print/CLI 메시지로 **emit하지 않음**. E001~E004 **판정**도 `control` 담당 | `entity`에서 `:` 없음 시 에러 문자열; `entity`가 E005 출력 형식 검사 |
| 3 | **입출력 계약 · 3줄 SSOT** | 입력 `unit:value` (`:` 분리). 성공 시 **meter/feet/yard 3줄**·단위 표기·반올림이 **SSOT 한 곳**과 일치. README 비율 **3.28084 / 1.09361**, `feet`↔`yard`는 **meter 경유**만 | README와 다른 비율·3줄 아님·직접 ft↔yd 비율·하드코딩 메시지 산재 |
| 4 | **MagicConstant SSOT** | `3.28084`, `1.09361`, `meter`/`feet`/`yard`, E001~E005 키·메시지가 **단일 SSOT**에서만 정의; `src/`·`tests/`에 동일 리터럴 **중복 산재 없음** (테스트는 SSOT import) | entity·test에 `3.28084` 리터럴 반복; 오류 문구가 boundary·control에 각각 하드코딩 |
| 5 | **Logic Track · Domain Mock** | `tests/entity`, `tests/control`, `test_d_*`에 entity/control **`@patch`·Mock·Fake 도메인 대체 없음** | `test_d_conv_01`에서 `patch("entity.convert")` |

### E001~E005 emit 주체 (참고)

| 코드 | 의미 | 허용 emit |
|------|------|-----------|
| E001 | `:` 없음 | **boundary만** |
| E002 | 숫자 아님 | **boundary만** |
| E003 | unknown unit | **boundary만** |
| E004 | 음수 | **boundary만** |
| E005 | 출력 형식/계약 위반 | **boundary만** |
| E006~E007 | 예약 | 본 세션 범위 밖 |

`control`: E001~E004 **판정 결과**만 (bool/enum/예외 타입 등, **에러 코드 문자열 emit 금지**).

## 보고 형식 (표만)

### 요약

| 항목 | 값 |
|------|-----|
| 검사 범위 | (경로 목록) |
| 위반 건수 | N |
| 판정 | ✅ 위반 없음 / ⚠️ N건 |

### 위반 목록 (있을 때만)

| # | 체크 | 파일:줄(또는 심볼) | 위반 내용 | 심각도 |
|---|------|-------------------|-----------|--------|
| 1 | import 방향 | `…` | … | P0 / P1 |

(위반 없으면 이 표는 「—」 한 줄.)

## 금지

- 코드·테스트·설정 **수정**
- pytest 실행으로 green 맞추기 (리뷰 범위 밖)
- Golden Master·`tests/golden/*.approved.txt` **갱신**
- JSON/동적 단위/conftest/`pip install -e .` **도입 제안** (본 세션 범위 밖)
