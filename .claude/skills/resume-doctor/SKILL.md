---
name: resume-doctor
description: ATS-focused professional resume doctor. Ingests job listings (URLs/docs), extracts requirements & keyword targets, analyzes candidate profile gaps, rewrites resumes in clean Overleaf-compatible LaTeX (.tex) format, validates against ATS parser simulations via pdflatex + pdftotext (Greenhouse, Lever, Workday, iCIMS, Taleo). Outputs a single self-contained main.tex file ready for pdflatex compilation.
---

# Resume Doctor — Operating Manual

**Version:** 2.0 (Executable Tool Interface)  
**Last Updated:** 2026-07-12

---

## 0. CLI / Tool Interface Specification

### 0.1 Core Commands

This skill exposes **three executable entry points** via a unified CLI. All commands produce validated JSON artifacts.

| Command | Purpose | Job Target Required? |
|---------|---------|---------------------|
| `resume-doctor ats-audit --resume <file> [--out <file>] [--session-dir <dir>] [--no-prompt]` | General ATS audit (format, structure, readability, Unicode extraction, parser simulation) | ❌ No |
| `resume-doctor tailor --resume <file> --job <url\|file> --mode <ats-max\|designer-polish> [--session-dir <dir>] [--no-prompt] [--name <base>] [--portfolio <file>] [--phase <1-5>]` | Full 5-phase targeted optimization | ✅ Yes |
| `resume-doctor review --resume <file> --job <url\|file> --phase <1-5> [--auto-approve] [--session-dir <dir>] [--no-prompt]` | Run phases 1-N with interactive gate enforcement | ✅ Yes |
| `resume-doctor analyze --job <url\|file> [--company <name>] [--session-dir <dir>] [--no-prompt] [--out <file>]` | Analyze job description to produce job-analysis.json | ✅ Yes |
| `resume-doctor build --resume <file> --job <url\|file> --mode <ats-max\|designer-polish> [--session-dir <dir>] [--no-prompt] [--name <base>]` | Build PDF from optimized LaTeX | ✅ Yes |

### 0.1.1 Session Directory Management

**All commands support session-scoped output directories** for organizing multi-run workflows:

| Flag | Behavior |
|------|----------|
| `--session-dir <path>` | Explicit session directory (created if not exists) |
| `--no-prompt` | Skip interactive prompt, use auto-generated name |
| *(neither flag)* | Prompt user for session name with auto-generated default |

**Auto-generated session name format:** `{resume_stem}__{job_stem}_{YYYYMMDD_HHMMSS}` (URL jobs use `url_<hash>`).

**Example session directory structure:**
```
output/
├── my_resume__senior_pd_20260712_143022/
│   ├── my_resume_tailored.tex
│   ├── my_resume_tailored.pdf
│   ├── my_resume_tailored.txt
│   ├── my_resume_normalized.txt
│   ├── my_resume_gap_report.md
│   ├── my_resume_injection_map.json
│   ├── my_resume_audit.json
│   ├── my_resume_validation.json
│   ├── my_resume_run_context.json
│   └── my_resume_job_analysis.json
```

All artifacts (optimized `.tex`, PDF, extracted text, gap reports, injection maps, audit results, validation reports, run context) are written into the session directory by default.

### 0.2 JSON I/O Contracts (Input/Output Schemas)

All commands consume and produce JSON files with the following schemas (defined in `schemas/`):

| Artifact | Schema File | Produced By | Consumed By |
|----------|-------------|-------------|-------------|
| `job-analysis.json` | `schemas/job-analysis.json` | Phase 1 / `job_analyzer.analyze()` | Phases 2-5 |
| `candidate-profile.yaml` | `schemas/candidate-profile.yaml` | Phase 2 / `profile_builder.build()` | Phase 3 |
| `gap-report.md` | `schemas/gap-report.md` (frontmatter) | Phase 3 / `gap_analyzer.analyze()` | Phase 4 |
| `keyword-injection-map.json` | `schemas/keyword-injection-map.json` | Phase 3 / `gap_analyzer.analyze()` | Phase 4 |
| `ats-audit.json` | `schemas/ats-audit.json` | `ats_audit.run()` / Phase 1 `ats-audit` cmd | — |
| `validation-report.json` | `schemas/validation-report.json` | Phase 5 / `validation_gates.run_all()` | — |
| `build-result.json` | `schemas/build-result.json` | `latex_builder.build()` | — |

### 0.3 Python Module Interface (for Agent Use)

Agents MUST call these modules directly — **never invoke pseudo-commands** like `agent job analyze`:

