# Lesson 08: Plugins and Distribution

When a set of skills is mature and useful to an entire team or the broader community, packaging it as a plugin makes distribution straightforward. A plugin bundles skills, agents, and other assets into a single directory with a manifest. Users install the whole package with one command.

---

## Plugin basics

A plugin is a directory containing:

- `plugin.json` — the manifest
- `skills/` — one subdirectory per skill, each with a `SKILL.md`
- `agents/` — one subdirectory per agent definition (optional)

The manifest declares what the plugin contains and identifies it by name and version.

**Skill invocation from a plugin:**
Skills in a plugin use a namespaced command: `/plugin-name:skill-name`

If the plugin is named `release-plugin` and contains a skill named `release`, users invoke it as:
```
/release-plugin:release
```

**Agent references from within plugin skills:**
Subagents defined in the plugin are referenced as `@agent-plugin-name:agent-name`.

---

## plugin.json structure

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin provides",
  "skills": [
    "skills/skill-one",
    "skills/skill-two"
  ],
  "agents": [
    "agents/my-agent"
  ]
}
```

- `name`: the plugin namespace. Must be lowercase with hyphens only. This becomes the prefix for all slash commands.
- `version`: semantic version string. Used for update checks and conflict resolution.
- `description`: shown when listing installed plugins.
- `skills`: list of relative paths to skill directories. Each path must contain a `SKILL.md`.
- `agents`: list of relative paths to agent definition files (optional).

---

## Distribution options

**Local installation:**
```bash
claude plugin add ./path/to/plugin-directory
```
Useful during development and for team-internal plugins stored in a shared repository.

**Git URL:**
```bash
claude plugin add https://github.com/org/repo
```
Claude Code clones the repository and installs it as a plugin. Updates can be pulled with `claude plugin update plugin-name`.

**Marketplace:**
Plugins can be listed on the Claude Code plugin marketplace for public distribution. Users install them by name: `claude plugin add plugin-name`.

**Managed settings (enterprise):**
Organizations can pre-install plugins for all members by specifying them in organization-level Claude Code settings. Members receive the plugins automatically when they open Claude Code.

---

## Security restrictions for plugin skills

Plugin skills run with reduced trust compared to project or user skills. The following frontmatter fields are silently ignored in plugin skills:

- `hooks` — plugins cannot define lifecycle hooks
- `mcpServers` — plugins cannot provision MCP server connections
- `permissionMode` — plugins cannot override the session permission mode

These restrictions protect users from plugins that could run arbitrary code through hooks or modify their tool permissions.

**Workaround for hooks in plugins:**
If a plugin skill requires hooks to function correctly, document the required hook configuration in the plugin's README and provide a ready-to-paste JSON snippet. Users who want hook behavior can add the configuration to their `.claude/settings.json` globally.

Alternatively, document that users can copy the skill out of the plugin directory into `.claude/skills/` to get full hook support. A copied skill is treated as a project skill with full trust.

---

## Example: release-plugin

The `examples/release-plugin/` directory packages the four release-flow skills from lesson 05 as a distributable plugin.

**Structure:**
```
release-plugin/
  plugin.json
  skills/
    release/SKILL.md
    changelog-entry/SKILL.md
    tag-version/SKILL.md
    publish/SKILL.md
```

**Install and use:**
```bash
claude plugin add ./examples/release-plugin

# Invoke the orchestrator
/release-plugin:release 1.2.0

# Or use individual skills
/release-plugin:changelog-entry
/release-plugin:tag-version patch
/release-plugin:publish
```

**Note on the plugin's `release` skill:**
The orchestrator body references `/changelog-entry`, `/tag-version`, and `/publish` — the unqualified names. When running from within a plugin context, Claude resolves these as `/release-plugin:changelog-entry`, etc. If the skills are also installed as standalone project skills with the same names, the unqualified references will resolve to the project skills instead. To avoid ambiguity in mixed environments, use fully qualified names in plugin orchestrator bodies: `/release-plugin:changelog-entry`.

---

## Versioning and updates

The `version` field in `plugin.json` follows semantic versioning:

- Increment **patch** (1.0.0 → 1.0.1) for bug fixes to existing skill bodies or descriptions.
- Increment **minor** (1.0.0 → 1.1.0) for new skills added to the plugin.
- Increment **major** (1.0.0 → 2.0.0) for breaking changes: skill renames, removed skills, changed argument signatures, or behavioral changes that require users to update how they invoke the skills.

When distributing via Git, tag the release commit with the version: `v1.0.0`. This allows users to pin to a specific version.

---

## Next section

[Capstone: Code Quality Bot](../capstone/README.md)
