"""
Optimizer — Surgical LaTeX transformations for resume tailoring.

Public API:
    optimize_resume(latex, injection_map, mode) -> optimized_latex
    inject_keywords(latex, injection_map, mode) -> latex
    calibrate_density(latex, targets, mode) -> latex
    upgrade_verbs(latex) -> latex
    add_signal_tags(latex, taxonomy) -> latex
    apply_nda_abstraction(latex, level) -> latex
    reorder_sections(latex, role) -> latex
    apply_audience_aware(latex, job_analysis) -> latex
    auto_calibrate_density(latex, job_analysis, mode) -> latex
"""
import re
import json
from pathlib import Path
from typing import Literal


TIER3_VERBS = [
    r'\bassisted with\b', r'\bhelped (?:to )?\b', r'\bsupported\b', r'\bparticipated in\b',
    r'\bcontributed to\b', r'\bworked on\b', r'\bwas responsible for\b', r'\bwas involved in\b'
]
TIER2_REPLACEMENTS = {
    r'\bassisted with\b': 'Enabled',
    r'\bhelped (?:to )?\b': 'Facilitated',
    r'\bsupported\b': 'Supported',
    r'\bparticipated in\b': 'Contributed to',
    r'\bcontributed to\b': 'Advanced',
    r'\bworked on\b': 'Built',
    r'\bwas responsible for\b': 'Owned',
    r'\bwas involved in\b': 'Drove',
}


VARIANT_MAP = {
    "design systems": ["design system", "component library", "design tokens", "storybook", "zeroheight"],
    "a/b testing": ["experimentation", "split testing", "statistical significance", "p-value", "holdout"],
    "figma": ["figma", "figjam", "devmode", "auto layout", "components", "variants"],
    "accessibility": ["wcag", "wcag 2.2 aa", "screen reader", "keyboard navigation", "inclusive design"],
    "react": ["react", "react.js", "jsx", "hooks", "next.js"],
    "typescript": ["typescript", "ts", "type-safe", "typed"],
}


def inject_keywords(latex: str, injection_map: dict, mode: Literal["ats-max", "designer-polish"]) -> str:
    """Inject keywords at specified locations from keyword-injection-map.json"""
    injections = injection_map.get('injections', [])
    if not injections:
        return latex

    # First, handle Summary section
    for inj in injections:
        kw = inj['keyword']
        locations = inj['locations']

        if 'summary' in locations:
            latex = inject_into_summary(latex, kw, inj.get('variant', kw))

        if 'skills' in locations:
            latex = inject_into_skills(latex, kw, inj.get('variant', kw))

        for loc in locations:
            if loc.startswith('experience:'):
                idx = int(loc.split(':')[1])
                latex = inject_into_experience(latex, kw, idx, inj.get('variant', kw))

    return latex


def inject_into_summary(latex: str, keyword: str, variant: str) -> str:
    """Inject keyword into Professional Summary — add to existing sentence or as new \\kw{}"""
    pattern = r'(\\section\*\{Professional Summary\}(?:.*?))'
    match = re.search(pattern, latex, re.DOTALL)
    if not match:
        return latex

    summary_text = match.group(1)
    # Check if already present
    if keyword.lower() in summary_text.lower() or variant.lower() in summary_text.lower():
        return latex

    # Find a sentence to inject into, or add \kw{} macro
    # Simple approach: inject before final period of first sentence
    sentences = re.split(r'(?<=[.!?])\s+', summary_text.strip())
    if sentences:
        first = sentences[0]
        # Inject before period
        new_first = first.rstrip('.') + f' in {variant}.' if 'in ' not in first.lower() else first.rstrip('.') + f' with {variant}.'
        summary_text = summary_text.replace(first, new_first, 1)
        latex = latex.replace(match.group(1), summary_text)
    return latex


