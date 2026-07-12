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
| **Unicode Glyph Mapping** | `\usepackage{cmap} + \input{glyphtounicode} + \pdfgentounicode=1` before font loading — ligatures (`fi`, `fl`, `ffi`) and bullets map to correct Unicode |
| **Zero Dependencies** | Standard TeX Live packages only: `article`, `geometry`, `titlesec`, `enumitem`, `hyperref`, `xcolor`, `microtype`, `mathptmx`/`tgheros` |
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
| Line height | 1.0 (cramped) | **1.15** (professional) |
| Section spacing | 4pt/8pt tight | **8pt/14pt** breathing room |
| Bullet `itemsep` | 2pt | **4pt** |
| Bullet `parsep` | 0pt | **2pt** |
| Header rule weight | 0.4pt | **0.5pt** |
| Signal tag render | `[\textbf{Tag}]` inline | **Badge** with padding + rounded corners (TikZ-free) |
| Page margins | 1.6cm/1.8cm | **1.8cm/2.0cm** (wider optical margins) |
| Font size | 10.5pt | **10.5pt** (same) |
| Font family | `mathptmx` (Times) | **`tgheros`** (Helvetica-clone, sans-serif) |
| Skills position | After Experience | **After Projects** (per design role convention) |

---

## 3. Complete `main.tex` Template (Dual-Mode)

