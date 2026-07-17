# Documentation Standard

**Version:** 1.0.0 | **Applies to:** All SKILL.md, reference files, and user-facing docs

---

## File Types & Purposes

| Type | Location | Purpose | Max Lines |
|------|----------|---------|-----------|
| SKILL.md | `skills/<domain>/<skill>/` | Main entry point, methodology | 500 |
| Reference | `skills/<domain>/<skill>/references/` | Deep-dive, playbooks, frameworks | 800 |
| Asset | `skills/<domain>/<skill>/assets/` | Templates, examples, schemas | N/A |
| Standard | `skills/standards/<category>/` | Cross-cutting rules | 500 |
| Template | `skills/templates/` | Reusable starter files | 300 |

---

## Markdown Conventions

### Headings
- `#` — Skill name (once, top of SKILL.md)
- `##` — Major sections (Core Workflow, Anti-Patterns, etc.)
- `###` — Sub-sections
- `####` — Rarely, only for deep nesting

### Frontmatter (SKILL.md Only)
```yaml
---
name: kebab-case-skill-name
description: "What it does. Use when the user asks to [trigger phrase]."
---
```

### Tables
- **Always** use pipes `|` with header separator `|---|---|`
- Align columns for readability in source
- Header row required
- Max 5 columns for readability

### Code Blocks
- Fenced with language: ````python````
- No line numbers
- Max 80 chars width (soft)

### Links
- **Relative** for repo files: `../references/seo-playbook.md`
- **Absolute** for external: `https://example.com`
- **Anchor** for same-file: `#quality-loop`

---

## Reference File Categories

| Suffix | Purpose | Example |
|--------|---------|---------|
| `-playbook.md` | Step-by-step process | `seo-playbook.md` |
| `-framework.md` | Decision framework | `persuasion-framework.md` |
| `-checklist.md` | Validation list | `editing-checklist.md` |
| `-patterns.md` | Pattern catalog | `hook-patterns.md` |
| `-templates.md` | Reusable templates | `email-templates.md` |
| `-methodology.md` | Research/approach | `research-methodology.md` |

---

## SKILL.md Required Sections (In Order)

1. **Frontmatter** — name + description with "Use when"
2. **Executive Summary** — 1 paragraph
3. **Core Methodology/Workflow** — The "meat" (phases, principles, patterns)
4. **Domain-Specific Sections** — 2-4 sections relevant to skill
5. **Anti-Patterns (Enforced)** — Table, ≥3 rows
6. **Short-Circuit Options** — When to abbreviate
7. **Related Skills** — Table, 3-7 entries, when/when-not
8. **Reference Files Index** — Table, all files in references/
9. **Quality Loop** — Checklist + confidence tag

---

## Reference File Structure

### Playbook Template
```markdown
---
name: <topic>-playbook
description: "Step-by-step process for <topic>"
---

# <Topic> Playbook

## Overview
<1 paragraph: what this achieves>

## Prerequisites
- [ ] Required input/state

## Steps

### Phase 1: <Name>
1. **Action** — Detail
   - Sub-detail
   - *Why this matters*

### Phase 2: <Name>
...

## Decision Points
| Situation | Choose | Because |
|-----------|--------|---------|
| ... | ... | ... |

## Output Artifact
<What the user has at the end>

## Common Pitfalls
| Pitfall | Symptom | Fix |
|---------|---------|-----|
| ... | ... | ... |
```

### Framework Template
```markdown
---
name: <topic>-framework
description: "Decision framework for <topic>"
---

# <Topic> Framework

## Purpose
<When to use this framework>

## The Framework
| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Criterion 1 | ... | ... | ... |

## Decision Rules
1. If X → Choose A
2. If Y → Choose B
3. Default → C

## Worked Examples
### Example 1: <Scenario>
**Decision:** Option B
**Reasoning:** ...
```

---

## Asset Conventions

| Asset Type | Naming | Format |
|------------|--------|--------|
| Template | `<format>-template.md` | Markdown with `{{placeholders}}` |
| Example | `<topic>-example.md` | Filled template |
| Schema | `<name>.json` / `.yaml` | JSON Schema or YAML |
| Data | `<name>.csv` / `.json` | Raw data |

---

## Cross-References

### In SKILL.md → References
```markdown
| File | Topics Covered | When to Read |
|------|----------------|--------------|
| `references/seo-playbook.md` | Keyword research, on-page, audit | SEO requests |
```

### In References → SKILL.md
```markdown
> **See also:** [`../SKILL.md`](../SKILL.md) — Core methodology
```

### In Standards → Skills
```markdown
> **Enforced by:** `skills/standards/quality/quality-standard.md`
```

---

## Maintenance Rules

| Rule | Enforcement |
|------|-------------|
| No dead links | CI link check |
| References index complete | CI validates all files listed |
| Line limits respected | CI line count |
| Em-dash free | CI grep check |
| Frontmatter valid | CI YAML parse |

---

*Documentation is the API between skills and users. Keep it sharp.*