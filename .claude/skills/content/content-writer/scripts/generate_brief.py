#!/usr/bin/env python3
"""
Content Brief Generator - CLI tool that enforces 4 clarifying questions
before any content generation.
"""

import argparse
import json
import re
import sys
import textwrap
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


# =============================================================================
# TEMPLATES - Pre-filled briefs for common formats
# =============================================================================

TEMPLATES = {
    "blog": {
        "audience": "Professionals seeking practical insights on [topic]; mid-level knowledge, looking for actionable takeaways",
        "goal": "educate",
        "format": "blog",
        "length": "1200-1800 words",
        "tone": "confident, practical, slightly conversational",
        "angle": "The one actionable insight that changes how they approach [topic]",
    },
    "landing-page": {
        "audience": "Decision-makers evaluating solutions for [problem]; aware of problem, evaluating options",
        "goal": "convert",
        "format": "landing-page",
        "length": "800-1200 words",
        "tone": "confident, authoritative, trust-building",
        "angle": "Why this solution is the logical choice for [specific problem/audience]",
    },
    "email": {
        "audience": "Subscribers who know the brand; warm audience, varying engagement levels",
        "goal": "nurture",
        "format": "email",
        "length": "150-300 words",
        "tone": "warm, personal, conversational",
        "angle": "One insight or story that moves them one step closer to trust/action",
    },
    "social": {
        "audience": "Scrolling professionals; 2-second attention span, skimming for value",
        "goal": "engage",
        "format": "social",
        "length": "150-280 characters (X/LinkedIn) or 100-150 words (LinkedIn long-form)",
        "tone": "punchy, insightful, conversational",
        "angle": "One contrarian take or actionable insight that stops the scroll",
    },
    "case-study": {
        "audience": "Prospects evaluating solutions; need proof, specifics, and relatability",
        "goal": "persuade",
        "format": "case-study",
        "length": "1200-2000 words",
        "tone": "credible, specific, customer-voice-forward",
        "angle": "How [customer] achieved [specific result] by solving [specific problem] differently",
    },
    "whitepaper": {
        "audience": "Senior decision-makers and technical evaluators; deep knowledge, high scrutiny",
        "goal": "educate, persuade",
        "format": "whitepaper",
        "length": "3000-6000 words",
        "tone": "authoritative, evidence-based, authoritative but accessible",
        "angle": "The definitive analysis of [problem/trend] that reframes how leaders think about [topic]",
    },
    "press-release": {
        "audience": "Journalists, analysts, industry observers; time-pressed, seeking newsworthiness",
        "goal": "inform",
        "format": "press-release",
        "length": "400-600 words",
        "tone": "objective, newsworthy, quote-rich, factual",
        "angle": "The one newsworthy development that matters to [industry/audience] right now",
    },
    "video-script": {
        "audience": "Viewers with 3-second attention span; watching for value or entertainment",
        "goal": "educate, entertain",
        "format": "video-script",
        "length": "60-90 seconds (150-250 words)",
        "tone": "energetic, clear, hook-driven",
        "angle": "One hook-worthy insight delivered in a visual, memorable way",
    },
}

LENGTH_PATTERNS = [
    r"\b\d+[,-]?\d*\s*-\s*\d+[,-]?\d*\s*(?:words?|characters?|chars?|minutes?|seconds?|pages?)\b",
    r"\b\d+[,-]?\d*\s*(?:words?|characters?|chars?|minutes?|seconds?|pages?)\b",
    r"\b\d+\s*-\s*\d+\s*(?:sec|secs|min|mins)\b",
]

GOAL_OPTIONS = [
    "educate",
    "persuade",
    "inform",
    "entertain",
    "convert",
    "nurture",
    "reassure",
    "warn",
]

FORMAT_OPTIONS = [
    "blog",
    "landing-page",
    "email",
    "social",
    "case-study",
    "whitepaper",
    "press-release",
    "video-script",
]


# =============================================================================
# QUESTIONS
# =============================================================================

QUESTIONS = [
    {
        "key": "audience",
        "prompt": "Audience: Who is reading this? (role, knowledge level, pain points, existing knowledge)",
        "hint": "e.g., 'Senior engineers evaluating monitoring tools; know Prometheus, pain point is alert fatigue'",
    },
    {
        "key": "goal",
        "prompt": "Goal: What should this piece DO? (educate, persuade, inform, entertain, convert, nurture, reassure, warn)",
        "hint": "Pick one primary goal: educate / persuade / inform / entertain / convert / nurture / reassure / warn",
    },
    {
        "key": "format",
        "prompt": "Format & Length: Where will this live? (blog, email, landing-page, social, PDF, print? word count)",
        "hint": "e.g., 'blog post, 1500 words' or 'LinkedIn post, 200 words'",
    },
    {
        "key": "tone",
        "prompt": "Tone & Voice: What feeling should the reader walk away with? (confident, reassured, curious, urgent, inspired) Brand voice examples?",
        "hint": "e.g., 'confident but warm, like Stripe docs' or 'urgent and direct, like a breaking news alert'",
    },
]


