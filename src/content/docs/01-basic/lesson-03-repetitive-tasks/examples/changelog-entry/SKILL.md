---
title: "changelog-entry"
name: changelog-entry
description: Draft a CHANGELOG.md entry for the current changes in Keep a Changelog format. Use when releasing, tagging a version, or updating CHANGELOG.md.
allowed-tools: Bash(git log *) Bash(git diff *)
---

## Instructions

1. Find the most recent git tag:

   ```
   git describe --tags --abbrev=0
   ```

   If a tag exists, list commits since that tag:

   ```
   git log --oneline --no-merges <last-tag>..HEAD
   ```

   If no tag exists (the repository has no releases yet), list all commits:

   ```
   git log --oneline --no-merges
   ```

2. Read each commit subject line and classify it into one of the Keep a Changelog sections:

   - **Added** — new features, new files, new API endpoints, new configuration options
   - **Changed** — changes to existing behavior, updated dependencies, modified defaults
   - **Fixed** — bug fixes, corrected behavior, resolved errors
   - **Removed** — deleted features, removed files, dropped API endpoints
   - **Deprecated** — features that still work but are marked for future removal
   - **Security** — vulnerability patches, authentication improvements, permission changes

   Ignore merge commits, version bump commits, and changelog update commits. Ignore commits whose subject line is obviously tooling noise (dependency lock file updates with no semantic change, CI config tweaks that do not affect users).

3. Write the entry in Keep a Changelog format:

   ```markdown
   ## [Unreleased]

   ### Added
   - Description of added thing

   ### Changed
   - Description of change

   ### Fixed
   - Description of fix
   ```

   Omit sections that have no entries.

   Write each bullet in present tense, starting with a verb: "Add", "Fix", "Remove", "Update". Do not start bullets with the commit type prefix (feat:, fix:, etc.) — strip those and rephrase.

4. Output only the new CHANGELOG block. Do not output any surrounding explanation.