def inject_into_skills(latex: str, keyword: str, variant: str) -> str:
    """Add keyword to Skills section — find appropriate category bullet"""
    section_match = re.search(r'(\\section\*\{Skills\}(?:.*?))(?:\\section|\Z)', latex, re.DOTALL)
    if not section_match:
        return latex

    skills_text = section_match.group(1)
    if keyword.lower() in skills_text.lower() or variant.lower() in skills_text.lower():
        return latex

    # Determine category
    category = categorize_keyword(keyword)
    pattern = rf'(\\item\s+\\textbf\{{{{{re.escape(category)}}}:}})'
    match = re.search(pattern, skills_text)
    if match:
        # Add to existing category line
        line = match.group(0)
        new_line = line.replace(r'\kw{', f'\\kw{{{variant}}}, ')
        skills_text = skills_text.replace(line, new_line, 1)
    else:
        # Add new category bullet - use lambda to avoid backslash issues
        new_bullet = f'\n\\item \\textbf{{{category}:}} \\kw{{{variant}}}'
        def add_bullet(m):
            return m.group(1) + new_bullet + m.group(2)
        skills_text = re.sub(r'(\\section\*\{Skills\}.*?)(\\section|\Z)', add_bullet, skills_text, flags=re.DOTALL)

    return latex.replace(section_match.group(1), skills_text)


def inject_into_experience(latex: str, keyword: str, role_index: int, variant: str) -> str:
    """Inject keyword into specific experience bullet"""
    sections = re.split(r'(\\section\*\{Work Experience\})', latex)
    if len(sections) < 2:
        return latex

    exp_section = sections[2]  # Content after header
    # Find role entries
    roles = re.findall(r'(\\roleentry\{[^}]+\}\{[^}]+\}\{[^}]+\}\{[^}]+\}\{(?:[^}]*\}))', exp_section)
    if role_index >= len(roles):
        return latex

    # Find bullets in this role
    role_content = roles[role_index]
    bullets = re.findall(r'(\\bulletitem\s*(?:\{[^}]+\}|[^\n]*))', role_content)

    # Inject into first bullet that doesn't already have keyword
    for i, bullet in enumerate(bullets):
        if keyword.lower() not in bullet.lower() and variant.lower() not in bullet.lower():
            # Inject naturally
            new_bullet = bullet.replace('.', f' using {variant}.').replace(';', f'; leveraging {variant}')
            role_content = role_content.replace(bullet, new_bullet, 1)
            break

    # Reconstruct
    new_exp_section = exp_section.replace(roles[role_index], role_content)
    new_latex = sections[0] + sections[1] + new_exp_section
    for s in sections[3:]:
        new_latex += s
    return new_latex


def categorize_keyword(keyword: str) -> str:
    kw = keyword.lower()
    if kw in ['figma', 'sketch', 'framer', 'principle', 'protopie', 'adobe xd', 'zeplin', 'invision', 'miro', 'figjam']:
        return 'Design'
    if kw in ['design systems', 'design tokens', 'storybook', 'style dictionary', 'component library', 'design ops']:
        return 'Systems'
    if kw in ['react', 'typescript', 'javascript', 'html', 'css', 'sass', 'less', 'tailwind', 'styled-components', 'emotion', 'next.js', 'vite', 'webpack']:
        return 'Technical'
    if kw in ['mixpanel', 'amplitude', 'heap', 'looker', 'tableau', 'mode', 'sql', 'python', 'r', 'a/b testing', 'experimentation']:
        return 'Analytics'
    if kw in ['wcag', 'wcag 2.1', 'wcag 2.2', 'section 508', 'aria', 'screen reader', 'nvda', 'jaws', 'voiceover']:
        return 'Accessibility'
    if kw in ['cross-functional', 'stakeholder management', 'mentor', 'coach', 'design review', 'roadmap', 'prioritization', 'raci']:
        return 'Leadership'
    if kw in ['fintech', 'payments', 'banking', 'kyc', 'aml', 'pci-dss', 'b2b saas', 'marketplace', 'ecommerce', 'healthtech', 'edtech']:
        return 'Domain'
    return 'Skills'


