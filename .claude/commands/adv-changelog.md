---
description: Print a one-line-per-commit changelog for the last N commits (default 5)
argument-hint: "[number of commits]"
allowed-tools: Bash(git log:*)
---

ADV-CHANGELOG-COMMAND-EXPANDED

Show a changelog for the last N commits. Arguments given: "$ARGUMENTS" (if empty, use 5).

Run `git log -n <N> --pretty=format:'%h %ad %s' --date=short` and print the result as a markdown list
under the heading `## ADV Changelog`. Each line: `- <date> <short sha> <subject>`.
Finish with a line `changelog-source: /adv-changelog`.
