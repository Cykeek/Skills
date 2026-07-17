---
name: content-changelog
description: Changelog for content domain skills
---

# Content Domain - Changelog

All notable changes to the content domain skills.

## [2026-07-17] - Domain Restructure & Validation

### Added
- Domain context file: `content-context.md`
- Domain index: `INDEX.md`
- Domain changelog: `CHANGELOG.md`

### Changed
- Migrated `content-writer` skill from flat structure to `skills/content/content-writer/`
- Updated all cross-references in Related Skills tables to use domain paths
- Verified CLI works correctly with all input/output options

### Fixed
- CLI validation passes: `python -m content_writer_skill.cli --help`
- Fixed unicode arrow (→) encoding issue in CLI output
- Removed unused imports (`run_pipeline`, `run_pipeline_from_file`)
- All 19 reference files accessible at new paths

## [2026-07-15] - Initial Skill Creation

### Added
- `content/content-writer` skill (v2.1.0)
- 19 reference files covering content pipeline
- CLI with 4 input methods and flexible output

---

## Version History

| Skill | Current Version | Previous Versions |
|-------|----------------|-------------------|
| content/content-writer | 2.1.0 | 2.0.0, 1.x |

---

*Generated per SKILL_PIPELINE.md domain maintenance requirements*