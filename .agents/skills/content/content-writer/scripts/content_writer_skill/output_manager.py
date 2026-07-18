"""
Output Manager
==============
Handles dual output modes: CLI (human-readable) and Agent (JSON envelope).
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import textwrap

from content_writer_skill.models import ContentDraft, OutputFormat, ValidationGateResult
from content_writer_skill.models.validation_results import SEOAudit, DEIResult, LintResult


@dataclass
class OutputConfig:
    """Configuration for output generation."""
    format: OutputFormat = OutputFormat.TEXT
    include_metadata: bool = True
    include_validation: bool = True
    include_seo: bool = True
    include_dei: bool = True
    include_lint: bool = True
    color_output: bool = False
    max_content_preview: int = 0  # 0 = full content


class OutputManager:
    """
    Manages output generation for both CLI and Agent modes.

    CLI Mode (--output-format text):
    - Human-readable formatted output
    - Color-coded validation status
    - Summary sections with key metrics

    Agent Mode (--output-format json):
    - Standardized JSON envelope with:
      - timestamp: ISO 8601 UTC
      - format_version: "2.1"
      - data: {content, word_count, brief, outline, validation_summary, seo_audit, lint_summary, dei_summary}
      - metadata: {skill, command, pipeline_stage, brief_id, execution_time_ms}
    """

    FORMAT_VERSION = "2.1"
    SKILL_NAME = "content-writer"

    def __init__(self, config: Optional[OutputConfig] = None):
        self.config = config or OutputConfig()

    def generate_output(self, draft: ContentDraft,
                        execution_time_ms: int = 0,
                        brief_id: str = "unknown") -> str:
        """
        Generate output based on configured format.

        Args:
            draft: Completed content draft
            execution_time_ms: Total pipeline execution time
            brief_id: Identifier for the brief

        Returns:
            Formatted output string
        """
        if self.config.format == OutputFormat.JSON:
            return self._generate_agent_output(draft, execution_time_ms, brief_id)
        else:
            return self._generate_cli_output(draft, execution_time_ms, brief_id)

    def _generate_agent_output(self, draft: ContentDraft,
                                execution_time_ms: int,
                                brief_id: str) -> str:
        """Generate JSON envelope for agent consumption."""
        envelope = self._build_envelope(draft, execution_time_ms, brief_id)
        return json.dumps(envelope, indent=2, ensure_ascii=False)

    def _build_envelope(self, draft: ContentDraft,
                        execution_time_ms: int,
                        brief_id: str) -> Dict[str, Any]:
        """Build the standard agent output envelope."""
        envelope = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "format_version": self.FORMAT_VERSION,
            "data": {
                "content": draft.content,
                "word_count": draft.word_count,
                "reading_time_minutes": round(draft.reading_time_minutes, 1),
            },
            "metadata": {
                "skill": self.SKILL_NAME,
                "command": "generate",
                "pipeline_stage": "complete",
                "brief_id": brief_id,
                "execution_time_ms": execution_time_ms,
            },
        }

        # Add optional sections based on config
        if self.config.include_metadata and draft.brief:
            envelope["data"]["brief"] = draft.brief.to_dict()

        if self.config.include_metadata and draft.outline:
            envelope["data"]["outline"] = draft.outline.to_dict()

        if self.config.include_validation:
            envelope["data"]["validation_summary"] = self._build_validation_summary(draft)

        if self.config.include_seo and draft.seo_audit:
            envelope["data"]["seo_audit"] = draft.seo_audit.to_dict()

        if self.config.include_lint and draft.lint_result:
            envelope["data"]["lint_summary"] = self._build_lint_summary(draft.lint_result)

        if self.config.include_dei and draft.dei_result:
            envelope["data"]["dei_summary"] = self._build_dei_summary(draft.dei_result)

        return envelope

    def _build_validation_summary(self, draft: ContentDraft) -> Dict[str, Any]:
        """Build validation summary from all gates."""
        gates = [
            (1, "Brief Validation", draft.brief_validation),
            (2, "Lint Validation", draft.lint_validation),
            (3, "Structure Validation", draft.structure_validation),
            (4, "SEO/Conversion", draft.seo_conversion_validation),
            (5, "DEI/Accessibility", draft.dei_accessibility_validation),
            (6, "Output Envelope", draft.output_envelope_validation),
        ]

        gate_results = []
        all_passed = True

        for num, name, gate in gates:
            if gate:
                gate_passed = gate.passed
                if not gate_passed:
                    all_passed = False
                gate_results.append({
                    "gate": num,
                    "name": name,
                    "passed": gate_passed,
                    "issues_count": len(gate.issues),
                    "errors": sum(1 for i in gate.issues if i.get("severity") == "error"),
                    "warnings": sum(1 for i in gate.issues if i.get("severity") == "warning"),
                    "info": sum(1 for i in gate.issues if i.get("severity") == "info"),
                })
            else:
                gate_results.append({
                    "gate": num,
                    "name": name,
                    "passed": False,
                    "issues_count": 0,
                    "errors": 0,
                    "warnings": 0,
                    "info": 0,
                    "not_run": True,
                })
                all_passed = False

        return {
            "all_gates_passed": all_passed,
            "failed_gates": [g["gate"] for g in gate_results if not g["passed"]],
            "gate_results": gate_results,
            "total_issues": sum(g["issues_count"] for g in gate_results),
        }

    def _build_lint_summary(self, lint: LintResult) -> Dict[str, Any]:
        """Build lint summary for envelope."""
        return {
            "passed": lint.passed,
            "alerts": lint.get_alert_count(),
            "warnings": lint.get_warning_count(),
            "info": lint.get_info_count(),
            "metrics": lint.metrics,
        }

    def _build_dei_summary(self, dei: DEIResult) -> Dict[str, Any]:
        """Build DEI summary for envelope."""
        return {
            "passed": dei.passed,
            "alerts": dei.get_alert_count(),
            "warnings": dei.get_warning_count(),
            "info": dei.get_info_count(),
            "inclusive_language_score": dei.inclusive_language_score,
            "accessibility_score": dei.accessibility_score,
            "bias_score": dei.bias_score,
        }

    def _generate_cli_output(self, draft: ContentDraft,
                              execution_time_ms: int,
                              brief_id: str) -> str:
        """Generate human-readable CLI output."""
        lines = []

        # Header
        lines.append(self._colorize("=" * 60, "cyan"))
        lines.append(self._colorize("CONTENT GENERATION COMPLETE", "bold"))
        lines.append(self._colorize("=" * 60, "cyan"))
        lines.append("")

        # Content
        lines.append(self._colorize("CONTENT:", "bold"))
        lines.append(self._colorize("-" * 60, "dim"))
        content = draft.content
        if self.config.max_content_preview > 0 and len(content) > self.config.max_content_preview:
            content = content[:self.config.max_content_preview] + "... [truncated]"
        lines.append(content)
        lines.append("")

        # Summary
        lines.append(self._colorize("SUMMARY:", "bold"))
        lines.append(self._colorize("-" * 60, "dim"))
        lines.append(f"  Word Count:       {draft.word_count:,}")
        lines.append(f"  Reading Time:     {draft.reading_time_minutes:.1f} minutes")
        lines.append(f"  Sections:         {draft.outline.estimated_sections if draft.outline else 0}")
        lines.append(f"  Execution Time:   {execution_time_ms}ms")
        lines.append("")

        # Validation Status
        if self.config.include_validation:
            lines.append(self._colorize("VALIDATION STATUS:", "bold"))
            lines.append(self._colorize("-" * 60, "dim"))

            gates = [
                (1, "Brief Validation", draft.brief_validation),
                (2, "Lint Validation", draft.lint_validation),
                (4, "SEO/Conversion", draft.seo_conversion_validation),
                (5, "DEI/Accessibility", draft.dei_accessibility_validation),
                (6, "Output Envelope", draft.output_envelope_validation),
            ]

            all_passed = True
            for num, name, gate in gates:
                if gate:
                    status = self._colorize("✓ PASSED", "green") if gate.passed else self._colorize("✗ FAILED", "red")
                    if not gate.passed:
                        all_passed = False
                    lines.append(f"  Gate {num} ({name}): {status}")
                    if gate.issues:
                        for issue in gate.issues[:2]:
                            severity = issue.get("severity", "info")
                            color = "red" if severity == "error" else "yellow" if severity == "warning" else "blue"
                            lines.append(f"    {self._colorize('→', color)} {issue['message']}")
                        if len(gate.issues) > 2:
                            lines.append(f"    ... and {len(gate.issues) - 2} more issues")
                else:
                    lines.append(f"  Gate {num} ({name}): {self._colorize('NOT RUN', 'yellow')}")
                    all_passed = False

            lines.append("")
            overall = self._colorize("✓ ALL GATES PASSED", "green") if all_passed else self._colorize("✗ SOME GATES FAILED", "red")
            lines.append(f"OVERALL: {overall}")
            lines.append("")

        # SEO Summary
        if self.config.include_seo and draft.seo_audit:
            lines.append(self._colorize("SEO AUDIT:", "bold"))
            lines.append(self._colorize("-" * 60, "dim"))
            audit = draft.seo_audit
            lines.append(f"  Overall Score:    {audit.overall_score}/100")
            lines.append(f"  Keyword Score:    {audit.keyword_score}/100")
            lines.append(f"  Structure Score:  {audit.structure_score}/100")
            lines.append(f"  Readability:      {audit.flesch_reading_ease} (Grade {audit.flesch_kincaid_grade})")
            lines.append(f"  E-E-A-T Score:    {audit.eeat_score}/100")
            if audit.primary_keyword:
                lines.append(f"  Primary Keyword:  '{audit.primary_keyword}' ({audit.primary_keyword_density}% density)")
            lines.append("")

        # DEI Summary
        if self.config.include_dei and draft.dei_result:
            lines.append(self._colorize("DEI / ACCESSIBILITY:", "bold"))
            lines.append(self._colorize("-" * 60, "dim"))
            dei = draft.dei_result
            lines.append(f"  Inclusive Language: {dei.inclusive_language_score:.0f}/100")
            lines.append(f"  Accessibility:      {dei.accessibility_score:.0f}/100")
            lines.append(f"  Bias Score:         {dei.bias_score:.0f}/100")
            lines.append(f"  Alerts:             {dei.get_alert_count()}")
            lines.append(f"  Warnings:           {dei.get_warning_count()}")
            lines.append("")

        # Footer
        lines.append(self._colorize("=" * 60, "cyan"))
        lines.append(f"Brief ID: {brief_id} | Format: v{self.FORMAT_VERSION} | Skill: {self.SKILL_NAME}")
        lines.append(self._colorize("=" * 60, "cyan"))

        return "\n".join(lines)

    def _colorize(self, text: str, color: str) -> str:
        """Apply ANSI color codes if enabled."""
        if not self.config.color_output:
            return text

        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "cyan": "\033[96m",
            "bold": "\033[1m",
            "dim": "\033[2m",
            "reset": "\033[0m",
        }
        return f"{colors.get(color, '')}{text}{colors['reset']}"

    def save_to_file(self, output: str, filepath: str) -> None:
        """Save output to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)

    def create_summary_dict(self, draft: ContentDraft,
                            execution_time_ms: int,
                            brief_id: str) -> Dict[str, Any]:
        """Create a summary dictionary for programmatic access."""
        return {
            "brief_id": brief_id,
            "word_count": draft.word_count,
            "reading_time_minutes": round(draft.reading_time_minutes, 1),
            "sections": draft.outline.estimated_sections if draft.outline else 0,
            "execution_time_ms": execution_time_ms,
            "all_gates_passed": draft.all_gates_passed(),
            "failed_gates": draft.get_failed_gates(),
            "seo_score": draft.seo_audit.overall_score if draft.seo_audit else None,
            "dei_passed": draft.dei_result.passed if draft.dei_result else None,
            "lint_passed": draft.lint_result.passed if draft.lint_result else None,
        }


def create_cli_output(draft: ContentDraft,
                      execution_time_ms: int = 0,
                      brief_id: str = "unknown",
                      color: bool = False) -> str:
    """Convenience function to generate CLI output."""
    config = OutputConfig(format=OutputFormat.TEXT, color_output=color)
    manager = OutputManager(config)
    return manager.generate_output(draft, execution_time_ms, brief_id)


def create_agent_output(draft: ContentDraft,
                        execution_time_ms: int = 0,
                        brief_id: str = "unknown") -> str:
    """Convenience function to generate agent JSON output."""
    config = OutputConfig(format=OutputFormat.JSON)
    manager = OutputManager(config)
    return manager.generate_output(draft, execution_time_ms, brief_id)