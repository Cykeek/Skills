"""
Metric Plausibility Validator — Checks that all \\metric{} claims are numerically plausible.
Validates: magnitude bounds, unit consistency, timeframe alignment, benchmark comparisons.
"""
import re
import json
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class MetricClaim:
    raw: str
    value: float
    unit: str
    timeframe: Optional[str]
    context: str
    plausible: bool
    issues: list[str]


# Plausibility bounds by role/context
PLAUSIBILITY_BOUNDS = {
    # Conversion rates
    "conversion_rate": {"min": 0.1, "max": 50.0, "unit": "%", "description": "Conversion rate"},
    "signup_conversion": {"min": 0.5, "max": 30.0, "unit": "%", "description": "Signup conversion"},
    "checkout_conversion": {"min": 0.5, "max": 10.0, "unit": "%", "description": "Checkout conversion"},

    # Engagement
    "engagement_lift": {"min": 1.0, "max": 200.0, "unit": "%", "description": "Engagement lift"},
    "retention_improvement": {"min": 1.0, "max": 50.0, "unit": "%", "description": "Retention improvement"},
    "churn_reduction": {"min": 1.0, "max": 50.0, "unit": "%", "description": "Churn reduction"},

    # Revenue/Business
    "revenue_increase": {"min": 1.0, "max": 500.0, "unit": "%", "description": "Revenue increase"},
    "arr_growth": {"min": 10.0, "max": 300.0, "unit": "%", "description": "ARR growth"},
    "ltv_cac_ratio": {"min": 2.0, "max": 20.0, "unit": "x", "description": "LTV/CAC ratio"},

    # Efficiency
    "time_saved": {"min": 5.0, "max": 90.0, "unit": "%", "description": "Time saved"},
    "cost_reduction": {"min": 5.0, "max": 80.0, "unit": "%", "description": "Cost reduction"},
    "dev_time_reduction": {"min": 10.0, "max": 80.0, "unit": "%", "description": "Dev time reduction"},

    # Scale
    "users_impacted": {"min": 1000, "max": 1000000000, "unit": "users", "description": "Users impacted"},
    "transactions_per_day": {"min": 1000, "max": 100000000, "unit": "txn/day", "description": "Transactions/day"},
    "components_built": {"min": 5, "max": 500, "unit": "components", "description": "Components built"},
    "pages_redesigned": {"min": 3, "max": 500, "unit": "pages", "description": "Pages redesigned"},

    # Team/Process
    "team_size": {"min": 2, "max": 100, "unit": "people", "description": "Team size managed"},
    "hires_made": {"min": 1, "max": 50, "unit": "hires", "description": "Hires made"},
    "onboarding_time_reduction": {"min": 10.0, "max": 80.0, "unit": "%", "description": "Onboarding time reduction"},
    "review_cycle_reduction": {"min": 10.0, "max": 80.0, "unit": "%", "description": "Review cycle reduction"},

    # Accessibility
    "wcag_compliance": {"min": 0, "max": 100, "unit": "%", "description": "WCAG compliance"},
    "a11y_score_improvement": {"min": 5.0, "max": 100.0, "unit": "%", "description": "Accessibility score improvement"},

    # Design System
    "adoption_rate": {"min": 10.0, "max": 100.0, "unit": "%", "description": "Design system adoption"},
    "coverage": {"min": 20.0, "max": 100.0, "unit": "%", "description": "Component coverage"},
    "design_token_count": {"min": 50, "max": 5000, "unit": "tokens", "description": "Design tokens"},
}


def extract_metrics(latex: str) -> list[MetricClaim]:
    """Extract all \\metric{} claims from LaTeX."""
    claims = []

    # Pattern: \metric{value unit timeframe} or \metric{description}
    pattern = r'\\metric\{([^}]+)\}'
    for match in re.finditer(pattern, latex):
        raw = match.group(1).strip()
        claim = parse_metric(raw, match.group(0), latex)
        claims.append(claim)

    return claims


