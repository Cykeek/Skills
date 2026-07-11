---
name: validation-checklist
description: Pre-submission validation gates for resume-doctor. LaTeX format compliance, keyword density, ATS parser simulation, readability, and content quality checks.
---

# Validation Checklist — Deep Reference (LaTeX)

**Purpose:** Comprehensive validation gates that every tailored LaTeX resume must pass before submission. Used in Phase 5 of the resume-doctor workflow.

---

## 1. LaTeX Format Compliance Gates (Hard Fail)

### 1.1 Structure & Linear Flow
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Single-column linear flow | Visual + `pdftotext -layout` | Company → Date → Title → Location reads sequentially per role |
| No tables for layout | `latex_table_check` | Zero `tabularx`/`tabular` environments |
| No TikZ / graphics | `latex_graphics_check` | Zero `\includegraphics`, `tikzpicture`, `pgfplots` |
| No custom `.cls` file | `latex_class_check` | `\documentclass{article}` only |
| No `fontspec` / XeLaTeX / LuaLaTeX | `latex_engine_check` | `pdflatex` + `mathptmx` only |
| Contact info in body only | `latex_header_check` | `\contactline` in body, no `fancyhdr` content |
| Required sections present | `latex_section_check` | Summary, Skills, Experience, Education |

### 1.2 Typography & Unicode (Critical for ATS)
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| `cmap` + `glyphtounicode` loaded conditionally | `latex_unicode_check` | `\usepackage{ifpdf}` + `\ifpdf` ... `\fi` wrapper around cmap/glyphtounicode/pdfgentounicode BEFORE fonts |
| Microtype enabled | `latex_microtype_check` | `\usepackage{microtype}` present |
| Font: mathptmx (Times-compatible) | `latex_font_check` | `\usepackage{mathptmx}` present |
| Hyperref with hidelinks | `latex_hyperref_check` | `\usepackage[hidelinks]{hyperref}` |
| Geometry margins correct | `latex_geometry_check` | `top=1.6cm, bottom=1.6cm, left=1.8cm, right=1.8cm` |
| Section formatting (titlesec) | `latex_section_check` | SC headers + thin rule, small caps, muted color |

### 1.3 Dates & Sections
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Date format MM/YYYY | `latex_date_check` | All dates match `MM/YYYY` or `MM/YYYY – Present` |
| Section order valid | `latex_order_check` | Per career stage rules (§4 optimization-patterns.md) |

---

## 2. Keyword Density Gates

### 2.1 Algorithm
```python
def keyword_density(resume_text: str, keyword: str) -> float:
    words = resume_text.lower().split()
    total = len(words)
    kw_words = len(keyword.split())
    count = resume_text.lower().count(keyword.lower())
    return (count * kw_words / total) * 100
```

### 2.2 Targets (from job-analysis.json)

| Priority | Min Density | Max Density | Action if Under | Action if Over |
|----------|-------------|-------------|-----------------|----------------|
| Critical | 2.0% | 3.5% | Inject in Summary, Skills, 2 bullets | Replace with variants |
| High | 1.5% | 3.0% | Inject in Summary, Skills, 1 bullet | Replace with variants |
| Medium | 1.0% | 2.0% | Inject in Skills, 1 bullet | Replace with variants |
| Low | 0.5% | 1.5% | Optional | Replace with variants |

### 2.3 Stuffing Detection
- **Hard fail:** Any single keyword > 5% density
- **Hard fail:** Same keyword 5+ times in one bullet
- **Hard fail:** Keywords only in footer/header/skills list
- **Warning:** Keyword density > max but < 5%

---

## 3. ATS Parser Simulation Gates

### 3.1 Target Parsers
| Parser | Market Share | Test Method |
|--------|--------------|-------------|
| Greenhouse | ~30% | `pdflatex → pdftotext -layout → parse` |
| Lever | ~20% | Same pipeline |
| Workday | ~25% | Same pipeline |
| iCIMS | ~15% | Same pipeline |
| Taleo | ~10% | Same pipeline |

