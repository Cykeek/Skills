---
name: latex-resume-format
description: Overleaf-compatible pdflatex executive LaTeX resume template with ATS-safe linear text extraction, Unicode glyph mapping, and audience-aware signal highlighting.
---

# LaTeX Resume Format — Overleaf Executive Template

**Purpose:** Single source-of-truth LaTeX (`.tex`) format for resume output. Compiles natively on Overleaf with `pdflatex` — no external `.cls` files, no Pandoc, no Weasyprint, no HTML/CSS pipelines.

---

## 1. Design Principles

| Principle | Implementation |
|-----------|----------------|
| **ATS Linear Extraction** | `\hfill`-based paragraph alignment (no `tabularx`/tables) so `pdftotext -layout` reads Company → Date → Title → Location sequentially |
| **Unicode Glyph Mapping** | `\usepackage{iftex} + \ifpdf \usepackage{cmap} \input{glyphtounicode} \pdfgentounicode=1 \fi + \usepackage[T1]{fontenc} + \usepackage[utf8]{inputenc}` before font loading — ligatures (`fi`, `fl`, `ffi`) and bullets map to correct Unicode |
| **Zero Dependencies** | Standard TeX Live packages only: `article`, `geometry`, `titlesec`, `enumitem`, `hyperref`, `xcolor`, `microtype`, `iftex`, `textcomp`, `tgheros` |
| **Audience Signal Highlighting** | `\signaltag{Tag}` macro renders as colored badge for CEOs/Leads, extracts as plain text `[Tag]` for HR keyword scanners |
| **Single-File Output** | One `main.tex` — self-contained, version-controlled, diffable |
| **Dual Layout Modes** | **`ats-max`** (dense, keyword-heavy, parser-first) **OR** **`designer-polish`** (professional typography, visual hierarchy, designer-credible) — both 100% ATS-compatible |
| **PDF Metadata Injection** | `\hypersetup` auto-populated from candidate profile + job analysis: `pdfauthor`, `pdftitle`, `pdfsubject`, `pdfkeywords` |

---

## 2. Layout Mode Selection

Add **one line** at the very top of your `main.tex` (before `\documentclass`) to select mode:

```latex
% MODE SELECTION — uncomment exactly ONE:
%\def\resumemode{ats-max}        % Dense, keyword-packed, parser-first (legacy default)
\def\resumemode{designer-polish} % Professional typography, visual hierarchy, designer-credible
```

**Both modes guarantee:**
- ✅ 100% linear ATS extraction (`pdftotext -layout` reads sequentially)
- ✅ Unicode glyph mapping (`fi`/`fl`/bullets/dashes extract correctly)
- ✅ Overleaf `pdflatex` compatibility (zero external dependencies)
- ✅ Same macros (`\roleentry`, `\projectentry`, `\signaltag`, `\kw`, `\metric`)

**Mode differences:**

| Aspect | `ats-max` | `designer-polish` |
|--------|-----------|-------------------|
| Line height | 1.0 (cramped) | **1.14** (professional) |
| Section spacing | 4pt/8pt tight | **10pt/4pt** breathing room |
| Bullet `itemsep` | 2pt | **3pt** |
| Bullet `parsep` | 0pt | **1pt** |
| Header rule weight | 0.4pt | **0.4pt** |
| Signal tag render | `[\textbf{Tag}]` inline | **No badge** — ATS-visible inline bracket only |
| Page margins | 1.65cm/1.8cm | **1.65cm/1.65cm** (symmetric) |
| Font size | 10pt | **10pt** (same) |
| Font family | `mathptmx` (Times) | **`tgheros`** (Helvetica-clone, sans-serif) |
| Skills position | After Experience | **After Projects** (per design role convention) |
| Color palette | Monochrome grays | **Dark charcoal monochrome** (`#1A1A2E`, `#404050`, `#4A4A5A`) |

---

## 3. Complete `main.tex` Template (Dual-Mode)

