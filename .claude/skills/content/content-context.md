---
name: content-context
description: Domain context for content skills - content strategy, writing, SEO, editing, content operations, and publishing workflows
---

# Content Domain Context

## Domain Overview
The **Content** domain covers skills for content strategy, creation, optimization, and operations. Focus areas include the 5-phase content pipeline, SEO, editorial standards, content design, and publishing workflows.

## Core Capabilities

### 1. 5-Phase Content Pipeline
- **Phase 1 - Discover**: Audience research, keyword analysis, competitive gap, brand voice alignment
- **Phase 2 - Outline**: Information architecture, heading structure, SEO brief, DEI review
- **Phase 3 - Draft**: Evidence-based writing, citation management, tone consistency
- **Phase 4 - Revise**: Lint gate (readability, passive voice, clichés), SEO gate (keyword density, structure), DEI gate (inclusive language, accessibility)
- **Phase 5 - Output**: Multi-format export (HTML, Markdown, JSON, social snippets), agent envelope for chaining

### 2. Content Types Supported
- Blog/Article (1200-3000 words)
- Landing Page (conversion-optimized)
- Email (nurture, transactional, broadcast)
- Social (LinkedIn, Twitter/X, Threads)
- Case Study (problem-solution-results)
- Whitepaper (3000+ words, gated)
- Press Release (AP style)
- Video Script (hook-body-CTA)

### 3. Quality Gates
- **Lint**: Flesch-Kincaid ≥ 60, passive voice < 10%, cliché density < 2%
- **SEO**: Primary keyword in H1, first 100 words, 2+ H2s; secondary keywords in H2/H3
- **DEI/Accessibility**: Inclusive language, alt text for images, heading hierarchy, reading level

## Skills in This Domain

| Skill | Description | Key Files |
|-------|-------------|-----------|
| `content/content-writer` | 5-phase AI content creation pipeline with validation gates | `SKILL.md`, `scripts/cli.py`, `references/*.md` |

## Reference Standards
- **SKILL-AUTHORING-STANDARD.md**: All skills ≤500 lines, ≤10KB, kebab-case names
- **SKILL_PIPELINE.md**: 5-stage pipeline (PLAN → SCAFFOLD → AUTHOR → VALIDATE → PUBLISH)
- **Content-Specific**: AP Style / Chicago Manual, WCAG 2.2 AA for content, SEO best practices (Google Search Essentials)

## Integration Points
- **Design Domain**: UX writing with `design/designer-god`, content design handoff
- **Productivity Domain**: Resume/content writing with `productivity/resume-doctor`
- **Business Domain**: Booking confirmation emails via `business/cal-com-api`
- **Engineering Domain**: Technical documentation with `engineering/wix-support`

## Domain Conventions
1. **Brief-First**: Every content piece starts with a structured brief (audience, goal, format, length, tone, angle, keywords)
2. **Evidence-Based**: Claims require citations; stats require sources; quotes require attribution
3. **Gate-Enforced**: Pipeline cannot advance past failed gate without explicit override
4. **Format-Agnostic Core**: Drafting produces structured content; renderers handle output formats
5. **Agent Envelope**: JSON output includes metadata for chaining (brief_id, phase_times, validation_results)

## Change Log
See `CHANGELOG.md` for domain-level changes and skill additions.