### 3.2 Simulation Pipeline
```bash
# 1. Compile LaTeX (2-3 passes for cross-refs)
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex

# 2. Extract text (layout-preserving)
pdftotext -layout main.pdf main.txt

# 3. Parse with each parser's rules
python -m ats_parsers.greenhouse main.txt
python -m ats_parsers.lever main.txt
python -m ats_parsers.workday main.txt
python -m ats_parsers.icims main.txt
python -m ats_parsers.taleo main.txt
```

### 3.3 Pass Criteria

| Extraction | Greenhouse | Lever | Workday | iCIMS | Taleo |
|------------|------------|-------|---------|-------|-------|
| Contact info | ✅ | ✅ | ✅ | ✅ | ✅ |
| Summary | ✅ | ✅ | ✅ | ✅ | ✅ |
| Skills (all) | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| Experience (all) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Education | ✅ | ✅ | ✅ | ✅ | ✅ |
| Certifications | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| Projects | ⚠️ | ✅ | ❌ | ✅ | ❌ |
| Dates (MM/YYYY) | ✅ | ✅ | ✅ | ✅ | ✅ |

✅ = Full extraction | ⚠️ = Partial | ❌ = Not extracted

**Gate:** All ✅ sections must extract correctly. ⚠️ sections acceptable if non-critical.

### 3.4 Common Parser Failures & Fixes (LaTeX)

| Failure | Cause | Fix |
|---------|-------|-----|
| Skills merged into Experience | No clear Skills section | Add `\section*{Skills}` header |
| Dates parsed as text | Non-MM/YYYY format | Use `07/2022 – Present` |
| Company + role merged | No bold/italics distinction | `\roleentry` macro with `\textbf` + `\itshape` |
| Bullets lost | Non-standard bullets | Use `enumitem` with `\textbullet` |
| Contact in header/footer | `fancyhdr` with content | Move to body via `\contactline` |
| Garbled linear flow | Tables for layout | Use `\roleentry` + `\hfill` linear flow |
| Ligatures garbled (fi→fi) | Missing cmap/glyphtounicode | Add before font packages |

---

## 4. Unicode Extraction Gate (Critical for Engine Compatibility)

### 4.0 Root-Cause Guard: `glyphtounicode` Engine Mismatch

`\input{glyphtounicode}` must never be loaded unconditionally. It calls `\pdfglyphtounicode`, which exists in pdfLaTeX but may be undefined under XeLaTeX/LuaLaTeX. On Overleaf this can trigger a misleading `Missing \begin{document}` error and 100+ cascading fake errors from one preamble line.

**Required pattern:**
```latex
\usepackage{ifpdf}
\ifpdf
  \usepackage{cmap}
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi
```

**Gate:** If `\input{glyphtounicode}` appears outside an `\ifpdf` guard, hard fail before compile.

### 4.1 Test
```bash
pdftotext -layout main.pdf main.txt
cat main.txt | grep -E "(fi|fl|ffi|•|–|—)"
```

### 4.2 Required Mappings

| Glyph | Must Extract As | Status |
|-------|-----------------|--------|
| `fi` / `fl` / `ffi` | `fi` / `fl` / `ffi` | ✅ |
| `•` (bullet) | `•` | ✅ |
| `–` (en-dash) | `–` | ✅ |
| `—` (em-dash) | `—` | ✅ |

**Gate:** All above must extract correctly. Failure = hard fail.

---

## 5. Readability Gates (Measured on pdftotext extraction)

### 5.1 Metrics

| Metric | Threshold | Tool |
|--------|-----------|------|
| Flesch-Kincaid Grade | ≤ 12 | `textstat` |
| Avg Sentence Length | ≤ 20 words | `textstat` |
| Active Voice | ≥ 80% | `proselint` / manual |
| Passive Constructions | 0 | `proselint` |
| Syllables per Word | ≤ 1.6 | `textstat` |

