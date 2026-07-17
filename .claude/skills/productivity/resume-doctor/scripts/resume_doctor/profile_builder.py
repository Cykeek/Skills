"""
Profile Builder - Constructs candidate profile from master resume + LinkedIn
"""
from dataclasses import dataclass, asdict
from typing import Optional
import yaml
import re
import json


@dataclass
class CandidateProfile:
    name: str
    headline: str
    total_years: int
    target_roles: list[str]
    skills: dict
    experience: list[dict]
    education: list[dict]
    certifications: list[str]
    projects: list[dict]
    portfolio_url: str = ""
    linkedin_url: str = ""
    github_url: str = ""

    def model_dump(self) -> dict:
        return asdict(self)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key: str):
        return getattr(self, key)


def parse_latex_resume(tex_path: str) -> dict:
    """Extract structured data from master LaTeX resume"""
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract name
    name_match = re.search(r'\\name\{([^}]+)\}', content)
    if name_match:
        name = name_match.group(1)
    else:
        # Fallback for standard LaTeX or extracted text
        author_match = re.search(r'\\author\{([^}]+)\}', content)
        name = author_match.group(1) if author_match else "Candidate Name"

    # Extract headline
    headline_match = re.search(r'\\headline\{([^}]+)\}', content)
    headline = headline_match.group(1) if headline_match else "Professional Resume"

    # Extract contact
    contact = {}
    for key in ['email', 'phone', 'location', 'linkedin', 'portfolio', 'github']:
        pattern = r'\\' + key + r'\{([^}]+)\}'
        m = re.search(pattern, content)
        if m:
            contact[key] = m.group(1)

    # Extract experience sections
    experience = []
    # Pattern: \roleentry{Company}{Role}{Location}{Dates}
    role_pattern = r'\\roleentry\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}\{([^}]+)\}'
    for match in re.finditer(role_pattern, content):
        company, role, location, dates = match.groups()
        # Find bullets after this roleentry until next roleentry or section
        start = match.end()
        next_match = re.search(role_pattern, content[start:])
        end = start + next_match.start() if next_match else start + 500
        section = content[start:end]

        bullets = re.findall(r'\\bulletitem\{([^}]+)\}', section)
        signals = re.findall(r'\\signaltag\{([^}]+)\}', section)

        experience.append({
            "company": company,
            "role": role,
            "location": location,
            "dates": dates,
            "bullets": bullets,
            "signals": signals
        })

    if not experience:
        # Fallback for standard LaTeX experience section
        exp_sec = re.search(r'\\section\*?\{(?:Work|Professional)?\s*Experience\}(.*?)(?:\\section|$)', content, re.DOTALL | re.I)
        if exp_sec:
            bullets = [re.sub(r'\\[a-zA-Z]+\*?(?:\{[^}]*\})?', '', b).strip() for b in re.findall(r'\\item\s+([^\n\\]+)', exp_sec.group(1))]
            bullets = [b for b in bullets if len(b) > 3]
            if bullets:
                experience.append({
                    "company": "Experience Record",
                    "role": "Professional Role",
                    "location": "",
                    "dates": "2020 – Present",
                    "bullets": bullets,
                    "signals": []
                })

    # Extract education
    education = []
    edu_pattern = r'\\eduentry\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}'
    for match in re.finditer(edu_pattern, content):
        degree, date, school, location = match.groups()
        education.append({"degree": degree, "date": date, "school": school, "location": location})

    # Extract certifications
    certs = []
    cert_pattern = r'\\certentry\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}'
    for match in re.finditer(cert_pattern, content):
        name, date, issuer, _ = match.groups()
        certs.append(f"{name} — {issuer} ({date})")

    # Extract projects
    projects = []
    proj_pattern = r'\\projectentry\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}'
    for match in re.finditer(proj_pattern, content):
        name, context, dates, role = match.groups()
        # Find bullets and signals in project section
        start = match.end()
        next_match = re.search(proj_pattern, content[start:])
        end = start + next_match.start() if next_match else start + 500
        section = content[start:end]

        bullets = re.findall(r'\\bulletitem\{([^}]+)\}', section)
        signals = re.findall(r'\\signaltag\{([^}]+)\}', section)
        stack = re.findall(r'\\kw\{([^}]+)\}', section)

        projects.append({
            "name": name,
            "context": context,
            "dates": dates,
            "role": role,
            "bullets": bullets,
            "signals": signals,
            "stack": stack
        })

    # Extract skills from \section*{Skills}
    skills = {"hard_skills": [], "soft_skills": [], "tools": [], "domain_knowledge": [], "technical": []}
    skills_section = re.search(r'\\section\*\{Skills\}(.*?)(?:\\section|$)', content, re.DOTALL)
    if skills_section:
        skill_text = skills_section.group(1)
        # Parse \item \textbf{Category:} \kw{...}
        for match in re.finditer(r'\\item\s*\\textbf\{([^:}]+):\}\s*(.*?)(?=\\item|\\section|$)', skill_text, re.DOTALL):
            category, items = match.groups()
            kws = re.findall(r'\\kw\{([^}]+)\}', items)
            cat_lower = category.lower()
            if 'design' in cat_lower or 'product' in cat_lower:
                skills['hard_skills'].extend(kws)
            elif 'tool' in cat_lower:
                skills['tools'].extend(kws)
            elif 'technical' in cat_lower or 'code' in cat_lower or 'frontend' in cat_lower:
                skills['technical'].extend(kws)
            elif 'domain' in cat_lower:
                skills['domain_knowledge'].extend(kws)
            else:
                skills['soft_skills'].extend(kws)

        if not any(skills.values()):
            # Fallback: extract plain items or comma-separated terms
            raw_items = re.findall(r'\\item\s+([^\n]+)', skill_text)
            for item in raw_items:
                cleaned = re.sub(r'\\[a-zA-Z]+\*?(?:\{[^}]*\})?', '', item).strip()
                if cleaned:
                    skills['hard_skills'].extend([s.strip() for s in re.split(r'[,|–-]', cleaned) if len(s.strip()) > 1])

    # Calculate total years from experience dates
    total_years = 0
    for exp in experience:
        dates = exp.get('dates', '')
        # Parse MM/YYYY – MM/YYYY or Present
        year_matches = re.findall(r'(\d{4})', dates)
        if len(year_matches) >= 2:
            total_years += int(year_matches[1]) - int(year_matches[0])
        elif len(year_matches) == 1 and 'Present' in dates:
            from datetime import datetime
            total_years += datetime.now().year - int(year_matches[0])

    return {
        "name": name,
        "headline": headline,
        "contact": contact,
        "experience": experience,
        "education": education,
        "certifications": certs,
        "projects": projects,
        "skills": skills,
        "total_years": total_years
    }


