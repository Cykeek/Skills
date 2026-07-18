# Mandatory Pre-Submission Subagent Validation Checklist

Before delivering any final `main.tex`, `audit-summary.md`, `ats-audit.json`, or `OVERLEAF_INSTRUCTIONS.md`, the `resume-doctor` skill MUST evaluate the generated LaTeX across these five hard-gate checklists. The final answer is blocked until all five return PASS or their findings are fixed and rechecked.

---

## Subagent 1: LaTeX Engine Compatibility Auditor

**Task:**
Review `main.tex` for compatibility with Overleaf using `pdfLaTeX`, `XeLaTeX`, and `LuaLaTeX`.

**Checklist:**
- [ ] Verify `\pdfgentounicode=1` is never used bare at root preamble level.
- [ ] Verify the preamble contains the exact engine-safe guard block:
  ```latex
  \usepackage{iftex}
  \ifPDFTeX
    \usepackage[T1]{fontenc}
    \usepackage[utf8]{inputenc}
    \input{glyphtounicode}
    \pdfgentounicode=1
  \fi
  ```
- [ ] Verify no `pdfLaTeX`-only primitive appears outside `\ifPDFTeX`.
- [ ] Verify all packages used in the document are declared in the preamble.
- [ ] Verify the document is self-contained and does not depend on local images, fonts, `.sty` files, or external assets.

**Output:**
Return `PASS` or `FAIL`, plus exact line references and required edits.

---

## Subagent 2: LaTeX Reserved Character Escaping Auditor

**Task:**
Scan every non-comment line of `main.tex` for unescaped LaTeX reserved characters in body text, headings, metadata, URLs, and bullets.

**Checklist:**
- [ ] Bare `&` must not appear outside valid alignment environments (e.g. `tabular`). Use `\&` in regular text.
- [ ] Literal percentages must be written as `\%`.
- [ ] Literal underscores must be written as `\_` unless inside a URL handled by `\href`.
- [ ] Literal hashes must be written as `\#`.
- [ ] Literal dollar signs must be written as `\$`.
- [ ] PDF metadata fields inside `\hypersetup{}` must avoid or escape special characters. Prefer plain words like `and` instead of `&`.
- [ ] Verify section titles like `Skills \& Technical Proficiency` and `Education \& Certifications` are escaped properly.

**Output:**
Return `PASS` or `FAIL`, exact offending lines, and corrected replacements.

---

## Subagent 3: ATS Parser Structure Auditor

**Task:**
Evaluate whether the generated resume structure is clean for Greenhouse, Lever, Workday, iCIMS, and Taleo.

**Checklist:**
- [ ] Resume must use standard canonical sections:
  - `Professional Summary`
  - `Skills & Technical Proficiency` (or `Skills`)
  - `Experience` (or `Work Experience`)
  - `Key Projects` if needed
  - `Education & Certifications` (or `Education`)
- [ ] There must be only one skills/proficiency section. Do not split into separate `Core Skills` and `Technical Proficiency` sections that fragment ATS parsing.
- [ ] Avoid tables, multi-column layouts, text boxes, icons, image-only content, and decorative graphics.
- [ ] Contact info must be plain text and extractable.
- [ ] Dates must be explicit and parser-friendly, e.g. `04/2025 -- Present` or `01/2020 -- 03/2024`.
- [ ] Role, company, date, location, and domain context must be clearly separated.

**Output:**
Return `PASS` or `FAIL`, parser risk rating, and exact structural changes required.

---

## Subagent 4: Unicode and Ligature Extraction Auditor

**Task:**
Check whether the source resume text and generated LaTeX avoid problematic glyph extraction.

**Checklist:**
- [ ] Detect ligatures: `ﬀ`, `ﬁ`, `ﬂ`, `ﬃ`, `ﬄ`.
- [ ] Ensure all generated text uses normal ASCII sequences: `ff`, `fi`, `fl`, `ffi`, `ffl`.
- [ ] Ensure generated LaTeX preamble includes the engine-safe Unicode guard (`\ifPDFTeX \input{glyphtounicode} \pdfgentounicode=1 \fi`).
- [ ] Confirm text extraction should recover at least 98% of characters.
- [ ] Flag words where ligatures would break ATS keyword matching, such as:
  - `handoff`
  - `efficiency`
  - `fluency`
  - `defined`
  - `workflow`
  - `Confluence`

**Output:**
Return `PASS` or `FAIL`, ligature count, affected words, and replacements.

---

## Subagent 5: Recruiter Scanner and Keyword Hygiene Auditor

**Task:**
Evaluate the resume like a recruiter scanning for 6-10 seconds and like an ATS keyword parser.

**Checklist:**
- [ ] Remove bracketed tags like `[systems-thinking]`, `[technical-fluency]`, `[accessibility-advocacy]`.
- [ ] Convert tags into natural language inside bullets.
- [ ] Verify high-priority skills are present naturally:
  - Figma
  - Design Systems
  - Design Tokens
  - Component Libraries
  - React
  - TypeScript
  - Tailwind CSS
  - WCAG 2.1 / 2.2 AA
  - User Research
  - A/B Testing
  - Analytics
- [ ] Verify impact metrics appear where plausible.
- [ ] Flag vague bullets that lack scope, scale, or outcome.

**Output:**
Return `PASS` or `FAIL`, top recruiter risks, and replacement bullet suggestions.

---

## Final Gate Contract

- No final answer is permitted until all 5 checklist sections audit as `PASS`.
- If any checklist returns `FAIL`, apply exact edits to `main.tex` and re-run all failing checks until `PASS`.