### 5.2 Auto-Fail Patterns
| Pattern | Detection | Example Fix |
|---------|-----------|-------------|
| "Was responsible for" | Passive | → "Spearheaded" |
| "Was involved in" | Passive | → "Contributed to" |
| "Helped to" | Weak + passive | → "Enabled" |
| "Assisted with" | Weak | → "Supported" |

---

## 6. Content Quality Gates

### 6.1 Bullet Quality (Every Bullet)
| Requirement | Check | Fix |
|-------------|-------|-----|
| Starts with Tier 1/2 verb | `verb_check` | Replace Tier 3 |
| Contains quantified metric | `metric_check` | Add number/%/$ |
| Contains method/skill | `skill_check` | Inject keyword |
| Has 1–3 signal tags | `signal_check` | Add `\signaltag{...}` |
| No pronouns | `pronoun_check` | Remove I/my/we/our |
| ≤ 2 lines wrapped | `length_check` | Split or condense |

### 6.2 Section Quality

| Section | Requirements |
|---------|--------------|
| Summary | 2–4 lines, 3–5 bold keywords (`\kw{}`), 1–2 metrics, no pronouns |
| Skills | Categorized, exact keyword matches, verifiable in Experience |
| Experience | Reverse chron, 4–6 bullets current, 2–4 prior, all STAR format |
| Education | Degree + school + year, no GPA unless ≥3.8 early career |
| Certifications | Only field-relevant, current, with year |
| Projects | Name, context, role, stack, 2–3 bullets with metrics + signals |

### 6.3 NDA Compliance
| Level | Allowed | Example |
|-------|---------|---------|
| Full transparency | Company, metrics, details | "Stripe: +9pp activation" |
| Company-abstracted | Domain, metrics, no name | "Series C FinTech (payments): +9pp" |
| Domain-abstracted | Function, metrics, no domain | "B2B SaaS checkout: +9pp activation" |
| Pattern-abstracted | Method, directional metric | "A/B tested checkout redesign: +9pp (n=24k, p<0.01)" |
| Full blackout | Process only | "Ran 0→1 discovery under NDA: JTBD → 3 pivots" |

**Gate:** No raw confidential data. Minimum Pattern-abstracted for all NDA work.

---

## 7. Audience Comprehension Gates (NEW)

### 7.1 Per-Bullet Comprehension Test
| Audience | Must Understand | Check Method |
|----------|-----------------|--------------|
| **HR/Recruiter** | 1-2 job description keywords per bullet | Keyword scan |
| **CEO/Executive** | Business outcome (revenue, users, risk, speed) | "$" or "%" or "users" or "risk" present |
| **Hiring Manager** | Scope (team size, budget, timeline, users) | Numbers with context |
| **Technical Lead** | Method/proof (tools, statistical rigor) | Specific tools, "n=", "p<" |

### 7.2 Plain Language Gates
| Check | Threshold | Tool |
|-------|-----------|------|
| First-use acronym expanded | 100% | Manual scan |
| Jargon translated inline | ≥ 80% of technical terms | Manual scan |
| Numbers have context | 100% (no bare numbers) | Manual scan |
| Flesch-Kincaid Grade | ≤ 10 (stricter) | `textstat` |
| Avg Sentence Length | ≤ 18 words (stricter) | `textstat` |
| Passive Constructions | 0 | `proselint` |
| Active Voice | ≥ 85% (stricter) | `proselint` |

### 7.3 Summary Section Comprehension
| Requirement | Check |
|-------------|-------|
| Understandable by non-specialist in 15 seconds | Manual read |
| Contains 2-3 business outcomes with $ or % | Scan |
| No unexplained acronyms | Manual scan |
| Role + years + domain in first sentence | Manual scan |

---

## 8. Validation Report Format