```latex
% ============================================================
% MODE SELECTION — uncomment exactly ONE:
% ============================================================
%\def\resumemode{ats-max}        % Dense, keyword-packed, parser-first
\def\resumemode{designer-polish} % Professional typography, visual hierarchy
% ============================================================

\documentclass[10pt,a4paper]{article}

% ── Engine Detection & Encoding Compatibility (Zero Warnings across engines) ──
\usepackage{iftex}
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage[utf8]{inputenc}

\ifpdf
  \usepackage{cmap}
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi

% ── Zero-Warning Line Breaking & Overflow Protection ──
\emergencystretch=1.5em
\linespread{1.14}\selectfont

% ── Geometry ──
\usepackage[margin=0.65in]{geometry}

% ── Digital Sans-Serif Typography (Clean Neo-Grotesque / Helvetica Clone) ──
\usepackage[scale=0.92]{tgheros}
\renewcommand{\familydefault}{\sfdefault}

% ── Microtype (protrusion, expansion, kerning) ──
\usepackage{microtype}

% ── Enumitem for bullet lists ──
\usepackage{enumitem}

% ── Colors ──
\usepackage{xcolor}

% ── Dark Charcoal Monochrome Palette ──
\definecolor{linkcolor}{HTML}{1A1A2E}
\definecolor{rulecolor}{HTML}{404050}
\definecolor{mutedcolor}{HTML}{4A4A5A}

% ── Hyperref with PDF Metadata Injection (auto-populated by agent) ──
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  urlcolor=linkcolor,
  linkcolor=linkcolor,
  citecolor=linkcolor,
  pdftitle={Candidate Name — Target Role},   % ← populated by agent from job-analysis.json
  pdfauthor={Candidate Name},                 % ← populated by agent from candidate-profile.yaml
  pdfsubject={Tailored resume for Target Role at Company}, % ← populated by agent
  pdfkeywords={kw1, kw2, kw3, kw4}            % ← populated by agent from job-analysis.json keyword_targets
}

% ── Section Heading Styling (Uppercase with clean 0.4pt divider anchor) ──
% CRITICAL: \MakeUppercase in 5th argument (not 4th) to avoid uppercasing color names
\usepackage{titlesec}
\titleformat{\section}
  {\normalfont\fontsize{10pt}{12pt}\selectfont\bfseries}
  {}{0em}{\MakeUppercase}
  [\vspace{2pt}{\color{rulecolor}\hrule height 0.4pt}\vspace{4pt}]
\titlespacing{\section}{0pt}{10pt}{4pt}

% ── Candidate Variables (ATS-safe macro names, no @ catcode issues) ──
\newcommand{\name}[1]{\def\resumename{#1}}
\newcommand{\headline}[1]{\def\resumeheadline{#1}}
\newcommand{\email}[1]{\def\resumeemail{#1}}
\newcommand{\phone}[1]{\def\resumephone{#1}}
\newcommand{\linkedin}[1]{\def\resumelinkedin{#1}}
\newcommand{\portfolio}[1]{\def\resumeportfolio{#1}}
\newcommand{\location}[1]{\def\resumelocation{#1}}

% ── Skills Keyword Helper (Normal weight to let bold category heads pop) ──
\newcommand{\kw}[1]{#1}
\newcommand{\metric}[1]{\textbf{#1}}
\newcommand{\signaltag}[1]{}  % No-op in designer-polish; ATS-visible inline in ats-max

% ── Contact Line (single line, pipe-separated, hyperlinked) ──
\newcommand{\contactline}{%
  \resumelocation \textbar\ \resumephone \textbar\ \href{mailto:\resumeemail}{\resumeemail} \textbar\ \href{https://\resumelinkedin}{\resumelinkedin} \textbar\ \href{https://\resumeportfolio}{\resumeportfolio}
}

% ── Hierarchical Role Entry: Line 1: Company (Bold) | Dates; Line 2: Role (Italic) | Location ──
\newcommand{\roleentry}[5]{%
  \vspace{3pt}%
  \noindent \textbf{#1} \hfill {\small\color{mutedcolor}#4} \par
  \vspace{-1.5pt}%
  \noindent {\itshape #2} \hfill {\small\color{mutedcolor}\itshape #3} \par
  \vspace{1.5pt}%
  \begin{itemize}[leftmargin=1.3em,topsep=2pt,itemsep=3pt,parsep=1pt]#5\end{itemize}%
}

\newcommand{\bulletitem}[1]{\item #1}

% ── Hierarchical Project Entry: Line 1: Project (Bold) | Domain; Line 2: Tech Stack (Italic) ──
\newcommand{\projectentry}[5]{%
  \vspace{3pt}%
  \noindent \textbf{#1} \hfill {\small\color{mutedcolor}#3} \par
  \vspace{-1.5pt}%
  \noindent {\small\itshape #2} \hfill {\small\color{mutedcolor}\itshape #4} \par
  \vspace{1.5pt}%
  \begin{itemize}[leftmargin=1.3em,topsep=2pt,itemsep=3pt,parsep=1pt]#5\end{itemize}%
}

% ── Education Entry: 2-line rhythm (Degree | Date / Institution | Location) ──
\newcommand{\eduentry}[4]{%
  \vspace{2pt}%
  \noindent \textbf{#1}, #2 \hfill {\small\color{mutedcolor}#3} \par
  \vspace{1.5pt}%
}

% ── Certification Entry: 2-line rhythm (Cert Name | Date / Issuer | Detail) ──
\newcommand{\certentry}[4]{%
  \vspace{2pt}%
  \noindent \textbf{#1}, #2 \hfill {\small\color{mutedcolor}#3} \par
  \vspace{1.5pt}%
}

% ── Document ──
\begin{document}

\begin{center}
{\fontsize{18pt}{22pt}\selectfont \textbf{\resumename}}\\[3pt]
{\fontsize{10.5pt}{13pt}\selectfont \color{mutedcolor} \resumeheadline}\\[4pt]
\contactline
\end{center}

\vspace{2pt}

% ── PROFESSIONAL SUMMARY ──
% TEMPLATE: 3-sentence plain paragraph (no macros in last sentence)
% 1. [Role] with [years] experience in [domains].
% 2. [Method/skills] — [1-2 metrics with scale context].
% 3. [Passion/values — plain language, no macros].
\section*{Professional Summary}
UI/UX Designer with 2+ years experience crafting web and mobile interfaces for B2B SaaS, EdTech, and developer tooling. Turn complex workflows into accessible, user-centered designs using Figma, prototyping, and design system thinking. Deliver across agile teams with clean handoff and iterative refinement.

% ── WORK EXPERIENCE ──
\section*{Work Experience}
\roleentry{Company Name}{Role Title}{Location}{MM/YYYY – MM/YYYY}{
\bulletitem{Lead with outcome metric. Describe scope, method, and tooling. \signaltag{Signal Tag}}
\bulletitem{Second bullet with quantified impact and validation cite. \signaltag{Another Tag}}
}

% ── EDUCATION ──
\section*{Education}
\eduentry{Degree Name}{Institution, City}{MM/YYYY – MM/YYYY}{}
\eduentry{Degree Name}{Institution, City}{MM/YYYY – MM/YYYY}{}

% ── CERTIFICATIONS ──
\section*{Certifications}
\certentry{Certification Name}{Issuer}{MM/YYYY}{}

% ── SELECTED PROJECTS ──
\section*{Projects}
\projectentry{Project Name}{Tech Stack: Tools}{Domain}{YYYY}{
\bulletitem{Outcome metric + method + validation. \signaltag{Signal Tag}}
\bulletitem{Second bullet with scale context. \signaltag{Another Tag}}
}

% ── SKILLS (designer-polish mode: after Projects) ──
\section*{Skills}
\begin{itemize}[leftmargin=1.3em,topsep=3pt,itemsep=2.5pt]
\item \textbf{Design:} \kw{Wireframing \& Prototyping}, \kw{Interaction Design}, \kw{Visual Design}, \kw{Information Architecture}, \kw{Usability Testing}, \kw{User Research (JTBD, Surveys, Interviews)}, \kw{Customer Journey Maps}
\item \textbf{Systems:} \kw{Design Systems \& Tokens}, \kw{Storybook}, \kw{Figma DevMode}, \kw{Component Libraries}, \kw{Design Tokens}, \kw{Zeroheight}
\item \textbf{Technical:} \kw{HTML}, \kw{CSS}, \kw{React}, \kw{Tailwind}, \kw{GitHub}
\item \textbf{Analytics:} \kw{A/B Testing}, \kw{Mixpanel}, \kw{Amplitude}, \kw{Hotjar}, \kw{Conversion Optimization}, \kw{Retention Design}
\item \textbf{Accessibility:} \kw{WCAG 2.2 AA Audit}, \kw{axe-core}, \kw{78\% fewer violations}
\item \textbf{Tools:} \kw{Figma}, \kw{Miro}, \kw{Linear}, \kw{AI Tools}, \kw{Vibe-Coding}
\item \textbf{Domains:} \kw{B2B SaaS}, \kw{EdTech}, \kw{Energy/Utilities}, \kw{Dev Tools}, \kw{Mobile App Design}, \kw{Responsive Web}
\end{itemize}

\end{document}
```

