"""
Content Outline Model
=====================
Structured outline with sections, hook, CTA, and SEO elements.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models.enums import HookType, StructurePattern, PersuasionFramework, CTAType, CTACommitmentLevel, Goal, Format


@dataclass
class Hook:
    """Opening hook for the content."""
    type: HookType = HookType.QUESTION
    text: str = ""
    promise: str = ""  # What the hook promises the reader will get
    rationale: str = ""  # Why this hook type was selected

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = HookType(self.type)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type.value, "text": self.text, "promise": self.promise, "rationale": self.rationale}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Hook":
        if "type" in data and isinstance(data["type"], str):
            data["type"] = HookType(data["type"])
        return cls(**data)


@dataclass
class CTA:
    """Call to action."""
    type: CTAType = CTAType.READ_NEXT
    text: str = ""
    url: str = ""
    commitment_level: CTACommitmentLevel = CTACommitmentLevel.LOW
    position: str = "end"  # "end", "middle", "inline"

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = CTAType(self.type)
        if isinstance(self.commitment_level, str):
            self.commitment_level = CTACommitmentLevel(self.commitment_level)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "text": self.text,
            "url": self.url,
            "commitment_level": self.commitment_level.value,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CTA":
        if "type" in data and isinstance(data["type"], str):
            data["type"] = CTAType(data["type"])
        if "commitment_level" in data and isinstance(data["commitment_level"], str):
            data["commitment_level"] = CTACommitmentLevel(data["commitment_level"])
        return cls(**data)


@dataclass
class SEOElements:
    """SEO metadata for the content."""
    primary_keyword: str = ""
    secondary_keywords: List[str] = field(default_factory=list)
    meta_title: str = ""
    meta_description: str = ""
    target_word_count: int = 0
    heading_structure: List[str] = field(default_factory=list)  # H1, H2, H3 hierarchy
    internal_links: List[Dict[str, str]] = field(default_factory=list)  # [{"anchor": "text", "url": "..."}]
    external_links: List[Dict[str, str]] = field(default_factory=list)
    search_intent: str = ""  # informational, commercial, transactional, navigational

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SEOElements":
        return cls(**data)


@dataclass
class OutlineSection:
    """Individual section in the outline."""
    heading: str = ""
    level: int = 2  # H2=2, H3=3, etc.
    key_points: List[str] = field(default_factory=list)
    target_word_count: int = 0
    persuasion_element: str = ""  # Which persuasion framework element this covers
    evidence_needed: List[str] = field(default_factory=list)  # Stats, quotes, examples needed
    transition: str = ""  # Transition to next section

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OutlineSection":
        return cls(**data)


@dataclass
class ContentOutline:
    """
    Complete content outline generated from brief.

    Contains:
    - Hook (opening)
    - Sections with hierarchy
    - CTA (closing)
    - SEO elements
    - Structural pattern used
    - Persuasion framework applied
    """
    title: str = ""
    hook: Hook = field(default_factory=Hook)
    sections: List[OutlineSection] = field(default_factory=list)
    cta: CTA = field(default_factory=CTA)
    seo: SEOElements = field(default_factory=SEOElements)

    # Structural metadata
    structure_pattern: StructurePattern = StructurePattern.PROBLEM_SOLUTION
    persuasion_framework: PersuasionFramework = PersuasionFramework.NONE
    format: Format = Format.BLOG
    goal: Goal = Goal.EDUCATE

    # Estimates
    estimated_word_count: int = 0
    estimated_sections: int = 0

    # Metadata
    template_used: Optional[str] = None
    source_brief_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.structure_pattern, str):
            self.structure_pattern = StructurePattern(self.structure_pattern)
        if isinstance(self.persuasion_framework, str):
            self.persuasion_framework = PersuasionFramework(self.persuasion_framework)
        if isinstance(self.format, str):
            self.format = Format(self.format)

        # Compute estimates
        self.estimated_sections = len(self.sections)
        self.estimated_word_count = sum(s.target_word_count for s in self.sections)

    def get_heading_structure(self) -> List[str]:
        """Get heading hierarchy for SEO."""
        structure = [f"H1: {self.title}"]
        for section in self.sections:
            prefix = "H" + str(section.level)
            structure.append(f"{prefix}: {section.heading}")
        return structure

    def get_all_key_points(self) -> List[str]:
        """Flatten all key points from all sections."""
        points = []
        for section in self.sections:
            points.extend(section.key_points)
        return points

    def get_section_by_heading(self, heading: str) -> Optional[OutlineSection]:
        """Find section by heading (case-insensitive)."""
        for section in self.sections:
            if section.heading.lower() == heading.lower():
                return section
        return None

    def add_section(self, section: OutlineSection) -> None:
        """Add a section and update estimates."""
        self.sections.append(section)
        self.estimated_sections = len(self.sections)
        self.estimated_word_count += section.target_word_count

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["hook"] = self.hook.to_dict()
        data["cta"] = self.cta.to_dict()
        data["seo"] = self.seo.to_dict()
        data["sections"] = [s.to_dict() for s in self.sections]
        data["structure_pattern"] = self.structure_pattern.value
        data["persuasion_framework"] = self.persuasion_framework.value
        return data

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentOutline":
        # Handle nested objects
        if "hook" in data and data["hook"]:
            data["hook"] = Hook.from_dict(data["hook"])
        if "cta" in data and data["cta"]:
            data["cta"] = CTA.from_dict(data["cta"])
        if "seo" in data and data["seo"]:
            data["seo"] = SEOElements.from_dict(data["seo"])
        if "sections" in data and data["sections"]:
            data["sections"] = [OutlineSection.from_dict(s) for s in data["sections"]]

        # Handle enums
        if "structure_pattern" in data and isinstance(data["structure_pattern"], str):
            data["structure_pattern"] = StructurePattern(data["structure_pattern"])
        if "persuasion_framework" in data and isinstance(data["persuasion_framework"], str):
            data["persuasion_framework"] = PersuasionFramework(data["persuasion_framework"])

        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "ContentOutline":
        return cls.from_dict(json.loads(json_str))