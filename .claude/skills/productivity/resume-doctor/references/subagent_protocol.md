# Compile-Test Subagent Protocol & Harness Specification

This protocol defines the mandatory 5-subagent verification pass executed before finalizing any `resume-doctor` output (`tailor`, `review`, `ats-audit`, or `build`).

---

## Architecture Overview

When `resume-doctor` finishes creating or tailoring `main.tex`, it enters the **Compile-Test Subagent Harness**. The host agent spawns 5 specialized subagents to evaluate the LaTeX document independently against critical failure modes.

```
                  [ Generated main.tex ]
                            │
       ┌────────────────────┼────────────────────┬────────────────────┐
       ▼                    ▼                    ▼                    ▼
[1. Engine Compat]   [2. Char Escaping]   [3. ATS Structure]   [4. Unicode/Lig]   [5. Recruiter/Hygiene]
       │                    │                    │                    │                    │
       └────────────────────┴─────────┬──────────┴────────────────────┴────────────────────┘
                                      ▼
                        All 5 Subagents return PASS?
                                 /          \
                              YES             NO
                              /                 \
                     Final Deliverable   Apply Fixes & Re-run Failing Checks
```

---

## 1. Subagent Specifications & Expected Outputs

### Subagent 1: LaTeX Engine Compatibility Auditor
- **Role:** Verifies `main.tex` compiles cleanly on Overleaf across `pdfLaTeX`, `XeLaTeX`, and `LuaLaTeX`.
- **Target Checks:**
  1. `\pdfgentounicode=1` is guarded inside `\ifPDFTeX ... \fi` with `\usepackage{iftex}`.
  2. No bare `pdfLaTeX` primitives exist outside `\ifPDFTeX`.
  3. All used packages are properly declared in the preamble.
  4. Document is 100% self-contained.
- **Output Schema:**
  ```json
  {
    "auditor": "Engine Compatibility",
    "status": "PASS | FAIL",
    "line_references": [12, 18],
    "required_edits": ["Wrap \\pdfgentounicode=1 in \\ifPDFTeX conditional block"]
  }
  ```

### Subagent 2: LaTeX Reserved Character Escaping Auditor
- **Role:** Scans every non-comment line for unescaped reserved characters (`&`, `%`, `_`, `#`, `$`).
- **Target Checks:**
  1. No unescaped `&` outside `tabular`/`array` environments.
  2. No unescaped `%`, `_`, `#`, `$` in regular text or section headers.
  3. Safe strings inside `\hypersetup{}` metadata.
- **Output Schema:**
  ```json
  {
    "auditor": "Character Escaping",
    "status": "PASS | FAIL",
    "offending_lines": [{"line": 45, "text": "AT&T and 50% growth"}],
    "corrections": [{"line": 45, "replacement": "AT\\&T and 50\\% growth"}]
  }
  ```

### Subagent 3: ATS Parser Structure Auditor
- **Role:** Checks structure against Greenhouse, Lever, Workday, iCIMS, Taleo requirements.
- **Target Checks:**
  1. Standard canonical sections (`Professional Summary`, `Skills & Technical Proficiency`, `Experience`, `Education & Certifications`).
  2. Single consolidated skills/proficiency section (no split/fragmented skill sections).
  3. No multi-column layouts, tables, text boxes, or decorative graphics.
  4. Explicit date parsing (`MM/YYYY -- Present`).
- **Output Schema:**
  ```json
  {
    "auditor": "ATS Structure",
    "status": "PASS | FAIL",
    "parser_risk_rating": "LOW | MEDIUM | HIGH",
    "structural_changes_required": []
  }
  ```

### Subagent 4: Unicode and Ligature Extraction Auditor
- **Role:** Ensures zero PDF ligature artifacts (`ﬀ`, `ﬁ`, `ﬂ`, `ﬃ`, `ﬄ`) and reliable OCR/text extraction.
- **Target Checks:**
  1. Zero ligature chars (`ﬀ`, `ﬁ`, `ﬂ`, `ﬃ`, `ﬄ`) across source `.tex` and `.txt`.
  2. Guarded Unicode preamble present (`\ifPDFTeX \input{glyphtounicode} \pdfgentounicode=1 \fi`).
  3. Protects ATS keyword words (`handoff`, `efficiency`, `fluency`, `defined`, `workflow`, `Confluence`).
- **Output Schema:**
  ```json
  {
    "auditor": "Unicode & Ligatures",
    "status": "PASS | FAIL",
    "ligature_count": 0,
    "affected_words": [],
    "replacements": []
  }
  ```

### Subagent 5: Recruiter Scanner and Keyword Hygiene Auditor
- **Role:** Evaluates 6-10s human scan clarity & ATS keyword prominence.
- **Target Checks:**
  1. Zero bracketed signal tags (`[systems-thinking]`, `[technical-fluency]`, etc.) in output.
  2. High-priority role keywords present naturally.
  3. Plausible impact metrics (`%`, `$`, scale/scope numbers) present in experience bullets.
- **Output Schema:**
  ```json
  {
    "auditor": "Recruiter & Keyword Hygiene",
    "status": "PASS | FAIL",
    "top_recruiter_risks": [],
    "bullet_suggestions": []
  }
  ```

---

## 2. Hard Gate Execution Policy

1. Every command outputting a final resume (`tailor`, `review`, `build`, `ats-audit`) runs all 5 subagent audits.
2. If **any** subagent returns `FAIL`, the `resume-doctor` agent automatically applies the specified corrections to `main.tex` and re-evaluates the failed checks.
3. Only when all 5 audits return `PASS` does the agent deliver the final output summary to the user, reporting the validation status table.
