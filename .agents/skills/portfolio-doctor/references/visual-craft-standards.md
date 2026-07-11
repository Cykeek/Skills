# Visual Craft Standards — Deep Reference

This reference defines the visual and interaction quality bar for portfolios targeting senior IC, lead, and manager roles at top-tier companies. Use when auditing or implementing portfolio visual systems.

---

## 1. Typography System

### 1.1 Type Scale (Modular Scale, Base 16px)

| Token | Size (rem) | Size (px) | Line Height | Use Case |
|---|---|---|---|---|
| `--text-display` | 3.5rem | 56px | 1.1 | Hero headlines, case study titles |
| `--text-h1` | 2.5rem | 40px | 1.15 | Page titles, section headers |
| `--text-h2` | 1.75rem | 28px | 1.2 | Case study section heads |
| `--text-h3` | 1.25rem | 20px | 1.3 | Sub-sections, card titles |
| `--text-body-lg` | 1.125rem | 18px | 1.6 | Lead paragraphs, intro copy |
| `--text-body` | 1rem | 16px | 1.6 | Body copy, case study narrative |
| `--text-body-sm` | 0.875rem | 14px | 1.5 | Metadata, captions, footnotes |
| `--text-caption` | 0.75rem | 12px | 1.4 | Tags, labels, timestamps |
| `--text-mono` | 0.875rem | 14px | 1.5 | Code, metrics, data tables |

### 1.2 Font Stacks

**Sans-Serif (Primary — UI, Body, Headings):**
```css
--font-sans: "Inter", "IBM Plex Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```
*Rationale: Inter/IBM Plex Sans offer excellent legibility at small sizes, extensive weight ranges, and variable font support for performance.*

**Serif (Optional — Editorial, Long-form):**
```css
--font-serif: "IBM Plex Serif", "Source Serif 4", Georgia, Cambria, serif;
```

**Mono (Code, Metrics, Data):**
```css
--font-mono: "JetBrains Mono", "IBM Plex Mono", "SF Mono", Menlo, Consolas, monospace;
```

### 1.3 Font Weight Strategy

| Weight | Token | Usage |
|---|---|---|
| 400 | `--weight-regular` | Body, long-form |
| 500 | `--weight-medium` | Emphasis, subheads, buttons |
| 600 | `--weight-semibold` | Headings, strong emphasis |
| 700 | `--weight-bold` | Display, hero, metric callouts |

**Variable Font Preferred:** Single `.woff2` with `wght` axis (100–700) for performance.

### 1.4 Typographic Rules

- **Measure (line length):** 60–75ch for body copy; max 90ch for wide layouts.
- **Paragraph spacing:** `1.5em` margin-bottom (not `<br>`).
- **Heading proximity:** `margin-top: 2.5rem; margin-bottom: 1rem;` — headings belong to the content *below*.
- **No all-caps for body text.** Small-caps (`font-variant-caps: small-caps`) only for metadata/tags at ≤14px.
- **Tabular numerals** (`font-variant-numeric: tabular-nums`) for all metrics, data tables, counters.

---

## 2. Spacing System

### 2.1 Base Unit: 4px (0.25rem)

All spacing values derive from multiples of 4px.

| Token | Value (rem) | Value (px) | Use Case |
|---|---|---|---|
| `--space-0` | 0 | 0 | Reset |
| `--space-1` | 0.25rem | 4px | Micro gaps, inline icon spacing |
| `--space-2` | 0.5rem | 8px | Tight component padding, form field gaps |
| `--space-3` | 0.75rem | 12px | Standard component padding |
| `--space-4` | 1rem | 16px | **Base rhythm** — card padding, section gutter |
| `--space-5` | 1.25rem | 20px | Medium separation |
| `--space-6` | 1.5rem | 24px | Section padding, card gaps |
| `--space-8` | 2rem | 32px | Large section separation |
| `--space-10` | 2.5rem | 40px | Page-level padding (mobile) |
| `--space-12` | 3rem | 48px | Page-level padding (desktop) |
| `--space-16` | 4rem | 64px | Hero vertical rhythm |
| `--space-24` | 6rem | 96px | Major section breaks |

### 2.2 Layout Grid

- **Container max-width:** 1200px (content) / 1400px (wide case study layouts with side-aside).
- **Columns:** 12-column fluid grid, 24px gutter (desktop), 16px (tablet), 16px (mobile).
- **Content column:** 8/12 default; 6/12 for dense case study reading; 12/12 mobile.

