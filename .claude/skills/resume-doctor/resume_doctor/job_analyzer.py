"""
Job Analyzer — Ingests job postings (URL, text, PDF) and extracts structured requirements,
keyword targets, and company intelligence.

Public API:
    analyze_job(source: str, source_type: Literal["url", "text", "pdf"]) -> JobAnalysis
    gather_company_intel(company: str, role: str) -> CompanyIntel
    build_keyword_targets(entities: dict, requirements: dict) -> dict
"""

from dataclasses import dataclass, asdict
from typing import Literal
import json
import re
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class JobAnalysis:
    """Structured job analysis matching schemas/job-analysis.json"""
    meta: dict
    company: str
    role_title: str
    role_level: str
    employment_type: str
    location: str
    visa_sponsorship: bool
    remote_policy: str
    description_raw: str
    must_have: dict
    nice_to_have: dict
    keywords_at_freq: dict
    keyword_targets: dict
    ats_signals: dict
    company_intel: dict

    def to_json(self, path: str) -> None:
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2, default=str)


@dataclass
class CompanyIntel:
    """Company intelligence matching job-analysis.json.company_intel"""
    stage: str
    size: str
    founded: int
    culture_keywords: list[str]
    tech_stack: list[str]
    design_maturity: str
    design_leadership: str
    recent_news: list[str]
    glassdoor_rating: float
    interview_process: list[str]
    compensation_band: dict


# Taxonomy for entity extraction (updated quarterly)
TAXONOMY = {
    'design_tools': ['figma', 'sketch', 'framer', 'principle', 'protopie', 'adobe xd', 'zeplin', 'invision', 'miro', 'figjam'],
    'design_systems': ['design systems', 'design tokens', 'storybook', 'style dictionary', 'component library', 'design ops'],
    'research': ['user research', 'usability testing', 'jtbd', 'jobs to be done', 'surveys', 'card sorting', 'tree testing', 'diary studies'],
    'frontend': ['react', 'typescript', 'javascript', 'html', 'css', 'sass', 'less', 'tailwind', 'styled-components', 'emotion', 'next.js', 'vite', 'webpack'],
    'analytics': ['mixpanel', 'amplitude', 'heap', 'looker', 'tableau', 'mode', 'sql', 'python', 'r', 'a/b testing', 'experimentation'],
    'accessibility': ['wcag', 'wcag 2.1', 'wcag 2.2', 'section 508', 'aria', 'screen reader', 'nvda', 'jaws', 'voiceover'],
    'leadership': ['cross-functional', 'stakeholder management', 'mentor', 'coach', 'design review', 'roadmap', 'prioritization', 'raci'],
    'domains': ['fintech', 'payments', 'banking', 'kyc', 'aml', 'pci-dss', 'b2b saas', 'marketplace', 'ecommerce', 'healthtech', 'edtech'],
}