```latex
% ============================================================
% MODE SELECTION — uncomment exactly ONE:
% ============================================================
%\def\resumemode{ats-max}        % Dense, keyword-packed, parser-first
\def\resumemode{designer-polish} % Professional typography, visual hierarchy
% ============================================================

\documentclass[10.5pt, a4paper]{article}

% ── Engine Detection & Encoding Compatibility (Zero Warnings across engines) ──
\usepackage{ifpdf}
\ifpdf
  % pdfLaTeX engine: T1 encoding, utf8 input, and glyphtounicode for ATS extraction
  \usepackage{cmap}
  \input{glyphtounicode}
  \pdfgentounicode=1
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
\else
  % XeLaTeX / LuaLaTeX engine: Unicode native encodings (TU engine)
  \usepackage{fontspec}
\fi

% ── Zero-Warning Line Breaking & Overflow Protection ──
\emergencystretch=3em
\tolerance=1000
\hbadness=10000
\hfuzz=0.5pt

% ── Mode-Dependent Geometry ──
\ifdefined\resumemode
  \ifx\resumemode\undefined\else
    \ifx\resumemode\empty\else
      \expandafter\ifx\csname resumemode@\resumemode\endcsname\relax\else
        \csname resumemode@\resumemode\endcsname
      \fi
    \fi
  \fi
\fi

% Fallback geometry (ats-max defaults)
\providecommand{\resumemode@ats-max}{%
  \usepackage[a4paper, top=1.6cm, bottom=1.6cm, left=1.8cm, right=1.8cm]{geometry}%
}
\providecommand{\resumemode@designer-polish}{%
  \usepackage[a4paper, top=1.8cm, bottom=1.8cm, left=2.0cm, right=2.0cm]{geometry}%
}

% ── PDF Metadata Injection (Auto-populated from candidate profile + job analysis) ──
% Agent populates these at build time from candidate-profile.yaml and job-analysis.json
\hypersetup{
  pdfauthor  = {Candidate Name},           % ← populated by agent from candidate-profile.yaml
  pdftitle   = {Target Role at Company},   % ← populated by agent from job-analysis.json
  pdfsubject = {Target Role at Company},   % ← populated by agent
  pdfkeywords = {kw1, kw2, kw3, kw4},      % ← populated by agent from job-analysis.json keyword_targets
  hidelinks  = true
}

% ── Paragraphs ──
\usepackage{parskip}

% ── Microtype (protrusion, expansion, kerning) ──
\usepackage{microtype}

% ── Mode-Dependent Font ──
\providecommand{\resumemode@ats-max@font}{%
  \usepackage{mathptmx}% Times-compatible, serif
}
\providecommand{\resumemode@designer-polish@font}{%
  \usepackage[scale=0.92]{tgheros}% Helvetica-clone, sans-serif; ATS-safe ligatures
  \renewcommand{\familydefault}{\sfdefault}%
}
\csname resumemode@\resumemode @font\endcsname

% ── Colors ──
\usepackage{xcolor}
\definecolor{textmain}{gray}{0.10}
\definecolor{muted}{gray}{0.40}
\definecolor{rulecolor}{gray}{0.75}
\definecolor{linkcolor}{RGB}{30, 90, 180}
\definecolor{signalcolor}{RGB}{15, 82, 186}
\definecolor{signalbg}{RGB}{230, 242, 255}  % Light blue badge background

% ── Hyperref with PDF Metadata Injection (auto-populated) ──
\usepackage[hidelinks]{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 0},
  pdfauthor={},          % Filled by agent from candidate profile
  pdftitle={},           % Filled by agent: "Full Name — Target Role at Company"
  pdfsubject={},         % Filled by agent: "Tailored resume for Target Role at Company"
  pdfkeywords={},        % Filled by agent: comma-separated critical/high keywords from job-analysis.json
  pdfproducer={LaTeX with pdflatex},
  pdfcreator={resume-doctor}
}

% ── Mode-Dependent Section Formatting ──
\usepackage{titlesec}
\providecommand{\resumemode@ats-max@section}{%
  \titleformat{\section}
    {\normalfont\fontsize{9pt}{11pt}\selectfont\bfseries\color{muted}\MakeUppercase}
    {}{0em}{}
    [\vspace{1pt}{\color{rulecolor}\hrule height 0.4pt}\vspace{4pt}]%
  \titlespacing{\section}{0pt}{8pt}{4pt}%
}
\providecommand{\resumemode@designer-polish@section}{%
  \titleformat{\section}
    {\normalfont\fontsize{9.5pt}{12pt}\selectfont\bfseries\color{muted}\MakeUppercase}
    {}{0em}{}
    [\vspace{2pt}{\color{rulecolor}\hrule height 0.5pt}\vspace{6pt}]%
  \titlespacing{\section}{0pt}{14pt}{6pt}%
}
\csname resumemode@\resumemode @section\endcsname

% ── Mode-Dependent Bullet Lists ──
\usepackage{enumitem}
\providecommand{\resumemode@ats-max@list}{%
  \setlist[itemize]{label={\small\textbullet}, leftmargin=1.2em, itemsep=2pt, parsep=0pt, topsep=2pt}%
}
\providecommand{\resumemode@designer-polish@list}{%
  \setlist[itemize]{label={\small\textbullet}, leftmargin=1.3em, itemsep=4pt, parsep=2pt, topsep=3pt}%
}
\csname resumemode@\resumemode @list\endcsname

% ── Mode-Dependent Custom Macros ──

% Role Entry: Company | Date on first line; Title | Location on second line
\providecommand{\resumemode@ats-max@roleentry}{%
  \newcommand{\roleentry}[4]{%
    \vspace{4pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{-1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{2pt}%
  }%
}
\providecommand{\resumemode@designer-polish@roleentry}{%
  \newcommand{\roleentry}[4]{%
    \vspace{6pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{3pt}%
  }%
}
\csname resumemode@\resumemode @roleentry\endcsname

% Project Entry: Project Name | Date on first line; Role | Stack on second line
\providecommand{\resumemode@ats-max@projectentry}{%
  \newcommand{\projectentry}[4]{%
    \vspace{3pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{-1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{1pt}%
  }%
}
\providecommand{\resumemode@designer-polish@projectentry}{%
  \newcommand{\projectentry}[4]{%
    \vspace{5pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{2pt}%
  }%
}
\csname resumemode@\resumemode @projectentry\endcsname

% Education Entry: Degree | Date on first line; School | Location on second line
\providecommand{\resumemode@ats-max@eduentry}{%
  \newcommand{\eduentry}[4]{%
    \vspace{3pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{-1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{1pt}%
  }%
}
\providecommand{\resumemode@designer-polish@eduentry}{%
  \newcommand{\eduentry}[4]{%
    \vspace{5pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{2pt}%
  }%
}
\csname resumemode@\resumemode @eduentry\endcsname

% Certification Entry: Cert Name | Date on first line; Issuer | (optional detail) on second line
\providecommand{\resumemode@ats-max@certentry}{%
  \newcommand{\certentry}[4]{%
    \vspace{3pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{-1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{1pt}%
  }%
}
\providecommand{\resumemode@designer-polish@certentry}{%
  \newcommand{\certentry}[4]{%
    \vspace{5pt}%
    \noindent \textbf{##1} \hfill {\small\color{muted} ##2} \par
    \vspace{1pt}%
    \noindent {\small\itshape ##3} \hfill {\small\color{muted}\itshape ##4} \par
    \vspace{2pt}%
  }%
}
\csname resumemode@\resumemode @certentry\endcsname

% Mode-Dependent Signal Tag Rendering
% DESIGNER-POLISH: Visual badge + ATS-visible bracketed text
% ATS-MAX: Inline bracketed text only
\providecommand{\resumemode@ats-max@signaltag}{%
  \newcommand{\signaltag}[1]{%
    \textcolor{signalcolor}{[\textbf{##1}]}%
  }%
}
\providecommand{\resumemode@designer-polish@signaltag}{%
  \newcommand{\signaltag}[1]{%
    \textcolor{signalcolor}{%
      \fboxsep=2pt\relax
      \colorbox{signalbg}{\strut[\textbf{##1}]}%
    }%
    \ \textnormal{[\textbf{##1}]}% ATS-visible fallback
  }%
}
\csname resumemode@\resumemode @signaltag\endcsname

% Inline keyword highlight (bold for ATS, normal weight for reading)
\newcommand{\kw}[1]{\textbf{#1}}

% Metric highlight (bold + slight color for CEO scan)
\newcommand{\metric}[1]{\textcolor{textmain}{\textbf{#1}}}

% Company/Role inline formatting
\newcommand{\company}[1]{\textbf{#1}}
\newcommand{\role}[1]{{\itshape #1}}
\newcommand{\location}[1]{{\small\color{muted}\itshape #1}}
\newcommand{\dates}[1]{{\small\color{muted} #1}}

% Mode-Dependent Divider Rule
\providecommand{\resumemode@ats-max@divider}{%
  \newcommand{\divider}{\vspace{4pt}\noindent{\color{rulecolor}\hrule height 0.4pt}\vspace{4pt}}%
}
\providecommand{\resumemode@designer-polish@divider}{%
  \newcommand{\divider}{\vspace{6pt}\noindent{\color{rulecolor}\hrule height 0.5pt}\vspace{6pt}}%
}
\csname resumemode@\resumemode @divider\endcsname

% Contact line (single line, pipe-separated)
\newcommand{\contactline}[1]{%
  \noindent {\small\color{muted} #1} \par
  \vspace{2pt}%
}

% ── Document ──
\begin{document}

% Page color
\pagecolor{white}
\color{textmain}

% ── Mode-Dependent Baseline Stretch ──
\providecommand{\resumemode@ats-max@baseline}{%
  \linespread{1.0}\selectfont%
}
\providecommand{\resumemode@designer-polish@baseline}{%
  \linespread{1.15}\selectfont%
}
\csname resumemode@\resumemode @baseline\endcsname

% ── HEADER ──
% VALIDATION GATE: Single target role only — no "UI/UX Designer & Product Designer"
\begin{center}
  {\LARGE \textbf{Full Name}} \\[4pt]
  {\large Target Role — Domain Specialization} \\[6pt]
\end{center}
\contactline{City, State | +1 555 123 4567 | email@domain.com | linkedin.com/in/username | github.com/username}

\divider

% ── PROFESSIONAL SUMMARY ──
% TEMPLATE: 3-sentence plain paragraph (no macros in last sentence)
% 1. [Role] with [years] experience in [domains].
% 2. [Method/skills] — [1-2 metrics with scale context].
% 3. [Passion/values — plain language, no macros].
\section*{Professional Summary}
Senior Product Designer with 7 years building FinTech and B2B SaaS products at scale.
Led design systems adoption across \metric{12 cross-functional product teams} (\metric{87\%} UI coverage, \metric{0} breaking changes in \metric{18 months}); drove \metric{+9pp activation (18\%→27\%)} via checkout redesign validated through \kw{A/B testing (controlled experiments, n=24k, p<0.01)}.
Passionate about payments infrastructure, KYC/AML compliance, and accessible financial experiences.

\divider

% ── MODE-DEPENDENT SECTION ORDERING ──
% ats-max: Summary → Skills → Experience → Education → Certifications → Projects → Signals
% designer-polish: Summary → Experience → Education → Certifications → Projects → Skills → Signals
\ifx\resumemode\designer-polish
  % Designer-polish: Skills moved after Projects (design role convention)
\else
  % ats-max: Skills in top 1/3
  % ── SKILLS ──
  \section*{Skills}

  \subsection*{Technical Skills}
  \begin{itemize}
    \item \textbf{Product Design:} Product Design, \kw{Design Systems}, Design Operations, User Research (JTBD, Usability), Prototyping (\kw{Figma}, \kw{React}, Framer), \kw{Accessibility (WCAG 2.2 AA)}, \kw{A/B Testing}, Analytics (Mixpanel, Looker)
    \item \textbf{Engineering:} \kw{React}, \kw{TypeScript}, HTML/CSS, Tailwind, Storybook, Design Tokens, CI/CD, GraphQL
  \end{itemize}

  \subsection*{Tools \& Platforms}
  \kw{Figma}, FigJam, Jira, Linear, Mixpanel, Amplitude, Looker, Git, GitHub, Storybook, Zeroheight, Notion, Miro, Dovetail

  \subsection*{Domain Knowledge}
  FinTech, Payments, KYC/AML, PCI-DSS, B2B SaaS, Marketplace, E-commerce, Design Systems

  \divider
\fi

% ── PROFESSIONAL EXPERIENCE ──
\section*{Professional Experience}

\roleentry{\company{Stripe}}{San Francisco, CA}{\role{Senior Product Designer (Lead)}}{\dates{07/2022 – Present}}
\begin{itemize}
  \item \textbf{Spearheaded} checkout redesign for \metric{15+ million merchants (payment processing scale)} delivering \metric{+9pp activation (18\%→27\%)}, \metric{\$460K ARR retained}; validated via \kw{A/B test (controlled experiment, n=24,847, statistically significant p<0.01, holdout confirmed)} \signaltag{Data-Informed Iteration} \signaltag{Cross-functional Leadership}
  \item \textbf{Built} unified design standards (Design System v2) adopted by \metric{12 cross-functional product teams} covering \metric{87\%} of product UI — \textbf{zero breaking changes in 18 months}; migrated \metric{240+} components to \kw{React/TypeScript} \signaltag{Systems Thinking} \signaltag{Technical Fluency}
  \item \textbf{Established} JTBD research practice: \metric{52 interviews/year}, insights logged in Dovetail, \textbf{directly informed 3 product pivots} \signaltag{User Research Rigor} \signaltag{Strategic Influence}
  \item \textbf{Championed} \kw{WCAG 2.2 AA (accessibility standard, level AA)} compliance: audited \metric{240 components}, trained \metric{15 engineers}, \textbf{reduced a11y bugs 78\%} (\metric{47→10/quarter}) \signaltag{Accessibility Advocacy}
\end{itemize}

\roleentry{\company{Airbnb}}{San Francisco, CA}{\role{Product Designer}}{\dates{07/2020 – 06/2022}}
\begin{itemize}
  \item \textbf{Delivered} host onboarding redesign: \metric{+23\% activation}, \metric{-45 min setup time} via JTBD-driven progressive disclosure \signaltag{0→1 Ambiguity} \signaltag{Data-Informed Iteration}
  \item \textbf{Designed} marketplace trust flows (identity verification, reviews): \metric{+15\% booking conversion} for new hosts \signaltag{Cross-functional Leadership}
\end{itemize}

\divider

% ── EDUCATION ──
% FORMAT: 2-line rhythm — Degree | Date / Institution | Location
\section*{Education}

\eduentry{M.S. Human-Computer Interaction}{\dates{2020}}{Stanford University}{Stanford, CA}
\eduentry{B.S. Design Engineering}{\dates{2018}}{University of Washington}{Seattle, WA}

\divider

% ── CONTINUOUS LEARNING / CERTIFICATIONS ──
% SAME 2-line rhythm as Education
\section*{Certifications}

\certentry{Certified Usability Analyst (CUA)}{\dates{2021}}{Human Factors International}{}
\certentry{AWS Certified Cloud Practitioner}{\dates{2023}}{Amazon Web Services}{}

\divider

% ── SELECTED PROJECTS ──
\section*{Selected Projects}

\projectentry{Unified Billing Dashboard}{Internal Platform | Jan–Jun 2023}{\role{Lead Designer (3D, 2E, 1PM, 1R)}}{Stack: Figma, Storybook, React, BigQuery}
\begin{itemize}
  \item \textbf{Architected} billing dashboard for \metric{500+} internal stakeholders; \textbf{reduced reconciliation time 60\%}
  \item \textbf{Signals:} \signaltag{Systems Thinking} \signaltag{0→1 Ambiguity} \signaltag{Cross-functional Leadership}
\end{itemize}

\divider

% ── SKILLS (designer-polish mode only) ──
\ifx\resumemode\designer-polish
  \section*{Skills}

  \subsection*{Technical Skills}
  \begin{itemize}
    \item \textbf{Product Design:} Product Design, \kw{Design Systems}, Design Operations, User Research (JTBD, Usability), Prototyping (\kw{Figma}, \kw{React}, Framer), \kw{Accessibility (WCAG 2.2 AA)}, \kw{A/B Testing}, Analytics (Mixpanel, Looker)
    \item \textbf{Engineering:} \kw{React}, \kw{TypeScript}, HTML/CSS, Tailwind, Storybook, Design Tokens, CI/CD, GraphQL
  \end{itemize}

  \subsection*{Tools \& Platforms}
  \kw{Figma}, FigJam, Jira, Linear, Mixpanel, Amplitude, Looker, Git, GitHub, Storybook, Zeroheight, Notion, Miro, Dovetail

  \subsection*{Domain Knowledge}
  FinTech, Payments, KYC/AML, PCI-DSS, B2B SaaS, Marketplace, E-commerce, Design Systems

  \divider
\fi

% ── SIGNALS DEMONSTRATED ──
\section*{Signals Demonstrated}
\signaltag{Data-Informed Iteration} \signaltag{Cross-functional Leadership} \signaltag{Systems Thinking} \signaltag{Technical Fluency} \signaltag{0→1 Ambiguity} \signaltag{User Research Rigor} \signaltag{Strategic Influence} \signaltag{Accessibility Advocacy}

\end{document}
```

