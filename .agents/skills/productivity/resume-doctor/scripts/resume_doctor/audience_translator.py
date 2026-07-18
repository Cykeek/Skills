"""
Audience Translator — Applies audience-aware comprehension gates (HR/CEO/Manager/Lead).
Expands acronyms on first use, translates jargon, ensures cross-audience clarity.
"""
import re
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Literal


@dataclass
class AudienceGate:
    name: str
    expanded: dict[str, str]  # acronym -> expansion
    translations: dict[str, str]  # jargon -> plain
    complexity_threshold: int  # max syllables before flag


# HR/Recruiter gate - most expansive
HR_GATE = AudienceGate(
    name="HR/Recruiter",
    expanded={
        "A/B": "A/B testing (controlled experiments comparing two versions)",
        "WCAG": "WCAG (Web Content Accessibility Guidelines)",
        "JTBD": "JTBD (Jobs to Be Done — user needs framework)",
        "PCI-DSS": "PCI-DSS (payment card security standard)",
        "KYC": "KYC (Know Your Customer — identity verification)",
        "AML": "AML (Anti-Money Laundering)",
        "ARR": "ARR (Annual Recurring Revenue)",
        "CI/CD": "CI/CD (continuous integration and deployment)",
        "RICE": "RICE (prioritization: Reach, Impact, Confidence, Effort)",
        "OKR": "OKR (Objectives and Key Results)",
        "KPI": "KPI (Key Performance Indicator)",
        "SLA": "SLA (Service Level Agreement)",
        "ROI": "ROI (Return on Investment)",
        "SOC2": "SOC2 (security compliance standard)",
        "GDPR": "GDPR (data privacy regulation)",
        "API": "API (application programming interface)",
        "SDK": "SDK (software development kit)",
        "UI": "UI (user interface)",
        "UX": "UX (user experience)",
        "CMS": "CMS (content management system)",
        "SSO": "SSO (single sign-on)",
        "MFA": "MFA (multi-factor authentication)",
    },
    translations={
        "design system": "design system (unified component library and design standards)",
        "component library": "component library (reusable UI building blocks)",
        "design tokens": "design tokens (centralized design values like colors, spacing)",
        "Storybook": "Storybook (component development and documentation tool)",
        "Zeroheight": "Zeroheight (design system documentation platform)",
        "prototyping": "prototyping (interactive mockups for user testing)",
        "high-fidelity": "high-fidelity (polished, realistic mockups)",
        "low-fidelity": "low-fidelity (rough sketches/wireframes)",
        "usability testing": "usability testing (watching users complete tasks)",
        "heuristic evaluation": "heuristic evaluation (expert review against usability principles)",
        "cognitive load": "cognitive load (mental effort required to use interface)",
        "information architecture": "information architecture (content organization and navigation)",
        "WCAG 2.2 AA": "WCAG 2.2 AA (accessibility standard level AA)",
        "screen reader": "screen reader (assistive technology for visually impaired)",
        "keyboard navigation": "keyboard navigation (using interface without mouse)",
        "A/B test": "A/B test (controlled experiment comparing two versions)",
        "statistical significance": "statistical significance (result unlikely due to chance)",
        "p-value": "p-value (probability result occurred by chance)",
        "conversion rate": "conversion rate (percentage completing desired action)",
        "funnel": "funnel (user journey steps to conversion)",
        "retention": "retention (percentage of users returning over time)",
        "churn": "churn (percentage of users leaving)",
        "LTV": "LTV (lifetime value — revenue per customer over time)",
        "CAC": "CAC (customer acquisition cost)",
        "design ops": "design ops (design operations — process and tooling)",
        "design QA": "design QA (design quality assurance review)",
        "micro-interaction": "micro-interaction (small animated feedback)",
        "motion design": "motion design (animation and transitions)",
        "responsive design": "responsive design (adapts to screen sizes)",
        "mobile-first": "mobile-first (design for mobile, enhance for desktop)",
        "atomic design": "atomic design (component methodology: atoms, molecules, organisms)",
        "design tokens": "design tokens (centralized design values)",
        "component coverage": "component coverage (percentage of UI using design system)",
        "adoption rate": "adoption rate (percentage of teams using design system)",
        "contribution model": "contribution model (how teams add to design system)",
        "governance": "governance (decision-making process for design system)",
        "Figma": "Figma (collaborative design tool)",
        "FigJam": "FigJam (collaborative whiteboarding in Figma)",
        "DevMode": "DevMode (developer handoff in Figma)",
        "Auto Layout": "Auto Layout (responsive layout in Figma)",
        "Variants": "Variants (component states in Figma)",
        "React": "React (JavaScript UI library)",
        "TypeScript": "TypeScript (typed JavaScript)",
        "Next.js": "Next.js (React framework)",
        "Tailwind": "Tailwind (utility-first CSS framework)",
        "Styled Components": "Styled Components (CSS-in-JS library)",
        "CSS-in-JS": "CSS-in-JS (styling approach)",
        "Web Components": "Web Components (browser-native components)",
    },
    complexity_threshold=4
)

