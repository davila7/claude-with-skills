---
name: release
description: Run the complete release workflow: changelog entry, version bump, git tag, and GitHub release. Invokes changelog-entry, tag-version, and publish in sequence. Use when releasing a new version of the project.
disable-model-invocation: true
argument-hint: [version|patch|minor|major]
allowed-tools: Bash(git tag *) Bash(git log *) Bash(git status) Bash(git describe *) Bash(npm version *) Bash(gh release *)
---

Run the complete release workflow for `$ARGUMENTS` (e.g., `1.2.0`, `patch`, `minor`, `major`).

If `$ARGUMENTS` is empty, stop and tell the user: "Provide a version or bump type — for example: `/release patch` or `/release 1.2.0`."

## Pre-flight

Check the current state before doing anything:

!`git status --short 2>&1`

!`git describe --tags --abbrev=0 2>/dev/null && echo "latest tag found" || echo "no tags yet"`

If the working tree is dirty (uncommitted changes shown above), stop and tell the user to commit or stash their changes before running the release workflow. A release must start from a clean state.

## Steps

1. Run `/changelog-entry` to generate the changelog entry for all commits since the last tag.

   Review the output carefully. Ask the user: "Does this changelog entry look accurate? Type 'yes' to continue or 'edit' to open CHANGELOG.md first."

   If the user says 'edit', open CHANGELOG.md and wait for them to confirm they are done editing before continuing.

2. Run `/tag-version $ARGUMENTS` to bump the version in package.json and create the annotated git tag.

   Confirm the tag was created by showing the output of `git describe --tags --abbrev=0`.

3. Run `/publish` to push the tag to origin and create the GitHub release.

4. Report the release URL returned by `/publish`. Tell the user the release is complete.

If any step fails, stop immediately and report which step failed and what the error was. Do not attempt to continue after a failure.