---

## 4. Key Macro Reference

| Macro | Purpose | PDF Render | Text Extraction (`pdftotext`) |
|-------|---------|------------|-------------------------------|
| `\roleentry{Co}{Role}{Loc}{Date}{bullets}` | Experience header | Bold company + date right; italic role + loc right | `Company Date Role Location` (linear) |
| `\projectentry{Name}{Stack}{Domain}{Date}{bullets}` | Project header | Bold name + domain right; italic stack + date right | `Name Domain Stack Date` (linear) |
| `\eduentry{Degree}{Institution}{Date}{}` | Education line | Bold degree + date right; institution + loc | `Degree Date Institution` (linear) |
| `\certentry{Cert}{Issuer}{Date}{}` | Certification line | Bold cert + date right; issuer | `Cert Date Issuer` (linear) |
| `\signaltag{Tag}` | Hiring signal badge | **designer-polish:** no-op (ATS-visible only) | `[Tag]` (plain text, keyword-scannable) |
| `\kw{term}` | Keyword highlight | Normal weight (category heads are bold) | `term` |
| `\metric{val}` | Metric highlight | Bold dark | `val` |
| `\contactline` | Contact line | Muted, small, pipe-separated | Full contact line |

---

## 5. Audience-Aware LaTeX Patterns

