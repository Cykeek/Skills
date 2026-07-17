"""
Role-Aware Recruiter Scorecard Engine for Resume Doctor.
Inspired by objective evidence evaluation (bonus points, deductions, concrete citations)
without developer-only GitHub bias. Adapts rubrics across Engineering, Design, Product, Leadership, and General roles.
"""
from dataclasses import dataclass, asdict
import re
from typing import Optional, Dict, List


@dataclass
class PillarScore:
    name: str
    max_score: int
    score: int
    evidence: List[str]
    gaps: List[str]


@dataclass
class RecruiterScorecard:
    designation_family: str
    overall_score: int
    max_score: int
    verdict: str  # "INTERVIEW_READY", "BORDERLINE", "NEEDS_EVIDENCE"
    bonus_points: int
    deductions: int
    pillars: Dict[str, dict]
    bonuses_awarded: List[str]
    deductions_applied: List[str]
    recruiter_summary: str


# Domain role mapping detector
ROLE_FAMILIES = {
    "engineering_swe": [
        "software engineer", "swe", "backend", "frontend", "fullstack", "devops",
        "sre", "platform engineer", "data engineer", "ml engineer", "ai engineer"
    ],
    "product_management": [
        "product manager", "pm", "technical product manager", "tpm", "platform pm",
        "growth pm"
    ],
    "design_ux": [
        "product designer", "ui designer", "ux designer", "design systems",
        "user researcher", "interaction designer"
    ],
    "engineering_leadership": [
        "engineering manager", "director of engineering", "vp engineering",
        "head of engineering", "cto"
    ]
}

# Verifiable artifact signals per role family
ROLE_ARTIFACT_SIGNALS = {
    "engineering_swe": ["github.com/", "gitlab.com/", "open source", "pypi.org", "crates.io"],
    "product_management": ["http", "www.", "kpi", "launch", "roadmap", "prd", "retention", "wau", "mau", "arr"],
    "design_ux": ["figma", "behance", "dribbble", "portfolio", "design system", "case study"],
    "engineering_leadership": ["hired", "team of", "engineers", "scale", "retention", "velocity", "roadmap", "org"]
}

# Vague buzzwords that trigger deductions if not accompanied by impact metrics
VAGUE_BUZZWORDS = [
    "synergy", "rockstar", "ninja", "guru", "visionary leadership",
    "thought leader", "results-driven professional", "self-motivated team player"
]


def detect_designation_family(text: str) -> str:
    """Classify resume text into designation family for fair rubric evaluation."""
    lower = text.lower()
    scores = {}
    for family, keywords in ROLE_FAMILIES.items():
        score = sum(1 for kw in keywords if kw in lower)
        scores[family] = score

    best_family = max(scores, key=scores.get)
    if scores[best_family] == 0:
        return "general_professional"
    return best_family


