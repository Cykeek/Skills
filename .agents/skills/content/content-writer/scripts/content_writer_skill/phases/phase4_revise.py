"""
Phase 4: Revise
===============
Runs all validation gates (lint, structure, SEO/conversion, DEI/accessibility).
"""

from dataclasses import dataclass
from typing import Optional, Dict, List, Any
import re

from content_writer_skill.models import (
    ContentDraft, ContentBrief, ContentOutline,
    ValidationGateResult, SEOAudit, LintResult, DEIResult,
    LintSeverity, GateStatus
)
from content_writer_skill.lint import LintEngine
from content_writer_skill.validation import SEOValidator, DEIValidator


@dataclass
class Phase4Result:
    """Result of Phase 4: Revise."""
    draft: ContentDraft
    lint_result: LintResult
    structure_validation: ValidationGateResult
    seo_conversion_validation: ValidationGateResult
    dei_accessibility_validation: ValidationGateResult


class RevisePhase:
    """
    Phase 4: Revise

    Runs all validation gates (2-5):
    - Gate 2: Lint validation (voice, style, grammar)
    - Gate 3: Structure validation (outline adherence)
    - Gate 4: SEO/Conversion validation
    - Gate 5: DEI/Accessibility validation

    Inputs: ContentDraft from Phase 3
    Outputs: ContentDraft with all validation results populated
    """

    def __init__(self, lint_config: Optional[Dict] = None, strict_seo: bool = False,
                 strict_dei: bool = False, skip_gates: Optional[List[str]] = None,
                 strict_mode: bool = True):
        """
        Initialize Revise Phase.

        Args:
            lint_config: Optional custom lint rules
            strict_seo: If True, fail on SEO warnings
            strict_dei: If True, fail on DEI warnings
            skip_gates: List of gate names to skip (e.g., ["lint", "dei"])
            strict_mode: If True, ALERT severity fails gates; if False, only ERROR fails
        """
        self.lint_engine = LintEngine(lint_config, strict=strict_mode)
        self.seo_validator = SEOValidator(strict=strict_seo)
        self.dei_validator = DEIValidator(strict=strict_dei)
        self.skip_gates = skip_gates or []
        self.strict_mode = strict_mode

    def run(self, draft: ContentDraft) -> Phase4Result:
        """
        Execute Phase 4: Run all validation gates.

        Args:
            draft: ContentDraft from Phase 3

        Returns:
            Phase4Result with populated validation results
        """
        # Gate 2: Lint validation
        if "lint" not in self.skip_gates:
            lint_result = self.lint_engine.lint(draft.content, draft.brief, strict=self.strict_mode)
            draft.lint_result = lint_result
            draft.lint_validation = self._lint_to_gate(lint_result)
        else:
            draft.lint_result = LintResult()
            draft.lint_validation = ValidationGateResult(gate=2, gate_name="lint-validation", passed=True, status=GateStatus.PASSED, issues=[], metrics={})

        # Gate 3: Structure validation
        if "structure" not in self.skip_gates:
            structure_validation = self._validate_structure(draft)
            draft.structure_validation = structure_validation
        else:
            draft.structure_validation = ValidationGateResult(gate=3, gate_name="structure-validation", passed=True, status=GateStatus.PASSED, issues=[], metrics={})

        # Gate 4: SEO/Conversion validation
        if "seo" not in self.skip_gates:
            seo_audit = self.seo_validator.audit(draft.content, draft.brief, draft.outline)
            seo_validation = self._seo_to_gate(seo_audit)
            draft.seo_audit = seo_audit
            draft.seo_conversion_validation = seo_validation
        else:
            draft.seo_audit = SEOAudit()
            draft.seo_conversion_validation = ValidationGateResult(gate=4, gate_name="seo-conversion-validation", passed=True, status=GateStatus.PASSED, issues=[], metrics={})

        # Gate 5: DEI/Accessibility validation
        if "dei" not in self.skip_gates:
            dei_result = self.dei_validator.validate(draft.content, draft.brief)
            dei_validation = self._dei_to_gate(dei_result)
            draft.dei_result = dei_result
            draft.dei_accessibility_validation = dei_validation
        else:
            draft.dei_result = DEIResult()
            draft.dei_accessibility_validation = ValidationGateResult(gate=5, gate_name="dei-accessibility-validation", passed=True, status=GateStatus.PASSED, issues=[], metrics={})

        return Phase4Result(
            draft=draft,
            lint_result=draft.lint_result,
            structure_validation=draft.structure_validation,
            seo_conversion_validation=draft.seo_conversion_validation,
            dei_accessibility_validation=draft.dei_accessibility_validation,
        )

    def _lint_to_gate(self, lint_result: LintResult) -> ValidationGateResult:
        """Convert lint result to validation gate."""
        issues = []
        for issue in lint_result.issues:
            issues.append({
                "code": issue.rule_id,
                "message": issue.message,
                "severity": issue.severity.value,
                "line": issue.line,
                "column": issue.column,
                "suggestion": issue.suggestion,
                "auto_fixable": issue.auto_fixable,
                "context": issue.context,
            })

        metrics = {
            "total_issues": len(lint_result.issues),
            "alerts": lint_result.get_alert_count(),
            "warnings": lint_result.get_warning_count(),
            "voice_drift_score": lint_result.voice_drift_score,
            **lint_result.metrics,
        }

        return ValidationGateResult(
            gate=2,
            gate_name="lint-validation",
            passed=lint_result.passed,
            status=lint_result.status,
            issues=issues,
            metrics=metrics,
        )

    def _validate_structure(self, draft: ContentDraft) -> ValidationGateResult:
        """Validate draft structure matches outline."""
        issues = []
        metrics = {}

        if not draft.outline:
            return ValidationGateResult(
                gate=3,
                gate_name="structure-validation",
                passed=False,
                issues=[{"code": "NO_OUTLINE", "message": "No outline to validate against", "severity": "error"}],
            )

        # Check all sections present
        outline_headings = [s.heading for s in draft.outline.sections]
        content_headings = self._extract_headings(draft.content)

        missing = [h for h in outline_headings if h not in content_headings]
        extra = [h for h in content_headings if h not in outline_headings]

        if missing:
            issues.append({
                "code": "MISSING_SECTIONS",
                "message": f"Missing {len(missing)} planned sections: {', '.join(missing[:3])}",
                "severity": "error",
                "suggestion": "Write all planned sections from outline",
            })

        if extra:
            issues.append({
                "code": "EXTRA_SECTIONS",
                "message": f"Found {len(extra)} unplanned sections: {', '.join(extra[:3])}",
                "severity": "warning",
                "suggestion": "Remove or add to outline",
            })

        # Check heading hierarchy
        hierarchy_issues = self._check_heading_hierarchy(draft.content)
        issues.extend(hierarchy_issues)

        metrics["planned_sections"] = len(outline_headings)
        metrics["written_sections"] = len(content_headings)
        metrics["missing_sections"] = len(missing)
        metrics["extra_sections"] = len(extra)

        passed = len([i for i in issues if i["severity"] == "error"]) == 0

        return ValidationGateResult(
            gate=3,
            gate_name="structure-validation",
            passed=passed,
            status=GateStatus.PASSED if passed else GateStatus.FAILED,
            issues=issues,
            metrics=metrics,
        )

    def _seo_to_gate(self, seo_audit: SEOAudit) -> ValidationGateResult:
        """Convert SEO audit to validation gate."""
        issues = []
        for issue in seo_audit.issues:
            issues.append({
                "code": issue.get("code", "SEO_ISSUE"),
                "message": issue["message"],
                "severity": issue.get("severity", "warning"),
                "suggestion": issue.get("suggestion", ""),
            })

        metrics = {
            "overall_score": seo_audit.overall_score,
            "keyword_score": seo_audit.keyword_score,
            "structure_score": seo_audit.structure_score,
            "readability_score": seo_audit.readability_score,
            "metadata_score": seo_audit.metadata_score,
            "eeat_score": seo_audit.eeat_score,
            "primary_keyword_density": seo_audit.primary_keyword_density,
            "flesch_kincaid_grade": seo_audit.flesch_kincaid_grade,
            "flesch_reading_ease": seo_audit.flesch_reading_ease,
        }

        passed = seo_audit.overall_score >= 70

        return ValidationGateResult(
            gate=4,
            gate_name="seo-conversion-validation",
            passed=passed,
            status=GateStatus.PASSED if passed else GateStatus.FAILED,
            issues=issues,
            metrics=metrics,
        )

    def _dei_to_gate(self, dei_result: DEIResult) -> ValidationGateResult:
        """Convert DEI result to validation gate."""
        issues = []
        for finding in dei_result.findings:
            issues.append({
                "code": finding.rule_id,
                "message": finding.message,
                "severity": finding.severity.value,
                "suggestion": finding.suggestion,
                "auto_fixable": finding.auto_fixable,
            })

        metrics = {
            "inclusive_language_score": dei_result.inclusive_language_score,
            "accessibility_score": dei_result.accessibility_score,
            "bias_score": dei_result.bias_score,
            "total_findings": len(dei_result.findings),
            "alerts": dei_result.get_alert_count(),
            "warnings": dei_result.get_warning_count(),
        }

        passed = dei_result.passed

        return ValidationGateResult(
            gate=5,
            gate_name="dei-accessibility-validation",
            passed=passed,
            status=GateStatus.PASSED if passed else GateStatus.FAILED,
            issues=issues,
            metrics=metrics,
        )

    def _extract_headings(self, content: str) -> List[str]:
        """Extract markdown headings from content."""
        return [h.strip('# ').strip() for h in re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)]

    def _check_heading_hierarchy(self, content: str) -> List[Dict[str, Any]]:
        """Check for proper heading hierarchy (no skipped levels)."""
        issues = []
        headings = re.findall(r'^(#{1,3})\s+(.+)$', content, re.MULTILINE)

        prev_level = 0
        for i, (hashes, text) in enumerate(headings):
            level = len(hashes)
            if prev_level > 0 and level > prev_level + 1:
                issues.append({
                    "code": "HEADING_HIERARCHY_SKIP",
                    "message": f"Heading level jumps from H{prev_level} to H{level}: '{text}'",
                    "severity": "warning",
                    "line": i + 1,
                    "suggestion": "Use sequential heading levels (H1 → H2 → H3)",
                })
            prev_level = level

        return issues


def run_revise(draft: ContentDraft, lint_config: Optional[Dict] = None,
               strict_seo: bool = False, strict_dei: bool = False,
               skip_gates: Optional[List[str]] = None, strict_mode: bool = True) -> Phase4Result:
    """Convenience function to run Phase 4."""
    phase = RevisePhase(lint_config=lint_config, strict_seo=strict_seo, strict_dei=strict_dei, skip_gates=skip_gates, strict_mode=strict_mode)
    return phase.run(draft)