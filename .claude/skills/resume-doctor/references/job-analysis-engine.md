---
name: job-analysis-engine
description: Job posting ingestion, requirement extraction, keyword analysis, gap mapping, and company intelligence gathering for resume tailoring.
---

# Job Analysis Engine — Deep Reference

**Purpose:** Transform any job input (URL, text, PDF, JSON) into structured requirement map + keyword targets + company intel for resume tailoring.

---

## 1. Input Sources & Ingestion

| Source | Tool | Parser Strategy |
|--------|------|-----------------|
| **Greenhouse** | `WebFetch` + DOM | `.job-description`, `.content`, `[data-qa="job-description"]` |
| **Lever** | `WebFetch` + DOM | `.posting-description`, `.description` |
| **Workday** | `WebFetch` + DOM | `.WDJD`, `[data-automation-id="jobDescription"]` |
| **Company Careers** | `WebFetch` + heuristics | Find largest text block after title |
| **LinkedIn Jobs** | `WebFetch` (needs auth) | `.description__text`, `show-more-less-html__markup` |
| **PDF/Word** | `Read` | `pymupdf` / `python-docx` → text |
| **Raw Text** | Direct | Parse with regex + NLP |
| **Structured JSON** | `Read` | Direct mapping |

---

## 2. Extraction Pipeline

### 2.1 Stage 1: Raw Text Cleaning

```python
def clean_job_text(raw: str) -> str:
    # Remove navigation, footer, apply buttons, EEO boilerplate
    text = re.sub(r'(?i)(equal opportunity|eeo|accommodation|background check|drug free).*?(?=\n\n|\Z)', '', raw)
    text = re.sub(r'(?i)(apply now|apply here|submit application).*?(?=\n\n|\Z)', '', text)
    text = re.sub(r'\s{3,}', '\n\n', text)  # Normalize whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
    return text.strip()
```

### 2.2 Stage 2: Section Segmentation

```python
def segment_sections(text: str) -> dict:
    patterns = {
        'about': r'(?i)(about (us|the team|the role|the company))',
        'responsibilities': r'(?i)(what you.?(ll|will) do|responsibilities|key responsibilities|duties)',
        'requirements': r'(?i)(requirements|qualifications|must have|required|you have|you.?ve got)',
        'nice_to_have': r'(?i)(nice to have|preferred|bonus|plus|ideal|desired)',
        'benefits': r'(?i)(benefits|perks|what we offer|compensation)',
        'about_company': r'(?i)(about (us|the company|company name))',
    }
    # Find positions, split, return dict
```

### 2.3 Stage 3: Entity Extraction

```python
# Skill/Tool/Tech taxonomy (updated quarterly)
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

def extract_entities(text: str, taxonomy: dict) -> dict:
    found = defaultdict(list)
    text_lower = text.lower()
    for category, terms in taxonomy.items():
        for term in terms:
            count = len(re.findall(rf'\b{re.escape(term)}\b', text_lower))
            if count > 0:
                found[category].append({"term": term, "count": count})
    return dict(found)
```

### 2.4 Stage 4: Requirement Classification

```python
def classify_requirements(text: str) -> dict:
    lines = re.split(r'\n[\-\*•]\s*|\n\d+\.\s*', text)
    must_have = []
    nice_to_have = []
    
    for line in lines:
        line_lower = line.lower()
        if any(kw in line_lower for kw in ['must', 'required', 'essential', 'need', 'have to', 'strong']):
            must_have.append(line.strip())
        elif any(kw in line_lower for kw in ['nice', 'preferred', 'bonus', 'plus', 'ideal', 'desired', 'familiar', 'exposure']):
            nice_to_have.append(line.strip())
        elif len(line.strip()) > 20:
            must_have.append(line.strip())
    
    return {"must_have": must_have, "nice_to_have": nice_to_have}
```

---

## 3. Output Schema: `job-analysis.json`