# =============================================================================
# DATA CLASS
# =============================================================================

@dataclass
class Brief:
    audience: str = ""
    goal: str = ""
    format: str = ""
    length: str = ""
    tone: str = ""
    angle: str = ""
    assumptions: List[str] = field(default_factory=list)
    template_used: str = ""
    source_file: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audience": self.audience,
            "goal": self.goal,
            "format": self.format,
            "length": self.length,
            "tone": self.tone,
            "angle": self.angle,
            "assumptions": self.assumptions,
        }

    def get_missing_fields(self) -> List[str]:
        missing = []
        for key in ["audience", "goal", "format", "length", "tone"]:
            if not getattr(self, key):
                missing.append(key)
        return missing


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def infer_angle(brief: Brief) -> str:
    """Infer the core angle from brief components."""
    audience_short = brief.audience.split(";")[0].split(",")[0].strip()[:60]
    goal_short = brief.goal.strip()
    format_short = brief.format.strip()

    angle_templates = {
        "educate": f"The one insight that changes how {audience_short} approaches [topic]",
        "persuade": f"Why {audience_short} should choose [solution/approach] over alternatives",
        "inform": f"What {audience_short} needs to know about [topic] right now",
        "entertain": f"A memorable take on [topic] that {audience_short} will share",
        "convert": f"The case for {audience_short} to take [specific action] today",
        "nurture": f"One step deeper in trust for {audience_short} on [topic]",
        "reassure": f"Evidence that [concern] is solvable for {audience_short}",
        "warn": f"The risk {audience_short} is overlooking in [topic]",
    }

    return angle_templates.get(goal_short, f"The key takeaway for {audience_short} about [topic]")


def split_format_and_length(value: str) -> Tuple[str, str]:
    """Split a combined format/length answer into separate fields."""
    cleaned = value.strip()
    if not cleaned:
        return "", ""

    for pattern in LENGTH_PATTERNS:
        match = re.search(pattern, cleaned, flags=re.IGNORECASE)
        if match:
            length = match.group(0).strip()
            fmt = (cleaned[:match.start()] + cleaned[match.end():]).strip(" ,;:-")
            return fmt or cleaned, length

    return cleaned, ""


def infer_missing_fields(brief: Brief) -> Brief:
    """Fill empty required fields from template or conservative defaults."""
    format_key = brief.format.lower().replace(" ", "-") if brief.format else ""

    if format_key in TEMPLATES:
        template = TEMPLATES[format_key]
        for key in ["audience", "goal", "format", "length", "tone"]:
            if not getattr(brief, key):
                setattr(brief, key, template[key])
                brief.assumptions.append(f"Inferred {key} from '{format_key}' format: {template[key]}")

    fallback_values = {
        "audience": "General professional audience; knowledge level and pain points not specified",
        "goal": "educate",
        "format": "blog",
        "length": "800-1200 words",
        "tone": "professional, warm, conversational",
    }

    for key, value in fallback_values.items():
        if not getattr(brief, key):
            setattr(brief, key, value)
            brief.assumptions.append(f"Inferred {key} from default assumption: {value}")

    if not brief.angle:
        brief.angle = infer_angle(brief)
        brief.assumptions.append("Inferred angle from audience, goal, and format")

    return brief


def load_brief_from_file(filepath: str) -> Brief:
    """Load brief from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    brief = Brief()
    for key, value in data.items():
        if hasattr(brief, key):
            setattr(brief, key, value)
    return brief


def save_brief(brief: Brief, filename: str) -> str:
    """Save brief to briefs/ directory."""
    briefs_dir = Path.cwd() / "briefs"
    briefs_dir.mkdir(parents=True, exist_ok=True)
    filepath = briefs_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(brief.to_dict(), f, indent=2, ensure_ascii=False)
    return str(filepath)


def load_existing_content(filepath: str) -> str:
    """Load content from file for auditing."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.read_text(encoding="utf-8")


