---
title: "dependency-audit"
name: dependency-audit
description: Audit npm or pip dependencies for outdated packages and known vulnerabilities. Use when checking package health, preparing for a release, reviewing dependencies before merging a PR, or when asked about outdated packages or security advisories.
when_to_use: Also use when the user mentions CVEs, npm audit output, pip check, dependency rot, or wants to know if it is safe to upgrade a specific package.
argument-hint: [package-name or "all"]
allowed-tools: Bash(npm outdated) Bash(npm audit) Bash(npm list *) Bash(pip list *) Bash(pip-audit) Bash(pip show *) Read
---

## Dependency audit

Run a dependency health check for the current project. If a specific package name was provided as an argument, focus the audit on that package. Otherwise audit all dependencies.

### Step 1: Detect the package manager

Check whether this is a Node.js or Python project:
- If `package.json` exists in the working directory, use npm.
- If `requirements.txt`, `pyproject.toml`, or `setup.py` exists, use pip.
- If both exist, audit both.

### Step 2: Check for outdated packages

For npm:
```
npm outdated
```

For pip:
```
pip list --outdated
```

If `$ARGUMENTS` is a specific package name, filter the output to that package. If `$ARGUMENTS` is empty or "all", show the full list.

### Step 3: Check for known vulnerabilities

For npm:
```
npm audit
```

For pip (if pip-audit is available):
```
pip-audit
```

If pip-audit is not installed, note its absence and recommend installing it: `pip install pip-audit`.

### Step 4: Summarize findings

Present a concise report:

1. Total outdated packages (current version vs latest version for the top 10 most outdated)
2. Any vulnerabilities found: severity level, affected package, advisory ID
3. Recommended actions in priority order: fix critical vulnerabilities first, then high, then update packages with breaking changes separately from patch updates
4. If `$ARGUMENTS` names a specific package: show its current version, latest version, changelog link if available from `npm info <package> homepage` or `pip show <package>`, and whether any known vulnerabilities affect this specific package

### Notes

- Do not modify `package.json`, `requirements.txt`, or any lock file. This skill audits only; it does not upgrade.
- If the project has no dependencies file at all, report that and stop.
