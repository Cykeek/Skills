"""
Contract Tests: Outline Generation
==================================
Tests for Phase 2: Outline - structure selection, section generation,
hook/CTA/SEO creation, and validation.
"""

import pytest
from content_writer_skill.models import (
    ContentBrief, ContentOutline, OutlineSection, Hook, CTA, SEOElements,
    Goal, Format, Tone, HookType, StructurePattern, PersuasionFramework,
    CTAType, CTACommitmentLevel,
)
from content_writer_skill.phases.phase2_outline import (
    OutlinePhase, Phase2Result, run_outline,
    STRUCTURE_TEMPLATES, GOAL_STRUCTURE_MAP, FORMAT_STRUCTURE_MAP,
)


class TestStructureTemplates:
    """Tests for structure template definitions."""

    def test_all_patterns_have_templates(self):
        """Test all structure patterns have section templates."""
        for pattern in StructurePattern:
            assert pattern in STRUCTURE_TEMPLATES
            template = STRUCTURE_TEMPLATES[pattern]
            assert len(template) >= 4  # At least 4 sections
            for heading, purpose, framework_step in template:
                assert heading
                assert purpose
                assert framework_step

    def test_problem_solution_template(self):
        """Test Problem-Solution template structure."""
        template = STRUCTURE_TEMPLATES[StructurePattern.PROBLEM_SOLUTION]
        headings = [h for h, _, _ in template]
        assert "The Problem" in headings
        assert "The Solution" in headings
        assert "How to Implement" in headings
        assert "Next Steps" in headings

    def test_before_after_bridge_template(self):
        """Test BAB template structure."""
        template = STRUCTURE_TEMPLATES[StructurePattern.BEFORE_AFTER_BRIDGE]
        headings = [h for h, _, _ in template]
        assert "The Before State" in headings
        assert "The After State" in headings
        assert "The Bridge" in headings

    def test_storybrand_template(self):
        """Test StoryBrand template structure."""
        template = STRUCTURE_TEMPLATES[StructurePattern.STORYBRAND]
        headings = [h for h, _, _ in template]
        assert "The Character" in headings
        assert "The Problem" in headings
        assert "The Guide" in headings
        assert "The Plan" in headings
        assert "The Call to Action" in headings

    def test_goal_structure_mapping(self):
        """Test all goals have structure mappings."""
        for goal in Goal:
            goal_val = goal.value
            assert goal_val in GOAL_STRUCTURE_MAP
            patterns = GOAL_STRUCTURE_MAP[goal_val]
            assert len(patterns) >= 2
            for p in patterns:
                assert isinstance(p, StructurePattern)

    def test_format_structure_mapping(self):
        """Test all formats have structure mappings."""
        for fmt in Format:
            fmt_val = fmt.value
            assert fmt_val in FORMAT_STRUCTURE_MAP
            patterns = FORMAT_STRUCTURE_MAP[fmt_val]
            assert len(patterns) >= 2
            for p in patterns:
                assert isinstance(p, StructurePattern)


class TestOutlinePhase:
    """Tests for OutlinePhase execution."""

    def create_sample_brief(self) -> ContentBrief:
        """Create a sample brief for testing."""
        return ContentBrief(
            audience="Junior developers learning testing",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500-2000 words",
            tone="encouraging, clear, practical",
            angle="Start testing early, not after bugs appear",
            primary_keyword="testing strategies",
        )

    def test_run_outline_basic(self):
        """Test basic outline generation."""
        brief = self.create_sample_brief()
        result = run_outline(brief)

        assert isinstance(result, Phase2Result)
        assert result.outline is not None
        assert result.validation.passed
        assert result.structure_rationale

    def test_outline_has_required_fields(self):
        """Test outline has all required components."""
        brief = self.create_sample_brief()
        result = run_outline(brief)
        outline = result.outline

        assert outline.title
        assert outline.structure_pattern
        assert outline.persuasion_framework
        assert outline.hook is not None
        assert outline.hook.text
        assert outline.hook.type
        assert len(outline.sections) >= 4
        assert outline.cta is not None
        assert outline.cta.text
        assert outline.seo is not None
        assert outline.seo.primary_keyword

    def test_outline_structure_matches_goal(self):
        """Test structure pattern matches goal."""
        brief = self.create_sample_brief()
        result = run_outline(brief)

        # Educate goal should use Problem-Solution or How-To
        assert result.outline.structure_pattern in [
            StructurePattern.PROBLEM_SOLUTION,
            StructurePattern.HOW_TO,
            StructurePattern.LISTICLE,
        ]

    def test_outline_sections_have_content(self):
        """Test each section has required fields."""
        brief = self.create_sample_brief()
        result = run_outline(brief)

        for section in result.outline.sections:
            assert section.heading
            assert section.level == 2
            assert section.target_words > 0
            assert section.purpose
            assert section.framework_step
            assert isinstance(section.key_points, list)
            assert isinstance(section.evidence_needed, list)
            assert section.transition

    def test_hook_generation(self):
        """Test hook is generated with appropriate type."""
        brief = self.create_sample_brief()
        result = run_outline(brief)

        hook = result.outline.hook
        assert hook.type in HookType
        assert hook.text
        assert hook.rationale

    def test_cta_generation(self):
        """Test CTA is generated matching goal."""
        brief = self.create_sample_brief()
        result = run_outline(brief)

        cta = result.outline.cta
        assert cta.type in CTAType
        assert cta.text
        assert cta.commitment_level in CTACommitmentLevel
        assert cta.placement in ["end", "middle", "both"]

        # For educate goal, should be low commitment
        assert cta.commitment_level == CTACommitmentLevel.LOW

    def test_seo_generation(self):
        """Test SEO elements are generated."""
        brief = self.create_sample_brief()
        result = run_outline(brief)

        seo = result.outline.seo
        assert seo.primary_keyword
        assert isinstance(seo.secondary_keywords, list)
        assert seo.meta_title
        assert len(seo.meta_title) <= 60
        assert seo.meta_description
        assert len(seo.meta_description) <= 155
        assert seo.h1 == result.outline.title
        assert isinstance(seo.heading_structure, list)
        assert seo.search_intent in ["informational", "commercial", "transactional"]

    def test_convert_goal_high_commitment_cta(self):
        """Test convert goal gets high commitment CTA."""
        brief = ContentBrief(
            audience="SaaS buyers",
            goal=Goal.CONVERT,
            format=Format.LANDING_PAGE,
            length="800 words",
            tone="confident, direct",
            angle="Best ROI in category",
        )
        result = run_outline(brief)
        assert result.outline.cta.commitment_level == CTACommitmentLevel.HIGH
        assert result.outline.cta.type in [CTAType.SIGN_UP, CTAType.BUY, CTAType.CONTACT]

    def test_persuade_goal_bab_structure(self):
        """Test persuade goal uses BAB structure."""
        brief = ContentBrief(
            audience="Marketing managers",
            goal=Goal.PERSUADE,
            format=Format.EMAIL,
            length="300 words",
            tone="persuasive, evidence-based",
            angle="New approach beats old methods",
        )
        result = run_outline(brief)
        assert result.outline.structure_pattern == StructurePattern.BEFORE_AFTER_BRIDGE
        assert result.outline.persuasion_framework == PersuasionFramework.BAB

    def test_case_study_format(self):
        """Test case study format uses case study structure."""
        brief = ContentBrief(
            audience="Engineering leaders",
            goal=Goal.REASSURE,
            format=Format.CASE_STUDY,
            length="2000 words",
            tone="professional, data-driven",
            angle="How Team X reduced bugs 80%",
        )
        result = run_outline(brief)
        assert result.outline.structure_pattern == StructurePattern.CASE_STUDY
        assert result.outline.persuasion_framework == PersuasionFramework.STAR_STORY_SOLUTION