```markdown
# Validation Report — main-stripe-pd-20240115.tex

**Generated:** 2024-01-15 14:32 UTC
**Job:** Stripe — Senior Product Designer (Greenhouse #123456)
**Candidate:** Maya Chen

---

## LaTeX Format Gates ✅ PASS
- [x] article class, 10.5pt, a4paper
- [x] geometry margins: top=1.6cm, bottom=1.6cm, left=1.8cm, right=1.8cm
- [x] cmap + glyphtounicode + pdfgentounicode=1 before font loading
- [x] microtype enabled
- [x] mathptmx font
- [x] No tabularx / tables / TikZ / graphics
- [x] Single-column, linear flow (ATS-safe)
- [x] hyperref with hidelinks
- [x] Contact in body via \contactline

---

## Keyword Density ✅ PASS
| Keyword | Priority | Min | Max | Actual | Status |
|---------|----------|-----|-----|--------|--------|
| design systems | Critical | 2.0% | 3.5% | 2.1% | ✅ |
| figma | High | 1.5% | 3.0% | 1.8% | ✅ |
| a/b testing | High | 1.5% | 3.0% | 2.2% | ✅ |
| react | High | 1.0% | 2.0% | 1.1% | ✅ |
| typescript | High | 1.0% | 2.0% | 1.3% | ✅ |
| payments | Medium | 1.0% | 2.0% | 1.4% | ✅ |

---

## Parser Simulation (pdflatex → pdftotext -layout)
| Parser | Contact | Summary | Skills | Experience | Education | Certs | Projects | Dates |
|--------|---------|---------|--------|------------|-----------|-------|----------|-------|
| Greenhouse | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Lever | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Workday | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ❌ | ✅ |
| iCIMS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Taleo | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ❌ | ✅ |

**Verdict:** PASS (Core sections ✅ across all parsers)

---

## Unicode Extraction Gate ✅ PASS
| Glyph | Extracted As | Status |
|-------|--------------|--------|
| fi / fl / ffi | fi / fl / ffi | ✅ |
| • (bullet) | • | ✅ |
| – (en-dash) | – | ✅ |
| — (em-dash) | — | ✅ |

---

## Readability ✅ PASS
| Metric | Threshold | Actual | Status |
|--------|-----------|--------|--------|
| Flesch-Kincaid Grade | ≤ 12 | 11.2 | ✅ |
| Avg Sentence Length | ≤ 20 | 17.4 | ✅ |
| Active Voice | ≥ 80% | 87% | ✅ |
| Passive Constructions | 0 | 0 | ✅ |

---

## Content Quality ✅ PASS
- [x] All bullets: Tier 1/2 verb + metric + signal tag(s)
- [x] No Tier 3 verbs
- [x] No pronouns
- [x] NDA projects: Pattern-abstracted minimum
- [x] Contact info in body
- [x] Acronyms spelled out (TypeScript (TS), etc.)

---

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

---

## Artifacts Generated
- `main-stripe-pd-20240115.pdf` — **Single submission artifact** (pdflatex, Overleaf-compatible)
- `main-stripe-pd-20240115.txt` — Plain text fallback (pdftotext -layout)

---

## Sign-Off
**Status:** ✅ READY FOR SUBMISSION
**Validated by:** resume-doctor v2.1
**Next re-validation:** 2024-04-15 (quarterly)
```

---

## 9. Agent Commands (LaTeX)

```bash
# Full validation suite
agent validate latex-format --resume main.tex
agent validate density --resume main.tex --job job-analysis.json
agent validate parsers --resume main.tex --parsers all
agent validate unicode-extraction --resume main.tex
agent validate readability --resume main.tex
agent validate audience --resume main.tex --job job-analysis.json
agent build --resume main.tex --engine pdflatex
# Runs: pdflatex -interaction=nonstopmode -halt-on-error main.tex (2-3 passes)
# Generates: main.pdf (submission), main.txt (pdftotext -layout fallback)

# Quick check (format + density only)
agent validate quick-check --resume main.tex --job job-analysis.json
```

---

## 10. Maintenance

- **Parser rules update:** Monthly (ATS vendor changes)
- **Density targets calibration:** Per-application A/B test → aggregate per company/role
- **Readability thresholds:** Annual review against industry benchmarks
- **Signal taxonomy:** Sync with internal signal tag taxonomy (§6 SKILL.md) quarterly
- **LaTeX template:** Review quarterly for Overleaf/TeX Live compatibility