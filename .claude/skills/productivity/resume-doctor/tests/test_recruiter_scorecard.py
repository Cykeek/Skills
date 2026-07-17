"""
Unit tests for Role-Aware Recruiter Scorecard engine.
Verifies fair evaluation rubrics across SWE, Product Managers, Design/UX, and Leadership.
"""
from resume_doctor.recruiter_scorecard import (
    evaluate_recruiter_scorecard,
    detect_designation_family,
)


def test_detect_designation_family_swe():
    text = "Senior Software Engineer building scalable backend systems in Python and Docker."
    assert detect_designation_family(text) == "engineering_swe"


def test_detect_designation_family_pm():
    text = "Senior Technical Product Manager driving user retention and go-to-market milestones."
    assert detect_designation_family(text) == "product_management"


def test_detect_designation_family_design():
    text = "Lead UX Designer creating Figma prototypes, user research studies, and design systems."
    assert detect_designation_family(text) == "design_ux"


def test_recruiter_scorecard_pm_no_github_penalty():
    """Ensure a Product Manager with strong product KPIs and portfolio URL scores high without GitHub."""
    pm_resume = """
    Senior Product Manager
    - Owned enterprise roadmap aligning cross-functional stakeholder teams.
    - Grew Monthly Active Users (MAU) by 45% ($2.4M ARR impact) through scientific funnel optimization.
    - Launched 3 go-to-market initiatives verified at https://product-portfolio.example.com
    """
    card = evaluate_recruiter_scorecard(pm_resume)
    assert card.designation_family == "product_management"
    assert card.overall_score >= 80, f"Expected PM overall score >= 80, got {card.overall_score}"
    assert card.verdict == "INTERVIEW_READY"
    assert card.deductions == 0


def test_recruiter_scorecard_designer_fairness():
    """Ensure a UX Designer is evaluated fairly on Figma/design systems and portfolio case study links."""
    designer_resume = """
    Lead UX Designer
    - Designed comprehensive interactive prototype and figma design system for 200k daily users.
    - Conducted usability testing and user research to reduce onboarding drop-off by 31%.
    - Complete portfolio and case studies at https://ux-portfolio.example.com
    """
    card = evaluate_recruiter_scorecard(designer_resume)
    assert card.designation_family == "design_ux"
    assert card.overall_score >= 80
    assert card.verdict == "INTERVIEW_READY"


def test_fluff_penalty_deduction():
    """Check that excessive buzzwords get penalized."""
    fluffy_resume = """
    Rockstar Synergy Guru
    - Thought leader providing visionary leadership for various ambiguous projects.
    """
    card = evaluate_recruiter_scorecard(fluffy_resume)
    assert card.deductions >= 10
    assert len(card.deductions_applied) > 0
