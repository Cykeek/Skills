---
name: productivity-context
description: Domain context for productivity skills - career optimization, resume optimization, personal productivity, and professional development
---

# Productivity Domain Context

## Domain Overview
The **Productivity** domain covers skills for career optimization, professional development, personal productivity systems, and tools that help individuals work more effectively. Focus on measurable outcomes and evidence-based methodologies.

## Core Capabilities

### 1. Career Optimization
- **ATS Optimization**: Keyword extraction, formatting compliance, section ordering
- **Resume Engineering**: STAR method, quantified achievements, role-specific tailoring
- **Interview Preparation**: Behavioral frameworks (STAR, CAR), technical prep, negotiation
- **LinkedIn Profile**: Headline optimization, skill alignment, content strategy

### 2. Professional Development
- **Skill Gap Analysis**: Current vs target role requirements
- **Learning Path Design**: Curriculum planning, milestone tracking
- **Portfolio Building**: Project selection, case study structure, presentation

### 3. Productivity Systems
- **Task Management**: GTD, time blocking, energy management
- **Focus Techniques**: Pomodoro, deep work, context switching costs
- **Tool Evaluation**: Criteria frameworks, migration paths, integration patterns

## Skills in This Domain

| Skill | Description | Key Files |
|-------|-------------|-----------|
| `productivity/resume-doctor` | 5-phase ATS optimization with CLI validation | `SKILL.md`, `scripts/cli.py`, `references/*.md` |

## Reference Standards
- **SKILL-AUTHORING-STANDARD.md**: All skills ≤500 lines, ≤10KB, kebab-case names
- **SKILL_PIPELINE.md**: 5-stage pipeline (PLAN → SCAFFOLD → AUTHOR → VALIDATE → PUBLISH)
- **Productivity-Specific**: ATS parser compatibility, resume parsing standards (HR-XML, JSON Resume)

## Integration Points
- **Content Domain**: Resume content writing with `content/content-writer`
- **Design Domain**: Resume layout/visual design with `design/designer-god`
- **Engineering Domain**: Technical resume optimization for `engineering/wix-support` roles
- **Business Domain**: Sales/business development resumes with `business/cal-com-api` context

## Domain Conventions
1. **Evidence-Based**: Every recommendation backed by ATS parser behavior or hiring data
2. **Quantified Output**: Metrics over adjectives (e.g., "increased revenue 23%" vs "drove growth")
3. **Role-Specific**: Templates per role family (IC, Manager, Director, Founder)
4. **Validation-First**: CLI validates against real ATS parsers before output
5. **Privacy-Aware**: No PII in logs; local processing by default

## Change Log
See `CHANGELOG.md` for domain-level changes and skill additions.