# CEO/Executive gate - business focused
CEO_GATE = AudienceGate(
    name="CEO/Executive",
    expanded={
        "ARR": "ARR (Annual Recurring Revenue)",
        "LTV": "LTV (Customer Lifetime Value)",
        "CAC": "CAC (Customer Acquisition Cost)",
        "ROI": "ROI (Return on Investment)",
        "OKR": "OKR (Objectives and Key Results)",
        "RICE": "RICE (prioritization framework)",
        "CI/CD": "CI/CD (automated deployment pipeline)",
        "SOC2": "SOC2 (security compliance)",
        "GDPR": "GDPR (data privacy regulation)",
    },
    translations={
        "design system": "design system (scalable design infrastructure reducing dev time)",
        "component library": "component library (reusable code reducing rebuild effort)",
        "A/B test": "A/B test (data-driven experiment improving metrics)",
        "conversion rate": "conversion rate (percentage completing desired action)",
        "retention": "retention (percentage of users returning over time)",
        "churn": "churn (percentage of users leaving)",
        "LTV:CAC": "LTV:CAC ratio (unit economics health)",
        "payback period": "payback period (months to recover acquisition cost)",
        "design ops": "design ops (design operations — process efficiency)",
        "component coverage": "component coverage (design system adoption metric)",
        "adoption rate": "adoption rate (team usage of design system)",
    },
    complexity_threshold=5
)

# Engineering Manager / Tech Lead gate - technical depth
LEAD_GATE = AudienceGate(
    name="Engineering Lead/Manager",
    expanded={
        "CI/CD": "CI/CD (continuous integration/deployment)",
        "API": "API (application programming interface)",
        "SDK": "SDK (software development kit)",
        "SSO": "SSO (single sign-on)",
        "MFA": "MFA (multi-factor authentication)",
        "SOC2": "SOC2 (security compliance)",
        "GDPR": "GDPR (data privacy regulation)",
        "WCAG": "WCAG (accessibility guidelines)",
        "JTBD": "JTBD (Jobs to Be Done framework)",
        "RICE": "RICE (prioritization framework)",
    },
    translations={
        "design system": "design system (component library + tokens + documentation)",
        "component library": "component library (React/Vue/Web Components)",
        "design tokens": "design tokens (JSON/TS design values for cross-platform)",
        "Storybook": "Storybook (component sandbox and docs)",
        "Zeroheight": "Zeroheight (design system documentation)",
        "Figma DevMode": "Figma DevMode (developer handoff)",
        "Auto Layout": "Auto Layout (constraint-based layout)",
        "Variants": "Variants (component state management)",
        "React": "React (component framework)",
        "TypeScript": "TypeScript (static typing)",
        "Next.js": "Next.js (React meta-framework)",
        "Tailwind": "Tailwind (utility CSS)",
        "Styled Components": "Styled Components (CSS-in-JS)",
        "CSS-in-JS": "CSS-in-JS (runtime styles)",
        "Web Components": "Web Components (custom elements, shadow DOM)",
        "WCAG 2.2 AA": "WCAG 2.2 AA (contrast, keyboard, ARIA)",
        "screen reader": "screen reader (NVDA, JAWS, VoiceOver)",
        "keyboard navigation": "keyboard navigation (tab order, focus management)",
        "A/B test": "A/B test (experiment with statistical rigor)",
        "statistical significance": "statistical significance (p < 0.05 typically)",
        "p-value": "p-value (null hypothesis probability)",
        "conversion rate": "conversion rate (goal completions / sessions)",
        "funnel": "funnel (multi-step conversion path)",
        "retention": "retention (cohort-based return rate)",
        "churn": "churn (inverse of retention)",
        "design ops": "design ops (tooling, process, handoff automation)",
        "design QA": "design QA (pixel-perfect vs implementation review)",
        "micro-interaction": "micro-interaction (state transition animation)",
        "motion design": "motion design (Framer Motion, CSS animations)",
        "responsive design": "responsive design (breakpoints, fluid layouts)",
        "mobile-first": "mobile-first (progressive enhancement)",
        "atomic design": "atomic design (atoms→molecules→organisms→templates→pages)",
        "component coverage": "component coverage (% UI from design system)",
        "adoption rate": "adoption rate (teams consuming design system)",
        "contribution model": "contribution model (federated vs centralized)",
        "governance": "governance (RFC process, versioning, breaking changes)",
    },
    complexity_threshold=6
)

