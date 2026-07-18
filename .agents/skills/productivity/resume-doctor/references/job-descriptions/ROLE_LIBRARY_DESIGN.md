# Role-Specific Job-Description Reference Library Design

## Folder Structure

```
references/
└── job-descriptions/
    ├── product-manager/
    │   ├── associate-pm.md
    │   ├── product-manager.md
    │   ├── senior-pm.md
    │   ├── staff-pm.md
    │   └── principal-pm.md
    ├── software-engineer/
    │   ├── backend-engineer.md
    │   ├── frontend-engineer.md
    │   ├── fullstack-engineer.md
    │   ├── staff-engineer.md
    │   └── principal-engineer.md
    ├── designer/
    │   ├── product-designer.md
    │   ├── ux-designer.md
    │   ├── ui-designer.md
    │   ├── ux-researcher.md
    │   └── design-systems-engineer.md
    ├── data/
    │   ├── data-analyst.md
    │   ├── data-scientist.md
    │   ├── ml-engineer.md
    │   ├── data-engineer.md
    │   └── analytics-engineer.md
    ├── engineering-leadership/
    │   ├── engineering-manager.md
    │   ├── director-engineering.md
    │   ├── vp-engineering.md
    │   └── cto.md
    ├── devops-platform/
    │   ├── devops-engineer.md
    │   ├── platform-engineer.md
    │   ├── sre.md
    │   └── cloud-engineer.md
    ├── security/
    │   ├── security-engineer.md
    │   ├── application-security.md
    │   └── security-architect.md
    ├── qa-test/
    │   ├── qa-engineer.md
    │   ├── sdet.md
    │   └── test-automation-engineer.md
    ├── mobile/
    │   ├── ios-engineer.md
    │   ├── android-engineer.md
    │   ├── flutter-engineer.md
    │   └── react-native-engineer.md
    └── specialized/
        ├── solutions-engineer.md
        ├── developer-advocate.md
        ├── technical-writer.md
        ├── engineering-manager.md
        └── staff-software-engineer.md
```

---

## Template Document Structure

Each role template file (`role-name.md`) must contain these sections:

---

### 1. Role Metadata (YAML Frontmatter)

```yaml
---
role_id: "software-engineer/fullstack-engineer"
canonical_title: "Full-Stack Software Engineer"
aliases: ["Full-Stack Engineer", "Fullstack Engineer", "Software Engineer (Full Stack)"]
seniority_levels: ["Mid", "Senior", "Staff", "Principal"]
related_roles: ["frontend-engineer", "backend-engineer", "software-engineer"]
ats_keywords:
  - "React"
  - "Node.js"
  - "TypeScript"
  - "PostgreSQL"
  - "AWS"
  - "REST APIs"
  - "GraphQL"
  - "CI/CD"
  - "Docker"
  - "Kubernetes"
  - "System Design"
  - "Microservices"
ats_skills_taxonomy:
  frontend: ["React", "TypeScript", "Next.js", "Tailwind", "Vite", "Vitest"]
  backend: ["Node.js", "Python", "Go", "PostgreSQL", "Redis", "REST", "GraphQL"]
  infrastructure: ["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD", "Observability"]
  architecture: ["System Design", "Microservices", "Event-Driven", "Caching", "API Design"]
  practices: ["TDD", "Code Review", "CI/CD", "Observability", "Performance Optimization"]
seniority_signals:
  mid:
    - "Ships features independently"
    - "Writes tests"
    - "Participates in code reviews"
  senior:
    - "Designs system architecture"
    - "Mentors engineers"
    - "Drives technical decisions"
    - "Owns end-to-end delivery"
  staff:
    - "Defines technical strategy"
    - "Cross-team architecture"
    - "Technical standards"
    - "Organizational influence"
  principal:
    - "Company-wide technical strategy"
    - "Industry thought leadership"
    - "Multi-year technical vision"
ats_weight_hints:
  must_have: ["React", "Node.js", "TypeScript", "PostgreSQL", "AWS", "System Design"]
  strong_signal: ["GraphQL", "Kubernetes", "Terraform", "Observability", "Mentoring"]
  nice_to_have: ["Go", "Python", "WebSockets", "WebRTC", "WebAssembly"]
ats_ats_parser_hints:
  greenhouse: ["react", "node.js", "typescript", "postgresql", "aws"]
  lever: ["react", "node", "typescript", "postgres", "aws"]
  workday: ["React", "Node.js", "TypeScript", "PostgreSQL", "Amazon Web Services"]
  greenhouse_weight_map:
    "system design": 3.0
    "react": 2.5
    "typescript": 2.5
    "aws": 2.0
    "kubernetes": 2.0
    "mentoring": 1.5
---
```

