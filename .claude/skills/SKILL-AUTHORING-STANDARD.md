# Skill Authoring Standard

**Version:** 1.0.0 | **Created:** 2026-07-15 | **Applies to:** All skills in this repository

---

## Overview

This document defines the mandatory structure, patterns, and quality standards for every skill in this repository. It is based on the proven patterns from the [claude-skills](https://github.com/alirezarezvani/claude-skills) repository (355 production skills, 602 Python tools, 731 references).

**Core principle:** Every skill is a self-contained package that can be extracted and dropped into any workflow without modification.

---

## 1. File Structure Standard

### Required Structure

```
skills/<domain>/<skill-name>/
├── SKILL.md              # Main skill file (≤500 lines, ≤10 KB)
├── scripts/              # Python CLI tools (stdlib only, JSON output)
│   └── *.py
├── references/           # Deep-dive reference material
│   └── *.md
├── assets/               # Templates, examples, schemas
│   └── *
└── .claude-plugin/       # Optional: marketplace plugin
    └── plugin.json
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Domain folder | kebab-case | `content`, `engineering`, `design` |
| Skill folder | kebab-case | `content-writer`, `zero-hallucination-coder` |
| Scripts | snake_case.py | `keyword_analyzer.py` |
| References | kebab-case.md | `seo-playbook.md` |
| Assets | kebab-case | `blog-template.md` |

---

## 2. SKILL.md Template (Mandatory)

Every `SKILL.md` **must** follow this exact structure:

```markdown
---
name: <kebab-case-skill-name>
description: "<1-2 sentences: what it does + when to use. Must contain 'Use when...' trigger phrase.>"
---

# <Skill Display Name>

<1-paragraph executive summary: what this skill does, its core philosophy/approach.>

## Core [Concept/Methodology/Workflow]

<The meat of the skill. Organize by phases, principles, or patterns. Use tables for decision trees.>

## [Domain-Specific Sections]

<At least 3 major sections relevant to the skill's domain>

## Anti-Patterns (Enforced)

<List of what this skill actively prevents. Use "❌ Don't" format.>

## Short-Circuit Options

<When to use full vs. abbreviated workflow>

## Related Skills

| Skill | When to Use | When NOT to Use |
|-------|-------------|-----------------|
| `domain/other-skill` | Scenario A | Scenario B |

## Reference Files Index

| File | Topics Covered | When to Read |
|------|----------------|--------------|
| `references/xyz.md` | ... | ... |

## Quality Gates

- [ ] SKILL.md ≤ 500 lines
- [ ] YAML frontmatter has `name` + `description` with "Use when"
- [ ] At least 3 major content sections
- [ ] Anti-patterns section present
- [ ] Related skills table (3-7 entries)
- [ ] References index table present
- [ ] Scripts use stdlib only, JSON output, --help flag
- [ ] References are kebab-case.md in references/
```

### YAML Frontmatter Requirements

```yaml
name: content-writer          # kebab-case, unique across repo
description: "Comprehensive content writing skill... Use when the user asks to write, rewrite, edit, optimize for SEO, or needs a senior content writer's judgment on tone, structure, audience, or strategy."
```

**The description MUST contain "Use when" (or "Use for") to serve as a proactive trigger.**

---

## 3. The 10 Authoring Patterns

### Pattern 1: Context-First
Check for a domain context file before asking questions. If `company-context.md` exists, read it. If not, ask the 4 clarifying questions.

### Pattern 2: Practitioner Voice
Write as an expert, not a textbook. "Do X" beats "You might consider X." Be direct. Own your recommendations.

### Pattern 3: Multi-Mode Workflows
Provide at least 3 modes:
- **Build from scratch** — full workflow
- **Optimize existing** — audit → fix → verify
- **Situation-specific** — e.g., "hotfix," "migration," "exploratory"

### Pattern 4: Related Skills Navigation
3-7 cross-references with explicit when/when-not guidance. Prevents skill sprawl and guides users to the right tool.

### Pattern 5: Reference Separation
SKILL.md ≤ 10 KB. Deeper material goes to `references/`. SKILL.md references them via the index table.

### Pattern 6: Proactive Triggers
List 4-6 conditions where this skill should self-activate (user didn't ask but should have).

### Pattern 7: Output Artifacts
Table mapping common requests → concrete deliverables (not "advice" but "a blog post draft," "an SEO audit report").

### Pattern 8: Quality Loop
Self-verification step before output. Confidence tagging: 🟢 high / 🟡 medium / 🔴 low.

### Pattern 9: Communication Standard
Bottom-line first. Structure: **Bottom Line → Reasoning → Evidence → Next Steps**. Confidence emoji on every claim.

### Pattern 10: Python Tools
- Stdlib only (no `requests`, `pandas`, etc.)
- CLI-first: `python script.py --help` works
- JSON output on stdout for machine parsing
- Scoring 0-100 where applicable
- Exit codes: 0=success, 1=error, 2=validation fail

---

## 4. Pre-Launch Quality Checklist

### Structure
- [ ] Folder follows `skills/<domain>/<skill-name>/`
- [ ] SKILL.md exists with valid frontmatter
- [ ] scripts/ contains only .py files
- [ ] references/ contains only .md files
- [ ] assets/ contains templates/examples
- [ ] .claude-plugin/plugin.json (if publishing)

### Content
- [ ] SKILL.md ≤ 500 lines
- [ ] Frontmatter: name + description with "Use when"
- [ ] 3+ major sections with substantive content
- [ ] Anti-patterns section (enforced rules)
- [ ] Short-circuit options documented
- [ ] Related skills table (3-7 entries, when/when-not)
- [ ] References index table (all files in references/ listed)
- [ ] No em dashes in body prose (replace with . , : or ())

### Integration
- [ ] Skill triggers correctly for its domain queries
- [ ] Related skills point back (bidirectional where logical)
- [ ] References are actually read during relevant tasks
- [ ] Scripts executable and tested

### Automation
- [ ] `.claude-plugin/plugin.json` valid (if applicable)
- [ ] Skill loads in Claude Code without errors
- [ ] No absolute paths in skill or scripts

---

## 5. Domain Context Files

These files live at `skills/<domain>/` level and are checked by skills in that domain:

| File | Created By | Purpose |
|------|------------|---------|
| `company-context.md` | User/Org | Org brand, voice, audience, goals |
| `<domain>-context.md` | Skill Author | Domain defaults, conventions, tooling |
| `project-context.md` | User | Current project specifics |

**Pattern:** Skill checks for `../../<domain>-context.md` first. If missing, asks clarifying questions.

---

## 6. Versioning & Changelog

- **Patch (x.y.z):** Improvements, bug fixes, reference updates
- **Minor (x.y.0):** New skill in domain, new workflow mode
- **Major (x.0.0):** Breaking changes to SKILL.md structure or tool interfaces

Record changes in domain-level `CHANGELOG.md`.

---

## 7. Cross-Platform Packaging (Optional)

For marketplace distribution, each skill can include:
- `.claude-plugin/` — Claude Code plugin
- `.codex/` — OpenAI Codex CLI
- `.gemini/` — Gemini CLI
- `.vibe/` — Mistral Vibe

See `scripts/convert.sh` in claude-skills repo for automation.

---

## 8. Enforcement

This standard is enforced by:
1. **Automated checks** in CI (line count, frontmatter, naming)
2. **Peer review** on every skill PR
3. **Periodic audits** using the checklist above

Non-compliant skills are flagged and must be fixed before merge.

---

*Based on claude-skills v2.11.1 patterns. Adapted for D:\AI-Workflows.*