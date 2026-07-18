"""
Contract Tests - Content Brief Validation
=========================================
Tests for ContentBrief model and Phase 1 validation.
"""

import pytest
import json
from content_writer_skill.models import ContentBrief, Goal, Format, Tone
from content_writer_skill.models.brief import BRIEF_TEMPLATES, apply_template, infer_missing_fields
from content_writer_skill.phases.phase1_discover import DiscoverAlignPhase, run_discover_align


class TestContentBrief:
    """Tests for ContentBrief model."""

    def test_brief_creation_minimal(self):
        """Test creating brief with minimal required fields."""
        brief = ContentBrief(
            audience="Software engineers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1200-1800 words",
            tone="confident, practical",
            angle="Testing improves code quality"
        )
        assert brief.audience == "Software engineers"
        assert brief.goal == Goal.EDUCATE
        assert brief.format == Format.BLOG

    def test_brief_from_dict(self):
        """Test creating brief from dictionary."""
        data = {
            "audience": "Marketing managers",
            "goal": "persuade",
            "format": "landing-page",
            "length": "800-1200 words",
            "tone": "persuasive, urgent",
            "angle": "Our tool saves 10 hours/week"
        }
        brief = ContentBrief.from_dict(data)
        assert brief.audience == "Marketing managers"
        assert brief.goal == Goal.PERSUADE
        assert brief.format == Format.LANDING_PAGE

    def test_brief_to_dict(self):
        """Test brief serialization."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.INFORM,
            format=Format.EMAIL,
            length="300-500 words",
            tone="concise, friendly",
            angle="New feature announcement"
        )
        data = brief.to_dict()
        assert data["audience"] == "Developers"
        assert data["goal"] == "inform"
        assert data["format"] == "email"

    def test_brief_json_roundtrip(self):
        """Test JSON serialization roundtrip."""
        brief = ContentBrief(
            audience="CTOs",
            goal=Goal.CONVERT,
            format=Format.CASE_STUDY,
            length="2000-3000 words",
            tone="authoritative, evidence-based",
            angle="Migration reduces risk"
        )
        json_str = brief.to_json()
        brief2 = ContentBrief.from_json(json_str)
        assert brief.audience == brief2.audience
        assert brief.goal == brief2.goal
        assert brief.angle == brief2.angle

    def test_get_missing_fields(self):
        """Test detection of missing required fields."""
        brief = ContentBrief()
        missing = brief.get_missing_fields()
        assert "audience" in missing
        assert "goal" in missing
        assert "format" in missing
        assert "length" in missing
        assert "tone" in missing
        assert "angle" in missing

    def test_brief_with_optional_fields(self):
        """Test brief with all optional fields populated."""
        brief = ContentBrief(
            audience="Product managers",
            goal=Goal.NURTURE,
            format=Format.SOCIAL,
            length="280 characters",
            tone="warm, personal",
            angle="Small wins compound",
            primary_keyword="productivity tips",
            secondary_keywords=["time management", "focus", "habits"],
            brand_voice="Helpful mentor",
            cta_type="read-next",
            metadata={"campaign": "q4-productivity"}
        )
        assert brief.primary_keyword == "productivity tips"
        assert "time management" in brief.secondary_keywords
        assert brief.metadata["campaign"] == "q4-productivity"


class TestBriefTemplates:
    """Tests for brief template system."""

    def test_all_templates_exist(self):
        """Test that all 8 format templates are defined."""
        expected_formats = [
            "blog", "landing-page", "email", "social",
            "case-study", "whitepaper", "press-release", "video-script"
        ]
        for fmt in expected_formats:
            assert fmt in BRIEF_TEMPLATES
            template = BRIEF_TEMPLATES[fmt]
            assert "length" in template
            assert "tone" in template
            assert "structure_hint" in template

    def test_apply_blog_template(self):
        """Test applying blog template."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="",  # Will be filled by template
            tone="",    # Will be filled by template
            angle="Testing strategies"
        )
        result = apply_template(brief, "blog")
        assert result.length != ""
        assert result.tone != ""
        assert result.template_used == "blog"
        assert "Applied 'blog' template" in result.assumptions[0]

    def test_apply_landing_page_template(self):
        """Test applying landing page template."""
        brief = ContentBrief(
            audience="SaaS buyers",
            goal=Goal.CONVERT,
            format=Format.LANDING_PAGE,
            length="",
            tone="",
            angle="Best ROI"
        )
        result = apply_template(brief, "landing-page")
        assert result.length != ""
        assert result.tone != ""
        assert result.template_used == "landing-page"

    def test_apply_template_preserves_existing(self):
        """Test template doesn't override explicitly set fields."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="5000 words",  # Explicitly set
            tone="formal, academic",  # Explicitly set
            angle="Deep dive"
        )
        result = apply_template(brief, "blog")
        assert result.length == "5000 words"
        assert result.tone == "formal, academic"

    def test_infer_missing_fields(self):
        """Test inferring missing fields from context."""
        brief = ContentBrief(
            audience="Beginners",
            goal=Goal.EDUCATE,
            format=Format.HOW_TO,
            length="1000-1500 words",
            tone="",
            angle=""  # Will be inferred from goal+format
        )
        result = infer_missing_fields(brief)
        assert result.tone != ""
        assert result.angle != ""
        assert len(result.assumptions) > 0


class TestPhase1DiscoverAlign:
    """Tests for Phase 1: Discover & Align."""

    def test_phase1_success(self):
        """Test successful Phase 1 execution."""
        input_data = {
            "audience": "Junior developers",
            "goal": "educate",
            "format": "blog",
            "length": "1500-2000 words",
            "tone": "encouraging, clear",
            "angle": "Start testing early"
        }
        result = run_discover_align(input_data)
        assert result.brief is not None
        assert result.validation.passed
        assert result.template_applied == "blog"

    def test_phase1_strict_mode_missing_fields(self):
        """Test strict mode fails on missing fields."""
        input_data = {
            "audience": "Developers",
            "goal": "educate",
            # Missing format, length, tone, angle
        }
        with pytest.raises(ValueError, match="Missing required fields"):
            run_discover_align(input_data, strict_mode=True)

    def test_phase1_non_strict_infers(self):
        """Test non-strict mode infers missing fields."""
        input_data = {
            "audience": "Developers",
            "goal": "educate",
            "format": "blog",
            # Missing length, tone, angle
        }
        result = run_discover_align(input_data, strict_mode=False)
        assert result.brief.length != ""
        assert result.brief.tone != ""
        assert result.brief.angle != ""
        assert len(result.assumptions) > 0

    def test_phase1_invalid_length_format(self):
        """Test validation catches invalid length format."""
        input_data = {
            "audience": "Developers",
            "goal": "educate",
            "format": "blog",
            "length": "about a thousand words",  # Invalid format
            "tone": "clear",
            "angle": "Testing"
        }
        result = run_discover_align(input_data)
        assert not result.validation.passed
        issues = result.validation.issues
        assert any(i["code"] == "INVALID_LENGTH_FORMAT" for i in issues)

    def test_phase1_questions_for_missing(self):
        """Test clarifying questions generated for missing fields."""
        input_data = {
            "audience": "Developers",
            "goal": "educate",
        }
        result = run_discover_align(input_data, strict_mode=False)
        questions = result.questions_needed
        assert any("format" in q.lower() for q in questions)
        assert any("length" in q.lower() for q in questions)
        assert any("tone" in q.lower() for q in questions)
        assert any("angle" in q.lower() for q in questions)

    def test_phase1_load_from_file(self, tmp_path):
        """Test loading brief from JSON file."""
        brief_data = {
            "audience": "Designers",
            "goal": "persuade",
            "format": "landing-page",
            "length": "800 words",
            "tone": "compelling",
            "angle": "Design systems scale"
        }
        filepath = tmp_path / "brief.json"
        filepath.write_text(json.dumps(brief_data))

        from content_writer_skill.phases.phase1_discover import load_brief_from_file
        brief = load_brief_from_file(str(filepath))
        assert brief.audience == "Designers"
        assert brief.format == Format.LANDING_PAGE


class TestPhase1EdgeCases:
    """Edge case tests for Phase 1."""

    def test_empty_audience(self):
        """Test handling of empty audience."""
        input_data = {
            "audience": "  ",
            "goal": "educate",
            "format": "blog",
            "length": "1000 words",
            "tone": "clear",
            "angle": "Testing"
        }
        result = run_discover_align(input_data)
        assert not result.validation.passed
        assert any(i["code"] == "MISSING_FIELD" and i["field"] == "audience" for i in result.validation.issues)

    def test_unknown_goal_warning(self):
        """Test unknown goal generates warning not error."""
        input_data = {
            "audience": "Developers",
            "goal": "custom-goal",  # Not in enum
            "format": "blog",
            "length": "1000 words",
            "tone": "clear",
            "angle": "Testing"
        }
        result = run_discover_align(input_data)
        issues = result.validation.issues
        assert any(i["code"] == "INVALID_GOAL" for i in issues)
        # Should be warning, not error
        assert all(i["severity"] == "warning" for i in issues if i["code"] == "INVALID_GOAL")

    def test_unknown_format_warning(self):
        """Test unknown format generates warning."""
        input_data = {
            "audience": "Developers",
            "goal": "educate",
            "format": "custom-format",
            "length": "1000 words",
            "tone": "clear",
            "angle": "Testing"
        }
        result = run_discover_align(input_data)
        issues = result.validation.issues
        assert any(i["code"] == "INVALID_FORMAT" for i in issues)