---

### 2. Role Summary (1 paragraph)

> **Full-Stack Software Engineer** — Designs, builds, and operates end-to-end features across the full stack (frontend, backend, infrastructure). Owns features from design through production operation. Collaborates with product, design, and platform teams. Expected to own significant subsystems at Senior+ levels.

---

### 3. Core Responsibilities (ATS-Keyword-Rich Bullet Bank)

```markdown
## Core Responsibilities (ATS-Optimized Bullet Bank)

### Feature Delivery (All Levels)
- Design, build, and ship **end-to-end features** across **React/TypeScript frontend** and **Node.js/Go/Python backend** services
- Develop **RESTful APIs** and **GraphQL APIs** with **OpenAPI/Swagger** specifications
- Build **responsive, accessible UIs** using **React**, **TypeScript**, **Tailwind CSS**, **Next.js**
- Implement **server-side rendering (SSR)**, **static site generation (SSG)**, and **client-side rendering** patterns
- Write **unit tests (Vitest/Jest)**, **integration tests**, and **E2E tests (Playwright/Cypress)** achieving >80% coverage

### Backend & Data (All Levels)
- Design and optimize **PostgreSQL** schemas, **Redis** caching layers, and **Elasticsearch** indexes
- Build **event-driven architectures** using **Kafka**, **RabbitMQ**, or **AWS EventBridge**
- Implement **authentication/authorization** (OAuth 2.0, OIDC, JWT, RBAC/ABAC)
- Design **database migration strategies** (Prisma, Drizzle, raw SQL) with zero-downtime deployments

### Infrastructure & Operations (Senior+)
- Provision and manage **AWS infrastructure** using **Terraform**/**CloudFormation**/**CDK**
- Containerize services with **Docker**; orchestrate with **Kubernetes (EKS/GKE/AKS)**
- Implement **CI/CD pipelines** (GitHub Actions, GitLab CI, CircleCI) with **automated testing, staging, progressive delivery**
- Establish **observability**: **OpenTelemetry**, **Prometheus**, **Grafana**, **Datadog**, **ELK**, **Sentry**
- Implement **feature flags** (LaunchDarkly, Unleash), **canary deployments**, **blue-green deployments**

### System Design & Architecture (Senior+)
- Design **scalable microservices architectures** with **domain-driven design (DDD)**, **event sourcing**, **CQRS**
- Conduct **system design reviews**, **architecture decision records (ADRs)**, **threat modeling**
- Define **API contracts**, **service contracts**, **data contracts** with **schema registry** (Confluent, Apicurio)
- Lead **capacity planning**, **cost optimization**, **disaster recovery**, **chaos engineering**

### Technical Leadership (Staff+)
- Define **technical strategy** and **multi-year technical roadmap** aligned with business objectives
- Establish **engineering standards**: code style, architecture patterns, testing strategy, security baselines
- Lead **cross-team initiatives**: platform migrations, re-architecture, tech debt reduction
- Mentor **Senior+ engineers**; grow **Staff+ engineers**; define **career ladders**
- Represent engineering in **executive reviews**, **board presentations**, **industry conferences**

### Collaboration & Product (All Levels)
- Partner with **Product Managers** on **discovery**, **roadmap planning**, **OKR setting**
- Collaborate with **Designers** on **design systems**, **component libraries**, **accessibility (WCAG 2.1 AA)**
- Work with **Platform/DevOps/SRE** teams on **developer experience**, **self-service platforms**
- Participate in **incident response**, **blameless postmortems**, **runbook authoring**
```

---

### 4. Required Skills Taxonomy (ATS Parser Optimized)

