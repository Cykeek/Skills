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
from typing import Literal, Optional


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


# NDA abstraction levels
NDA_LEVELS = {
    "L0": "full",           # Full transparency: company, metrics, details
    "L1": "company-abstracted",   # Domain, metrics, no company name
    "L2": "domain-abstracted",    # Function, metrics, no domain
    "L3": "pattern-abstracted",   # Method, directional metric only
    "L4": "blackout",      # Process only, no specifics
}


SECTION_ORDER = {
    "ats-max": [
        "Professional Summary",
        "Skills",
        "Work Experience",
        "Education",
        "Certifications",
        "Projects",
    ],
    "designer-polish": [
        "Professional Summary",
        "Skills",
        "Work Experience",
        "Projects",
        "Education",
        "Certifications",
    ],
    "software-engineer": [
        "Professional Summary",
        "Technical Skills",
        "Work Experience",
        "Projects",
        "Education",
        "Certifications",
    ],
    "product-manager": [
        "Professional Summary",
        "Core Competencies",
        "Work Experience",
        "Key Achievements",
        "Education",
        "Certifications",
    ],
    "engineering-leadership": [
        "Professional Summary",
        "Leadership Scope",
        "Work Experience",
        "Key Achievements",
        "Education",
        "Certifications",
    ],
}


AUDIENCE_REWRITE_MAP = {
    "hr": {
        "patterns": [
            (r'\b(MVP|PoC|CI/CD|API|SDK|K8s|Docker)\b', r'\1 (industry standard)'),
            (r'\b(React|TypeScript|Python|Go|Java)\b', r'\1 (programming language)'),
            (r'\b(A/B test|experiment|p-value)\b', r'A/B experiment with statistical rigor'),
        ],
        "focus": "keywords, outcomes, role clarity",
    },
    "hiring_manager": {
        "patterns": [
            (r'\bteam\b', r'cross-functional team'),
            (r'\bled\b', r'led team of'),
            (r'\bdelivered\b', r'delivered on time'),
        ],
        "focus": "scope, team size, timeline, budget, users",
    },
    "tech_lead": {
        "patterns": [
            (r'\b(refactored|optimized|architected)\b', r'\1 with measurable impact'),
            (r'\b(scaled|migrated)\b', r'\1 with zero downtime'),
        ],
        "focus": "method, tools, statistical rigor, architectural decisions",
    },
    "executive": {
        "patterns": [
            (r'\b(\$?\d+(?:\.\d+)?[KMB]?)\b', r'\1 business impact'),
            (r'\b(\d+%)\b', r'\1 improvement'),
        ],
        "focus": "revenue, users, risk, speed, strategic outcomes",
    },
}


def calibrate_density(latex: str, targets: dict, mode: Literal["ats-max", "designer-polish"] = "designer-polish") -> str:
    """
    Adjust keyword density to hit target ranges.
    - If under target: inject keyword at natural locations
    - If over target: replace with variants from VARIANT_MAP
    """
    if not targets:
        return latex

    text = latex

    for keyword, target in targets.items():
        priority = target.get('priority', 'medium')
        min_density = target.get('min', 1.0)
        max_density = target.get('max', 2.5)

        current_density = _calculate_density(text, keyword)

        if current_density < min_density:
            # Under target - inject keyword
            text = _inject_for_density(text, keyword, min_density - current_density, mode)
        elif current_density > max_density:
            # Over target - replace with variants
            text = _replace_with_variants(text, keyword, current_density - max_density)

    return text


def _calculate_density(text: str, keyword: str) -> float:
    """Calculate keyword density percentage in text."""
    words = re.findall(r'\b\w+\b', text.lower())
    total = len(words)
    if total == 0:
        return 0.0
    kw_words = len(keyword.split())
    count = len(re.findall(rf'\b{re.escape(keyword.lower())}\b', text.lower()))
    return (count * kw_words / total) * 100


