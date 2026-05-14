# Exercise 02: Restrict a Skill by Path

Create a skill that auto-activates only when the user is working with database migration files. This exercise focuses on the `paths` field and writing a skill body that enforces structural conventions.

## Goal

The skill should:

1. Auto-activate when the user opens, edits, or references a file matching:
   - `migrations/**` (any file under a migrations directory)
   - `*.sql` (any SQL file in the project root)
   - `db/migrate/**` (Rails-style migration directory)

2. Check migration file naming conventions:
   - Timestamp-prefixed format: `YYYYMMDDHHMMSS_description.sql` (e.g., `20260513143207_add_user_roles.sql`)
   - Sequential format: `NNNN_description.sql` (e.g., `0042_add_user_roles.sql`)
   - Report non-conforming names as a warning

3. Warn about potentially dangerous SQL operations:
   - `DROP TABLE` without a preceding check (like `DROP TABLE IF EXISTS`)
   - `DELETE` without a `WHERE` clause
   - `UPDATE` without a `WHERE` clause
   - `TRUNCATE` on any table
   - Column removal (`DROP COLUMN`) — flags for attention, not necessarily wrong

4. Look for a rollback or a comment marking the migration as irreversible.

## What to write

Create `SKILL.md` in a new directory. Think through:

- Which `paths` patterns cover all three migration directory conventions above?
- Should this be `user-invocable: false` or left as default?
- Does this skill need any `allowed-tools`?
- Should `disable-model-invocation` be set?

## Output format

The skill should produce a checklist:

```
Migration review: 20260513143207_add_user_roles.sql

[ ] Naming convention: PASS / FAIL: <reason>
[ ] Rollback present: YES / NO / MARKED IRREVERSIBLE
[ ] Dangerous operations: NONE / WARNING: <list each one with line number>
```

## Validation

1. Create a test migration file with at least one dangerous operation and a non-conforming name.
2. Open that file in Claude Code.
3. Confirm the skill activates automatically (without you typing `/skill-name`).
4. Confirm the output matches the expected checklist format.
5. Also confirm the skill does NOT activate when you open a regular TypeScript or Python file.

## Solution

A worked solution is in `solutions/02-migration-guard/SKILL.md`.