```markdown
## Required Skills Taxonomy (ATS Keyword Bank)

### Must-Have (ATS Gate Keywords)
**Frontend**
- React 18+, TypeScript 5+, Next.js 14+, Tailwind CSS, Vite
- State Management: TanStack Query, Zustand, Redux Toolkit
- Testing: Vitest, React Testing Library, Playwright
- Accessibility: WCAG 2.1 AA, ARIA, semantic HTML

**Backend**
- Node.js 20+ (Express, Fastify, Hono, tRPC) OR Go 1.22+ OR Python 3.11+ (FastAPI, Django)
- PostgreSQL 15+ (indexing, partitioning, read replicas), Redis 7+, MongoDB
- API: REST (OpenAPI 3.1), GraphQL (Apollo, GraphQL Yoga), gRPC, tRPC
- Auth: NextAuth.js, Clerk, Auth0, custom JWT/OAuth2/OIDC

**Infrastructure**
- AWS (ECS/Fargate, Lambda, RDS, ElastiCache, CloudFront, S3, IAM)
- Docker, Docker Compose, Multi-stage builds
- CI/CD: GitHub Actions (preferred), GitLab CI
- Observability: OpenTelemetry, Prometheus, Grafana, Sentry, PagerDuty

### Strong Signal (Differentiators)
- Kubernetes (EKS/GKE), Helm, Kustomize, ArgoCD/Flux
- Terraform, Pulumi, AWS CDK
- Event-driven: Kafka, NATS, EventBridge, Temporal
- Real-time: WebSockets, Server-Sent Events, Socket.io, LiveView
- Performance: Profiling (Py-Spy, 0x), Load Testing (k6, Artillery), Core Web Vitals
- Security: OWASP Top 10, SAST/DAST (Semgrep, Snyk), SBOM (Syft, Cosign)

### Seniority Differentiators
**Senior**: System design, mentoring, incident command, technical debt paydown
**Staff**: Cross-team architecture, technical strategy, platform decisions, org influence
**Principal**: Company-wide strategy, industry leadership, patent/IP, keynote speaking
```

---

### 5. Seniority-Specific Signal Keywords (ATS Weight Hints)

```markdown
## Seniority Signal Keywords (ATS Weight Hints)

### Mid-Level (2-5 yrs)
WEIGHT: 1.0-1.5x
- "Shipped", "Delivered", "Implemented", "Built", "Developed", "Wrote tests"
- "Collaborated with", "Participated in code reviews", "Fixed bugs"
- "React", "TypeScript", "Node.js", "PostgreSQL", "Git", "CI/CD"

### Senior (5-8 yrs)
WEIGHT: 2.0-2.5x
- "Designed", "Architected", "Led", "Owned", "Drove", "Spearheaded"
- "System design", "Architecture decision records", "Technical strategy"
- "Mentored", "Code review leader", "Incident commander", "On-call lead"
- "Microservices", "Event-driven", "Observability", "Cost optimization"

### Staff (8-12 yrs)
WEIGHT: 3.0x
- "Defined technical strategy", "Multi-team architecture", "Platform decisions"
- "Technical standards", "Engineering culture", "Hiring bar", "Career ladders"
- "Executive presentation", "Board reporting", "Industry speaking"
- "Platform engineering", "Developer experience", "Technical vision"

### Principal (12+ yrs)
WEIGHT: 4.0x+
- "Company-wide technical strategy", "Multi-year roadmap", "Industry thought leadership"
- "Patents", "Open source leadership", "Standards bodies", "Keynote speaker"
- "M&A technical due diligence", "Crisis leadership", "Transformation"
```

---

### 6. ATS Parser Keyword Maps (Per-Parser)

```markdown
## ATS Parser Keyword Maps

### Greenhouse
EXACT_MATCH: ["React", "TypeScript", "Node.js", "PostgreSQL", "AWS", "Docker", "Kubernetes", "GraphQL", "REST API", "CI/CD", "Terraform", "System Design"]
FUZZY_MATCH: ["react.js", "node", "postgres", "amazon web services", "k8s", "gql", "continuous integration"]

### Lever
EXACT_MATCH: ["React", "TypeScript", "Node", "PostgreSQL", "AWS", "Docker", "Kubernetes", "GraphQL", "REST", "CI/CD"]
STEMMING: ["develop", "architect", "lead", "mentor", "design", "optimize", "scale", "deploy"]

### Workday
EXACT_MATCH: ["React", "Node.js", "TypeScript", "PostgreSQL", "Amazon Web Services", "Docker", "Kubernetes", "GraphQL", "RESTful APIs", "Continuous Integration"]
SYNONYMS: {"React": ["React.js", "ReactJS"], "Node.js": ["Node", "NodeJS"], "AWS": ["Amazon Web Services", "Amazon Cloud"]}

### iCIMS
SKILL_CLUSTERS:
  frontend: ["React", "TypeScript", "Next.js", "Tailwind CSS", "Redux", "Webpack", "Vite"]
  backend: ["Node.js", "Express", "Fastify", "PostgreSQL", "Redis", "MongoDB", "GraphQL"]
  cloud: ["AWS", "EC2", "Lambda", "RDS", "ECS", "EKS", "CloudFormation", "Terraform"]
  devops: ["Docker", "Kubernetes", "GitHub Actions", "Jenkins", "Prometheus", "Grafana"]
```

---