def _inject_for_density(latex: str, keyword: str, deficit: float, mode: str) -> str:
    """Inject keyword into natural locations to reach target density."""
    # Determine how many injections needed
    word_count = len(re.findall(r'\b\w+\b', latex))
    injections_needed = max(1, int((deficit / 100) * word_count / len(keyword.split())))

    locations = ['summary', 'skills']
    if mode == "ats-max":
        locations += ['experience:0', 'experience:1']
    else:
        locations += ['experience:0', 'experience:1', 'experience:2']

    variant = VARIANT_MAP.get(keyword.lower(), [keyword])[0]

    for i, loc in enumerate(locations[:injections_needed]):
        if loc == 'summary':
            latex = inject_into_summary(latex, keyword, variant)
        elif loc == 'skills':
            latex = inject_into_skills(latex, keyword, variant)
        elif loc.startswith('experience:'):
            idx = int(loc.split(':')[1])
            latex = inject_into_experience(latex, keyword, idx, variant)

    return latex


def _replace_with_variants(latex: str, keyword: str, excess: float) -> str:
    """Replace excess keyword occurrences with variants."""
    variants = VARIANT_MAP.get(keyword.lower(), [keyword])
    if len(variants) <= 1:
        return latex

    # Replace every Nth occurrence with a variant
    count = 0
    def replacer(match):
        nonlocal count
        count += 1
        if count % 2 == 0:
            return variants[count % len(variants)]
        return match.group(0)

    pattern = rf'\b{re.escape(keyword)}\b'
    return re.sub(pattern, replacer, latex, flags=re.IGNORECASE)


def apply_nda_abstraction(latex: str, level: str | int = "L3") -> str:
    """
    Apply NDA abstraction to protect confidential information.
    Levels: L0=full, L1=company-abstracted, L2=domain-abstracted, L3=pattern-abstracted, L4=blackout
    """
    level_str = str(level).upper()
    if level_str not in NDA_LEVELS:
        level_str = "L3"

    level_type = NDA_LEVELS[level_str]

    if level_type == "full":
        return latex

    # Patterns to abstract
    company_patterns = [
        (r'\b(Google|Meta|Apple|Amazon|Microsoft|Netflix|Uber|Airbnb|Stripe|Shopify)\b',
         lambda m: _abstract_company(m.group(1), level_type)),
        (r'\b([A-Z][a-z]+)\s+(?:Inc|LLC|Ltd|Corp|Technologies?|Systems?)\b',
         lambda m: _abstract_company(m.group(0), level_type)),
    ]

    metric_patterns = [
        (r'(\$\d+(?:\.\d+)?[KMB]?)', lambda m: _abstract_metric(m.group(1), level_type)),
        (r'(\d+(?:\.\d+)?%)\s*(?:increase|growth|improvement|reduction|conversion)',
         lambda m: _abstract_metric(m.group(1), level_type)),
        (r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:users?|customers?|merchants?|transactions?)',
         lambda m: _abstract_metric(m.group(1), level_type)),
    ]

    result = latex
    for pattern, replacer in company_patterns + metric_patterns:
        result = re.sub(pattern, replacer, result)

    return result


def _abstract_company(name: str, level: str) -> str:
    """Abstract company name based on NDA level."""
    if level == "company-abstracted":
        return "Series C FinTech (payments)"  # Example abstraction
    elif level == "domain-abstracted":
        return "B2B SaaS platform"
    elif level == "pattern-abstracted":
        return "high-growth tech company"
    else:  # blackout
        return "[Company Name Redacted]"


def _abstract_metric(metric: str, level: str) -> str:
    """Abstract specific metrics based on NDA level."""
    if level in ("domain-abstracted", "pattern-abstracted"):
        if '%' in metric:
            return "~9%+ (directional)"
        if '$' in metric:
            return "$XM+ ARR"
        if any(c.isdigit() for c in metric):
            return "10K+"
    elif level == "blackout":
        return "[Metric Redacted]"
    return metric


