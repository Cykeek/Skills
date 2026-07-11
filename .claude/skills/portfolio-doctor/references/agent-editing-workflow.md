# Agent Editing Workflow — Deep Reference

This reference provides explicit, step-by-step instructions for agents executing the Portfolio Doctor skill to **read, write, and edit files** in a user's portfolio repository. Follow this workflow exactly — do not improvise.

---

## 1. Workflow Overview

```
Phase 1: DISCOVER  →  Phase 2: AUDIT  →  Phase 3: WRITE  →  Phase 4: EDIT  →  Phase 5: VERIFY
   (Read)              (Analyze)           (Write)            (Edit)            (Read+Lint)
```

**Each phase must complete before the next begins.** Output the deliverable for each phase before proceeding.

---

## 2. Phase 1: DISCOVER — Locate & Read Portfolio Files

### 2.1 Find Portfolio Root

```bash
# Try common locations in order
ls -la portfolio/                    # 1. Dedicated folder
ls -la site/                         # 2. Alternative name
ls -la website/                      # 3. Alternative name
ls -la . | grep -E "(portfolio|site|website|web)"  # 4. Scan root
```

If multiple candidates exist, read `package.json` or `astro.config.mjs` / `next.config.js` to confirm.

### 2.2 Read Configuration Files (Priority Order)

| File | Purpose | Tool |
|---|---|---|
| `package.json` | Scripts, dependencies, framework detection | `Read` |
| `tailwind.config.ts` / `.js` / `.cjs` | Design tokens, theme | `Read` |
| `astro.config.mjs` / `next.config.js` / `vite.config.ts` | Build config, content collections | `Read` |
| `tsconfig.json` | TypeScript paths, aliases | `Read` |
| `.github/workflows/*.yml` | CI/CD, deployment | `Read` |

### 2.3 Read Content Files

**For Next.js + MDX / Astro / VitePress:**
```bash
# List all project content files
ls -la content/projects/
ls -la src/content/projects/
ls -la docs/work/
```

Read each project file:
```typescript
// Agent: Read these files sequentially
Read: content/projects/project-a.mdx
Read: content/projects/project-b.mdx
Read: content/projects/project-c.mdx
// ... all published projects
```

**For Framer / Webflow:** Export CMS data or request JSON export from user.

**For Notion + Super:** Request Notion database CSV export.

### 2.4 Read Component & Layout Files

```bash
# Project index / filter components
Read: src/components/project/ProjectCard.tsx
Read: src/components/project/ProjectIndex.tsx
Read: src/components/project/TagFilter.tsx

# Case study layout
Read: src/components/project/CaseStudyLayout.tsx
Read: src/app/work/[slug]/page.tsx      # Next.js
Read: src/pages/work/[slug].astro       # Astro

# Design system / tokens
Read: src/styles/globals.css
Read: tailwind.config.ts
Read: src/lib/design-tokens.ts
```

### 2.5 Read Existing Audit Artifacts (If Any)

```bash
Read: portfolio-audit-report.md
Read: portfolio-architecture-spec.md
Read: .portfolio-doctor/rewrite-plan.md
```

---

## 3. Phase 2: AUDIT — Produce Portfolio Audit Report

### 3.1 Execute Audit Using Section 3.1 Template

Apply the **Portfolio Audit Report Template** from `SKILL.md` Section 3.1 against all discovered files.

### 3.2 Output Format

Save audit to workspace:
```bash
Write: .portfolio-doctor/audit-report.md
```

### 3.3 Produce Rewrite Plan

Create a structured plan listing every file to create/modify/delete:

```markdown
# Rewrite Plan — [Candidate Name] / [Target Role]

## New Files to Create (Write)
- content/projects/unified-billing-dashboard-rewritten.mdx
- content/projects/design-system-v2-rewritten.mdx
- .portfolio-doctor/portfolio-architecture-spec.md

## Existing Files to Modify (Edit)
- content/projects/unified-billing-dashboard.mdx
  - Inject metrics in Impact section
  - Add contribution clarity statement
  - Restructure headers to canonical 7-section template
- src/components/project/ProjectCard.tsx
  - Add data-signal attributes for filtering
  - Add role badge component
- src/components/project/TagFilter.tsx
  - Implement multi-tag AND logic
  - Sync with URLSearchParams

## Files to Delete
- content/projects/old-marketing-page.mdx  (archived, not relevant)

## Configuration Updates
- tailwind.config.ts → add semantic color tokens
- src/lib/projects.ts → add filter/sort helpers for new taxonomy
```

