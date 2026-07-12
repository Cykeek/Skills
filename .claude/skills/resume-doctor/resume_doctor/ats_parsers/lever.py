"""
Lever ATS Parser Simulation
"""
import re
from dataclasses import dataclass


@dataclass
class ParsedResume:
    contact: dict
    summary: str
    skills: list[str]
    experience: list[dict]
    education: list[dict]
    certifications: list[str]
    projects: list[dict]
    dates: list[str]


def parse(text: str) -> ParsedResume:
    contact = extract_contact(text)
    summary = extract_summary(text)
    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)
    certifications = extract_certifications(text)
    projects = extract_projects(text)
    dates = extract_dates(text)

    return ParsedResume(
        contact=contact,
        summary=summary,
        skills=skills,
        experience=experience,
        education=education,
        certifications=certifications,
        projects=projects,
        dates=dates
    )


def extract_contact(text: str) -> dict:
    email = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    phone = re.search(r'[\+\(]?\d{1,3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text)
    linkedin = re.search(r'linkedin\.com/in/[\w-]+', text)
    portfolio = re.search(r'(https?://)?(www\.)?[\w.-]+\.(com|io|dev|design|me)/', text)

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "portfolio": portfolio.group(0) if portfolio else None
    }


def extract_summary(text: str) -> str:
    match = re.search(r'Professional Summary\s*\n(.*?)(?:\n\s*(?:Skills|Work Experience|Experience|Education|Projects|Certifications)\s*\n)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:500]
    return ""


def extract_skills(text: str) -> list[str]:
    skills = []
    match = re.search(r'Skills\s*\n(.*?)(?:\n\s*(?:Work Experience|Experience|Education|Projects|Certifications)\s*\n)', text, re.DOTALL | re.IGNORECASE)
    if match:
        skill_text = match.group(1)
        items = re.split(r'[,\n•·▪▫●○◆◇■□]+', skill_text)
        skills = [s.strip() for s in items if s.strip() and len(s.strip()) > 2]
    return skills[:50]


def extract_experience(text: str) -> list[dict]:
    experience = []
    match = re.search(r'Work Experience\s*\n(.*?)(?:\n\s*(?:Education|Projects|Certifications|Skills)\s*\n)', text, re.DOTALL | re.IGNORECASE)
    if not match:
        return experience

    exp_text = match.group(1)
    # Split by date ranges
    entries = re.split(r'\n\s*(?:\d{1,2}/\d{4}\s*[–-]\s*(?:\d{1,2}/\d{4}|Present))', exp_text)

    for entry in entries:
        if len(entry.strip()) < 30:
            continue
        lines = [l.strip() for l in entry.split('\n') if l.strip()]
        if len(lines) < 2:
            continue

        company_role = lines[0]
        parts = re.split(r'\s*[|–-]\s*', company_role)
        company = parts[0] if parts else ""
        role = parts[1] if len(parts) > 1 else ""

        bullets = [l for l in lines[1:] if l.startswith(('•', '-', '*', '●', '○', '▪', '▫')) or re.match(r'^\d+\.', l)]
        experience.append({
            "company": company,
            "role": role,
            "bullets": bullets[:10]
        })

    return experience


def extract_education(text: str) -> list[dict]:
    education = []
    match = re.search(r'Education\s*\n(.*?)(?:\n\s*(?:Certifications|Projects|Continuous Learning|Skills|$))', text, re.DOTALL | re.IGNORECASE)
    if match:
        edu_text = match.group(1)
        lines = [l.strip() for l in edu_text.split('\n') if l.strip()]
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                education.append({
                    "degree": lines[i],
                    "school": lines[i + 1],
                    "date": ""
                })
    return education


def extract_certifications(text: str) -> list[str]:
    certs = []
    match = re.search(r'Certifications\s*\n(.*?)(?:\n\s*(?:Projects|Continuous Learning|Skills|Education|$))', text, re.DOTALL | re.IGNORECASE)
    if match:
        cert_text = match.group(1)
        lines = [l.strip() for l in cert_text.split('\n') if l.strip()]
        certs = lines[:10]
    return certs


def extract_projects(text: str) -> list[dict]:
    projects = []
    match = re.search(r'Projects\s*\n(.*?)(?:\n\s*(?:Continuous Learning|Skills|Education|Certifications|$))', text, re.DOTALL | re.IGNORECASE)
    if match:
        proj_text = match.group(1)
        entries = re.split(r'\n\s*\n', proj_text)
        for entry in entries:
            lines = [l.strip() for l in entry.split('\n') if l.strip()]
            if len(lines) >= 2:
                projects.append({
                    "name": lines[0],
                    "details": lines[1:]
                })
    return projects


def extract_dates(text: str) -> list[str]:
    return re.findall(r'\b\d{1,2}/\d{4}\s*[–-]\s*(?:\d{1,2}/\d{4}|Present)\b', text)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    if len(sys.argv) < 2:
        print("Usage: python -m ats_parsers.lever <text_file>")
        sys.exit(1)

    text = Path(sys.argv[1]).read_text(encoding='utf-8')
    result = parse(text)
    import json
    print(json.dumps(result.__dict__, indent=2))