---
name: resume-doctor
description: ATS-focused professional resume doctor. Ingests job listings (URLs/docs), extracts requirements & keyword targets, analyzes candidate profile gaps, rewrites resumes in clean Overleaf-compatible LaTeX (.tex) format, validates against ATS parser simulations via pdflatex + pdftotext (Greenhouse, Lever, Workday, iCIMS, Taleo). Outputs a single self-contained main.tex file ready for pdflatex compilation.
---

# Resume Doctor — Operating Manual

**Purpose:** Transform resumes from "task lists" into ATS-optimized, signal-rich narratives that pass electronic screening AND impress human reviewers. Every output is a single self-contained LaTeX file (`main.tex`) that compiles natively on Overleaf with `pdflatex` — no external `.cls` files, no Pandoc, no Weasyprint, no HTML/CSS pipelines.

---

## 1. Request Intake Protocol

Before any audit or rewrite, collect:

| Field | Required | Source |
|-------|----------|--------|
| **Target job URL(s)** | Yes* | User provides (Greenhouse, Lever, Workday, company careers, LinkedIn, PDF, text) |
| **Target job text** | If no URL | User pastes / uploads |
| **Current resume** | Yes | User provides (Markdown, PDF, DOCX, LinkedIn export, plain text) |
| **Candidate profile (master)** | No | User provides or agent builds from resume |
| **Target role(s)** | Yes | User states (e.g., "Senior Product Designer", "Staff Design Engineer") |
| **NDA constraints** | Yes | User states: full transparency / company-abstracted / domain-abstracted / pattern-abstracted |
| **Layout mode** | **Recommended** | User states: **`ats-max`** (dense, parser-first, legacy default) **OR** **`designer-polish`** (professional typography, visual hierarchy, designer-credible) — **both 100% ATS-compatible** |
| **Timeline** | No | User states urgency |

\* If user has no specific job yet, run **General ATS Audit** mode (no job analysis, only format/structure/keyword hygiene).

### Layout Mode Selection (Critical for Designer Roles)

The resume-doctor skill now supports **two layout modes** — both 100% ATS-compatible, differing only in visual presentation:

| Mode | Target Audience | Typography | Spacing | Signal Tags | Best For |
|------|-----------------|------------|---------|-------------|----------|
| **`ats-max`** | ATS parsers, high-volume recruiters | 1.0 line height, tight | Minimal (2pt bullets, 4pt sections) | Inline `[\textbf{Tag}]` | Backend engineers, data analysts, legacy ATS (Taleo, old Workday) |
| **`designer-polish`** | **Designers, PMs, creative leads, CEOs** | **1.15 line height, professional** | **Breathing room (4pt bullets, 14pt sections)** | **Badged `\colorbox` with padding** | **UI/UX Designers, Product Designers, Design Engineers, Creative Directors** |

**Both modes guarantee:**
- ✅ Linear ATS extraction (`pdftotext -layout` reads Company → Date → Title → Location sequentially)
- ✅ Unicode glyph mapping (`fi`/`fl`/bullets/dashes extract correctly)
- ✅ Overleaf `pdflatex` compatibility (zero external deps)
- ✅ Same macros (`\roleentry`, `\projectentry`, `\signaltag`, `\kw`, `\metric`)

**Default recommendation:**
- **Designers/PMs/Creative roles** → **`designer-polish`** (resume is a portfolio artifact)
- **Engineers/Analysts/High-volume ATS** → `ats-max` (max keyword density per page)

**Agent Action:** If user doesn't specify, **default to `designer-polish` for any design/product/creative role**.

---

**Agent Action — Discovery:**
```bash
# Agent MUST run these to find input files
Glob "**/resume*.md"
Glob "**/resume*.pdf"
Glob "**/resume*.docx"
Glob "**/job*.txt"
Glob "**/job*.pdf"
Glob "**/job*.md"
Read each found file
```

---

## 2. End-to-End Workflow (5 Phases)

```
PHASE 1: JOB ANALYSIS          → job-analysis.json
    ↓
PHASE 2: CANDIDATE INVENTORY   → candidate-profile.yaml
    ↓
PHASE 3: GAP ANALYSIS          → gap-report.md + keyword-injection-map.json
    ↓
PHASE 4: OPTIMIZATION (REWRITE)→ main-{company}-{role}-{YYYYMMDD}.tex  (LaTeX only)
    ↓
PHASE 5: VALIDATION            → validation-report.md + main-{company}-{role}-{YYYYMMDD}.pdf + main-{company}-{role}-{YYYYMMDD}.txt
```

**Agent Action — Phase Gates:**
- **After Phase 1:** Present `job-analysis.json` to user for confirmation before proceeding
- **After Phase 3:** Present `gap-report.md` + `keyword-injection-map.json` for approval before rewrite
- **After Phase 4:** Present tailored LaTeX resume for review before validation
- **After Phase 5:** Deliver final artifacts + validation report