Save plan:
```bash
Write: .portfolio-doctor/rewrite-plan.md
```

---

## 4. Phase 3: WRITE — Create New / Refactored Content

### 4.1 Write Rewritten Case Studies

For each project in the rewrite plan, write a new `.mdx` file using the **Case Study Rewrite Specification** (SKILL.md Section 3.2).

**Naming Convention:** `{slug}-rewritten.mdx` (review with user before replacing original).

**Content Requirements:**
- All 7 canonical sections present
- Frontmatter matches taxonomy schema (Section 2.1 of `portfolio-architecture.md`)
- Metrics use "Before → After → Attribution" format (`impact-metric-framing.md`)
- Explicit contribution statement included
- Signals tagged with evidence

### 4.2 Write Portfolio Architecture Spec

Write `portfolio-architecture-spec.md` using **Section 3.3** template.

### 4.3 Write Design Token Updates (If Needed)

If visual audit reveals gaps, write new token files:

```bash
Write: src/styles/design-tokens.css
Write: tailwind.config.ts (updated)
```

---

## 5. Phase 4: EDIT — Surgical In-Place Fixes

### 5.1 Edit Original Content Files

For each file in the rewrite plan's "Existing Files to Modify" list, apply targeted `Edit` operations.

**Pattern:** One `Edit` call per logical change. Group related changes.

**Example: Adding Metrics to Existing Case Study**
```typescript
// BEFORE (in file):
## Results
Improved conversion and user satisfaction.

// AFTER (via Edit):
## Impact & Results

### Primary Metric: Enterprise Activation Rate
**Before:** 18% (Q2 2023, Mixpanel cohort n=2,400)
**After:** 27% (Q4 2023, Mixpanel cohort n=2,100)
**Change:** +9 pp / +50% relative (p < 0.01)
**Attribution:** Checkout redesign (my ownership) + pricing page copy (marketing). Isolation test: redesign variant held pricing constant → +6 pp.

### Secondary Metrics
- Billing investigation time: 45 min → 4 min (Zendesk tag analysis, n=1,200 tickets)
- ARR retained: $460K/yr (Finance model)
- NPS: +34 (from -12, n=180 survey responses)
```

**Example: Adding Contribution Clarity**
```typescript
// Insert after Problem section, before Research
## My Contribution

**Scope Owned:** End-to-end checkout redesign — IA, flows, hi-fi screens (47), interactive prototype, design system component updates (12), developer handoff specs, accessibility audit.

**Decisions Made:** Single-page vs multi-step (chose single-page with progressive disclosure); custom select vs native (built accessible combobox on native select); error recovery pattern (inline + toast).

**Collaboration:** Partnered with PM (Sarah) on scope sequencing; Tech Lead (Miguel) on responsive breakpoints & state management; Research (Priya) on usability test script & synthesis; Marketing (Jen) on pricing page alignment.

**Metric Ownership:** Primary driver of activation lift (+6 pp in isolation); co-owner of investigation time reduction.
```

### 5.2 Edit Component Files

Apply structural fixes to React/Astro/Vue components.

**Example: Add Signal Data Attributes to ProjectCard**
```typescript
// Edit: src/components/project/ProjectCard.tsx
// Find: <article className="project-card">
// Replace with:
<article
  className="project-card"
  data-domain={project.frontmatter.domain}
  data-signals={project.frontmatter.signals.join(',')}
  data-outcome={project.frontmatter.outcomeType.join(',')}
  data-role={project.frontmatter.role}
  data-complexity={project.frontmatter.complexity}
>
```

**Example: Implement Multi-Tag AND Filter Logic**
```typescript
// Edit: src/components/project/TagFilter.tsx
// Replace filter logic:
const filteredProjects = useMemo(() => {
  return allProjects.filter(project => {
    // Domain: OR within category
    const domainMatch = activeFilters.domain.length === 0 ||
      activeFilters.domain.includes(project.frontmatter.domain);

    // Signals: AND across selected signals
    const signalMatch = activeFilters.signals.length === 0 ||
      activeFilters.signals.every(s => project.frontmatter.signals.includes(s));

    // Outcome: OR within category
    const outcomeMatch = activeFilters.outcome.length === 0 ||
      activeFilters.outcome.some(o => project.frontmatter.outcomeType.includes(o));

    // Complexity: OR
    const complexityMatch = activeFilters.complexity.length === 0 ||
      activeFilters.complexity.includes(project.frontmatter.complexity);

    return domainMatch && signalMatch && outcomeMatch && complexityMatch;
  });
}, [allProjects, activeFilters]);
```

### 5.3 Edit Configuration Files

