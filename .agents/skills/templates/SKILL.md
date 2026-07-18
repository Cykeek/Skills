# SKILL.md Template

**Purpose:** Standard template for all skills. Copy this file to create a new skill.

---

## Skill Structure

```
.agents/skills/<domain>/<skill-name>/
├── SKILL.md              # This file (main skill definition, ≤500 lines, ≤10KB)
├── scripts/              # Python CLI tools (stdlib only)
│   ├── <tool-name>.py
│   └── __init__.py
├── references/           # Deep-dive reference material
│   ├── <topic-1>.md
│   └── <topic-2>.md
├── assets/               # Templates, examples, schemas
│   ├── <template-1>.md
│   └── <schema-1>.json
└── .agents-plugin/       # Marketplace plugin (optional)
    └── plugin.json
```

---

## SKILL.md Content Template

Copy the structure below. Replace ALL `<placeholders>`.

```markdown
---
name: <skill-name>
description: "Use when <specific trigger condition>. Example: '<concrete user request>'. <One sentence on what this skill delivers.>"
---

# <Skill Display Name>

<1-2 sentences: what this skill is and what it delivers. Practitioner voice: "This skill helps you..." not "This skill is designed to...">

---

## 1. Quick Start

**When to use:** <3-5 bullet triggers>

**What you get:** <Concrete output artifact(s)>

**Read first:** `<reference-file>.md` for <topic>

---

## 2. Core Methodology

### Phase 1: <Name>

<What happens, practitioner voice. "Do X. Then Y.">

### Phase 2: <Name>

...

### Phase 3: <Name>

---

## 3. Anti-Patterns (Always Enforced)

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| <pattern> | <reason> | <what to do instead> |
| <pattern> | <reason> | <what to do instead> |

---

## 4. Short-Circuit Options

| Scenario | Mode | Steps |
|----------|------|-------|
| <High-stakes / complex> | Full Loop | All phases |
| <Standalone fix> | Abbreviated | Phase 1 → 3 only |
| <Typos / docs> | Direct | Skip to execute |

---

## 5. Forcing Questions

Before starting, clarify:

1. <Question 1>
2. <Question 2>
3. <Question 3>
4. <Question 4>

---

## 6. Related Skills

| Skill | When to Use | When NOT to Use |
|-------|-------------|-----------------|
| `<domain>/<skill-1>` | <trigger> | <avoid when> |
| `<domain>/<skill-2>` | <trigger> | <avoid when> |
| `<other-domain>/<skill-3>` | <trigger> | <avoid when> |

---

## 7. Quality Loop

After every output, self-verify:

- [ ] <Check 1>
- [ ] <Check 2>
- [ ] <Check 3>

**Confidence tag:** 🟢 High / 🟡 Medium / 🔴 Low — append to response.

---

## 8. Communication Standard

**Format:** Bottom-line first → Evidence → Nuance

**Emoji tags:** 🟢 Confirmed / 🟡 Probable / 🔴 Speculative

---

## 9. Output Management (Workspace Standard)

**Every skill MUST write outputs to the workspace `outputs/<skill-name>/` directory**, not inside `.agents/`.

This is handled automatically by the scaffold-generated script template using `workspace_utils`:

```python
# In your skill's CLI entry point (scripts/<skill-name>.py):
from workspace_utils import get_skill_output_dir, create_task_dir

# Get skill's master output directory (creates if needed)
output_dir = get_skill_output_dir("your-skill-name")

# Create a timestamped subfolder for this specific invocation
task_dir = create_task_dir("your-skill-name", "analysis")  # or "generation", "audit", etc.

# Write files to task_dir/
(task_dir / "result.json").write_text(json.dumps(data))
```

**Output structure:**
```
<workspace-root>/
├── outputs/
│   ├── your-skill-name/           # Skill master directory
│   │   ├── analysis_20260717_143022/  # Per-invocation task dir
│   │   │   ├── result.json
│   │   │   └── ...
│   │   └── generation_20260717_143105/
│   │       └── ...
│   └── other-skill/               # Other skills get their own folders
```

**Environment variable:** `CLAUDE_WORKSPACE` can override workspace root (useful for CI/CD).

---

## 10. Reference Files Index

| File | Topics Covered | When to Read |
|------|----------------|--------------|
| `references/<file-1>.md` | <topics> | <trigger> |
| `references/<file-2>.md` | <topics> | <trigger> |

---

## 11. Scripts Index

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `scripts/<tool-1>.py` | <what it does> | <args> | JSON: {...} |
| `scripts/<tool-2>.py` | <what it does> | <args> | JSON: {...} |

---

## 11. Assets Index

| Asset | Purpose | Format |
|-------|---------|--------|
| `assets/<template-1>.md` | <use case> | Markdown template |
| `assets/<schema-1>.json` | <use case> | JSON Schema |

---

## 12. Writing & Communication Style (for your responses)

- Be direct and structured: sections, tables, short paragraphs
- Default to prose first; bullets for steps, comparisons, options
- **No em dashes (—) in body prose.** Replace with period, colon, comma, or parenthesis.
- Explain reasoning on close calls: "I chose X because..."
- Show, don't tell in feedback: show unclear version → show rewrite
- Prioritize ruthlessly: top 3 issues first
- Final scan before every response: (1) no em dashes, (2) grid parity if grids exist, (3) opening starts with reader's reality
```