# Product Manager gate - product/business + technical
PM_GATE = AudienceGate(
    name="Product Manager",
    expanded={
        "A/B": "A/B testing (controlled experiments)",
        "WCAG": "WCAG (accessibility guidelines)",
        "JTBD": "JTBD (Jobs to Be Done framework)",
        "PCI-DSS": "PCI-DSS (payment security)",
        "KYC": "KYC (identity verification)",
        "AML": "AML (anti-money laundering)",
        "ARR": "ARR (Annual Recurring Revenue)",
        "CI/CD": "CI/CD (automated deployment)",
        "RICE": "RICE (prioritization framework)",
        "OKR": "OKR (Objectives and Key Results)",
        "KPI": "KPI (Key Performance Indicator)",
        "SLA": "SLA (Service Level Agreement)",
        "ROI": "ROI (Return on Investment)",
        "LTV": "LTV (Lifetime Value)",
        "CAC": "CAC (Customer Acquisition Cost)",
    },
    translations={
        "design system": "design system (unified components accelerating feature delivery)",
        "component library": "component library (reusable UI reducing design/dev time)",
        "design tokens": "design tokens (single source of truth for design values)",
        "Storybook": "Storybook (component documentation and testing)",
        "prototyping": "prototyping (validating concepts before build)",
        "usability testing": "usability testing (validating with real users)",
        "A/B test": "A/B test (experiment measuring feature impact)",
        "conversion rate": "conversion rate (key funnel metric)",
        "retention": "retention (product health indicator)",
        "churn": "churn (revenue/user loss)",
        "LTV:CAC": "LTV:CAC (unit economics)",
        "design ops": "design ops (scaling design process)",
        "component coverage": "component coverage (design system maturity metric)",
        "adoption rate": "adoption rate (design system success metric)",
    },
    complexity_threshold=5
)


GATES = {
    "hr": HR_GATE,
    "ceo": CEO_GATE,
    "lead": LEAD_GATE,
    "pm": PM_GATE,
}


def apply_audience_aware(latex: str, job_analysis_path: str, target_audience: Literal["hr", "ceo", "lead", "pm"] = "hr") -> str:
    """Apply audience-aware transformations to LaTeX."""
    with open(job_analysis_path) as f:
        job = json.load(f)

    gate = GATES.get(target_audience, HR_GATE)

    # Track which acronyms have been expanded in each section
    section_acronyms = set()
    seen_acronyms_global = set()

    # Split by sections
    sections = re.split(r'(\\section\*\{[^}]+\})', latex)
    result = []

    for i, section in enumerate(sections):
        if section.startswith('\\section*'):
            # New section - reset section tracking
            section_acronyms = set()
            result.append(section)
            continue

        # Process text in this section
        processed = section

        # Expand acronyms on first use per section
        for acronym, expansion in gate.expanded.items():
            # Skip if already expanded globally and not in summary
            if acronym in seen_acronyms_global and 'Professional Summary' not in ''.join(sections[max(0,i-3):i]):
                continue

            # Pattern: acronym as whole word, not already expanded
            pattern = rf'\b{re.escape(acronym)}\b(?!\s*\([^)]*\))'
            matches = list(re.finditer(pattern, processed))
            if matches:
                # Only expand first occurrence in section
                first = matches[0]
                if acronym not in section_acronyms:
                    replacement = f'{acronym} ({expansion})'
                    processed = processed[:first.start()] + replacement + processed[first.end():]
                    section_acronyms.add(acronym)
                    seen_acronyms_global.add(acronym)

        # Translate jargon (always apply)
        for jargon, translation in gate.translations.items():
            # Only translate if not already parenthetically expanded
            pattern = rf'\b{re.escape(jargon)}\b(?!\s*\([^)]*\))'
            processed = re.sub(pattern, translation, processed, flags=re.IGNORECASE)

        # Add context to bare numbers
        processed = add_context_to_numbers(processed, gate)

        result.append(processed)

    return ''.join(result)


