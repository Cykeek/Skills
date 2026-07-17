"""
Job Analyzer — Ingests job postings (URL, text, PDF) and extracts structured requirements,
keyword targets, and company intelligence.

Public API:
    analyze_job(source: str, source_type: Literal["url", "text", "pdf"], company: str | None = None) -> JobAnalysis
    gather_company_intel(company: str, role: str) -> CompanyIntel
    build_keyword_targets(entities: dict, requirements: dict) -> dict
    load_role_template(role_id: str) -> RoleTemplate
    get_ats_keywords(role_id: str, ats_parser: str) -> list[str]
    get_seniority_signals(role_id: str, seniority: str) -> list[str]
    get_gap_triggers(role_id: str) -> list[dict]
"""

from dataclasses import dataclass, asdict, field
from typing import Literal, Optional
import json
import re
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
import yaml

# Optional imports for production fetching
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_HTTP = True
except ImportError:
    HAS_HTTP = False

try:
    import fitz  # pymupdf
    HAS_PDF = True
except ImportError:
    HAS_PDF = False


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

    def model_dump(self) -> dict:
        return asdict(self)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key: str):
        return getattr(self, key)

    def keys(self):
        return asdict(self).keys()


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


# Shared taxonomy for entity extraction (kept in sync with optimizer.py)
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
    term_freq = {}
    for category, terms in entities.items():
        for item in terms:
            term = item['term']
            term_freq[term] = term_freq.get(term, 0) + item['count']

    # Boost terms appearing in requirements
    for req in requirements.get('must_have', []):
        req_lower = req.lower()
        for term in term_freq:
            if re.search(rf'\b{re.escape(term)}\b', req_lower):
                term_freq[term] += 5

    for req in requirements.get('nice_to_have', []):
        req_lower = req.lower()
        for term in term_freq:
            if re.search(rf'\b{re.escape(term)}\b', req_lower):
                term_freq[term] += 2

    # Assign priority bands
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