---

## 3. Phase Details & Agent Directives

### Phase 1: Job Analysis (`job-analysis-engine.md`)

**Input:** Job URL / text / PDF  
**Output:** `job-analysis.json`

```json
{
  "source": { "type": "url|text|pdf", "value": "..." },
  "role_title": "Senior Product Designer",
  "company": "Stripe",
  "must_have": {
    "hard_skills": ["Figma", "Design Systems", "React", "TypeScript", "A/B Testing"],
    "soft_skills": ["Cross-functional Leadership", "Ambiguity Navigation"],
    "tools": ["Figma", "Jira", "Mixpanel", "Looker", "Git"],
    "domain": ["Payments", "KYC/AML", "PCI-DSS"],
    "years_experience": "5+",
    "education": "Bachelor's Design/HCI/CS or equivalent"
  },
  "nice_to_have": { ... },
  "keyword_targets": {
    "design systems": { "min": 2.0, "max": 3.5, "priority": "critical" },
    "a/b testing": { "min": 1.5, "max": 3.0, "priority": "high" },
    "stakeholder": { "min": 1.0, "max": 2.5, "priority": "high" },
    "figma": { "min": 1.5, "max": 3.0, "priority": "high" },
    "payments": { "min": 1.0, "max": 2.0, "priority": "medium" }
  },
  "ats_signals": ["Greenhouse", "Lever"],
  "company_intel": { "stage": "public", "size": "8000", "recent_launches": ["..."] }
}
```

**Agent Commands:**
```bash
# From URL
agent job analyze --url "https://boards.greenhouse.io/stripe/jobs/12345" --out job-analysis.json

# From text file
agent job analyze --text-file job-description.txt --out job-analysis.json

# From PDF
agent job analyze --pdf job-description.pdf --out job-analysis.json

# Deep company intel
agent job intel --company "Stripe" --role "Senior Product Designer" --out company-intel.json
```

---

### Phase 2: Candidate Inventory (Master Profile)

**Input:** Current resume + user conversation  
**Output:** `candidate-profile.yaml`

```yaml
name: "Maya Chen"
headline: "Senior Product Designer — FinTech & Design Systems"
total_years: 7
target_roles: ["Senior Product Designer", "Staff Product Designer"]
skills:
  hard_skills: [Figma, Design Systems, Prototyping, User Research, A/B Testing, Accessibility, Design Tokens]
  soft_skills: [Cross-functional Leadership, Stakeholder Management, Mentorship, Design Ops]
  tools: [Figma, FigJam, Jira, Linear, Mixpanel, Amplitude, Looker, Git, GitHub, Storybook, Zeroheight, Notion, Miro, Dovetail]
  domain_knowledge: [E-commerce, Marketplace, B2B SaaS, Design Systems]
  technical: [React, TypeScript, HTML/CSS, Tailwind, Storybook, Design Tokens, CI/CD, GraphQL]
experience:
  - company: "Stripe"
    role: "Senior Product Designer (Lead)"
    dates: "07/2022 – Present"
    bullets: [...]
  - company: "Airbnb"
    role: "Product Designer"
    dates: "07/2020 – 06/2022"
    bullets: [...]
education:
  - degree: "M.S. Human-Computer Interaction"
    school: "Stanford University"
    years: "2018–2020"
certifications:
  - "Certified Usability Analyst (CUA) — HFI, 2021"
  - "AWS Certified Cloud Practitioner — 2023"
projects:
  - name: "Unified Billing Dashboard"
    context: "Internal Platform"
    dates: "01/2023 – 06/2023"
    role: "Lead Designer (3D, 2E, 1PM, 1R)"
    stack: [Figma, Storybook, React, BigQuery]
    signals: ["Systems Thinking", "0→1 Ambiguity", "Cross-functional Leadership"]
```

**Agent Action:** If user provides only resume, agent extracts & structures into this schema. If user provides master profile, agent validates & enriches.

---

### Phase 3: Gap Analysis (`gap-analysis-template.md`)

**Input:** `job-analysis.json` + `candidate-profile.yaml`  
**Output:** `gap-report.md` + `keyword-injection-map.json`

**Agent Action:** Run gap analysis algorithm (see `gap-analysis-template.md` §2–§3):
1. Compare must-have hard skills, tools, domain, years, education
2. Compare keyword targets vs. current resume density
3. Score gaps: Critical > High > Medium > Low
4. Generate prioritized remediation queue
5. Generate exact keyword injection locations

