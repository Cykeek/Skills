# Platform Guidance — Deep Reference

This reference provides platform-specific implementation guidance for the most common portfolio hosting and building platforms. Use when implementing, migrating, or debugging a portfolio on a specific platform.

---

## 1. Platform Decision Framework

| Candidate Profile | Recommended Platform | Rationale |
|---|---|---|
| **Frontend / Full-Stack Engineer** | Next.js + MDX (Vercel) | Demonstrates craft; full control; CI/CD; performance |
| **Design Engineer** | Astro + MDX (Cloudflare Pages) | Island architecture; minimal JS; excellent performance |
| **Senior Product Designer (Code-Comfortable)** | Framer | Visual editing + code components; fast iteration; good defaults |
| **Product Designer (No-Code Preferred)** | Webflow | Visual CMS; interactions; hosting; client handoff friendly |
| **Designer (Notion-Native)** | Notion + Super | Zero friction; content-first; limited customization |
| **Staff+ / Lead (Content-Heavy)** | VitePress / Astro Starlight | Docs-style; search; versioning; low maintenance |
| **Quick MVP / Contractor** | Carrd / Typedream | One-page; minutes to publish; good enough for referral |

---

## 2. Next.js + MDX (Vercel) — Gold Standard for Engineers

### 2.1 Stack
- **Framework:** Next.js 14+ (App Router)
- **Content:** MDX with `next-mdx-remote` or `@next/mdx`
- **Styling:** Tailwind CSS + CSS Variables (design tokens)
- **Deployment:** Vercel (native Next.js support)
- **Analytics:** Vercel Analytics + Plausible/Umami
- **Search:** Algolia DocSearch or client-side Fuse.js

### 2.2 Project Structure
```
portfolio/
├── content/
│   ├── projects/
│   │   ├── project-slug.mdx
│   │   └── ...
│   ├── writing/
│   └── about.mdx
├── src/
│   ├── components/
│   │   ├── ui/              # Primitives (Button, Card, Badge, etc.)
│   │   ├── project/         # ProjectCard, ProjectIndex, CaseStudyLayout
│   │   ├── layout/          # Header, Footer, Navigation, TOC
│   │   └── mdx/             # MDX component overrides
│   ├── lib/
│   │   ├── projects.ts      # getAllProjects, getProject, filter, sort
│   │   ├── taxonomy.ts      # Controlled vocabularies, validation
│   │   └── utils.ts         # clsx, date formatting, etc.
│   ├── app/
│   │   ├── layout.tsx       # Root layout, providers, fonts
│   │   ├── page.tsx         # Home
│   │   ├── work/
│   │   │   ├── page.tsx     # Index (Client Component for filters)
│   │   │   └── [slug]/
│   │   │       └── page.tsx # Case Study (Server Component)
│   │   ├── about/page.tsx
│   │   ├── resume/page.tsx
│   │   └── writing/
│   │       ├── page.tsx
│   │       └── [slug]/page.tsx
│   └── styles/
│       └── globals.css      # CSS variables, @tailwind, base styles
├── public/
│   ├── images/projects/
│   └── fonts/
├── tailwind.config.ts
├── next.config.mjs
├── tsconfig.json
└── package.json
```

### 2.3 Key Implementation Patterns