def evaluate_recruiter_scorecard(resume_text: str, role_family: Optional[str] = None) -> RecruiterScorecard:
    """Evaluate resume text against a role-polymorphic recruiter scorecard."""
    if not role_family:
        role_family = detect_designation_family(resume_text)

    lower = resume_text.lower()
    paragraphs = [p.strip() for p in resume_text.split("\n") if p.strip()]

    # 1. Pillar: Proven Impact / Quantifiable Outcomes (Max 35 pts)
    # Search for numeric impact metrics (%, $, Nx, ms, scale, initiatives, teams, etc)
    metrics_found = re.findall(
        r'(\d+(?:\.\d+)?%|\$\d+(?:\.\d+)?[kmbKMB]?|\b\d+[kmbKMB]\b|\d+[xX]|\b\d+\+?\s*(?:ms|users|engineers|kpi|initiatives|teams|projects|customers|arr|mau|wau)\b)',
        resume_text,
        re.I
    )
    impact_score = min(35, len(metrics_found) * 9)
    impact_evidence = [f"Found quantitative metrics: {', '.join(metrics_found[:5])}"] if metrics_found else []
    impact_gaps = [] if impact_score >= 25 else ["Add concrete business or system metrics (%, $, scale) to bullets."]

    # 2. Pillar: Domain & Technical Rigor (Max 25 pts)
    # Check domain core vocabulary
    domain_terms = {
        "engineering_swe": ["api", "cloud", "sql", "architecture", "docker", "test", "pipeline", "latency"],
        "product_management": ["roadmap", "stakeholder", "user", "go-to-market", "metric", "experiment", "funnel"],
        "design_ux": ["figma", "wireframe", "user research", "prototype", "usability", "accessibility", "design system"],
        "engineering_leadership": ["hiring", "scaling", "mentorship", "delivery", "strategy", "roadmap", "architecture"],
        "general_professional": ["project", "delivery", "stakeholder", "process", "optimization", "collaboration"]
    }
    targets = domain_terms.get(role_family, domain_terms["general_professional"])
    matched_domain = [t for t in targets if t in lower]
    rigor_score = min(25, len(matched_domain) * 7)
    rigor_evidence = [f"Domain rigor signals present: {', '.join(matched_domain[:5])}"] if matched_domain else []
    rigor_gaps = [] if rigor_score >= 18 else [f"Expand concrete domain terminology for {role_family}."]

    # 3. Pillar: Verifiable External Proof / Portfolio Signals (Max 20 pts)
    signals = ROLE_ARTIFACT_SIGNALS.get(role_family, ["http", "www.", "linkedin"])
    matched_signals = [s for s in signals if s in lower]
    proof_score = min(20, len(matched_signals) * 10)
    proof_evidence = [f"Verifiable external evidence cues found: {', '.join(matched_signals)}"] if matched_signals else []
    proof_gaps = [] if proof_score >= 15 else [f"Include direct artifact proof links appropriate for {role_family}."]

    # 4. Pillar: Signal-to-Noise Ratio (Max 20 pts)
    noise_hits = [bw for bw in VAGUE_BUZZWORDS if bw in lower]
    snr_score = max(0, 20 - (len(noise_hits) * 5))
    snr_evidence = ["Clean signal-to-noise ratio: professional action verbs used without fluff."] if not noise_hits else []
    snr_gaps = [f"Remove vague buzzwords: {', '.join(noise_hits)}"] if noise_hits else []

    # Calculate base points
    base_score = impact_score + rigor_score + proof_score + snr_score

    # Bonus & Deductions mechanics
    bonus_points = 0
    bonuses_awarded = []
    if len(metrics_found) >= 5:
        bonus_points += 5
        bonuses_awarded.append("+5 High metric plaque: 5+ quantified outcomes")
    if any(url in lower for url in ["github.com", "portfolio", "figma", "http"]):
        bonus_points += 5
        bonuses_awarded.append("+5 Live artifact verification link present")

    deductions = 0
    deductions_applied = []
    if len(noise_hits) >= 2:
        deductions += 10
        deductions_applied.append(f"-10 Fluff vocabulary detected ({', '.join(noise_hits[:2])})")

    overall_score = max(0, min(100, base_score + bonus_points - deductions))

    if overall_score >= 80:
        verdict = "INTERVIEW_READY"
        summary = f"Strong evidence-backed profile tailored for {role_family}. Clear impact metrics and verifiable domain rigor."
    elif overall_score >= 60:
        verdict = "BORDERLINE"
        summary = f"Solid profile for {role_family}, but would benefit from richer quantitative outcomes or artifact links."
    else:
        verdict = "NEEDS_EVIDENCE"
        summary = f"Profile scores below recruiter interview threshold for {role_family}. Requires concrete metrics and evidence."

    pillars = {
        "proven_impact": asdict(PillarScore("Proven Impact & Scale", 35, impact_score, impact_evidence, impact_gaps)),
        "domain_rigor": asdict(PillarScore("Domain & Technical Rigor", 25, rigor_score, rigor_evidence, rigor_gaps)),
        "verifiable_proof": asdict(PillarScore("Verifiable External Proof", 20, proof_score, proof_evidence, proof_gaps)),
        "signal_to_noise": asdict(PillarScore("Signal-to-Noise Ratio", 20, snr_score, snr_evidence, snr_gaps)),
    }

    return RecruiterScorecard(
        designation_family=role_family,
        overall_score=overall_score,
        max_score=100,
        verdict=verdict,
        bonus_points=bonus_points,
        deductions=deductions,
        pillars=pillars,
        bonuses_awarded=bonuses_awarded,
        deductions_applied=deductions_applied,
        recruiter_summary=summary
    )
