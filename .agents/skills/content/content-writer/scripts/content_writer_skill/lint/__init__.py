"""
Lint Package
============
Linting rules and logic for content validation.
"""

from content_writer_skill.lint.engine import LintEngine
from content_writer_skill.lint.rules import (
    BANNED_OPENERS,
    ROBOTIC_TELLS,
    FORMAL_PHRASES,
    HEDGING_PHRASES,
    EM_DASH_PATTERN,
    CONTRACTION_MAP,
    SENTENCE_VARIETY_MIN,
    SENTENCE_VARIETY_MAX,
)

__all__ = [
    "LintEngine",
    "BANNED_OPENERS",
    "ROBOTIC_TELLS",
    "FORMAL_PHRASES",
    "HEDGING_PHRASES",
    "EM_DASH_PATTERN",
    "CONTRACTION_MAP",
    "SENTENCE_VARIETY_MIN",
    "SENTENCE_VARIETY_MAX",
]