**Output Example (`gap-report.md`):**
```markdown
# Gap Analysis — Maya Chen → Stripe Senior Product Designer

## Executive Summary
| Metric | Value |
|--------|-------|
| Overall Match | 78% |
| Critical Gaps | 2 |
| High Gaps | 3 |
| Est. Fix Time | 45–60 min |

## Critical Gaps (Must Fix)
| # | Category | Job Requires | Candidate Has | Remediation |
|---|----------|--------------|---------------|-------------|
| 1 | Hard Skill | **React** | ❌ Not listed | Add to Technical Skills; inject in 2 bullets |
| 2 | Keyword Density | **design systems** ≥ 2.0% | 0.8% (1 mention) | Add to Summary, Skills, 2 Experience bullets |

## Keyword Injection Map
| Keyword | Target | Current | Locations to Add |
|---------|--------|---------|------------------|
| design systems | 4 | 1 | Summary, Skills, Stripe bullet 2, Airbnb bullet 2 |
| figma | 4 | 1 | Summary, Skills, Stripe bullet 1, Airbnb bullet 1 |
| a/b testing | 3 | 0 | Summary, Skills, Stripe bullet 3 |
```

---

### Phase 4: Optimization / Rewrite (`optimization-patterns.md`, `action-verbs.md`, `writing-rules.md`, `latex-resume-format.md`)

**Input:** `candidate-profile.yaml` + `gap-report.md` + `keyword-injection-map.json`  
**Output:** `main-{company}-{role}-{YYYYMMDD}.tex` (LaTeX format per `latex-resume-format.md`)

**Agent Action — Surgical Edits (one semantic change per `Edit`):**

| Transformation | Pattern | Reference |
|----------------|---------|-----------|
| Upgrade weak verbs | "Worked on" → "Spearheaded" | `action-verbs.md` §1–6, `optimization-patterns.md` §1.2 |
| Inject keywords contextually | Add "design systems" in Summary, Skills, 2 bullets | `optimization-patterns.md` §2 |
| Calibrate density | Check each keyword 2–3% target | `optimization-patterns.md` §3 |
| Add metrics to bullets | "Led redesign" → "Led redesign: +9pp conversion (n=24k, p<0.01)" | `optimization-patterns.md` §6.1, `writing-rules.md` §2 |
| Replace soft-skill claims with evidence | "Team player" → "Collaborated with 3D/2E/1PM through weekly design reviews" | `optimization-patterns.md` §6.2 |
| Sanitize NDA projects | "Stripe" → "Series C FinTech (payments)" | `optimization-patterns.md` §6.3, `writing-rules.md` |
| Add signal tags to bullets | `\signaltag{Data-Informed Iteration} \signaltag{Cross-functional Leadership}` | `optimization-patterns.md` §1.1, `latex-resume-format.md` §4 |
| Reorder sections per role | Skills in top 1/3 for engineering/design | `optimization-patterns.md` §4, `resume-sections.md` §1 |
| **Translate jargon for HR/CEO** | "A/B testing" → "tested two versions to find what works better" | `writing-rules.md` §5, `latex-resume-format.md` §5 |
| **Add plain-language first-use** | "Design System (unified design standards)" | `writing-rules.md` §5.2, `latex-resume-format.md` §5 |
| **Lead bullets with outcome** | Outcome first, method second | `writing-rules.md` §5.3 Pattern A, `latex-resume-format.md` §5 |

**Agent Action — Apply All Optimizations (Command Pipeline):**

```bash
# 1. Upgrade all Tier 3 verbs to Tier 1/2
agent edit --resume main-stripe-pd-20240115.tex --upgrade-verbs --tier 1,2

# 2. Inject keywords per injection map (Summary, Skills, Experience bullets)
agent edit --resume main-stripe-pd-20240115.tex --inject-keywords --map keyword-injection-map.json

# 3. Add metrics to bullets missing quantification
agent edit --resume main-stripe-pd-20240115.tex --add-metrics --gap-report gap-report-stripe-pd.md

# 4. Add signal tags to all bullets (2-3 per bullet)
agent edit --resume main-stripe-pd-20240115.tex --add-signal-tags --taxonomy signals.json

# 5. Apply NDA abstraction per level
agent edit --resume main-stripe-pd-20240115.tex --nda-level pattern-abstracted

# 6. Reorder sections per role (Skills in top 1/3 for design/eng)
agent reorder --resume main-stripe-pd-20240115.tex --role design

# 7. Calibrate keyword density
agent calibrate --resume main-stripe-pd-20240115.tex --job job-analysis.json

# 8. Apply audience-aware transformations (HR/CEO/Lead readable)
agent edit --resume main-stripe-pd-20240115.tex --audience-aware --expand-acronyms --translate-jargon --lead-with-outcome --add-scale-context
```

