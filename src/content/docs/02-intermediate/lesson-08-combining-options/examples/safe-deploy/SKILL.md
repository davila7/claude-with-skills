---
title: "safe-deploy"
name: safe-deploy
description: Deploy to a target environment after running pre-flight checks. Only invoke manually.
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash(npm test) Bash(npm run build) Bash(git status) Bash(git log *) Bash(git push *) Bash(git tag *)
---

## Pre-flight checks

!`git status --short`

!`git log --oneline -5`

---

Deploy to: $ARGUMENTS

If `$ARGUMENTS` is empty, stop immediately. Report: "No environment specified. Invoke as: /safe-deploy <environment> (e.g., /safe-deploy staging or /safe-deploy production)."

### Step 1: Abort if there are uncommitted changes

Check the git status output above. If it shows any modified, untracked, or staged files, stop here.

Report: "Deploy aborted: the working tree has uncommitted changes. Commit or stash them before deploying to $ARGUMENTS."

Do not proceed past this step if there are uncommitted changes.

### Step 2: Run the test suite

Run:
```
npm test
```

If any test fails, stop here. Report the failing test names and do not proceed.

### Step 3: Build the project

Run:
```
npm run build
```

If the build fails, report the full error output and stop. Do not proceed.

### Step 4: Create a deployment tag

Construct a tag name:
```
deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
```

Use the current UTC date and time. For example, a production deploy on 2026-05-13 at 14:32:07 UTC produces: `deploy-production-20260513-143207`.

Run:
```
git tag deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
```

### Step 5: Push the tag

Run:
```
git push origin deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
```

If the push fails, report the error. Do not retry automatically.

### Step 6: Report success

Print a final summary:

```
Deploy initiated.
Environment: $ARGUMENTS
Tag: deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
Commit: <git rev-parse HEAD output>
Time: <YYYY-MM-DD HH:MM:SS UTC>
```

If any step failed, do not print this summary. The failure report for the failing step is the final output.