```python
# Job Analysis
from resume_doctor.job_analyzer import analyze_job
job = analyze_job(source="https://...", source_type="url")

# Candidate Profile
from resume_doctor.profile_builder import build_profile
profile = build_profile(resume_path="main.tex", linkedin_path="linkedin.pdf")

# Gap Analysis
from resume_doctor.gap_analyzer import analyze_gaps
gap_report, injection_map = analyze_gaps(job, profile)

# Optimization
from resume_doctor.optimizer import optimize_resume
optimized_latex = optimize_resume(latex, injection_map, mode="designer-polish")

# Validation
from resume_doctor.validation_gates import run_all_gates
report = run_all_gates(optimized_latex, job, mode="designer-polish")

# Build
from resume_doctor.latex_builder import build_resume
result = build_resume(optimized_latex, job, mode="designer-polish")

# ATS Audit (no job target)
from resume_doctor.ats_audit import run_ats_audit
audit = run_ats_audit(latex_path="main.tex")
```

---

## 1. Modes of Operation

### 1.1 Targeted Optimization (`tailor` command)

**Full 5-phase pipeline** with a specific job target:

```
Phase 1: Job Analysis     → job-analysis.json
Phase 2: Candidate Inventory → candidate-profile.yaml
Phase 3: Gap Analysis     → gap-report.md + keyword-injection-map.json
Phase 4: Optimization     → optimized.tex (surgical edits)
Phase 5: Validation       → validation-report.json (ALL gates PASS)
Build:                    → PDF + extracted text + build-result.json
```

**Phase Gates:** Each phase requires explicit confirmation (interactive) or `--auto-approve`.

### 1.2 General ATS Audit (`ats-audit` command)

**No job target required.** Validates resume against universal ATS best practices:

| Check | Description |
|-------|-------------|
| **Format Compliance** | Linear flow, no tables/columns/graphics, cmap+glyphtounicode, T1/UTF8 |
| **Structure Completeness** | Required sections present (Summary, Experience, Skills, Education) |
| **Keyword Hygiene** | No stuffing (>3.5%), no missing core skills, variant coverage |
| **Readability Baseline** | Flesch-Kincaid ≥ 30, Gunning Fog ≤ 14, sentence length ≤ 25 words |
| **Unicode Extraction** | pdftotext -layout recovers ≥98% chars, ligatures resolved |
| **Parser Simulation** | Greenhouse, Lever, Workday, iCIMS, Taleo all parse core sections |

Output: `ats-audit.json` with `{passed: bool, findings: [], score: 0-100}`.

---

## 2. Phase Gates (Enforced)

| Gate | Trigger | Required Artifact | Validation |
|------|---------|-------------------|------------|
| **Gate 1** | Phase 1 complete | `job-analysis.json` | Schema valid, keyword_targets populated, company_intel present |
| **Gate 2** | Phase 2 complete | `candidate-profile.yaml` | Schema valid, skills taxonomy mapped, years_experience computed |
| **Gate 3** | Phase 3 complete | `gap-report.md` + `keyword-injection-map.json` | Critical gaps ≤ 3, injection map covers all critical/high gaps |
| **Gate 4** | Phase 4 complete | `optimized.tex` | Density within targets, no keyword stuffing, signal tags valid |
| **Gate 5** | Phase 5 complete | `validation-report.json` | **ALL 10 gates PASS** |

**Enforcement:** `validation_gates.PhaseGate` decorator + CLI `--phase` flag.

---

## 3. Dual Layout Modes (ATS-Safe Both)

| Property | `ats-max` | `designer-polish` |
|----------|-----------|-------------------|
| **Density** | Maximum (1.02 line stretch, tight margins) | Comfortable (1.08 line stretch, generous margins) |
| **Skills Position** | After Experience (ATS-first) | Top third (human scan) |
| **Signal Tags** | Inline text `[Tag]` | Badged `\signaltag{Tag}` (ATS-visible fallback) |
| **Section Rules** | Thin (0.4pt) | Medium (0.6pt) + color |
| **Typography** | System fonts only | `tgheros` (Helvetica-like) |
| **Color** | Monochrome | Semantic palette (muted, print-safe) |
| **Page Target** | 1 page if ≤8 yrs exp | 2 pages max |

**Both modes guarantee:** Linear flow, Unicode extraction, no tables/graphics/text boxes, PDF metadata injection.

---

## 4. Keyword Density Targets (Per Job Analysis)

Generated by `job_analyzer.build_keyword_targets()` from job posting frequency:

