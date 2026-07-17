# Wix Support Skill Architecture

## Overview
This document describes the architecture of the Wix Support Skill, a comprehensive diagnostic and guidance tool for the Wix platform covering Classic Editor, Wix Studio, Editor X, Velo (Frontend + Backend), CMS, Stores, Bookings, Blog, Events, SEO, Performance, Mobile, Multilingual, Members, Domain/Hosting, CRM, Automations, Debugging, Handoff, Headless, and AI Tools.

## Component Structure

```
skills/engineering/wix-support/
├── SKILL.md                    # Main skill file (agent behavior guide)
├── ARCHITECTURE.md             # This file
├── references/                 # Deep-dive reference material (9 files)
│   ├── editors.md              # Editor types & UI
│   ├── velo-apis.md            # Velo code (frontend + backend)
│   ├── cms.md                  # CMS, datasets, dynamic pages
│   ├── ecommerce.md            # Wix Stores, payments, shipping
│   ├── apps-services.md        # Bookings, Blog, Events, Members, Automations
│   ├── seo-performance.md      # SEO, performance, mobile, domains, multilingual
│   ├── headless-sdk.md         # Wix Headless, REST API, SDK
│   ├── debug-known-bugs.md     # Debugging, known bugs, workarounds
│   └── client-handoff.md       # Client handoff, collaboration, admin
├── schemas/                    # JSON schemas for validation (6 files)
│   ├── diagnose-request.json
│   ├── diagnose-response.json
│   ├── velo-check-request.json
│   ├── velo-check-response.json
│   ├── cms-debug-request.json
│   ├── cms-debug-response.json
│   ├── dns-check-request.json
│   ├── dns-check-response.json
│   └── editor-comparison.json
├── scripts/                    # Python CLI tools
│   ├── __init__.py
│   └── wix_support_skill/
│       ├── __init__.py
│       ├── cli.py              # Main CLI entry point
│       ├── diagnostics.py      # Diagnostic engine
│       ├── validators.py       # Schema validators
│       └── output_manager.py   # Output formatting
└── tests/                      # Contract tests
    ├── test_cli.py
    ├── test_diagnostics.py
    └── test_schemas.py
```

## Data Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Query Classification (SKILL.md Section 1)                  │
│  - Determine intent from 17 categories                      │
│  - Identify editor type (Classic/Studio/Editor X)           │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Reference File Resolution (SKILL.md Section 6)             │
│  - Map intent to reference file(s)                          │
│  - Read relevant reference content                          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Diagnostic Flow Execution (SKILL.md Section 2)             │
│  - Flow A: Visual/layout issues                             │
│  - Flow B: CMS 404 / content not showing                    │
│  - Flow C: Velo code not working                            │
│  - Flow D: Domain/DNS issues                                │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Response Formatting (SKILL.md Section 3)                   │
│  - Structured templates for each query type                 │
│  - Include diagnosis, steps, code examples, prevention      │
└─────────────────────────────────────────────────────────────┘
```

## CLI Architecture

### Command Structure
```
wix-support <command> [options]

Commands:
  diagnose       Diagnose editor/layout issues
  velo-check     Validate Velo code for common issues
  cms-debug      Debug CMS 404 / dynamic page issues
  dns-check      Check domain DNS configuration
  editor-compare Show editor comparison table
  ai-tools       List Wix AI tools and capabilities
  escalation     Show escalation guide