def reorder_sections(latex: str, role: str = "") -> str:
    """
    Reorder LaTeX sections based on target role and mode.
    Uses SECTION_ORDER mapping for different role types.
    """
    # Determine which order to use
    role_lower = role.lower()
    if 'engineer' in role_lower or 'developer' in role_lower:
        order = SECTION_ORDER.get("software-engineer", SECTION_ORDER["ats-max"])
    elif 'product manager' in role_lower or 'pm' in role_lower:
        order = SECTION_ORDER.get("product-manager", SECTION_ORDER["designer-polish"])
    elif 'director' in role_lower or 'vp' in role_lower or 'engineering manager' in role_lower:
        order = SECTION_ORDER.get("engineering-leadership", SECTION_ORDER["designer-polish"])
    elif 'designer' in role_lower:
        order = SECTION_ORDER["designer-polish"]
    else:
        order = SECTION_ORDER["ats-max"]

    # Extract all sections
    sections = {}
    pattern = r'(\\section\*\{([^}]+)\}(.*?))(?=\\section\*\{|$)'
    matches = list(re.finditer(pattern, latex, re.DOTALL))

    if not matches:
        return latex

    # Get preamble (everything before first section)
    preamble_end = matches[0].start()
    preamble = latex[:preamble_end]

    # Extract section content
    for match in matches:
        full_section = match.group(1)
        section_name = match.group(2)
        section_content = match.group(3)
        sections[section_name] = full_section

    # Rebuild in order
    result = preamble
    for section_name in order:
        if section_name in sections:
            result += sections[section_name]

    # Add any remaining sections not in order
    for section_name, content in sections.items():
        if section_name not in order:
            result += content

    return result


def apply_audience_aware(latex: str, job_analysis) -> str:
    """
    Apply audience-aware rewriting for 4 audiences: HR, Hiring Manager, Tech Lead, Executive.
    Injects audience-specific clarifications and emphasis.
    """
    if isinstance(job_analysis, str):
        try:
            job = json.loads(job_analysis)
        except:
            job = {}
    elif isinstance(job_analysis, dict):
        job = job_analysis
    else:
        job = {}

    # Determine primary audience from job analysis
    company_size = job.get('company_intel', {}).get('size', 'Unknown')
    role = job.get('role_title', '')

    # Apply rewrites for each audience
    result = latex
    for audience, config in AUDIENCE_REWRITE_MAP.items():
        result = _apply_audience_rewrites(result, audience, config, role)

    return result


def _apply_audience_rewrites(latex: str, audience: str, config: dict, role: str) -> str:
    """Apply specific audience rewrite patterns."""
    result = latex
    for pattern, replacement in config['patterns']:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def auto_calibrate_density(latex: str, job_analysis: dict, mode: Literal["ats-max", "designer-polish"] = "designer-polish") -> str:
    """Convenience wrapper: calibrate using keyword_targets from job analysis."""
    targets = job_analysis.get('keyword_targets', {}) if isinstance(job_analysis, dict) else {}
    return calibrate_density(latex, targets, mode)


def inject_keywords(latex: str, injection_map: dict, mode: Literal["ats-max", "designer-polish"] = "designer-polish") -> str:
    """
    Inject keywords from injection map into LaTeX resume at optimal locations.
    Priority sections: summary, skills, experience (recent roles first).
    """
    result = latex

    for keyword, target_section in injection_map.items():
        priority = target_section.get('priority', 'medium') if isinstance(target_section, dict) else 'medium'
        section = target_section.get('section', 'skills') if isinstance(target_section, dict) else target_section
        variant = target_section.get('variant', keyword) if isinstance(target_section, dict) else keyword

        if section == 'summary':
            result = inject_into_summary(result, keyword, variant)
        elif section == 'skills':
            result = inject_into_skills(result, keyword, variant)
        elif section.startswith('experience:'):
            idx = int(section.split(':')[1])
            result = inject_into_experience(result, keyword, idx, variant)
        elif section == 'auto':
            # Auto-detect best section based on priority
            if priority == 'critical':
                result = inject_into_summary(result, keyword, variant)
                result = inject_into_skills(result, keyword, variant)
            elif priority == 'high':
                result = inject_into_skills(result, keyword, variant)
                result = inject_into_experience(result, keyword, 0, variant)
            else:
                result = inject_into_skills(result, keyword, variant)

    return result


