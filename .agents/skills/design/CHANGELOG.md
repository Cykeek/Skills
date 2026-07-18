---
name: design-changelog
description: Changelog for design domain skills
---

# Design Domain - Changelog

All notable changes to the design domain skills.

## [2026-07-17] - Domain Restructure & Validation

### Added
- Domain context file: `design-context.md`
- Domain index: `INDEX.md`
- Domain changelog: `CHANGELOG.md`

### Changed
- Migrated `designer-god` skill from flat structure to `skills/design/designer-god/`
- Updated all cross-references in Related Skills tables to use domain paths
- Verified CLI works correctly with all 6 design commands

### Fixed
- CLI validation passes: `python -m product_designer.cli --help`
- All 26 reference files accessible at new paths

## [2026-07-15] - Initial Skill Creation

### Added
- `design/designer-god` skill (v1.0.0)
- 26 reference files covering complete design methodology
- CLI with 6 design workflow commands

---

## Version History

| Skill | Current Version | Previous Versions |
|-------|----------------|-------------------|
| design/designer-god | 1.0.0 | - |

---

*Generated per SKILL_PIPELINE.md domain maintenance requirements*