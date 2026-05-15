---
title: "Lesson 02: Invocation Control"
---

Two frontmatter fields control who can invoke a skill and whether it appears in Claude's context at all. Getting this right is the difference between a skill that protects you from accidental deploys and one that silently informs Claude without cluttering the slash command menu.

## The invocation matrix

| Frontmatter | You can invoke | Claude can invoke | Loaded into context |
|---|---|---|---|
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description NOT in context, full skill loads when YOU invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when Claude invokes |

Read each row carefully. The behavior of the "Loaded into context" column is the most counterintuitive part.

When `disable-model-invocation: true` is set, Claude does not see the skill description at all at startup. This means Claude cannot decide to invoke the skill on its own — it does not know the skill exists until you invoke it directly with `/skill-name`. The full skill body then loads for that one invocation.

When `user-invocable: false` is set, the skill description is always in Claude's context (so Claude can auto-invoke it), but it does not appear in the `/` menu. The user cannot run `/skill-name` in an interactive session.

## When to use `disable-model-invocation: true`

Use this for any skill with side effects you do not want Claude triggering automatically:

- **Deploy skills**: You do not want Claude to decide to deploy because you said "ship it" in a message.
- **Send-message skills**: A Slack or email skill should not fire because you said "notify the team".
- **Destructive operations**: Anything that calls `rm`, drops a database, or pushes to a remote branch.
- **Billing operations**: Any skill that triggers paid actions in an external service.

The rule of thumb: if running this skill by accident would require effort to undo, set `disable-model-invocation: true`.

## When to use `user-invocable: false`

Use this for background knowledge that should silently shape Claude's behavior rather than being an action the user runs directly:

- **Team conventions**: "Here are our REST API naming conventions and response formats." Claude applies them when writing API code without the user needing to invoke anything.
- **Architecture context**: "This service owns the billing domain and talks to these three downstream services." Claude uses this when discussing architecture without the user managing a separate context file.
- **Legacy system notes**: "This module is deprecated. Do not add new functionality. If asked to extend it, suggest migrating to the new module instead." Claude applies this whenever it touches the legacy code.

The rule of thumb: if the skill is knowledge rather than an action, set `user-invocable: false`.

## The inaccessible skill mistake

**Never set both `disable-model-invocation: true` and `user-invocable: false` on the same skill.**

With both set:
- Claude cannot invoke it (description is not in context)
- You cannot invoke it (not in the `/` menu)

The skill becomes permanently inaccessible. It can only be run via `claude -p "/skill-name"` in headless mode, which is almost certainly not what you intended. If you want a headless-only skill, document that intent explicitly in the description.

## Examples

- `examples/manual-only-deploy/` — uses `disable-model-invocation: true` to protect a deploy workflow
- `examples/claude-only-context/` — uses `user-invocable: false` to provide background API conventions

## Next lesson

[Lesson 03: Allowed tools](../lesson-03-allowed-tools/)