### Lead with Outcome (CEO/HR)
```latex
% Technical-heavy (avoid)
\item \textbf{Architected} Design System v2 token architecture: 12 teams, 87\% UI coverage

% Audience-balanced (use)
\item \textbf{Built} unified design standards (Design System v2) adopted by \metric{12 cross-functional product teams} covering \metric{87\%} of product UI — \textbf{zero breaking changes in 18 months}; migrated \metric{240+} components to \kw{React/TypeScript} \signaltag{Systems Thinking} \signaltag{Technical Fluency}
```

### Inline First-Use Expansion (HR/CEO)
```latex
% Acronym only (avoid)
\item Championed WCAG 2.2 AA compliance

% Expanded first use (use)
\item Championed \kw{WCAG 2.2 AA (accessibility standard, level AA)} compliance
```

### Scale Context (Manager/HR)
```latex
% Bare number (avoid)
\item 15M+ merchants

% With context (use)
\item \metric{15+ million merchants (payment processing scale)}
```

### Plain Verb Substitution (All Audiences)
| Jargon Verb | LaTeX Plain Verb |
|-------------|------------------|
| Architected | Built / Designed |
| Orchestrated | Led / Coordinated |
| Spearheaded | Led / Drove |
| Engineered | Built / Developed |
| Optimized | Improved / Made faster |

---

## 6. NDA Abstraction Levels (LaTeX)

| Level | Company | Metrics | Example LaTeX |
|-------|---------|---------|---------------|
| **Full Transparency** | `\company{Stripe}` | Exact | `\company{Stripe}` + `\metric{+9pp}` |
| **Company-Abstracted** | Series C FinTech (payments) | Exact | `\company{Series C FinTech (payments)}` + `\metric{+9pp}` |
| **Domain-Abstracted** | B2B SaaS (checkout) | Exact | `\company{B2B SaaS (checkout)}` + `\metric{+9pp}` |
| **Pattern-Abstracted** | (unnamed) | Directional | `\company{Payments platform}` + `\metric{~40\% task time reduction (n=12, p<0.05)}` |
| **Full Blackout** | (unnamed) | Process only | `\company{NDA project}` + `Ran 0→1 discovery under NDA: JTBD → 3 pivots` |

---

## 7. Validation Gates (LaTeX-Specific)

| Gate | Check | Tool |
|------|-------|------|
| **Zero-Warning Clean Compiles** | Compiles with **0 errors and 0 warnings** under `pdflatex` or `xelatex` (no `Overfull \hbox`, no font substitution, no missing characters `"ec-lmb10"`) | Overleaf / local log |
| **No Overfull Boxes** | Log contains zero `Overfull \hbox` lines (enforced via `\emergencystretch=1.5em` and breaking long lists) | Log inspection |
| **ATS Linear** | `pdftotext -layout main.pdf` reads Company→Date→Title→Location per role | `pdftotext` |
| **Unicode Glyphs** | `fi`, `fl`, `•` extract correctly in `main.txt` | `pdftotext` + `cat` |
| **No Missing Fonts/Shapes** | Log shows zero `Font shape ... undefined` or substitution warnings | `pdflatex` / `xelatex` log |
| **Hyperref Clean** | No colored link boxes in PDF | Visual |
| **Signal Tags Extract** | `\signaltag{Tag}` → `[Tag]` in text | `pdftotext` |

---

## 7.5 Banned Raw Characters & Safe Symbols Table

