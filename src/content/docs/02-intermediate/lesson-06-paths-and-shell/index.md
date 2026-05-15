---
title: "Lesson 06: Paths and Shell"
---

Two fields control where and how a skill activates: `paths` restricts auto-activation to specific file contexts, and `shell` sets the interpreter used for dynamic context injection commands.

## The `paths` field

### What it does

When `paths` is set, the skill only auto-activates when the user is working with files that match one of the glob patterns. "Working with" means the file is open, being edited, or referenced in the current task.

```yaml
paths:
  - "src/components/**"
  - "src/pages/**"
```

A skill with this configuration will not auto-activate when the user is editing a migration file or a backend route. It only surfaces when the context involves component or page files.

### What it does NOT do

`paths` does not prevent you from invoking the skill directly. If you type `/frontend-only-lint` while editing a backend file, the skill runs. Path restrictions only affect auto-invocation — when Claude decides on its own to activate a skill based on its description.

### Why use it

Without path restrictions, a skill's description keywords might match contexts where the skill is not useful. A "check React component props" skill that activates during a Python debugging session is noise. `paths` makes auto-invocation precise.

### Glob pattern syntax

Patterns follow standard glob conventions:
- `*` — matches any characters within a single path segment
- `**` — matches any number of path segments (including zero)
- `?` — matches exactly one character
- `{a,b}` — matches either `a` or `b`

Examples:
- `"src/components/**"` — any file anywhere under `src/components/`
- `"**/*.sql"` — any `.sql` file in any directory
- `"migrations/**"` — any file under a `migrations/` directory at any depth
- `"**/*.{test,spec}.{ts,js}"` — any test file in TypeScript or JavaScript
- `"db/migrate/**"` — files under `db/migrate/` specifically

### Combining multiple patterns

List multiple patterns to cover related locations:

```yaml
paths:
  - "src/components/**"
  - "src/pages/**"
  - "src/hooks/**"
```

The skill auto-activates if the current file matches any of the listed patterns.

---

## The `shell` field

### What it does

`shell` sets the interpreter used to run dynamic context injection commands (the `` !`cmd` `` and `` ```! `` blocks in the skill body).

```yaml
shell: bash
```

```yaml
shell: powershell
```

### Default

`bash` is the default. On macOS and Linux, leave this field unset.

### When to set `shell: powershell`

On Windows, if your dynamic context injection commands use PowerShell syntax (for example, `$env:PATH`, `Get-ChildItem`, or `Select-Object`), set `shell: powershell`.

PowerShell injection also requires the environment variable `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` to be set. Without it, the field is accepted but may not take effect.

### Portability note

Skills that use `shell: powershell` do not run correctly on macOS or Linux. If you want a cross-platform skill, write injection commands in POSIX shell syntax and leave `shell` unset.

---

## Examples

- `examples/frontend-only-lint/` — uses `paths` to restrict auto-activation to frontend component files

## Next lesson

[Lesson 07: Model and effort](../lesson-07-model-and-effort/)
