"""
Content Draft Model
===================
Core data structure for drafted content with metadata, SEO audit, and lint results.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models.enums import Goal, Format, Tone
from content_writer_skill.models.outline import ContentOutline
from content_writer_skill.models.validation_results import (
    SEOAudit,
    LintResult,
    DEIResult,
    ValidationGateResult,
)


@dataclass
class ContentDraft:
    """
    Complete drafted content with all validation results.

    Generated in Phase 3 (Draft), validated in Phases 4-5, finalized in Phase 6.
    """
    content: str = ""
    outline: Optional[ContentOutline] = None
    brief: Optional['ContentBrief'] = None  # Forward reference

    # Validation results (Phases 4-6)
    brief_validation: Optional[ValidationGateResult] = None
    lint_validation: Optional[ValidationGateResult] = None
    structure_validation: Optional[ValidationGateResult] = None
    seo_conversion_validation: Optional[ValidationGateResult] = None
    dei_accessibility_validation: Optional[ValidationGateResult] = None
    output_envelope_validation: Optional[ValidationGateResult] = None

    # Detailed results
    seo_audit: Optional[SEOAudit] = None
    lint_result: Optional[LintResult] = None
    dei_result: Optional[DEIResult] = None

    # Final envelope (Phase 6)
    output_envelope: Optional[Dict[str, Any]] = None

    # Metadata
    word_count: int = 0
    sentence_count: int = 0
    reading_time_minutes: float = 0.0
    draft_number: int = 1
    template_used: Optional[str] = None
    source_file: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Compute derived metrics."""
        if self.content:
            self.word_count = len(self.content.split())
            self.sentence_count = len([s for s in self.content.split('.') if s.strip()])
            self.reading_time_minutes = round(self.word_count / 200, 1)

    def all_gates_passed(self) -> bool:
        """Check if all validation gates passed."""
        gates = [
            self.brief_validation,
            self.lint_validation,
            self.structure_validation,
            self.seo_conversion_validation,
            self.dei_accessibility_validation,
            self.output_envelope_validation,
        ]
        return all(g and g.passed for g in gates)

    def get_failed_gates(self) -> List[int]:
        """Get list of failed gate numbers."""
        gates = [
            (1, self.brief_validation),
            (2, self.lint_validation),
            (3, self.structure_validation),
            (4, self.seo_conversion_validation),
            (5, self.dei_accessibility_validation),
            (6, self.output_envelope_validation),
        ]
        return [num for num, gate in gates if gate and not gate.passed]

    def get_all_issues(self) -> List[Dict[str, Any]]:
        """Aggregate all issues from all gates."""
        issues = []
        gates = [
            ("brief", self.brief_validation),
            ("lint", self.lint_validation),
            ("structure", self.structure_validation),
            ("seo", self.seo_conversion_validation),
            ("dei", self.dei_accessibility_validation),
            ("envelope", self.output_envelope_validation),
        ]
        for gate_name, gate in gates:
            if gate and gate.issues:
                for issue in gate.issues:
                    issue = issue.copy()
                    issue["gate"] = gate_name
                    issues.append(issue)
        return issues

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = {
            "content": self.content,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "reading_time_minutes": self.reading_time_minutes,
            "draft_number": self.draft_number,
            "template_used": self.template_used,
            "source_file": self.source_file,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

        # Add nested objects
        if self.outline:
            data["outline"] = self.outline.to_dict()
        if self.brief:
            from content_writer_skill.models.brief import ContentBrief
            if isinstance(self.brief, ContentBrief):
                data["brief"] = self.brief.to_dict()
            else:
                data["brief"] = self.brief

        for gate_name in [
            "brief_validation", "lint_validation", "structure_validation",
            "seo_conversion_validation", "dei_accessibility_validation",
            "output_envelope_validation"
        ]:
            gate = getattr(self, gate_name)
            if gate:
                data[gate_name] = gate.to_dict()

        for result_name in ["seo_audit", "lint_result", "dei_result"]:
            result = getattr(self, result_name)
            if result:
                data[result_name] = result.to_dict()

        if self.output_envelope:
            data["output_envelope"] = self.output_envelope

        return data

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentDraft":
        """Create from dictionary."""
        # Extract nested objects
        outline = None
        if "outline" in data and data["outline"]:
            from content_writer_skill.models.outline import ContentOutline
            outline = ContentOutline.from_dict(data["outline"])

        brief = None
        if "brief" in data and data["brief"]:
            from content_writer_skill.models.brief import ContentBrief
            brief = ContentBrief.from_dict(data["brief"])

        gates = {}
        for gate_name in [
            "brief_validation", "lint_validation", "structure_validation",
            "seo_conversion_validation", "dei_accessibility_validation",
            "output_envelope_validation"
        ]:
            if gate_name in data and data[gate_name]:
                gates[gate_name] = ValidationGateResult.from_dict(data[gate_name])

        seo_audit = None
        if "seo_audit" in data and data["seo_audit"]:
            seo_audit = SEOAudit.from_dict(data["seo_audit"])

        lint_result = None
        if "lint_result" in data and data["lint_result"]:
            lint_result = LintResult.from_dict(data["lint_result"])

        dei_result = None
        if "dei_result" in data and data["dei_result"]:
            dei_result = DEIResult.from_dict(data["dei_result"])

        return cls(
            content=data.get("content", ""),
            outline=outline,
            brief=brief,
            word_count=data.get("word_count", 0),
            sentence_count=data.get("sentence_count", 0),
            reading_time_minutes=data.get("reading_time_minutes", 0.0),
            draft_number=data.get("draft_number", 1),
            template_used=data.get("template_used"),
            source_file=data.get("source_file"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            metadata=data.get("metadata", {}),
            brief_validation=gates.get("brief_validation"),
            lint_validation=gates.get("lint_validation"),
            structure_validation=gates.get("structure_validation"),
            seo_conversion_validation=gates.get("seo_conversion_validation"),
            dei_accessibility_validation=gates.get("dei_accessibility_validation"),
            output_envelope_validation=gates.get("output_envelope_validation"),
            seo_audit=seo_audit,
            lint_result=lint_result,
            dei_result=dei_result,
            output_envelope=data.get("output_envelope"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "ContentDraft":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))