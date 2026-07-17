---
name: validation-checklist
description: Pre-submission validation gates for resume-doctor. LaTeX format compliance, keyword density, ATS parser simulation, readability, and content quality checks.
---

# Validation Checklist — Deep Reference (LaTeX)

**Purpose:** Comprehensive validation gates that every tailored LaTeX resume must pass before submission. Used in Phase 5 of the resume-doctor workflow.

---

## 1. LaTeX Format Compliance Gates (Hard Fail)

### 1.0 Zero-Warning & Zero-Error Compilation (Hard Gate)
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| **Zero Compilation Errors** | `pdflatex` / `xelatex` exit code | Exits `0` with zero error messages |
| **Zero Compilation Warnings** | Log inspection | Absolutely zero LaTeX/package warnings: no `Package inputenc Warning: ignored`, no `Font shape ... undefined`, no `Some font shapes were not available`, no `Missing character` warning |
| **Zero Overfull / Underfull Boxes** | Log inspection (`Overfull \hbox`) | Zero `Overfull \hbox` lines (protected via `\emergencystretch=3em` and clean line breaking) |
| **Zero Missing / Banned Symbols** | Log inspection | No raw Unicode symbols (`★`, `→`, smart quotes) causing missing character warnings (`There is no ★ in font ec-lmb10!`) |

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
| Standard section headers used | `latex_section_check` | Headers exactly: `\section*{Professional Summary}`, `\section*{Work Experience}`, `\section*{Skills}`, `\section*{Education}`, `\section*{Projects}` |
| No contact info in header/footer | `latex_header_check` | Zero `fancyhdr` usage; `\contactline` only in body |

### 1.2 Typography & Engine-Agnostic Unicode (Critical for ATS & Zero Warnings)
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Engine-agnostic font & input encoding | `latex_unicode_check` | `\ifpdf` guard wrapping `cmap`, `glyphtounicode`, `[T1]{fontenc}`, and `[utf8]{inputenc}` for pdfLaTeX; native Unicode handling for XeLaTeX/LuaLaTeX |
| Zero overfull boxes / line-breaking tolerance | `latex_linebreaking_check` | `\emergencystretch=3em`, `\tolerance=1000`, `\hfuzz=0.5pt` present |
| Microtype enabled | `latex_microtype_check` | `\usepackage{microtype}` present |
| Font: mode-compatible | `latex_font_check` | `mathptmx` (`ats-max`) or `tgheros` (`designer-polish`) |
| Hyperref with hidelinks & PDF Metadata | `latex_hyperref_check` | `\usepackage[hidelinks]{hyperref}` + populated `\hypersetup{pdfauthor, pdftitle, pdfsubject, pdfkeywords}` |
| Section formatting (titlesec) | `latex_section_check` | Uppercase bold headers (`\MakeUppercase`) + rule; zero font shape warnings |

### 1.3 Dates & Sections
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Date format MM/YYYY | `latex_date_check` | All dates match `MM/YYYY` or `MM/YYYY – Present` |
| Section order valid | `latex_order_check` | Per career stage rules (§4 optimization-patterns.md) |

---

## 2. Keyword Density Gates

### 2.1 Algorithm (Implemented in `tools/validation_gates.py`)
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

### 2.4 Keyword Context Requirement
| Requirement | Check | Fix |
|-------------|-------|-----|
| Critical/High keywords appear in Experience bullets + Summary | `keyword_context_check` | Inject in top 2 bullets of most recent role + Summary |
| No keyword appears ONLY in Skills list | `keyword_distribution_check` | Move at least one occurrence to Experience/Summary |
| Keywords surrounded by action/outcome context (not list format) | `keyword_context_nlp` | Rewrite "Skills: Python, React" → "Built React dashboards with Python backend" |

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

### 3.2 Simulation Pipeline (Implemented in `tools/ats_parsers/`)
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
| Skills (all) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Experience (all) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Education | ✅ | ✅ | ✅ | ✅ | ✅ |
| Certifications | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| Projects | ⚠️ | ✅ | ❌ | ✅ | ❌ |
| Dates (MM/YYYY) | ✅ | ✅ | ✅ | ✅ | ✅ |

✅ = Full extraction | ⚠️ = Partial | ❌ = Not extracted

**Gate:** All required sections (Contact, Summary, Skills, Experience, Education, Dates) must extract correctly (✅). Optional sections (Certifications, Projects) may be ⚠️/❌.

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

### 3.5 Date Parser Stress Test (NEW — Zero Unparseable Ranges)

