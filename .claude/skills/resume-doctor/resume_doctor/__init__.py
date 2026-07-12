"""
Resume Doctor — ATS-safe resume tailoring toolkit.

Public API:
    from resume_doctor import (
        analyze_job,
        build_profile,
        analyze_gaps,
        optimize_resume,
        run_all_gates,
        build_resume,
        run_ats_audit,
    )
"""
from .job_analyzer import (
    analyze_job,
    gather_company_intel,
    build_keyword_targets,
    JobAnalysis,
    CompanyIntel,
)

from .profile_builder import (
    parse_latex_resume,
    parse_linkedin_pdf,
    build_profile,
    CandidateProfile,
)

from .gap_analyzer import (
    analyze_gaps,
    analyze_general_ats_gaps,
    build_injection_map,
    GapReport,
    KeywordInjectionMap,
    Gap,
    Severity,
)

from .validation_gates import (
    validate_latex_format,
    validate_keyword_density,
    validate_parser_simulation,
    validate_unicode_extraction,
    validate_readability,
    validate_audience_comprehension,
    validate_metric_plausibility,
    validate_single_role,
    validate_summary_template,
    validate_portfolio_crossref,
    run_all_gates,
    GateResult,
    ValidationReport,
    PhaseGate,
)

from .optimizer import (
    inject_keywords,
    calibrate_density,
    upgrade_verbs,
    add_signal_tags,
    apply_nda_abstraction,
    reorder_sections,
    apply_audience_aware,
    auto_calibrate_density,
    optimize_resume,
)

from .latex_builder import (
    build_resume,
    BuildResult,
)

from .ats_audit import (
    run_ats_audit,
    ATSAuditResult,
)

from .signal_tagger import add_signal_tags

from .audience_translator import (
    apply_audience_aware,
    apply_all_audiences,
    validate_audience_comprehension,
)

from .metric_plausibility import (
    extract_metrics,
    validate_all_metrics,
    MetricClaim,
)

from .portfolio_crossref import (
    cross_reference,
    validate_portfolio_crossref,
    CrossRefResult,
)

__all__ = [
    # Job analysis
    "analyze_job",
    "gather_company_intel",
    "build_keyword_targets",
    "JobAnalysis",
    "CompanyIntel",

    # Profile
    "parse_latex_resume",
    "parse_linkedin_pdf",
    "build_profile",
    "CandidateProfile",

    # Gap analysis
    "analyze_gaps",
    "analyze_general_ats_gaps",
    "build_injection_map",
    "GapReport",
    "KeywordInjectionMap",
    "Gap",
    "Severity",

    # Validation gates
    "validate_latex_format",
    "validate_keyword_density",
    "validate_parser_simulation",
    "validate_unicode_extraction",
    "validate_readability",
    "validate_audience_comprehension",
    "validate_metric_plausibility",
    "validate_single_role",
    "validate_summary_template",
    "validate_portfolio_crossref",
    "run_all_gates",
    "GateResult",
    "ValidationReport",
    "PhaseGate",

    # Optimizer
    "inject_keywords",
    "calibrate_density",
    "upgrade_verbs",
    "add_signal_tags",
    "apply_nda_abstraction",
    "reorder_sections",
    "apply_audience_aware",
    "auto_calibrate_density",
    "optimize_resume",

    # LaTeX builder
    "build_resume",
    "BuildResult",

    # ATS audit
    "run_ats_audit",
    "ATSAuditResult",

    # Signal tagger
    "add_signal_tags",

    # Audience translator
    "apply_audience_aware",
    "apply_all_audiences",
    "validate_audience_comprehension",

    # Metric plausibility
    "extract_metrics",
    "validate_all_metrics",
    "MetricClaim",

    # Portfolio cross-ref
    "cross_reference",
    "validate_portfolio_crossref",
    "CrossRefResult",
]

__version__ = "2.0.0"