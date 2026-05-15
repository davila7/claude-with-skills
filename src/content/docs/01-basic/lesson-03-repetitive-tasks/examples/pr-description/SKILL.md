---
title: "pr-description"
name: pr-description
description: Write a pull request description with summary, motivation, and test plan. Use when creating a PR, asked for a PR description, or preparing to submit a pull request.
allowed-tools: Bash(git log *) Bash(git diff *)
---

## Instructions

1. List the commits on this branch:

   ```
   git log --oneline main..HEAD
   ```

   If `main` does not exist, try `master`:

   ```
   git log --oneline master..HEAD
   ```

2. Get a summary of changed files:

   ```
   git diff main...HEAD --stat
   ```

   (Use `master...HEAD` if `main` does not exist.)

3. Write a PR description using the following structure. Output only the description, with no surrounding explanation.

---

## Summary

- What changed, as a bullet list. One bullet per logical change. Focus on the user-visible or caller-visible effect, not the implementation detail.

## Motivation

A short paragraph (two to four sentences) explaining the problem being solved. Why does this PR need to exist? What was wrong or missing before?

## Test plan

A checklist of specific steps a reviewer can follow to verify the change works:

- [ ] Step one
- [ ] Step two
- [ ] Edge case or error scenario to check

## Notes

Anything a reviewer should know that is not obvious from the diff: migrations that need to run, environment variables that need to be set, follow-up work that is intentionally deferred, known limitations.

If there are no reviewer notes, omit this section entirely.

---

Keep the description factual and concise. Do not pad with filler phrases. If the PR is straightforward, the description should be short.
