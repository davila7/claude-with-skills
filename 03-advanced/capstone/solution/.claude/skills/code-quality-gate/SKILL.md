---
name: code-quality-gate
description: Run all code quality checks (security, complexity, test coverage) on the current PR and post a combined report as a GitHub PR comment. Use before merging a PR, during code review, or when asked to check code quality.
disable-model-invocation: true
allowed-tools: Bash(gh pr *)
---

Run the complete code quality gate for this PR.

## Pre-flight

Check whether an open PR exists:
!`gh pr view --json number,title,headRefName 2>/dev/null || echo "NO_PR"`

If the output above contains "NO_PR", note that no PR is open. Proceed with the scans anyway, but print the final report to the terminal instead of posting it as a comment.

## Steps

1. Run `/security-scan`. It will return findings in this format:
   ```
   SECURITY FINDINGS:
   - [severity] file:line — description
   ```
   Capture the full output.

2. Run `/complexity-check`. It will return findings in this format:
   ```
   COMPLEXITY FINDINGS:
   - file:line — description
   ```
   Capture the full output.

3. Run `/test-coverage-check`. It will return findings in this format:
   ```
   COVERAGE FINDINGS:
   - source-file — description
   ```
   Capture the full output.

4. Collect all three findings blocks.

5. If a PR is open, invoke `@quality-reporter` with this message:
   "Post a code quality report for this PR with the following findings. Format as a GitHub PR comment and post it.

   [paste the SECURITY FINDINGS block here]

   [paste the COMPLEXITY FINDINGS block here]

   [paste the COVERAGE FINDINGS block here]"

   Confirm the comment URL was returned and print it.

6. If no PR is open, format and print the report to the terminal using the same structure the quality-reporter would use.

## Summary line

After posting (or printing), output a summary:
"Code quality gate complete. Security: [count or 'clean'], Complexity: [count or 'clean'], Coverage: [count or 'clean']."