### 7. Resume Section Templates (ATS-Optimized)

```markdown
## Resume Section Templates (Copy-Paste Ready)

### Professional Summary (Senior Full-Stack)
Senior Full-Stack Engineer with 7+ years designing, building, and operating **scalable web applications** serving **10M+ users**. Expert in **React/TypeScript**, **Node.js/Go**, **PostgreSQL**, **AWS**, **Kubernetes**. Proven track record: **reduced API latency 60%** (p99 < 200ms), **cut infrastructure costs 35%** via **Kubernetes rightsizing**, **led 5-engineer team** delivering **$2M ARR feature**. Passionate about **developer experience**, **observability**, **system design**.

### Core Competencies (Keyword Bank)
**Frontend:** React 18, TypeScript 5, Next.js 14, Tailwind CSS, TanStack Query, Zustand, Vitest, Playwright, Storybook, WCAG 2.1 AA
**Backend:** Node.js 20, Go 1.22, Fastify, tRPC, PostgreSQL 16, Redis 7, Prisma, Drizzle ORM, Kafka, NATS
**Cloud/Infra:** AWS (ECS, Lambda, RDS, ElastiCache, CloudFront, IAM), Terraform, Docker, Kubernetes (EKS), GitHub Actions, ArgoCD
**Observability:** OpenTelemetry, Prometheus, Grafana, Datadog, Sentry, PagerDuty, k6
**Practices:** System Design, DDD, Event-Driven Architecture, TDD, Code Review, RFC/ADR, Incident Response, Chaos Engineering

### Experience Bullets (STAR + Metrics Template)
**Senior Full-Stack Engineer** | Company | 2021-Present
- **Architected** and **led migration** of **monolithic Rails API → microservices (Go/Node.js)** on **EKS**, reducing **deployment frequency from weekly → 50+/day** and **p99 latency 800ms → 120ms**
- **Designed** **event-driven order processing pipeline** using **Kafka + Temporal**, processing **$500M/yr GMV** with **99.99% reliability**
- **Built** **real-time collaboration features** (WebSockets, CRDTs) in **React/TypeScript**, supporting **100K+ concurrent users**
- **Established** **observability platform** (OpenTelemetry → Prometheus/Grafana/Datadog), reducing **MTTR 45min → 8min**
- **Mentored** **3 mid-level engineers** → **2 promoted to Senior**; **established** **RFC process** adopted org-wide
- **Drove** **cost optimization initiative** (rightsizing, Savings Plans, Graviton), saving **$400K/yr (35% reduction)**

### Projects (ATS-Scannable)
**Design System Platform** | TypeScript, React, Storybook, Chromatic, GitHub Actions
- Built **shared component library** (60+ components) adopted by **12 product teams**, reducing **UI dev time 40%**
- Implemented **automated visual regression testing** (Chromatic), catching **200+ UI regressions/quarter**

**Real-Time Analytics Pipeline** | Go, Kafka, ClickHouse, Kubernetes, Terraform
- Designed **stream processing pipeline** ingesting **5B events/day**, powering **customer-facing dashboards** <1s latency
```

---

### 8. Gap Analysis Triggers (For gap_analyzer.py)

```markdown
## Gap Analysis Triggers (Missing Signal Detectors)

### Missing Must-Have Keywords (ATS Gate Risk)
- No "React" / "TypeScript" / "Node.js" / "PostgreSQL" / "AWS" mentions
- No "System Design" or "Architecture" for Senior+ roles
- No "CI/CD" / "Docker" / "Kubernetes" for Senior+ roles
- No metrics/outcomes in experience bullets (pure task lists)

### Missing Strong Signals (Differentiation Risk)
- No "GraphQL" / "tRPC" / "WebSockets" for real-time roles
- No "Kubernetes" / "Terraform" / "Observability" for Staff+ roles
- No "Mentoring" / "Code Review" / "RFC" / "ADR" for Senior+ roles
- No "Cost Optimization" / "Capacity Planning" / "Disaster Recovery" for Staff+

### Seniority Mismatch Signals
- Mid-level resume with "Architected", "Led strategy", "Defined standards" (overclaim)
- Senior resume with only "Implemented", "Fixed", "Wrote tests" (undersell)
- Staff resume without cross-team / org-wide impact language

### ATS Parser Gaps
- Missing exact parser keywords for target ATS (Greenhouse/Lever/Workday/iCIMS)
- Skills listed in paragraph prose instead of scannable keyword bank
- Acronyms without expansions (e.g., "K8s" without "Kubernetes", "GQL" without "GraphQL")
```

---