```python
# tools/validation_gates.validate_date_parsing()
import dateparser, re
text = open('main.normalized.txt').read()
ranges = re.findall(r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\,\/]*\d{2,4}|\b\d{1,2}/\d{2,4}|\b\d{4})\s*[\-\–\—to]+\s*(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\,\/]*\d{2,4}|\b\d{1,2}/\d{2,4}|\b\d{4}|Present|Current|Now|Ongoing)', text, re.I)
for start, end in ranges:
    d = dateparser.parse(end, settings={'PREFER_DAY_OF_MONTH': 'first'})
    if 'present' in end.lower() or 'current' in end.lower() or 'now' in end.lower() or 'ongoing' in end.lower():
        print(f'OK: {start} – Present')
    elif d:
        print(f'OK: {start} – {end}')
    else:
        raise ValueError(f'FAIL: Could not parse {start} – {end}')
```

**Gate:** Zero `FAIL` lines. Any unparseable date range = hard fail.

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

### 4.3 Normalized Extraction Stress Test (NEW — Parser Pipeline Fidelity)

```bash
# 1. Extract with layout
pdftotext -layout main.pdf main.txt

# 2. Normalize ligatures, bullets, dashes (NFKC + explicit maps)
python3 -c "
import unicodedata, re, sys
text = open('main.txt').read()
text = unicodedata.normalize('NFKC', text)
lig = {'ﬀ':'ff','ﬁ':'fi','ﬂ':'fl','ﬃ':'ffi','ﬄ':'ffl'}
for k,v in lig.items(): text = text.replace(k,v)
text = re.sub(r'[•‣▶◆◀◦▪▫●○✓✔➡\-–—*●]+', '-', text)
text = re.sub(r'–|—', '--', text)
open('main.normalized.txt','w').write(text)
"

# 3. Verify all job-analysis.json keywords still match
python -m ats_parsers.keyword_check main.normalized.txt job-analysis.json
```

| Glyph | Normalized To | Status |
|-------|---------------|--------|
| `fi`/`fl`/`ffi`/`ffl` ligatures | `fi`/`fl`/`ffi`/`ffl` | ✅ |
| All bullet variants (`• ▪ ◦ ● * -`) | `-` | ✅ |
| En/em dashes (`–` `—`) | `--` | ✅ |
| **Gate:** All job-analysis keywords found in `main.normalized.txt` | | **HARD FAIL** if any missing |

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
| Summary | **3-sentence template**: "[Role] with [years] experience in [domains]. [Method/skills]. [Passion/values — plain, no macros]." 3–5 bold keywords (`\kw{}`), 1–2 metrics, no pronouns, no macros in sentence 3 |
| Skills | Categorized (`\item \textbf{Category:} \kw{...}` bullets), exact keyword matches, verifiable in Experience |
| Experience | Reverse chron, 4–6 bullets current, 2–4 prior, all flipped STAR format |
| Education | 2-line format: `\eduentry{Degree}{Date}{Institution}{Location}` — degree + date on line 1, school + location on line 2 |
| Certifications | 2-line format: `\certentry{Cert Name}{Date}{Issuer}{}` — same rhythm as Education |
| Continuous Learning | If present, identical 2-line rhythm as Education/Certifications |
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

### 6.4 Flipped STAR & Quantification Gates (6-Second Scan Survival)
| Requirement | Check | Fix |
|-------------|-------|-----|
| Bullet opens with outcome metric ($, %, time, scale) | `star_lead_check` | Rewrite: "Increased conversion +9pp (18%→27%) by redesigning payment selector…" |
| Every metric includes baseline→target OR explicit scale context | `metric_context_check` | "12 teams" → "12 cross-functional product teams (3D/2E/1PM/1R each)" |
| No vague/round-only metrics without validation cite | `validation_cite_check` | Add "A/B test n=24,847, p<0.01" or "Usability n=12" |
| Active verb tier 1/2 (no "worked on", "helped", "assisted") | `verb_tier_check` | Upgrade: "Spearheaded", "Engineered", "Orchestrated" |

### 6.5 Metric Plausibility Guardrails (NEW)
| Rule | Check | Action if Violated |
|------|-------|-------------------|
| % gains >15% in <6 months require sample size (n=) | `metric_plausibility_check` | Flag → require "n=X" or downgrade to "~X% (directional)" |
| Session/interview counts exceed tenure duration | `tenure_consistency_check` | Flag → recalculate or remove |
| Duplicate metric values across bullets | `duplicate_metric_check` | Flag → consolidate or differentiate |
| "WCAG compliant" without version/level | `a11y_baseline_check` | Rewrite: "WCAG 2.1 AA as baseline standard" or "WCAG 2.2 AA achieved" |
| ARR/revenue claims without timeframe | `revenue_context_check` | Add "annual" or "quarterly" context |

