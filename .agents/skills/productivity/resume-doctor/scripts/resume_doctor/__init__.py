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
    load_role_template,
    get_ats_keywords,
    get_seniority_signals,
    get_gap_triggers,
    JobAnalysis,
    CompanyIntel,
    RoleTemplate,
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
    HybridSkillMatcher,
    lemmatize_phrase,
    lemmatize_word,
    compute_cosine_similarity,
    get_skill_synonyms,
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
    validate_experience_overlap,
    validate_concept_vs_shipped,
    validate_metric_verification,
    validate_subagent_harness,
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
    escape_latex_special_chars,
    ensure_engine_safe_preamble,
)

from .ats_audit import (
    run_ats_audit,
    ATSAuditResult,
)

from .recruiter_scorecard import (
    evaluate_recruiter_scorecard,
    detect_designation_family,
    RecruiterScorecard,
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

from .output_manager import (
    ensure_master_output_dir,
    create_task_subfolder,
    write_overleaf_instructions,
    find_workspace_root,
)

__all__ = [
    # Job analysis
    "analyze_job",
    "gather_company_intel",
    "build_keyword_targets",
    "load_role_template",
    "get_ats_keywords",
    "get_seniority_signals",
    "get_gap_triggers",
    "JobAnalysis",
    "CompanyIntel",
    "RoleTemplate",

    # Profile
    "parse_latex_resume",
    "parse_linkedin_pdf",
    "build_profile",
    "CandidateProfile",

    # Gap analysis
    "analyze_gaps",
    "analyze_general_ats_gaps",
    "build_injection_map",
    "HybridSkillMatcher",
    "lemmatize_phrase",
    "lemmatize_word",
    "compute_cosine_similarity",
    "get_skill_synonyms",
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
    "validate_experience_overlap",
    "validate_concept_vs_shipped",
    "validate_metric_verification",
    "validate_subagent_harness",
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
    "escape_latex_special_chars",
    "ensure_engine_safe_preamble",

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

    # Output management
    "ensure_master_output_dir",
    "create_task_subfolder",
    "write_overleaf_instructions",
    "find_workspace_root",
]

__version__ = "2.1.0"