**Example: Add Semantic Color Tokens to Tailwind**
```typescript
// Edit: tailwind.config.ts
// Find: colors: {
// Insert semantic mappings:
colors: {
  primary: 'var(--color-primary)',
  secondary: 'var(--color-secondary)',
  tertiary: 'var(--color-tertiary)',
  // ... all semantic tokens from visual-craft-standards.md
},
```

---

## 6. Phase 5: VERIFY — Confirm Changes

### 6.1 Re-Read Modified Files

```bash
Read: content/projects/unified-billing-dashboard.mdx
Read: src/components/project/ProjectCard.tsx
Read: tailwind.config.ts
```

### 6.2 Run Project Lint / Typecheck / Build

```bash
# Detect package manager
cat package.json | grep -E '"(lint|typecheck|build|check)"'

# Run appropriate commands
npm run lint          # or: pnpm lint, yarn lint
npm run typecheck     # or: tsc --noEmit
npm run build         # verify production build succeeds
```

### 6.3 Verify Audit Criteria Improved

Re-run key audit checks programmatically:

```bash
# Count projects with metrics
grep -r "Primary Metric:" content/projects/ | wc -l

# Verify all 7 sections present in each case study
for f in content/projects/*.mdx; do
  echo "=== $f ==="
  grep -c "^## " "$f"  # should be >= 7
done

# Check for contribution statements
grep -r "My Contribution" content/projects/
```

### 6.4 Output Verification Summary

```markdown
# Verification Summary

## Build & Lint
- TypeScript: ✅ Pass
- ESLint: ✅ Pass (0 errors, 2 warnings)
- Build: ✅ Success (Next.js 14.2.3)

## Audit Improvements
- Projects with primary metrics: 3/3 (was 1/3)
- Projects with 7 canonical sections: 3/3 (was 0/3)
- Projects with contribution statements: 3/3 (was 0/3)
- ProjectCard data-attributes: ✅ Added
- Multi-tag AND filter: ✅ Implemented
- Semantic color tokens: ✅ Added to Tailwind

## Remaining Work
- Dark mode testing on case study pages
- Mobile breakpoint verification for ProjectIndex
- Analytics event instrumentation
```

Save:
```bash
Write: .portfolio-doctor/verification-summary.md
```

---

## 7. Agent Communication Protocol

### 7.1 Phase Transition Messages

At each phase boundary, output a clear status:

```
🔍 PHASE 1 COMPLETE: DISCOVER
Found: Next.js 14 + MDX portfolio at ./portfolio
Read: 4 project files, 12 component files, 3 config files
Ready for AUDIT phase.
```

```
📋 PHASE 2 COMPLETE: AUDIT
Audit saved to .portfolio-doctor/audit-report.md
Rewrite plan saved to .portfolio-doctor/rewrite-plan.md
Ready for WRITE phase.
```

```
✍️ PHASE 3 COMPLETE: WRITE
Created: 3 rewritten case studies, 1 architecture spec
Ready for EDIT phase.
```

```
🔧 PHASE 4 COMPLETE: EDIT
Applied: 12 surgical edits across 5 files
Ready for VERIFY phase.
```

```
✅ PHASE 5 COMPLETE: VERIFY
Build: PASS | Lint: PASS | Audit criteria: 85% improved
All deliverables in .portfolio-doctor/
```

### 7.2 Error Handling

If any tool call fails:
1. Output error details
2. Retry with corrected path/parameters
3. If persistent, note in verification summary and continue

---

## 8. Quick Reference: Tool Call Patterns

| Action | Tool | Example |
|---|---|---|
| Read single file | `Read` | `Read: portfolio/content/projects/a.mdx` |
| Read multiple files | `Read` (parallel) | 4x `Read` calls in one message |
| Write new file | `Write` | `Write: .portfolio-doctor/audit.md, content...` |
| Edit existing file | `Edit` | `Edit: portfolio/src/components/Card.tsx, old, new` |
| List directory | `Bash` | `Bash: ls -la portfolio/content/projects/` |
| Search content | `Grep` | `Grep: "Primary Metric:", portfolio/content/` |
| Run build/lint | `Bash` | `Bash: cd portfolio && npm run build` |

---

## 9. Guardrails

- **Never** edit files not listed in the rewrite plan without user confirmation.
- **Never** delete original content files — write `-rewritten.mdx` variants first.
- **Always** run build/lint before declaring VERIFY complete.
- **Always** preserve frontmatter schema validity when editing `.mdx`.
- **Default** to semantic tokens from `visual-craft-standards.md` for any style changes.