def add_context_to_numbers(text: str, gate: AudienceGate) -> str:
    """Add context to bare numbers that lack units."""
    # Pattern: number followed by text without clear unit
    def add_context(match):
        num = match.group(1)
        context = match.group(2) or ""

        # Check if already has unit
        if re.search(r'\b(users|merchants|teams|components|years|months|K|M|B|%|x|transactions|customers|hires)\b', context, re.I):
            return match.group(0)

        # Default context based on gate
        if gate.name == "HR/Recruiter":
            return f'{num} users{context}.'
        elif gate.name == "CEO/Executive":
            return f'{num} users{context}.'
        elif gate.name == "Engineering Lead/Manager":
            return f'{num} users{context}.'
        else:
            return f'{num} users{context}.'

    # Match numbers at sentence start or after period
    pattern = r'(\b\d+(?:,\d{3})*(?:\.\d+)?\b)\s*([^.]*?)(?=\.|$)'
    return re.sub(pattern, add_context, text)


def apply_all_audiences(latex: str, job_analysis_path: str) -> dict[str, str]:
    """Generate versions for all four audiences."""
    return {
        "hr": apply_audience_aware(latex, job_analysis_path, "hr"),
        "ceo": apply_audience_aware(latex, job_analysis_path, "ceo"),
        "lead": apply_audience_aware(latex, job_analysis_path, "lead"),
        "pm": apply_audience_aware(latex, job_analysis_path, "pm"),
    }


def validate_audience_comprehension(latex: str, job_analysis_path: str) -> dict:
    """Validation gate: check all four audience gates pass."""
    with open(job_analysis_path) as f:
        job = json.load(f)

    results = {}
    all_passed = True
    all_issues = []

    for audience_key, gate in GATES.items():
        issues = []

        # Check for unexpanded critical acronyms
        text = latex_to_plain(latex)
        for acronym in gate.expanded:
            if acronym in text and f'{acronym} (' not in text:
                issues.append(f"Unexpanded acronym: {acronym}")

        # Check for untranslated jargon
        for jargon in gate.translations:
            if jargon.lower() in text.lower() and jargon not in gate.expanded:
                # Only flag if it's a key term
                if any(kw in jargon.lower() for kw in ["design system", "component", "A/B", "conversion", "retention"]):
                    issues.append(f"Untranslated jargon for {gate.name}: {jargon}")

        # Check complexity (simplified: count syllables > threshold)
        words = text.split()
        complex_words = sum(1 for w in words if count_syllables(w) > gate.complexity_threshold)
        if complex_words > len(words) * 0.1:  # >10% complex words
            issues.append(f"High complexity: {complex_words} words exceed {gate.complexity_threshold} syllables")

        passed = len(issues) == 0
        if not passed:
            all_passed = False
        all_issues.extend([f"[{gate.name}] {i}" for i in issues])

        results[audience_key] = {
            "gate": gate.name,
            "passed": passed,
            "issues": issues
        }

    return {
        "gate": "audience_comprehension",
        "passed": all_passed,
        "details": results,
        "issues": all_issues
    }


def latex_to_plain(latex: str) -> str:
    text = re.sub(r'%.*', '', latex)
    text = re.sub(r'\\(kw|metric|signaltag|textbf|textit|emph)\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?', ' ', text)
    text = re.sub(r'[{}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def count_syllables(word: str) -> int:
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    return max(1, count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--audience", choices=["hr", "ceo", "lead", "pm", "all"], default="all")
    args = parser.parse_args()

    latex = Path(args.resume).read_text()

    if args.audience == "all":
        versions = apply_all_audiences(latex, args.job)
        for aud, v in versions.items():
            Path(f"{args.out}.{aud}.tex").write_text(v)
    else:
        result = apply_audience_aware(latex, args.job, args.audience)
        Path(args.out).write_text(result)

    print(f"Audience translation complete: {args.audience}")