### 6.6 Single Target Role Enforcement (NEW)
| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Header contains exactly ONE target role | `single_role_check` | No "&", "/", "or", "and" in role line — matches `job-analysis.json` role_title exactly |

### 6.7 Professional Summary Template Compliance (NEW)
| Requirement | Check | Fix |
|-------------|-------|-----|
| Exactly 3 sentences | `summary_sentence_count` | Enforce: Sentence 1 = role+years+domain; Sentence 2 = method/skills+metric; Sentence 3 = passion/values (plain) |
| Sentence 3 contains no macros (`\kw{}`, `\metric{}`, `\signaltag{}`) | `summary_plain_check` | Remove macros, use plain text only |
| 3–5 bold keywords in sentences 1–2 | `summary_keyword_check` | Inject from job-analysis.json critical/high list |
| 1–2 metrics in sentences 1–2 | `summary_metric_check` | Add outcome metric with context |

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
- `main-{company}-{role}-{YYYYMMDD}.pdf` — **Primary submission artifact** (pdflatex, Overleaf-compatible)
- `main-{company}-{role}-{YYYYMMDD}.txt` — Plain text fallback (pdftotext -layout)
- `main-{company}-{role}-{YYYYMMDD}.normalized.txt` — NFKC+ligature+bullet normalized text for parser simulation fidelity

---

## Sign-Off
**Status:** ✅ READY FOR SUBMISSION
**Validated by:** resume-doctor v2.1
**Next re-validation:** 2024-04-15 (quarterly)
```

---

## 9. Python Module Interface (Executable Gates)

**All pseudo-code `agent validate ...` commands replaced with direct Python calls:**

```python
# tools/validation_gates.py

from resume_doctor.validation_gates import (
    validate_latex_format,
    validate_keyword_density,
    validate_parser_simulation,
    validate_unicode_extraction,
    validate_readability,
    validate_audience_comprehension,
    validate_metric_plausibility,
    validate_single_role,
    validate_summary_template,
    validate_portfolio_crossref,
    run_all_gates
)

# Individual gate calls (return GateResult with passed, details, artifacts)
result = validate_latex_format(latex_path="main.tex")
result = validate_keyword_density(latex_path="main.tex", job_analysis="job-analysis.json")
result = validate_parser_simulation(latex_path="main.tex", parsers=["greenhouse", "lever", "workday", "icims", "taleo"])
result = validate_unicode_extraction(latex_path="main.tex")
result = validate_readability(latex_path="main.tex")
result = validate_audience_comprehension(latex_path="main.tex", job_analysis="job-analysis.json")
result = validate_metric_plausibility(latex_path="main.tex")
result = validate_single_role(latex_path="main.tex", job_analysis="job-analysis.json")
result = validate_summary_template(latex_path="main.tex", job_analysis="job-analysis.json")
result = validate_portfolio_crossref(latex_path="main.tex", portfolio_dir="./portfolio")

# Run all gates (used in Phase 5)
report = run_all_gates(latex_path="main.tex", job_analysis="job-analysis.json", mode="designer-polish")
# Returns ValidationReport with overall_passed: bool, gates: list[GateResult]
```

### GateResult Schema
```python
@dataclass
class GateResult:
    gate: str                    # e.g., "keyword_density"
    passed: bool
    details: dict                # Gate-specific details
    artifacts: list[str]         # Generated files (e.g., ["main.normalized.txt"])
```

### ValidationReport Schema
```python
@dataclass
class ValidationReport:
    overall_passed: bool
    gates: list[GateResult]
    generated_at: str
    job_ref: str
    candidate: str
```

---

## 10. CLI Entry Points

```bash
# Run single gate
python -m resume_doctor.validation_gates validate_latex_format --resume main.tex

# Run all gates
python -m resume_doctor.validation_gates run_all --resume main.tex --job job-analysis.json --mode designer-polish --out validation-report.json

# Quick check (format + density only)
python -m resume_doctor.validation_gates quick_check --resume main.tex --job job-analysis.json
```

---

## 11. Maintenance

- **Parser rules update:** Monthly (ATS vendor changes)
- **Density targets calibration:** Per-application A/B test → aggregate per company/role
- **Readability thresholds:** Annual review against industry benchmarks
- **Signal taxonomy:** Sync with internal signal tag taxonomy (§6 SKILL.md) quarterly
- **LaTeX template:** Review quarterly for Overleaf/TeX Live compatibility
- **Normalized extraction pipeline:** Verify ligature/bullet/dash maps quarterly (TeX Live updates)
- **Date parser patterns:** Update regex for new `Present` variants (e.g., "Ongoing", "Active")
- **Keyword context NLP:** Retrain quarterly on latest job-description corpus