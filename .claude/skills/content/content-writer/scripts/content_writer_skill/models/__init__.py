"""
Content Writer Skill Models Package
====================================
Exports all data models for the content creation pipeline.
"""

from content_writer_skill.models.enums import (
    Goal,
    Format,
    Tone,
    HookType,
    StructurePattern,
    PersuasionFramework,
    CTAType,
    CTACommitmentLevel,
    GateStatus,
    LintSeverity,
    OutputFormat,
)

from content_writer_skill.models.brief import (
    ContentBrief,
    BRIEF_TEMPLATES,
    apply_template,
    infer_angle,
    infer_missing_fields,
)

from content_writer_skill.models.outline import (
    ContentOutline,
    OutlineSection,
    Hook,
    CTA,
    SEOElements,
)

from content_writer_skill.models.draft import ContentDraft

from content_writer_skill.models.validation_results import (
    ValidationGateResult,
    ValidationResult,
    SEOAudit,
    LintIssue,
    LintResult,
    DEIFinding,
    DEIResult,
    OutputEnvelope,
)

__all__ = [
    # Enums
    "Goal",
    "Format",
    "Tone",
    "HookType",
    "StructurePattern",
    "PersuasionFramework",
    "CTAType",
    "CTACommitmentLevel",
    "GateStatus",
    "LintSeverity",
    "OutputFormat",
    # Brief
    "ContentBrief",
    "BRIEF_TEMPLATES",
    "apply_template",
    "infer_angle",
    "infer_missing_fields",
    # Outline
    "ContentOutline",
    "OutlineSection",
    "Hook",
    "CTA",
    "SEOElements",
    # Draft
    "ContentDraft",
    # Validation
    "ValidationGateResult",
    "ValidationResult",
    "SEOAudit",
    "LintIssue",
    "LintResult",
    "DEIFinding",
    "DEIResult",
    "OutputEnvelope",
]