---
name: productivity-index
description: Index of all skills in the productivity domain
---

# Productivity Domain - Skill Index

## Skills

| Skill | Version | Status | Description | Last Updated |
|-------|---------|--------|-------------|--------------|
| `productivity/resume-doctor` | 2.1.0 | ✅ Active | 5-phase ATS-optimized resume pipeline with 13 reference guides | 2026-07-17 |

## Domain Statistics
- **Total Skills**: 1
- **Total Reference Files**: 13
- **Total CLI Tools**: 1
- **Lines of Skill Code**: ~490 (SKILL.md only)

## Quick Links
- [Domain Context](productivity-context.md)
- [Changelog](CHANGELOG.md)
- [Skill Authoring Standard](../SKILL-AUTHORING-STANDARD.md)
- [Skill Pipeline](../SKILL_PIPELINE.md)

## Skill Details

### productivity/resume-doctor
**Path**: `skills/productivity/resume-doctor/`

**Capabilities**:
- 5-phase ATS optimization: Parse → Analyze → Optimize → Format → Validate
- 13 reference files covering ATS parsers, keywords, formats, compliance
- CLI with 5 pipeline phase commands + batch processing
- Multiple output formats: PDF, DOCX, HTML, JSON, Markdown, Text
- Industry-specific optimization (tech, healthcare, finance, etc.)
- Gap analysis against job descriptions
- Accessibility compliance (WCAG 2.1 AA for PDF output)

**Reference Files** (13):
- `ats-parsers.md`, `keyword-strategy.md`, `resume-formats.md`
- `section-optimization.md`, `achievement-writing.md`, `ats-compliance.md`
- `industry-keywords.md`, `format-specifications.md`, `gap-analysis.md`
- `cover-letter.md`, `linkedin-optimization.md`, `portfolio-integration.md`
- `accessibility.md`

**CLI**: `scripts/resume_doctor/cli.py`
- Commands: `parse`, `analyze`, `optimize`, `format`, `validate`, `batch`
- Input: `--input-file`, `--input-dir`, `--job-description`
- Output: `--output-dir`, `--format pdf|docx|html|json|md|txt`
- Options: `--industry`, `--seniority`, `--ats-target`, `--strict`
- Exit codes: 0 (success), 1 (error), 2 (input error), 3 (validation fail)

**Validation**: `python -m resume_doctor.cli --help` ✅

## Related Skills (Cross-Domain)
- `content/content-writer` - Resume content, cover letters, LinkedIn
- `design/designer-god` - Resume design, portfolio layout, visual hierarchy
- `business/cal-com-api` - Interview scheduling, calendar coordination
- `engineering/wix-support` - Wix portfolio sites, personal websites