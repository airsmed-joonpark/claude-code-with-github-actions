# Step 5: Issue Triage (구조화 출력)

새 이슈가 열리면 Claude가 이슈를 분류하고, 그 결과로 라벨과 댓글이 붙습니다.
워크플로: [`.github/workflows/step5-issue-triage.yml`](../.github/workflows/step5-issue-triage.yml)

---

## 1. 동작 방식

1. 쓰기 권한이 있는 사람(OWNER/MEMBER/COLLABORATOR)이 이슈를 엽니다.
2. Claude는 `--json-schema`로 정한 형식의 JSON만 돌려줍니다. 라벨을 붙이거나 댓글을 쓰는 도구는 주지 않습니다.
3. 다음 셸 단계가 JSON을 검사한 뒤 라벨(`type:*`, `priority:*`, `area:*`, `needs-more-info`)을 붙이고 댓글을 하나 남깁니다.

Claude는 판단만 하고, 실제 변경은 셸 단계가 합니다. Claude가 잘못 답해도 스키마의 enum 값 밖으로는 나갈 수 없습니다.

## 2. 실습

```bash
gh issue create --title "Step 3 실행 시 MCP 서버가 연결되지 않습니다" \
  --body "Run Claude Code with MCP 단계에서 chrome-devtools 가 failed 로 나옵니다. 재현: Actions 탭에서 Step 3 실행."
```

1~2분 뒤 이슈에 라벨과 분류 댓글이 붙습니다. 기능 요청, 막연한 질문으로도 하나씩 열어 분류 결과를 비교해 보세요.

## 3. 설정 설명

| 설정 | 하는 일 |
|---|---|
| `--json-schema '{...}'` | 답을 이 JSON 스키마로 강제합니다. 결과는 `steps.claude.outputs.structured_output`에 담깁니다 |
| `--tools Read,Glob,Grep` | 쓸 수 있는 도구를 이 셋으로 줄입니다. `--allowedTools`는 자동 승인 목록일 뿐 도구를 줄이지 않습니다 |
| `--setting-sources user` | 레포의 CLAUDE.md·`.claude/settings.json`을 읽지 않습니다. 다른 용도의 프로젝트 규칙이 분류 결과에 섞이지 않게 합니다 |
| `--max-turns 6 --max-budget-usd 0.50` | 비용 상한. 실측 비용은 이슈당 $0.01~0.08, 2턴입니다 |
| `RESULT: ${{ ...structured_output }}` (env) | 결과를 환경변수로 넘깁니다 |

## 4. 주의

- **`structured_output`을 run 스크립트 안에 `'${{ ... }}'`로 직접 넣지 마세요.** 이슈 본문에서 온 글자가 셸 명령으로 실행될 수 있습니다. 반드시 `env:`로 넘기고 `jq`로 읽습니다.
- 이슈 본문은 프롬프트로 들어가므로 public 레포에서는 Actions 로그에 그대로 찍힙니다.
- 외부인의 이슈는 실행하지 않습니다(author_association 조건). 외부인 이슈까지 분류하려면 `github_token`과 `allowed_non_write_users`를 써야 하는데, 누구나 토큰 사용량을 쓰게 되므로 private 레포나 사용량 상한과 함께 쓰세요.
