---
title: "on-edit-formatter"
name: on-edit-formatter
description: Apply code formatting rules after file edits in the source directory. Use when asked to format code or after making changes to source files.
paths:
  - "src/**"
  - "lib/**"
allowed-tools: Bash(npx prettier --write *) Bash(npx eslint --fix *)
user-invocable: false
---

## Post-edit formatting

After making any file edit in `src/` or `lib/`, apply formatting automatically. This skill runs as background context — Claude applies these rules after edits without the user needing to ask.

### Step 1: Run prettier on the edited file

Run:
```
npx prettier --write <path-to-edited-file>
```

Replace `<path-to-edited-file>` with the actual path of the file that was just edited.

If prettier modifies the file, note what changed (e.g., "Reformatted 3 lines in src/auth/login.ts").

If prettier is not installed or not configured (no `.prettierrc`, `prettier.config.js`, or `prettier` key in `package.json`), skip this step and note: "prettier not configured in this project."

### Step 2: Run eslint --fix on the edited file

Run:
```
npx eslint --fix <path-to-edited-file>
```

Replace `<path-to-edited-file>` with the same path.

If eslint --fix makes changes, note what was fixed.

If eslint reports errors that --fix cannot resolve automatically, list them clearly so the user is aware. Do not hide linting errors.

If eslint is not installed or not configured (no `.eslintrc*`, `eslint.config.*`, or `eslintConfig` key in `package.json`), skip this step and note: "eslint not configured in this project."

### Step 3: Report

Summarize what was done:
- Which file was formatted
- What prettier changed (or that it made no changes)
- What eslint fixed (or that it made no changes)
- Any remaining eslint errors requiring manual attention

If neither tool is installed, report that and do not treat it as an error. The task proceeds normally.
