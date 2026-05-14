# Exercise 01: Build Your First Skill

## Goal

Create a skill named `explain-code` that asks Claude to explain a piece of code in plain language, as if talking to someone who does not know the programming language.

## Requirements

Your skill must:

1. Have a valid `name` field: `explain-code` (lowercase, hyphens only, matches the directory name)
2. Have a `description` field that includes at least two or three trigger keywords so Claude auto-invokes it reliably
3. Have a body with clear steps telling Claude what to do

## What to put in the body

Think through what Claude needs to do this well:

- **What code?** Claude needs to know which code to explain. The body should tell Claude to read the file or code currently being discussed, or the last file mentioned in the conversation.
- **For what audience?** The skill is for someone unfamiliar with the language. The body should say that explicitly.
- **What depth?** The body should specify: overall purpose, main data flow, any non-obvious logic. It should also say what to skip — do not over-explain parts that are obvious from naming.

## Hints

- The description drives auto-invocation. A user typing "explain this code to me" or "walk me through this" should trigger the skill. Include those phrases as guidance in the description.
- The body should guide Claude to check what language the code is written in — the explanation style differs between a bash script and a React component.
- Use an analogy only if it genuinely helps. Do not force one.

## Validation

1. Create the skill file at: `~/.claude/skills/explain-code/SKILL.md`
2. Open Claude Code in any project that has code you want to understand
3. Test auto-invocation: type "explain this code to me" or "walk me through this function" and check that the skill activates
4. Test direct invocation: type `/explain-code` and verify it works
5. Check the output quality: is it in plain language? Does it cover the three required areas (purpose, data flow, non-obvious logic)?

## Solution

A reference solution is in `solutions/01-explain-code/SKILL.md`. Try writing your own version first — there is no single correct answer, and your description keywords should reflect how you naturally ask for explanations.