**Agent Edit Pattern Examples (LaTeX):**
```python
# Upgrade verb
Edit(file="main.tex", old="Worked on checkout redesign", new="Spearheaded checkout redesign")

# Inject keyword in Summary
Edit(file="main.tex", old="Senior Product Designer with 7 years building FinTech products.", new="Senior Product Designer with 7 years building FinTech products. Led design systems adoption across 12 teams (87% coverage).")

# Add metric to bullet
Edit(file="main.tex", old="\item Spearheaded checkout redesign for 15M+ merchants delivering +9pp activation", new="\item Spearheaded checkout redesign for \metric{15+ million merchants (payment processing scale)} delivering \metric{+9pp activation (18\%\rightarrow27\%)}, \metric{\$460K ARR retained}; validated via A/B test (n=24,847, p<0.01) \signaltag{Data-Informed Iteration}")

# Add signal tag
Edit(file="main.tex", old="\item Spearheaded checkout redesign...", new="\item Spearheaded checkout redesign... \signaltag{Data-Informed Iteration} \signaltag{Cross-functional Leadership}")

# Translate jargon inline (first use) — Audience-Aware
Edit(file="main.tex", old="\item Validated via A/B test (n=24,847, p<0.01)", new="\item Validated via \kw{A/B testing (tested two versions to find what works better; n=24,847, statistically significant p<0.01)}")

# Expand acronym at first use — Audience-Aware
Edit(file="main.tex", old="\item Championed WCAG 2.2 AA compliance", new="\item Championed \kw{WCAG 2.2 AA (accessibility standard, level AA)} compliance")

# Lead with business outcome — Audience-Aware
Edit(file="main.tex", old="\item \textbf{Architected} Design System v2 token architecture: 12 teams, 87% UI coverage, 0 breaking changes in 18mo", new="\item \textbf{Built} unified design standards (Design System v2) adopted by \metric{12 cross-functional product teams} covering \metric{87\%} of product UI — \textbf{zero breaking changes in 18 months} \signaltag{Systems Thinking} \signaltag{Technical Fluency}")

# Add scale context for non-domain experts — Audience-Aware
Edit(file="main.tex", old="\item Led checkout redesign for 15M+ merchants", new="\item Led checkout redesign for \metric{15+ million merchants (payment processing scale)}")
```

**Audience-Aware Transformation Rules (from `writing-rules.md` §5 & `optimization-patterns.md` §6.4):**
- **Lead with outcome:** Every bullet opens with business impact ($, %, users, risk reduction, speed)
- **Translate first use:** Acronyms and jargon expanded inline at first mention per bullet/section
- **Contextualize scale:** "12 teams" → "12 cross-functional product teams"; "15M+" → "15+ million merchants (payment processing scale)"
- **Summary = 80% plain, 20% technical:** CEO/HR reads this first
- **Skills = exact technical terms:** ATS needs precise keywords
- **Experience = 50/50 balance:** Lead with outcome, include method
- **Never assume domain knowledge:** "PCI-DSS (payment security standard)" not just "PCI-DSS"

---

### Phase 5: Validation & Build (`validation-checklist.md`, `ats-compliance.md`, `optimization-patterns.md`, `latex-resume-format.md`)

**Input:** Tailored resume `main.tex` + `job-analysis.json`  
**Output:** `validation-report.md` + `main.pdf` (pdflatex) + `main.txt` (pdftotext)

**Agent Action — Run All Gates:**

```bash
# 1. LaTeX format compliance (hard gates)
agent validate latex-format --resume main.tex
# Checks: single-column article class, no tabularx/tables, no TikZ/pictures, cmap+glyphtounicode present, microtype, geometry margins

# 2. Keyword density (on extracted text)
agent validate density --resume main.tex --job job-analysis.json
# Extract text via pdflatex → pdf → pdftotext, check each keyword within [min, max] band

# 3. ATS parser simulation (pdflatex → pdftotext → parser rules)
agent validate parsers --resume main.tex --parsers greenhouse,lever,workday,icims,taleo
# Generates: main.txt per parser, extracts skills/sections, flags parsing errors

# 3b. ATS Unicode extraction gate (critical for pdflatex)
agent validate unicode-extraction --resume main.tex
# pdftotext -layout main.pdf main.txt → verify ligatures (fi, fl, ffi), bullets (•), dashes (–, —) map to correct Unicode

# 4. Readability (general, on extracted text)
agent validate readability --resume main.tex
# Flesch-Kincaid ≤ 12, avg sentence ≤ 20 words, active voice ≥ 80%, zero passive

# 5. Audience Comprehension Gates (NEW — from validation-checklist.md §5)
agent validate audience --resume main.tex --job job-analysis.json
# Per-bullet: HR keywords ✓, CEO outcome ($/%) ✓, Manager scope (team/budget) ✓, Lead proof (tools/n/p) ✓
# FK Grade ≤ 10 (stricter), avg sentence ≤ 18, active voice ≥ 85%, zero passive
# 100% acronyms expanded first use, ≥80% jargon translated inline, 100% numbers contextualized
# Summary: non-specialist readable in 15s, 2-3 business outcomes, no unexplained acronyms

# 6. Build artifacts (pdflatex only)
agent build --resume main.tex --engine pdflatex
# Runs: pdflatex -interaction=nonstopmode -halt-on-error main.tex (2-3 passes for refs)
# Generates: main.pdf (submission), main.txt (pdftotext -layout fallback)
```