def infer_brief_from_content(content: str) -> Brief:
    """Reverse-engineer a brief from existing content."""
    brief = Brief()

    word_count = len(content.split())
    char_count = len(content)

    if word_count < 300:
        fmt, length = "social", f"{word_count} words"
    elif word_count < 800:
        fmt, length = "email", f"{word_count} words"
    elif word_count < 2000:
        fmt, length = "blog", f"{word_count} words"
    elif word_count < 4000:
        fmt, length = "case-study", f"{word_count} words"
    else:
        fmt, length = "whitepaper", f"{word_count} words"

    brief.format = fmt
    brief.length = length

    content_lower = content.lower()

    if any(w in content_lower for w in ["buy", "sign up", "start free", "get started", "conversion", "cta"]):
        brief.goal = "convert"
    elif any(w in content_lower for w in ["case study", "customer", "achieved", "results:", "roi", "testimonial"]):
        brief.goal = "persuade"
    elif any(w in content_lower for w in ["announced", "press release", "partnership", "launch", "acquisition"]):
        brief.goal = "inform"
    elif any(w in content_lower for w in ["deep dive", "analysis", "research", "methodology", "framework"]):
        brief.goal = "educate"
    else:
        brief.goal = "educate"

    if word_count < 500:
        brief.audience = "Busy professionals scanning for quick value"
    elif "dear " in content_lower or "hi " in content_lower:
        brief.audience = "Email subscribers; warm audience"
    else:
        brief.audience = "Professionals seeking insight on this topic; mid-level knowledge assumed"

    if "you " in content_lower and "we " in content_lower:
        brief.tone = "conversational, direct, you-focused"
    elif "analysis" in content_lower or "methodology" in content_lower:
        brief.tone = "authoritative, evidence-based, analytical"
    elif "!" in content and word_count < 300:
        brief.tone = "energetic, punchy, engaging"
    else:
        brief.tone = "professional, warm, informative"

    brief = infer_missing_fields(brief)
    brief.assumptions.insert(0, "Reverse-engineered from existing content; assumptions may need verification")

    return brief


