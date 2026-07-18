---
name: engineering-changelog
description: Changelog for engineering domain skills
---

# Engineering Domain - Changelog

All notable changes to the engineering domain skills.

## [2026-07-17] - Domain Restructure & Validation

### Added
- Domain context file: `engineering-context.md`
- Domain index: `INDEX.md`
- Domain changelog: `CHANGELOG.md`

### Changed
- Migrated `wix-support` skill from flat structure to `skills/engineering/wix-support/`
- Updated all cross-references in Related Skills tables to use domain paths
- Verified CLI works correctly with all 7 diagnostic commands

### Fixed
- CLI validation passes: `python -m wix_support_skill.cli --help`
- All 9 reference files accessible at new paths

## [2026-07-15] - Initial Skill Creation

### Added
- `engineering/wix-support` skill (v1.0.0)
- 9 reference files covering Wix platform diagnostics
- CLI with 7 diagnostic workflow commands

---

## Version History

| Skill | Current Version | Previous Versions |
|-------|----------------|-------------------|
| engineering/wix-support | 1.0.0 | - |

---

*Generated per SKILL_PIPELINE.md domain maintenance requirements*