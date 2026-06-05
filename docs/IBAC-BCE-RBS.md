# IBAC · BCE · RBS — 개발 3축 가이드

> UnitConverter_Agroup 피드백 반영 · Agent는 `.cursor/rules/ibac-bce-rbs.mdc`(alwaysApply)로 자동 적용

---

## 한눈에

| 약어 | 한 줄 | 본 프로젝트 |
|------|--------|-------------|
| **BCE** | 유스케이스를 Boundary / Control / Entity 로 분리 | `src/boundary`, `src/control`, `src/entity` |
| **IBAC** | 입력→경계→응용→핵심 **처리 순서** (BCE의 흐름 이름) | `unit:value` → boundary → control → entity |
| **RBS** | RED → Green → Stabilize **TDD 루프** + 요구↔테스트 추적 | `/tdd-red`, GREEN, REFACTOR, PRD §4 |

**ECB vs BCE:** 같은 패턴. Ivar Jacobson **Entity–Control–Boundary**; Adam Bien 등은 **Boundary–Control–Entity(BCE)** 순으로 표기. 의존은 **바깥(Boundary) → Control → Entity(안)**.

---

## BCE (Boundary · Control · Entity)

### 역할

- **Boundary:** 사용자·CLI·포맷. 로직 최소, **에러 메시지 emit**(E001~E005).
- **Control:** 파싱·검증·유스케이스 조율. **판정만**, emit 없음.
- **Entity:** meter 기준 변환. stdlib + entity 내부만, **순수 함수**.

### 의존 규칙

```
boundary → control → entity
```

역방향·건너뛰기(boundary가 entity 직접 호출) 금지.

### SRP 매핑 (PRD NFR-02)

| SRP | BCE |
|-----|-----|
| Parser | Control |
| Converter / Registry | Entity |
| Printer | Boundary |

---

## IBAC (Input · Boundary · Application · Core)

BCE를 **한 요청이 지나는 단계**로 본 이름이다.

| 단계 | = BCE | 예 (meter:2.5) |
|------|-------|----------------|
| **I** Input & Infrastructure | (계약 + tests/) | 형식 `unit:value`, pytest 수집 |
| **B** Boundary | Boundary | stdin, 3줄 stdout |
| **A** Application | Control | parse → validate → entity 호출 |
| **C** Core | Entity | 2.5m → ft/yd 값 계산 |

실패 경로: **A**에서 E001~E004 **판정** → **B**에서 메시지 **emit**. **C**는 에러 문자열을 모른다.

---

## RBS (RED · Blue/Green · Stabilize)

### TDD

| 단계 | 활동 | 금지 |
|------|------|------|
| **R** RED | `D-*`/`U-*` 테스트 1개, pytest **FAIL** | `src/` 선행 수정, assert 완화 |
| **B** Blue/Green | 최소 코드, Track pytest **PASS** | 테스트 없는 기능 추가 |
| **S** Stabilize | REFACTOR, SSOT·ECB 정리 | assert·FR 계약 변경 |

### 요구 추적 (R과 함께)

- PRD **FR-01~06** ↔ [reference.md](../.cursor/skills/unitconverter-tdd/reference.md) **1:1**
- 새 FR 추가 시 `D-*` 또는 `U-*`를 **같이** 정의

---

## Cursor 아티팩트 매핑

| 3축 | Rule | Skill | Command | Hook |
|-----|------|-------|---------|------|
| BCE | `.cursorrules` ECB | SKILL ECB 절 | `/review-ecb` | — |
| IBAC | PRD §2 도메인 | Layer·Track 표 | — | Write→pytest 힌트 |
| RBS | TDD·Loop | RED/GREEN/REFACTOR | `/tdd-red` | postToolUse |

---

## 참고

- [PRD.md](PRD.md)
- [.cursorrules](../.cursorrules)
- [Report/02](../Report/02.UnitConverter_Session4_CursorDesign_Report.md)