---

## 3. Color System (Semantic Tokens)

### 3.1 Token Architecture

```
color/
  primitive/       # Raw values (never used directly in components)
    neutral-0      # #FFFFFF
    neutral-50     # #FAFAFA
    neutral-100    # #F5F5F5
    neutral-200    # #E5E5E5
    neutral-300    # #D4D4D4
    neutral-400    # #A3A3A3
    neutral-500    # #737373
    neutral-600    # #525252
    neutral-700    # #404040
    neutral-800    # #262626
    neutral-900    # #171717
    neutral-950    # #0A0A0A
    brand-50..950  # Brand hue scale (single hue, 10 steps)
    accent-50..950 # Accent hue scale (complementary, 10 steps)
    status-success
    status-warning
    status-error
    status-info

  semantic/        # Component-facing tokens (ONLY these in CSS)
    bg-primary     # Page background
    bg-secondary   # Card/surface background
    bg-tertiary    # Subtle elevation, hover states
    bg-inverse     # Dark surface for light content
    text-primary   # Primary body text
    text-secondary # Muted body, metadata
    text-tertiary  # Placeholder, disabled, captions
    text-inverse   # On dark/brand backgrounds
    text-link      # Link default
    text-link-hover
    border-subtle  # Hairline dividers
    border-default # Standard borders
    border-strong  # Focus rings, active states
    focus-ring     # Visible focus indicator (WCAG)
    status-success-bg / text / border
    status-warning-bg / text / border
    status-error-bg / text / border
    status-info-bg / text / border
```

### 3.2 Light / Dark Mode Mapping

| Semantic Token | Light Mode | Dark Mode |
|---|---|---|
| `bg-primary` | `neutral-50` | `neutral-950` |
| `bg-secondary` | `neutral-0` | `neutral-900` |
| `bg-tertiary` | `neutral-100` | `neutral-800` |
| `text-primary` | `neutral-900` | `neutral-50` |
| `text-secondary` | `neutral-600` | `neutral-400` |
| `text-tertiary` | `neutral-400` | `neutral-500` |
| `border-subtle` | `neutral-200` | `neutral-800` |
| `border-default` | `neutral-300` | `neutral-700` |
| `focus-ring` | `brand-500` | `brand-400` |

**Implementation:** CSS custom properties with `@media (prefers-color-scheme: dark)` or class-based `.theme-dark` toggle.

### 3.3 Contrast Requirements (WCAG 2.2 AA)

| Element | Minimum Ratio | Target |
|---|---|---|
| Body text (≥16px) | 4.5:1 | 7:1 |
| Large text (≥18px bold / ≥24px) | 3:1 | 4.5:1 |
| UI components (borders, icons) | 3:1 | 4.5:1 |
| Focus indicators | 3:1 (against adjacent) | 4.5:1 |

**Test with:** `color-contrast-checker` in CI, manual audit on all semantic pairs.

---

## 4. Component Visual Standards

### 4.1 Project Card (Index View)

```markdown
┌─────────────────────────────────────────────────────┐
│  [Thumbnail: 16:9, object-fit: cover, 240×135px]   │
├─────────────────────────────────────────────────────┤
│  [Role Badge]  [Outcome Tag]  [Domain Tag]          │  ← Gap: space-2
│                                                     │
│  **Project Title**                                  │  ← H3, weight 600
│  One-line impact summary (metric + outcome)         │  ← Body-sm, text-secondary
│                                                     │
│  [Stack: Figma, React, SQL]  [6 mo • Lead • 3D/2E]  │  ← Caption, text-tertiary
└─────────────────────────────────────────────────────┘
```

**States:**
- Default: `border-subtle`, `bg-secondary`
- Hover: `border-default`, `shadow-md` (elevation), `translateY(-2px)`
- Focus: `outline: 2px solid var(--focus-ring); outline-offset: 2px;`
- Active: `scale(0.98)`

**Accessibility:** Card is a `<article>` with `aria-labelledby="title-id"`. Entire card is a link wrapper (not just title).

### 4.2 Case Study Hero