| Priority | Min Density | Max Density | Typical Terms |
|----------|-------------|-------------|---------------|
| Critical | 2.0% | 3.5% | Role-defining skills, tools, domains |
| High | 1.5% | 3.0% | Core competencies, methodologies |
| Medium | 1.0% | 2.5% | Supporting skills, soft skills |
| Low | 0.5% | 1.5% | Nice-to-have, adjacent domains |

**Enforcement:** `optimizer.calibrate_density()` + `validation_gates.validate_keyword_density()`.

---

## 5. Signal Tag Taxonomy (Controlled Vocabulary)

**10 tags only** — defined in `references/signals.json`:

| Tag | Display | Triggers |
|-----|---------|----------|
| `data-informed-iteration` | Data-Informed Iteration | Metrics, A/B testing, analytics-driven decisions |
| `cross-functional-leadership` | Cross-functional Leadership | Leading PM/Eng/Design collaboration |
| `systems-thinking` | Systems Thinking | Design systems, component library, tokens, governance |
| `technical-fluency` | Technical Fluency | Code (React, TS), prototypes in Storybook, eng collaboration |
| `user-research-rigor` | User Research Rigor | Interviews, usability tests, JTBD, synthesis → decisions |
| `accessibility-advocacy` | Accessibility Advocacy | WCAG audit, inclusive patterns, training, bug reduction |
| `craft-polish` | Craft & Polish | Motion specs, edge cases, pixel-perfect, design QA |
| `zero-to-one-ambiguity` | 0→1 Ambiguity | Defined problem, strategy from scratch, shipped v1 |
| `strategic-influence` | Strategic Influence | Roadmap change, budget secured, exec memo, org process change |
| `mentorship-culture` | Mentorship & Culture | Mentees promoted, rituals created, hiring panels |

**Validation:** `validation_gates.validate_signal_tags()` — rejects invented tags.

---

## 6. NDA Abstraction Ladder (5 Levels)

Applied via `optimizer.apply_nda_abstraction(latex, level)`:

| Level | Description | Example Transformation |
|-------|-------------|------------------------|
| **L0** | Public | "Stripe Payments API" |
| **L1** | Category | "Major payments platform API" |
| **L2** | Domain + Scale | "High-volume fintech payment processing (10M+ txn/day)" |
| **L3** | Problem + Outcome | "Reduced payment failure rate 40% via intelligent retry logic" |
| **L4** | Outcome Only | "Cut transaction failures 40% through retry optimization" |

**Default:** L2 for portfolio, L3 for applications. User specifies via `--nda-level`.

---

## 7. Audience-Aware Writing (Comprehension Gates)

Transformed by `optimizer.apply_audience_aware(latex, job_analysis)`:

| Audience | Gate | Transformation |
|----------|------|----------------|
| **HR/Recruiter** | Keywords + outcomes visible in 6s scan | Lead with metric, expand acronyms |
| **Hiring Manager** | Scope/scale/impact clear in 30s | Add team size, budget, timeline context |
| **Technical Lead** | Implementation credibility | Name tools, patterns, technical decisions |
| **Executive** | Strategic value + business outcome | Revenue/retention/cost impact, not tasks |

---

## 8. File I/O Conventions

```
project/
├── resume/
│   ├── main.tex                 # Master resume (source of truth)
│   ├── job-analysis.json        # Per-application (generated)
│   ├── candidate-profile.yaml   # Per-application (generated)
│   └── output/
│       └── {company}-{role}-{YYYYMMDD}/
│           ├── optimized.tex
│           ├── resume.pdf
│           ├── resume.txt       # pdftotext -layout
│           ├── build-result.json
│           ├── gap-report.md
│           ├── keyword-injection-map.json
│           └── validation-report.json
```

**CLI Flags:** `--resume-dir`, `--output-dir`, `--job-file` (instead of URL).

---

## 9. Quick Start

```bash
# 1. General ATS Audit (no job target)
resume-doctor ats-audit --resume resume/main.tex --out resume/ats-audit.json

# 2. Targeted optimization for a specific job (auto session dir)
resume-doctor tailor \
  --resume resume/main.tex \
  --job-url "https://boards.greenhouse.io/stripe/jobs/12345" \
  --mode designer-polish

# 3. Targeted optimization with explicit session directory
resume-doctor tailor \
  --resume resume/main.tex \
  --job-file resume/job-analysis.json \
  --mode ats-max \
  --session-dir resume/output/stripe-senior-pd-20260712

# 4. Review with phase gates (interactive)
resume-doctor review \
  --resume resume/main.tex \
  --job-file resume/output/stripe-senior-pd-20260712/job-analysis.json \
  --phase 5

# 5. Analyze job description only
resume-doctor analyze --job "https://jobs.example.com/123" --company "Acme Corp"

# 6. Build PDF from optimized LaTeX
resume-doctor build \
  --resume resume/output/stripe-senior-pd-20260712/my_resume_tailored.tex \
  --job resume/output/stripe-senior-pd-20260712/job-analysis.json \
  --mode designer-polish
```

