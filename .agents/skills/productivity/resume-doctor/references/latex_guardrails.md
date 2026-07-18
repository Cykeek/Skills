# LaTeX Guardrails & Overleaf Engine Compatibility

This document specifies the mandatory guardrails for all LaTeX resumes generated or tailored by `resume-doctor`. These rules ensure zero-warning, zero-error compilation across all Overleaf compilation engines (`pdfLaTeX`, `XeLaTeX`, `LuaLaTeX`) and prevent ATS parsing failures.

---

## 1. Engine-Safe Preamble Guardrail

### The Problem
Bare root-level definitions of `\input{glyphtounicode}` or `\pdfgentounicode=1` crash non-pdfTeX engines (`XeLaTeX` and `LuaLaTeX`) with:
```
! Undefined control sequence.
l.xx \pdfgentounicode=1
```
Similarly, `inputenc` and `fontenc` packages can trigger warnings or conflicts on LuaLaTeX/XeLaTeX.

### The Mandatory Solution
Every generated LaTeX file MUST include `\usepackage{iftex}` and wrap `pdfLaTeX`-specific Unicode and font settings in the `\ifPDFTeX` conditional guard:

```latex
\documentclass[10pt,a4paper]{article}
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi
```

- When compiled with **pdfLaTeX** on Overleaf: `glyphtounicode` is loaded and `\pdfgentounicode=1` ensures proper character mapping for ATS parsers.
- When compiled with **XeLaTeX** or **LuaLaTeX** on Overleaf: native UTF-8 handling works out of the box and primitive commands are safely bypassed.

---

## 2. LaTeX Reserved Character Escaping Rules

Any unescaped LaTeX reserved character in document body text, section headings, table headers, or PDF metadata will cause Overleaf compilation failures (`Misplaced alignment tab character &`) or broken PDF outputs.

### Special Character Escaping Table

| Character | LaTeX Reserved Meaning | Mandatory Escaping in Body Text | Example Correct Usage |
|-----------|------------------------|---------------------------------|-----------------------|
| `&` | Alignment tab in tables | `\&` | `AT\&T`, `Skills \& Expertise` |
| `%` | Comment character | `\%` | `Increased revenue by 25\%` |
| `$` | Math mode toggle | `\$` | `Managed \$500k budget` |
| `#` | Macro parameter | `\#` | `Ranked \#1 engineer` |
| `_` | Subscript toggle | `\_` | `file\_name\_v2` |

### Special Rules for PDF Metadata (`\hypersetup`)
Inside `\hypersetup{pdftitle={...}, pdfauthor={...}}`, special formatting characters like `\&` should be avoided or replaced with plain English words:
- **AVOID:** `\hypersetup{pdfsubject={Design \& Frontend Engineering}}`
- **USE:** `\hypersetup{pdfsubject={Design and Frontend Engineering}}`

---

## 3. ATS Parser Structure & Canonical Headers

To ensure clean segmentation across ATS parsers (Greenhouse, Lever, Workday, iCIMS, Taleo):
1. **Never split skills into multiple disjoint sections** (e.g., do not create both a `\section*{Core Skills}` and `\section*{Technical Proficiency}` apart from each other). Use a single consolidated canonical section: `\section*{Skills & Technical Proficiency}` or `\section*{Skills}`.
2. **Never use multi-column tables, text boxes (`tcolorbox`), icons, or image badges** for core qualifications or experience.
3. **Use standard canonical section headers**:
   - `\section*{Professional Summary}`
   - `\section*{Skills & Technical Proficiency}`
   - `\section*{Experience}` or `\section*{Work Experience}`
   - `\section*{Education & Certifications}`

---

## 4. Unicode Ligature Avoidance

Ligatures (`ﬀ`, `ﬁ`, `ﬂ`, `ﬃ`, `ﬄ`) corrupt ATS keyword extraction and matching.
- **Rule:** Never emit Unicode ligature characters in generated `.tex` or `.txt` artifacts.
- **Always convert:**
  - `ﬀ` → `ff`
  - `ﬁ` → `fi`
  - `ﬂ` → `fl`
  - `ﬃ` → `ffi`
  - `ﬄ` → `ffl`
- **Critical ATS keywords affected:** `handoff`, `efficiency`, `fluency`, `defined`, `workflow`, `Confluence`.

---

## 5. Recruiter & ATS Hygiene (No Bracketed Tags)

Internal classification tags (`[systems-thinking]`, `[technical-fluency]`, `[accessibility-advocacy]`) must NEVER appear in the final candidate resume visible to recruiters or ATS parsers.
- **Rule:** Strip all bracketed metadata tags matching `\[[a-zA-Z0-9_-]+\]` before saving `main.tex`.
- **Action:** Convert tagged concepts into natural language phrases inside bullet impact statements.
