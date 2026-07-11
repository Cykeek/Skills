# Skills & Commands

## Skills System

Skills are **reusable working instructions** defined by a `SKILL.md` file. They describe when and how the Agent should work for specific scenarios.

### SKILL.md Format
```yaml
---
name: my-skill
description: "What this skill does and when to trigger it"
---

# Skill Instructions

Detailed instructions for the Agent to follow...
```

### Where Skills Live
Skills are discovered from these directories (highest priority first):
1. `<project>/.zcode/skills/<name>/SKILL.md`
2. `<project>/.agents/skills/<name>/SKILL.md`
3. `~/.zcode/skills/<name>/SKILL.md`
4. `~/.agents/skills/<name>/SKILL.md`

### Skill Directory Structure
```
my-skill/
├── SKILL.md          (required — YAML frontmatter + markdown body)
├── references/       (optional — extra docs read on demand)
├── scripts/          (optional — helper scripts the model can invoke)
└── assets/           (optional — templates, fixtures, etc.)
```

ZCode loads skills in three layers:
1. **Metadata** (name + description) — always in context. Keep it short.
2. **SKILL.md body** — loaded only when skill triggers. Target under 500 lines.
3. **Bundled files** (`references/`, `scripts/`, `assets/`) — read on demand.

### Creating a Skill
1. Create a directory in one of the discovery paths.
2. Write `SKILL.md` with:
   - **name** — lowercase kebab-case, 1-64 chars, matches directory name.
   - **description** — when to trigger and what it does. Be slightly pushy to ensure triggering.
   - **Body** — detailed instructions. Under 500 lines recommended.
3. Refresh **Settings → Skills** to ensure visibility.

### Using Skills
- Type `$` in chat input to see available skills.
- Invoke with: `$skill-name your request`
- Example: `$code-review-checklist review my changes`

### Importing Skills
- Supports importing from external agents (Claude Code, Codex CLI, etc.).
- Options: **Symlink** or **Copy**.
- Target: **Global** (user-wide) or **current Project**.

### Best-Fit Use Cases
Skills are best for:
- Repeated workflows
- Consistent outputs
- Templates and checklists
- Cross-project reuse

---

## Commands

### Built-in Commands
| Command | Purpose |
|---|---|
| `/goal` | Manage session goals |
| `/compact` | Compress conversation context while preserving key info |

### Using Commands
- Type `/` in input to open the command panel.
- Continue typing to filter by name.
- Add arguments after the command if needed.

### Creating Custom Commands
In **Settings → Commands**:
| Field | Description |
|---|---|
| **Scope** | User (all workspaces) or Workspace (project-specific) |
| **Name** | Invoked as `/command-name` |
| **Description** | Shown in the command picker |
| **Argument hint** | Parameter placeholder (e.g. `<file-path>`) |
| **Prompt** | Content sent to the Agent |

Saved as `.md` files in:
- User scope: `~/.zcode/commands/`
- Workspace scope: project directory

### Importing Commands
- Click **Import commands from external Agent** in Commands settings.
- Select external commands to import.
- Imported commands are editable like custom ones.

### Skills vs Commands
- Use **Commands** for simple prompts.
- Use **Skills** for complete methods, templates, and reusable workflows.