**Content Layer (`src/lib/projects.ts`):**
```typescript
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { compileMDX } from 'next-mdx-remote/rsc';

export interface ProjectFrontmatter {
  title: string;
  slug: string;
  role: string;
  durationMonths: number;
  team: string;
  domain: string;
  signals: string[];
  outcomeType: string[];
  complexity: 'Greenfield' | 'Replatform' | 'Feature' | 'Optimization' | '0→1';
  stack: string[];
  metrics: { primary: string; secondary: string[] };
  thumbnail: string;
  heroImage: string;
  status: 'published' | 'draft' | 'archived';
  featured: boolean;
  order: number;
  publishedAt: string;
  updatedAt: string;
}

export interface Project {
  frontmatter: ProjectFrontmatter;
  content: string;
  slug: string;
}

const projectsDir = path.join(process.cwd(), 'content/projects');

export function getAllProjects(): Project[] {
  const files = fs.readdirSync(projectsDir).filter(f => f.endsWith('.mdx'));
  return files.map(file => {
    const source = fs.readFileSync(path.join(projectsDir, file), 'utf-8');
    const { data, content } = matter(source);
    return { frontmatter: data as ProjectFrontmatter, content, slug: file.replace('.mdx', '') };
  }).filter(p => p.frontmatter.status === 'published')
    .sort((a, b) => a.frontmatter.order - b.frontmatter.order);
}

export function getProject(slug: string): Project | null { ... }
export function filterProjects(projects: Project[], filters: FilterState): Project[] { ... }
```

**Case Study Page (`src/app/work/[slug]/page.tsx`):**
```typescript
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getProject, getAllProjects } from '@/lib/projects';
import { CaseStudyLayout } from '@/components/project/CaseStudyLayout';
import { MDXRemote } from 'next-mdx-remote/rsc';
import components from '@/components/mdx/components';

export async function generateStaticParams() {
  const projects = getAllProjects();
  return projects.map(p => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const project = getProject(params.slug);
  if (!project) return { title: 'Not Found' };
  const { frontmatter } = project;
  return {
    title: `${frontmatter.title} — Maya Chen`,
    description: `${frontmatter.metrics.primary}. ${frontmatter.role}, ${frontmatter.durationMonths} months.`,
    openGraph: {
      title: frontmatter.title,
      description: frontmatter.metrics.primary,
      images: [`https://mayachen.dev${frontmatter.heroImage}`],
      type: 'article',
    },
  };
}

export default async function Page({ params }: { params: { slug: string } }) {
  const project = getProject(params.slug);
  if (!project) notFound();
  return (
    <CaseStudyLayout project={project.frontmatter}>
      <MDXRemote source={project.content} components={components} />
    </CaseStudyLayout>
  );
}
```

**MDX Components (`src/components/mdx/components.tsx`):**
```tsx
import { MetricCallout } from '@/components/project/MetricCallout';
import { ArtifactGallery } from '@/components/project/ArtifactGallery';
import { RoleBadge } from '@/components/project/RoleBadge';
import { TagList } from '@/components/project/TagList';

