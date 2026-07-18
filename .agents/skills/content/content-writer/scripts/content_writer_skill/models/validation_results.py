"""
Validation Result Models
========================
Data structures for validation gate results, SEO audit, lint results, and DEI results.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models.enums import GateStatus, LintSeverity


@dataclass
class ValidationGateResult:
    """Result of a single validation gate check."""
    gate: int  # 1-6
    gate_name: str
    passed: bool
    status: GateStatus = GateStatus.PASSED
    issues: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValidationGateResult":
        return cls(**data)

    @classmethod
    def create_passed(cls, gate: int, gate_name: str, metrics: Dict[str, Any] = None,
                      execution_time_ms: int = 0) -> "ValidationGateResult":
        """Create a passed gate result."""
        return cls(
            gate=gate,
            gate_name=gate_name,
            passed=True,
            status=GateStatus.PASSED,
            issues=[],
            metrics=metrics or {},
            execution_time_ms=execution_time_ms,
        )

    @classmethod
    def create_failed(cls, gate: int, gate_name: str, issues: List[Dict[str, Any]],
                      metrics: Dict[str, Any] = None, execution_time_ms: int = 0) -> "ValidationGateResult":
        """Create a failed gate result."""
        return cls(
            gate=gate,
            gate_name=gate_name,
            passed=False,
            status=GateStatus.FAILED,
            issues=issues,
            metrics=metrics or {},
            execution_time_ms=execution_time_ms,
        )

    def add_issue(self, code: str, message: str, severity: str = "error",
                  field: str = "", line: int = 0, column: int = 0,
                  suggestion: str = "", auto_fixable: bool = False) -> None:
        """Add an issue to this gate result."""
        self.issues.append({
            "code": code,
            "message": message,
            "severity": severity,
            "field": field,
            "line": line,
            "column": column,
            "suggestion": suggestion,
            "auto_fixable": auto_fixable,
        })
        self.passed = False


@dataclass
class SEOAudit:
    """SEO audit results for the draft."""
    score: int = 0  # 0-100
    primary_keyword: str = ""
    primary_keyword_count: int = 0
    primary_keyword_density: float = 0.0
    secondary_keywords_found: Dict[str, int] = field(default_factory=dict)
    secondary_keyword_density: Dict[str, float] = field(default_factory=dict)
    meta_title: str = ""
    meta_description: str = ""
    h1_present: bool = False
    h1_matches_title: bool = False
    heading_structure_valid: bool = False
    issues: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    eeat_signals: Dict[str, Any] = field(default_factory=dict)
    status: GateStatus = GateStatus.PASSED

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SEOAudit":
        if "status" in data and isinstance(data["status"], str):
            data["status"] = GateStatus(data["status"])
        return cls(**data)

    def add_issue(self, code: str, message: str, severity: str = "warning",
                  suggestion: str = "") -> None:
        """Add an SEO issue."""
        self.issues.append({
            "code": code,
            "message": message,
            "severity": severity,
            "suggestion": suggestion,
        })
        if severity in ("error", "alert"):
            self.status = GateStatus.FAILED


@dataclass
class LintIssue:
    """Individual lint issue."""
    rule_id: str
    message: str
    severity: LintSeverity = LintSeverity.WARNING
    line: int = 0
    column: int = 0
    suggestion: str = ""
    auto_fixable: bool = False
    context: str = ""  # Surrounding text for context

    def __post_init__(self):
        if isinstance(self.severity, str):
            self.severity = LintSeverity(self.severity)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LintIssue":
        if "severity" in data and isinstance(data["severity"], str):
            data["severity"] = LintSeverity(data["severity"])
        return cls(**data)


@dataclass
class LintResult:
    """Complete lint validation result."""
    passed: bool = True
    status: GateStatus = GateStatus.PASSED
    issues: List[LintIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "status": self.status.value if isinstance(self.status, GateStatus) else self.status,
            "issues": [issue.to_dict() for issue in self.issues],
            "metrics": self.metrics,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LintResult":
        issues = [LintIssue.from_dict(i) for i in data.get("issues", [])]
        status = data.get("status", GateStatus.PASSED)
        if isinstance(status, str):
            status = GateStatus(status)
        return cls(
            passed=data.get("passed", True),
            status=status,
            issues=issues,
            metrics=data.get("metrics", {}),
        )

    def add_issue(self, issue: LintIssue) -> None:
        """Add an issue and update passed status."""
        self.issues.append(issue)
        if issue.severity == LintSeverity.ALERT:
            self.passed = False
            self.status = GateStatus.FAILED

    def get_issues_by_severity(self, severity: LintSeverity) -> List[LintIssue]:
        """Get all issues of a specific severity."""
        return [i for i in self.issues if i.severity == severity]

    def get_alert_count(self) -> int:
        """Count of alert-level issues."""
        return len(self.get_issues_by_severity(LintSeverity.ALERT))

    def get_warning_count(self) -> int:
        """Count of warning-level issues."""
        return len(self.get_issues_by_severity(LintSeverity.WARNING))

    def get_info_count(self) -> int:
        """Count of info-level issues."""
        return len([i for i in self.issues if i.severity.value == "info"])


@dataclass
class DEIFinding:
    """Individual DEI/Accessibility finding."""
    category: str  # "bias", "accessibility", "inclusive_language", "readability"
    rule_id: str
    message: str
    severity: LintSeverity = LintSeverity.WARNING
    location: str = ""  # e.g., "section 2, paragraph 3"
    suggestion: str = ""
    auto_fixable: bool = False

    def __post_init__(self):
        if isinstance(self.severity, str):
            self.severity = LintSeverity(self.severity)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DEIFinding":
        if "severity" in data and isinstance(data["severity"], str):
            data["severity"] = LintSeverity(data["severity"])
        return cls(**data)


@dataclass
class DEIResult:
    """Complete DEI/Accessibility validation result."""
    passed: bool = True
    status: GateStatus = GateStatus.PASSED
    findings: List[DEIFinding] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "status": self.status.value if isinstance(self.status, GateStatus) else self.status,
            "findings": [f.to_dict() for f in self.findings],
            "metrics": self.metrics,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DEIResult":
        findings = [DEIFinding.from_dict(f) for f in data.get("findings", [])]
        status = data.get("status", GateStatus.PASSED)
        if isinstance(status, str):
            status = GateStatus(status)
        return cls(
            passed=data.get("passed", True),
            status=status,
            findings=findings,
            metrics=data.get("metrics", {}),
        )

    def add_finding(self, finding: DEIFinding) -> None:
        """Add a finding and update passed status."""
        self.findings.append(finding)
        if finding.severity == LintSeverity.ALERT:
            self.passed = False
            self.status = GateStatus.FAILED

    def get_findings_by_category(self, category: str) -> List[DEIFinding]:
        """Get all findings of a specific category."""
        return [f for f in self.findings if f.category == category]

    def get_alert_count(self) -> int:
        """Count of alert-level findings."""
        return len([f for f in self.findings if f.severity == LintSeverity.ALERT])

    def get_warning_count(self) -> int:
        """Count of warning-level findings."""
        return len([f for f in self.findings if f.severity == LintSeverity.WARNING])

    def get_info_count(self) -> int:
        """Count of info-level findings."""
        return len([f for f in self.findings if f.severity.value == "info"])


# Backward-compatibility alias
ValidationResult = ValidationGateResult


@dataclass
class OutputEnvelopeData:
    """Data payload for output envelope."""
    content: str = ""
    word_count: int = 0
    reading_time_minutes: float = 0.0
    brief: Optional[Dict[str, Any]] = None
    outline: Optional[Dict[str, Any]] = None
    seo_audit: Optional[Dict[str, Any]] = None
    lint_summary: Optional[Dict[str, Any]] = None
    dei_summary: Optional[Dict[str, Any]] = None


@dataclass
class OutputEnvelope:
    """Standardized output envelope for agent/CLI consumption."""
    format_version: str = "1.0"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    data: OutputEnvelopeData = field(default_factory=OutputEnvelopeData)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: GateStatus = GateStatus.PASSED

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value if isinstance(self.status, GateStatus) else self.status
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OutputEnvelope":
        if "status" in data and isinstance(data["status"], str):
            data["status"] = GateStatus(data["status"])
        if "data" in data and isinstance(data["data"], dict):
            data["data"] = OutputEnvelopeData(**data["data"])
        return cls(**data)

    @classmethod
    def create_cli_output(cls, draft: "ContentDraft", execution_time_ms: int = 0,
                          brief_id: str = "unknown") -> "OutputEnvelope":
        """Create CLI-format output envelope."""
        from content_writer_skill.models import ContentDraft
        data = OutputEnvelopeData(
            content=draft.content,
            word_count=draft.word_count,
            reading_time_minutes=round(draft.reading_time_minutes, 1),
        )
        if draft.brief:
            data.brief = draft.brief.to_dict()
        if draft.outline:
            data.outline = draft.outline.to_dict()
        envelope = cls(
            format_version="1.0",
            timestamp=datetime.utcnow().isoformat() + "Z",
            data=data,
            metadata={
                "skill": "content-writer",
                "command": "generate",
                "pipeline_stage": "complete",
                "brief_id": brief_id,
                "execution_time_ms": execution_time_ms,
                "pipeline_version": "2.1",
            },
            status=GateStatus.PASSED,
        )
        return envelope

    @classmethod
    def create_agent_output(cls, draft: "ContentDraft", execution_time_ms: int = 0,
                            brief_id: str = "unknown") -> "OutputEnvelope":
        """Create Agent JSON envelope output."""
        from content_writer_skill.models import ContentDraft
        data = OutputEnvelopeData(
            content=draft.content,
            word_count=draft.word_count,
            reading_time_minutes=round(draft.reading_time_minutes, 1),
        )
        if draft.brief:
            data.brief = draft.brief.to_dict()
        if draft.outline:
            data.outline = draft.outline.to_dict()
        if draft.seo_audit:
            data.seo_audit = draft.seo_audit.to_dict()
        if draft.lint_result:
            data.lint_summary = {
                "passed": draft.lint_result.passed,
                "alerts": draft.lint_result.get_alert_count(),
                "warnings": draft.lint_result.get_warning_count(),
                "info": draft.lint_result.get_info_count(),
                "metrics": draft.lint_result.metrics,
            }
        if draft.dei_result:
            data.dei_summary = {
                "passed": draft.dei_result.passed,
                "alerts": draft.dei_result.get_alert_count(),
                "warnings": draft.dei_result.get_warning_count(),
                "info": draft.dei_result.get_info_count(),
                "inclusive_language_score": draft.dei_result.inclusive_language_score,
                "accessibility_score": draft.dei_result.accessibility_score,
                "bias_score": draft.dei_result.bias_score,
            }
        envelope = cls(
            format_version="1.0",
            timestamp=datetime.utcnow().isoformat() + "Z",
            data=data,
            metadata={
                "skill": "content-writer",
                "command": "generate",
                "pipeline_stage": "complete",
                "brief_id": brief_id,
                "execution_time_ms": execution_time_ms,
                "pipeline_version": "2.1",
            },
            status=GateStatus.PASSED,
        )
        return envelope
