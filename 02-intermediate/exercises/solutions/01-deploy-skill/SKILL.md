---
name: python-deploy
description: Deploy a Python project to the target environment. Runs pytest, builds the wheel, and pushes a deployment tag. Only invoke manually when ready to deploy.
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash(python *) Bash(pip *) Bash(git status) Bash(git log *) Bash(git tag *) Bash(git push *)
---

## Pre-flight checks

!`git status --short`

!`git log --oneline -5`

---

Deploy to: $ARGUMENTS

If `$ARGUMENTS` is empty, stop immediately. Report: "No environment specified. Invoke as: /python-deploy <environment> (e.g., /python-deploy staging or /python-deploy production)."

### Step 1: Abort if there are uncommitted changes

Check the git status output above. If it shows any lines (modified, untracked, staged, or deleted files), stop here.

Report: "Deploy aborted: there are uncommitted changes. Commit or stash them before deploying to $ARGUMENTS."

A clean working tree shows no output from `git status --short`. Do not proceed unless the output is empty.

### Step 2: Run the test suite

Run:
```
python -m pytest
```

If any tests fail, report the failing test names and count, then stop. Do not proceed.

If pytest is not installed, try:
```
python -m unittest discover
```

If neither is available, report that no test runner was found and stop. Do not deploy without running tests.

### Step 3: Build the distribution package

Run:
```
python -m build
```

This requires the `build` package. If it is not installed, run:
```
pip install build
```

Then retry `python -m build`.

If the build fails, report the error output and stop.

On success, confirm the output: the `dist/` directory should contain a `.whl` and a `.tar.gz` file.

### Step 4: Create a deployment tag

Construct the tag name:
```
deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
```

Use current UTC date and time. Example: `deploy-staging-20260513-143207`.

Run:
```
git tag deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
```

### Step 5: Push the tag

Run:
```
git push origin deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
```

If the push fails, report the error and stop.

### Step 6: Report success

Print a final summary:

```
Deploy initiated.
Environment: $ARGUMENTS
Tag: deploy-$ARGUMENTS-<YYYYMMDD>-<HHMMSS>
Time: <YYYY-MM-DD HH:MM:SS UTC>
Build artifacts: dist/
```
