# KD Report — 템플릿 · 네이밍 · 예시

## 넘버링 규칙

| 폴더 | 패턴 | 예 |
|------|------|-----|
| `Report/` | `NN.<Project>_<Topic>_Report.md` | `02.UnitConverter_Session4_CursorDesign_Report.md` |
| `prompting/` | `NN.<Project>_<Topic>-Transcript.md` | `04.UnitConverter_Session4_CursorDesign-Transcript.md` |

- `NN` = 2자리 순번, 폴더 내 기존 최대값 + 1.
- Report ↔ Transcript **같은 세션 번호** 권장 (다르면 헤더에 상호 링크).

---

## Report template

```markdown
# <Project> — <세션 주제> 보고서 (NN)

> 작성 일시: YYYY-MM-DD  
> 선행: [01....md](01....md) · [../prompting/NN....md](../prompting/NN....md)  
> Transcript: [prompting/NN....md](../prompting/NN....md)

---

## 1. Executive Summary

<한 문장 주제. 이번 세션에서 한 일·미완·다음 단계 2~3문장.>

---

## 2. 산출물 목록

| 계층/유형 | 산출물 | 경로 | 상태 |
|-----------|--------|------|------|
| Report | … | `Report/…` | ✅ |
| Test | D-CONV-01 RED | `tests/entity/test_d_conv_01.py` | ✅ FAIL 확인 |
| Harness | entity 패키지 | `src/entity/` | ❌ |

---

## 3. 작업 상세

### 3.1 <주제 A>

| 항목 | 내용 |
|------|------|
| Phase | RED / GREEN / … |
| Test ID | D-CONV-01 (FR-02) |
| pytest | `python -m pytest …` → exit 1, ModuleNotFoundError |

---

## 4. Gap · 다음 세션 권장

| 우선순위 | 작업 | 근거 |
|----------|------|------|
| P0 | GREEN `convert_all` | D-CONV-01 RED 완료 |
| P1 | … | … |

---

## 5. 참조

- [docs/PRD.md](../docs/PRD.md)
- [README.md](../README.md)
- GitHub: `https://github.com/miplkkd/UnitConverter_A_group.git`

---

*End of Session NN report*
```

---

## Transcript template

```markdown
# <Project> — <세션 주제> Transcript

**보내기 일시:** YYYY-MM-DD  
**워크스페이스:** UnitConverter_Agroup  
**Session ID:** `<uuid>`  
**소스:** Cursor `agent-transcripts` JSONL  
**주제:** <한 줄>

**선행 세션 (본 export 제외):**

| # | Session ID | 파일 | 주제 |
|---|------------|------|------|
| … | … | `03....md` | … |

**제외 (페르소나 오류·병렬):**

| Session ID | 사유 |
|------------|------|
| `…` | 마방진 페르소나 — UnitConverter 불일치 |

**대응 Report:** [Report/NN....md](../Report/NN....md)

---

## [User] <첫 요청 요약>

\`\`\`
<사용자 원문 (핵심만)>
\`\`\`

---

## [Assistant] <응답 요약>

<핵심 결정·산출물·pytest 결과>

_[Tool: Read `.cursorrules`]_

---

## [User] …

…

---

*End of transcript — Session NN*
```

### JSONL 파싱 요약

1. 각 줄 JSON → `role`, `message.content[]`.
2. `type: text`만 본문에 사용; `tool_use` / `tool_result`는 `_[Tool: Name]_`.
3. 연속 User 턴은 하나의 섹션으로 묶지 말고 턴마다 `## [User]` 유지.
4. 50줄 이상 assistant 응답은 표·목록으로 요약, 원문 핵심 인용만.

---

## Git · PR 예시 (본 레포)

| 항목 | 값 |
|------|-----|
| remote | `origin` → `https://github.com/miplkkd/UnitConverter_A_group.git` |
| base | `main` |
| feature | `red`, `spec`, … |
| PR 제목 예 | `Session 5: D-CONV-01 RED + kdreport skill` |

### PR body 예

```markdown
## Summary
- Add Report/03 Session5 RED report and prompting/05 transcript
- D-CONV-01 RED test (ModuleNotFoundError confirmed)

## Test plan
- [ ] Review Report and Transcript
- [ ] `python -m pytest tests/entity/test_d_conv_01.py -v` → FAIL (RED)
```

---

## 기존 파일 참고 (SSOT)

| # | Report | Transcript |
|---|--------|------------|
| 01 | `01.UnitConvert_ProblemDefinition_Report.md` | `02.transcript-export.md` (통합 1~2) |
| 02 | `02.UnitConverter_Session4_CursorDesign_Report.md` | `04.UnitConverter_Session4_CursorDesign-Transcript.md` |
| 03 | — | `03.UnitConverter_Session3_CursorRulesReview-Transcript.md` |

다음 신규 세션 권장 번호: **Report 03**, **prompting 05** (2026-06-05 기준).
