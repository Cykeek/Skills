---
name: design-index
description: Index of all skills in the design domain
---

# Design Domain - Skill Index

## Skills

| Skill | Version | Status | Description | Last Updated |
|-------|---------|--------|-------------|--------------|
| `design/designer-god` | 1.0.0 | ✅ Active | Complete design operating manual with 26 reference guides | 2026-07-17 |

## Domain Statistics
- **Total Skills**: 1
- **Total Reference Files**: 26
- **Total CLI Tools**: 1
- **Lines of Skill Code**: ~133 (SKILL.md only)

## Quick Links
- [Domain Context](design-context.md)
- [Changelog](CHANGELOG.md)
- [Skill Authoring Standard](../SKILL-AUTHORING-STANDARD.md)
- [Skill Pipeline](../SKILL_PIPELINE.md)

## Skill Details

### design/designer-god
**Path**: `skills/design/designer-god/`

**Capabilities**:
- Complete design methodology: product strategy → visual design → design systems → branding
- 12 short-circuit modes for focused tasks (critique, audit, research, mobile-first, etc.)
- Evidence hierarchy: user data > analytics > heuristics > best practices
- Anti-slop design law enforcement
- Quality loop with 5 verification gates

**Reference Files** (26):
- `design-principles.md`, `visual-design.md`, `accessibility.md`
- `dashboard-design.md`, `website-design.md`, `mobile-app-design.md`
- `branding-identity.md`, `interaction-design.md`, `information-architecture.md`
- `design-systems.md`, `ux-research.md`, `design-thinking.md`
- `prototyping.md`, `domains.md`, `faang-design-culture.md`
- `design-craft.md`, `premium-visual-spec.md`
- `design-templates.md`, `ui-skills-visual.md`, `ui-skills-animation.md`
- `ui-skills-accessibility.md`, `ui-skills-polish.md`, `ui-skills-frameworks.md`
- `anti-slop-design-law.md`, `platform-design.md`

**CLI**: `scripts/product_designer/cli.py`
- Commands: `critique`, `audit`, `spec`, `research-plan`, `brief`, `handoff`
- Options: `--format json|markdown|text`, `--shortcut`
- Exit codes: 0 (success), 1 (error)

**Validation**: `python -m product_designer.cli --help` ✅

## Related Skills (Cross-Domain)
- `engineering/wix-support` - Wix design capabilities, Editor/Studio features
- `business/cal-com-api` - Booking flow design, scheduling UI widgets
- `content/content-writer` - UX writing, content design
- `productivity/resume-doctor` - Portfolio/resume design