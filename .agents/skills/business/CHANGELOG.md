---
name: business-changelog
description: Changelog for business domain skills
---

# Business Domain - Changelog

All notable changes to the business domain skills.

## [2026-07-17] - Domain Restructure & CLI Fix

### Added
- Domain context file: `business-context.md`
- Domain index: `INDEX.md`
- Domain changelog: `CHANGELOG.md`

### Changed
- Migrated `cal-com-api` skill from flat structure to `skills/business/cal-com-api/`
- Updated all cross-references in Related Skills tables to use domain paths
- **Fixed CLI**: `--help` now works without authentication (ValueError resolved)
- Verified CLI works correctly with all 20+ commands

### Fixed
- `CalComClient.__init__` now allows deferred auth validation (only validates on actual API calls)
- Early help display in `main()` before client creation
- Clear error message "At least one authentication method must be provided for API calls" when making API calls without auth

## [2026-07-15] - Initial Skill Creation

### Added
- `business/cal-com-api` skill (v1.0.0)
- 6 reference files covering Cal.com API v2
- CLI with 20+ booking and scheduling commands

---

## Version History

| Skill | Current Version | Previous Versions |
|-------|----------------|-------------------|
| business/cal-com-api | 1.0.0 | - |

---

*Generated per SKILL_PIPELINE.md domain maintenance requirements*