export default {
  h1: (props) => <h1 className="text-display font-bold mb-4" {...props} />,
  h2: (props) => <h2 className="text-h1 font-semibold mt-12 mb-4" {...props} />,
  h3: (props) => <h3 className="text-h2 font-semibold mt-8 mb-3" {...props} />,
  p: (props) => <p className="text-body leading-relaxed mb-6" {...props} />,
  ul: (props) => <ul className="list-disc list-inside mb-6 space-y-2" {...props} />,
  ol: (props) => <ol className="list-decimal list-inside mb-6 space-y-2" {...props} />,
  li: (props) => <li className="text-body leading-relaxed" {...props} />,
  blockquote: (props) => <blockquote className="border-l-4 border-brand-500 pl-4 italic text-secondary my-6" {...props} />,
  code: (props) => <code className="font-mono text-mono bg-tertiary px-1.5 py-0.5 rounded" {...props} />,
  pre: (props) => <pre className="bg-neutral-900 text-neutral-100 p-4 rounded-lg overflow-x-auto mb-6" {...props} />,
  a: (props) => <a className="text-link underline underline-offset-2 hover:text-link-hover" {...props} />,
  img: (props) => <figure className="my-8"><img className="w-full rounded-lg shadow-lg" {...props} /><figcaption className="text-caption text-tertiary text-center mt-2" /></figure>,
  // Custom components
  MetricCallout,
  ArtifactGallery,
  RoleBadge,
  TagList,
};
```

### 2.4 Tailwind Config with Design Tokens
```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        // Semantic tokens mapped to CSS variables
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        tertiary: 'var(--color-tertiary)',
        // ... map all semantic tokens
      },
      fontSize: {
        display: ['clamp(2.5rem, 5vw, 3.5rem)', { lineHeight: '1.1', fontWeight: '700' }],
        h1: ['clamp(2rem, 4vw, 2.5rem)', { lineHeight: '1.15', fontWeight: '700' }],
        h2: ['clamp(1.5rem, 3vw, 1.75rem)', { lineHeight: '1.2', fontWeight: '600' }],
        // ... full type scale
      },
      spacing: {
        // 4px base unit scale
        1: '0.25rem', 2: '0.5rem', 3: '0.75rem', 4: '1rem',
        5: '1.25rem', 6: '1.5rem', 8: '2rem', 10: '2.5rem',
        12: '3rem', 16: '4rem', 24: '6rem',
      },
      transitionDuration: {
        fast: '120ms', base: '200ms', slow: '300ms',
      },
      transitionTimingFunction: {
        'ease-out': 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        'ease-spring': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
    },
  },
  plugins: [],
};
export default config;
```

### 2.5 Performance Checklist
- [ ] `next/image` for all images with `priority` on hero, `sizes` for responsive.
- [ ] Variable font (Inter/IBM Plex) single `.woff2` with `font-display: swap`.
- [ ] MDX compiled at build time (static generation) — no runtime compilation.
- [ ] Client-side filter only on `/work` (IntersectionObserver for hydration boundary).
- [ ] Vercel Analytics + Speed Insights enabled.
- [ ] `next-sitemap` for auto sitemap.xml + robots.txt.

---

## 3. Astro (Cloudflare Pages) — Modern Alternative

### 3.1 Why Astro
- **Islands Architecture:** Zero-JS by default; hydrate only interactive components (filters, TOC).
- **Content Collections:** First-class schema validation for frontmatter.
- **Performance:** Consistently tops Lighthouse; minimal bundle.
- **Deploy:** Cloudflare Pages (free, fast, edge).

### 3.2 Key Differences from Next.js
```astro
// src/pages/work/[slug].astro
---
import { getCollection, type CollectionEntry } from 'astro:content';
import CaseStudyLayout from '@/layouts/CaseStudyLayout.astro';

export async function getStaticPaths() {
  const projects = await getCollection('projects', ({ data }) => data.status === 'published');
  return projects.map(project => ({ params: { slug: project.slug }, props: { project } }));
}

const { project } = Astro.props;
const { Content } = await project.render();
---

<CaseStudyLayout project={project.data}>
  <Content />
</CaseStudyLayout>
```

```astro
// src/components/ProjectFilter.astro (Client Island)
---
// Only this component hydrates
const filter = createFilterState();
---
<div class="filter-ui" data-astro-island="visible">
  <!-- Filter UI with Fuse.js search -->
</div>
```

### 3.3 Content Collections Schema
```typescript
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
    domain: z.enum(['FinTech', 'HealthTech', 'B2B SaaS', 'Consumer', 'Marketplace', 'Developer Tools', 'Infrastructure', 'AI/ML', 'Enterprise Software']),
    signals: z.array(z.enum([...])),
    outcomeType: z.array(z.enum([...])),
    complexity: z.enum(['Greenfield', 'Replatform', 'Feature', 'Optimization', '0→1']),
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

---

## 4. Framer — Designer-Friendly with Code Escape Hatch

### 4.1 When to Use
- Designer wants visual editing + custom React components.
- Fast iteration on layout without touching code.
- Good default animations, scroll effects, CMS.

### 4.2 Architecture
- **CMS Collection:** "Projects" with fields per taxonomy (Section 2 of `portfolio-architecture.md`).
- **Custom Code Components:** Build `ProjectCard`, `MetricCallout`, `TagFilter`, `CaseStudyTOC` as Framer Code Components (React + TypeScript).
- **Design Tokens:** CSS Variables in Project Settings → Custom Code → Head.