```json
{
  "meta": {
    "source_url": "https://boards.greenhouse.io/stripe/jobs/123456",
    "source_type": "greenhouse",
    "extracted_at": "2024-01-15T10:30:00Z",
    "extractor_version": "1.2.0"
  },
  "company": "Stripe",
  "role_title": "Senior Product Designer",
  "role_level": "Senior (IC5)",
  "employment_type": "Full-time",
  "location": "San Francisco, CA / Remote US",
  "visa_sponsorship": true,
  "remote_policy": "Hybrid (3 days/week SF) or Remote US",
  "description_raw": "...",
  "must_have": {
    "hard_skills": ["Figma", "Design Systems", "React", "TypeScript", "A/B Testing"],
    "soft_skills": ["Cross-functional Leadership", "Ambiguity Navigation", "Stakeholder Management"],
    "tools": ["Figma", "Jira", "Mixpanel", "Looker", "Git"],
    "domain_knowledge": ["Payments", "KYC/AML", "PCI-DSS", "Financial Regulations"],
    "years_experience": "5+",
    "education": "Bachelor's Design/HCI/CS or equivalent"
  },
  "nice_to_have": {
    "hard_skills": ["iOS/Android", "Motion Design", "SQL", "Python", "Node.js"],
    "certifications": ["Pragmatic Marketing", "CUxD", "AWS"],
    "domain": ["B2B SaaS", "Marketplace", "Developer Tools"]
  },
  "keywords_at_freq": {
    "design systems": 4,
    "a/b testing": 3,
    "stakeholder": 5,
    "figma": 6,
    "payments": 3,
    "cross-functional": 4,
    "prototyping": 2,
    "accessibility": 2
  },
  "keyword_targets": {
    "design systems": {"min": 2.0, "max": 3.5, "priority": "critical"},
    "a/b testing": {"min": 1.5, "max": 3.0, "priority": "high"},
    "stakeholder": {"min": 1.0, "max": 2.5, "priority": "high"},
    "figma": {"min": 1.5, "max": 3.0, "priority": "high"},
    "payments": {"min": 1.0, "max": 2.0, "priority": "medium"},
    "cross-functional": {"min": 1.0, "max": 2.0, "priority": "medium"},
    "prototyping": {"min": 0.5, "max": 1.5, "priority": "medium"},
    "accessibility": {"min": 0.5, "max": 1.5, "priority": "medium"}
  },
  "ats_signals": {
    "preferred_format": "PDF",
    "required_sections": ["Summary", "Experience", "Skills", "Education"],
    "avoid": ["columns", "graphics", "headers", "footers", "tables", "text boxes"],
    "keyword_density_target": "2-3% per core keyword",
    "parser": "Greenhouse/Workday standard"
  },
  "company_intel": {
    "stage": "Public",
    "size": "8000+",
    "founded": 2010,
    "culture_keywords": ["user obsession", "move fast", "think rigorously", "trust", "simplicity"],
    "tech_stack": ["React", "TypeScript", "GraphQL", "Kubernetes", "Ruby", "Go"],
    "design_maturity": "High — dedicated Design Systems team, 50+ designers",
    "design_leadership": "Kate Aronowitz (former), current VP Design",
    "recent_news": ["Stripe Climate launch", "Revenue Recognition GA", "Identity verification"],
    "glassdoor_rating": 4.3,
    "interview_process": ["Recruiter screen", "Portfolio review", "Design exercise", "Onsite (4-5 rounds)", "Hiring committee"],
    "compensation_band": {"base": "$180-240K", "equity": "$100-300K", "total": "$280-540K"}
  }
}
```

---

## 4. Gap Analysis Algorithm

```python
def analyze_gaps(job_analysis: dict, candidate_profile: dict) -> GapReport:
    gaps = []
    
    # Skills gap
    for category in ['hard_skills', 'tools', 'domain_knowledge']:
        required = set(job_analysis['must_have'].get(category, []))
        candidate = set(candidate_profile.get('skills', {}).get(category, []))
        missing = required - candidate
        for skill in missing:
            gaps.append(Gap(
                category=category,
                item=skill,
                severity="critical" if category == 'hard_skills' else "high",
                suggestion=generate_suggestion(skill, candidate_profile)
            ))
    
    # Keyword density gap
    for kw, target in job_analysis['keyword_targets'].items():
        current_density = estimate_current_density(candidate_profile, kw)
        if current_density < target['min']:
            gaps.append(Gap(
                category="keyword_density",
                item=kw,
                severity="high" if target['priority'] == 'critical' else "medium",
                current=current_density,
                target=target['min'],
                suggestion=f"Inject '{kw}' in {ceil((target['min'] - current_density) * resume_word_count / 100)} bullets"
            ))
    
    # Experience gap
    req_years = parse_years(job_analysis['must_have'].get('years_experience', '0'))
    cand_years = candidate_profile.get('total_years', 0)
    if cand_years < req_years:
        gaps.append(Gap(
            category="experience",
            item=f"{req_years}+ years",
            severity="high",
            current=cand_years,
            target=req_years,
            suggestion="Reframe seniority of past roles; emphasize scope/scale over years"
        ))
    
    # Education gap
    req_edu = job_analysis['must_have'].get('education', '')
    cand_edu = candidate_profile.get('education', [])
    if req_edu and not education_matches(req_edu, cand_edu):
        gaps.append(Gap(
            category="education",
            item=req_edu,
            severity="medium",
            suggestion="Add 'or equivalent experience' framing; highlight relevant coursework"
        ))
    
    return GapReport(gaps=sorted(gaps, key=lambda g: g.severity_rank))
```

---

## 5. Company Intelligence Gathering

| Source | Data Points | Tool |
|--------|-------------|------|
| **Company Website** | Mission, values, products, leadership, tech blog | `WebFetch` |
| **Crunchbase** | Stage, funding, investors, employee count | API |
| **LinkedIn** | Employee count, growth, alumni, skills | `WebFetch` (auth) |
| **Glassdoor** | Rating, interview process, comp, culture | `WebFetch` |
| **Blind/Levels.fyi** | Comp bands, interview details | `WebFetch` |
| **GitHub** | Open source, tech stack, engineering blog | `WebFetch` |
| **Twitter/X** | Leadership voice, announcements | `WebFetch` |
| **News (TechCrunch, etc.)** | Recent launches, funding, strategy | `WebFetch` |

---

## 6. Agent Commands

```bash
# Analyze from URL
agent job analyze --url "https://boards.greenhouse.io/stripe/jobs/12345" --out job-stripe-pd.json

# Analyze from text
agent job analyze --text-file job-description.txt --out job-analysis.json

# Analyze from PDF
agent job analyze --pdf job-description.pdf --out job-analysis.json

# Deep company intel
agent job intel --company "Stripe" --role "Senior Product Designer" --out company-intel.json

# Gap analysis
agent job gap --job job-analysis.json --candidate candidate-profile.yaml --out gap-report.md

# Keyword targets
agent job keywords --job job-analysis.json --resume main.tex --out keyword-report.md
```

---

## 7. Maintenance

- **Taxonomy update**: Quarterly (new tools, frameworks, methodologies)
- **Parser update**: Monthly (ATS vendor changes)
- **Company intel cache**: 7-day TTL (refresh on demand)
- **Keyword target calibration**: Per-application A/B test → aggregate per company/role