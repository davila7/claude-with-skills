---
title: "summarize-changes"
name: summarize-changes
description: Summarizes uncommitted git changes and flags anything risky. Use when the user asks what changed, wants a commit message draft, or asks to review their diff before committing.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullet points. Focus on the logical intent of the changes, not the line-by-line diff.

Then list any risks you observe, such as:

- Missing error handling on new code paths
- Hardcoded values (API URLs, credentials, magic numbers) that should be configuration
- Removed tests or disabled assertions
- Changes to public API signatures or exported interfaces
- Large refactors mixed with behavior changes (should be separate commits)

If the diff is empty, say there are no uncommitted changes.

---

Note for learners: the `!` backtick line above is dynamic context injection. When Claude Code activates this skill, it runs `git diff HEAD` and replaces that line with the real diff output before Claude reads the file. The result is that Claude sees the actual diff as part of the skill body, without needing a separate tool call. This is the canonical example from the Claude Code skills documentation.
