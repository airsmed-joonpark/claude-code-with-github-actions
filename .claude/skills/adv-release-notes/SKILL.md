---
name: adv-release-notes
description: Write release notes from recent git history in the fixed ADV-RN format. Use whenever the user asks for release notes, a release summary, or "what changed" over a range of commits.
allowed-tools: Bash(git log:*), Bash(git rev-parse:*)
---

# adv-release-notes

Produce release notes from `git log` in exactly this format. Do not add other sections.

1. Run `git log -n <N> --pretty=format:'%h|%an|%ad|%s' --date=short` (N = number of commits asked for, default 10).
2. Sort each commit into one bucket by its subject:
   - **Features**: subjects starting with `feat`, `Add`, `add`, `qa:`
   - **Fixes**: subjects starting with `fix`, `Fix`
   - **Chores**: everything else
3. Output this block and nothing else (keep empty buckets with `- (none)`):

```
## ADV-RN Release Notes (<N> commits, <oldest short sha>..<newest short sha>)

### Features
- <subject> (<short sha>, <date>)

### Fixes
- <subject> (<short sha>, <date>)

### Chores
- <subject> (<short sha>, <date>)

ADV-RN-FORMAT-v1
```

The literal marker line `ADV-RN-FORMAT-v1` must be the last line of the block.