```css
/* Injected in <head> */
:root {
  --color-primary: #0a0a0a;
  --color-secondary: #ffffff;
  --color-brand-500: #2563eb;
  --space-4: 1rem;
  --font-sans: "Inter", system-ui, sans-serif;
  /* ... all semantic tokens */
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #fafafa;
    --color-secondary: #0a0a0a;
  }
}
```

### 4.3 Limitations & Workarounds
| Limitation | Workaround |
|---|---|
| No multi-tag AND filter | Custom Code Component with Fuse.js + URL sync |
| Limited typography control | CSS variables + `font-variation-settings` |
| No dark mode toggle | CSS `prefers-color-scheme` + manual class toggle via component |
| SEO control limited | Custom Code Component injecting `<meta>` per page |
| Bundle size | Avoid heavy libs; use native Framer motion |

---

## 5. Webflow — Visual CMS, Designer-Handoff Friendly

### 5.1 When to Use
- Designer prefers pure visual development.
- Client handoff required (marketing team edits content).
- Complex scroll animations, Lottie, interactions.

### 5.2 CMS Structure
**Collection: Projects**
| Field | Type | Notes |
|---|---|---|
| Name | Plain Text | Title |
| Slug | Plain Text | Auto-generated from Name |
| Role | Plain Text | "Senior Product Designer (Lead)" |
| Duration | Number | Months |
| Team | Plain Text | "3D, 2E, 1PM, 1R" |
| Domain | Option Set | Controlled vocab |
| Signals | Multi-select Option Set | Controlled vocab |
| Outcome Type | Multi-select Option Set | Controlled vocab |
| Complexity | Option Set | Greenfield/Replatform/Feature/Optimization/0→1 |
| Stack | Multi-select Option Set | Tools |
| Primary Metric | Plain Text | "Trial→Paid +50% (18%→27%)" |
| Secondary Metrics | Plain Text (List) | One per line |
| Thumbnail | Image | 16:9, WebP |
| Hero Image | Image | 2x, WebP |
| Status | Option Set | Published/Draft/Archived |
| Featured | Switch | Home page top 3 |
| Order | Number | Manual sort |
| Published Date | Date/Time | |
| Updated Date | Date/Time | |
| Case Study Body | Rich Text | Full MDX-like content |

### 5.3 Filter Implementation
- **Native:** Category filters (OR logic only).
- **AND Logic:** Custom code in Page Settings → Footer Code:
```javascript
// Fuse.js multi-tag filter with URL sync
// Listen for tag clicks → update URLSearchParams → filter CMS list via DOM
```

### 5.4 Design Tokens in Webflow
- **Variables (New):** Webflow Variables for colors, spacing, typography.
- **Legacy:** CSS custom properties in Project Settings → Custom Code → Head.
- **Typography:** Define global font styles; use `rem` units.

---

## 6. Notion + Super — Zero-Code, Content-First

### 6.1 When to Use
- Candidate lives in Notion; wants zero maintenance.
- Content > craft demonstration.
- Rapid deployment for job search deadline.

### 6.2 Database Properties (Per `portfolio-architecture.md` Section 2.1)
Map each taxonomy field to a Notion property (see table in Section 7.4 of `portfolio-architecture.md`).

### 6.3 Super Configuration
- **Custom Domain:** `mayachen.dev` → Super.
- **CSS Injection:** Super Dashboard → Code → CSS for design tokens.
- **Pretty URLs:** Enabled (uses Notion page slug).
- **Password Protection:** Optional for private drafts.

### 6.4 Hard Limitations
| Limitation | Impact | Mitigation |
|---|---|---|
| No custom components | No MetricCallout, TagFilter, TOC | Rich text formatting only |
| No dark mode tokens | Light-only or OS-level only | CSS `prefers-color-scheme` in Super CSS |
| No client-side filter | Browse-only | Curated "Best Of" pages per domain/signal |
| Limited typography | System fonts mostly | Super CSS `@font-face` for custom fonts |
| No build-time optimization | Large images, no srcset | Manual WebP export; Notion compresses |