async def fetch_url_content(url: str) -> str:
    """Fetch and extract text from job posting URL"""
    if not HAS_HTTP:
        return f"[HTTP FETCH UNAVAILABLE - install requests and beautifulsoup4] URL: {url}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; ResumeDoctor/2.0; +https://github.com/resume-doctor)'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')

        # Remove script/style/nav/footer
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        # Try to find main content
        main = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'job|description|content', re.I))
        text = main.get_text(separator='\n', strip=True) if main else soup.get_text(separator='\n', strip=True)
        return text
    except Exception as e:
        return f"[FETCH ERROR: {e}] URL: {url}"


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF file"""
    if not HAS_PDF:
        return f"[PDF EXTRACTION UNAVAILABLE - install pymupdf] Path: {pdf_path}"

    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        return f"[PDF ERROR: {e}] Path: {pdf_path}"


def _merge_role_keywords(targets: dict, role_keywords: dict) -> dict:
    """Merge role template keywords with extracted keyword targets."""
    merged = targets.copy()

    # Add ATS keywords with critical priority
    for kw in role_keywords.get("ats_keywords", []):
        if kw.lower() not in [k.lower() for k in merged]:
            merged[kw] = {"min": 2.0, "max": 3.5, "priority": "critical"}

    # Boost weights for parser-specific keywords
    for parser, parser_kws in role_keywords.get("ats_parser_hints", {}).items():
        if isinstance(parser_kws, list):
            for kw in parser_kws:
                kw_lower = kw.lower()
                for k in merged:
                    if k.lower() == kw_lower:
                        # Boost priority
                        if merged[k]["priority"] == "low":
                            merged[k]["priority"] = "medium"
                        elif merged[k]["priority"] == "medium":
                            merged[k]["priority"] = "high"
                        elif merged[k]["priority"] == "high":
                            merged[k]["priority"] = "critical"
                        break

    return merged


async def analyze_job(source: str, source_type: Literal["url", "text", "pdf"], company: Optional[str] = None, role: Optional[str] = None) -> JobAnalysis:
    """
    Full pipeline: ingest -> clean -> segment -> extract -> classify -> build targets -> gather intel

    Args:
        source: Job source (URL, text, or PDF path)
        source_type: "url", "text", or "pdf"
        company: Optional company name hint
        role: Optional role ID for parser-optimized keyword extraction (e.g., "software-engineer/backend-engineer")
    """
    # Load role template if provided
    role_template = None
    role_keywords = {}
    if role:
        try:
            role_template = load_role_template(role)
            role_keywords = {
                "ats_keywords": role_template.ats_keywords,
                "ats_skills_taxonomy": role_template.ats_skills_taxonomy,
                "seniority_signals": role_template.seniority_signals,
                "ats_weight_hints": role_template.ats_weight_hints,
                "ats_parser_hints": role_template.ats_parser_hints,
            }
        except FileNotFoundError:
            pass  # Role template not found, continue with generic extraction

    # Ingest raw text
    if source_type == "url":
        raw_text = await fetch_url_content(source)
    elif source_type == "pdf":
        raw_text = extract_pdf_text(source)
    else:
        raw_text = source

    cleaned = clean_job_text(raw_text)
    sections = segment_sections(cleaned)
    entities = extract_entities(cleaned)
    req_text = sections.get('requirements', '') + '\n' + sections.get('responsibilities', '')
    requirements = classify_requirements(req_text)

    # Extract company name
    company_name = company or "Unknown Company"
    if not company:
        company_match = re.search(r'(?i)(?:at|@)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)', cleaned)
        if company_match:
            company_name = company_match.group(1)

    # Extract role title
    title_match = re.search(r'(?i)(senior|staff|principal|lead)?\s*(product designer|ux designer|designer|software engineer|product manager|data scientist|devops engineer)', cleaned)
    role_title = title_match.group(0).strip() if title_match else "Unknown Role"

    # Build keyword targets - merge role template keywords with extracted entities
    keyword_targets = build_keyword_targets(entities, requirements)

    # Merge role-specific keywords if template loaded
    if role_keywords:
        keyword_targets = _merge_role_keywords(keyword_targets, role_keywords)

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

    # Company intel
    intel = await gather_company_intel(company_name, role_title)

    return JobAnalysis(
        meta={
            "source_url": source if source_type == "url" else "",
            "source_type": source_type,
            "extracted_at": datetime.utcnow().isoformat() + "Z",
            "extractor_version": "2.1.0"
        },
        company=company_name,
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


def gather_company_intel(company: str, role: str) -> CompanyIntel:
    """Fetch company intelligence from public sources (placeholder implementation)"""
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


async def gather_company_intel_async(company: str, role: str) -> CompanyIntel:
    return gather_company_intel(company, role)


# =============================================================================
# Role Template Loading (for parser-optimized keyword extraction)
# =============================================================================

ROLE_LIBRARY_ROOT = Path(__file__).parent.parent / "references" / "job-descriptions"


@dataclass
class RoleTemplate:
    """Parsed role template from reference library"""
    role_id: str
    canonical_title: str
    aliases: list[str]
    seniority_levels: list[str]
    related_roles: list[str]
    ats_keywords: list[str]
    ats_skills_taxonomy: dict
    seniority_signals: dict
    ats_weight_hints: dict
    ats_parser_hints: dict
    role_summary: str
    core_responsibilities: str
    required_skills_taxonomy: str
    seniority_keywords: str
    ats_parser_keyword_maps: str
    typical_jd_patterns: str
    gap_triggers: list[dict]
    portfolio_crossref: str
    ats_optimization_notes: str


def load_role_template(role_id: str) -> RoleTemplate:
    """
    Load role-specific ATS optimization data from reference library.

    Args:
        role_id: Role identifier like "software-engineer/backend-engineer" or "mobile/mobile-engineer"

    Returns:
        RoleTemplate with all parser-optimized data

    Raises:
        FileNotFoundError: If role template doesn't exist
    """
    path = ROLE_LIBRARY_ROOT / f"{role_id}.md"
    if not path.exists():
        # Try with common prefixes
        for prefix in ["", "software-engineer/", "designer/", "data-science/", "devops-platform/",
                       "engineering-leadership/", "devops-platform/", "mobile/", "security/",
                       "qa-test/", "specialized/"]:
            test_path = ROLE_LIBRARY_ROOT / prefix / f"{role_id}.md"
            if test_path.exists():
                path = test_path
                break
        else:
            raise FileNotFoundError(f"Role template not found: {role_id}")

    content = path.read_text(encoding="utf-8")
    return _parse_role_template(content, role_id)


def _parse_role_template(content: str, role_id: str) -> RoleTemplate:
    """Parse markdown role template with YAML frontmatter into RoleTemplate dataclass."""
    # Extract YAML frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            frontmatter = yaml.safe_load(content[3:end])
            body = content[end + 3:].strip()
        else:
            frontmatter = {}
            body = content
    else:
        frontmatter = {}
        body = content

    # Extract markdown sections
    sections = _extract_markdown_sections(body)

    return RoleTemplate(
        role_id=frontmatter.get("role_id", role_id),
        canonical_title=frontmatter.get("canonical_title", ""),
        aliases=frontmatter.get("aliases", []),
        seniority_levels=frontmatter.get("seniority_levels", []),
        related_roles=frontmatter.get("related_roles", []),
        ats_keywords=frontmatter.get("ats_keywords", []),
        ats_skills_taxonomy=frontmatter.get("ats_skills_taxonomy", {}),
        seniority_signals=frontmatter.get("seniority_signals", {}),
        ats_weight_hints=frontmatter.get("ats_weight_hints", {}),
        ats_parser_hints=frontmatter.get("ats_parser_hints", {}),
        role_summary=sections.get("Role Summary", ""),
        core_responsibilities=sections.get("Core Responsibilities (ATS-Keyword-Rich Bullet Bank)", ""),
        required_skills_taxonomy=sections.get("Required Skills Taxonomy (ATS Keyword Bank)", ""),
        seniority_keywords=sections.get("Seniority Signal Keywords (Verb/Metric Combos)", ""),
        ats_parser_keyword_maps=sections.get("ATS Parser Keyword Maps (Per-Parser)", ""),
        typical_jd_patterns=sections.get("Typical JD Patterns (3 Archetypes)", ""),
        gap_triggers=_parse_gap_triggers(sections.get("Gap Analysis Triggers", "")),
        portfolio_crossref=sections.get("Portfolio Cross-Reference Signals", ""),
        ats_optimization_notes=sections.get("Role-Specific ATS Optimization Notes", ""),
    )


def _extract_markdown_sections(body: str) -> dict[str, str]:
    """Extract markdown sections by ## headers."""
    sections = {}
    current_section = "preamble"
    current_content = []

    for line in body.split("\n"):
        if line.startswith("## "):
            # Save previous section
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def _parse_gap_triggers(content: str) -> list[dict]:
    """Parse gap analysis triggers table from markdown."""
    triggers = []
    lines = content.split("\n")
    in_table = False
    headers = []

    for line in lines:
        if line.startswith("| Missing Keyword"):
            headers = [h.strip() for h in line.split("|")[1:-1]]
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) == len(headers):
                triggers.append(dict(zip(headers, cells)))
        elif in_table and not line.startswith("|"):
            break

    return triggers


