---
name: design-context
description: Domain context for design skills - product design, UI/UX, visual design, design systems, accessibility, branding, and design operations
---

# Design Domain Context

## Domain Overview
The **Design** domain covers the complete design operating model: product strategy, UX research, interaction design, visual design, information architecture, accessibility, design systems, branding, and design operations. Focus on evidence-based decisions with measurable outcomes.

## Core Capabilities

### 1. Product Design & Strategy
- **Problem Framing**: JTBD, problem statements, hypothesis statements, success metrics
- **Discovery**: User interviews, surveys, card sorting, tree testing, analytics audit
- **Strategy**: Product vision, roadmap prioritization (RICE/ICE), OKR alignment
- **Validation**: Usability testing (moderated/unmoderated), A/B testing, prototype validation

### 2. UX & Interaction Design
- **Flows**: User flows, task flows, wireflows, screen flows, state diagrams
- **Patterns**: Navigation, forms, onboarding, empty states, error handling, loading
- **Micro-interactions**: Easing curves (spring, cubic-bezier), timing, choreography
- **Platform Conventions**: iOS HIG, Material Design, Web (WAI-ARIA), Desktop

### 3. Visual Design
- **Typography**: Type scales (modular, fluid), variable fonts, optical alignment
- **Color**: OKLCH/P3, semantic tokens, contrast ratios (WCAG 2.2 AA/AAA), dark mode
- **Spacing**: 4px/8px base grid, fluid spacing, layout density tokens
- **Effects**: Shadows (elevation), blur, gradients (mesh, conic), borders/radii

### 4. Information Architecture
- **Sitemaps**: Hierarchical, faceted, hybrid; labeling taxonomy
- **Navigation**: Global, local, contextual, footer, search, breadcrumbs
- **Content Models**: Entity relationships, content types, metadata schemas

### 5. Accessibility (WCAG 2.2)
- **Perceivable**: Text alternatives, adaptable, distinguishable (contrast, resize)
- **Operable**: Keyboard accessible, enough time, seizure safe, navigable
- **Understandable**: Readable, predictable, input assistance
- **Robust**: Compatible, parsing, name/role/value
- **Audit Process**: Automated (axe-core) + manual (screen reader, keyboard, zoom)

### 6. Design Systems
- **Tokens**: Primitive → semantic → component → composite; JSON/Figma Tokens
- **Components**: Anatomy, variants, states, props, slots, composition
- **Documentation**: Storybook, Figma dev mode, design tokens studio
- **Governance**: Contribution model, versioning (semver), deprecation policy

### 7. Brand & Identity
- **Logo System**: Primary, secondary, monogram, responsive breakpoints
- **Brand Book**: Voice/tone, photography style, iconography, motion principles
- **Applications**: Print, digital, environmental, merchandise, motion

### 8. Design Operations
- **Tools**: Figma (primary), FigJam, Figma Slides, plugins
- **Process**: Design critiques, design reviews, handoff specs, QA checklists
- **Metrics**: Design system adoption, component coverage, design debt index
- **Team**: Roles, rituals, career ladders, hiring, onboarding

## Skills in This Domain

| Skill | Description | Key Files |
|-------|-------------|-----------|
| `design/designer-god` | Complete design operating manual with 26 reference guides | `SKILL.md`, `references/*.md` |

## Reference Standards
- **SKILL-AUTHORING-STANDARD.md**: All skills ≤500 lines, ≤10KB, kebab-case names
- **SKILL_PIPELINE.md**: 5-stage pipeline (PLAN → SCAFFOLD → AUTHOR → VALIDATE → PUBLISH)
- **Design-Specific**: WCAG 2.2, Apple HIG, Material Design 3, Figma Plugin API, Design Tokens Format Module

## Integration Points
- **Engineering Domain**: Design token sync, component handoff, accessibility specs
- **Content Domain**: UX writing guidelines, content design patterns
- **Business Domain**: Booking flow design with `business/cal-com-api`
- **Productivity Domain**: Portfolio/resume design with `productivity/resume-doctor`

## Domain Conventions
1. **Evidence Hierarchy**: User data > Analytics > Heuristics > Best practices > Opinion
2. **Anti-Slop Mandatory**: Run all outputs through `anti-slop-design-law.md` checklist
3. **State Coverage**: Every component defines empty, loading, error, partial, full states
4. **Platform Respect**: Native patterns for iOS/Android/Web; no cross-platform forcing
5. **Accessibility First**: WCAG AA as baseline; AAA for critical flows; not a post-check
6. **Token-Driven**: No hardcoded values; all spacing/color/typography via design tokens
7. **Critique Format**: Structured (Problem → Evidence → Recommendation → Trade-offs)

## Change Log
See `CHANGELOG.md` for domain-level changes and skill additions.