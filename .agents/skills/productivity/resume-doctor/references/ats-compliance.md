# ATS Compliance — Deep Reference (LaTeX + pdflatex)

**Purpose:** Ensure LaTeX resume output compiles on Overleaf (pdflatex) and passes all major ATS parser simulations (Greenhouse, Lever, Workday, iCIMS, Taleo).

---

## 1. Output Format: Single LaTeX Source → PDF → Text Extraction

| Artifact | Purpose | Generation |
|----------|---------|------------|
| `main.tex` | Master source (article class, 10.5pt, a4paper) | Agent writes |
| `main.pdf` | Submission artifact (human + ATS) | `pdflatex` (2-3 passes) |
| `main.txt` | Fallback for parsers requiring plain text | `pdftotext -layout main.pdf main.txt` |

**No other formats:** No DOCX, no RTF, no HTML, no Markdown, no Pandoc, no Weasyprint.

---

## 2. How ATS Parsers Work (Modern Pipeline)

Modern ATS parsers (Greenhouse, Lever, Workday, iCIMS, Taleo) follow this pipeline:

```
PDF Upload → Text Extraction (pdftotext / PDFMiner / Apache Tika)
         → Section Segmentation (regex headers: Experience, Skills, Education)
         → Entity Extraction (skills, companies, dates, titles, degrees)
         → Structured JSON → Recruiter Dashboard
```

**Critical insight:** The parser never "sees" your PDF visually. It only sees the **linear text extraction**. If `pdftotext -layout` reads your resume in the wrong order, the ATS will too.

---

## 3. LaTeX-Specific ATS Compliance Rules (Hard Gates)

### 3.1 Document Class & Engine
| Rule | Enforcement |
|------|-------------|
| `\documentclass{article}` only | No custom `.cls`, no `memoir`, no `moderncv` |
| `pdflatex` only | No `xelatex`, no `lualatex` (Overleaf default = pdfLaTeX) |
| `mathptmx` for Times-compatible | No `fontspec`, no system fonts |
| `10.5pt` minimum | Below 10pt fails OCR on some parsers |

### 3.2 Layout: Single-Column Linear Flow (Mandatory)
| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| `tabularx` / `tabular` for layout | `pdftotext` shows merged columns | Use `\roleentry` + `\hfill` paragraph alignment |
| Multi-column (`multicol`) | Parser reads left column → right column | Single column only |
| `minipage` / `parbox` side-by-side | Text extraction order breaks | Sequential paragraphs only |
| `fancyhdr` with content | Parsers skip headers/footers | Contact info in body via `\contactline` |
| TikZ / graphics / images | Binary content, no text extraction | Zero graphics |

### 3.3 Section Structure (Parser Landmarks)
Parsers detect sections by header text. Required headers (exact match or close variant):

| Section | Accepted Variants |
|---------|-------------------|
| Summary | `Professional Summary`, `Executive Summary`, `Summary` |
| Skills | `Skills`, `Core Competencies`, `Technical Skills`, `Key Skills` |
| Experience | `Professional Experience`, `Work Experience`, `Experience`, `Employment History` |
| Education | `Education`, `Academic Background` |
| Certifications | `Certifications`, `Certificates`, `Licenses` |
| Projects | `Projects`, `Selected Projects`, `Key Projects` |

**Rule:** Use `\section*{Exact Header}` — starred to suppress numbering, exact text for parser recognition.

### 3.4 Date Format (Strict)
| Format | Parser Support |
|--------|----------------|
| `MM/YYYY – MM/YYYY` | ✅ All parsers |
| `MM/YYYY – Present` | ✅ All parsers |
| `Month YYYY – Month YYYY` | ⚠️ Partial (Greenhouse/Lever only) |
| `YYYY – YYYY` | ❌ Fails Workday/iCIMS |

**Rule:** All dates in `\dates{}` macro must use `07/2022 – Present` format.

### 3.5 Bullet Lists
| Requirement | Implementation |
|-------------|----------------|
| Standard bullet character | `\textbullet` via `enumitem` label=`\small\textbullet` |
| No custom bullets (▸, ▹, ◆, emoji) | Parser may drop or garble |
| Consistent indentation | `leftmargin=1.2em` (ats-max) / `1.3em` (designer-polish) |

---

## 4. Unicode Glyph Mapping (Critical for pdflatex)

pdflatex uses 8-bit fonts by default. Without explicit mapping, ligatures and special chars extract as garbage:

| Glyph in PDF | Without Mapping | With `cmap` + `glyphtounicode` |
|--------------|-----------------|--------------------------------|
| `fi` | `ﬁ` (U+FB01) or garbage | `fi` (U+0066 U+0069) ✅ |
| `fl` | `ﬂ` (U+FB02) or garbage | `fl` ✅ |
| `•` (bullet) | `â—¢` or `?` | `•` (U+2022) ✅ |
| `–` (en-dash) | `â€"` or `-` | `–` (U+2013) ✅ |
| `—` (em-dash) | `â€"` or `--` | `—` (U+2014) ✅ |

**Required preamble order (before font packages):**
```latex
\usepackage{ifpdf}
\ifpdf
  \usepackage{cmap}
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx}  % Font package AFTER glyph mapping
```

**Gate:** `agent validate unicode-extraction` runs `pdftotext -layout` and greps for correct mappings. Failure = hard fail.

---

