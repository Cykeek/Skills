"""
Portfolio Cross-Reference Validator — Ensures every project claim in resume
has a corresponding portfolio entry (and vice versa).
"""
import re
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class PortfolioEntry:
    name: str
    url: str
    description: str
    tags: list[str]
    role: str
    metrics: list[str]


@dataclass
class CrossRefResult:
    resume_projects: list[str]
    portfolio_entries: list[str]
    matched: list[dict]
    resume_only: list[str]  # In resume but not portfolio
    portfolio_only: list[str]  # In portfolio but not resume
    mismatched_metrics: list[dict]


def extract_resume_projects(latex: str) -> list[dict]:
    """Extract project names, descriptions, and metrics from resume."""
    projects = []

    # Find Projects section
    match = re.search(r'\\section\*\{Projects\}(?:.*?))(?=\\section\*\{|\Z)', latex, re.DOTALL)
    if not match:
        return projects

    proj_text = match.group(1)

    # Find each project entry
    entries = re.findall(r'\\projectentry\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}', proj_text)
    for name, url, desc, metrics in entries:
        projects.append({
            "name": name.strip(),
            "url": url.strip(),
            "description": desc.strip(),
            "metrics": [m.strip() for m in metrics.split(';') if m.strip()] if metrics else []
        })

    # Also check for inline project mentions in experience
    exp_match = re.search(r'\\section\*\{Work Experience\}(?:.*?))(?=\\section\*\{|\Z)', latex, re.DOTALL)
    if exp_match:
        exp_text = exp_match.group(1)
        # Look for project names in bullets
        bullets = re.findall(r'\\bulletitem\s*(?:\{([^}]+)\}|([^\n]+))', exp_text)
        for b in bullets:
            text = b[0] or b[1]
            if any(kw in text.lower() for kw in ["project", "launched", "shipped", "built", "redesigned"]):
                projects.append({
                    "name": text[:100].strip(),
                    "url": "",
                    "description": text.strip(),
                    "metrics": extract_metrics_from_text(text)
                })

    return projects


def extract_metrics_from_text(text: str) -> list[str]:
    """Extract metric-like strings from text."""
    metrics = []
    patterns = [
        r'\d+(?:\.\d+)?%\s*(?:increase|improvement|lift|reduction|growth)',
        r'\$\d+(?:\.\d+)?[KMB]?\s*(?:ARR|revenue|sales)',
        r'\d+(?:,\d{3})*\s*(?:users|customers|merchants|transactions)',
        r'\d+(?:\.\d+)?x\s*(?:faster|improvement|ROI)',
    ]
    for pat in patterns:
        metrics.extend(re.findall(pat, text, re.IGNORECASE))
    return metrics


def load_portfolio(portfolio_path: str) -> list[PortfolioEntry]:
    """Load portfolio entries from JSON file."""
    path = Path(portfolio_path)
    if not path.exists():
        return []

    with open(path) as f:
        data = json.load(f)

    entries = []
    for item in data.get('projects', []):
        entries.append(PortfolioEntry(
            name=item.get('name', ''),
            url=item.get('url', ''),
            description=item.get('description', ''),
            tags=item.get('tags', []),
            role=item.get('role', ''),
            metrics=item.get('metrics', [])
        ))

    return entries


def normalize_name(name: str) -> str:
    """Normalize project name for comparison."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


def cross_reference(latex: str, portfolio_path: str) -> CrossRefResult:
    """Cross-reference resume projects with portfolio."""
    resume_projects = extract_resume_projects(latex)
    portfolio_entries = load_portfolio(portfolio_path)

    resume_names = {normalize_name(p['name']): p for p in resume_projects}
    portfolio_names = {normalize_name(p.name): p for p in portfolio_entries}

    matched = []
    mismatched_metrics = []

    for rn, rp in resume_names.items():
        if rn in portfolio_names:
            pp = portfolio_names[rn]
            matched.append({
                "resume": rp['name'],
                "portfolio": pp.name,
                "url_match": rp['url'] == pp.url or (rp['url'] in pp.url or pp.url in rp['url'])
            })

            # Compare metrics
            r_metrics = set(m.lower() for m in rp['metrics'])
            p_metrics = set(m.lower() for m in pp.metrics)
            if r_metrics != p_metrics:
                mismatched_metrics.append({
                    "project": rp['name'],
                    "resume_only": list(r_metrics - p_metrics),
                    "portfolio_only": list(p_metrics - r_metrics)
                })

    resume_only = [p['name'] for n, p in resume_names.items() if n not in portfolio_names]
    portfolio_only = [p.name for n, p in portfolio_names.items() if n not in resume_names]

    return CrossRefResult(
        resume_projects=[p['name'] for p in resume_projects],
        portfolio_entries=[p.name for p in portfolio_entries],
        matched=matched,
        resume_only=resume_only,
        portfolio_only=portfolio_only,
        mismatched_metrics=mismatched_metrics
    )


def validate_portfolio_crossref(latex: str, portfolio_path: str) -> dict:
    """Validation gate: check portfolio cross-reference."""
    result = cross_reference(latex, portfolio_path)

    issues = []
    for name in result.resume_only:
        issues.append(f"Project in resume but not portfolio: '{name}'")
    for name in result.portfolio_only:
        issues.append(f"Project in portfolio but not resume: '{name}'")
    for m in result.mismatched_metrics:
        if m["resume_only"]:
            issues.append(f"Metrics in resume not in portfolio for '{m['project']}': {m['resume_only']}")
        if m["portfolio_only"]:
            issues.append(f"Metrics in portfolio not in resume for '{m['project']}': {m['portfolio_only']}")
    for m in result.matched:
        if not m["url_match"] and m["resume"]:
            issues.append(f"URL mismatch for '{m['resume']}': resume vs portfolio")

    return {
        "gate": "portfolio_crossref",
        "passed": len(issues) == 0,
        "details": {
            "matched_count": len(result.matched),
            "resume_only_count": len(result.resume_only),
            "portfolio_only_count": len(result.portfolio_only),
            "mismatched_metrics_count": len(result.mismatched_metrics)
        },
        "issues": issues
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--portfolio", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    latex = Path(args.resume).read_text()
    result = validate_portfolio_crossref(latex, args.portfolio)

    Path(args.out).write_text(json.dumps(result, indent=2))

    print(f"Portfolio cross-ref: {result['details']['matched_count']} matched, "
          f"{result['details']['resume_only_count']} resume-only, "
          f"{result['details']['portfolio_only_count']} portfolio-only")
    for issue in result["issues"]:
        print(f"  ISSUE: {issue}")

    if not result["passed"]:
        exit(1)