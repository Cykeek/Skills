---
name: engineering-index
description: Index of all skills in the engineering domain
---

# Engineering Domain - Skill Index

## Skills

| Skill | Version | Status | Description | Last Updated |
|-------|---------|--------|-------------|--------------|
| `engineering/wix-support` | 1.0.0 | ✅ Active | Wix platform diagnostic toolkit with 7 commands | 2026-07-17 |

## Domain Statistics
- **Total Skills**: 1
- **Total Reference Files**: 8
- **Total CLI Tools**: 1
- **Lines of Skill Code**: ~280 (SKILL.md only)

## Quick Links
- [Domain Context](engineering-context.md)
- [Changelog](CHANGELOG.md)
- [Skill Authoring Standard](../SKILL-AUTHORING-STANDARD.md)
- [Skill Pipeline](../SKILL_PIPELINE.md)

## Skill Details

### engineering/wix-support
**Path**: `skills/engineering/wix-support/`

**Capabilities**:
- 7 diagnostic commands: diagnose, velo-check, cms-debug, dns-check, editor-compare, ai-tools, escalation
- 8 reference files covering Wix Editor, Velo, CMS, DNS, AI tools, escalation paths
- JSON Schema validation for all commands
- Multiple output formats: JSON, text, table
- No authentication required for diagnostics

**Reference Files** (8):
- `wix-editor-classic.md`, `wix-editor-studio.md`, `velo-overview.md`
- `cms-dynamic-pages.md`, `dns-configuration.md`, `wix-ai-tools.md`
- `escalation-guide.md`, `troubleshooting-checklist.md`

**CLI**: `scripts/wix_support_skill/cli.py`
- Commands: `diagnose`, `velo-check`, `cms-debug`, `dns-check`, `editor-compare`, `ai-tools`, `escalation`
- Options: `--output json|text|table`, `--validate`
- Exit codes: 0 (success), 1 (error)

**Validation**: `python -m wix_support_skill.cli --help` ✅

## Related Skills (Cross-Domain)
- `design/designer-god` - Wix design capabilities, Editor/Studio features
- `business/cal-com-api` - Booking flow integration with Wix sites
- `content/content-writer` - Wix blog/CMS content features
- `productivity/resume-doctor` - Wix portfolio sites, personal websites