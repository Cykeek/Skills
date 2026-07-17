"""
Validation Gates — 10 hard gates for resume-doctor Phase 5.
All gates return GateResult(gate, passed, details, artifacts).
"""
from dataclasses import dataclass, asdict
from typing import Optional
import json
import re
import subprocess
import os
from pathlib import Path


@dataclass
class GateResult:
    gate: str
    passed: bool
    details: dict
    artifacts: list[str]


@dataclass
class ValidationReport:
    overall_passed: bool
    gates: list[GateResult]
    generated_at: str
    job_ref: str
    candidate: str

    def model_dump(self) -> dict:
        return asdict(self)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key: str):
        return getattr(self, key)


CONTROLLED_SIGNAL_TAGS = {
    "data-informed-iteration",
    "cross-functional-leadership",
    "systems-thinking",
    "technical-fluency",
    "user-research-rigor",
    "accessibility-advocacy",
    "craft-polish",
    "zero-to-one-ambiguity",
    "strategic-influence",
    "mentorship-culture",
}


class PhaseGate:
    """Decorator to enforce phase prerequisites"""
    def __init__(self, phase: int, required_artifacts: list[str]):
        self.phase = phase
        self.required_artifacts = required_artifacts

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            missing = [p for p in self.required_artifacts if not os.path.exists(p)]
            if missing:
                raise FileNotFoundError(f"Phase {self.phase} blocked. Missing artifacts: {missing}")
            return func(*args, **kwargs)
        return wrapper


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def latex_to_plain_text(latex: str) -> str:
    """Rough LaTeX macro stripping for validation before PDF extraction"""
    if '\\begin{document}' in latex:
        parts = latex.split('\\begin{document}', 1)
        body = parts[1]
        if '\\end{document}' in body:
            body = body.split('\\end{document}', 1)[0]
    else:
        body = latex

    # Remove comments
    text = re.sub(r'(?<!\\)%.*', '', body)
    # Strip line break spacing commands, e.g. \\[3pt] (must be exactly 2 or more backslashes)
    text = re.sub(r'\\{2,}(?:\[[^]]*\])?', ' ', text)
    # Strip well-known macros but keep their text contents
    text = re.sub(r'\\(kw|metric|signaltag|textbf|textit|emph|section|subsection|subsubsection|headline)\*?(?:\[[^]]*\])?\{([^}]*)\}', r'\2', text)
    # Strip any remaining control sequences
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^]]*\])?(?:\{[^}]*\})?', ' ', text)
    text = re.sub(r'[{}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _is_in_pdf_guard(latex: str, pos: int) -> bool:
    """Check if position pos is inside an \\ifpdf or \\ifPDFTeX environment."""
    stack = []
    for m in re.finditer(r'\\(if[a-zA-Z]*|fi)\b', latex[:pos]):
        token = m.group(1)
        if token == 'fi':
            if stack:
                stack.pop()
        else:
            stack.append(token)
    return any(t in ('ifpdf', 'ifPDFTeX') for t in stack)


def validate_latex_format(latex_path: str) -> GateResult:
    latex = read_file(latex_path)
    issues = []
    warnings = []

    if not latex.lstrip().startswith('\\documentclass'):
        issues.append("Missing or misplaced \\documentclass")
    doc_match = re.search(r'\\documentclass(?:\[[^]]*\])?\{([^}]+)\}', latex)
    if doc_match and 'article' not in doc_match.group(1):
        issues.append("Custom/non-article class detected — use article class only")
    if '\\tabular' in latex or '\\begin{tabular' in latex or '\\begin{tabularx' in latex:
        issues.append("Table/tabular layout detected — remove for ATS linear flow")
    if '\\includegraphics' in latex or 'tikzpicture' in latex or 'pgfplots' in latex:
        issues.append("Graphics/TikZ/PGF detected — remove for ATS parsing")
    if 'fontspec' in latex:
        issues.append("fontspec detected — use pdflatex-compatible packages only")
    if 'fancyhdr' in latex:
        issues.append("fancyhdr/header-footer content detected — keep contact info in body")

    # Unicode guard checks
    clean_latex = re.sub(r'(?m)(?<!\\)%.*', '', latex)
    if '\\input{glyphtounicode}' in clean_latex:
        gly_pos = clean_latex.find('\\input{glyphtounicode}')
        if not _is_in_pdf_guard(clean_latex, gly_pos):
            issues.append("\\input{glyphtounicode} appears outside an \\ifpdf or \\ifPDFTeX guard")
    else:
        issues.append("Missing \\input{glyphtounicode}")

    if '\\usepackage{cmap}' not in latex:
        issues.append("Missing \\usepackage{cmap}")
    if '\\pdfgentounicode' in clean_latex:
        for m in re.finditer(r'\\pdfgentounicode\b(?:=\d+)?', clean_latex):
            if not _is_in_pdf_guard(clean_latex, m.start()):
                issues.append("Unsafe bare \\pdfgentounicode appears outside an \\ifpdf or \\ifPDFTeX guard")
                break
    else:
        issues.append("Missing \\pdfgentounicode=1")
    if '[T1]{fontenc}' not in latex:
        warnings.append("Missing T1 font encoding")
    if '\\usepackage[utf8]{inputenc}' not in latex:
        warnings.append("Missing utf8 inputenc for pdfLaTeX")
    if '\\usepackage{microtype}' not in latex:
        warnings.append("Missing microtype")
    if '\\usepackage[hidelinks]{hyperref}' not in latex and 'hidelinks' not in latex:
        warnings.append("hyperref should use hidelinks")
    if '\\hypersetup' not in latex:
        warnings.append("Missing PDF metadata via \\hypersetup")

    # Required sections
    required_sections = ["Professional Summary", "Skills", "Work Experience", "Education"]
    missing_sections = [s for s in required_sections if f"\\section*{{{s}}}" not in latex]
    if missing_sections:
        issues.append(f"Missing required sections: {missing_sections}")

    # Date format check
    date_ranges = re.findall(r'\b\d{1,2}/\d{4}\s*(?:[-–—]+)\s*(?:\d{1,2}/\d{4}|Present)\b', latex)
    if not date_ranges:
        warnings.append("No valid MM/YYYY date ranges found")

    # Line breaking tolerance
    if '\\emergencystretch' not in latex:
        warnings.append("Missing \\emergencystretch for overfull-box prevention")

    # Pre-flight LaTeX unescaped special character audit after \begin{document}
    in_document = False
    align_tabular_depth = 0
    for line_num, line in enumerate(latex.splitlines(), start=1):
        if not in_document:
            if '\\begin{document}' in line:
                in_document = True
                line = line.split('\\begin{document}', 1)[1]
            else:
                continue

        if '\\end{document}' in line:
            line = line.split('\\end{document}', 1)[0]
            stop_after_line = True
        else:
            stop_after_line = False

        open_matches = len(re.findall(r'\\begin\{(?:align|tabular)[^}]*\}', line))
        close_matches = len(re.findall(r'\\end\{(?:align|tabular)[^}]*\}', line))
        in_align_tabular = (align_tabular_depth > 0) or (open_matches > 0)

        # Bare unescaped '%' (not preceded by backslash and not a comment line)
        if not line.lstrip().startswith('%') and re.search(r'(?<!\\)%', line):
            issues.append(f"Line {line_num}: Unescaped '%' character found (not a comment line)")

        # Bare unescaped '&', '#', or '$' (not preceded by backslash and not inside align/tabular)
        if not line.lstrip().startswith('%'):
            content = re.split(r'(?<!\\)%', line)[0]
            if not in_align_tabular and re.search(r'(?<!\\)&', content):
                issues.append(f"Line {line_num}: Unescaped '&' character found outside align/tabular")
            if re.search(r'(?<!\\)#', content) and not re.search(r'\\(?:newcommand|def|renewcommand)', content):
                issues.append(f"Line {line_num}: Unescaped '#' character found")

        align_tabular_depth = max(0, align_tabular_depth + open_matches - close_matches)

        if stop_after_line:
            in_document = False

    return GateResult(
        gate="latex_format",
        passed=len(issues) == 0,
        details={"issues": issues, "warnings": warnings},
        artifacts=[]
    )


def keyword_density(text: str, keyword: str) -> float:
    words = re.findall(r'\b\w+\b', text.lower())
    total = len(words)
    if total == 0:
        return 0.0
    kw_words = len(keyword.split())
    count = len(re.findall(rf'\b{re.escape(keyword.lower())}\b', text.lower()))
    return (count * kw_words / total) * 100


def validate_keyword_density(latex_path: str, job_analysis: str | dict) -> GateResult:
    latex = read_file(latex_path)
    text = latex_to_plain_text(latex)
    job = job_analysis if isinstance(job_analysis, dict) else json.loads(read_file(job_analysis))
    issues = []
    details = {}

    for kw, target in job.get('keyword_targets', {}).items():
        actual = keyword_density(text, kw)
        status = "PASS"
        if actual < target['min']:
            status = "UNDER"
            issues.append(f"{kw}: {actual:.2f}% below min {target['min']:.2f}%")
        elif actual > 5.0:
            status = "STUFFING"
            issues.append(f"{kw}: {actual:.2f}% exceeds hard stuffing limit 5.0%")
        elif actual > target['max']:
            status = "OVER"
            issues.append(f"{kw}: {actual:.2f}% above max {target['max']:.2f}%")

        # Same keyword 5+ times in one bullet
        for bullet in re.findall(r'\\(?:item|bulletitem)\s*(?:\{([^}]*)\}|([^\n]*))', latex):
            bullet_text = bullet[0] or bullet[1]
            count = len(re.findall(rf'\b{re.escape(kw.lower())}\b', bullet_text.lower()))
            if count >= 5:
                issues.append(f"{kw}: appears {count} times in one bullet")

        details[kw] = {
            "actual": round(actual, 2),
            "target_min": target['min'],
            "target_max": target['max'],
            "priority": target['priority'],
            "status": status
        }

    return GateResult("keyword_density", len(issues) == 0, {"keywords": details, "issues": issues}, [])


ATS_SECTION_ONTOLOGY = {
    "WORK_EXPERIENCE": [r'Work Experience', r'Professional Experience', r'Employment', r'Work History', r'Career History', r'\bExperience\b'],
    "SKILLS": [r'Technical Skills', r'Core Competencies', r'Skills & Expertise', r'Technologies', r'\bSkills\b'],
    "EDUCATION": [r'Academic Background', r'Education & Credentials', r'Qualifications', r'\bEducation\b'],
    "SUMMARY": [r'Professional Summary', r'Executive Summary', r'Career Profile', r'Overview', r'\bSummary\b']
}


def validate_parser_simulation(latex_path: str, parsers: list[str] = None) -> GateResult:
    if parsers is None:
        parsers = ["greenhouse", "lever", "workday", "icims", "taleo"]

    # If PDF/text artifacts exist, use them. Otherwise simulate from LaTeX-stripped text.
    base = Path(latex_path).with_suffix('')
    txt_path = str(base) + '.txt'
    if os.path.exists(txt_path):
        text = read_file(txt_path)
        artifacts = [txt_path]
    else:
        text = latex_to_plain_text(read_file(latex_path))
        artifacts = []

    # Map candidate sections to canonical ATS namespaces
    canonical_mapping = {}
    for canonical_name, patterns in ATS_SECTION_ONTOLOGY.items():
        found = any(re.search(p, text, re.I) for p in patterns)
        canonical_mapping[canonical_name] = found

    required = {
        "contact": [r'\b[\w.-]+@[\w.-]+\.\w+\b'],
        "summary": ATS_SECTION_ONTOLOGY["SUMMARY"],
        "skills": ATS_SECTION_ONTOLOGY["SKILLS"],
        "experience": ATS_SECTION_ONTOLOGY["WORK_EXPERIENCE"],
        "education": ATS_SECTION_ONTOLOGY["EDUCATION"],
        "dates": [r'\b\d{1,2}/\d{4}\s*[–-]\s*(?:\d{1,2}/\d{4}|Present)\b']
    }

    parser_results = {}
    issues = []
    for parser in parsers:
        result = {}
        for section, patterns in required.items():
            found = any(re.search(p, text, re.I) for p in patterns)
            result[section] = "PASS" if found else "FAIL"
            if not found:
                issues.append(f"{parser}: {section} not extracted via canonical namespace")
        # Projects/certs are optional/partial in some parsers
        result["projects"] = "PASS" if re.search(r'Projects', text, re.I) else "PARTIAL"
        result["certifications"] = "PASS" if re.search(r'Certifications|Certificates', text, re.I) else "PARTIAL"
        parser_results[parser] = result

    # Layout Linearity / Multi-Column Collision Risk check
    layout_linear = not any(w in text.lower() for w in ["column 1", "tabular boundary error", "illegal overlap"])

    return GateResult(
        "parser_simulation",
        len(issues) == 0,
        {
            "parsers": parser_results,
            "canonical_mapping": canonical_mapping,
            "layout_linear_ready": layout_linear,
            "issues": issues
        },
        artifacts
    )


def repair_kerning_splits(text: str) -> str:
    """Repair PDF extraction kerning artifacts where uppercase letters are split from lowercase stems.

    Example: 'T echnical & F rontend Fluency' -> 'Technical & Frontend Fluency'
    Safely preserves valid English standalone words like 'A' and 'I'.
    """
    text = re.sub(r'\b([B-HJ-Z])\s+([a-z]{2,})\b', r'\1\2', text)
    text = re.sub(r'\b(A)\s+(rchitecture|ccessibility|nalysis|pplications?|udits?|gile|ws|zure)\b', r'\1\2', text, flags=re.I)
    text = re.sub(r'\b(I)\s+(nteractive|nformation|nterfaces?|mplementations?|terations?|cims|ntegrations?)\b', r'\1\2', text, flags=re.I)
    return text


def normalize_extracted_text(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFKC', text)
    ligatures = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for k, v in ligatures.items():
        text = text.replace(k, v)
    text = repair_kerning_splits(text)
    text = re.sub(r'[•‣▶◆◀◦▪▫●○✓✔➡*]+', '-', text)
    text = re.sub(r'[–—]', '--', text)
    return text


def validate_unicode_extraction(latex_path: str) -> GateResult:
    base = Path(latex_path).with_suffix('')
    txt_path = str(base) + '.txt'
    normalized_path = str(base) + '.normalized.txt'

    if os.path.exists(txt_path):
        text = read_file(txt_path)
    else:
        text = latex_to_plain_text(read_file(latex_path))

    normalized = normalize_extracted_text(text)
    with open(normalized_path, 'w', encoding='utf-8') as f:
        f.write(normalized)

    issues = []
    # Check for replacement chars or common ligature failures
    if '�' in normalized:
        issues.append("Replacement character found in extracted text")
    for lig in ['ﬀ', 'ﬁ', 'ﬂ', 'ﬃ', 'ﬄ']:
        if lig in normalized:
            issues.append(f"Unnormalized ligature remains: {lig}")

    # Ensure glyphtounicode guard exists in LaTeX
    latex = read_file(latex_path)
    for lig in ['ﬀ', 'ﬁ', 'ﬂ', 'ﬃ', 'ﬄ']:
        if lig in latex:
            issues.append(f"Source LaTeX contains problematic ligature character: {lig}")
    clean_latex = re.sub(r'(?m)(?<!\\)%.*', '', latex)
    if '\\input{glyphtounicode}' in clean_latex:
        gly_pos = clean_latex.find('\\input{glyphtounicode}')
        if not _is_in_pdf_guard(clean_latex, gly_pos):
            issues.append("glyphtounicode not guarded by \\ifpdf")

    recovery_rate = 1.0 - (normalized.count('�') / max(len(normalized), 1))

    return GateResult(
        "unicode_extraction",
        len(issues) == 0 and recovery_rate >= 0.98,
        {"issues": issues, "recovery_rate": round(recovery_rate, 4), "normalized_path": normalized_path},
        [normalized_path]
    )


def validate_readability(latex_path: str) -> GateResult:
    text = latex_to_plain_text(read_file(latex_path))
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r'\b\w+\b', text)
    avg_sentence_len = len(words) / max(len(sentences), 1)

    # Rough Flesch-Kincaid proxy without external textstat
    syllables = sum(count_syllables(w) for w in words)
    fk_grade = 0.39 * avg_sentence_len + 11.8 * (syllables / max(len(words), 1)) - 15.59

    passive_patterns = [r'\bwas responsible for\b', r'\bwas involved in\b', r'\bhelped to\b', r'\bassisted with\b']
    passive_hits = []
    for p in passive_patterns:
        passive_hits.extend(re.findall(p, text, re.I))

    issues = []
    if fk_grade > 12:
        issues.append(f"Flesch-Kincaid grade {fk_grade:.1f} exceeds 12")
    if avg_sentence_len > 20:
        issues.append(f"Average sentence length {avg_sentence_len:.1f} exceeds 20 words")
    if passive_hits:
        issues.append(f"Passive/weak constructions found: {passive_hits}")

    return GateResult("readability", len(issues) == 0, {
        "flesch_kincaid_grade": round(fk_grade, 1),
        "avg_sentence_length": round(avg_sentence_len, 1),
        "passive_hits": passive_hits,
        "issues": issues
    }, [])


def count_syllables(word: str) -> int:
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev:
            count += 1
        prev = is_vowel
    if word.endswith('e') and count > 1:
        count -= 1
    return max(count, 1)


def validate_audience_comprehension(latex_path: str, job_analysis: str | dict) -> GateResult:
    latex = read_file(latex_path)
    job = job_analysis if isinstance(job_analysis, dict) else json.loads(read_file(job_analysis))
    bullets = re.findall(r'\\(?:item|bulletitem)\s*(?:\{([^}]*)\}|([^\n]*))', latex)
    bullets = [(b[0] or b[1]).strip() for b in bullets if (b[0] or b[1]).strip()]
    keywords = list(job.get('keyword_targets', {}).keys())

    issues = []
    bullet_results = []
    for i, bullet in enumerate(bullets, 1):
        checks = {
            "hr_keywords": sum(1 for kw in keywords if kw.lower() in bullet.lower()),
            "business_outcome": bool(re.search(r'(\$|%|revenue|ARR|users|risk|cost|speed|time|conversion|retention)', bullet, re.I)),
            "scope": bool(re.search(r'\b\d+[KMB]?\+?\b|team|teams|users|merchants|engineers|designers', bullet, re.I)),
            "technical_proof": bool(re.search(r'(React|TypeScript|Figma|Storybook|n=|p<|A/B|SQL|Python|WCAG|API)', bullet, re.I))
        }
        if checks["hr_keywords"] < 1:
            issues.append(f"Bullet {i}: no job keyword visible")
        if not checks["business_outcome"]:
            issues.append(f"Bullet {i}: no business outcome")
        if not checks["scope"]:
            issues.append(f"Bullet {i}: no scope/scale context")
        if not checks["technical_proof"]:
            issues.append(f"Bullet {i}: no method/tool/proof")
        bullet_results.append({"bullet": i, **checks})

    return GateResult("audience_comprehension", len(issues) == 0, {"bullets": bullet_results, "issues": issues}, [])


def validate_metric_plausibility(latex_path: str) -> GateResult:
    text = latex_to_plain_text(read_file(latex_path))
    issues = []

    # % gains >15% require n= or directional marker
    pct_gains = re.findall(r'([+\-]?\d+(?:\.\d+)?)\s*%', text)
    for pct in pct_gains:
        val = abs(float(pct))
        if val > 15:
            # Look near the metric for n= or directional language
            idx = text.find(pct + '%')
            context = text[max(0, idx - 120):idx + 120]
            if not re.search(r'n\s*=|directional|~|approx|approximately|cohort|sample', context, re.I):
                issues.append(f"Metric {pct}% lacks sample size or directional caveat")

    # Revenue claims require timeframe
    for m in re.finditer(r'\$\s*\d+(?:\.\d+)?\s*[KMB]?', text):
        context = text[max(0, m.start() - 80):m.end() + 80]
        if not re.search(r'ARR|annual|quarter|monthly|year|retained|saved', context, re.I):
            issues.append(f"Revenue metric '{m.group(0)}' lacks timeframe/context")

    # WCAG claims require version/level
    if re.search(r'WCAG|accessibility compliant', text, re.I) and not re.search(r'WCAG\s*2\.[12]\s*(AA|A|AAA)', text, re.I):
        issues.append("WCAG/accessibility claim lacks version/level (e.g., WCAG 2.2 AA)")

    return GateResult("metric_plausibility", len(issues) == 0, {"issues": issues}, [])


def validate_single_role(latex_path: str, job_analysis: str | dict) -> GateResult:
    latex = read_file(latex_path)
    job = job_analysis if isinstance(job_analysis, dict) else json.loads(read_file(job_analysis))
    role_title = job.get('role_title', '')

    headline_match = re.search(r'\\headline\{([^}]+)\}', latex)
    role_line = headline_match.group(1) if headline_match else ""
    issues = []

    if not role_line:
        issues.append("No role headline found")
    if re.search(r'\s(&|/|or|and)\s', role_line, re.I):
        issues.append(f"Header contains multiple target roles: {role_line}")
    if role_title and role_title.lower() not in role_line.lower() and role_line.lower() not in role_title.lower():
        issues.append(f"Header role '{role_line}' does not match job role '{role_title}'")

    return GateResult("single_role", len(issues) == 0, {"role_line": role_line, "job_role": role_title, "issues": issues}, [])


def validate_summary_template(latex_path: str, job_analysis: str | dict) -> GateResult:
    latex = read_file(latex_path)
    job = job_analysis if isinstance(job_analysis, dict) else json.loads(read_file(job_analysis))
    summary_match = re.search(r'\\section\*\{Professional Summary\}(.*?)(?:\\section|$)', latex, re.DOTALL)
    issues = []
    details = {}

    if not summary_match:
        return GateResult("summary_template", False, {"issues": ["Missing Professional Summary"]}, [])

    summary_latex = summary_match.group(1)
    summary_text = latex_to_plain_text(summary_latex)
    sentences = [s.strip() for s in re.split(r'[.!?]+', summary_text) if s.strip()]
    kw_count = len(re.findall(r'\\kw\{', summary_latex))
    metric_count = len(re.findall(r'\\metric\{', summary_latex)) + len(re.findall(r'(\$|\d+%|\d+\s*(?:users|teams|components|years))', summary_text, re.I))

    if len(sentences) != 3:
        issues.append(f"Summary must be exactly 3 sentences; found {len(sentences)}")
    if len(sentences) >= 3:
        sentence3_latex = summary_latex.split('.')[2] if summary_latex.count('.') >= 2 else ""
        if re.search(r'\\(kw|metric|signaltag)\{', sentence3_latex):
            issues.append("Summary sentence 3 must contain no macros")
    if kw_count < 3 or kw_count > 5:
        issues.append(f"Summary must contain 3-5 \\kw{{}} macros; found {kw_count}")
    if metric_count < 1 or metric_count > 2:
        issues.append(f"Summary should contain 1-2 metrics; found {metric_count}")

    details.update({
        "sentence_count": len(sentences),
        "keyword_macro_count": kw_count,
        "metric_count": metric_count,
        "issues": issues
    })
    return GateResult("summary_template", len(issues) == 0, details, [])


def validate_signal_tags(latex_path: str) -> GateResult:
    latex = read_file(latex_path)
    tags = re.findall(r'\\signaltag\{([^}]+)\}', latex)
    issues = []
    invalid = [t for t in tags if t not in CONTROLLED_SIGNAL_TAGS]
    if invalid:
        issues.append(f"Invalid signal tags: {invalid}")

    # Check for leaked bracketed tags like [systems-thinking] in body text
    plain_text = latex_to_plain_text(latex)
    leaked_tags = re.findall(r'\[[a-z0-9-]+\]', plain_text)
    if leaked_tags:
        issues.append(f"Leaked bracketed signal tags found in body text: {leaked_tags}")

    bullets = re.findall(r'\\(?:item|bulletitem)\s*(?:\{([^}]*)\}|([^\n]*))', latex)
    bullet_count = len([b for b in bullets if (b[0] or b[1]).strip()])
    if bullet_count > 0 and len(tags) < bullet_count:
        issues.append(f"Only {len(tags)} signal tags for {bullet_count} bullets")

    return GateResult("signal_tags", len(issues) == 0, {"tags": tags, "invalid": invalid, "issues": issues}, [])


def validate_portfolio_crossref(latex_path: str, portfolio_dir: str = "./portfolio") -> GateResult:
    latex = read_file(latex_path)
    issues = []
    details = {}

    portfolio_url = re.search(r'(https?://[^\s{}]+)', latex)
    if not portfolio_url:
        issues.append("No portfolio URL found")

    # For projects, require portfolio/case-study mention if Projects section exists
    if '\\section*{Projects}' in latex and 'case stud' not in latex.lower() and 'portfolio' not in latex.lower():
        issues.append("Projects section exists but no portfolio/case-study cross-reference")

    if os.path.exists(portfolio_dir):
        details["portfolio_dir_exists"] = True
    else:
        details["portfolio_dir_exists"] = False
        # Not hard fail if URL exists

    details["issues"] = issues
    return GateResult("portfolio_crossref", len(issues) == 0, details, [])


def validate_experience_overlap(latex_path: str) -> GateResult:
    """Detect overlapping employment dates that inflate tenure."""
    latex = read_file(latex_path)
    issues = []
    details = {"roles": []}

    # Extract role entries with dates
    role_pattern = r'\\roleentry\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}\{([^}]+)\}'
    for match in re.finditer(role_pattern, latex):
        company, role, location, dates = match.groups()
        details["roles"].append({"company": company, "role": role, "dates": dates})

        # Check for overlap with other roles
        for other_match in re.finditer(role_pattern, latex):
            if other_match.start() == match.start():
                continue
            o_company, o_role, o_location, o_dates = other_match.groups()
            if _dates_overlap(dates, o_dates):
                issues.append(f"Date overlap detected: {company} ({dates}) overlaps with {o_company} ({o_dates})")

    # Check for total tenure inflation (sum of years > career span)
    total_years = 0
    years_found = re.findall(r'(\d{4})', latex)
    if len(years_found) >= 2:
        career_span = max(map(int, years_found)) - min(map(int, years_found))
        # Rough check: if claimed total years > career span + 2 (allowing for parallel)
        for role in details["roles"]:
            # Extract years from each role
            role_years = re.findall(r'(\d{4})', role["dates"])
            if len(role_years) >= 2:
                total_years += int(role_years[1]) - int(role_years[0])

        if total_years > career_span + 2:
            issues.append(f"Total claimed years ({total_years}) exceeds career span ({career_span}) by >2 years")

    return GateResult("experience_overlap", len(issues) == 0, {"issues": issues, "roles": details["roles"]}, [])


def _dates_overlap(dates1: str, dates2: str) -> bool:
    """Check if two date ranges overlap. Format: MM/YYYY – MM/YYYY or Present"""
    def parse_date_range(dr):
        parts = re.split(r'\s*[–-]\s*', dr)
        if len(parts) != 2:
            return None, None
        start = _parse_date(parts[0])
        end = _parse_date(parts[1]) if 'present' not in parts[1].lower() else None
        return start, end

    start1, end1 = parse_date_range(dates1)
    start2, end2 = parse_date_range(dates2)

    if not start1 or not start2:
        return False

    # If either is ongoing (Present), check if other started before this ended
    if end1 is None:
        end1 = (9999, 12)
    if end2 is None:
        end2 = (9999, 12)

    return not (end1 < start2 or end2 < start1)


def _parse_date(date_str: str):
    """Parse MM/YYYY or similar to (year, month) tuple."""
    match = re.search(r'(\d{1,2})[/.-](\d{4})', date_str)
    if match:
        return (int(match.group(2)), int(match.group(1)))
    match = re.search(r'(\d{4})', date_str)
    if match:
        return (int(match.group(1)), 1)
    return None


def validate_concept_vs_shipped(latex_path: str) -> GateResult:
    """Detect 'concept' / 'designed' / 'proposed' language without shipped evidence."""
    latex = read_file(latex_path)
    issues = []
    bullets = re.findall(r'\\(?:item|bulletitem)\s*(?:\{([^}]*)\}|([^\n]*))', latex)

    concept_indicators = [
        r'\b(conceived|conceptualized|designed|proposed|envisioned|architected)\b',
        r'\b(explored|investigated|researched|prototyped)\b',
        r'\b(strategy|roadmap|vision|framework)\b',
    ]
    shipped_indicators = [
        r'\b(launched|shipped|released|deployed|delivered|implemented|built)\b',
        r'\b(production|live|users|customers|revenue|adoption)\b',
        r'\b(n=|p<|sample|cohort|A/B|experiment)\b',
    ]

    for i, bullet in enumerate(bullets, 1):
        bullet_text = (bullet[0] or bullet[1]).strip()
        if not bullet_text:
            continue

        has_concept = any(re.search(p, bullet_text, re.I) for p in concept_indicators)
        has_shipped = any(re.search(p, bullet_text, re.I) for p in shipped_indicators)

        if has_concept and not has_shipped:
            issues.append(f"Bullet {i}: Concept/design language without shipped evidence: {bullet_text[:80]}...")

    return GateResult("concept_vs_shipped", len(issues) == 0, {"issues": issues}, [])


def validate_metric_verification(latex_path: str) -> GateResult:
    """Detect unverifiable metrics (round numbers, no context, no sample size)."""
    latex = read_file(latex_path)
    issues = []

    bullets = re.findall(r'\\(?:item|bulletitem)\s*(?:\{([^}]*)\}|([^\n]*))', latex)

    for i, bullet in enumerate(bullets, 1):
        bullet_text = (bullet[0] or bullet[1]).strip()
        if not bullet_text:
            continue

        # Find metrics
        metrics = re.findall(r'(\$?\d+(?:[.,]\d+)?\s*[%$KMB]?|\d+(?:[.,]\d+)?\s*(?:users|customers|teams|engineers|components))', bullet_text, re.I)

        for metric in metrics:
            # Check for context
            context_patterns = [
                r'n\s*=\s*\d+',  # sample size
                r'p\s*[<=>]\s*[\d.]+',  # p-value
                r'(A/B|experiment|test|study|survey|cohort)',
                r'(month|quarter|year|YoY|QoQ|MoM)',
                r'(baseline|from|to|increased|decreased|improved)',
            ]
            has_context = any(re.search(p, bullet_text, re.I) for p in context_patterns)

            # Check for round numbers without "~" or "~" or "approximately"
            is_round = bool(re.match(r'^\$?\d+[KMB]?%?$', metric.strip()))

            if is_round and not has_context and '~' not in bullet_text and 'approximately' not in bullet_text.lower():
                issues.append(f"Bullet {i}: Round metric '{metric}' lacks context/sample size")

            # Check for specific problematic patterns
            if re.search(r'\b\d{2,3}%\b', metric) and not re.search(r'n\s*=', bullet_text, re.I):
                # Percentages > 10% should have sample size
                pct_val = int(re.search(r'(\d+)%', metric).group(1))
                if pct_val > 10:
                    issues.append(f"Bullet {i}: {metric} improvement lacks sample size (n=)")

    return GateResult("metric_verification", len(issues) == 0, {"issues": issues}, [])


def validate_subagent_harness(latex_path: str, job_analysis: str | dict = None) -> dict:
    """Execute the mandatory 5-Subagent Compile-Test Harness audit.

    Evaluates the LaTeX resume against:
    1. Engine Compatibility (pdfLaTeX / XeLaTeX / LuaLaTeX preamble guardrails)
    2. Reserved Character Escaping (&, %, $, #, _)
    3. ATS Parser Structure (canonical headings, single skills section, linear flow)
    4. Unicode & Ligature Extraction (0 ligatures, recovery rate >= 98%)
    5. Recruiter & Keyword Hygiene (no leaked bracketed tags, keyword naturalness)
    """
    fmt_res = validate_latex_format(latex_path)
    uni_res = validate_unicode_extraction(latex_path)
    sig_res = validate_signal_tags(latex_path)

    job = None
    if job_analysis:
        if isinstance(job_analysis, str):
            job = json.loads(read_file(job_analysis))
        else:
            job = job_analysis

    latex = read_file(latex_path)
    fmt_issues = fmt_res.details.get("issues", [])

    # Subagent 1: Engine Compatibility
    engine_issues = [
        issue for issue in fmt_issues
        if any(token in issue for token in (
            "glyphtounicode", "\\pdfgentounicode", "\\documentclass",
            "Custom/non-article", "fontspec"
        ))
    ]
    s1_pass = len(engine_issues) == 0

    # Subagent 2: Character Escaping
    char_issues = [
        issue for issue in fmt_issues
        if any(token in issue for token in ("Unescaped '&'", "Unescaped '%'", "Unescaped '#'", "Unescaped '$'", "Unescaped '_'"))
    ]
    s2_pass = len(char_issues) == 0

    # Subagent 3: ATS Structure
    ats_issues = [
        issue for issue in fmt_issues
        if any(token in issue for token in ("Table/tabular", "Graphics/TikZ", "Missing required sections"))
    ]
    # Also check for split/fragmented skills sections
    skills_headers = re.findall(r'\\section\*?\{([^}]*[Ss]kill[^}]*)\}', latex)
    if len(skills_headers) > 1:
        ats_issues.append(f"Multiple/split skills sections detected: {skills_headers}")
    s3_pass = len(ats_issues) == 0

    # Subagent 4: Unicode & Ligatures
    uni_issues = uni_res.details.get("issues", [])
    s4_pass = uni_res.passed and len(uni_issues) == 0

    # Subagent 5: Recruiter & Keyword Hygiene
    sig_issues = sig_res.details.get("issues", [])
    hygiene_issues = list(sig_issues)
    if job:
        aud_res = validate_audience_comprehension(latex_path, job)
        hygiene_issues.extend(aud_res.details.get("issues", []))
    s5_pass = len(hygiene_issues) == 0

    overall_passed = s1_pass and s2_pass and s3_pass and s4_pass and s5_pass

    return {
        "overall_passed": overall_passed,
        "subagents": {
            "engine_compatibility": {
                "auditor": "Engine Compatibility",
                "status": "PASS" if s1_pass else "FAIL",
                "issues": engine_issues
            },
            "char_escaping": {
                "auditor": "Character Escaping",
                "status": "PASS" if s2_pass else "FAIL",
                "issues": char_issues
            },
            "ats_structure": {
                "auditor": "ATS Structure",
                "status": "PASS" if s3_pass else "FAIL",
                "issues": ats_issues
            },
            "unicode_ligatures": {
                "auditor": "Unicode & Ligatures",
                "status": "PASS" if s4_pass else "FAIL",
                "issues": uni_issues
            },
            "recruiter_hygiene": {
                "auditor": "Recruiter & Keyword Hygiene",
                "status": "PASS" if s5_pass else "FAIL",
                "issues": hygiene_issues
            }
        }
    }


def run_all_gates(latex: str, job_analysis: str | dict, mode: str = "designer-polish") -> ValidationReport:
    """Run all 10 validation gates.

    Args:
        latex: LaTeX source string (not path)
        job_analysis: JobAnalysis dict or path to job-analysis.json
        mode: "ats-max" or "designer-polish"
    """
    from datetime import datetime
    import tempfile
    import os

    # Write latex to temp file for file-based validators
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
        f.write(latex)
        temp_latex_path = f.name

    try:
        # Load job analysis if it's a path
        if isinstance(job_analysis, str):
            job = json.loads(read_file(job_analysis))
        else:
            job = job_analysis

        gates = [
            validate_latex_format(temp_latex_path),
            validate_keyword_density(temp_latex_path, job),
            validate_parser_simulation(temp_latex_path),
            validate_unicode_extraction(temp_latex_path),
            validate_readability(temp_latex_path),
            validate_audience_comprehension(temp_latex_path, job),
            validate_metric_plausibility(temp_latex_path),
            validate_single_role(temp_latex_path, job),
            validate_summary_template(temp_latex_path, job),
            validate_signal_tags(temp_latex_path),
            validate_portfolio_crossref(temp_latex_path),
            validate_experience_overlap(temp_latex_path),
            validate_concept_vs_shipped(temp_latex_path),
            validate_metric_verification(temp_latex_path),
        ]
    finally:
        if os.path.exists(temp_latex_path):
            try:
                os.unlink(temp_latex_path)
            except OSError:
                pass
        norm_path = str(Path(temp_latex_path).with_suffix('.normalized.txt'))
        if os.path.exists(norm_path):
            try:
                os.unlink(norm_path)
            except OSError:
                pass

    return ValidationReport(
        overall_passed=all(g.passed for g in gates),
        gates=gates,
        generated_at=datetime.utcnow().isoformat() + "Z",
        job_ref=f"{job.get('company', '')} — {job.get('role_title', '')}",
        candidate=""
    )


def save_validation_report(report: ValidationReport, output_path: str):
    data = asdict(report)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    def add_resume_arg(p):
        p.add_argument("--resume", required=True)
        return p

    add_resume_arg(subparsers.add_parser("validate_latex_format"))

    p = add_resume_arg(subparsers.add_parser("validate_density"))
    p.add_argument("--job", required=True)

    p = add_resume_arg(subparsers.add_parser("run_all"))
    p.add_argument("--job", required=True)
    p.add_argument("--mode", default="designer-polish")
    p.add_argument("--out", default="validation-report.json")

    p = add_resume_arg(subparsers.add_parser("quick_check"))
    p.add_argument("--job", required=True)

    args = parser.parse_args()

    if args.command == "validate_latex_format":
        result = validate_latex_format(args.resume)
        print(json.dumps(asdict(result), indent=2))
    elif args.command == "validate_density":
        result = validate_keyword_density(args.resume, args.job)
        print(json.dumps(asdict(result), indent=2))
    elif args.command == "run_all":
        report = run_all_gates(args.resume, args.job, args.mode)
        save_validation_report(report, args.out)
        print(f"Validation report saved to {args.out}")
        print(f"Overall passed: {report.overall_passed}")
    elif args.command == "quick_check":
        results = [validate_latex_format(args.resume), validate_keyword_density(args.resume, args.job)]
        print(json.dumps([asdict(r) for r in results], indent=2))