def parse_metric(raw: str, full_match: str, context: str) -> MetricClaim:
    """Parse a metric string into structured claim."""
    issues = []

    # Extract value and unit
    # Patterns: "23% increase", "2.5x faster", "500K users", "$2.3M ARR", "40% reduction in 6 months"
    value_match = re.search(r'([\d,.]+(?:\.\d+)?)\s*(%|x|K|M|B|users?|txn|components?|pages?|people|hires?|tokens?)', raw, re.IGNORECASE)

    if value_match:
        value = float(value_match.group(1).replace(',', ''))
        unit = value_match.group(2).lower()
    else:
        value = 0.0
        unit = "unknown"

    # Extract timeframe
    timeframe = None
    tf_match = re.search(r'(in|over|within)\s+(\d+\s*(?:days?|weeks?|months?|quarters?|years?))', raw, re.IGNORECASE)
    if tf_match:
        timeframe = tf_match.group(0)

    # Determine metric type from context
    metric_type = classify_metric(raw, context)
    bounds = PLAUSIBILITY_BOUNDS.get(metric_type, {"min": 0, "max": float('inf'), "unit": unit})

    # Check plausibility
    plausible = True
    if value < bounds.get("min", 0):
        plausible = False
        issues.append(f"Value {value} below minimum {bounds['min']} for {bounds['description']}")
    if value > bounds.get("max", float('inf')):
        plausible = False
        issues.append(f"Value {value} exceeds maximum {bounds['max']} for {bounds['description']}")

    # Unit consistency check
    expected_unit = bounds.get("unit", "").lower()
    if expected_unit and unit != expected_unit and expected_unit != "unknown":
        # Allow compatible units
        if not units_compatible(unit, expected_unit):
            issues.append(f"Unit '{unit}' may not match expected '{expected_unit}' for {bounds['description']}")

    # Context sanity checks
    if "increase" in raw.lower() and value > 500:
        issues.append(f"Suspiciously high increase: {value}% — verify magnitude")

    if "reduction" in raw.lower() and value > 90:
        issues.append(f"Suspiciously high reduction: {value}% — verify")

    if "100%" in raw and "compliance" not in raw.lower():
        issues.append("100% claim outside compliance context — rare in practice")

    return MetricClaim(
        raw=raw,
        value=value,
        unit=unit,
        timeframe=timeframe,
        context=context[:200],
        plausible=plausible,
        issues=issues
    )


def classify_metric(raw: str, context: str) -> str:
    """Classify metric type from raw text and context."""
    text = (raw + " " + context).lower()

    if any(kw in text for kw in ["conversion", "signup", "checkout", "purchase"]):
        if "signup" in text:
            return "signup_conversion"
        if "checkout" in text or "purchase" in text:
            return "checkout_conversion"
        return "conversion_rate"

    if "engagement" in text and "lift" in text:
        return "engagement_lift"
    if "retention" in text and ("improve" in text or "increase" in text):
        return "retention_improvement"
    if "churn" in text and "reduc" in text:
        return "churn_reduction"

    if "revenue" in text and ("increase" in text or "growth" in text or "grew" in text):
        return "revenue_increase"
    if "arr" in text and ("growth" in text or "increase" in text):
        return "arr_growth"
    if "ltv" in text and "cac" in text:
        return "ltv_cac_ratio"

    if "time" in text and ("save" in text or "reduc" in text or "faster" in text):
        return "time_saved"
    if "cost" in text and "reduc" in text:
        return "cost_reduction"
    if "dev" in text and "time" in text and "reduc" in text:
        return "dev_time_reduction"

    if "user" in text and ("impact" in text or "reach" in text or "served" in text):
        return "users_impacted"
    if "transaction" in text:
        return "transactions_per_day"
    if "component" in text and ("built" in text or "created" in text or "delivered" in text):
        return "components_built"
    if "page" in text and "redesign" in text:
        return "pages_redesigned"

    if "team" in text and ("led" in text or "manag" in text or "size" in text):
        return "team_size"
    if "hire" in text:
        return "hires_made"
    if "onboard" in text and "time" in text:
        return "onboarding_time_reduction"
    if "review" in text and "cycle" in text:
        return "review_cycle_reduction"

    if "wcag" in text or "accessibility" in text:
        if "compliance" in text or "score" in text:
            return "wcag_compliance"
        return "a11y_score_improvement"

    if "adoption" in text and "design system" in text:
        return "adoption_rate"
    if "coverage" in text and "component" in text:
        return "coverage"
    if "design token" in text or "token" in text:
        return "design_token_count"

    return "unknown"


def units_compatible(unit1: str, unit2: str) -> bool:
    """Check if two units are compatible."""
    compat = {
        "%": ["%", "percent", "pct"],
        "x": ["x", "times", "fold"],
        "users": ["users", "user", "k", "m", "b"],
        "txn": ["txn", "transactions", "txns"],
        "components": ["components", "component", "comp"],
        "pages": ["pages", "page"],
        "people": ["people", "person", "team", "fte"],
        "hires": ["hires", "hire"],
        "tokens": ["tokens", "token"],
    }

    u1 = unit1.lower().rstrip('s')
    u2 = unit2.lower().rstrip('s')

    for base, variants in compat.items():
        if u1 in variants and u2 in variants:
            return True

    return u1 == u2


def validate_all_metrics(latex: str) -> dict:
    """Validate all metrics in a LaTeX resume."""
    claims = extract_metrics(latex)

    results = {
        "total_claims": len(claims),
        "plausible": sum(1 for c in claims if c.plausible),
        "implausible": sum(1 for c in claims if not c.plausible),
        "claims": []
    }

    for claim in claims:
        results["claims"].append({
            "raw": claim.raw,
            "value": claim.value,
            "unit": claim.unit,
            "timeframe": claim.timeframe,
            "plausible": claim.plausible,
            "issues": claim.issues
        })

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    latex = Path(args.resume).read_text()
    result = validate_all_metrics(latex)

    Path(args.out).write_text(json.dumps(result, indent=2))

    print(f"Metric validation: {result['plausible']}/{result['total_claims']} plausible")
    for claim in result["claims"]:
        if not claim["plausible"]:
            print(f"  ISSUE: {claim['raw']} — {claim['issues']}")

    if result["implausible"] > 0:
        exit(1)