**Validation Report (`validation-report.md`):**
```markdown
# Validation Report — main.tex (Stripe Senior Product Designer)

## LaTeX Format Gates ✅ PASS
- [x] article class, 10.5pt, a4paper
- [x] geometry margins: top=1.6cm, bottom=1.6cm, left=1.8cm, right=1.8cm
- [x] cmap + glyphtounicode + pdfgentounicode=1 before font loading
- [x] microtype enabled
- [x] No tabularx / tables / TikZ / images
- [x] Single-column, linear flow (ATS-safe)

## Keyword Density ✅ PASS
| Keyword | Target | Actual | Status |
|---------|--------|--------|--------|
| design systems | 2.0–3.5% | 2.1% | ✅ |
| figma | 1.5–3.0% | 1.8% | ✅ |
| a/b testing | 1.5–3.0% | 2.2% | ✅ |

## Parser Simulation (pdflatex → pdftotext -layout)
| Parser | Skills Extracted | Sections Found | Issues |
|--------|------------------|----------------|--------|
| Greenhouse | 28/30 | 6/6 | None |
| Lever | 27/30 | 6/6 | None |
| Workday | 25/30 | 5/6 | "Projects" section missed |
| iCIMS | 29/30 | 6/6 | None |
| Taleo | 26/30 | 6/6 | "Certifications" header variant |

**Verdict:** PASS (Core sections ✅ across all parsers)

## Unicode Extraction Gate ✅ PASS
| Glyph | Extracted As | Status |
|-------|--------------|--------|
| fi / fl / ffi | fi / fl / ffi | ✅ |
| • (bullet) | • | ✅ |
| – (en-dash) | – | ✅ |
| — (em-dash) | — | ✅ |

## Readability ✅ PASS
| Metric | Threshold | Actual | Status |
|--------|-----------|--------|--------|
| Flesch-Kincaid Grade | ≤ 12 | 11.2 | ✅ |
| Avg Sentence Length | ≤ 20 | 17.4 | ✅ |
| Active Voice | ≥ 80% | 87% | ✅ |
| Passive Constructions | 0 | 0 | ✅ |

## Audience Comprehension Gates ✅ PASS (NEW)
| Check | Threshold | Actual | Status |
|-------|-----------|--------|--------|
| Per-bullet: HR keywords | 1-2 per bullet | ✅ All bullets | ✅ |
| Per-bullet: CEO outcome ($/%) | 1 per bullet | ✅ All bullets | ✅ |
| Per-bullet: Manager scope | 1 per bullet | ✅ All bullets | ✅ |
| Per-bullet: Lead proof | 1 per bullet | ✅ All bullets | ✅ |
| Flesch-Kincaid Grade | ≤ 10 | 9.8 | ✅ |
| Avg Sentence Length | ≤ 18 | 16.2 | ✅ |
| Active Voice | ≥ 85% | 89% | ✅ |
| Passive Constructions | 0 | 0 | ✅ |
| First-use acronym expanded | 100% | 100% | ✅ |
| Jargon translated inline | ≥ 80% | 87% | ✅ |
| Numbers contextualized | 100% | 100% | ✅ |
| Summary: 15s non-specialist read | ✅ | ✅ | ✅ |
| Summary: 2-3 business outcomes | 2+ | 3 | ✅ |
| Summary: no unexplained acronyms | 0 | 0 | ✅ |

## Artifacts Generated
- `main.pdf` — **Single submission artifact** (pdflatex, Overleaf-compatible)
- `main.txt` — Plain text fallback (pdftotext -layout)
```

---

## 4. Reference Routing Table

| User Query Contains… | Primary Reference | Secondary |
|----------------------|-------------------|-----------|
| "job description", "JD", "job url", "analyze job", "extract keywords" | `job-analysis-engine.md` | `gap-analysis-template.md` |
| "gap", "missing", "what do I need", "compare", "keyword target" | `gap-analysis-template.md` | `job-analysis-engine.md` |
| "rewrite", "optimize", "bullet", "verb", "inject keyword", "density" | `optimization-patterns.md` | `action-verbs.md`, `writing-rules.md` |
| "format", "ATS", "parser", "PDF", "parse", "compliance" | `ats-compliance.md` | `optimization-patterns.md` §5, `validation-checklist.md` |
| "section", "structure", "order", "header", "summary", "skills" | `resume-sections.md` | `optimization-patterns.md` §4 |
| "verb", "action verb", "replace verb" | `action-verbs.md` | `optimization-patterns.md` §1 |
| "tone", "pronoun", "passive", "acronym", "number format" | `writing-rules.md` | `optimization-patterns.md` §6 |
| "latex", "tex", "overleaf", "pdflatex", "compile", "main.tex" | `latex-resume-format.md` | `resume-sections.md`, `validation-checklist.md` |
| "validate", "check", "gate", "pre-submission", "readability", "density" | `validation-checklist.md` | `ats-compliance.md`, `optimization-patterns.md` §5 |
| "company intel", "company research", "culture", "compensation", "interview process" | `job-analysis-engine.md` §5 | — |