def get_ats_keywords(role_id: str, ats_parser: str) -> list[str]:
    """Get parser-specific keyword list for target role."""
    template = load_role_template(role_id)
    parser_hints = template.ats_parser_hints.get(ats_parser, {})

    if isinstance(parser_hints, dict):
        # iCIMS has skill_clusters structure
        if "skill_clusters" in parser_hints:
            keywords = []
            for cluster, skills in parser_hints["skill_clusters"].items():
                if isinstance(skills, list):
                    keywords.extend(skills)
            return keywords
        # Taleo has keywords string
        if "keywords" in parser_hints:
            return [k.strip() for k in parser_hints["keywords"].split(",")]
    elif isinstance(parser_hints, list):
        return parser_hints

    # Fallback to general ATS keywords
    return template.ats_keywords


def get_seniority_signals(role_id: str, seniority: str) -> list[str]:
    """Get seniority-specific signal keywords for role."""
    template = load_role_template(role_id)
    # Normalize seniority key
    seniority_lower = seniority.lower()
    for key in template.seniority_signals:
        if key.lower() == seniority_lower or seniority_lower in key.lower():
            return template.seniority_signals[key]
    return template.seniority_signals.get("senior", [])


def get_gap_triggers(role_id: str) -> list[dict]:
    """Get gap analysis triggers for role."""
    template = load_role_template(role_id)
    return template.gap_triggers


if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) < 3:
        print("Usage: python -m resume_doctor.job_analyzer <source> <source_type> [--out <file>] [--company <name>]")
        sys.exit(1)

    source = sys.argv[1]
    source_type = sys.argv[2]
    out_path = sys.argv[4] if "--out" in sys.argv else "job-analysis.json"
    company = sys.argv[sys.argv.index("--company") + 1] if "--company" in sys.argv else None

    job = asyncio.run(analyze_job(source, source_type, company))
    job.to_json(out_path)
    print(f"Job analysis saved to {out_path}")