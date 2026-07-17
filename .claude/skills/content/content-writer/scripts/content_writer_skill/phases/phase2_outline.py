"""
Phase 2: Outline
================
Structure selection, section planning, hook/CTA creation, SEO elements.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models import (
    ContentBrief, ContentOutline, OutlineSection, Hook, CTA, SEOElements,
    StructurePattern, PersuasionFramework, HookType, CTAType, CTACommitmentLevel,
    ValidationGateResult, Goal, Format
)


@dataclass
class Phase2Result:
    """Result of Phase 2: Outline."""
    outline: ContentOutline
    validation: ValidationGateResult
    structure_rationale: str


class OutlinePhase:
    """
    Phase 2: Outline

    Inputs: Validated ContentBrief from Phase 1
    Outputs: ContentOutline with sections, hook, CTA, SEO elements
    """

    # Structure pattern -> section templates mapping
    STRUCTURE_TEMPLATES = {
        StructurePattern.PROBLEM_SOLUTION: [
            ("The Problem", "What the reader is struggling with", "PAS - Problem"),
            ("Why It Matters", "Impact and stakes", "PAS - Agitation"),
            ("The Solution", "Your approach/methodology", "PAS - Solution"),
            ("How to Implement", "Step-by-step guidance", "PAS - Solution"),
            ("Common Pitfalls", "What to avoid", "PAS - Solution"),
            ("Next Steps", "Actionable takeaway", "CTA setup"),
        ],
        StructurePattern.BEFORE_AFTER_BRIDGE: [
            ("The Before State", "Current pain/frustration", "BAB - Before"),
            ("The After State", "Desired transformation", "BAB - After"),
            ("The Bridge", "Your solution as the path", "BAB - Bridge"),
            ("Proof It Works", "Evidence/case studies", "BAB - Bridge"),
            ("Your Next Move", "Call to action", "CTA"),
        ],
        StructurePattern.ATTENTION_INTEREST_DESIRE_ACTION: [
            ("Hook", "Grab attention immediately", "AIDA - Attention"),
            ("The Problem", "Build interest with relevance", "AIDA - Interest"),
            ("The Solution", "Create desire for the outcome", "AIDA - Desire"),
            ("How to Get Started", "Clear action steps", "AIDA - Action"),
        ],
        StructurePattern.FEATURE_ADVANTAGE_BENEFIT: [
            ("Feature Overview", "What it is", "FAB - Feature"),
            ("Why It Matters", "Advantage over alternatives", "FAB - Advantage"),
            ("What You Gain", "Tangible benefit", "FAB - Benefit"),
            ("Proof Points", "Evidence", "FAB - Benefit"),
            ("Take Action", "CTA", "CTA"),
        ],
        StructurePattern.STORYBRAND: [
            ("The Character", "Your reader as hero", "StoryBrand - Character"),
            ("The Problem", "Villain they face", "StoryBrand - Problem"),
            ("The Guide", "You as trusted advisor", "StoryBrand - Guide"),
            ("The Plan", "Simple 3-step path", "StoryBrand - Plan"),
            ("The Call to Action", "Direct next step", "StoryBrand - CTA"),
            ("Success Story", "What winning looks like", "StoryBrand - Success"),
            ("Failure Stakes", "Cost of inaction", "StoryBrand - Failure"),
        ],
        StructurePattern.LISTICLE: [
            ("Introduction", "Hook + promise of value", "Hook"),
            ("Item 1", "First key point", "Body"),
            ("Item 2", "Second key point", "Body"),
            ("Item 3", "Third key point", "Body"),
            ("Item 4", "Fourth key point", "Body"),
            ("Item 5", "Fifth key point", "Body"),
            ("Conclusion + CTA", "Summary + next step", "CTA"),
        ],
        StructurePattern.HOW_TO: [
            ("Why This Matters", "Context and motivation", "Hook"),
            ("Prerequisites", "What you need first", "Setup"),
            ("Step 1", "First action", "Process"),
            ("Step 2", "Second action", "Process"),
            ("Step 3", "Third action", "Process"),
            ("Troubleshooting", "Common issues", "Support"),
            ("Next Steps", "Where to go from here", "CTA"),
        ],
        StructurePattern.CASE_STUDY: [
            ("The Challenge", "Client's problem", "STAR - Situation"),
            ("The Approach", "What we did", "STAR - Task/Action"),
            ("The Results", "Measurable outcomes", "STAR - Result"),
            ("Key Takeaways", "Lessons for reader", "Application"),
            ("Your Turn", "CTA for similar results", "CTA"),
        ],
        StructurePattern.THOUGHT_LEADERSHIP: [
            ("The Conventional Wisdom", "What everyone believes", "Hook"),
            ("Why It's Wrong", "Your contrarian insight", "Agitation"),
            ("The New Framework", "Your mental model", "Solution"),
            ("Evidence", "Data, examples, stories", "Proof"),
            ("Implications", "What this means for reader", "Application"),
            ("Challenge to Reader", "Call to think/act differently", "CTA"),
        ],
    }

    # Goal -> recommended structure patterns
    GOAL_STRUCTURE_MAP = {
        "educate": [StructurePattern.HOW_TO, StructurePattern.PROBLEM_SOLUTION, StructurePattern.LISTICLE],
        "persuade": [StructurePattern.PROBLEM_SOLUTION, StructurePattern.BEFORE_AFTER_BRIDGE, StructurePattern.STORYBRAND],
        "inform": [StructurePattern.PROBLEM_SOLUTION, StructurePattern.LISTICLE, StructurePattern.HOW_TO],
        "entertain": [StructurePattern.STORYBRAND, StructurePattern.LISTICLE, StructurePattern.THOUGHT_LEADERSHIP],
        "convert": [StructurePattern.BEFORE_AFTER_BRIDGE, StructurePattern.STORYBRAND, StructurePattern.PROBLEM_SOLUTION],
        "nurture": [StructurePattern.STORYBRAND, StructurePattern.BEFORE_AFTER_BRIDGE, StructurePattern.PROBLEM_SOLUTION],
        "reassure": [StructurePattern.CASE_STUDY, StructurePattern.PROBLEM_SOLUTION, StructurePattern.BEFORE_AFTER_BRIDGE],
        "warn": [StructurePattern.PROBLEM_SOLUTION, StructurePattern.THOUGHT_LEADERSHIP, StructurePattern.HOW_TO],
    }

    # Format -> recommended structure patterns
    FORMAT_STRUCTURE_MAP = {
        "blog": [StructurePattern.PROBLEM_SOLUTION, StructurePattern.HOW_TO, StructurePattern.LISTICLE, StructurePattern.THOUGHT_LEADERSHIP],
        "landing-page": [StructurePattern.BEFORE_AFTER_BRIDGE, StructurePattern.STORYBRAND, StructurePattern.PROBLEM_SOLUTION],
        "email": [StructurePattern.BEFORE_AFTER_BRIDGE, StructurePattern.PROBLEM_SOLUTION, StructurePattern.STORYBRAND],
        "social": [StructurePattern.LISTICLE, StructurePattern.THOUGHT_LEADERSHIP, StructurePattern.STORYBRAND],
        "case-study": [StructurePattern.CASE_STUDY, StructurePattern.STORYBRAND],
        "whitepaper": [StructurePattern.PROBLEM_SOLUTION, StructurePattern.THOUGHT_LEADERSHIP, StructurePattern.HOW_TO],
        "press-release": [StructurePattern.PROBLEM_SOLUTION, StructurePattern.CASE_STUDY],
        "video-script": [StructurePattern.HOW_TO, StructurePattern.STORYBRAND, StructurePattern.PROBLEM_SOLUTION],
    }

    def __init__(self):
        pass

    def run(self, brief: ContentBrief) -> Phase2Result:
        """
        Execute Phase 2: Generate outline from brief.

        Args:
            brief: Validated ContentBrief from Phase 1

        Returns:
            Phase2Result with ContentOutline
        """
        # Select structure pattern
        structure_pattern = self._select_structure_pattern(brief)
        persuasion_framework = self._select_persuasion_framework(brief, structure_pattern)

        # Create outline
        outline = ContentOutline(
            title=self._generate_title(brief),
            structure_pattern=structure_pattern,
            persuasion_framework=persuasion_framework,
            format=brief.format,
            goal=brief.goal,
        )

        # Generate hook
        outline.hook = self._generate_hook(brief, structure_pattern)

        # Generate sections
        outline.sections = self._generate_sections(brief, structure_pattern, persuasion_framework)

        # Generate CTA
        outline.cta = self._generate_cta(brief, structure_pattern)

        # Generate SEO elements
        outline.seo = self._generate_seo(brief, outline)

        # Set metadata
        outline.brief_id = getattr(brief, 'source_file', '') or 'brief-1'

        # Validate outline
        validation = self._validate_outline(outline, brief)

        # Generate rationale
        rationale = self._generate_rationale(brief, structure_pattern, persuasion_framework)

        return Phase2Result(
            outline=outline,
            validation=validation,
            structure_rationale=rationale,
        )

    def _select_structure_pattern(self, brief: ContentBrief) -> StructurePattern:
        """Select best structure pattern based on goal and format."""
        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
        format_val = brief.format.value if isinstance(brief.format, Format) else str(brief.format)

        # Check format-specific recommendations first
        if format_val in self.FORMAT_STRUCTURE_MAP:
            return self.FORMAT_STRUCTURE_MAP[format_val][0]

        # Fall back to goal-based
        if goal in self.GOAL_STRUCTURE_MAP:
            return self.GOAL_STRUCTURE_MAP[goal][0]

        return StructurePattern.PROBLEM_SOLUTION

    def _select_persuasion_framework(self, brief: ContentBrief,
                                      structure: StructurePattern) -> PersuasionFramework:
        """Select persuasion framework based on structure and goal."""
        framework_map = {
            StructurePattern.PROBLEM_SOLUTION: PersuasionFramework.PAS,
            StructurePattern.BEFORE_AFTER_BRIDGE: PersuasionFramework.BAB,
            StructurePattern.ATTENTION_INTEREST_DESIRE_ACTION: PersuasionFramework.AIDA,
            StructurePattern.FEATURE_ADVANTAGE_BENEFIT: PersuasionFramework.FAB,
            StructurePattern.STORYBRAND: PersuasionFramework.STORYBRAND,
            StructurePattern.LISTICLE: PersuasionFramework.FOUR_U,
            StructurePattern.HOW_TO: PersuasionFramework.SSA,
            StructurePattern.CASE_STUDY: PersuasionFramework.STORYBRAND,
            StructurePattern.THOUGHT_LEADERSHIP: PersuasionFramework.FOUR_PS,
        }
        return framework_map.get(structure, PersuasionFramework.PAS)

    def _generate_title(self, brief: ContentBrief) -> str:
        """Generate working title from brief."""
        audience = brief.audience.split(';')[0].split(',')[0].strip()[:40]
        angle = brief.angle[:60] if brief.angle else "Key Insights"
        return f"{angle} for {audience}"

    def _generate_hook(self, brief: ContentBrief, structure: StructurePattern) -> Hook:
        """Generate opening hook based on brief and structure."""
        hook_templates = {
            StructurePattern.PROBLEM_SOLUTION: {
                HookType.QUESTION: f"Struggling with {{topic}}? You're not alone.",
                HookType.PAIN_POINT: f"Most {{audience}} waste hours on {{problem}}.",
                HookType.STATISTIC: f"{{stat}}% of {{audience}} fail at {{topic}}.",
            },
            StructurePattern.BEFORE_AFTER_BRIDGE: {
                HookType.STORY: f"Three months ago, {{persona}} was {{before_state}}.",
                HookType.PAIN_POINT: f"{{audience}} used to {{before}}. Now they {{after}}.",
            },
            StructurePattern.LISTICLE: {
                HookType.DIRECT_BENEFIT: f"{{number}} ways to {{benefit}} without {{pain}}.",
                HookType.CURIOSITY_GAP: f"The {{number}} {{topic}} mistakes {{audience}} keep making.",
            },
            StructurePattern.THOUGHT_LEADERSHIP: {
                HookType.CONTRARIAN: f"Everyone says {{conventional_wisdom}}. They're wrong.",
                HookType.BOLD_CLAIM: f"{{bold_statement}} — and here's the proof.",
            },
        }

        templates = hook_templates.get(structure, hook_templates[StructurePattern.PROBLEM_SOLUTION])
        hook_type = HookType.QUESTION  # Default

        # Select hook type based on goal
        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
        if goal == "persuade":
            hook_type = HookType.PAIN_POINT
        elif goal == "convert":
            hook_type = HookType.DIRECT_BENEFIT
        elif goal == "entertain":
            hook_type = HookType.STORY
        elif goal == "warn":
            hook_type = HookType.STATISTIC

        template = templates.get(hook_type, list(templates.values())[0])

        return Hook(
            type=hook_type,
            text=template,
            rationale=f"Selected {hook_type.value} hook for {goal} goal with {structure.value} structure",
        )

    def _generate_sections(self, brief: ContentBrief,
                           structure: StructurePattern,
                           framework: PersuasionFramework) -> List[OutlineSection]:
        """Generate outline sections from structure template."""
        template = self.STRUCTURE_TEMPLATES.get(structure, self.STRUCTURE_TEMPLATES[StructurePattern.PROBLEM_SOLUTION])

        sections = []
        total_words = self._parse_target_words(brief.length)
        words_per_section = max(150, total_words // len(template)) if total_words else 300

        for i, (heading, purpose, framework_step) in enumerate(template):
            section = OutlineSection(
                heading=heading,
                level=2,
                key_points=self._generate_key_points(brief, heading, purpose, i),
                target_word_count=words_per_section,
                persuasion_element=purpose,
                evidence_needed=self._generate_evidence_needs(brief, heading, purpose),
                transition=self._generate_transition(i, len(template)),
            )
            sections.append(section)

        return sections

    def _generate_key_points(self, brief: ContentBrief, heading: str, purpose: str, index: int) -> List[str]:
        """Generate key points for a section."""
        points = []

        # Add angle-relevant point
        if brief.angle:
            points.append(f"Tie back to core angle: {brief.angle[:80]}")

        # Add primary keyword in first section for SEO
        if index == 0 and brief.primary_keyword:
            points.append(f"Introduce primary keyword: '{brief.primary_keyword}' naturally in opening")

        # Add goal-specific points
        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
        if goal == "educate":
            points.extend(["Explain the concept clearly", "Provide concrete example", "Address common misconception"])
        elif goal == "persuade":
            points.extend(["Present the argument", "Address objection", "Show evidence"])
        elif goal == "convert":
            points.extend(["Highlight benefit", "Reduce friction", "Add urgency"])

        return points[:4]  # Limit to 4 points per section

    def _generate_evidence_needs(self, brief: ContentBrief, heading: str, purpose: str) -> List[str]:
        """Generate evidence needs for a section."""
        needs = []

        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
        if "problem" in purpose.lower() or "pain" in purpose.lower():
            needs.append("Statistics on problem prevalence")
            needs.append("Anecdotal example")
        elif "solution" in purpose.lower() or "bridge" in purpose.lower():
            needs.append("Case study or testimonial")
            needs.append("Specific methodology steps")
        elif "proof" in purpose.lower() or "result" in purpose.lower():
            needs.append("Quantifiable metrics")
            needs.append("Before/after comparison")

        return needs[:3]

    def _generate_transition(self, index: int, total: int) -> str:
        """Generate transition to next section."""
        if index == total - 1:
            return "Now let's look at what to do next."
        return f"Building on that, let's explore the next piece."

    def _generate_cta(self, brief: ContentBrief, structure: StructurePattern) -> CTA:
        """Generate appropriate CTA based on brief and structure."""
        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)

        cta_map = {
            "educate": (CTAType.READ_NEXT, CTACommitmentLevel.LOW, "Read the full guide on [topic]"),
            "persuade": (CTAType.DOWNLOAD, CTACommitmentLevel.MEDIUM, "Download the comparison guide"),
            "inform": (CTAType.SUBSCRIBE, CTACommitmentLevel.LOW, "Subscribe for more insights"),
            "entertain": (CTAType.SHARE, CTACommitmentLevel.LOW, "Share if this resonated"),
            "convert": (CTAType.SIGN_UP, CTACommitmentLevel.HIGH, "Start your free trial"),
            "nurture": (CTAType.READ_NEXT, CTACommitmentLevel.LOW, "Read the next article in this series"),
            "reassure": (CTAType.CONTACT, CTACommitmentLevel.MEDIUM, "Book a consultation"),
            "warn": (CTAType.DOWNLOAD, CTACommitmentLevel.MEDIUM, "Get the risk assessment checklist"),
        }

        cta_type, commitment, default_text = cta_map.get(goal, (CTAType.READ_NEXT, CTACommitmentLevel.LOW, "Learn more"))

        return CTA(
            type=cta_type,
            text=default_text,
            commitment_level=commitment,
            position="end",
        )

    def _generate_seo(self, brief: ContentBrief, outline: ContentOutline) -> SEOElements:
        """Generate SEO elements."""
        # Extract potential keywords from brief
        primary = self._extract_primary_keyword(brief)

        return SEOElements(
            primary_keyword=primary,
            secondary_keywords=self._extract_secondary_keywords(brief),
            meta_title=f"{outline.title} | {primary}"[:60],
            meta_description=self._generate_meta_description(brief, outline)[:155],
            target_word_count=self._parse_target_words(brief.length) or 1000,
            heading_structure=outline.get_heading_structure(),
            search_intent=self._infer_search_intent(brief),
        )

    def _extract_primary_keyword(self, brief: ContentBrief) -> str:
        """Extract primary keyword from brief."""
        # Use explicit primary_keyword if provided
        if brief.primary_keyword:
            return brief.primary_keyword
        # Simple extraction from angle and audience
        angle = brief.angle.lower()
        words = angle.split()
        # Filter out stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'one', 'that', 'this', 'how', 'why', 'what', 'who'}
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        return keywords[0] if keywords else "topic"

    def _extract_secondary_keywords(self, brief: ContentBrief) -> List[str]:
        """Extract secondary keywords."""
        # Simplified - in production would use keyword research
        return ["guide", "tips", "strategy", "best practices"]

    def _generate_meta_description(self, brief: ContentBrief, outline: ContentOutline) -> str:
        """Generate meta description."""
        return f"Discover {brief.angle[:80]}. Learn actionable insights for {brief.audience[:50]}."

    def _infer_search_intent(self, brief: ContentBrief) -> str:
        """Infer search intent from goal."""
        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
        intent_map = {
            "educate": "informational",
            "inform": "informational",
            "persuade": "commercial",
            "convert": "transactional",
            "nurture": "informational",
            "entertain": "informational",
            "reassure": "commercial",
            "warn": "informational",
        }
        return intent_map.get(goal, "informational")

    def _parse_target_words(self, length: str) -> int:
        """Parse target word count from length string."""
        import re
        if not length:
            return 1200
        # Find first number
        match = re.search(r'(\d+[,-]?\d*)', length.replace(',', ''))
        if match:
            return int(match.group(1))
        return 1200

    def _validate_outline(self, outline: ContentOutline, brief: ContentBrief) -> ValidationGateResult:
        """Validate outline against brief requirements."""
        issues = []
        metrics = {}

        # Check title
        if not outline.title:
            issues.append({
                "code": "MISSING_TITLE",
                "message": "Outline missing title",
                "severity": "error",
                "field": "title",
            })

        # Check hook
        if not outline.hook.text:
            issues.append({
                "code": "MISSING_HOOK",
                "message": "Outline missing hook text",
                "severity": "error",
                "field": "hook",
            })

        # Check sections
        if not outline.sections:
            issues.append({
                "code": "NO_SECTIONS",
                "message": "Outline has no sections",
                "severity": "error",
                "field": "sections",
            })
        else:
            metrics["section_count"] = len(outline.sections)
            total_words = sum(s.target_word_count or 0 for s in outline.sections)
            metrics["estimated_word_count"] = total_words

            # Check word count alignment
            target = self._parse_target_words(brief.length)
            if target > 0:
                diff_pct = abs(total_words - target) / target * 100
                if diff_pct > 30:
                    issues.append({
                        "code": "WORD_COUNT_MISMATCH",
                        "message": f"Estimated word count ({total_words}) differs from target ({target}) by {diff_pct:.0f}%",
                        "severity": "warning",
                        "field": "sections",
                        "suggestion": "Adjust section target_word_counts to match brief length",
                    })

        # Check CTA
        if not outline.cta.text:
            issues.append({
                "code": "MISSING_CTA",
                "message": "Outline missing CTA text",
                "severity": "warning",
                "field": "cta",
            })

        # Check SEO
        if not outline.seo.primary_keyword:
            issues.append({
                "code": "MISSING_PRIMARY_KEYWORD",
                "message": "No primary keyword defined for SEO",
                "severity": "warning",
                "field": "seo",
            })

        passed = len([i for i in issues if i["severity"] == "error"]) == 0

        return ValidationGateResult(
            gate=2,
            gate_name="structure-validation",
            passed=passed,
            issues=issues,
            metrics=metrics,
        )

    def _generate_rationale(self, brief: ContentBrief, structure: StructurePattern,
                            framework: PersuasionFramework) -> str:
        """Generate human-readable rationale for structure choices."""
        goal = brief.goal.value if isinstance(brief.goal, Goal) else str(brief.goal)
        format_val = brief.format.value if isinstance(brief.format, Format) else str(brief.format)

        return (
            f"Selected {structure.value} structure for {goal} goal in {format_val} format. "
            f"Applied {framework.value} persuasion framework. "
            f"Structure follows {len(self.STRUCTURE_TEMPLATES.get(structure, []))} sections "
            f"optimized for {goal} outcomes."
        )


def run_outline(brief: ContentBrief) -> Phase2Result:
    """Convenience function to run Phase 2."""
    phase = OutlinePhase()
    return phase.run(brief)


# Module-level aliases for templates and mappings
STRUCTURE_TEMPLATES = OutlinePhase.STRUCTURE_TEMPLATES
GOAL_STRUCTURE_MAP = OutlinePhase.GOAL_STRUCTURE_MAP
FORMAT_STRUCTURE_MAP = OutlinePhase.FORMAT_STRUCTURE_MAP

__all__ = [
    "Phase2Result",
    "OutlinePhase",
    "run_outline",
    "STRUCTURE_TEMPLATES",
    "GOAL_STRUCTURE_MAP",
    "FORMAT_STRUCTURE_MAP",
]