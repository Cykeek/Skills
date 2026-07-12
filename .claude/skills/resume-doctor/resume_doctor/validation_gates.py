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
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def latex_to_plain_text(latex: str) -> str:
    """Rough LaTeX macro stripping for validation before PDF extraction"""
    text = re.sub(r'%.*', '', latex)
    text = re.sub(r'\\(kw|metric|signaltag|textbf|textit|emph)\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^]]*\])?(?:\{[^}]*\})?', ' ', text)
    text = re.sub(r'[{}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def validate_latex_format(latex_path: str) -> GateResult:
    latex = read_file(latex_path)
    issues = []
    warnings = []

    if not latex.lstrip().startswith('\\documentclass'):
        issues.append("Missing or misplaced \\documentclass")
    if '\\documentclass' in latex and 'article' not in re.search(r'\\documentclass(?:\[[^]]*\])?\{([^}]+)\}', latex).group(1):
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
    if '\\input{glyphtounicode}' in latex:
        gly_pos = latex.find('\\input{glyphtounicode}')
        ifpdf_before = latex.rfind('\\ifpdf', 0, gly_pos)
        fi_after = latex.find('\\fi', gly_pos)
        if ifpdf_before == -1 or fi_after == -1:
            issues.append("\\input{glyphtounicode} appears outside an \\ifpdf guard")
    else:
        issues.append("Missing \\input{glyphtounicode}")

    if '\\usepackage{cmap}' not in latex:
        issues.append("Missing \\usepackage{cmap}")
    if '\\pdfgentounicode=1' not in latex:
        issues.append("Missing \\pdfgentounicode=1")
    if '\\usepackage[T1]{fontenc}' not in latex and '\\usepackage[T1]{fontenc}' not in latex:
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
    date_ranges = re.findall(r'\b\d{1,2}/\d{4}\s*[–-]\s*(?:\d{1,2}/\d{4}|Present)\b', latex)
    if not date_ranges:
        warnings.append("No valid MM/YYYY date ranges found")

    # Line breaking tolerance
    if '\\emergencystretch' not in latex:
        warnings.append("Missing \\emergencystretch for overfull-box prevention")

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


def validate_keyword_density(latex_path: str, job_analysis: str) -> GateResult:
    latex = read_file(latex_path)
    text = latex_to_plain_text(latex)
    job = json.loads(read_file(job_analysis))
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

    required = {
        "contact": [r'\b[\w.-]+@[\w.-]+\.\w+\b'],
        "summary": [r'Professional Summary|Summary'],
        "skills": [r'Skills'],
        "experience": [r'Work Experience|Experience'],
        "education": [r'Education'],
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
                issues.append(f"{parser}: {section} not extracted")
        # Projects/certs are optional/partial in some parsers
        result["projects"] = "PASS" if re.search(r'Projects', text, re.I) else "PARTIAL"
        result["certifications"] = "PASS" if re.search(r'Certifications|Certificates', text, re.I) else "PARTIAL"
        parser_results[parser] = result

    return GateResult("parser_simulation", len(issues) == 0, {"parsers": parser_results, "issues": issues}, artifacts)


def normalize_extracted_text(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFKC', text)
    ligatures = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for k, v in ligatures.items():
        text = text.replace(k, v)
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
    for lig in ['ﬁ', 'ﬂ', 'ﬃ', 'ﬄ']:
        if lig in normalized:
            issues.append(f"Unnormalized ligature remains: {lig}")

    # Ensure glyphtounicode guard exists in LaTeX
    latex = read_file(latex_path)
    if '\\input{glyphtounicode}' in latex and '\\ifpdf' not in latex:
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


def validate_audience_comprehension(latex_path: str, job_analysis: str) -> GateResult:
    latex = read_file(latex_path)
    job = json.loads(read_file(job_analysis))
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


def validate_single_role(latex_path: str, job_analysis: str) -> GateResult:
    latex = read_file(latex_path)
    job = json.loads(read_file(job_analysis))
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


def validate_summary_template(latex_path: str, job_analysis: str) -> GateResult:
    latex = read_file(latex_path)
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


def run_all_gates(latex_path: str, job_analysis: str, mode: str = "designer-polish") -> ValidationReport:
    from datetime import datetime
    gates = [
        validate_latex_format(latex_path),
        validate_keyword_density(latex_path, job_analysis),
        validate_parser_simulation(latex_path),
        validate_unicode_extraction(latex_path),
        validate_readability(latex_path),
        validate_audience_comprehension(latex_path, job_analysis),
        validate_metric_plausibility(latex_path),
        validate_single_role(latex_path, job_analysis),
        validate_summary_template(latex_path, job_analysis),
        validate_portfolio_crossref(latex_path),
    ]

    job = json.loads(read_file(job_analysis))
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