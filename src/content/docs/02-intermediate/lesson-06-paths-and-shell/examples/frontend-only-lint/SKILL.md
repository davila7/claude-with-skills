---
title: "frontend-only-lint"
name: frontend-only-lint
description: Apply frontend code quality rules for React and TypeScript components. Auto-activates when editing component files.
paths:
  - "src/components/**"
  - "src/pages/**"
  - "src/hooks/**"
allowed-tools: Bash(npx eslint *) Bash(npx prettier *) Read
---

## Frontend code quality rules

These rules apply whenever you write or modify code in `src/components/`, `src/pages/`, or `src/hooks/`.

### Component rules

1. Components must be functional. Do not write class components. If you encounter an existing class component during a task, note it but do not refactor it unless the task specifically asks for that.

2. Hooks must follow the `use` prefix convention. A function that calls other hooks must start with `use`. A function that does not call hooks must not start with `use`.

3. The props interface must be defined directly above the component function, not inside it and not in a separate file. Name it `<ComponentName>Props`:
   ```typescript
   interface ButtonProps {
     label: string;
     onClick: () => void;
     disabled?: boolean;
   }
   
   export function Button({ label, onClick, disabled = false }: ButtonProps) {
   ```

4. No inline styles except for values that are computed at runtime and cannot be expressed as a static class. Use CSS modules, Tailwind, or the project's existing styling system for static styles.

5. Export components as named exports, not default exports:
   ```typescript
   // Correct
   export function Button() { ... }
   
   // Avoid
   export default function Button() { ... }
   ```

### After editing

After making changes to any component file, apply formatting and linting:

Run prettier on the edited file:
```
npx prettier --write <edited-file>
```

Run eslint on the edited file:
```
npx eslint <edited-file>
```

If eslint reports errors that `--fix` can safely resolve, run:
```
npx eslint --fix <edited-file>
```

Report any remaining eslint errors that require manual attention. Do not hide them or continue without noting them.

If npx, eslint, or prettier is not installed or not configured in this project, skip the tool and note its absence. Do not fail the task because of a missing linter.