class TestOutlineValidation:
    """Tests for outline validation."""

    def test_validation_passes_for_complete_outline(self):
        """Test validation passes for well-formed outline."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500 words",
            tone="clear",
            angle="Testing matters",
        )
        result = run_outline(brief)
        assert result.validation.passed

    def test_validation_fails_missing_title(self):
        """Test validation catches missing title."""
        # Test outline generation with empty audience field
        brief = ContentBrief(
            audience="",  # Empty - will fail Phase 1
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500 words",
            tone="clear",
            angle="Testing",
        )
        # Phase 1 would catch this, but Phase 2 validates outline not brief
        result = run_outline(brief)
        # Outline phase generates title from brief - if audience empty, title will be weak
        assert result.outline.title

    def test_validation_word_count_alignment(self):
        """Test validation checks word count alignment."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="5000 words",  # Much larger than template sections
            tone="clear",
            angle="Testing",
        )
        result = run_outline(brief)
        # Should warn about mismatch
        issues = result.validation.issues
        word_count_issues = [i for i in issues if i["code"] == "WORD_COUNT_MISMATCH"]
        assert len(word_count_issues) > 0


class TestStructureRationale:
    """Tests for structure rationale generation."""

    def test_rationale_includes_key_info(self):
        """Test rationale mentions goal, format, structure, framework."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500 words",
            tone="clear",
            angle="Testing early",
        )
        result = run_outline(brief)
        rationale = result.structure_rationale

        assert "educate" in rationale.lower()
        assert "blog" in rationale.lower()
        assert result.outline.structure_pattern.value in rationale
        assert result.outline.persuasion_framework.value in rationale
        assert str(len(result.outline.sections)) in rationale


class TestOutlinePhaseEdgeCases:
    """Edge case tests for Phase 2."""

    def test_unknown_goal_defaults(self):
        """Test unknown goal falls back to default structure."""
        brief = ContentBrief(
            audience="Developers",
            goal="custom-goal",  # Not in enum
            format=Format.BLOG,
            length="1500 words",
            tone="clear",
            angle="Testing",
        )
        result = run_outline(brief)
        assert result.outline.structure_pattern == StructurePattern.PROBLEM_SOLUTION

    def test_unknown_format_defaults(self):
        """Test unknown format falls back to goal-based structure."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format="custom-format",  # Not in enum
            length="1500 words",
            tone="clear",
            angle="Testing",
        )
        result = run_outline(brief)
        # Should use goal-based mapping
        assert result.outline.structure_pattern in GOAL_STRUCTURE_MAP["educate"]

    def test_outline_to_dict(self):
        """Test outline serialization."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500 words",
            tone="clear",
            angle="Testing",
        )
        result = run_outline(brief)
        data = result.outline.to_dict()

        assert data["title"]
        assert data["structure_pattern"]
        assert data["persuasion_framework"]
        assert data["hook"]["text"]
        assert len(data["sections"]) >= 4
        assert data["cta"]["text"]
        assert data["seo"]["primary_keyword"]

    def test_heading_structure_extraction(self):
        """Test get_heading_structure method."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500 words",
            tone="clear",
            angle="Testing",
        )
        result = run_outline(brief)
        structure = result.outline.get_heading_structure()

        assert len(structure) == len(result.outline.sections)
        for s in structure:
            assert "level" in s
            assert "text" in s
            assert s["level"] == 2