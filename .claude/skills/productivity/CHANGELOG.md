---
name: productivity-changelog
description: Changelog for productivity domain skills
---

# Productivity Domain - Changelog

All notable changes to the productivity domain skills.

## [2026-07-17] - Domain Restructure & Validation

### Added
- Domain context file: `productivity-context.md`
- Domain index: `INDEX.md`
- Domain changelog: `CHANGELOG.md`

### Changed
- Migrated `resume-doctor` skill from flat structure to `skills/productivity/resume-doctor/`
- Updated all cross-references in Related Skills tables to use domain paths
- Verified CLI works correctly with all 5 commands

### Fixed
- CLI validation passes: `python -m resume_doctor.cli --help`
- All 13 reference files accessible at new paths

## [2026-07-15] - Initial Skill Creation

### Added
- `productivity/resume-doctor` skill (v2.1.0)
- 13 reference files covering ATS optimization
- CLI with 5 pipeline phase commands

---

## Version History

| Skill | Current Version | Previous Versions |
|-------|----------------|-------------------|
| productivity/resume-doctor | 2.1.0 | 2.0.0, 1.0.0 |

---

*Generated per SKILL_PIPELINE.md domain maintenance requirements*