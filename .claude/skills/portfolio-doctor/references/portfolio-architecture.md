# Portfolio Architecture — Deep Reference

This reference defines the information architecture, navigation patterns, and project taxonomy standards for high-signal portfolio sites. Use when restructuring a portfolio's IA, designing project discovery, or mapping projects to target role signals.

---

## 1. Site Map Standards

### 1.1 Minimum Viable Portfolio Structure

```markdown
/                          # Home — Hero + Top 3 Projects + CTA
/work                      # Project Index — Filterable, searchable, deep-linkable
/work/[slug]               # Case Study — Canonical 7-section template
/about                     # Narrative Bio + Values + Speaking/Writing + Contact
/resume                    # PDF Download + Plain-text version + LinkedIn sync
```

### 1.2 Enhanced Structure (Senior / Lead / Manager)

```markdown
/                          # Home — Hero + Role Signal + Top 3 + Recent Writing
/work                      # Project Index — Multi-tag filter, outcome sort, view modes
/work/[slug]               # Case Study — Full template + TOC + prev/next + share
/work?tag=systems-thinking # Deep-linked filtered views (shareable URLs)
/about                     # Bio + Values + Principles + Mentorship + Speaking
/writing                   # Articles, case study deep-dives, talks (optional)
/resume                    # PDF + Text + Skills matrix + References
/contact                   # Form + Calendly + Email + LinkedIn + GitHub
/design-system             # Public design system docs (if applicable) — Lead+
```

### 1.3 URL Conventions

- **Lowercase, kebab-case:** `/work/unified-billing-dashboard`
- **No dates in URLs:** Avoid `/work/2023/06/project` — breaks if republished.
- **Stable slugs:** Once published, never change. Add redirects if needed.
- **Deep-linkable filters:** `/work?domain=fintech&signal=systems-thinking` — enables recruiter sharing.

---

## 2. Project Taxonomy (Filter System)

Every project must carry structured metadata enabling multi-dimensional filtering. This is the primary discovery mechanism for hiring managers.

### 2.1 Required Taxonomy Fields

```yaml
# Frontmatter example (MDX / YAML / JSON)
title: "Unified Billing Dashboard"
slug: "unified-billing-dashboard"
role: "Senior Product Designer (Lead)"
durationMonths: 6
team: "3 Design, 2 Eng, 1 PM, 1 Research"
domain: "FinTech"                    # Primary domain
subDomain: "Billing & Invoicing"     # Optional specificity
signals:                             # Maps to target role competencies (2–4)
  - "Systems Thinking"
  - "0→1 Ambiguity"
  - "Cross-functional Leadership"
outcomeType:                         # What kind of result? (1–2)
  - "Revenue Growth"
  - "Efficiency"
complexity: "Greenfield"             # Greenfield | Replatform | Feature | Optimization | 0→1
stack:                               # Tools relevant to target role
  - "Figma"
  - "Storybook"
  - "React"
  - "BigQuery"
  - "Mixpanel"
metrics:                             # For index card display
  primary: "Trial→Paid +50% (18%→27%)"
  secondary:
    - "Investigation time 45min→4min"
    - "$460K ARR retained"
thumbnail: "/images/projects/billing-dashboard-hero.webp"
heroImage: "/images/projects/billing-dashboard-hero@2x.webp"
status: "published"                  # published | draft | archived
featured: true                       # Appears in home page top 3
order: 1                             # Manual sort within featured
publishedAt: "2024-01-15"
updatedAt: "2024-03-20"
```

### 2.2 Controlled Vocabularies

**Domain (pick 1):**
`FinTech`, `HealthTech`, `EdTech`, `B2B SaaS`, `Consumer`, `Marketplace`, `Developer Tools`, `Infrastructure`, `AI/ML`, `Web3/Crypto`, `Gaming`, `Enterprise Software`, `Public Sector`, `Non-Profit`

**Signal (pick 2–4 — maps to hiring rubrics):**
`Systems Thinking`, `0→1 Ambiguity`, `Cross-functional Leadership`, `User Research Rigor`, `Design Systems`, `Platform Design`, `Accessibility Champion`, `Data-Informed Design`, `Strategic Influence`, `Mentorship & Growth`, `Design Operations`, `Innovation & R&D`, `Conversion Optimization`, `Retention & Engagement`, `Quality & Craft`, `Technical Partnership`

