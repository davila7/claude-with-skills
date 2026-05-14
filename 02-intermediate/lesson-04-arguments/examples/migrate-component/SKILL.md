---
name: migrate-component
description: Migrate a UI component from one framework to another, preserving behavior and tests.
disable-model-invocation: true
argument-hint: [component-name] [from-framework] [to-framework]
---

## Migrate component

Migrate the $0 component from $1 to $2.

### Step 1: Read the current implementation

Find and read the current $0 component file. Search for it:
- In `src/components/`, `components/`, `app/components/`, or similar common locations
- Using `grep -r "$0" --include="*.$1*" -l` if the framework extension is known (e.g., `.vue`, `.jsx`)

Read all files that make up the component:
- The main component file
- Any associated style files (`.css`, `.scss`, `.module.css`)
- Any associated test files (`*.test.*`, `*.spec.*`)

If you cannot find the component, stop and ask the user for the file path.

### Step 2: Understand props, state, and behavior

Before writing any code, document:
- All props the component accepts (name, type, default value, whether required)
- All internal state (what it tracks and how it changes)
- All events the component emits or callbacks it invokes
- Side effects (data fetching, subscriptions, DOM manipulation)
- The rendered structure (what it produces visually or structurally)

This documentation becomes the specification the new implementation must satisfy.

### Step 3: Write the equivalent in $2

Write the $0 component in $2, matching the same public API:
- Same prop names and types
- Same event names and payloads
- Same rendered structure (or nearest equivalent in $2)
- Same behavior for all documented state transitions

Use idiomatic $2 patterns. Do not transliterate $1 patterns directly into $2 if $2 has a better way to express the same thing.

### Step 4: Update tests

Rewrite any tests associated with the original component to use $2 testing conventions:
- Update imports to point to the new component file
- Update any framework-specific test utilities (e.g., `mount` from $1 to the $2 equivalent)
- Preserve all test cases — every behavior tested in $1 must be tested in $2

### Step 5: Report what changed and what needs manual review

Produce a brief report:

**Changed:**
- List of files created or modified

**Preserved:**
- Confirmation that all props, events, and behaviors have equivalents

**Needs manual review:**
- Any behavior that could not be automatically preserved (e.g., a lifecycle hook that has no direct equivalent in $2)
- Any $1-specific third-party libraries used in the original that may not have $2 equivalents
- Performance characteristics that may differ between frameworks

Do not delete the original $1 component file. Leave that for the user to remove after verifying the migration.