def parse_linkedin_pdf(pdf_path: str) -> dict:
    """Extract supplementary data from LinkedIn PDF export (placeholder)"""
    # In production: use pymupdf to extract text, parse sections
    return {}


def build_profile(resume_path: str, linkedin_path: Optional[str] = None) -> CandidateProfile:
    """Build complete candidate profile from master resume + optional LinkedIn"""
    data = parse_latex_resume(resume_path)

    if linkedin_path:
        linkedin_data = parse_linkedin_pdf(linkedin_path)
        # Merge supplementary data
        pass

    profile = CandidateProfile(
        name=data["name"],
        headline=data["headline"],
        total_years=data["total_years"],
        target_roles=[data["headline"]],
        skills=data["skills"],
        experience=data["experience"],
        education=data["education"],
        certifications=data["certifications"],
        projects=data["projects"],
        portfolio_url=data["contact"].get("portfolio", ""),
        linkedin_url=data["contact"].get("linkedin", ""),
        github_url=data["contact"].get("github", "")
    )

    return profile


def save_profile(profile: CandidateProfile, output_path: str):
    """Save as YAML for human review/editing"""
    with open(output_path, 'w') as f:
        yaml.dump(asdict(profile), f, sort_keys=False, allow_unicode=True)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Build candidate profile from LaTeX resume")
    parser.add_argument("--resume", required=True, help="Path to master LaTeX resume (.tex)")
    parser.add_argument("--linkedin", help="Optional LinkedIn PDF export")
    parser.add_argument("--out", default="candidate-profile.yaml", help="Output YAML path")
    args = parser.parse_args()

    profile = build_profile(args.resume, args.linkedin)
    save_profile(profile, args.out)
    print(f"Candidate profile saved to {args.out}")