---

## 5. Resume Format Specification (LaTeX — Overleaf pdflatex)

> **Full specification:** See `latex-resume-format.md` for complete LaTeX template, macros, compilation instructions, validation gates, and anti-patterns.

### 5.1 File Structure
```
resume/
├── main.tex                              # Master LaTeX source (template from latex-resume-format.md)
├── main-{company}-{role}-{YYYYMMDD}.tex  # Tailored version per application
├── main-{company}-{role}-{YYYYMMDD}.pdf  # Submission artifact (pdflatex / Overleaf)
└── main-{company}-{role}-{YYYYMMDD}.txt  # Plain text fallback (pdftotext -layout)
```

### 5.2 Core LaTeX Structure (from `latex-resume-format.md`)

**Preamble (required order — engine-safe glyph mapping):**
```latex
\documentclass[10.5pt, a4paper]{article}
\usepackage{ifpdf}
\ifpdf
  \usepackage{cmap}
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[a4paper, top=1.6cm, bottom=1.6cm, left=1.8cm, right=1.8cm]{geometry}
\usepackage{parskip}
\usepackage{microtype}
\usepackage{mathptmx}
\usepackage{xcolor}
\definecolor{textmain}{gray}{0.10}
\definecolor{muted}{gray}{0.40}
\definecolor{rulecolor}{gray}{0.75}
\definecolor{linkcolor}{RGB}{30, 90, 180}
\definecolor{signalcolor}{RGB}{15, 82, 186}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\titleformat{\section}{\normalfont\fontsize{9pt}{11pt}\selectfont\bfseries\color{muted}\scshape}{}{0em}{}[\vspace{1pt}{\color{rulecolor}\hrule height 0.4pt}\vspace{4pt}]
\titlespacing{\section}{0pt}{8pt}{4pt}
\usepackage{enumitem}
\setlist[itemize]{label={\small\textbullet}, leftmargin=1.2em, itemsep=2pt, parsep=0pt, topsep=2pt}
```

**Custom Macros:**
```latex
\newcommand{\roleentry}[4]{%  Company, Location, Role, Date
  \vspace{4pt}\noindent \textbf{#1} \hfill {\small\color{muted} #2} \par
  \vspace{-1pt}\noindent {\small\itshape #3} \hfill {\small\color{muted}\itshape #4} \par \vspace{2pt}}
\newcommand{\projectentry}[4]{%  Name, Context, Role, Stack
  \vspace{3pt}\noindent \textbf{#1} \hfill {\small\color{muted} #2} \par
  \vspace{-1pt}\noindent {\small\itshape #3} \hfill {\small\color{muted}\itshape #4} \par \vspace{1pt}}
\newcommand{\signaltag}[1]{\textcolor{signalcolor}{[\textbf{#1}]}}
\newcommand{\kw}[1]{\textbf{#1}}
\newcommand{\metric}[1]{\textcolor{textmain}{\textbf{#1}}}
\newcommand{\company}[1]{\textbf{#1}}
\newcommand{\role}[1]{{\itshape #1}}
\newcommand{\location}[1]{{\small\color{muted}\itshape #1}}
\newcommand{\dates}[1]{{\small\color{muted} #1}}
\newcommand{\divider}{\vspace{4pt}\noindent{\color{rulecolor}\hrule height 0.4pt}\vspace{4pt}}
\newcommand{\contactline}[1]{\noindent {\small\color{muted} #1} \par \vspace{2pt}}
```

**Body (required order):**
```latex
\begin{document}
\pagecolor{white}\color{textmain}
\begin{center}{\LARGE \textbf{Full Name}} \\[4pt] {\large Target Role — Domain} \\[6pt]\end{center}
\contactline{City, State | +1 555 123 4567 | email@domain.com | linkedin.com/in/username | github.com/username}
\divider
\section*{Professional Summary} ... \divider
\section*{Skills} ... \divider
\section*{Professional Experience} ... \divider
\section*{Education} ... \divider
\section*{Certifications} ... \divider
\section*{Selected Projects} ... \divider
\section*{Signals Demonstrated} ...
\end{document}
```

### 5.3 Compilation Pipeline (pdflatex only)
```bash
# Local (TeX Live)
pdflatex main.tex
pdflatex main.tex  # 2nd pass for cross-refs

# Overleaf: Set Compiler → pdfLaTeX, click Recompile

# Verify ATS extraction
pdftotext -layout main.pdf main.txt
cat main.txt
```

---

## 6. Signal Tag Taxonomy (For Resume Bullets)

Controlled vocabulary — match internal signal tag taxonomy (§6):

