"""
Phase 1: Discover & Align
=========================
Content brief intake, audience analysis, template selection, and brief validation.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models import ContentBrief, ValidationGateResult, Goal, Format, Tone
from content_writer_skill.models.brief import BRIEF_TEMPLATES, apply_template, infer_missing_fields


@dataclass
class Phase1Result:
    """Result of Phase 1: Discover & Align."""
    brief: ContentBrief
    validation: ValidationGateResult
    assumptions: List[str]
    template_applied: Optional[str]
    questions_needed: List[str]


class DiscoverAlignPhase:
    """
    Phase 1: Discover & Align

    Inputs: Raw brief input (JSON, CLI args, or interactive)
    Outputs: Validated ContentBrief with template applied and assumptions documented
    """

    REQUIRED_FIELDS = ["audience", "goal", "format", "length", "tone", "angle"]

    def __init__(self, strict_mode: bool = False):
        """
        Initialize Phase 1.

        Args:
            strict_mode: If True, fail on missing fields instead of inferring
        """
        self.strict_mode = strict_mode

    def run(self, input_data: Dict[str, Any]) -> Phase1Result:
        """
        Execute Phase 1.

        Args:
            input_data: Raw input containing brief fields

        Returns:
            Phase1Result with validated brief
        """
        # Create brief from input
        brief = ContentBrief.from_dict(input_data)

        # Track assumptions
        assumptions = []

        # Apply template if format specified and template exists
        template_applied = None
        format_key = brief.format.value if isinstance(brief.format, Format) else str(brief.format)

        if format_key in BRIEF_TEMPLATES:
            brief = apply_template(brief, format_key)
            template_applied = format_key
            assumptions.append(f"Applied '{format_key}' template defaults")

        # Infer missing fields
        missing_before = brief.get_missing_fields()
        if missing_before and not self.strict_mode:
            brief = infer_missing_fields(brief)
            assumptions.extend(brief.assumptions)
        elif missing_before and self.strict_mode:
            raise ValueError(f"Missing required fields in strict mode: {missing_before}")

        # Validate brief
        validation = self._validate_brief(brief)

        # Determine what questions still need answers
        questions_needed = self._get_remaining_questions(brief)

        return Phase1Result(
            brief=brief,
            validation=validation,
            assumptions=assumptions,
            template_applied=template_applied,
            questions_needed=questions_needed,
        )

    def _validate_brief(self, brief: ContentBrief) -> ValidationGateResult:
        """Validate the brief against schema and rules."""
        issues = []
        metrics = {}

        # Check required fields
        missing = brief.get_missing_fields()
        for field in missing:
            issues.append({
                "code": "MISSING_FIELD",
                "message": f"Required field '{field}' is empty",
                "severity": "error",
                "field": field,
                "suggestion": f"Provide {field} or use a template that infers it",
            })

        # Validate goal
        if isinstance(brief.goal, Goal):
            metrics["goal"] = brief.goal.value
        else:
            issues.append({
                "code": "INVALID_GOAL",
                "message": f"Goal '{brief.goal}' not in standard goals",
                "severity": "warning",
                "field": "goal",
            })

        # Validate format
        if isinstance(brief.format, Format):
            metrics["format"] = brief.format.value
        else:
            issues.append({
                "code": "INVALID_FORMAT",
                "message": f"Format '{brief.format}' not in standard formats",
                "severity": "warning",
                "field": "format",
            })

        # Validate length format
        if brief.length:
            import re
            length_patterns = [
                r"\d+[,-]?\d*\s*-\s*\d+[,-]?\d*\s*(?:words?|characters?|chars?|minutes?|seconds?|pages?)",
                r"\d+[,-]?\d*\s*(?:words?|characters?|chars?|minutes?|seconds?|pages?)",
                r"\d+\s*-\s*\d+\s*(?:sec|secs|min|mins)",
            ]
            if not any(re.search(p, brief.length, re.IGNORECASE) for p in length_patterns):
                issues.append({
                    "code": "INVALID_LENGTH_FORMAT",
                    "message": f"Length '{brief.length}' doesn't match expected format (e.g., '1200-1800 words')",
                    "severity": "warning",
                    "field": "length",
                    "suggestion": "Use format like '1200-1800 words' or '500 words'",
                })
            else:
                metrics["length"] = brief.length

        # Count assumptions
        metrics["assumption_count"] = len(brief.assumptions)
        metrics["template_used"] = brief.template_used

        passed = len([i for i in issues if i["severity"] == "error"]) == 0

        return ValidationGateResult(
            gate=1,
            gate_name="brief-validation",
            passed=passed,
            issues=issues,
            metrics=metrics,
        )

    def _get_remaining_questions(self, brief: ContentBrief) -> List[str]:
        """Get clarifying questions for remaining unknowns."""
        questions = []

        if not brief.audience or not brief.audience.strip():
            questions.append("Who is the target audience? (role, knowledge level, pain points)")

        if not brief.goal or (isinstance(brief.goal, Goal) and brief.goal == Goal.EDUCATE and not brief.angle):
            questions.append("What is the PRIMARY goal? (educate, persuade, convert, inform, entertain, nurture, reassure, warn)")

        if not brief.format or (isinstance(brief.format, Format) and brief.format == Format.BLOG and not brief.angle):
            questions.append("What format and where will this live? (blog, landing page, email, social, case study, etc.)")

        if not brief.length or not brief.length.strip():
            questions.append("What is the target length? (e.g., '1200-1800 words', '500 words', '90 seconds')")

        if not brief.tone or not brief.tone.strip():
            questions.append("What tone/voice should this have? (e.g., 'confident, practical', 'warm, personal')")

        if not brief.angle or not brief.angle.strip():
            questions.append("What is the ONE thing the reader must remember? (the angle/key takeaway)")

        return questions


def run_discover_align(input_data: Dict[str, Any], strict_mode: bool = False) -> Phase1Result:
    """Convenience function to run Phase 1."""
    phase = DiscoverAlignPhase(strict_mode=strict_mode)
    return phase.run(input_data)


def load_brief_from_file(filepath: str) -> ContentBrief:
    """Load brief from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return ContentBrief.from_dict(data)


def load_brief_from_json(json_str: str) -> ContentBrief:
    """Load brief from JSON string."""
    return ContentBrief.from_json(json_str)