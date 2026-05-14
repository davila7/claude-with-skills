---
name: migration-guard
description: Review database migration files for naming conventions and dangerous operations. Auto-activates for migration files.
paths:
  - "migrations/**"
  - "*.sql"
  - "db/migrate/**"
---

## Migration review

Review the current migration file for naming conventions, rollback presence, and dangerous operations.

### Step 1: Identify the file being reviewed

Use the current file context to determine which migration file is being worked on. If the user specified a file path, use that. If the context is ambiguous, ask the user which file to review before proceeding.

### Step 2: Check the file name

Extract the file name (not the full path) and check it against two accepted naming formats:

**Format A — Timestamp prefix:**
Pattern: `YYYYMMDDHHMMSS_description.sql`
Example: `20260513143207_add_user_roles.sql`
- Year: 4 digits
- Month: 2 digits (01–12)
- Day: 2 digits (01–31)
- Hour: 2 digits (00–23)
- Minute: 2 digits (00–59)
- Second: 2 digits (00–59)
- Underscore separator
- Description: lowercase letters, digits, underscores
- Extension: `.sql`

**Format B — Sequential prefix:**
Pattern: `NNNN_description.sql`
Example: `0042_add_user_roles.sql`
- Number: 1 or more digits, typically zero-padded to 4 digits
- Underscore separator
- Description: lowercase letters, digits, underscores
- Extension: `.sql`

If the file name matches neither format, mark the naming check as FAIL and note the reason.

### Step 3: Check for rollback

Read the file content and look for either:

- A clearly labeled rollback section (a comment like `-- rollback`, `-- down`, `-- revert`, followed by SQL that undoes the migration)
- A comment explicitly marking it as irreversible (e.g., `-- This migration is irreversible`, `-- no rollback`)

If neither is present, mark rollback as NO.

### Step 4: Check for dangerous operations

Read the file and scan for these patterns (case-insensitive):

- `DROP TABLE` without `IF EXISTS` immediately following — flag as WARNING
- `DROP TABLE IF EXISTS` — acceptable, no warning
- `DELETE FROM` without a `WHERE` clause on the same or next line — flag as WARNING
- `UPDATE` without a `WHERE` clause on the same or next line — flag as WARNING
- `TRUNCATE` on any table — flag as WARNING (destructive, often irreversible in production)
- `DROP COLUMN` — flag as NOTICE (may break dependent code; not always dangerous but requires attention)

For each match, note the line number.

### Step 5: Output the checklist

Present findings in this format:

```
Migration review: <filename>

Naming convention: PASS
  - Format: timestamp-prefix / sequential-prefix
  
  (or)
  
Naming convention: FAIL
  - Reason: <specific reason>

Rollback: YES / NO / MARKED IRREVERSIBLE
  - <brief note on what the rollback does, or why it is marked irreversible>

Dangerous operations: NONE
  
  (or)
  
Dangerous operations:
  WARNING line 14: DELETE without WHERE clause
  WARNING line 22: TRUNCATE on orders table
  NOTICE  line 31: DROP COLUMN — confirm no dependent code references this column
```

Do not modify the migration file. This skill reviews only.