```

### Core Classes

#### `OutputManager`
- Handles output formatting: JSON, text, table
- Configurable via `--output` flag
- Used by all CLI commands for consistent output

#### `WixDiagnostics`
- Contains all diagnostic logic
- Pure Python (stdlib only)
- Methods for each diagnostic flow
- Returns structured data for output

#### `CLI`
- Argument parsing with argparse
- Subcommand dispatch
- Input validation
- Error handling with proper exit codes

## Diagnostic Flows

### Flow A: Visual/Layout Issues
**Input:** Editor type + issue description
**Process:**
1. Classify issue: mobile-only, editor-only, live-site, element-specific, site-wide
2. Map to diagnostic tree (Flow A in SKILL.md)
3. Return step-by-step fix with exact Dashboard/Editor paths

### Flow B: CMS 404 / Dynamic Page Issues
**Input:** Collection name + page slug
**Process:**
1. Determine if Dynamic Item Page
2. Check "Pages Generated" count
3. Validate dataset mode (Read/Read&Write)
4. Check collection permissions
5. Verify CMS Live sync
6. Check for programmatic hiding (.hide()/.collapse())

### Flow C: Velo Code Issues
**Input:** Element ID + code + optional error
**Process:**
1. Check $w.onReady() wrapper
2. Validate element ID format (#prefix)
3. Check backend imports
4. Validate CMS collection names (case-sensitive)
5. Check sandbox vs live
6. Detect CORS/external API issues

### Flow D: Domain/DNS Issues
**Input:** Domain name
**Process:**
1. Check DNS propagation timeline
2. Verify A/CNAME/TXT records match Wix specs
3. Check for conflicting records
4. Verify SSL status
5. Provide dnschecker.org link

## Schema Validation

All CLI inputs/outputs validated against JSON schemas in `schemas/`:

| Schema | Purpose |
|--------|---------|
| diagnose-request.json | Validate diagnose command input |
| diagnose-response.json | Validate diagnose command output |
| velo-check-request.json | Validate velo-check command input |
| velo-check-response.json | Validate velo-check command output |
| cms-debug-request.json | Validate cms-debug command input |
| cms-debug-response.json | Validate cms-debug command output |
| dns-check-request.json | Validate dns-check command input |
| dns-check-response.json | Validate dns-check command output |
| editor-comparison.json | Validate editor comparison output |

## Reference Files Mapping

| User Intent | Reference File | SKILL.md Section |
|-------------|----------------|------------------|
| Editing, layout, design, adding elements | `editors.md` | Section 6, Flow A |
| Velo code questions, errors, examples | `velo-apis.md` | Section 6, Flow C |
| CMS, data, dynamic page issues | `cms.md` | Section 6, Flow B |
| Store, product, payment, order issues | `ecommerce.md` | Section 6 |
| Bookings, Blog, Events, Members, Automations | `apps-services.md` | Section 6 |
| SEO, speed, mobile, domains, translations | `seo-performance.md` | Section 6, Flow D |
| External apps, REST APIs, Headless SDK | `headless-sdk.md` | Section 6 |
| Bug reports, unexpected behavior | `debug-known-bugs.md` | Section 6 |
| Site transfer, collaborators, handoff | `client-handoff.md` | Section 6 |

## Quality Gates

### SKILL.md Requirements
- [ ] ≤ 500 lines
- [ ] YAML frontmatter with `name` + `description` containing "Use when"
- [ ] ≥ 3 major content sections
- [ ] Anti-patterns section (Do's and Don'ts)
- [ ] Short-circuit options documented
- [ ] Related skills table (3-7 entries)
- [ ] References index table (all files listed)

### Scripts Requirements
- [ ] Stdlib only (no external dependencies)
- [ ] CLI-first: `--help` works
- [ ] JSON output on stdout
- [ ] Scoring 0-100 where applicable
- [ ] Exit codes: 0=success, 1=error, 2=validation fail

### References Requirements
- [ ] All files kebab-case.md in `references/`
- [ ] All files listed in References Index table

### Tests Requirements
- [ ] Contract tests for all CLI commands
- [ ] Schema validation tests
- [ ] Diagnostic flow tests

## Integration Points

### Related Skills
- `content/content-writer` → SEO content, blog posts, landing pages for Wix sites
- `design/ui-ux-designer` → Wix Studio layouts, component variants, responsive design
- `engineering/cal-com-api` → Cal.com scheduling integration via Velo/Headless
- `productivity/business-context` → Business context before recommending Wix features

### External Tools
- DNS checking: `dnschecker.org` (referenced, not called)
- Wix Dashboard: All paths reference actual Dashboard navigation
- Wix Support: Escalation channels documented

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-16 | Initial architecture aligned to Skill Authoring Standard v1.0.0 |

---

*Aligned with Skill Authoring Standard v1.0.0 (SKILL-AUTHORING-STANDARD.md)*
*Based on claude-skills repository patterns (355 production skills)*