---

## 3. Compilation Instructions

### Overleaf (Recommended)
1. Create new project → "Blank Project"
2. Upload `main.tex` (this file)
3. Compiler: **pdfLaTeX** (default)
4. Click "Recompile" — produces `main.pdf`

### Local (TeX Live)
```bash
pdflatex main.tex
# Run twice for cross-refs
pdflatex main.tex
```

### Verify ATS Extraction
```bash
pdftotext -layout main.pdf main.txt
cat main.txt
# Should read linearly: Company Date Title Location, bullets in order
```

---

## 4. Key Macro Reference

| Macro | Purpose | PDF Render | Text Extraction (`pdftotext`) |
|-------|---------|------------|-------------------------------|
| `\roleentry{Co}{Loc}{Role}{Date}` | Experience header | Bold company + date right; italic role + loc right | `Company Date Role Location` (linear) |
| `\projectentry{Name}{Context}{Role}{Stack}` | Project header | Bold name + context right; italic role + stack right | `Name Context Role Stack` (linear) |
| `\signaltag{Tag}` | Hiring signal badge | Blue badge `[**Tag**]` | `[Tag]` (plain text, keyword-scannable) |
| `\kw{term}` | Keyword highlight | Bold | `term` (bold preserved in some parsers) |
| `\metric{val}` | Metric highlight | Bold dark | `val` |
| `\contactline{...}` | Contact line | Muted, small | Full contact line |

