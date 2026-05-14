---
name: fix-issue
description: Fix a GitHub issue by number. Reads the issue, implements a fix, and prepares a commit.
disable-model-invocation: true
argument-hint: [issue-number]
allowed-tools: Bash(gh issue view *) Bash(gh issue list *) Read Grep Glob
---

## Fix GitHub issue

### Step 1: Read the issue

Run:
```
gh issue view $ARGUMENTS
```

If the issue does not exist or the `gh` CLI is not authenticated, stop and report the error. Do not proceed.

### Step 2: Understand the requirements

From the issue output, identify:
- The reported problem or requested feature
- Any reproduction steps or acceptance criteria mentioned in the issue body
- Labels that indicate the type of work (bug, enhancement, documentation, etc.)
- Any linked issues or pull requests that provide additional context

If the issue is unclear or underspecified, state the assumptions you are making before proceeding.

### Step 3: Find the relevant code

Search for code related to the issue:
- Use `grep -r` to find files referencing the relevant function, component, or error message
- Read the most relevant files to understand the current implementation
- Identify where the change should be made and why

### Step 4: Implement a minimal fix

Make the smallest change that correctly addresses the issue. Follow the existing code patterns in the affected file:
- Match the style, naming conventions, and error handling patterns already in use
- Do not refactor unrelated code
- Do not add features beyond what the issue describes

### Step 5: Write or update tests

If the codebase has tests:
- Add a test that fails before the fix and passes after
- Update any existing tests that are affected by the change
- Run the existing tests to confirm nothing is broken (use the test runner you find in `package.json` or the nearest test configuration file)

If you cannot determine the test runner, note that and ask the user.

### Step 6: Prepare a commit message

Stage the changes and write a commit message in this format:

```
fix: <short description matching the issue title>

Fixes #$ARGUMENTS
```

Do not commit automatically. Present the staged diff and the proposed commit message, then wait for the user to confirm or adjust before committing.