| Signal ID | Display | Use When Bullet Shows… |
|-----------|---------|------------------------|
| `data-informed-iteration` | **Data-Informed Iteration** | A/B test, analytics, telemetry, metric-driven decision |
| `cross-functional-leadership` | **Cross-functional Leadership** | Led rituals, resolved conflicts, co-authored specs with PM/Eng |
| `systems-thinking` | **Systems Thinking** | Design system, component library, tokens, governance, migration |
| `technical-fluency` | **Technical Fluency** | Code (React, TS), prototypes in Storybook, eng collaboration |
| `zero-to-one-ambiguity` | **0→1 Ambiguity** | Defined problem, strategy from scratch, shipped v1 |
| `user-research-rigor` | **User Research Rigor** | Interviews, usability tests, JTBD, synthesis → decisions |
| `strategic-influence` | **Strategic Influence** | Roadmap change, budget secured, exec memo, org process change |
| `craft-polish` | **Craft & Polish** | Motion specs, edge cases, pixel-perfect, design QA |
| `mentorship-culture` | **Mentorship & Culture** | Mentees promoted, rituals created, hiring panels |
| `accessibility-advocacy` | **Accessibility Advocacy** | WCAG audit, inclusive patterns, training, bug reduction |

**Format in bullet (LaTeX):** `\signaltag{Data-Informed Iteration} \signaltag{Cross-functional Leadership}` (space-separated, macro-wrapped)

---

## 7. Anti-Patterns (Auto-Reject in Validation)

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Keyword density > 5% | `density_check` | Reduce, use variants |
| Same keyword 5× in one bullet | `bullet_scan` | Distribute across sections |
| Hidden text (white on white) | `pdf_inspect` | Never do this |
| Keywords only in footer/header | `section_check` | Move to body |
| Acronyms only (no spell-out) | `acronym_check` | "TypeScript (TS)" |
| **Tables for skills/layout (`tabularx`/`tabular`)** | `latex_table_check` | Use `\roleentry` + `\hfill` linear flow |
| "I led" / "My team" | `pronoun_check` | Third-person implicit |
| "Responsible for" / "Worked on" | `verb_check` | Tier 1/2 verb only |
| Soft skills as list items | `skills_check` | Weave into bullets as evidence |
| Progress bars / icons / emojis | `visual_check` | Remove |
| Multi-column layout | `layout_check` | Single column only |
| **Custom `.cls` file / `\documentclass{myresume}`** | `latex_class_check` | Use `article` class only |
| **`fontspec` / XeLaTeX / LuaLaTeX** | `latex_engine_check` | Use `pdflatex` + `mathptmx` only |
| **Missing `cmap`/`glyphtounicode`** | `latex_unicode_check` | Wrap in `\ifpdf` guard; add before font packages |
| **Unconditional `\input{glyphtounicode}`** | `latex_engine_check` | Wrap in `\ifpdf` ... `\fi` — breaks XeLaTeX/LuaLaTeX |
| **Colored link boxes (missing `hidelinks`)** | `latex_hyperref_check` | `\usepackage[hidelinks]{hyperref}` |
| **Text in header/footer (`fancyhdr`)** | `latex_header_check` | Contact in body via `\contactline` |

---

## 8. Versioning & Naming Strategy (LaTeX)

| Scenario | Action |
|----------|--------|
| New job application | Copy `main.tex` → `main-{company}-{role}-{YYYYMMDD}.tex`, tailor |
| Master update | Edit `main.tex`, regenerate all tailored versions |
| Quarterly refresh | Update metrics, add projects, refresh keyword taxonomies |
| Archive | `git tag resume-v{YYYYMMDD}` |

**Naming:** `main-{company}-{role}-{YYYYMMDD}.tex`  
Example: `main-stripe-senior-product-designer-20240115.tex`

**Artifacts per application:**
```
resume/
├── main.tex                                    # Master LaTeX source
├── main-stripe-senior-product-designer-20240115.tex  # Tailored LaTeX
├── main-stripe-senior-product-designer-20240115.pdf  # Submission (pdflatex)
└── main-stripe-senior-product-designer-20240115.txt  # Fallback (pdftotext)
```

---

## 9. Agent Commands Quick Reference (LaTeX)

