"""
Content Writer Skill Package
============================
A 5-phase content creation pipeline with 6 validation gates.
Provides both CLI tool and agent-callable Python package.
"""

from content_writer_skill.models import (
    ContentBrief,
    ContentOutline,
    ContentDraft,
    Goal,
    Format,
    Tone,
)
from content_writer_skill.pipeline import ContentPipeline
from content_writer_skill.validation import validate_brief, validate_outline, validate_draft
from content_writer_skill.output_manager import OutputManager, OutputFormat

__version__ = "2.1.0"
__author__ = "AI-Workflows"

__all__ = [
    "ContentBrief",
    "ContentOutline",
    "ContentDraft",
    "Goal",
    "Format",
    "Tone",
    "ContentPipeline",
    "validate_brief",
    "validate_outline",
    "validate_draft",
    "OutputManager",
    "OutputFormat",
]