```markdown
┌────────────────────────────────────────────────────────────┐
│  [Breadcrumb: Home / Work / Project Title]                 │
├────────────────────────────────────────────────────────────┤
│  [Role Badge]  [Duration]  [Team Size]  [Domain Tag]       │
│                                                            │
│  # Project Title                                            │  ← Display
│  **One-line impact summary with metric**                   │  ← Body-lg, text-secondary
│                                                            │
│  [Metric Callout]  [Metric Callout]  [Metric Callout]      │  ← 3-column grid
│  +83% conversion    45min→4min      $460K ARR retained    │
└────────────────────────────────────────────────────────────┘
```

**Metric Callout Component:**
```css
.metric-callout {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: var(--space-4);
  text-align: center;
}
.metric-value { font: var(--text-h2); font-weight: 700; font-variant-numeric: tabular-nums; color: var(--text-primary); }
.metric-label { font: var(--text-caption); color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
```

### 4.3 Case Study Content Layout

```markdown
<article class="case-study">
  <header class="case-study-hero">...</header>
  
  <nav class="case-study-toc" aria-label="Case study sections">
    <ol>
      <li><a href="#problem">Problem & Opportunity</a></li>
      <li><a href="#research">Research & Discovery</a></li>
      ...
    </ol>
  </nav>

  <section id="problem">...</section>
  <section id="research">...</section>
  ...
  
  <footer class="case-study-navigation">
    <a href="/work/prev-project" rel="prev">← Previous Project</a>
    <a href="/work" class="back-to-index">All Work</a>
    <a href="/work/next-project" rel="next">Next Project →</a>
  </footer>
</article>
```

**Content Width:** `max-width: 42rem` (672px / 42ch at 16px) for optimal reading measure.

**Image/Artifact Handling:**
- Full-bleed images: `width: 100vw; margin-left: calc(50% - 50vw);` (breakout)
- Figma embeds: Aspect ratio 16:9, lazy-loaded, fallback screenshot.
- Code blocks: `--font-mono`, `--text-mono`, `overflow-x: auto`, line numbers optional.

---

## 5. Interaction & Motion Standards

### 5.1 Motion Tokens

