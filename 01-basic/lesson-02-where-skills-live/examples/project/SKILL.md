---
name: project-conventions
description: Lists the conventions for this project and demonstrates the project scope for Claude Code skills. Use when asked about project conventions, code style, or as a demonstration of project-scoped skills.
---

## Instructions

This skill is installed at the project scope. Its expected location on disk is:

```
.claude/skills/project-conventions/SKILL.md
```

(That path is relative to the root of the repository.)

Tell the user this is a demonstration of a project-scoped skill, then list the following made-up conventions to show how project-specific knowledge can be encoded in a skill:

### Example project conventions (demonstration only)

**Branching**
- Feature branches: `feat/<ticket-id>-short-description`
- Bugfix branches: `fix/<ticket-id>-short-description`
- All PRs must target `main`. Never merge directly to `main` locally.

**Commit messages**
- Conventional Commits format: `type(scope): description`
- Allowed types: feat, fix, docs, style, refactor, test, chore
- Reference the Linear ticket ID in the commit body when applicable

**Code style**
- TypeScript strict mode is enabled. Do not use `any` without a comment explaining why.
- All exported functions must have JSDoc comments.
- No `console.log` in production code — use the internal logger at `src/lib/logger.ts`.

**Testing**
- Unit tests live alongside source files: `foo.ts` / `foo.test.ts`
- Integration tests live in `tests/integration/`
- Minimum coverage threshold: 80% lines. CI will fail below this.

After listing the conventions, remind the user that this skill would normally contain real conventions for the actual project, committed to version control so that all developers on the team get the same guidance when working with Claude Code.
