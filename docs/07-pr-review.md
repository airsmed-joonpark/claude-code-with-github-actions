# Step 6: PR Auto Review

PR이 열리거나 새 커밋이 푸시되면 Claude가 코드 리뷰를 합니다.
워크플로: [`.github/workflows/step6-pr-review.yml`](../.github/workflows/step6-pr-review.yml)

---

## 1. 동작 방식

- 버그가 있는 줄에 인라인 댓글을 답니다. 고칠 코드가 짧으면 ```` ```suggestion ```` 블록으로 제안합니다.
- PR에는 요약 댓글 하나만 남기고, 새 커밋이 오면 그 댓글을 고쳐 씁니다(`use_sticky_comment`, `track_progress`).
- 다시 리뷰할 때는 이미 고친 문제를 다시 지적하지 않고, 요약 표에 resolved로 표시합니다.
- 같은 PR에 커밋이 연달아 오면 앞 리뷰를 취소합니다(`concurrency`, `cancel-in-progress: true`).

실측: 일부러 넣은 버그 3개(off-by-one, None 처리 누락, SQL 문자열 연결)를 모두 정확한 줄에서 지적했습니다. 리뷰 1회 약 $0.08, 25초.

## 2. 실습

```bash
git switch -c review-demo
cat > review_demo.py <<'PY'
def last_n(items, n):
    return [items[i] for i in range(len(items) - n, len(items) + 1)]

def find_user(cursor, name):
    cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")
    return cursor.fetchone()
PY
git add review_demo.py && git commit -m "add review demo" && git push -u origin review-demo
gh pr create --fill
```

리뷰가 달리면 버그 하나를 고쳐 다시 푸시하고, 요약 댓글이 어떻게 바뀌는지 확인하세요.

## 3. 설정 설명

| 설정 | 하는 일 |
|---|---|
| `track_progress: true` | PR 이벤트에서도 진행 상황 댓글을 쓰는 모드로 실행합니다. PR diff가 프롬프트에 자동으로 들어갑니다 |
| `use_sticky_comment: true` | 요약 댓글을 하나만 유지합니다. Claude GitHub App 토큰을 쓸 때만 동작합니다 |
| `mcp__github_inline_comment__create_inline_comment` | 인라인 댓글 도구. PR 이벤트에서 이 이름을 `--allowedTools`에 넣어야 설치됩니다 |
| `Pass confirmed: true` (프롬프트) | OAuth 토큰으로는 인라인 댓글 분류 기능(`classify_inline_comments`)이 동작하지 않습니다. 확인된 지적만 달도록 프롬프트에서 지정합니다 |
| `fetch-depth: 0` | 전체 히스토리를 받아 `git diff`로 비교할 수 있게 합니다 |

## 4. 주의

- 포크에서 온 PR에는 레포 Secret이 전달되지 않으므로 실행하지 않습니다.
- 공식 플러그인(`code-review@claude-plugins-official`)을 쓰려면 `/code-review:code-review`처럼 플러그인 이름을 붙여 부르세요. `/code-review`라고만 쓰면 Claude Code에 내장된 같은 이름의 명령이 실행됩니다.
