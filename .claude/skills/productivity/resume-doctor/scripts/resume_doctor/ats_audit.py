"""
ATS Audit — General ATS readiness check (no job target required).
Runs 6 gates: format, structure, keyword hygiene, readability, unicode, parser simulation.
"""
from dataclasses import dataclass, asdict
import json
import os
import re
from pathlib import Path
from typing import Optional
from datetime import datetime

from resume_doctor.validation_gates import (
    validate_latex_format,
    validate_parser_simulation,
    validate_unicode_extraction,
    validate_readability,
    ATS_SECTION_ONTOLOGY,
    GateResult,
)
from resume_doctor.recruiter_scorecard import evaluate_recruiter_scorecard


@dataclass
class ATSAuditResult:
    meta: dict
    overall_score: int
    passed: bool
    findings: list[dict]
    factor_scores: dict = None
    subagent_harness: dict = None
    recruiter_scorecard: dict = None


def run_ats_audit(latex_path: str, output_path: Optional[str] = None) -> ATSAuditResult:
    """Run full general ATS audit on a LaTeX resume with Multi-Factor Weighted Scoring"""

    # Gate 1: Format Compliance
    format_result = validate_latex_format(latex_path)

    # Gate 2: Structure Completeness
    structure_result = validate_structure_completeness(latex_path)

    # Gate 3: Keyword Hygiene
    hygiene_result = validate_keyword_hygiene(latex_path)

    # Gate 4: Readability Baseline
    readability_result = validate_readability(latex_path)

    # Gate 5: Unicode Extraction
    unicode_result = validate_unicode_extraction(latex_path)

    # Gate 6: Parser Simulation
    parser_result = validate_parser_simulation(latex_path)

    gates = [
        ("format_compliance", format_result),
        ("structure_completeness", structure_result),
        ("keyword_hygiene", hygiene_result),
        ("readability_baseline", readability_result),
        ("unicode_extraction", unicode_result),
        ("ats_parser_simulation", parser_result),
    ]

    # Multi-Factor Weighted Scoring Engine
    s_lexical = 100 if (format_result.passed and unicode_result.passed) else int((int(format_result.passed) + int(unicode_result.passed)) * 50)
    s_structural = 100 if (structure_result.passed and parser_result.passed) else int((int(structure_result.passed) + int(parser_result.passed)) * 50)
    s_hygiene = 100 if hygiene_result.passed else 70
    s_readability = 100 if readability_result.passed else 75

    factor_scores = {
        "lexical_cleanliness": s_lexical,
        "structural_readiness": s_structural,
        "keyword_hygiene_prominence": s_hygiene,
        "readability_recency": s_readability
    }

    from resume_doctor.validation_gates import validate_subagent_harness
    subagent_harness_res = validate_subagent_harness(latex_path)

    with open(latex_path, 'r', encoding='utf-8') as f:
        latex_content = f.read()
    plain_text = latex_to_plain(latex_content)
    scorecard_obj = evaluate_recruiter_scorecard(plain_text)
    recruiter_scorecard_res = asdict(scorecard_obj)

    overall_score = int(0.25 * s_lexical + 0.25 * s_structural + 0.25 * s_hygiene + 0.25 * s_readability)
    overall_passed = all(r.passed for _, r in gates) and bool(subagent_harness_res.get("overall_passed", False))

    findings = []
    for gate_name, result in gates:
        findings.append({
            "gate": gate_name,
            "passed": result.passed,
            "details": result.details
        })
    findings.append({
        "gate": "5_subagent_validation_harness",
        "passed": bool(subagent_harness_res.get("overall_passed", False)),
        "details": subagent_harness_res
    })

    result = ATSAuditResult(
        meta={
            "resume_file": str(latex_path),
            "audited_at": datetime.utcnow().isoformat() + "Z",
            "auditor_version": "2.2.0"
        },
        overall_score=overall_score,
        passed=overall_passed,
        findings=findings,
        factor_scores=factor_scores,
        subagent_harness=subagent_harness_res,
        recruiter_scorecard=recruiter_scorecard_res
    )

    if output_path:
        with open(output_path, 'w') as f:
            json.dump(asdict(result), f, indent=2)

    return result


def validate_structure_completeness(latex_path: str):
    """Check required sections present using Canonical ATS Section Normalization"""
    with open(latex_path, 'r', encoding='utf-8') as f:
        latex = f.read()

    details = {}
    issues = []

    # Check against established canonical namespaces
    for canonical_name, patterns in ATS_SECTION_ONTOLOGY.items():
        found = any(re.search(p, latex, re.I) for p in patterns)
        details[canonical_name] = "PASS" if found else "FAIL"
        if not found:
            issues.append(f"Missing required canonical ATS section: {canonical_name}")

    optional = [
        ("Certifications", r'\\section\*\{Certifications\}'),
        ("Projects", r'\\section\*\{Projects\}'),
        ("Continuous Learning", r'\\section\*\{Continuous Learning\}'),
    ]

    for name, pattern in optional:
        found = bool(re.search(pattern, latex))
        details[name] = "PASS" if found else "MISSING"

    # Contact in body
    contact_in_body = bool(re.search(r'\\contactline', latex))
    details["Contact in body"] = "PASS" if contact_in_body else "FAIL"
    if not contact_in_body:
        issues.append("Contact info not in body via \\contactline")

    # Linear flow check (no tables)
    if '\\tabular' in latex or '\\begin{tabular' in latex:
        details["Linear flow"] = "FAIL"
        issues.append("Table layout detected — breaks linear ATS parsing")
    else:
        details["Linear flow"] = "PASS"

    return GateResult("structure_completeness", len(issues) == 0, {"sections": details, "issues": issues}, [])


def validate_keyword_hygiene(latex_path: str):
    """Check for keyword stuffing, missing core skills, variant coverage"""
    with open(latex_path, 'r', encoding='utf-8') as f:
        latex = f.read()

    text = latex_to_plain(latex)
    issues = []
    details = {}

    # Core design skills that should be present
    core_design = ["figma", "design system", "prototyping", "user research", "accessibility"]
    missing_core = [kw for kw in core_design if kw not in text.lower()]
    if missing_core:
        issues.append(f"Missing core design skills: {missing_core}")

    # Check for stuffing (>3.5% single keyword)
    words = text.lower().split()
    for kw in core_design + ["react", "typescript", "a/b testing", "stakeholder"]:
        count = text.lower().count(kw)
        density = (count * len(kw.split()) / len(words)) * 100 if words else 0
        if density > 3.5:
            issues.append(f"Keyword stuffing detected: '{kw}' at {density:.1f}%")
        details[kw] = round(density, 2)

    # Variant coverage
    variants = {
        "prototyping": ["high-fidelity prototyping", "interactive prototyping", "rapid prototyping"],
        "design system": ["component library", "design tokens", "storybook"],
        "user research": ["usability testing", "jtbd", "interviews"],
    }
    for primary, var_list in variants.items():
        if primary not in text.lower() and not any(v in text.lower() for v in var_list):
            issues.append(f"No variant coverage for '{primary}'")

    from resume_doctor.validation_gates import GateResult
    return GateResult("keyword_hygiene", len(issues) == 0, {"densities": details, "issues": issues}, [])


def latex_to_plain(latex: str) -> str:
    text = re.sub(r'%.*', '', latex)
    text = re.sub(r'\\(kw|metric|signaltag|textbf|textit|emph)\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^]]*\])?(?:\{[^}]*\})?', ' ', text)
    text = re.sub(r'[{}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    result = run_ats_audit(args.resume, args.out)
    print(json.dumps(asdict(result), indent=2))
    if not result.passed:
        exit(1)