def inject_into_summary(latex: str, keyword: str, variant: str) -> str:
    """Inject keyword/variant into Professional Summary section."""
    # Find Professional Summary section
    pattern = r'(\\section\*\{Professional Summary\}(.*?))(?=\\section\*\{|$)'
    match = re.search(pattern, latex, re.DOTALL)
    if not match:
        return latex

    summary_content = match.group(2)
    # Add keyword at end of summary if not already present
    if variant.lower() not in summary_content.lower():
        # Find last sentence and append
        new_content = summary_content.rstrip()
        if not new_content.endswith('.'):
            new_content += '.'
        new_content += f' {variant}.'
        result = latex[:match.start(2)] + new_content + latex[match.end(2):]
        return result
    return latex


def inject_into_skills(latex: str, keyword: str, variant: str) -> str:
    """Inject keyword/variant into Skills section."""
    # Find Skills section
    pattern = r'(\\section\*\{Skills\}(.*?))(?=\\section\*\{|$)'
    match = re.search(pattern, latex, re.DOTALL)
    if not match:
        return latex

    skills_content = match.group(2)
    if variant.lower() in skills_content.lower():
        return latex

    # Find a skill line (usually \item or bullet) and append variant
    lines = skills_content.split('\n')
    for i, line in enumerate(lines):
        if r'\item' in line or r'\textbullet' in line:
            # Append to this skill line
            lines[i] = line.rstrip() + f', {variant}'
            break
    else:
        # No skill line found, add new item
        lines.insert(1, f'\\item {variant}')

    new_content = '\n'.join(lines)
    result = latex[:match.start(2)] + new_content + latex[match.end(2):]
    return result


def inject_into_experience(latex: str, keyword: str, role_index: int, variant: str) -> str:
    """Inject keyword/variant into specific experience role."""
    # Find all role entries
    pattern = r'\\roleentry\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}(.*?)(?=\\roleentry\{|\\section\*\{|$)'
    matches = list(re.finditer(pattern, latex, re.DOTALL))

    if role_index >= len(matches) or not matches:
        return latex

    match = matches[role_index]
    content = match.group(4)

    if variant.lower() in content.lower():
        return latex

    # Find last bullet point and append
    bullet_pattern = r'(\\item .*?)(?=\\item|$)'
    bullets = list(re.finditer(bullet_pattern, content, re.DOTALL))

    if bullets:
        last_bullet = bullets[-1]
        new_bullet_content = last_bullet.group(1).rstrip() + f' {variant}.'
        new_content = content[:last_bullet.start(1)] + new_bullet_content + content[last_bullet.end(1):]
    else:
        # No bullets, add after role entry
        new_content = content.rstrip() + f'\\item {variant}.\n'

    result = latex[:match.start(4)] + new_content + latex[match.end(4):]
    return result


def upgrade_verbs(latex: str) -> str:
    """Upgrade weak verbs to stronger action verbs in bullet points."""
    result = latex

    # Only upgrade in bullet points (experience sections)
    for pattern, replacement in TIER2_REPLACEMENTS.items():
        # Only replace in bullet points
        def replacer(match):
            full_line = match.group(0)
            # Only replace if line starts with bullet
            if re.match(r'^\\s*\\\\item', full_line) or re.match(r'^\\s*\\\\textbullet', full_line):
                return re.sub(pattern, replacement, full_line, flags=re.IGNORECASE)
            return full_line

        result = re.sub(r'\\\\item.*?$', replacer, result, flags=re.MULTILINE)

    return result