## 5. Microtype & Typography (Parser-Safe Enhancements)

| Package | Purpose | ATS Impact |
|---------|---------|------------|
| `microtype` | Protrusion, expansion, kerning | ✅ Improves text extraction quality |
| `parskip` | Paragraph separation without `\parindent` | ✅ Cleaner linear flow |
| `titlesec` | Consistent section headers | ✅ Parser recognizes sections |

**Never disable microtype** — it improves character boundary detection in extraction.

---

## 6. Hyperref Configuration

```latex
\usepackage[hidelinks]{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 0},
  pdfproducer={LaTeX with pdflatex},
  pdfcreator={resume-doctor}
}
```

| Setting | Why |
|---------|-----|
| `hidelinks` | No colored boxes around links in PDF (visual + extraction clean) |
| `pdfborder={0 0 0}` | Explicit zero border |
| `pdfproducer` / `pdfcreator` | Identifies source for parser logs |

---

## 7. Dual Layout Modes (Both 100% ATS-Compatible)

| Mode | `ats-max` | `designer-polish` |
|------|-----------|-------------------|
| **Target** | High-volume ATS, legacy parsers | Designers, PMs, Creative Directors, CEOs |
| **Line height** | 1.0 | **1.15** |
| **Margins** | 1.6cm / 1.8cm | **1.8cm / 2.0cm** |
| **Section spacing** | 8pt / 4pt | **14pt / 6pt** |
| **Bullet `itemsep`** | 2pt | **4pt** |
| **Bullet `parsep`** | 0pt | **2pt** |
| **Header rule** | 0.4pt | **0.5pt** |
| **Signal tags** | `[\textbf{Tag}]` inline | **Badged** `\colorbox` with padding |
| **Font size** | 10.5pt | 10.5pt (same) |

**Both modes guarantee:**
- ✅ Linear ATS extraction (`pdftotext -layout`)
- ✅ Unicode glyph mapping
- ✅ Overleaf `pdflatex` compatibility
- ✅ Same macros (`\roleentry`, `\projectentry`, `\signaltag`, `\kw`, `\metric`)

**Selection:** Single line at top of `main.tex`:
```latex
\def\resumemode{designer-polish}  % or ats-max
```

---

## 8. ATS Parser Simulation Gates (Validation Phase)

### 8.1 Pipeline
```bash
# 1. Compile (2-3 passes for cross-refs)
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex

# 2. Extract text (layout-preserving)
pdftotext -layout main.pdf main.txt

# 3. Parse with each engine's rules
python -m ats_parsers.greenhouse main.txt
python -m ats_parsers.lever main.txt
python -m ats_parsers.workday main.txt
python -m ats_parsers.icims main.txt
python -m ats_parsers.taleo main.txt
```

### 8.2 Pass Criteria (from `validation-checklist.md`)

| Extraction | Greenhouse | Lever | Workday | iCIMS | Taleo |
|------------|------------|-------|---------|-------|-------|
| Contact info | ✅ | ✅ | ✅ | ✅ | ✅ |
| Summary | ✅ | ✅ | ✅ | ✅ | ✅ |
| Skills (all) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Experience (all) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Education | ✅ | ✅ | ✅ | ✅ | ✅ |
| Certifications | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| Projects | ⚠️ | ✅ | ❌ | ✅ | ❌ |
| Dates (MM/YYYY) | ✅ | ✅ | ✅ | ✅ | ✅ |

✅ = Full extraction | ⚠️ = Partial | ❌ = Not extracted

**Gate:** All required sections (Contact, Summary, Skills, Experience, Education, Dates) must extract correctly (✅). Optional sections (Certifications, Projects) may be ⚠️/❌.

---

## 9. Common Parser Failures & LaTeX Fixes

| Failure | LaTeX Cause | Fix |
|---------|-------------|-----|
| Skills merged into Experience | No clear `\section*{Skills}` header | Add explicit section |
| Dates parsed as text | Non-MM/YYYY format | Use `\dates{07/2022 – Present}` |
| Company + role merged | No bold/italic distinction | `\roleentry` macro with `\textbf` + `\itshape` |
| Bullets lost | Non-standard bullet character | `enumitem` label=`\small\textbullet` |
| Contact in header/footer | `fancyhdr` with content | Move to body via `\contactline` |
| Garbled linear flow | Tables for layout | Use `\roleentry` + `\hfill` linear flow |
| Ligatures garbled (`fi`→`fi`) | Missing `cmap`/`glyphtounicode` | Add before font packages in `\ifpdf` guard |

---

## 10. Validation Commands (Agent)

```bash
# Full validation suite
agent validate latex-format --resume main.tex
agent validate density --resume main.tex --job job-analysis.json
agent validate parsers --resume main.tex --parsers all
agent validate unicode-extraction --resume main.tex
agent validate readability --resume main.tex
agent validate audience --resume main.tex --job job-analysis.json

# Build artifacts
agent build --resume main.tex --engine pdflatex
# Generates: main.pdf (submission), main.txt (pdftotext fallback)
```

---

## 11. Maintenance

- **Parser rules update:** Monthly (ATS vendor changes)
- **Density targets calibration:** Per-application A/B test → aggregate per company/role
- **LaTeX template:** Review quarterly for Overleaf/TeX Live compatibility
- **Unicode mapping test:** Run `pdftotext -layout` after any preamble change