def calibrate_density(latex: str, targets: dict, mode: Literal["ats-max", "designer-polish"]) -> str:
    """Iterative fine-tuning: add/remove/replace until all in [min, max]"""
    text = latex_to_plain(latex)
    max_iterations = 3

    for _ in range(max_iterations):
        all_ok = True
        for kw, target in targets.items():
            actual = keyword_density(text, kw)
            if actual < target['min']:
                latex = inject_for_density(latex, kw, target['min'] - actual)
                text = latex_to_plain(latex)
                all_ok = False
            elif actual > target['max'] and actual > 3.5:
                latex = reduce_density(latex, kw)
                text = latex_to_plain(latex)
                all_ok = False
        if all_ok:
            break
    return latex


def keyword_density(text: str, keyword: str) -> float:
    words = re.findall(r'\b\w+\b', text.lower())
    total = len(words)
    if total == 0:
        return 0.0
    kw_words = len(keyword.split())
    count = text.lower().count(keyword.lower())
    return (count * kw_words / total) * 100


def latex_to_plain(latex: str) -> str:
    text = re.sub(r'%.*', '', latex)
    text = re.sub(r'\\(kw|metric|signaltag|textbf|textit|emph)\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^]]*\])?(?:\{[^}]*\})?', ' ', text)
    text = re.sub(r'[{}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def inject_for_density(latex: str, keyword: str, deficit: float) -> str:
    """Add keyword occurrences — try variants first"""
    variant = get_variant(keyword)
    if variant != keyword and variant.lower() not in latex.lower():
        return inject_keyword_once(latex, variant)
    return inject_keyword_once(latex, keyword)


def inject_keyword_once(latex: str, keyword: str) -> str:
    # Try summary first
    latex = inject_into_summary(latex, keyword, keyword)
    # Then skills
    latex = inject_into_skills(latex, keyword, keyword)
    return latex


def reduce_density(latex: str, keyword: str) -> str:
    """Replace excess exact matches with variants"""
    variant = get_variant(keyword)
    if variant == keyword:
        return latex

    # Replace in bullets/experience
    latex = re.sub(rf'\b{re.escape(keyword)}\b', variant, latex, count=1, flags=re.IGNORECASE)
    return latex


def get_variant(keyword: str) -> str:
    for k, variants in VARIANT_MAP.items():
        if keyword.lower() == k or keyword.lower() in [v.lower() for v in variants]:
            return variants[0] if variants else keyword
    return keyword


def upgrade_verbs(latex: str) -> str:
    """Replace all Tier 3 verbs with Tier 2 equivalents"""
    for pattern, replacement in TIER2_REPLACEMENTS.items():
        latex = re.sub(pattern, replacement, latex, flags=re.IGNORECASE)
    return latex


def add_signal_tags(latex: str, taxonomy_path: str = None) -> str:
    """Add \\signaltag{} macros to bullets based on taxonomy triggers"""
    if taxonomy_path:
        with open(taxonomy_path) as f:
            taxonomy = json.load(f)
        tags_info = {t['key']: t for t in taxonomy.get('tags', [])}
    else:
        # Fallback minimal triggers
        tags_info = {
            "data-informed-iteration": {"triggers": ["A/B", "conversion", "p<", "n=", "experiment", "metrics"]},
            "cross-functional-leadership": {"triggers": ["cross-functional", "led", "directed", "facilitated", "stakeholder"]},
            "systems-thinking": {"triggers": ["design system", "component library", "tokens", "storybook", "coverage"]},
            "technical-fluency": {"triggers": ["React", "TypeScript", "pair-program", "Storybook", "code", "prototype"]},
            "user-research-rigor": {"triggers": ["interview", "usability", "JTBD", "synthesis", "Dovetail"]},
            "accessibility-advocacy": {"triggers": ["WCAG", "accessibility", "a11y", "screen reader", "keyboard"]},
            "craft-polish": {"triggers": ["motion", "animation", "micro-interaction", "edge case", "design QA"]},
            "zero-to-one-ambiguity": {"triggers": ["0 to 1", "0→1", "from scratch", "greenfield", "v1", "strategy"]},
            "strategic-influence": {"triggers": ["roadmap", "budget", "VP", "executive", "memo", "hiring", "prioritization"]},
            "mentorship-culture": {"triggers": ["mentor", "promoted", "hiring panel", "ritual", "culture", "onboard"]},
        }

    bullets = re.findall(r'(\\bulletitem\s*(?:\{[^}]+\}|[^\n]*))', latex)
    for bullet in bullets:
        if '\\signaltag{' in bullet:
            continue  # Already tagged

        matched_tags = []
        for tag_key, info in tags_info.items():
            for trigger in info.get('triggers', []):
                if re.search(rf'\b{re.escape(trigger)}\b', bullet, re.IGNORECASE):
                    matched_tags.append(tag_key)
                    break

        if matched_tags:
            # Add up to 3 tags at end of bullet
            tag_macros = ' '.join(f'\\signaltag{{{t}}}' for t in matched_tags[:3])
            new_bullet = bullet.rstrip(' .') + f' {tag_macros}.'
            latex = latex.replace(bullet, new_bullet, 1)

    return latex


def apply_nda_abstraction(latex: str, level: str = "pattern-abstracted") -> str:
    """Apply NDA abstraction ladder to sanitize confidential content"""
    levels = {
        "public": 0,
        "category": 1,
        "domain+scale": 2,
        "problem+outcome": 3,
        "pattern-abstracted": 3,
        "outcome-only": 4,
        "full-blackout": 4,
    }
    target_level = levels.get(level, 3)

    # Pattern replacements
    patterns = {
        1: {r'\b(Stripe|Airbnb|Google|Meta|Amazon|Microsoft|Apple)\b': 'Major Tech Company'},
        2: {
            r'\b(Stripe|PayPal|Square|Adyen)\b': 'High-volume fintech payment platform (10M+ txn/day)',
            r'\b(Airbnb|Booking|Expedia)\b': 'Global marketplace platform (100M+ users)',
        },
        3: {
            r'\\kw\{(Stripe|Airbnb|Google)\}': r'\\kw{Major payments platform}',
            r'(\d+)\s*M\+?\s*(merchants|users|transactions)': r'\\metric{\1M+ \2}',
        }
    }

    for lvl in range(1, target_level + 1):
        for pattern, replacement in patterns.get(lvl, {}).items():
            latex = re.sub(pattern, replacement, latex)

    return latex


def reorder_sections(latex: str, role: str) -> str:
    """Reorder sections per career stage + target role rules"""
    # Extract all sections
    sections = {}
    pattern = r'(\\section\*\{[^}]+\}.*?)(?=\\section\*\{|\Z)'
    for match in re.finditer(pattern, latex, re.DOTALL):
        header = re.match(r'\\section\*\{([^}]+)\}', match.group(1))
        if header:
            sections[header.group(1)] = match.group(1)

    # Determine order
    role_lower = role.lower()
    if 'engineer' in role_lower or 'developer' in role_lower:
        order = ['Professional Summary', 'Skills', 'Work Experience', 'Education', 'Certifications', 'Projects']
    elif 'design' in role_lower:
        order = ['Professional Summary', 'Skills', 'Work Experience', 'Education', 'Certifications', 'Projects']
    elif 'product' in role_lower:
        order = ['Professional Summary', 'Work Experience', 'Skills', 'Education', 'Certifications', 'Projects']
    else:
        order = ['Professional Summary', 'Skills', 'Work Experience', 'Education', 'Certifications', 'Projects']

    # Rebuild
    rebuilt = []
    # Keep preamble (before first section)
    preamble = latex.split('\\section*{Professional Summary}')[0]
    rebuilt.append(preamble)

    for name in order:
        if name in sections:
            rebuilt.append(sections[name])

    return '\n'.join(rebuilt)


def apply_audience_aware(latex: str, job_analysis: str) -> str:
    """Apply HR/CEO/Manager/Lead comprehension transforms"""
    with open(job_analysis) as f:
        job = json.load(f)

    # First-use acronym expansion
    acronyms = {
        'A/B': 'A/B testing (controlled experiments comparing two versions)',
        'WCAG': 'WCAG (Web Content Accessibility Guidelines)',
        'JTBD': 'JTBD (Jobs to Be Done — user needs framework)',
        'PCI-DSS': 'PCI-DSS (payment security standard)',
        'KYC': 'KYC (Know Your Customer — identity verification)',
        'AML': 'AML (Anti-Money Laundering)',
        'ARR': 'ARR (Annual Recurring Revenue)',
        'CI/CD': 'CI/CD (automated testing and deployment)',
        'RICE': 'RICE (prioritization framework: Reach, Impact, Confidence, Effort)',
    }

    # Expand first use in each section
    sections = re.split(r'(\\section\*\{[^}]+\})', latex)
    seen_acronyms = set()
    for i, section in enumerate(sections):
        if section.startswith('\\section*'):
            continue
        for acronym, expansion in acronyms.items():
            if acronym in section and acronym not in seen_acronyms:
                sections[i] = section.replace(acronym, f'{acronym} ({expansion})', 1)
                seen_acronyms.add(acronym)

    latex = ''.join(sections)

    # Add context to bare numbers
    def add_context(match):
        num = match.group(1)
        context = match.group(2) or ""
        if not re.search(r'\b(users|merchants|teams|components|years|months|K|M|B|%)\b', context, re.I):
            return f'{num} users'  # default fallback
        return match.group(0)

    latex = re.sub(r'(\b\d+(?:\.\d+)?\b)\s*([^.]*)\.', add_context, latex)

    return latex


def auto_calibrate_density(latex: str, job_analysis: str | dict, mode: Literal["ats-max", "designer-polish"]) -> str:
    """Full post-rewrite calibration: inject → calibrate → verify"""
    if isinstance(job_analysis, str):
        with open(job_analysis) as f:
            job = json.load(f)
    else:
        job = job_analysis

    targets = job.get('keyword_targets', {})
    # Phase 1: Inject missing/under-density keywords
    injection_map = build_injection_map_from_targets(latex, targets)
    latex = inject_keywords(latex, injection_map, mode)
    # Phase 2: Calibrate
    latex = calibrate_density(latex, targets, mode)
    # Phase 3: Upgrade verbs
    latex = upgrade_verbs(latex)
    # Phase 4: Add signal tags
    latex = add_signal_tags(latex)
    return latex


def build_injection_map_from_targets(latex: str, targets: dict) -> dict:
    """Generate injection map from current density vs targets"""
    text = latex_to_plain(latex)
    injections = []
    for kw, target in targets.items():
        actual = keyword_density(text, kw)
        if actual >= target['min']:
            continue
        needed = max(1, int((target['min'] - actual) * len(text.split()) / 100))
        locations = ["summary", "skills"]
        for i in range(min(needed, 3)):
            locations.append(f"experience:{i}")
        injections.append({
            "keyword": kw,
            "target_density": target['min'],
            "current_density": round(actual, 2),
            "locations": locations,
            "variant": get_variant(kw)
        })
    return {"injections": injections}


def optimize_resume(latex: str, injection_map: dict, mode: Literal["ats-max", "designer-polish"]) -> str:
    """Main optimization pipeline"""
    latex = inject_keywords(latex, injection_map, mode)
    latex = upgrade_verbs(latex)
    latex = add_signal_tags(latex)
    return latex


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--map", required=True)
    parser.add_argument("--mode", choices=["ats-max", "designer-polish"], default="designer-polish")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    latex = Path(args.resume).read_text()
    with open(args.map) as f:
        injection_map = json.load(f)

    optimized = optimize_resume(latex, injection_map, args.mode)
    Path(args.out).write_text(optimized)
    print(f"Optimized resume written to {args.out}")