**Verdict:** Acceptable for IC designers; insufficient for engineers, design engineers, or staff+ roles where craft demonstration is expected.

---

## 7. VitePress / Astro Starlight — Docs-Style for Content-Heavy Portfolios

### 7.1 When to Use
- Staff/Principal designer with extensive writing, talks, RFCs.
- Design system documentation public.
- Search, versioning, sidebar navigation needed.

### 7.2 Structure
```
portfolio/
├── docs/
│   ├── index.md           # Home
│   ├── work/
│   │   ├── index.md       # Project index (auto-generated from frontmatter)
│   │   ├── project-slug.md
│   ├── writing/
│   ├── design-system/
│   ├── about.md
│   └── resume.md
├── .vitepress/
│   ├── config.ts
│   └── theme/
│       ├── Layout.vue     # Custom layout with project cards
│       └── components/
├── public/images/
└── package.json
```

### 7.3 VitePress Config
```typescript
// .vitepress/config.ts
import { defineConfig } from 'vitepress';

export default defineConfig({
  title: 'Maya Chen — Staff Product Designer',
  description: 'Platform strategy, design systems, organizational design.',
  themeConfig: {
    nav: [
      { text: 'Work', link: '/work/' },
      { text: 'Writing', link: '/writing/' },
      { text: 'Design System', link: '/design-system/' },
      { text: 'About', link: '/about' },
      { text: 'Resume', link: '/resume' },
    ],
    sidebar: {
      '/work/': [
        { text: 'Projects', items: generateProjectSidebar() },
      ],
    },
    search: { provider: 'local' },
  },
  markdown: { frontmatter: 'yaml' },
});
```

---

## 8. Platform Migration Checklist

When moving between platforms, verify:

- [ ] **All project frontmatter** maps to new schema (no data loss).
- [ ] **Images** re-optimized (WebP/AVIF, multiple widths, `srcset`).
- [ ] **URLs preserved** or 301 redirects mapped (Netlify `_redirects`, Vercel `vercel.json`, Cloudflare `_redirects`).
- [ ] **Design tokens** ported exactly (CSS variables ↔ Tailwind ↔ Webflow Variables).
- [ ] **Analytics events** re-implemented (project_view, cta_click, resume_download).
- [ ] **SEO meta tags** + JSON-LD present on all pages.
- [ ] **Sitemap.xml** + `robots.txt` generated.
- [ ] **Performance budget** met (LCP < 2.5s, CLS < 0.1).
- [ ] **Accessibility audit** passes (axe, keyboard, screen reader).
- [ ] **Contact/Resume download** functional.
- [ ] **Custom domain** + SSL configured.
- [ ] **Backup/Export** of old platform content before DNS switch.

---

## 9. Quick Reference: Platform → Skill Signal

| Platform | Signals Demonstrated |
|---|---|
| **Next.js + MDX** | `Technical Partnership`, `Quality & Craft`, `Platform Design` (if custom), `Design Operations` (CI/CD, content layer) |
| **Astro** | `Technical Partnership`, `Quality & Craft`, `Performance` awareness, `Innovation & R&D` (modern stack) |
| **Framer** | `Quality & Craft`, `Cross-functional Partnership` (designer↔engineer handoff), `Technical Partnership` (code components) |
| **Webflow** | `Cross-functional Partnership` (marketing handoff), `Quality & Craft` (interactions), `Design Operations` (CMS design) |
| **Notion + Super** | `User Research Rigor` (content-first), `Speed to Ship` — **Weak on:** `Technical Partnership`, `Platform Design`, `Quality & Craft` |
| **VitePress/Starlight** | `Strategic Influence` (public docs), `Design Operations`, `Technical Partnership`, `Mentorship & Growth` (knowledge sharing) |

**Choose the platform that *authentically* demonstrates your target role's top signals.** Don't over-engineer if you're a visual designer; don't under-engineer if you're a design engineer.