---

## Frontmatter Rules

| Field | Rule |
|-------|------|
| `name` | kebab-case, unique across all skills |
| `description` | Must contain "Use when" + concrete example + one-sentence deliverable. Max 300 chars. |

---

## Naming Conventions

| Element | Convention |
|---------|------------|
| Skill folder | kebab-case (e.g., `zero-hallucination-coder`) |
| Script files | snake_case.py (e.g., `goal_compiler.py`) |
| Reference files | kebab-case.md (e.g., `design-principles.md`) |
| Asset files | kebab-case.<ext> |
| Section headers | Numbered: `## 1.`, `## 2.` |

---

## Quality Checklist (Pre-Submit)

### Structure
- [ ] Folder follows structure above
- [ ] SKILL.md ≤ 500 lines, ≤ 10 KB
- [ ] Frontmatter valid YAML with name + description
- [ ] Description has "Use when" + example + deliverable

### Content
- [ ] Practitioner voice throughout ("Do X" not "You might consider X")
- [ ] Anti-patterns table present (≥3 entries)
- [ ] Short-circuit options table present
- [ ] Forcing questions present (4 questions)
- [ ] Related skills table (3-7 entries, with when/when-not)
- [ ] Quality loop checklist present
- [ ] Communication standard declared
- [ ] Reference index table complete
- [ ] Scripts index complete (or "None" stated)
- [ ] Assets index complete (or "None" stated)

### Style
- [ ] No em dashes (—) in prose (check with `grep -r "—" SKILL.md`)
- [ ] Bottom-line-first in all responses
- [ ] Confidence tags used (🟢/🟡/🔴)

### Integration
- [ ] All reference files exist in `references/`
- [ ] All scripts exist in `scripts/`, stdlib only, JSON output, `--help` works
- [ ] All assets exist in `assets/`
- [ ] Relative paths work from skill root
- [ ] Skill loads in Claude Code without errors

---

## Example: Minimal Valid Skill

```markdown
---
name: commit-message-writer
description: "Use when user needs a conventional commit message. Example: 'Write a commit message for my changes to auth.py'. Delivers a properly formatted commit message with type, scope, and description."
---

# Commit Message Writer

Helps you write clear, conventional commit messages that explain *fast.

---

## 1. Quick Start

**When to use:**
- "Write a commit message for..."
- "What should my commit message be?"
- Commits need to follow conventional format

**What you get:** A formatted commit message ready to copy.

**Read first:** `references/conventional-commits.md`

---

## 2. Core Methodology

### Phase 1: Analyze Changes
Read the diff. Identify: type (feat/fix/docs/refactor), scope, breaking changes.

### Phase 2: Compose Message
Format: `<type>(<scope>): <description>`
- Type: feat, fix, docs, style, refactor, test, chore
- Scope: file/module/component (optional)
- Description: imperative, lowercase, no period

### Phase 3: Validate
Check: under 72 chars, imperative mood, clear scope.

---

## 3. Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| "Fixed bug" | No scope, no context | "fix(auth): handle null token in refresh" |
| "Updated stuff" | Vague, not imperative | "refactor(api): simplify error handling" |
| Multi-line subject | Breaks tooling | Keep subject ≤ 72 chars |

---

## 4. Short-Circuit Options

| Scenario | Mode | Steps |
|----------|------|-------|
| Simple fix | Direct | Analyze → Compose |
| Breaking change | Full | Analyze → Compose → Add BREAKING CHANGE footer |

---

## 5. Forcing Questions

1. What files changed?
2. What type of change (feat/fix/refactor)?
3. Is there a breaking change?
4. Any related issue numbers?

---

## 6. Related Skills

| Skill | When to Use | When NOT to Use |
|-------|-------------|-----------------|
| `engineering/git-workflow` | Full git workflow including push/PR | Just need a message |
| `engineering/code-review` | Reviewing commit quality | Writing the message |

---

## 7. Quality Loop

- [ ] Subject ≤ 72 chars
- [ ] Imperative mood
- [ ] Type + scope correct
- [ ] Breaking changes noted

**Confidence tag:** 🟢 High

---

## 8. Communication Standard

Bottom-line first → Evidence → Nuance. Tags: 🟢/🟡/🔴

---

## 9. Reference Files Index

| File | Topics Covered | When to Read |
|------|----------------|--------------|
| `references/conventional-commits.md` | Spec, types, examples | Always first |

---

## 10. Scripts Index

None.

---

## 11. Assets Index

None.

---

## 12. Writing & Communication Style

Standard practitioner style. No em dashes.
```

---

*Based on claude-skills SKILL-AUTHORING-STANDARD.md v1.0.0. Adapted for D:\AI-Workflows.*