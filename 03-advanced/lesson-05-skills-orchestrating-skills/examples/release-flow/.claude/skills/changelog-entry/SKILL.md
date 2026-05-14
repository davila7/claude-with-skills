---
name: changelog-entry
description: Draft the changelog entry for all unreleased commits in Keep a Changelog format. Groups commits into Added, Changed, Fixed, Removed, and Security. Use before releasing a new version or when updating CHANGELOG.md.
allowed-tools: Bash(git log *) Bash(git describe *) Bash(git tag *)
---

Draft a changelog entry for the current unreleased changes.

## Step 1: Find the last release tag

!`git describe --tags --abbrev=0 2>/dev/null || echo "none"`

If the output above is `none`, there are no previous tags — include all commits in the log.

## Step 2: Get the commits since the last tag

If a last tag was found:
```
git log <last-tag>..HEAD --oneline --no-merges
```

If no last tag was found:
```
git log --oneline --no-merges
```

## Step 3: Categorize the commits

Group the commits into Keep a Changelog sections using these rules:

- **Added**: new features, new commands, new files, new endpoints
- **Changed**: modifications to existing behavior, refactors, renames
- **Fixed**: bug fixes, error handling improvements, incorrect behavior corrected
- **Removed**: deleted features, removed flags, dropped support
- **Security**: vulnerability fixes, dependency updates addressing CVEs, auth changes

Skip merge commits, version bump commits (e.g., "Bump version to 1.2.0"), and commits that only touch lock files.

If a commit is ambiguous, prefer the more specific category. If it touches multiple areas, list it under the primary one.

## Step 4: Output the entry

Output only the markdown block, ready to paste into CHANGELOG.md under `## [Unreleased]`. Do not include any surrounding prose.

Format:

```markdown
## [Unreleased]

### Added
- Description of new feature (commit: abc1234)

### Changed
- Description of change (commit: def5678)

### Fixed
- Description of fix (commit: ghi9012)
```

Omit sections that have no entries. If there are no unreleased commits at all, output: `No unreleased commits since the last tag.`