### 9. Portfolio Cross-Reference Signals (For portfolio_crossref.py)

```markdown
## Portfolio Cross-Reference Signals

### Expected Portfolio Artifacts
- **GitHub**: 3+ substantial repos (full-stack apps, libraries, tools) with README, tests, CI
- **Live Demos**: 2+ deployed projects (Vercel, AWS, Fly.io, Railway) with custom domains
- **Technical Writing**: 2+ blog posts / RFCs / ADRs / conference talks on relevant topics
- **Open Source**: Meaningful contributions (not just typo fixes) to relevant projects

### Portfolio-Resume Alignment Checks
- Resume "React/TypeScript" ↔ GitHub repos use React 18 + TypeScript 5 + strict mode
- Resume "Kubernetes" ↔ Portfolio shows k8s manifests, Helm charts, or EKS/GKE clusters
- Resume "System Design" ↔ Blog post / talk / ADR documenting architecture decisions
- Resume "Mentoring" ↔ GitHub shows PR reviews, onboarding docs, or intern project repos
```

---

### 10. Role-Specific ATS Optimization Notes

```markdown
## Role-Specific ATS Optimization Notes

### Full-Stack Engineer Specific
- **Greenhouse**: Heavily weights "React", "Node.js", "TypeScript", "PostgreSQL", "AWS", "System Design"
- **Lever**: Strong on "Full Stack", "End-to-End", "Production", "Scale", "Latency"
- **Workday**: Requires exact "Amazon Web Services" (not "AWS"), "React.js" (not "React"), "Node.js"
- **iCIMS**: Clusters skills; need at least 3 from each cluster (frontend, backend, cloud, devops)
- **Taleo**: Parses "years of experience" from dates; ensure date ranges are parseable (MM/YYYY)

### Keyword Density Targets (Per 2-Page Resume)
- "React": 4-6x | "TypeScript": 4-6x | "Node.js": 3-5x | "PostgreSQL": 3-4x
- "AWS": 4-6x | "System Design": 2-3x (Senior+) | "Kubernetes": 2-3x (Senior+)
- "Mentor": 1-2x (Senior+) | "Architect": 2-3x (Staff+) | "Strategy": 1-2x (Staff+)

### Red Flags (Auto-Reject Triggers)
- "Java" without "JavaScript" / "TypeScript" confusion (parser may mismatch)
- "React Native" only when role requires "React" (web) — different skill clusters
- "SQL" without specific dialect (PostgreSQL, MySQL) — parsers want specificity
- "Cloud" without provider (AWS/GCP/Azure) — too generic for ATS
```

---

## Usage in resume-doctor Pipeline

```python
# job_analyzer.py integration point
from pathlib import Path

ROLE_LIBRARY_ROOT = Path(__file__).parent.parent / "references" / "job-descriptions"

def load_role_template(role_id: str) -> RoleTemplate:
    """Load role-specific ATS optimization data."""
    path = ROLE_LIBRARY_ROOT / f"{role_id}.md"
    # Parse YAML frontmatter + markdown sections
    return RoleTemplate.from_markdown(path)

def get_ats_keywords(role_id: str, ats_parser: str) -> list[str]:
    """Get parser-specific keyword list for target role."""
    template = load_role_template(role_id)
    return template.ats_parser_hints.get(ats_parser, template.ats_keywords)

def get_seniority_signals(role_id: str, seniority: str) -> list[str]:
    """Get seniority-specific signal keywords."""
    template = load_role_template(role_id)
    return template.seniority_signals.get(seniority, [])

def get_gap_triggers(role_id: str) -> list[GapTrigger]:
    """Get gap analysis triggers for role."""
    template = load_role_template(role_id)
    return template.gap_triggers
```

---

## Adding New Roles

1. Create folder under `references/job-descriptions/{domain}/`
2. Create `{role-name}.md` with all 10 sections above
3. Use existing role as template (copy `fullstack-engineer.md` → modify)
4. Validate YAML frontmatter parses: `python -c "import yaml; yaml.safe_load(open('role.md'))"`
5. Add role_id to `job_analyzer.py` role registry
6. Test with `resume-doctor analyze --role software-engineer/fullstack-engineer --jd "..."`

---

## Maintenance Notes

- **Update quarterly**: Refresh ATS keyword weights from latest job board scrapes
- **Version control**: Track changes in git; tag major versions (v2024.1, v2024.2)
- **ATS parser updates**: When Greenhouse/Lever/Workday/iCIMS update parsers, update keyword maps
- **Seniority calibration**: Review annually against industry leveling guides (Levels.fyi, Radford)