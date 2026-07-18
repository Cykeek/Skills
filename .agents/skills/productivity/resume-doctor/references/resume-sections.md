---
name: resume-sections
description: Section ordering, header/summary/skills/experience/education specs, and LaTeX resume format specification with signal tag taxonomy.
---

# Resume Sections — Deep Reference

This is the deep reference for structuring and writing resume sections in a recruiter-friendly and ATS-compatible way. Use this when generating, rewriting, or restructuring resumes.

---

## 1. Recommended Section Order

### Entry-Level / Student / Career Switcher
1. Header
2. Professional Summary or Targeted Objective
3. Skills
4. Projects or Relevant Experience
5. Education
6. Certifications
7. Additional Experience (optional)

### Mid-Career Professional
1. Header
2. Professional Summary
3. Skills
4. Professional Experience
5. Education
6. Certifications / Projects (if relevant)

### Senior / Executive
1. Header
2. Executive Summary
3. Core Competencies
4. Professional Experience
5. Selected Achievements / Leadership Impact
6. Education
7. Board Memberships / Publications / Certifications

---

## 2. Header Section

### Include
- Full legal/professional name.
- City + State/Country only. Do not include full street address.
- Phone number in standard format.
- Professional email address.
- LinkedIn URL.
- Portfolio/GitHub/website only if relevant.

### Avoid
- Photos/headshots.
- Personal details such as age, marital status, religion, or nationality unless required by local hiring norms.
- Icons for phone/email/location. Use plain text labels or separators.

### Example
```markdown
# Maya Chen
Seattle, WA | (555) 123-4567 | maya.chen@email.com | linkedin.com/in/mayachen | github.com/mayachen
```

---

## 3. Professional Summary

The summary should be 2-4 lines and written specifically for the target job family. It should mention role, years of experience, domain expertise, and 2-4 high-value keywords from the target job description.

### Formula
`[Role/level] with [years] experience in [domain]. Skilled in [tools/skills]. Known for [measurable outcome or operating strength].`

### Good Example
> Product Manager with 6+ years of experience launching B2B SaaS workflows across analytics, payments, and onboarding. Skilled in roadmap strategy, user research, experimentation, and cross-functional delivery. Delivered adoption gains of up to 32% by improving activation funnels and simplifying enterprise configuration flows.

### Weak Example
> Hardworking and passionate professional looking for a challenging opportunity where I can grow and contribute to the company.

---

## 4. Skills Section

The Skills section should prioritize hard skills and exact terminology from the job description. ATS systems reward precise keyword matching, but recruiters punish keyword stuffing.

### Recommended Structure
```markdown
## Skills
- **Technical Skills:** Python, SQL, React, Node.js, AWS, Docker
- **Tools:** Jira, Figma, GitHub, Tableau, Salesforce
- **Methods:** Agile, A/B Testing, User Research, CI/CD, ETL
```

### Rules
- Use categorized skills if the candidate has many skills.
- Keep skills verifiable through the Experience section.
- Do not list vague soft skills such as "team player" or "excellent communicator" unless they are supported in bullet points.

---

## 5. Experience Section

Experience bullets should be achievement-oriented, not task-oriented.

### STAR/CAR Bullet Formula
- **STAR:** Situation + Task + Action + Result.
- **CAR:** Challenge + Action + Result.

The best resume bullets usually compress this into:
`Action Verb + Scope/Context + Method/Skill + Measurable Result`

### Strong Bullet Examples
- Optimized SQL queries across 14 reporting dashboards, reducing average load time by 42% and improving analyst workflow speed.
- Led a 6-person cross-functional team to redesign onboarding, increasing trial-to-paid conversion from 18% to 27% within two quarters.
- Automated monthly reconciliation workflows using Python and Airflow, saving 22 analyst hours per month and reducing manual errors by 31%.

### Weak Bullet Examples
- Responsible for reports.
- Worked with team members on onboarding.
- Helped automate processes.

### Bullet Count Guidelines
- Current/recent roles: 4-6 bullets.
- Older roles: 2-4 bullets.
- Very old or less relevant roles: 1-2 bullets or title-only.

---

## 6. Education Section

### Include
- Degree name and major.
- University/institution name.
- Graduation year or expected graduation date.
- Honors, thesis, or relevant coursework only if early-career or highly relevant.

### Example
```markdown
## Education
### Bachelor of Science in Computer Science
University of Washington, Seattle, WA | 2021
```

---

## 7. Certifications, Projects, and Publications

### Certifications
Use when certifications are valued in the target field (e.g., PMP, AWS Certified Solutions Architect, CPA, SHRM-CP, CISSP).

### Projects
Use for early-career candidates, technical candidates, career switchers, or portfolio-driven roles.

### Publications / Speaking
Use for executive, academic, research, medical, scientific, or industry authority roles.

---

## 8. LaTeX Resume Format Specification (Overleaf pdflatex)

> **Full specification:** See `latex-resume-format.md` for complete template, macros, compilation instructions, validation gates, and anti-patterns.

### 8.1 File Structure
```
resume/
├── main.tex                              # Master LaTeX source (template from latex-resume-format.md)
├── main-{company}-{role}-{YYYYMMDD}.tex  # Tailored version per application
├── main-{company}-{role}-{YYYYMMDD}.pdf  # Submission artifact (pdflatex / Overleaf)
└── main-{company}-{role}-{YYYYMMDD}.txt  # Plain text fallback (pdftotext -layout)
```

### 8.2 Core LaTeX Structure (from `latex-resume-format.md`)

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

### 8.3 Compilation Pipeline (pdflatex only)
```bash
# Local (TeX Live)
pdflatex main.tex
pdflatex main.tex  # 2nd pass for cross-refs

# Overleaf: Set Compiler → pdfLaTeX, click Recompile

# Verify ATS extraction
pdftotext -layout main.pdf main.txt
cat main.txt
# Should read linearly: Company Date Title Location, bullets in order
```

---

## 9. Signal Tag Taxonomy (For Resume Bullets)

Controlled vocabulary — match internal signal tag taxonomy (§5):

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

**Format in bullet:** `[Data-Informed Iteration] [Cross-functional Leadership]` (space-separated, bracketed)

---

## 10. Anti-Patterns (Auto-Reject in Validation)

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Keyword density > 5% | `density_check` | Reduce, use variants |
| Same keyword 5× in one bullet | `bullet_scan` | Distribute across sections |
| Hidden text (white on white) | `pdf_inspect` | Never do this |
| Keywords only in footer/header | `section_check` | Move to body |
| Acronyms only (no spell-out) | `acronym_check` | "TypeScript (TS)" |
| Tables for skills/layout | `table_check` | Use simple list |
| "I led" / "My team" | `pronoun_check` | Third-person implicit |
| "Responsible for" / "Worked on" | `verb_check` | Tier 1/2 verb only |
| Soft skills as list items | `skills_check` | Weave into bullets as evidence |
| Progress bars / icons / emojis | `visual_check` | Remove |
| Multi-column layout | `layout_check` | Single column only |