**Outcome Type (pick 1–2):**
`Revenue Growth`, `Cost Reduction`, `Efficiency`, `Adoption`, `Activation`, `Retention`, `Quality`, `Innovation`, `Risk Reduction`, `Compliance`, `Speed to Market`

**Complexity (pick 1):**
- `Greenfield` — New product/feature, no legacy
- `Replatform` — Migration, tech debt, legacy replacement
- `Feature` — Incremental addition to existing product
- `Optimization` — Iterative improvement, A/B testing, refinement
- `0→1` — Ambiguous problem space, high uncertainty, strategy + execution

**Role Contribution (for team projects):**
`Sole Designer`, `Lead Designer`, `Co-Lead`, `Core Contributor`, `Supporting Contributor`, `Design System Contributor`, `Design Manager`

---

## 3. Navigation & Discovery Patterns

### 3.1 Home Page (6-Second Scan)

| Zone | Content | Purpose |
|---|---|---|
| **Hero** | Name + **Target Role Tagline** + 1-sentence value prop | Immediate role signal |
| **Top 3 Projects** | Project cards with: Thumbnail, Title, One-Line Impact, Role Badge, Signals | Best evidence upfront |
| **CTA** | "View All Work" → `/work` + "Download Resume" → `/resume` | Clear next actions |
| **Trust Signals** | Logos of past companies, speaking events, publications (optional) | Credibility anchors |

**Tagline Formula:** `[Target Title] | [Domain Expertise] | [Superpower]`
> "Senior Product Designer | FinTech & B2B SaaS | Turning Ambiguity into Shipped Systems"

### 3.2 Project Index (`/work`)

**Layout Options:**
- **Grid (default):** 3-col desktop, 2-col tablet, 1-col mobile. Cards per 4.1.
- **List:** Dense, metadata-heavy, better for 20+ projects.
- **Masonry:** Visual-heavy portfolios (illustration, motion, brand).

**Required Controls:**
- **Multi-select Tag Filter:** Domain, Signal, Outcome, Complexity, Role Contribution.
- **Search:** Full-text across title, description, stack, signals.
- **Sort:** Newest, Oldest, Most Impact (primary metric), Alphabetical.
- **View Toggle:** Grid ↔ List.
- **URL Sync:** Filters reflect in query params for sharing.

**Filter UX Rules:**
- **AND logic within category** (Domain: FinTech OR HealthTech), **AND across categories** (Domain=FinTech AND Signal=Systems).
- **Active filter pills** visible above grid with × to remove.
- **Count badges** on each filter option (e.g., "FinTech (3)").
- **Empty state:** "No projects match. Clear filters or adjust selection."
- **Persist state** in `localStorage` for return visits.

### 3.3 Case Study Page (`/work/[slug]`)

**Required Navigation Elements:**
1. **Breadcrumb:** `Home / Work / Project Title`
2. **Progress Indicator:** Optional — "Section 3 of 7" or scroll progress bar.
3. **Table of Contents (Sticky):** Anchor links to all 7 sections.
4. **Prev/Next Project:** Chronological or curated sequence.
5. **Back to Index:** Prominent link to `/work`.
6. **Share/Download:** Copy link, Download PDF (if generated).

**Sticky TOC Behavior:**
- Desktop: Fixed left/right rail (240px), highlights current section via `IntersectionObserver`.
- Mobile: Collapsible drawer triggered by "Contents" button in header.

---

## 4. Home Page Hero Variants by Role Target

### 4.1 IC Designer / Engineer
```markdown
# Maya Chen
**Senior Product Designer** — FinTech & B2B SaaS
*Turning ambiguous problems into shipped, measurable systems.*

[View Work] [Download Resume] [LinkedIn]

## Featured Work
[Card] [Card] [Card]
```

### 4.2 Design Lead / Manager
```markdown
# Maya Chen
**Design Lead** — Building high-trust design organizations
*12 designers • 3 product areas • $40M ARR influence*

**Leadership Philosophy:** [1-sentence]
[View Case Studies] [Read Writing] [Download Resume]

## Recent Impact
- Scaled design team 4→12, 92% retention
- Established design system covering 87% UI
- Instituted JTBD research practice org-wide
```

### 4.3 Staff / Principal Designer
```markdown
# Maya Chen
**Staff Product Designer** — Platform & Systems Strategy
*Defining the design architecture for [Company]'s next decade.*

**Areas of Impact:**
[Systems Strategy] [Design Infrastructure] [Org Capability]

[Deep Dive: Platform Design System] [Speaking & Writing] [Contact]
```

