# D:\AI-Workflows Skills Library

**Version:** 1.0.0 | **Skills:** 23+ | **Domains:** 5 | **Standard:** SKILL-AUTHORING-STANDARD.md

---

## Overview

This is a structured skills library following the patterns from [claude-skills](https://github.com/alirezarezvani/claude-skills) (355 skills, 602 Python tools, 731 references). Each skill is a self-contained package that can be dropped into any workflow.

```
.agents/skills/
├── SKILL-AUTHORING-STANDARD.md    # Authoring standards (10 patterns)
├── SKILL_PIPELINE.md              # Creation pipeline (5 stages)
├── templates/                     # Starter templates
│   ├── SKILL.md                   # Skill template
│   └── agent-template.md          # Agent template
├── standards/                     # Cross-cutting standards
│   ├── communication/
│   ├── documentation/
│   ├── git/
│   ├── quality/
│   └── security/
├── engineering/                   # 81 skills (target)
│   ├── engineering-context.md
│   ├── INDEX.md
│   ├── zero-hallucination-coder/
│   ├── agent-harness/
│   ├── wix-support/
│   └── ...
├── content/                       # 12 skills (target)
│   ├── content-context.md
│   ├── INDEX.md
│   ├── content-writer/
│   ├── cal-com-api/
│   └── ...
├── design/                        # 8 skills (target)
│   ├── design-context.md
│   ├── INDEX.md
│   ├── product-designer/
│   ├── ui-ux-designer/
│   └── ...
├── productivity/                  # 10 skills (target)
│   ├── productivity-context.md
│   ├── INDEX.md
│   ├── resume-doctor/
│   └── ...
└── business/                      # 8 skills (target)
    ├── business-context.md
    ├── INDEX.md
    └── ...
```

---

## Quick Start

### Use a Skill

```bash
# Direct invocation (Claude Code)
/skill content/content-writer "Write a blog post on CI/CD optimization"

# Or reference in agent workflow
# Agent reads: .agents/skills/content/content-writer/SKILL.md
```

### Skill Structure

```
skill-name/
├── SKILL.md              # Main entry point (≤500 lines, ≤10KB)
├── scripts/              # Python CLI tools (stdlib only)
│   └── tool_name.py      # --help, JSON output, exit codes 0/1/2
├── references/           # Deep-dive references (kebab-case.md)
│   ├── topic-playbook.md
│   ├── topic-framework.md
│   └── topic-checklist.md
├── assets/               # Templates, examples, schemas
│   ├── template.md
│   └── schema.json
└── .agents-plugin/       # Marketplace plugin (optional)
    └── plugin.json
```

### Create a New Skill

```bash
# 1. Plan
cp .agents/skills/templates/SKILL.md skill-spec.md
# Edit skill-spec.md with name, domain, triggers, references

# 2. Scaffold
mkdir -p .agents/skills/<domain>/<skill-name>/{scripts,references,assets}

# 3. Author (follow SKILL-AUTHORING-STANDARD.md)
# - Frontmatter with "Use when" in description
# - 3+ major sections, anti-patterns, short-circuits
# - Related skills table (3-7, with when/when-not)
# - Quality loop + confidence tags

# 4. Validate
python .agents/scripts/validate_skill.py .agents/skills/<domain>/<skill-name>/
```

---

## Current Skills

### Content (3 skills)
| Skill | Description | Status |
|-------|-------------|--------|
| `content-writer` | Senior content writer: blog, landing, email, social, whitepapers | 🟢 Production |
| `cal-com-api` | Cal.com API v2: auth, bookings, events, webhooks, schedules | 🟢 Production |
| `seo-optimizer` | Keyword research, on-page SEO, content depth, technical SEO | 🟡 Planned |

### Engineering (5 skills)
| Skill | Description | Status |
|-------|-------------|--------|
| `zero-hallucination-coder` | 5-phase disciplined coding loop (Discuss→Map→Decompose→Execute→Verify) | 🟡 Planned |
| `agent-harness` | Universal agent loop: manifest→goal→plan→execute→verify→close | 🟡 Planned |
| `wix-support` | Wix Velo, CMS, eCommerce, Headless, SEO, debugging | 🟢 Production |
| `karpathy-coder` | Minimalist, stdlib-first, delete-over-add philosophy | 🟡 Planned |
| `chaos-engineering` | Failure injection, resilience testing, SLO validation | 🟡 Planned |

### Design (2 skills)
| Skill | Description | Status |
|-------|-------------|--------|
| `product-designer` | End-to-end product design: research→strategy→UI→handoff | 🟢 Production |
| `ui-ux-designer` | Visual design, interaction, prototyping, design systems | 🟢 Production |

### Productivity (1 skill)
| Skill | Description | Status |
|-------|-------------|--------|
| `resume-doctor` | ATS-optimized resume builder: analysis, optimization, tailoring | 🟢 Production |

### Business (0 skills - all planned)
| Skill | Description | Status |
|-------|-------------|--------|
| `strategy-analyst` | Market analysis, competitive intel, positioning, GTM | 🟡 Planned |
| `financial-modeler` | SaaS metrics, unit economics, forecasting, fundraising | 🟡 Planned |
| `product-manager` | Product strategy, roadmap, prioritization, metrics | 🟡 Planned |

---

## Standards Compliance

All skills must pass:

| Gate | Check | Tool |
|------|-------|------|
| Structure | Folder layout, naming, required files | `validate_structure.py` |
| Frontmatter | `name` + `description` with "Use when" | `validate_frontmatter.py` |
| Content | 3+ sections, anti-patterns, short-circuits | `validate_content.py` |
| References | Index complete, all files exist | `validate_refs.py` |
| Scripts | Stdlib only, `--help`, JSON, exit codes | `validate_scripts.py` |
| Prose | No em dashes (—) in body text | `grep -r "—" --include="*.md"` |
| Cross-refs | Related skills bidirectional | `validate_xrefs.py` |

Run all: `python .agents/scripts/validate_all.py`

---

## Domain Context Files

Each domain has a context file that skills check first:

| File | Purpose |
|------|---------|
| `engineering/engineering-context.md` | Language defaults, testing philosophy, deployment model |
| `content/content-context.md` | Brand voice, audience, content types, forbidden words |
| `design/design-context.md` | Design principles, process, tooling, accessibility baseline |
| `productivity/productivity-context.md` | GTD conventions, tool preferences, review cadence |
| `business/business-context.md` | Frameworks, metrics, decision types, communication style |

**Priority:** `project-context.md` (user) → `<domain>-context.md` → `company-context.md`

---

## Scripts

Located in `.agents/scripts/` (to be created):

| Script | Purpose |
|--------|---------|
| `validate_skill.py` | Full skill validation |
| `validate_all.py` | Validate all skills |
| `scaffold_skill.py` | Create skill from spec |
| `audit_skill.py` | Gap analysis for existing skills |
| `test_integration.py` | Load skill in test harness |
| `build_plugin.py` | Generate .agents-plugin for marketplace |

---

## Migration from Old Structure

| Old Path | New Path |
|----------|----------|
| `.agents/skills/content-writer/` | `.agents/skills/content/content-writer/` |
| `.agents/skills/cal_booking_skill/` | `.agents/skills/content/cal-com-api/` |
| `.agents/skills/wix_support_skill/` | `.agents/skills/engineering/wix-support/` |
| `.agents/skills/resume-doctor/` | `.agents/skills/productivity/resume-doctor/` |
| `.agents/skills/product-designer/` | `.agents/skills/design/product-designer/` |
| `.agents/skills/resume-doctor/ui-ux-designer/` | `.agents/skills/design/ui-ux-designer/` |

Old directories preserved for reference. New structure is canonical.

---

## Contributing

1. Read `SKILL-AUTHORING-STANDARD.md`
2. Follow `SKILL_PIPELINE.md` stages: Plan → Scaffold → Author → Validate → Publish
3. PRs target `dev` branch (never `main`)
4. Domain owner approves skill spec before scaffold
5. All gates must pass in CI

---

## License

MIT — Use freely in your workflows.

---

*Built on patterns from [claude-skills](https://github.com/alirezarezvani/claude-skills) v2.11.1*