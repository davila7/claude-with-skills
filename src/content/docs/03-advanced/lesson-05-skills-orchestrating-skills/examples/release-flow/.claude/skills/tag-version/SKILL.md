---
title: "tag-version"
name: tag-version
description: Bump the package version and create an annotated git tag. Accepts a semantic version number (1.2.0) or a bump type (patch, minor, major). Does not push — use the publish skill to push. Use as part of a release workflow.
disable-model-invocation: true
argument-hint: [version|patch|minor|major]
allowed-tools: Bash(npm version *) Bash(git tag *) Bash(git log *) Bash(cat package.json)
---

Bump the version and create an annotated git tag for `$ARGUMENTS`.

If `$ARGUMENTS` is empty, stop and tell the user: "Provide a version or bump type — for example: `/tag-version patch` or `/tag-version 1.2.0`."

## Step 1: Determine the new version

Inspect the current version:
!`cat package.json 2>/dev/null | grep '"version"' | head -1 || echo "no package.json found"`

If `$ARGUMENTS` is a semantic version string matching the pattern `X.Y.Z` (e.g., `1.2.0`, `0.9.1`), use it directly as the new version.

If `$ARGUMENTS` is `patch`, `minor`, or `major`, run:
```
npm version $ARGUMENTS --no-git-tag-version
```
This updates package.json without creating a git tag. Read the new version from package.json after the command runs:
```
cat package.json | grep '"version"'
```

## Step 2: Stage the version bump

If `npm version` was used to update package.json, stage the change:
```
git add package.json package-lock.json
git commit -m "Bump version to v$VERSION"
```

If the version was provided as a literal semver string, update package.json manually: edit the `"version"` field to the new value, then stage and commit it.

## Step 3: Create the annotated tag

```
git tag -a v$VERSION -m "Release v$VERSION"
```

## Step 4: Confirm

Run `git describe --tags --abbrev=0` and show the output. Confirm: "Tag v$VERSION created. Run `/publish` to push it to origin and create the GitHub release."

Do not push. The publish skill handles pushing.