---

## 5. Audience-Aware LaTeX Patterns

### Lead with Outcome (CEO/HR)
```latex
% Technical-heavy (avoid)
\item \textbf{Architected} Design System v2 token architecture: 12 teams, 87\% UI coverage

% Audience-balanced (use)
\item \textbf{Built} unified design standards (Design System v2) adopted by \metric{12 cross-functional product teams} covering \metric{87\%} of product UI — \textbf{zero breaking changes in 18 months} \signaltag{Systems Thinking} \signaltag{Technical Fluency}
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
| Full Transparency | \company{Stripe} | Exact | `\company{Stripe}` + `\metric{+9pp}` |
| Company-Abstracted | Series C FinTech (payments) | Exact | `\company{Series C FinTech (payments)}` + `\metric{+9pp}` |
| Domain-Abstracted | B2B SaaS (checkout) | Exact | `\company{B2B SaaS (checkout)}` + `\metric{+9pp}` |
| Pattern-Abstracted | (unnamed) | Directional | `\company{Payments platform}` + `\metric{~40\% task time reduction (n=12, p<0.05)}` |
| Full Blackout | (unnamed) | Process only | `\company{NDA project}` + `Ran 0→1 discovery under NDA: JTBD → 3 pivots` |

---

## 7. Validation Gates (LaTeX-Specific)

| Gate | Check | Tool |
|------|-------|------|
| **Zero-Warning Clean Compiles** | Compiles with **0 errors and 0 warnings** under `pdflatex` or `xelatex` (no `Overfull \hbox`, no font substitution, no missing characters `"ec-lmb10"`) | Overleaf / local log |
| **No Overfull Boxes** | Log contains zero `Overfull \hbox` lines (enforced via `\emergencystretch=3em` and breaking long lists) | Log inspection |
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
| `fontspec` / XeLaTeX / LuaLaTeX | Requires non-pdflatex compiler | Use `mathptmx` + `pdflatex` |
| Missing `cmap`/`glyphtounicode` | Garbled `fi`/`fl`/bullets in text extraction | Wrap in `\ifpdf` guard; add before font packages |
| Unconditional `\input{glyphtounicode}` | Breaks XeLaTeX/LuaLaTeX (command undefined) | Use `\ifpdf` ... `\fi` guard |
| Colored text without `hidelinks` | Link boxes appear in PDF | `\usepackage[hidelinks]{hyperref}` |
| Text in header/footer | `fancyhdr` with content | Contact info in body only via `\contactline` |
| Raw Unicode symbols (`★`, `→`) | Log shows `Missing character: There is no ★ in font ec-lmb10!` | Use clean LaTeX symbols (`4.8/5.0`, `$\rightarrow$`) per §7.5 |
| Using `\scshape` with `\bfseries` where unsupported | Log shows `Font shape 'T1/lmr/b/sc' undefined` or substitutions | Use `\MakeUppercase` with `\bfseries` in `\titleformat{\section}` |
| Unwrapped long technical lists | Log shows `Overfull \hbox (42.1pt too wide)` | Set `\emergencystretch=3em` and break long lists logically |

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