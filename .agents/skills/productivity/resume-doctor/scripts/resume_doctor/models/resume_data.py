"""
ResumeData — Format-agnostic structured resume model.

This is the single source of truth for all resume content.
Renderers convert this to LaTeX, Markdown, HTML, JSON, DOCX, PDF.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum
import json


class NDALevel(str, Enum):
    """NDA abstraction levels for sensitive content."""
    L0 = "full"                    # Full transparency: company, metrics, details
    L1 = "company-abstracted"      # Domain, metrics, no company name
    L2 = "domain-abstracted"       # Function, metrics, no domain
    L3 = "pattern-abstracted"      # Method, directional metric only
    L4 = "blackout"                # Process only, no specifics


class OutputFormat(str, Enum):
    """Supported output formats."""
    LATEX = "latex"
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    DOCX = "docx"
    PDF = "pdf"


@dataclass
class Link:
    """Contact/social link."""
    label: str
    url: str
    icon: Optional[str] = None


@dataclass
class ContactInfo:
    """Contact information."""
    name: str
    headline: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    links: List[Link] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Skill:
    """Individual skill with metadata."""
    name: str
    category: str = "General"
    proficiency: Optional[str] = None  # e.g., "Expert", "Advanced", "Intermediate"
    years_experience: Optional[float] = None
    keywords: List[str] = field(default_factory=list)  # ATS keyword variants

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SkillCategory:
    """Group of related skills."""
    name: str
    skills: List[Skill] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SkillSection:
    """Complete skills section with categories."""
    categories: List[SkillCategory] = field(default_factory=list)
    summary: str = ""  # Brief skills summary for quick scanning

    def all_skills(self) -> List[Skill]:
        """Flatten all skills across categories."""
        return [skill for cat in self.categories for skill in cat.skills]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExperienceEntry:
    """Single work experience entry."""
    role: str
    company: str
    location: str = ""
    start_date: str = ""  # Format: "MM/YYYY" or "YYYY"
    end_date: str = "Present"
    description: str = ""
    bullets: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)  # Quantified achievements
    signal_tags: List[str] = field(default_factory=list)  # e.g., "systems-thinking"
    nda_level: NDALevel = NDALevel.L0

    @property
    def date_range(self) -> str:
        return f"{self.start_date} -- {self.end_date}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProjectEntry:
    """Portfolio/case study project."""
    name: str
    role: str = ""
    description: str = ""
    bullets: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)
    link: Optional[str] = None
    image: Optional[str] = None
    signal_tags: List[str] = field(default_factory=list)
    nda_level: NDALevel = NDALevel.L0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EducationEntry:
    """Education/certification entry."""
    degree: str
    institution: str
    location: str = ""
    graduation_date: str = ""  # Format: "MM/YYYY" or "YYYY"
    gpa: Optional[str] = None
    honors: List[str] = field(default_factory=list)
    relevant_coursework: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Certification:
    """Professional certification."""
    name: str
    issuer: str
    date_earned: str = ""
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResumeMeta:
    """Metadata for ATS optimization and rendering."""
    target_role: str = ""
    target_company: str = ""
    ats_keywords: Dict[str, float] = field(default_factory=dict)  # keyword -> target density
    signal_tags: List[str] = field(default_factory=list)
    nda_level: NDALevel = NDALevel.L0
    mode: str = "designer-polish"  # "ats-max" or "designer-polish"
    created_at: str = ""
    updated_at: str = ""
    source_format: str = ""  # Original input format

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResumeData:
    """
    Complete format-agnostic resume data.

    This is the canonical representation that all renderers consume.
    """
    contact: ContactInfo
    summary: str = ""
    skills: SkillSection = field(default_factory=SkillSection)
    experience: List[ExperienceEntry] = field(default_factory=list)
    projects: List[ProjectEntry] = field(default_factory=list)
    education: List[EducationEntry] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    meta: ResumeMeta = field(default_factory=ResumeMeta)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "contact": self.contact.to_dict(),
            "summary": self.summary,
            "skills": self.skills.to_dict(),
            "experience": [e.to_dict() for e in self.experience],
            "projects": [p.to_dict() for p in self.projects],
            "education": [e.to_dict() for e in self.education],
            "certifications": [c.to_dict() for c in self.certifications],
            "meta": self.meta.to_dict(),
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResumeData":
        """Create ResumeData from dictionary."""
        return cls(
            contact=ContactInfo(**data.get("contact", {})),
            summary=data.get("summary", ""),
            skills=SkillSection(**data.get("skills", {})),
            experience=[ExperienceEntry(**e) for e in data.get("experience", [])],
            projects=[ProjectEntry(**p) for p in data.get("projects", [])],
            education=[EducationEntry(**e) for e in data.get("education", [])],
            certifications=[Certification(**c) for c in data.get("certifications", [])],
            meta=ResumeMeta(**data.get("meta", {})),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "ResumeData":
        """Create ResumeData from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def get_all_keywords(self) -> List[str]:
        """Extract all keywords from skills, experience, projects for ATS."""
        keywords = []
        for cat in self.skills.categories:
            for skill in cat.skills:
                keywords.append(skill.name.lower())
                keywords.extend([k.lower() for k in skill.keywords])
        for exp in self.experience:
            keywords.extend([t.lower() for t in exp.technologies])
        for proj in self.projects:
            keywords.extend([t.lower() for t in proj.technologies])
        return list(set(keywords))

    def get_all_signal_tags(self) -> List[str]:
        """Collect all signal tags."""
        tags = set(self.meta.signal_tags)
        for exp in self.experience:
            tags.update(exp.signal_tags)
        for proj in self.projects:
            tags.update(proj.signal_tags)
        return list(tags)

    def validate(self) -> List[str]:
        """Validate required fields, return list of issues."""
        issues = []
        if not self.contact.name or self.contact.name == "Candidate Name":
            issues.append("Missing candidate name")
        if not self.contact.email:
            issues.append("Missing email")
        if not self.summary:
            issues.append("Missing professional summary")
        if not self.experience:
            issues.append("No work experience entries")
        if not self.skills.categories and not self.skills.summary:
            issues.append("No skills section")
        return issues