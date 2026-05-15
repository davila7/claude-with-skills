---
title: "publish"
name: publish
description: Push the current branch and all tags to origin, then create a GitHub release using the latest tag and its CHANGELOG.md entry. Use after tag-version to complete a release.
disable-model-invocation: true
allowed-tools: Bash(git push *) Bash(git describe *) Bash(git tag *) Bash(gh release *) Read
---

Push the current branch and tags to origin, then create the GitHub release.

## Pre-flight

Check that a tag exists to publish:
!`git describe --tags --abbrev=0 2>/dev/null || echo "no tags found"`

If "no tags found" is shown above, stop and tell the user: "No tags found. Run `/release-plugin:tag-version` first to create a tag before publishing."

## Step 1: Push the current branch

```
git push origin HEAD
```

If this fails, report the error. Common causes: no remote configured, no upstream branch set. Do not continue if push fails.

## Step 2: Push all tags

```
git push origin --tags
```

## Step 3: Get the latest tag

```
git describe --tags --abbrev=0
```

Store this value as `$TAG` for the next steps.

## Step 4: Extract the changelog entry

Read CHANGELOG.md if it exists. Find the section for `$TAG` — look for a heading matching `## [$TAG]` or `## [v$TAG]` (versions may or may not include the `v` prefix in the changelog). Extract the text between that heading and the next `## [` heading. This is the release notes body.

If CHANGELOG.md does not exist or the version section is not found, use the git log since the previous tag as release notes:
```
git log $(git describe --tags --abbrev=0 $TAG^)..HEAD --oneline --no-merges
```

## Step 5: Create the GitHub release

```
gh release create "$TAG" --title "Release $TAG" --notes "$CHANGELOG_CONTENT"
```

## Step 6: Report the result

Print the release URL returned by `gh release create`. Tell the user: "Release $TAG is live at [URL]."