def clean_job_text(raw: str) -> str:
    """Stage 1: Remove navigation, footer, apply buttons, EEO boilerplate"""
    text = re.sub(r'(?i)(equal opportunity|eeo|accommodation|background check|drug free).*?(?=\n\n|\Z)', '', raw)
    text = re.sub(r'(?i)(apply now|apply here|submit application).*?(?=\n\n|\Z)', '', text)
    text = re.sub(r'\s{3,}', '\n\n', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def segment_sections(text: str) -> dict:
    """Stage 2: Split into about, responsibilities, requirements, nice_to_have, benefits, about_company"""
    patterns = {
        'about': r'(?i)(about (us|the team|the role|the company))',
        'responsibilities': r'(?i)(what you.?(ll|will) do|responsibilities|key responsibilities|duties)',
        'requirements': r'(?i)(requirements|qualifications|must have|required|you have|you.?ve got)',
        'nice_to_have': r'(?i)(nice to have|preferred|bonus|plus|ideal|desired)',
        'benefits': r'(?i)(benefits|perks|what we offer|compensation)',
        'about_company': r'(?i)(about (us|the company|company name))',
    }
    positions = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            positions[name] = match.start()

    # Sort by position and extract sections
    sorted_sections = sorted(positions.items(), key=lambda x: x[1])
    sections = {}
    for i, (name, pos) in enumerate(sorted_sections):
        end = sorted_sections[i + 1][1] if i + 1 < len(sorted_sections) else len(text)
        sections[name] = text[pos:end].strip()

    return sections


def extract_entities(text: str, taxonomy: dict = TAXONOMY) -> dict:
    """Stage 3: Find taxonomy terms in text with counts"""
    found = {}
    text_lower = text.lower()
    for category, terms in taxonomy.items():
        matches = []
        for term in terms:
            count = len(re.findall(rf'\b{re.escape(term)}\b', text_lower))
            if count > 0:
                matches.append({"term": term, "count": count})
        if matches:
            found[category] = matches
    return found


def classify_requirements(text: str) -> dict:
    """Stage 4: Split into must_have vs nice_to_have lines"""
    lines = re.split(r'\n[\-\*•]\s*|\n\d+\.\s*', text)
    must_have = []
    nice_to_have = []

    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower or len(line_lower) < 10:
            continue
        if any(kw in line_lower for kw in ['must', 'required', 'essential', 'need', 'have to', 'strong']):
            must_have.append(line.strip())
        elif any(kw in line_lower for kw in ['nice', 'preferred', 'bonus', 'plus', 'ideal', 'desired', 'familiar', 'exposure']):
            nice_to_have.append(line.strip())
        elif len(line.strip()) > 20:
            must_have.append(line.strip())

    return {"must_have": must_have, "nice_to_have": nice_to_have}


def build_keyword_targets(entities: dict, requirements: dict) -> dict:
    """Convert entity frequencies + requirement priority into density bands"""
    # Aggregate all terms with their frequencies
    term_freq = {}
    for category, terms in entities.items():
        for item in terms:
            term = item['term']
            term_freq[term] = term_freq.get(term, 0) + item['count']

    # Boost terms appearing in requirements
    for req in requirements.get('must_have', []):
        req_lower = req.lower()
        for term in term_freq:
            if term in req_lower:
                term_freq[term] += 5  # boost

    for req in requirements.get('nice_to_have', []):
        req_lower = req.lower()
        for term in term_freq:
            if term in req_lower:
                term_freq[term] += 2  # smaller boost

    # Assign priority bands based on frequency
    targets = {}
    for term, freq in term_freq.items():
        if freq >= 8:
            targets[term] = {"min": 2.0, "max": 3.5, "priority": "critical"}
        elif freq >= 5:
            targets[term] = {"min": 1.5, "max": 3.0, "priority": "high"}
        elif freq >= 3:
            targets[term] = {"min": 1.0, "max": 2.5, "priority": "medium"}
        else:
            targets[term] = {"min": 0.5, "max": 1.5, "priority": "low"}

    return targets


def parse_years(text: str) -> int:
    """Extract years from '5+', '5 years', etc."""
    match = re.search(r'(\d+)\+?', text)
    return int(match.group(1)) if match else 0


def infer_role_level(title: str, years: int) -> str:
    title_lower = title.lower()
    if 'staff' in title_lower or 'principal' in title_lower or 'lead' in title_lower:
        return f"Staff/Principal ({years}+)"
    elif 'senior' in title_lower:
        return f"Senior ({years}+)"
    elif years >= 5:
        return f"Senior ({years}+)"
    return f"Mid ({years}+)"


def detect_ats_from_url(url: str) -> str:
    """Detect ATS platform from job URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if 'greenhouse' in domain:
        return 'greenhouse'
    elif 'lever' in domain:
        return 'lever'
    elif 'workday' in domain or 'myworkdayjobs' in domain:
        return 'workday'
    elif 'icims' in domain:
        return 'icims'
    elif 'taleo' in domain:
        return 'taleo'
    return 'unknown'


async def analyze_job(source: str, source_type: Literal["url", "text", "pdf"]) -> JobAnalysis:
    """
    Full pipeline: ingest → clean → segment → extract → classify → build targets → gather intel
    """
    # Ingest raw text
    if source_type == "url":
        # In production: use WebFetch or requests + BeautifulSoup
        raw_text = f"[FETCHED FROM {source}]"  # Placeholder
    elif source_type == "pdf":
        # In production: use pymupdf/fitz
        raw_text = f"[EXTRACTED FROM {source}]"  # Placeholder
    else:
        raw_text = source

    cleaned = clean_job_text(raw_text)
    sections = segment_sections(cleaned)
    entities = extract_entities(cleaned)
    requirements = classify_requirements(sections.get('requirements', '') + '\n' + sections.get('responsibilities', ''))

    # Extract company name from URL or text
    company_match = re.search(r'(?i)(?:at|@)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)', cleaned)
    company = company_match.group(1) if company_match else "Unknown Company"

    # Extract role title
    title_match = re.search(r'(?i)(senior|staff|principal|lead)?\s*(product designer|ux designer|designer|software engineer)', cleaned)
    role_title = title_match.group(0).strip() if title_match else "Unknown Role"

    # Build keyword targets
    keyword_targets = build_keyword_targets(entities, requirements)

    # Build must_have structured
    must_have = {
        "hard_skills": [t['term'] for t in entities.get('design_tools', []) + entities.get('frontend', []) + entities.get('design_systems', [])],
        "soft_skills": [t['term'] for t in entities.get('leadership', [])],
        "tools": [t['term'] for t in entities.get('design_tools', []) + entities.get('analytics', [])],
        "domain_knowledge": [t['term'] for t in entities.get('domains', [])],
        "years_experience": "5+",
        "education": "Bachelor's or equivalent"
    }

    nice_to_have = {
        "hard_skills": [],
        "certifications": [],
        "domain": []
    }

    # Company intel (placeholder - in production uses WebFetch + APIs)
    intel = CompanyIntel(
        stage="Unknown",
        size="Unknown",
        founded=0,
        culture_keywords=[],
        tech_stack=[],
        design_maturity="Unknown",
        design_leadership="Unknown",
        recent_news=[],
        glassdoor_rating=0.0,
        interview_process=[],
        compensation_band={}
    )

    return JobAnalysis(
        meta={
            "source_url": source if source_type == "url" else "",
            "source_type": source_type,
            "extracted_at": datetime.utcnow().isoformat() + "Z",
            "extractor_version": "2.0.0"
        },
        company=company,
        role_title=role_title,
        role_level=infer_role_level(role_title, parse_years(must_have["years_experience"])),
        employment_type="Full-time",
        location="Unknown",
        visa_sponsorship=False,
        remote_policy="Unknown",
        description_raw=cleaned,
        must_have=must_have,
        nice_to_have=nice_to_have,
        keywords_at_freq={k: sum(item['count'] for item in v) for k, v in entities.items()},
        keyword_targets=keyword_targets,
        ats_signals={
            "preferred_format": "PDF",
            "required_sections": ["Summary", "Experience", "Skills", "Education"],
            "avoid": ["columns", "graphics", "headers", "footers", "tables", "text boxes"],
            "keyword_density_target": "2-3% per core keyword",
            "parser": detect_ats_from_url(source) if source_type == "url" else "unknown"
        },
        company_intel=asdict(intel)
    )


async def gather_company_intel(company: str, role: str) -> CompanyIntel:
    """Fetch company intelligence from public sources (placeholder)"""
    # In production: WebFetch company site, Crunchbase API, LinkedIn, Glassdoor, GitHub, Twitter, News
    return CompanyIntel(
        stage="Unknown",
        size="Unknown",
        founded=0,
        culture_keywords=[],
        tech_stack=[],
        design_maturity="Unknown",
        design_leadership="Unknown",
        recent_news=[],
        glassdoor_rating=0.0,
        interview_process=[],
        compensation_band={}
    )


if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) < 3:
        print("Usage: python -m resume_doctor.job_analyzer <source> <source_type> [--out <file>]")
        sys.exit(1)

    source = sys.argv[1]
    source_type = sys.argv[2]
    out_path = sys.argv[4] if "--out" in sys.argv else "job-analysis.json"

    job = asyncio.run(analyze_job(source, source_type))
    job.to_json(out_path)
    print(f"Job analysis saved to {out_path}")