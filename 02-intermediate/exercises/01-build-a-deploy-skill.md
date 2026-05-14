# Exercise 01: Build a Custom Deploy Skill

Build a deploy skill tailored to a project of your choice. This exercise puts together the fields covered in lessons 02, 03, 04, and 05 into a single working skill.

## Requirements

Your skill must:

1. Set `disable-model-invocation: true` — deploying should never happen automatically.
2. Include an `argument-hint` showing what argument the user should provide (typically an environment name: staging, production, etc.).
3. Set `allowed-tools` with only the commands your deploy workflow actually needs. Do not use `Bash(*)`.
4. Use at least one `` !`cmd` `` injection for a pre-flight check that runs before Claude does anything else.

## Choose your stack

Pick one of these or adapt to your own project:

### Node.js / npm
Pre-flight: `git status`, `git log --oneline -3`
Build: `npm run build`
Test: `npm test`
Publish: `git tag` + `git push`

### Python / pip
Pre-flight: `git status`, `git log --oneline -3`
Test: `pytest`
Build: `python -m build`
Publish: `git tag` + `git push`

### Docker
Pre-flight: `git status`, `docker info`
Build: `docker build`
Push: `docker push`
Deploy: `docker compose up -d` (or your orchestration tool)

### Static site (Netlify, Vercel, etc.)
Pre-flight: `git status`, `git log --oneline -3`
Build: `npm run build`
Deploy: `netlify deploy --prod` or `vercel --prod`

## Validation

After writing the skill, install it in your personal skills directory:

```bash
mkdir -p ~/.claude/skills/my-deploy
cp SKILL.md ~/.claude/skills/my-deploy/
```

Then open Claude Code in a project and test these two scenarios:

**Scenario A: Uncommitted changes**

1. Make an edit to any file without committing.
2. Invoke the skill: `/my-deploy staging`
3. Confirm the skill detects the uncommitted changes from the `` !`git status` `` output and aborts with a clear error message. It should not proceed to run tests or build.

**Scenario B: Clean working tree**

1. Commit all pending changes.
2. Invoke the skill: `/my-deploy staging`
3. Confirm the skill runs the full workflow in order.

## Checklist

- [ ] `disable-model-invocation: true` is set
- [ ] `argument-hint` is present
- [ ] `allowed-tools` lists specific commands, not `Bash(*)`
- [ ] At least one `` !`cmd` `` injection is in the body
- [ ] Scenario A: skill aborts on uncommitted changes
- [ ] Scenario B: skill runs the full workflow on a clean tree

## Solution

A worked solution for a Python project is in `solutions/01-deploy-skill/SKILL.md`. Read the exercise before looking at the solution.
