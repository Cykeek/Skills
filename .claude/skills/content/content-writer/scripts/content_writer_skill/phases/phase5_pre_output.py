"""
Phase 5: Pre-Output Scan
========================
Final output envelope validation and agent-mode JSON envelope generation.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from content_writer_skill.models import (
    ContentDraft, ContentBrief, ContentOutline,
    ValidationGateResult, OutputFormat, GateStatus
)
from content_writer_skill.output_manager import OutputManager


@dataclass
class Phase5Result:
    """Result of Phase 5: Pre-Output Scan."""
    draft: ContentDraft
    output_envelope: Dict[str, Any]
    validation: ValidationGateResult
    cli_output: str
    agent_output: str


class PreOutputPhase:
    """
    Phase 5: Pre-Output Scan

    - Validates output envelope (Gate 6)
    - Generates CLI human-readable output
    - Generates Agent JSON envelope output
    - Final quality check

    Inputs: ContentDraft with all validation results from Phase 4
    Outputs: Final validated output in both CLI and Agent formats
    """

    def __init__(self, output_format: OutputFormat = OutputFormat.TEXT,
                 include_metadata: bool = True):
        """
        Initialize Pre-Output Phase.

        Args:
            output_format: Primary output format
            include_metadata: Include detailed metadata in output
        """
        self.output_manager = OutputManager()
        self.output_format = output_format
        self.include_metadata = include_metadata

    def run(self, draft: ContentDraft) -> Phase5Result:
        """
        Execute Phase 5: Final validation and output generation.

        Args:
            draft: Fully validated ContentDraft from Phase 4

        Returns:
            Phase5Result with output envelope and both output formats
        """
        # Build output envelope first
        envelope = self._build_output_envelope(draft)
        draft.output_envelope = envelope

        # Gate 6: Output envelope validation
        validation = self._validate_output_envelope(draft)
        draft.output_envelope_validation = validation

        # Generate outputs
        cli_output = self._generate_cli_output(draft, envelope)
        agent_output = self._generate_agent_output(envelope)

        return Phase5Result(
            draft=draft,
            output_envelope=envelope,
            validation=validation,
            cli_output=cli_output,
            agent_output=agent_output,
        )

    def _validate_output_envelope(self, draft: ContentDraft) -> ValidationGateResult:
        """Validate output envelope completeness (Gate 6)."""
        issues = []
        metrics = {}

        # Check all previous gates passed
        failed_gates = draft.get_failed_gates()
        if failed_gates:
            issues.append({
                "code": "PREVIOUS_GATES_FAILED",
                "message": f"Previous validation gates failed: {failed_gates}",
                "severity": "error",
                "suggestion": "Fix all failed gates before output",
            })

        # Check content exists
        if not draft.content or not draft.content.strip():
            issues.append({
                "code": "EMPTY_CONTENT",
                "message": "Draft content is empty",
                "severity": "error",
            })

        # Check envelope has required fields
        required_envelope_fields = ["timestamp", "format_version", "data"]
        for field in required_envelope_fields:
            if field not in draft.output_envelope:
                issues.append({
                    "code": "MISSING_ENVELOPE_FIELD",
                    "message": f"Output envelope missing required field: {field}",
                    "severity": "error",
                })

        # Check data payload has content
        if "data" in draft.output_envelope:
            data = draft.output_envelope["data"]
            if "content" not in data or not data["content"]:
                issues.append({
                    "code": "EMPTY_ENVELOPE_CONTENT",
                    "message": "Output envelope data.content is empty",
                    "severity": "error",
                })

        metrics["failed_gates"] = failed_gates
        metrics["content_length"] = len(draft.content)
        metrics["word_count"] = draft.word_count

        passed = len([i for i in issues if i["severity"] == "error"]) == 0

        return ValidationGateResult(
            gate=6,
            gate_name="output-envelope-validation",
            passed=passed,
            status=GateStatus.PASSED if passed else GateStatus.FAILED,
            issues=issues,
            metrics=metrics,
        )

    def _build_output_envelope(self, draft: ContentDraft) -> Dict[str, Any]:
        """Build the standard agent output envelope."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "format_version": "2.1",
            "data": {
                "content": draft.content,
                "word_count": draft.word_count,
                "reading_time_minutes": draft.reading_time_minutes,
                "brief": draft.brief.to_dict() if draft.brief else None,
                "outline": draft.outline.to_dict() if draft.outline else None,
                "validation_summary": {
                    "all_gates_passed": draft.all_gates_passed(),
                    "failed_gates": draft.get_failed_gates(),
                    "total_issues": len(draft.get_all_issues()),
                },
                "seo_audit": draft.seo_audit.to_dict() if draft.seo_audit else None,
                "lint_summary": {
                    "passed": draft.lint_result.passed if draft.lint_result else False,
                    "alerts": draft.lint_result.get_alert_count() if draft.lint_result else 0,
                    "warnings": draft.lint_result.get_warning_count() if draft.lint_result else 0,
                } if draft.lint_result else None,
                "dei_summary": {
                    "passed": draft.dei_result.passed if draft.dei_result else False,
                    "alerts": draft.dei_result.get_alert_count() if draft.dei_result else 0,
                    "warnings": draft.dei_result.get_warning_count() if draft.dei_result else 0,
                } if draft.dei_result else None,
            },
            "metadata": {
                "skill": "content-writer",
                "command": "generate",
                "pipeline_stage": "complete",
                "brief_id": draft.brief.source_file if draft.brief else "unknown",
                "execution_time_ms": 0,  # Would be filled by pipeline
            },
        }

    def _generate_cli_output(self, draft: ContentDraft, envelope: Dict[str, Any]) -> str:
        """Generate human-readable CLI output."""
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append("CONTENT GENERATION COMPLETE")
        lines.append("=" * 60)
        lines.append("")

        # Content
        lines.append("CONTENT:")
        lines.append("-" * 60)
        lines.append(draft.content)
        lines.append("")

        # Summary
        lines.append("SUMMARY:")
        lines.append("-" * 60)
        lines.append(f"  Word Count: {draft.word_count}")
        lines.append(f"  Reading Time: {draft.reading_time_minutes:.1f} minutes")
        lines.append(f"  Sections: {draft.outline.estimated_sections if draft.outline else 0}")

        # Validation status
        lines.append("")
        lines.append("VALIDATION STATUS:")
        lines.append("-" * 60)

        gates = [
            (1, "Brief Validation", draft.brief_validation),
            (2, "Lint Validation", draft.lint_validation),
            (3, "Structure Validation", draft.structure_validation),
            (4, "SEO/Conversion", draft.seo_conversion_validation),
            (5, "DEI/Accessibility", draft.dei_accessibility_validation),
            (6, "Output Envelope", draft.output_envelope_validation),
        ]

        all_passed = True
        for num, name, gate in gates:
            if gate:
                status = "✓ PASSED" if gate.passed else "✗ FAILED"
                if not gate.passed:
                    all_passed = False
                lines.append(f"  Gate {num} ({name}): {status}")
                if gate.issues:
                    for issue in gate.issues[:2]:  # Show first 2 issues
                        lines.append(f"    - {issue['message']}")
                    if len(gate.issues) > 2:
                        lines.append(f"    ... and {len(gate.issues) - 2} more")
            else:
                lines.append(f"  Gate {num} ({name}): NOT RUN")

        lines.append("")
        lines.append(f"OVERALL: {'✓ ALL GATES PASSED' if all_passed else '✗ SOME GATES FAILED'}")
        lines.append("=" * 60)

        return "\n".join(lines)

    def _generate_agent_output(self, envelope: Dict[str, Any]) -> str:
        """Generate JSON envelope for agent mode."""
        return json.dumps(envelope, indent=2, ensure_ascii=False)


def run_pre_output(draft: ContentDraft,
                   output_format: OutputFormat = OutputFormat.TEXT,
                   include_metadata: bool = True) -> Phase5Result:
    """Convenience function to run Phase 5."""
    phase = PreOutputPhase(output_format=output_format, include_metadata=include_metadata)
    return phase.run(draft)