When generating or refactoring LaTeX resume files, **NEVER paste raw Unicode symbols** that lack glyphs in standard T1/EC fonts (`ec-lmb10`). Always use clean LaTeX macros or text equivalents:

| Banned Raw Character | Source / Example Issue | Safe Clean LaTeX Equivalent |
|----------------------|----------------------|-----------------------------|
| `★` (U+2605) | Rating / STAR icon (`Missing character: There is no ★ in font ec-lmb10!`) | `4.8/5.0` or `$\star$` |
| `→` (U+2192) | Arrow in metrics (`18%→27%`) | `$\rightarrow$` or plain text `->` |
| `–` / `—` (raw dashes) | En-dash / Em-dash in dates | `--` (en-dash for date ranges) or `---` (em-dash) |
| `“` / `”` | Smart double quotes | ```text''` or standard neutral quotes |
| Unescaped `%`, `&`, `$` | LaTeX special characters | `\%`, `\&`, `\$` |

---

## 8. File Naming & Versioning

```
resume/
├── main.tex                              # Master LaTeX source (this template)
├── main-{company}-{role}-{YYYYMMDD}.tex  # Tailored version per application
├── main-{company}-{role}-{YYYYMMDD}.pdf  # Submission artifact (from Overleaf)
└── main-{company}-{role}-{YYYYMMDD}.txt  # Plain text fallback (pdftotext)
```

**Naming:** `main-stripe-senior-product-designer-20240115.tex`

---

## 9. Anti-Patterns (LaTeX)

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| `tabularx` / `tabular` for layout | Visual + `pdftotext` shows merged columns | Use `\roleentry` + `\hfill` |
| Custom `.cls` file | `\documentclass{myresume}` | Use `article` class only |
| `fontspec` / XeLaTeX / LuaLaTeX | Requires non-pdflatex compiler | Use `tgheros` + `pdflatex` |
| Missing `cmap`/`glyphtounicode` | Garbled `fi`/`fl`/bullets in text extraction | Wrap in `\ifpdf` guard; add before font packages |
| Unconditional `\input{glyphtounicode}` | Breaks XeLaTeX/LuaLaTeX (command undefined) | Use `\ifpdf` ... `\fi` guard |
| Colored text without `hidelinks` | Link boxes appear in PDF | `\usepackage[hidelinks]{hyperref}` |
| Text in header/footer | `fancyhdr` with content | Contact info in body only via `\contactline` |
| Raw Unicode symbols (`★`, `→`) | Log shows `Missing character: There is no ★ in font ec-lmb10!` | Use clean LaTeX symbols (`4.8/5.0`, `$\rightarrow$`) per §7.5 |
| Using `\scshape` with `\bfseries` where unsupported | Log shows `Font shape 'T1/lmr/b/sc' undefined` or substitutions | Use `\MakeUppercase` with `\bfseries` in `\titleformat{\section}` |
| Unwrapped long technical lists | Log shows `Overfull \hbox (42.1pt too wide)` | Set `\emergencystretch=1.5em` and break long lists logically |

---

## 10. Quick Reference: Agent Commands (LaTeX)

```bash
# Build tailored LaTeX from master
agent latex build --master main.tex --job job-analysis.json --gap gap-report.md --out main-stripe-pd-20240115.tex

# Inject keyword into LaTeX bullet
agent latex inject --file main-stripe-pd-20240115.tex --bullet 3 --keyword "design systems" --after "Spearheaded"

# Upgrade verb in LaTeX
agent latex verb --file main-stripe-pd-20240115.tex --bullet 2 --from "Worked on" --to "Spearheaded"

# Add metric to LaTeX bullet
agent latex metric --file main-stripe-pd-20240115.tex --bullet 1 --append "+9pp (n=24,847, p<0.01)"

# Add signal tag to LaTeX bullet
agent latex signal --file main-stripe-pd-20240115.tex --bullet 1 --tags "Data-Informed Iteration,Cross-functional Leadership"

# Apply NDA abstraction
agent latex nda --file main-stripe-pd-20240115.tex --level pattern-abstracted

# Apply audience-aware transforms
agent latex audience --file main-stripe-pd-20240115.tex --expand-acronyms --translate-jargon --lead-with-outcome --add-scale-context

# Validate LaTeX
agent latex validate --file main-stripe-pd-20240115.tex --job job-analysis.json
# Runs: pdflatex → pdftotext → parser sims → density → readability → audience gates

# Compile on Overleaf (manual) or local
pdflatex main-stripe-pd-20240115.tex
pdftotext -layout main-stripe-pd-20240115.pdf main-stripe-pd-20240115.txt
```