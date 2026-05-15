---
title: "manual-only-deploy"
name: manual-only-deploy
description: Deploy the application to production. Only invoke this manually when you are ready to deploy.
disable-model-invocation: true
allowed-tools: Bash(npm run build) Bash(npm test) Bash(git push *) Bash(git tag *) Bash(git status) Bash(cat *)
---

## Deploy workflow

This skill deploys the application. It runs a series of checks before touching anything remote. If any step fails, it stops immediately and reports the failure. It does not retry automatically.

### Step 1: Confirm no uncommitted changes

Run:
```
git status
```

If the output shows modified or untracked files, stop here. Report: "Deploy aborted: there are uncommitted changes. Commit or stash them before deploying." Do not proceed.

### Step 2: Run the test suite

Run:
```
npm test
```

If any test fails, stop here. Report which tests failed and do not proceed.

### Step 3: Build the project

Run:
```
npm run build
```

If the build fails, stop here. Report the error output and do not proceed.

### Step 4: Create a version tag

Read the current version from `package.json`:
```
cat package.json
```

Extract the `version` field. Create a git tag in the format `v<version>-<YYYYMMDD>`:
```
git tag v<version>-<YYYYMMDD>
```

For example, if the version is `2.3.1` and today is 2026-05-13, the tag is `v2.3.1-20260513`.

If a tag with that name already exists, append a counter: `v2.3.1-20260513-2`.

### Step 5: Push the tag

Run:
```
git push origin <tag-name>
```

If the push fails, report the error. Do not retry.

### Step 6: Report completion

Print a summary:
- Tag name
- Commit SHA the tag points to (`git rev-parse HEAD`)
- Timestamp

Example output:
```
Deploy complete.
Tag: v2.3.1-20260513
Commit: a1b2c3d4e5f6
Time: 2026-05-13 14:32:07 UTC
```
