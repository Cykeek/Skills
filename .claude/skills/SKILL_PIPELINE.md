# Skill Pipeline Standard

**Version:** 1.0.0 | **Created:** 2026-07-15 | **Applies to:** Skill creation, migration, and validation workflows

---

## Overview

This document defines the end-to-end pipeline for creating, validating, and publishing skills. Based on the claude-skills repository pipeline that processes 355+ skills.

---

## Pipeline Stages

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌────────────┐   ┌───────────┐
│ 1. PLAN     │──▶│ 2. SCAFFOLD  │──▶│ 3. AUTHOR   │──▶│ 4. VALIDATE│──▶│ 5. PUBLISH│
└─────────────┘   └──────────────┘   └─────────────┘   └────────────┘   └───────────┘
```

### Stage 1: PLAN — Requirements & Domain Mapping

**Inputs:**
- User request or skill gap analysis
- Domain assignment (must map to existing domain or propose new one)

**Deliverables:**
- `skill-spec.md` with:
  - Skill name (kebab-case)
  - Domain assignment
  - 4-6 trigger phrases ("Use when...")
  - 3-5 core capabilities
  - 3-7 related skills with when/when-not
  - Reference file list
  - Script requirements (if any)

**Decision Gate:** Domain owner approves spec before scaffolding.

### Stage 2: SCAFFOLD — Generate Structure

Run scaffold script:

```bash
# Creates standard structure
python scripts/scaffold_skill.py --domain <domain> --name <skill-name> --spec skill-spec.md
```

**Output:**
```
skills/<domain>/<skill-name>/
├── SKILL.md (template with frontmatter + section headers)
├── scripts/
├── references/
├── assets/
└── .claude-plugin/
```

### Stage 3: AUTHOR — Content Development

**SKILL.md Authoring Rules:**
1. Fill frontmatter first (name, description with "Use when")
2. Write core methodology/workflow (the "meat")
3. Add anti-patterns (what this skill prevents)
4. Add short-circuit options
5. Write related skills table
6. Create reference files in parallel
7. Build scripts if specified
8. Add assets/templates

**Reference File Pattern:**
```
references/
├── <topic>-playbook.md      # Process/workflow guides
├── <topic>-framework.md     # Decision frameworks
├── <topic>-checklist.md     # Validation checklists
├── <topic>-patterns.md      # Catalog of patterns
└── <topic>-templates.md     # Templates
```

**Script Development:**
```python
#!/usr/bin/env python3
"""<one-line description>"""
import argparse, json, sys

def main():
    parser = argparse.ArgumentParser(description="<description>")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="json")
    args = parser.parse_args()
    
    # Logic here
    result = {"score": 85, "issues": []}
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Stage 4: VALIDATE — Quality Gates

Run validation script:

```bash
python scripts/validate_skill.py skills/<domain>/<skill-name>/
```

**Automated Checks:**
| Check | Threshold | Fail Action |
|-------|-----------|-------------|
| SKILL.md line count | ≤ 500 | Block |
| SKILL.md file size | ≤ 10 KB | Block |
| Frontmatter valid | name + description | Block |
| Description has "Use when" | Yes | Block |
| Section count | ≥ 3 major sections | Block |
| Anti-patterns section | Present | Block |
| Related skills table | 3-7 entries | Block |
| References index table | All refs listed | Block |
| Scripts: stdlib only | No external deps | Block |
| Scripts: JSON output | Yes | Block |
| Scripts: --help works | Yes | Block |
| Naming conventions | All kebab-case | Block |
| No em dashes in prose | 0 occurrences | Block |

**Manual Review:**
- [ ] Content accuracy (domain expert)
- [ ] Trigger phrases realistic
- [ ] Cross-references bidirectional where logical
- [ ] Quality loop / confidence tagging present
- [ ] Communication standard followed (bottom-line first)

### Stage 5: PUBLISH — Integration

1. Add to domain index: `skills/<domain>/INDEX.md`
2. Update domain `CHANGELOG.md`
3. Run integration test: `python scripts/test_integration.py --skill <skill-name>`
4. Create PR with template
5. CI runs full validation suite
6. Merge → auto-deploy to registry (if configured)

---

## Migration Pipeline (Existing Skills)

For skills already in repo (like content-writer, resume-doctor, etc.):

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌────────────┐
│ 1. AUDIT    │──▶│ 2. RESTRUCTURE│──▶│ 3. ENHANCE  │──▶│ 4. VALIDATE│
└─────────────┘   └──────────────┘   └─────────────┘   └────────────┘
```

### Stage 1: AUDIT
Run auditor on each existing skill:
```bash
python scripts/audit_skill.py skills/<old-path>/
```
Produces `audit-report.json` with gaps vs. standard.

### Stage 2: RESTRUCTURE
Move to new domain structure:
```
OLD: .claude/skills/content-writer/
NEW: .claude/skills/content/content-writer/
```
- Move SKILL.md → SKILL.md (may need rewrite)
- Create scripts/ from any inline tools
- Move references/ files, rename to kebab-case
- Create assets/ for templates

### Stage 3: ENHANCE
Apply patterns from standard:
- Add anti-patterns section
- Add short-circuit options
- Build related skills table
- Add reference index table
- Remove em dashes from prose

### Stage 4: VALIDATE
Run standard validation. Must pass all automated checks.

---

## Automation Scripts

Located in `.claude/skills/scripts/`:

| Script | Purpose |
|--------|---------|
| `scaffold_skill.py` | Create new skill structure from spec |
| `validate_skill.py` | Run all automated checks |
| `audit_skill.py` | Analyze existing skill for gaps |
| `convert_skill.py` | Migrate old structure to new |
| `test_integration.py` | Verify skill loads in Claude Code |
| `build_plugin.py` | Generate .claude-plugin/ for marketplace |
| `sync_domains.py` | Regenerate domain INDEX.md files |

---

## CI Pipeline (GitHub Actions / GitLab CI)

```yaml
# .github/workflows/skills.yml
name: Skill Pipeline
on:
  pull_request:
    paths:
      - '.claude/skills/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: python .claude/skills/scripts/validate_all.py
      - run: python .claude/skills/scripts/test_integration.py --all

  audit:
    runs-on: ubuntu-latest
    if: github.event.pull_request.title != '[AUTO]'
    steps:
      - uses: actions/checkout@v4
      - run: python .claude/skills/scripts/audit_changed.py
```

---

## Domain Ownership

Each domain has a designated owner responsible for:
- Approving skill specs (Stage 1)
- Code review on skill PRs
- Maintaining domain INDEX.md and CHANGELOG.md
- Domain context file: `skills/<domain>/<domain>-context.md`

| Domain | Owner | Context File |
|--------|-------|--------------|
| engineering | @engineering-lead | engineering-context.md |
| content | @content-lead | content-context.md |
| design | @design-lead | design-context.md |
| productivity | @productivity-lead | productivity-context.md |
| business | @business-lead | business-context.md |

---

## Metrics & Health

Tracked per skill:
- **Load time** in Claude Code (< 2s)
- **Trigger accuracy** (user asks X → skill activates)
- **Reference usage** (which refs are actually read)
- **Script execution success** rate
- **User satisfaction** (thumbs up/down)

Dashboard: `.claude/skills/health/dashboard.json` (updated by CI)

---

*Based on claude-skills pipeline v2.11.1. Adapted for D:\AI-Workflows.*