---

## 5. About Page Structure

```markdown
# About

## Narrative Bio (150–250 words)
[Not a resume summary. A story: origin → pivot → current focus → why it matters.]

## Design/Engineering Principles (3–5)
1. **Principle Name** — [1-sentence definition] — [How it shows in your work]
2. ...

## Selected Speaking & Writing
- [Talk Title] — [Event] — [Date] — [Link/Video]
- [Article Title] — [Publication] — [Date] — [Link]

## Mentorship & Community
- [Program/Role] — [Scope] — [Duration]

## Contact
- **Email:** [address]
- **LinkedIn:** [url]
- **GitHub:** [url] (if relevant)
- **Calendly:** [url] (for coffee chats / mentorship)
```

---

## 6. Resume Page Requirements

- **PDF Download:** Single-click, named `Maya-Chen-Resume-2024.pdf`
- **Plain-Text Version:** Copy-pasteable, ATS-friendly, same content
- **Skills Matrix:** Categorized (Tools, Methods, Domains, Languages)
- **LinkedIn Sync Note:** "Last synced: [Date]" — builds trust
- **No JavaScript Required:** Works with `curl` / `wget` / print-to-PDF

---

## 7. Implementation Patterns by Platform

### 7.1 Next.js + MDX (Recommended)

```
portfolio/
├── content/
│   ├── projects/
│   │   ├── unified-billing-dashboard.mdx
│   │   └── ...
│   ├── writing/
│   └── about.mdx
├── src/
│   ├── components/
│   │   ├── ProjectCard.tsx
│   │   ├── ProjectIndex.tsx
│   │   ├── CaseStudyLayout.tsx
│   │   ├── TagFilter.tsx
│   │   ├── MetricCallout.tsx
│   │   └── ...
│   ├── lib/
│   │   ├── projects.ts        # Content layer: getAllProjects, getProject, filterProjects
│   │   ├── taxonomy.ts        # Controlled vocabularies, validation
│   │   └── metrics.ts         # Metric formatting, sorting
│   └── app/
│       ├── work/
│       │   ├── page.tsx       # Index with client-side filter (Fuse.js)
│       │   └── [slug]/
│       │       └── page.tsx   # Case study with MDX remote
│       ├── page.tsx           # Home
│       ├── about/page.tsx
│       ├── resume/page.tsx
│       └── layout.tsx
├── tailwind.config.ts         # Design tokens → Tailwind theme
├── globals.css                # CSS variables for semantic tokens
└── package.json
```

**Content Layer (`lib/projects.ts`):**
```typescript
export interface Project {
  frontmatter: ProjectFrontmatter;
  content: string; // MDX serialized
  slug: string;
}

export function getAllProjects(): Project[] { ... }
export function getProject(slug: string): Project | null { ... }
export function filterProjects(projects: Project[], filters: FilterState): Project[] { ... }
export function sortProjects(projects: Project[], sort: SortOption): Project[] { ... }
```

### 7.2 Astro (Content Collections)

```astro
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    role: z.string(),
    durationMonths: z.number(),
    team: z.string(),
    domain: z.enum([...]),
    signals: z.array(z.enum([...])),
    outcomeType: z.array(z.enum([...])),
    complexity: z.enum([...]),
    stack: z.array(z.string()),
    metrics: z.object({ primary: z.string(), secondary: z.array(z.string()) }),
    thumbnail: z.string(),
    heroImage: z.string(),
    status: z.enum(['published', 'draft', 'archived']),
    featured: z.boolean(),
    order: z.number(),
    publishedAt: z.date(),
    updatedAt: z.date(),
  }),
});

export const collections = { projects };
```

### 7.3 Framer / Webflow (Designer-Friendly)

**CMS Collection: Projects**
- Fields map 1:1 to taxonomy (Section 2.1).
- **Filter Component:** Custom code for multi-tag AND logic + URL sync.
- **Case Study Template:** Rich Text for body + Component slots for MetricCallout, ArtifactGallery, RoleBadge.
- **Design Tokens:** CSS variables injected in Project Settings → Custom Code → Head.

### 7.4 Notion + Super (Low-Code)