def add_signal_tags(latex: str, taxonomy_path: str = None) -> str:
    """
    Add signal tags to bullets in experience section.
    Tags are injected as inline badges: [\textbf{Signal-Tag}]
    """
    if taxonomy_path:
        import json
        with open(taxonomy_path) as f:
            taxonomy = json.load(f)
    else:
        # Default taxonomy inline
        taxonomy = {
            "signal_tags": {
                "data-informed-iteration": ["metrics", "data-driven", "analytics", "A/B test", "experiment"],
                "cross-functional-leadership": ["cross-functional", "cross-team", "stakeholder", "partner"],
                "systems-thinking": ["architecture", "system design", "scalability", "platform"],
                "technical-fluency": ["code", "engineering", "technical", "implementation"],
                "user-research-rigor": ["user research", "usability", "user interview", "discovery"],
                "accessibility-advocacy": ["accessibility", "a11y", "WCAG", "inclusive"],
                "craft-polish": ["polish", "craft", "detail", "pixel-perfect", "delight"],
                "zero-to-one-ambiguity": ["zero-to-one", "greenfield", "ambiguity", "from scratch"],
                "strategic-influence": ["strategy", "roadmap", "vision", "influence", "direction"],
                "mentorship-culture": ["mentor", "coach", "grow", "team building", "culture"]
            }
        }

    result = latex
    signal_triggers = taxonomy.get("signal_tags", {})

    # Find all role entries and their bullet points
    pattern = r'(\\roleentry\{[^}]+\}\{[^}]+\}\{[^}]+\})(.*?)(?=\\roleentry\{|\\section\*\{|$)'
    matches = list(re.finditer(pattern, result, re.DOTALL))

    for match in matches:
        role_header = match.group(1)
        bullets_content = match.group(2)

        # Find bullets
        bullet_pattern = r'(\\item\s+.*?)(?=\\item|$)'
        bullet_matches = list(re.finditer(bullet_pattern, bullets_content, re.DOTALL))

        modified_bullets = bullets_content
        offset = 0

        for bm in bullet_matches:
            bullet_text = bm.group(1)
            tags_to_add = []

            for tag, triggers in signal_triggers.items():
                for trigger in triggers:
                    if re.search(rf'\b{re.escape(trigger)}\b', bullet_text, re.IGNORECASE):
                        tags_to_add.append(tag)
                        break  # One tag per bullet max

            if tags_to_add and len(tags_to_add) > 0:
                tag_str = ' '.join(f'[\\textbf{{{tag}}}]' for tag in tags_to_add[:2])  # Max 2 tags
                # Append tag to end of bullet
                new_bullet = bullet_text.rstrip() + f' {tag_str}'
                start = match.start(2) + bm.start(1) + offset
                end = match.start(2) + bm.end(1) + offset
                modified_bullets = modified_bullets[:bm.start(1)] + new_bullet + modified_bullets[bm.end(1):]
                offset += len(new_bullet) - len(bullet_text)

        # Reconstruct
        result = result[:match.start(2)] + modified_bullets + result[match.end(2):]

    return result


def optimize_resume(latex: str, injection_map: dict, mode: Literal["ats-max", "designer-polish"] = "designer-polish") -> str:
    latex = inject_keywords(latex, injection_map, mode)
    latex = upgrade_verbs(latex)
    latex = add_signal_tags(latex)
    return latex


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Optimize LaTeX resume")
    parser.add_argument("--resume", required=True)
    parser.add_argument("--injection-map", required=True)
    parser.add_argument("--mode", choices=["ats-max", "designer-polish"], default="designer-polish")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    latex = Path(args.resume).read_text()
    with open(args.injection_map) as f:
        injection_map = json.load(f)

    optimized = optimize_resume(latex, injection_map, args.mode)
    Path(args.out).write_text(optimized)
    print(f"Optimized resume written to {args.out}")