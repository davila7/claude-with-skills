---
title: "pr-summary"
name: pr-summary
description: Summarize the current pull request including diff, comments, and review status. Use when reviewing a PR, preparing for a review meeting, or getting a quick PR overview.
context: fork
agent: Explore
allowed-tools: Bash(gh pr *)
---

## Pull request info

!`gh pr view --json number,title,body,state,additions,deletions,changedFiles,reviews,statusCheckRollup`

## Changed files

!`gh pr diff --name-only`

## Recent comments

!`gh pr view --comments 2>/dev/null | tail -50`

---

Summarize this pull request:

### 1. What problem it solves

From the PR title and body, describe what this pull request is trying to accomplish. Be specific — do not just restate the title.

### 2. What changed

From the changed files list and the additions/deletions counts:
- How many files changed and roughly what areas of the codebase are affected
- Whether this is a focused change (one feature, one bug fix) or a broad change touching many areas
- Any files that stand out as high-risk or unexpected (e.g., changes to authentication, database migrations, public API files)

### 3. Unresolved comments or review concerns

From the comments section:
- List any reviewer comments that appear to be unresolved (no response or no "resolved" marker)
- Note any discussion threads that indicate disagreement or open questions

If there are no comments, say so.

### 4. Readiness to merge

Based on the review status and CI information from the JSON output:
- Number of approvals vs requested changes
- Whether required CI checks have passed, failed, or are still running
- A one-sentence assessment: ready to merge, blocked by reviews, or blocked by CI

Do not make a merge decision — only summarize the current state. The final merge decision belongs to the user.