| Token | Value | Use Case |
|---|---|---|
| `--duration-fast` | 120ms | Micro-interactions (hover, focus, ripple) |
| `--duration-base` | 200ms | Standard transitions (panel open, tooltip) |
| `--duration-slow` | 300ms | Page transitions, modal enter/exit |
| `--ease-out` | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` | Default easing (Material) |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful, bouncy (success states) |
| `--ease-in` | `cubic-bezier(0.55, 0.06, 0.68, 0.19)` | Exit, dismiss |

### 5.2 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 6. Responsive Breakpoints

| Breakpoint | Token | Container | Grid | Typography Adjustments |
|---|---|---|---|---|
| Mobile | `--bp-sm` | 320px–639px | 4col / 16px gutter | `--text-display: 2.5rem`, `--text-h1: 2rem`, base padding `space-4` |
| Tablet | `--bp-md` | 640px–1023px | 8col / 20px gutter | `--text-display: 3rem`, base padding `space-6` |
| Desktop | `--bp-lg` | 1024px–1439px | 12col / 24px gutter | Full scale |
| Wide | `--bp-xl` | 1440px+ | 12col / 24px gutter + side margins | Max container 1200px |

**Mobile-First CSS Pattern:**
```css
.component { /* mobile styles */ }
@media (min-width: 640px) { .component { /* tablet */ } }
@media (min-width: 1024px) { .component { /* desktop */ } }
@media (min-width: 1440px) { .component { /* wide */ } }
```

---

## 7. Accessibility Baseline (WCAG 2.2 AA)

### 7.1 Checklist (Every Component)

- [ ] **Color contrast** — All semantic pairs pass 4.5:1 (text) / 3:1 (UI)
- [ ] **Focus visible** — `outline: 2px solid var(--focus-ring); outline-offset: 2px;` on all interactive elements
- [ ] **Focus order** — Logical tab sequence matching visual hierarchy
- [ ] **Keyboard operable** — All interactions reachable and usable via keyboard
- [ ] **ARIA labels** — Icon-only buttons, status indicators, dynamic regions
- [ ] **Heading hierarchy** — Single `<h1>` per page; no skipped levels
- [ ] **Landmarks** — `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`
- [ ] **Images** — Descriptive `alt` for content images; `alt=""` for decorative
- [ ] **Forms** — Labels associated (`for`/`id`); error messages linked via `aria-describedby`
- [ ] **Motion** — Respects `prefers-reduced-motion`; no auto-play >5s without pause
- [ ] **Language** — `lang` attribute on `<html>`; `lang` on foreign phrases

### 7.2 Portfolio-Specific A11y

- Project cards: `<article>` with `aria-labelledby`, entire card clickable but keyboard-focusable once.
- Case study TOC: `<nav aria-label="Case study sections">` with `<ol>` links.
- Metric callouts: Use `<dl>` (definition list) for label/value pairs.
- Figma embeds: Title attribute + fallback link to Figma file.
- PDF download: `<a href="..." download>Download PDF</a>` — not a button.

---

## 8. Performance Budgets

| Metric | Budget | Measurement |
|---|---|---|
| Largest Contentful Paint (LCP) | ≤ 2.5s | WebPageTest / Lighthouse |
| First Input Delay (FID) | ≤ 100ms | Lighthouse |
| Cumulative Layout Shift (CLS) | ≤ 0.1 | Lighthouse |
| Total Blocking Time (TBT) | ≤ 200ms | Lighthouse |
| Font load (woff2 variable) | ≤ 50KB gzipped | Network tab |
| Hero image (WebP/AVIF) | ≤ 100KB | Network tab |
| JS bundle (gzipped) | ≤ 80KB | Bundle analyzer |

**Image Strategy:**
- Hero: AVIF + WebP fallbacks, multiple widths (`srcset`), `priority` loading.
- Thumbnails: WebP, 2× density, lazy-loaded (`loading="lazy"`).
- Figma embeds: Static screenshot fallback, lazy-load iframe on interaction.

---

## 9. Platform-Specific Implementation Notes

### 9.1 Next.js + MDX (Recommended for Engineers)
- Content: `content/projects/*.mdx` with frontmatter for taxonomy.
- Components: `components/` mapped via MDX components prop.
- Tokens: `tailwind.config.ts` extends design tokens; CSS variables in `globals.css`.
- Search/Filter: Client-side (Fuse.js) or server-side (Algolia/Meilisearch).
- Analytics: `next/script` for Plausible/GA4; custom events on project view, CTA click.

### 9.2 Framer / Webflow (Designer-Friendly)
- Tokens: CSS variables in Project Settings → Custom Code → Head.
- CMS: Collection for Projects (fields: title, slug, role, duration, team, tags, metrics, heroImage, caseStudyRichText).
- Filtering: CMS Filter + custom code for multi-tag AND logic.
- Components: Symbols for ProjectCard, MetricCallout, RoleBadge.

### 9.3 Notion + Super / Potion (Low-Code)
- Database: Properties map to taxonomy (Role, Domain, Outcome, Signals).
- Templates: Case study page template with synced blocks for hero, TOC, sections.
- Limitations: No custom components, limited typography control, no dark mode tokens.
- Workaround: Publish Notion → Super for custom domain + CSS injection for tokens.

### 9.4 Static HTML / Astro / VitePress (Maximum Control)
- Content: Markdown/MDX + frontmatter.
- Build-time: Generate project index JSON for client-side filtering.
- Deploy: Cloudflare Pages / Netlify / Vercel / GitHub Pages.
- Best for: Engineers demonstrating frontend craft.

---

## 10. Visual Audit Checklist (Agent Use)

When auditing a portfolio's visual craft, score each dimension 1–5:

| Dimension | 1 (Fail) | 3 (Pass) | 5 (Exemplary) |
|---|---|---|---|
| **Type Scale** | Inconsistent, random sizes | Modular scale applied | Variable font, fluid scaling, perfect measure |
| **Spacing Rhythm** | Arbitrary px values | 4px base unit consistent | Fluid spacing, container queries |
| **Color Semantics** | Hardcoded hex everywhere | Semantic tokens defined | Light/dark complete, WCAG AAA on key pairs |
| **Component Consistency** | Each card different | Shared component library | Design system docs + Storybook |
| **Responsive Behavior** | Broken < 768px | Works at all breakpoints | Container-queried, intrinsic layouts |
| **Focus & Keyboard** | No focus styles | Visible focus, logical order | Focus trapping, skip links, roving tabindex |
| **Motion Quality** | Janky, no easing | Smooth, consistent tokens | Respects reduced-motion, meaningful choreography |
| **Image Performance** | Unoptimized PNGs | WebP + srcset | AVIF/WebP, LQIP, priority hints |
| **Content Hierarchy** | Flat, scannability low | Clear heading structure | Progressive disclosure, TOC, anchor links |