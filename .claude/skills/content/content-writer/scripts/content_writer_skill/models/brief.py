"""
Content Brief Model
===================
Core data structure for content briefs - the 4 clarifying questions plus inferred angle.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models.enums import Goal, Format, Tone


@dataclass
class ContentBrief:
    """
    Complete content brief with all required fields.

    The 4 clarifying questions:
    1. Audience: Who is reading this?
    2. Goal: What should this piece DO?
    3. Format & Length: Where will this live? How long?
    4. Tone & Voice: What feeling should the reader walk away with?

    Plus inferred angle (the one thing this piece must leave the reader with).
    """
    audience: str = ""
    goal: Goal = Goal.EDUCATE
    format: Format = Format.BLOG
    length: str = ""
    tone: str = ""
    angle: str = ""

    # SEO fields
    primary_keyword: str = ""
    secondary_keywords: List[str] = field(default_factory=list)
    target_audience_level: str = ""  # beginner, intermediate, advanced

    # Metadata
    assumptions: List[str] = field(default_factory=list)
    template_used: Optional[str] = None
    source_file: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Required fields for validation
    REQUIRED_FIELDS = ["audience", "goal", "format", "length", "tone", "angle"]

    def __post_init__(self):
        """Normalize enum fields."""
        if isinstance(self.goal, str):
            self.goal = Goal(self.goal)
        if isinstance(self.format, str):
            self.format = Format(self.format)

    def get_missing_fields(self) -> List[str]:
        """Return list of required fields that are empty."""
        missing = []
        for field_name in self.REQUIRED_FIELDS:
            value = getattr(self, field_name, "")
            if not value or (isinstance(value, str) and not value.strip()):
                missing.append(field_name)
        return missing

    def is_complete(self) -> bool:
        """Check if all required fields are present."""
        return len(self.get_missing_fields()) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data["goal"] = self.goal.value
        data["format"] = self.format.value
        return data

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentBrief":
        """Create from dictionary."""
        # Handle enum conversion
        if "goal" in data and isinstance(data["goal"], str):
            data["goal"] = Goal(data["goal"])
        if "format" in data and isinstance(data["format"], str):
            data["format"] = Format(data["format"])
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "ContentBrief":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def validate(self) -> List[str]:
        """Validate brief and return list of warnings/issues."""
        warnings = []

        missing = self.get_missing_fields()
        if missing:
            warnings.append(f"Missing required fields: {', '.join(missing)}")

        if self.goal not in list(Goal):
            warnings.append(f"Goal '{self.goal}' not in standard options")

        if self.format not in list(Format):
            warnings.append(f"Format '{self.format}' not in standard options")

        # Check length format
        if self.length:
            import re
            length_patterns = [
                r"\d+[,-]?\d*\s*-\s*\d+[,-]?\d*\s*(?:words?|characters?|chars?|minutes?|seconds?|pages?)",
                r"\d+[,-]?\d*\s*(?:words?|characters?|chars?|minutes?|seconds?|pages?)",
                r"\d+\s*-\s*\d+\s*(?:sec|secs|min|mins)"
            ]
            if not any(re.search(p, self.length, re.IGNORECASE) for p in length_patterns):
                warnings.append(f"Length '{self.length}' doesn't match expected format (e.g., '1200-1800 words')")

        return warnings


# Template definitions for common formats
BRIEF_TEMPLATES = {
    "blog": {
        "audience": "Professionals seeking practical insights on [topic]; mid-level knowledge, looking for actionable takeaways",
        "goal": Goal.EDUCATE,
        "format": Format.BLOG,
        "length": "1200-1800 words",
        "tone": "confident, practical, slightly conversational",
        "angle": "The one actionable insight that changes how they approach [topic]",
    },
    "landing-page": {
        "audience": "Decision-makers evaluating solutions for [problem]; aware of problem, evaluating options",
        "goal": Goal.CONVERT,
        "format": Format.LANDING_PAGE,
        "length": "800-1200 words",
        "tone": "confident, authoritative, trust-building",
        "angle": "Why this solution is the logical choice for [specific problem/audience]",
    },
    "email": {
        "audience": "Subscribers who know the brand; warm audience, varying engagement levels",
        "goal": Goal.NURTURE,
        "format": Format.EMAIL,
        "length": "150-300 words",
        "tone": "warm, personal, conversational",
        "angle": "One insight or story that moves them one step closer to trust/action",
    },
    "social": {
        "audience": "Scrolling professionals; 2-second attention span, skimming for value",
        "goal": Goal.ENTERTAIN,
        "format": Format.SOCIAL,
        "length": "150-280 characters (X/LinkedIn) or 100-150 words (LinkedIn long-form)",
        "tone": "punchy, insightful, conversational",
        "angle": "One contrarian take or actionable insight that stops the scroll",
    },
    "case-study": {
        "audience": "Prospects evaluating solutions; need proof, specifics, and relatability",
        "goal": Goal.PERSUADE,
        "format": Format.CASE_STUDY,
        "length": "1200-2000 words",
        "tone": "credible, specific, customer-voice-forward",
        "angle": "How [customer] achieved [specific result] by solving [specific problem] differently",
    },
    "whitepaper": {
        "audience": "Senior decision-makers and technical evaluators; deep knowledge, high scrutiny",
        "goal": Goal.EDUCATE,
        "format": Format.WHITEPAPER,
        "length": "3000-6000 words",
        "tone": "authoritative, evidence-based, authoritative but accessible",
        "angle": "The definitive analysis of [problem/trend] that reframes how leaders think about [topic]",
    },
    "press-release": {
        "audience": "Journalists, analysts, industry observers; time-pressed, seeking newsworthiness",
        "goal": Goal.INFORM,
        "format": Format.PRESS_RELEASE,
        "length": "400-600 words",
        "tone": "objective, newsworthy, quote-rich, factual",
        "angle": "The one newsworthy development that matters to [industry/audience] right now",
    },
    "video-script": {
        "audience": "Viewers with 3-second attention span; watching for value or entertainment",
        "goal": Goal.EDUCATE,
        "format": Format.VIDEO_SCRIPT,
        "length": "60-90 seconds (150-250 words)",
        "tone": "energetic, clear, hook-driven",
        "angle": "One hook-worthy insight delivered in a visual, memorable way",
    },
}


def apply_template(brief: ContentBrief, template_name: str) -> ContentBrief:
    """Apply template defaults to brief, only filling empty fields."""
    if template_name not in BRIEF_TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}. Options: {', '.join(BRIEF_TEMPLATES.keys())}")

    template = BRIEF_TEMPLATES[template_name]
    assumptions = []

    for key, value in template.items():
        if key == "angle":
            continue
        current = getattr(brief, key, None)
        if not current:
            setattr(brief, key, value)
            assumptions.append(f"Inferred {key} from '{template_name}' template: {str(value)[:60]}...")

    brief.template_used = template_name
    brief.assumptions.extend(assumptions)

    # Infer angle if not set
    if not brief.angle:
        brief.angle = infer_angle(brief)
        brief.assumptions.append("Inferred angle from audience, goal, and format")

    return brief


def infer_angle(brief: ContentBrief) -> str:
    """Infer the core angle from brief components."""
    audience_short = brief.audience.split(";")[0].split(",")[0].strip()[:60]
    goal_short = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
    format_short = brief.format.value if isinstance(brief.format, Format) else str(brief.format)

    angle_templates = {
        Goal.EDUCATE: f"The one insight that changes how {audience_short} approaches [topic]",
        Goal.PERSUADE: f"Why {audience_short} should choose [solution/approach] over alternatives",
        Goal.INFORM: f"What {audience_short} needs to know about [topic] right now",
        Goal.ENTERTAIN: f"A memorable take on [topic] that {audience_short} will share",
        Goal.CONVERT: f"The case for {audience_short} to take [specific action] today",
        Goal.NURTURE: f"One step deeper in trust for {audience_short} on [topic]",
        Goal.REASSURE: f"Evidence that [concern] is solvable for {audience_short}",
        Goal.WARN: f"The risk {audience_short} is overlooking in [topic]",
    }

    return angle_templates.get(goal_short, f"The key takeaway for {audience_short} about [topic]")


def infer_missing_fields(brief: ContentBrief) -> ContentBrief:
    """Fill empty required fields from template or conservative defaults."""
    # Try to infer from format
    format_key = brief.format.value if isinstance(brief.format, Format) else str(brief.format)
    if format_key in BRIEF_TEMPLATES:
        return apply_template(brief, format_key)

    # Fallback defaults
    fallback_values = {
        "audience": "General professional audience; knowledge level and pain points not specified",
        "goal": Goal.EDUCATE,
        "format": Format.BLOG,
        "length": "800-1200 words",
        "tone": "professional, warm, conversational",
    }

    for key, value in fallback_values.items():
        if not getattr(brief, key, None):
            setattr(brief, key, value)
            brief.assumptions.append(f"Inferred {key} from default assumption: {value}")

    if not brief.angle:
        brief.angle = infer_angle(brief)
        brief.assumptions.append("Inferred angle from audience, goal, and format")

    return brief