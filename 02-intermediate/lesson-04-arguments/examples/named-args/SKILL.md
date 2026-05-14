---
name: branch-from-issue
description: Create a git branch named after a GitHub issue.
disable-model-invocation: true
argument-hint: [issue-number] [branch-prefix]
arguments: [issue, prefix]
allowed-tools: Bash(gh issue view *) Bash(git checkout *) Bash(git branch *)
---

## Create branch from GitHub issue

### Step 1: Read the issue title

Run:
```
gh issue view $issue
```

Extract the issue title from the output. If the issue does not exist or `gh` is not authenticated, stop and report the error.

### Step 2: Slugify the title

Convert the issue title to a branch-safe slug:
1. Convert to lowercase
2. Replace spaces and punctuation with hyphens
3. Remove any characters that are not letters, digits, or hyphens
4. Collapse consecutive hyphens into one
5. Strip leading and trailing hyphens
6. Truncate to 40 characters maximum (truncate at a word boundary if possible)

Examples:
- "Fix login page crash on mobile" → `fix-login-page-crash-on-mobile`
- "Add support for OAuth 2.0 / PKCE flow" → `add-support-for-oauth-20-pkce-flow`
- "Update README with installation instructions" → `update-readme-with-installation`

### Step 3: Determine the branch prefix

If `$prefix` is not empty, use it as provided.

If `$prefix` is empty, use `feature` as the default prefix.

Valid examples: `feature`, `fix`, `chore`, `hotfix`. Accept any non-empty string the user provides.

### Step 4: Create the branch

Construct the full branch name: `$prefix/$issue-<slug>`

For example, if `$prefix` is `fix`, `$issue` is `142`, and the slug is `login-page-crash-on-mobile`:
```
fix/142-login-page-crash-on-mobile
```

Run:
```
git checkout -b $prefix/$issue-<slug>
```

If the branch already exists, report the conflict and stop. Do not force-create or checkout the existing branch automatically.

### Step 5: Confirm

Report the new branch name and confirm the current branch has switched:
```
git branch --show-current
```

Example output:
```
Created and switched to: fix/142-login-page-crash-on-mobile
```
