---
name: git-diff-summary
description: Analyze the current uncommitted diff and give a detailed summary with risk assessment. Use when asking what changed, reviewing changes before a commit, or requesting a change summary.
---

## Staged changes

!`git diff --staged --stat`

## Unstaged changes

!`git diff --stat`

## Full diff

!`git diff HEAD`

---

Summarize the changes above:

### 1. What was modified and why

For each changed file, describe what was modified. Infer the intent from the diff — do not just list the line counts. Group related changes together if multiple files are part of the same logical change.

### 2. Risk factors

Flag any of the following if present in the diff:

- Removed or weakened error handling (try/catch blocks deleted, error paths removed)
- Changed public interfaces (function signatures, exported types, API response shapes)
- Missing or removed tests for changed code
- Hardcoded values where there were previously constants or configuration references
- Security-sensitive areas touched (authentication, authorization, cryptography, input validation)
- Dependency version changes
- Database schema changes or data migrations

For each risk factor found, cite the specific file and line range.

### 3. Recommended next steps before committing

Based on the changes and any risk factors identified, give a prioritized list of things to do or verify before committing. Examples: "Run the test suite", "Add a test for the new error path in auth.ts:42", "Confirm the API response shape change is backward compatible".

If there are no risk factors and the changes are straightforward, say so clearly.