def audit_existing_content(filepath: str, output_json: bool = False) -> Brief:
    """Audit existing content and reverse-engineer brief."""
    content = load_existing_content(filepath)
    brief = infer_brief_from_content(content)
    brief.source_file = filepath

    warnings = validate_brief(brief)
    if warnings and not output_json:
        print("\n[!] AUDIT WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    print_brief(brief, as_json=output_json)

    if not output_json:
        saved_path = save_brief(brief, f"audit_{Path(filepath).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        print(f"Saved audit brief to: {saved_path}")

    return brief


def apply_template(brief: Brief, template_name: str) -> Brief:
    """Apply template defaults to brief, only filling empty fields."""
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}. Options: {', '.join(TEMPLATES.keys())}")

    template = TEMPLATES[template_name]
    assumptions = []

    for key, value in template.items():
        if key == "angle":
            continue
        current = getattr(brief, key, "")
        if not current:
            setattr(brief, key, value)
            assumptions.append(f"Inferred {key} from '{template_name}' template: {value[:60]}...")

    brief.template_used = template_name
    brief.angle = infer_angle(brief)
    brief.assumptions.extend(assumptions)
    return brief


def prompt_for_field(brief: Brief, field: str, hint: str = "") -> str:
    """Prompt user for a single field."""
    current = getattr(brief, field, "")
    prompt_parts = [QUESTIONS[[q["key"] for q in QUESTIONS].index(field)]["prompt"]]
    if hint:
        prompt_parts.append(f"  Hint: {hint}")
    if current:
        prompt_parts.append(f"  [{current}]")
    prompt = "\n".join(prompt_parts) + "\n> "

    while True:
        response = input(prompt).strip()
        if response:
            return response
        elif current:
            return current
        else:
            print("  This field is required. Please provide a value or press Ctrl+C to cancel.")


def interactive_mode(brief: Brief) -> Brief:
    """Run interactive mode prompting for all 4 questions."""
    print("\n" + "=" * 60)
    print("CONTENT BRIEF GENERATOR - Interactive Mode")
    print("=" * 60)
    print("Answer the 4 clarifying questions. Press Enter to keep defaults [in brackets].\n")

    for q in QUESTIONS:
        key = q["key"]
        hint = q["hint"]
        value = prompt_for_field(brief, key, hint)
        if key == "format":
            fmt, length = split_format_and_length(value)
            brief.format = fmt
            if length:
                brief.length = length
            elif not brief.length:
                brief.assumptions.append("Length was not specified in the format answer; it will be inferred from format")
        else:
            setattr(brief, key, value)
        print()

    brief = infer_missing_fields(brief)
    if not brief.assumptions:
        brief.assumptions.append("All fields provided interactively; angle inferred from format+goal")

    return brief


def validate_brief(brief: Brief) -> List[str]:
    """Validate brief and return list of warnings/issues."""
    warnings = []

    missing = brief.get_missing_fields()
    if missing:
        warnings.append(f"Missing required fields: {', '.join(missing)}")

    if brief.goal and brief.goal.lower() not in GOAL_OPTIONS:
        warnings.append(f"Goal '{brief.goal}' not in standard options: {', '.join(GOAL_OPTIONS)}")

    if brief.format and brief.format.lower() not in FORMAT_OPTIONS:
        warnings.append(f"Format '{brief.format}' not in standard options: {', '.join(FORMAT_OPTIONS)}")

    return warnings


def print_brief(brief: Brief, as_json: bool = False):
    """Print brief in JSON or human-readable format."""
    if as_json:
        print(json.dumps(brief.to_dict(), indent=2, ensure_ascii=False))
        return

    print("\n" + "=" * 60)
    print("GENERATED CONTENT BRIEF")
    print("=" * 60)
    print(f"  Audience : {brief.audience}")
    print(f"  Goal     : {brief.goal}")
    print(f"  Format   : {brief.format}")
    print(f"  Length   : {brief.length}")
    print(f"  Tone     : {brief.tone}")
    print(f"  Angle    : {brief.angle}")
    if brief.template_used:
        print(f"  Template : {brief.template_used}")
    if brief.source_file:
        print(f"  Source   : {brief.source_file}")
    if brief.assumptions:
        print(f"\n  Assumptions made:")
        for a in brief.assumptions:
            print(f"    - {a}")
    print("=" * 60 + "\n")


# =============================================================================
# MAIN CLI
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brief",
        description="Content Brief Generator - Enforces 4 clarifying questions before content generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              brief                          # Interactive mode (prompts for all 4 questions)
              brief --json                   # Interactive mode, JSON output
              brief --template blog          # Pre-fill from blog template, then prompt
              brief --template email --json  # Pre-fill from email template, JSON output
              brief --from-file brief.json   # Load brief from JSON file
              brief --audit-existing post.md # Reverse-engineer brief from existing content
              brief --audit-existing post.md --json  # Audit with JSON output
              brief --list-templates         # List available templates
              brief --save brief.json        # Save brief to briefs/ directory

            Templates: blog, landing-page, email, social, case-study, whitepaper, press-release, video-script
        """),
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output brief as JSON (for programmatic use)",
    )

    parser.add_argument(
        "--template",
        choices=list(TEMPLATES.keys()),
        help="Pre-fill brief from format template (blog, landing-page, email, social, case-study, whitepaper, press-release, video-script)",
    )

    parser.add_argument(
        "--from-file",
        type=str,
        help="Load brief from JSON file",
    )

    parser.add_argument(
        "--audit-existing",
        type=str,
        metavar="FILE",
        help="Read existing content file, reverse-engineer brief, show gaps",
    )

    parser.add_argument(
        "--save",
        type=str,
        metavar="FILENAME",
        help="Save brief to briefs/ directory with given filename",
    )

    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available format templates and exit",
    )

    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Fail if any required fields are missing (for CI/automation)",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.list_templates:
        print("\nAvailable format templates:")
        for name, tmpl in TEMPLATES.items():
            print(f"  {name:15} - {tmpl['format']:15} | {tmpl['goal']:10} | {tmpl['length']}")
        print()
        return 0

    if args.audit_existing:
        try:
            audit_existing_content(args.audit_existing, output_json=args.json)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error auditing content: {e}", file=sys.stderr)
            return 1
        return 0

    brief = Brief()

    if args.from_file:
        try:
            brief = load_brief_from_file(args.from_file)
        except Exception as e:
            print(f"Error loading brief: {e}", file=sys.stderr)
            return 1

    if args.template:
        try:
            brief = apply_template(brief, args.template)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if not args.from_file and not args.template and not args.non_interactive:
        try:
            brief = interactive_mode(brief)
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            return 1
        except EOFError:
            print("\n\nCancelled.")
            return 1

    brief = infer_missing_fields(brief)

    warnings = validate_brief(brief)
    if warnings and not args.json:
        print("\n[!] VALIDATION WARNINGS:")
        for w in warnings:
            print(f"  - {w}")

    if args.non_interactive:
        missing = brief.get_missing_fields()
        if missing:
            print(f"Error: Missing required fields: {', '.join(missing)}", file=sys.stderr)
            print("Use --template or --from-file to pre-fill, or run interactively.", file=sys.stderr)
            return 1

    print_brief(brief, as_json=args.json)

    if args.save:
        saved_path = save_brief(brief, args.save)
        if not args.json:
            print(f"Saved to: {saved_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())