```bash
# PHASE 1: Job Analysis
agent job analyze --url "https://..." --out job-analysis.json
agent job analyze --text-file jd.txt --out job-analysis.json
agent job analyze --pdf jd.pdf --out job-analysis.json
agent job intel --company "Stripe" --role "Senior Product Designer" --out company-intel.json

# PHASE 2: Candidate Profile
agent profile build --resume main.tex --out candidate-profile.yaml
agent profile enrich --profile candidate-profile.yaml --interactive

# PHASE 3: Gap Analysis
agent gap analyze --job job-analysis.json --candidate candidate-profile.yaml --out gap-report.md
agent gap keywords --job job-analysis.json --resume main.tex --out keyword-report.md

# PHASE 4: Optimization (LaTeX)
agent latex build --master main.tex --job job-analysis.json --gap gap-report.md --layout-mode designer-polish --out main-stripe-pd-20240115.tex
agent latex inject --file main-stripe-pd-20240115.tex --bullet 3 --keyword "design systems" --after "Spearheaded"
agent latex verb --file main-stripe-pd-20240115.tex --bullet 2 --from "Worked on" --to "Spearheaded"
agent latex metric --file main-stripe-pd-20240115.tex --bullet 1 --append "+9pp (n=24,847, p<0.01)"
agent latex signal --file main-stripe-pd-20240115.tex --bullet 1 --tags "Data-Informed Iteration,Cross-functional Leadership"
agent latex nda --file main-stripe-pd-20240115.tex --level pattern-abstracted
agent latex audience --file main-stripe-pd-20240115.tex --expand-acronyms --translate-jargon --lead-with-outcome --add-scale-context

# PHASE 5: Validation & Build (LaTeX)
> **Full validation gates:** See `validation-checklist.md` and `latex-resume-format.md` §7
agent validate latex-format --resume main-stripe-pd-20240115.tex
agent validate density --resume main-stripe-pd-20240115.tex --job job-analysis.json
agent validate parsers --resume main-stripe-pd-20240115.tex --parsers all
agent validate unicode-extraction --resume main-stripe-pd-20240115.tex
agent validate readability --resume main-stripe-pd-20240115.tex
agent validate audience --resume main-stripe-pd-20240115.tex --job job-analysis.json
agent build --resume main-stripe-pd-20240115.tex --engine pdflatex
# Runs: pdflatex -interaction=nonstopmode -halt-on-error main.tex (2-3 passes)
# Generates: main.pdf (submission), main.txt (pdftotext -layout fallback)
```

---

## 10. Do's and Don'ts (Guardrails)

### DO
- ✅ Read all input files before any edit
- ✅ Present `job-analysis.json` for confirmation before gap analysis
- ✅ Present `gap-report.md` + `keyword-injection-map.json` for approval before rewrite
- ✅ One semantic change per `Edit` call
- ✅ Use Tier 1/2 verbs only (zero Tier 3)
- ✅ Every bullet: verb + scope + method + metric + signal tag(s)
- ✅ Spell out acronyms at least once: "TypeScript (TS)"
- ✅ Target 2–3% keyword density per critical term
- ✅ **Single-column, no tables, no TikZ/images, article class only**
- ✅ **`cmap` + `glyphtounicode` + `\pdfgentounicode=1` before font packages**
- ✅ **Verify ATS extraction: `pdflatex → pdftotext -layout` reads linearly**
- ✅ Validate against all 5 parsers before declaring done
- ✅ Respect NDA: use abstraction ladder from `optimization-patterns.md` §6.3
- ✅ **Lead every bullet with business outcome ($, %, users, risk, speed) — Audience Comprehension**
- ✅ **Expand acronyms & translate jargon at first use per bullet — Audience Comprehension**
- ✅ **Contextualize scale: "12 teams" → "12 cross-functional product teams" — Audience Comprehension**
- ✅ **Pass Audience Comprehension Gates: FK ≤ 10, sentence ≤ 18 words, 100% acronyms expanded, ≥80% jargon translated — Audience Comprehension**

### DON'T
- ❌ Edit without reading first
- ❌ Skip phase gates (no approval → no next phase)
- ❌ Invent metrics — use "~", "≈", "directional", or "per NDA"
- ❌ Use "Responsible for", "Worked on", "Helped with", "Assisted"
- ❌ List soft skills in Skills section
- ❌ Use first-person pronouns ("I", "my", "we", "our")
- ❌ **Multi-column layouts, text boxes, `tabularx`/`tabular`, TikZ, graphics, custom `.cls` files**
- ❌ Hidden text, white-on-white, keyword stuffing
- ❌ Acronyms without expansion
- ❌ **Use `fontspec`, XeLaTeX, LuaLaTeX — `pdflatex` + `mathptmx` only for Overleaf compatibility**
- ❌ **Omit `cmap`/`glyphtounicode` — breaks Unicode extraction (fi→fi, •→•)**
- ❌ Output DOCX/RTF/HTML/Markdown — **single `main.tex` source + PDF/TXT artifacts only**
- ❌ Assume domain knowledge — never use bare acronyms (PCI-DSS, JWT, CI/CD) without first-use expansion — Audience Comprehension
- ❌ Lead with method instead of outcome — HR/CEO must see business value first — Audience Comprehension
- ❌ Use bare numbers without context ("12 teams" vs "12 cross-functional product teams") — Audience Comprehension
- ❌ Skip Audience Comprehension Gates — resume must pass HR/CEO/Manager/Lead readability — Audience Comprehension