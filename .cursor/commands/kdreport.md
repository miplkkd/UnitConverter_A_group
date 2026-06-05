# KD Report — Report · Transcript · GitHub PR

세션 산출물 정리: **Report** 작성 → **prompting** Transcript export → **commit·push** → **PR**. Skill: `.cursor/skills/kdreport/SKILL.md`

## 필수 선언

응답 **첫 줄**:

```text
Phase: kdreport | Layer: — | Track: —
```

## 절차 (Skill 위임)

1. **넘버링** — `Report/`, `prompting/` 기존 `NN.` 확인 → 다음 번호.
2. **Report** — `Report/NN.<Project>_<Topic>_Report.md` ([reference.md](../skills/kdreport/reference.md) 템플릿).
3. **Transcript** — 현재 세션 `agent-transcripts/*.jsonl` → `prompting/NN.<Project>_<Topic>-Transcript.md`.
4. **Git** — `git status`·`diff`·`log` 확인 → add → commit → `git push -u origin HEAD`.
5. **PR** — `gh pr create` (base `main`) → **PR URL** 보고.

## 사용자 입력 (선택)

| 인자 | 기본값 |
|------|--------|
| 세션 주제 | 대화 맥락에서 추론 (예: `Session5_D-CONV-01_RED`) |
| PR base | `main` |
| 제외 Session ID | 페르소나 오류·병렬 탭 (Transcript 헤더 표) |

## 완료 보고

Report 경로 · Transcript 경로 · commit hash · push 여부 · **PR URL**.

## 금지

- Report/Transcript 생략 후 push만
- Transcript tool raw dump · credential 포함
- `git config` 변경 · force push
