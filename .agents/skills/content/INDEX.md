---
name: content-index
description: Index of all skills in the content domain
---

# Content Domain - Skill Index

## Skills

| Skill | Version | Status | Description | Last Updated |
|-------|---------|--------|-------------|--------------|
| `content/content-writer` | 2.1.0 | ✅ Active | 5-phase AI content pipeline with 19 reference guides | 2026-07-17 |

## Domain Statistics
- **Total Skills**: 1
- **Total Reference Files**: 19
- **Total CLI Tools**: 1
- **Lines of Skill Code**: ~394 (SKILL.md only)

## Quick Links
- [Domain Context](content-context.md)
- [Changelog](CHANGELOG.md)
- [Skill Authoring Standard](../SKILL-AUTHORING-STANDARD.md)
- [Skill Pipeline](../SKILL_PIPELINE.md)

## Skill Details

### content/content-writer
**Path**: `skills/content/content-writer/`

**Capabilities**:
- 5-phase pipeline: Discover → Outline → Draft → Revise → Output
- 19 reference files covering SEO, DEI, linting, formats, brand voice
- 5 validation gates with configurable strictness
- Multi-format output: blog, landing-page, email, social, case-study, whitepaper, press-release, video-script
- Agent envelope (JSON) and CLI output formats
- Interactive brief builder

**Reference Files** (19):
- `content-brief.md`, `content-formats.md`, `seo-framework.md`
- `dei-guidelines.md`, `brand-voice.md`, `tone-guide.md`
- `lint-rules.md`, `outline-templates.md`, `draft-principles.md`
- `revision-gates.md`, `output-formats.md`, `content-calendar.md`
- `content-metrics.md`, `content-repurposing.md`, `content-localization.md`
- `content-governance.md`, `content-workflow.md`, `ai-prompt-templates.md`
- `content-examples.md`

**CLI**: `scripts/content_writer_skill/cli.py`
- Input: `--brief-file`, `--brief-json`, `--stdin`, `--interactive`
- Output: `--output`, `--output-format text|json`, `--color`, `--preview-only`
- Pipeline: `--strict`, `--strict-seo`, `--strict-dei`, `--max-retries`, `--no-lint`, `--no-seo`, `--no-dei`
- Debug: `--verbose`, `--save-intermediate`, `--lint-config`
- Exit codes: 0 (success), 1 (pipeline fail), 2 (file not found), 3 (JSON error), 4 (validation error), 130 (cancelled)

**Validation**: `python -m content_writer_skill.cli --help` ✅

## Related Skills (Cross-Domain)
- `design/designer-god` - Visual content, layout, design systems
- `business/cal-com-api` - Email confirmations, calendar notifications
- `productivity/resume-doctor` - Resume content, cover letters
- `engineering/wix-support` - Wix blog/CMS content features