---

## 10. Artifact Contracts (JSON Schemas)

All schemas in `schemas/` directory. Key schemas:

### 10.1 `job-analysis.json`
```json
{
  "meta": {"source_url": "", "source_type": "", "extracted_at": "", "extractor_version": ""},
  "company": "", "role_title": "", "role_level": "", "employment_type": "",
  "location": "", "visa_sponsorship": false, "remote_policy": "",
  "description_raw": "",
  "must_have": {"hard_skills": [], "soft_skills": [], "tools": [], "domain_knowledge": [], "years_experience": "", "education": ""},
  "nice_to_have": {"hard_skills": [], "certifications": [], "domain": []},
  "keywords_at_freq": {},
  "keyword_targets": {"term": {"min": 0.0, "max": 0.0, "priority": "critical|high|medium|low"}},
  "ats_signals": {"preferred_format": "PDF", "required_sections": [], "avoid": [], "keyword_density_target": "", "parser": ""},
  "company_intel": {"stage": "", "size": "", "founded": 0, "culture_keywords": [], "tech_stack": [], "design_maturity": "", "design_leadership": "", "recent_news": [], "glassdoor_rating": 0.0, "interview_process": [], "compensation_band": {}}
}
```

### 10.2 `keyword-injection-map.json`
```json
{
  "injections": [
    {"keyword": "design systems", "target_density": 2.5, "current_density": 0.8, "locations": ["summary", "experience:0", "skills"], "variant": "design system"}
  ]
}
```

### 10.3 `validation-report.json`
```json
{
  "overall_passed": true,
  "gates": [
    {"gate": "latex_format", "passed": true, "details": {}},
    {"gate": "keyword_density", "passed": true, "details": {"term": "figma", "actual": 1.8, "target_min": 1.5, "target_max": 3.0}},
    {"gate": "parser_simulation", "passed": true, "details": {"parsers": ["greenhouse", "lever", "workday", "icims", "taleo"]}},
    {"gate": "unicode_extraction", "passed": true, "details": {"recovery_rate": 0.99}},
    {"gate": "readability", "passed": true, "details": {"flesch_kincaid": 45.2, "gunning_fog": 11.3}},
    {"gate": "audience_comprehension", "passed": true, "details": {}},
    {"gate": "metric_plausibility", "passed": true, "details": {}},
    {"gate": "single_role", "passed": true, "details": {}},
    {"gate": "summary_template", "passed": true, "details": {}},
    {"gate": "portfolio_crossref", "passed": true, "details": {}}
  ]
}
```

---

## 11. Tool Implementation Status

| Module | File | Status |
|--------|------|--------|
| `job_analyzer.py` | `tools/job_analyzer.py` | 🟡 Stub — needs implementation |
| `profile_builder.py` | `tools/profile_builder.py` | 🟡 Stub — needs implementation |
| `gap_analyzer.py` | `tools/gap_analyzer.py` | 🟡 Stub — needs implementation |
| `optimizer.py` | `tools/optimizer.py` | 🟡 Stub — needs implementation |
| `validation_gates.py` | `tools/validation_gates.py` | 🟡 Stub — needs implementation |
| `latex_builder.py` | `tools/latex_builder.py` | 🟡 Stub — needs implementation |
| `ats_audit.py` | `tools/ats_audit.py` | 🟡 Stub — needs implementation |
| `ats_parsers/` | `tools/ats_parsers/` | 🟡 Stub — needs implementation |
| `signal_tagger.py` | `tools/signal_tagger.py` | 🟡 Stub — needs implementation |
| `audience_translator.py` | `tools/audience_translator.py` | 🟡 Stub — needs implementation |
| `metric_plausibility.py` | `tools/metric_plausibility.py` | 🟡 Stub — needs implementation |
| `portfolio_crossref.py` | `tools/portfolio_crossref.py` | 🟡 Stub — needs implementation |

**Next Step:** Implement all modules in `tools/` with JSON I/O matching schemas.