**Notion Database Properties:**
| Property | Type | Maps To |
|---|---|---|
| Title | Title | `title` |
| Slug | Formula | `slug` |
| Role | Select | `role` |
| Duration | Number | `durationMonths` |
| Team | Rich Text | `team` |
| Domain | Select | `domain` |
| Signals | Multi-select | `signals` |
| Outcome | Multi-select | `outcomeType` |
| Complexity | Select | `complexity` |
| Stack | Multi-select | `stack` |
| Primary Metric | Rich Text | `metrics.primary` |
| Secondary Metrics | Rich Text | `metrics.secondary` |
| Thumbnail | Files | `thumbnail` |
| Hero Image | Files | `heroImage` |
| Status | Select | `status` |
| Featured | Checkbox | `featured` |
| Order | Number | `order` |
| Published Date | Date | `publishedAt` |

**Limitations:** No custom components, limited typography, no dark mode tokens, no client-side filter.
**Super Workaround:** Custom CSS injection for tokens; filter via Super's native tag pages (OR logic only).

---

## 8. Analytics & Instrumentation

### 8.1 Events to Track

| Event | Properties | Purpose |
|---|---|---|
| `project_view` | `slug`, `title`, `domain`, `signals`, `referrer` | Which projects get attention |
| `project_filter` | `filter_type`, `filter_value`, `result_count` | How recruiters explore |
| `case_study_scroll` | `slug`, `section`, `depth_pct` | Read depth per section |
| `cta_click` | `cta_name`, `location` (hero, card, footer) | Conversion funnel |
| `resume_download` | `format` (pdf, txt) | Recruiter intent signal |
| `contact_click` | `method` (email, linkedin, calendly) | Outbound interest |

### 8.2 Recommended Tools

- **Plausible / Fathom / Umami** — Privacy-first, no cookie banner needed.
- **GA4** — If enterprise requires it; configure `anonymize_ip`.
- **Custom** — Lightweight endpoint (Cloudflare Workers, Vercel Edge Functions) for full control.

---

## 9. SEO & Discoverability

### 9.1 Meta Tags (Per Page)

```html
<!-- Home -->
<title>Maya Chen — Senior Product Designer, FinTech & B2B SaaS</title>
<meta name="description" content="Senior Product Designer turning ambiguous problems into shipped, measurable systems. FinTech, B2B SaaS, Design Systems.">

<!-- Case Study -->
<title>Unified Billing Dashboard — Maya Chen</title>
<meta name="description" content="Cut enterprise billing investigation 45min → 4min, retaining $460K ARR. Senior Product Designer lead, 6 months, 3D/2E.">
<meta property="og:title" content="Unified Billing Dashboard — Maya Chen">
<meta property="og:description" content="Cut enterprise billing investigation 45min → 4min...">
<meta property="og:image" content="https://mayachen.dev/images/projects/billing-dashboard-og.webp">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
```

### 9.2 Structured Data (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Maya Chen",
  "url": "https://mayachen.dev",
  "sameAs": ["https://linkedin.com/in/mayachen", "https://github.com/mayachen"],
  "jobTitle": "Senior Product Designer",
  "worksFor": { "@type": "Organization", "name": "Current Company" },
  "knowsAbout": ["Product Design", "Design Systems", "FinTech", "User Research", "Design Leadership"]
}
```

---

## 10. Architecture Audit Checklist (Agent Use)

When reviewing a portfolio's IA, score each dimension:

| Dimension | 1 (Fail) | 3 (Pass) | 5 (Exemplary) |
|---|---|---|---|
| **Site Map Completeness** | Missing /work or /about | All required pages | Enhanced + writing + design-system |
| **URL Stability** | Dates in URLs, no redirects | Clean, stable slugs | Redirect map for legacy |
| **Project Taxonomy** | No tags, free-text only | Controlled vocabularies implemented | Multi-dim filter + URL sync + shareable |
| **Home Page Scan** | No tagline, no featured work | Tagline + 3 cards + CTA | Role-variant hero + trust signals |
| **Index Discoverability** | Scroll-only, no filter | Basic category filter | Multi-tag AND filter + search + sort + view modes |
| **Case Study Navigation** | No TOC, no prev/next | TOC + prev/next + breadcrumb | Sticky TOC + progress + share + PDF |
| **Deep Linking** | Broken or missing | Filter URLs work | Filter + scroll position + section anchors |
| **Analytics Coverage** | None | Pageviews only | Full event funnel + recruiter cohort |
| **SEO & Structured Data** | Missing | Basic meta tags | Full OG + Twitter + JSON-LD Person |
| **Performance** | LCP > 4s | LCP < 2.5s | LCP < 1.5s, perfect Core Web Vitals |