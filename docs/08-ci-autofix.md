# Step 7: CI Auto-fix

테스트가 실패하면 Claude가 실패 로그를 읽고 코드를 고쳐 같은 브랜치에 커밋합니다. 그 커밋으로 CI가 다시 돌아 통과하는지 확인합니다.
워크플로: [`step7-ci-tests.yml`](../.github/workflows/step7-ci-tests.yml), [`step7-ci-autofix.yml`](../.github/workflows/step7-ci-autofix.yml) · 데모 코드: [`demo_app/`](../demo_app/)

---

## 1. 동작 방식

1. 브랜치에 푸시하면 `Step 7 - CI Tests`가 `demo_app`의 pytest를 실행합니다.
2. 실패하면 `workflow_run` 이벤트로 `Step 7 - CI Auto-fix`가 실행됩니다.
3. 실패한 job 로그(`gh run view --log-failed`)를 프롬프트에 넣고, Claude가 원인을 찾아 **코드만** 고칩니다. 테스트 파일은 수정하지 않습니다.
4. Claude가 pytest로 확인한 뒤 커밋·푸시하면 CI가 다시 실행됩니다.

실측: 한 줄짜리 버그를 고치고 CI를 다시 통과시키기까지 약 2분, $0.05.

## 2. 실습

```bash
git switch -c ci-demo
sed -i '' 's|sum(values) / len(values)|sum(values) / (len(values) - 1)|' demo_app/calc.py   # macOS
git commit -am "break average" && git push -u origin ci-demo
```

Actions 탭에서 `Step 7 - CI Tests` 실패 → `Step 7 - CI Auto-fix` 실행 → Claude 커밋 → `Step 7 - CI Tests` 통과 순서를 확인하세요.

## 3. 무한 반복을 막는 장치

Claude의 푸시가 CI를 다시 실행하므로, 고치지 못하는 경우 실패와 수정이 계속 반복될 수 있습니다. 워크플로에는 다음 장치가 들어 있습니다.

| 장치 | 하는 일 |
|---|---|
| job `if:` | CI가 실패했고, 이벤트가 push이고, 기본 브랜치가 아니고, 같은 레포의 브랜치일 때만 실행합니다. 통과한 CI에는 runner도 쓰지 않습니다 |
| 시도 횟수 상한 | 수정 커밋마다 `Autofix-Attempt: N` 줄을 넣고, 브랜치에 그런 커밋이 `MAX_ATTEMPTS`(2)개 있으면 멈춥니다 |
| 브랜치 변경 확인 | 실패 이후 사람이 브랜치에 새로 푸시했으면 실행하지 않습니다 |
| `concurrency` | 브랜치당 한 번에 하나만 실행합니다 |
| 테스트 수정 금지 | `settings`의 deny 규칙으로 테스트 파일 편집을 막고, 사후 검사에서 테스트 파일이 바뀌었으면 job을 실패시킵니다 |

시도 횟수는 `git log --grep='^Autofix-Attempt:'`로 셉니다. git trailer로 세면 0이 나옵니다. 액션이 커밋 메시지 끝에 `Co-Authored-By` 문단을 따로 붙여서 trailer로 인식되지 않기 때문입니다.

## 4. 주의

- `workflow_run` 워크플로는 기본 브랜치(main)에 있어야 실행됩니다.
- 테스트 자체가 틀린 경우, Claude는 테스트를 고치지 않고 커밋 없이 이유를 설명했습니다. 이때 job은 경고만 남기고 통과하므로 Actions 요약에서 확인하세요.
- 기본 브랜치에는 자동 수정 커밋을 올리지 않습니다.
