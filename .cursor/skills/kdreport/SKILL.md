---
name: kdreport
description: >-
  세션 종료 시 Report 보고서·prompting Transcript export·GitHub push·PR 생성.
  /kdreport, kdreport, 보고서 생성, transcript export, 세션 보고, PR 생성 요청 시.
disable-model-invocation: true
---

# KD Report — Report · Transcript · GitHub PR

> 템플릿: [reference.md](reference.md) · 원격: `origin` → `https://github.com/miplkkd/UnitConverter_A_group.git`

## 필수 선언

응답 **첫 줄**:

```text
Phase: kdreport | Layer: — | Track: —
```

## 언제 실행

| 트리거 | 예 |
|--------|-----|
| `/kdreport` | 세션 마무리·산출물 정리 |
| 보고서 + transcript + GitHub | 「Report 쓰고 PR 올려줘」 |

**선행:** 이번 대화에서 완료한 작업·변경 파일·pytest 결과를 파악한 뒤 시작.

---

## 워크플로 (4단계)

```
1. Report 작성     → Report/NN.*_Report.md
2. Transcript export → prompting/NN.*-Transcript.md
3. Git commit·push → 현재 브랜치
4. PR 생성         → gh pr create (base: main)
```

진행 체크리스트를 응답에 표시하고 단계마다 완료 표시.

---

## 1. Report (`Report/`)

### 넘버링

1. `Report/` 기존 `NN.` 접두 파일 목록 확인.
2. 다음 번호 = **최대 NN + 1** (2자리: `01`, `02`, …).
3. 파일명: `Report/NN.<Project>_<SessionTopic>_Report.md`

예: `Report/03.UnitConverter_Session5_D-CONV-01_RED_Report.md`

### 본문 (필수 섹션)

| # | 섹션 | 내용 |
|---|------|------|
| 1 | Executive Summary | 한 문장 주제 + 이번 세션 성과·미완 |
| 2 | 산출물 목록 | 경로·상태 표 (✅/❌/⚠️) |
| 3 | 작업 상세 | Phase·Layer·Track·테스트 ID·pytest 결과 |
| 4 | Gap · 다음 권장 | P0/P1 우선순위 |
| 5 | 참조 | PRD, 선행 Report, Transcript 링크 |

상세 템플릿 → [reference.md § Report](reference.md#report-template)

**메타 헤더:** 작성 일시, 선행 Report/Transcript 상대 링크, 대응 Transcript 경로.

---

## 2. Transcript export (`prompting/`)

> 폴더명은 소문자 `prompting/` (레포 실제 경로).

### 소스

```
%USERPROFILE%\.cursor\projects\<workspace-slug>/agent-transcripts/<uuid>.jsonl
```

- **현재 세션** JSONL 우선 (대화에 `agent-transcripts` 경로가 있으면 사용).
- 없으면 `agent-transcripts/`에서 **최근 수정** `.jsonl` 또는 사용자 지정 UUID.

### 넘버링·파일명

- `prompting/` 기존 `NN.` 접두 확인 → 다음 번호.
- `prompting/NN.<Project>_<SessionTopic>-Transcript.md`

### 변환 규칙

| 규칙 | 처리 |
|------|------|
| User 메시지 | `## [User] <요약 제목>` + fenced 원문 |
| Assistant | `## [Assistant] <요약>` + 핵심 응답 (장문 요약 가능) |
| Tool 호출 | `_[Tool: Read path]_` 한 줄로 축약 (**전체 출력 생략**) |
| 이미지 | `_[Image: 설명]_` |
| 병렬·오류 세션 | 헤더 **제외 표**에 Session ID·사유 (마방진 등 페르소나 불일치) |
| 비밀 | `.env`, token, credential **미포함** |

상세 템플릿 → [reference.md § Transcript](reference.md#transcript-template)

Report 헤더에 Transcript 상대 링크; Transcript 헤더에 Report 역링크.

---

## 3. Git commit · push

사용자가 `/kdreport`를 호출했으면 **commit·push 허용** (명시 요청).

### 사전 점검 (병렬)

```bash
git status
git diff
git diff --staged
git log -5 --oneline
git branch -vv
```

### 커밋 범위

- 포함: `Report/`, `prompting/`, 이번 세션 코드·설정 변경.
- 제외: `.env`, credential, `venv/`, `.pytest_cache/`.

### 커밋 · push

```bash
git add Report/ prompting/ <기타 관련 경로>
git commit -m "$(cat <<'EOF'
<1~2문장: why 중심>

EOF
)"
git push -u origin HEAD
```

- `git config` 변경 금지.
- `--no-verify`, force push, `main` force push **금지**.

---

## 4. PR 생성 (`gh`)

### 사전 (병렬)

```bash
git status
git diff
git branch -vv
git log main..HEAD --oneline
git diff main...HEAD
```

### 생성

```bash
gh pr create --title "<제목>" --body "$(cat <<'EOF'
## Summary
- <bullet 1>
- <bullet 2>

## Test plan
- [ ] Report/NN.* 검토
- [ ] prompting/NN.* Transcript 검토
- [ ] (해당 시) pytest / Loop 결과

EOF
)"
```

- base 브랜치: **`main`** (다르면 사용자 확인).
- **PR URL**을 최종 응답에 반드시 포함.

`gh` 미설치·인증 실패 시: push까지 완료 보고 + 수동 PR 안내.

---

## 완료 보고 형식

| 항목 | 값 |
|------|-----|
| Report | `Report/NN....md` |
| Transcript | `prompting/NN....md` |
| Branch | `red` / `spec` / … |
| Commit | `<hash>` · 메시지 1줄 |
| Push | ✅ / ❌ |
| PR | URL 또는 수동 안내 |
| 제외 세션 | (있으면 UUID·사유) |

---

## 금지

- Report/Transcript 없이 push·PR만 수행
- Transcript에 tool raw output·비밀 전체 붙여넣기
- `git config` 수정 · `main` force push
- 사용자 `/kdreport` 없이 임의 commit/push

## 추가 자료

- [reference.md](reference.md) — Report·Transcript 템플릿·예시 파일명
