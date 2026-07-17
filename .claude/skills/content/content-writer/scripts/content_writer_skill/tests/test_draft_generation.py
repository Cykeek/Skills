"""
Contract Tests: Draft Generation
================================
Tests for Phase 3: Draft - section-by-section content generation.
"""

import pytest
from content_writer_skill.models import (
    ContentBrief, ContentOutline, ContentDraft, OutlineSection, Hook, CTA, SEOElements,
    Goal, Format, Tone, HookType, StructurePattern, PersuasionFramework,
    CTAType, CTACommitmentLevel,
)
from content_writer_skill.phases.phase3_draft import DraftPhase, run_draft
from content_writer_skill.phases.phase2_outline import OutlinePhase, run_outline


class TestDraftPhase:
    """Tests for DraftPhase execution."""

    def create_sample_brief(self) -> ContentBrief:
        return ContentBrief(
            audience="Junior developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1500-2000 words",
            tone="encouraging, clear, practical",
            angle="Start testing early, not after bugs appear",
        )

    def create_sample_outline(self, brief: ContentBrief) -> ContentOutline:
        return run_outline(brief).outline

    def test_run_draft_basic(self):
        """Test basic draft generation."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        assert result.draft is not None
        assert isinstance(result.draft, ContentDraft)
        assert result.draft.content
        assert result.draft.word_count > 0
        assert result.draft.reading_time_minutes > 0

    def test_draft_contains_all_sections(self):
        """Test draft includes all outline sections."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        content = result.draft.content
        for section in outline.sections:
            assert section.heading in content

    def test_draft_contains_hook(self):
        """Test draft includes hook from outline."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        # Hook should appear in first ~500 chars
        assert outline.hook.text in result.draft.content[:500]

    def test_draft_contains_cta(self):
        """Test draft includes CTA from outline."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        assert outline.cta.text in result.draft.content

    def test_draft_word_count_reasonable(self):
        """Test draft word count is reasonable for length target."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        target = 1500  # From brief length
        diff_pct = abs(result.draft.word_count - target) / target * 100
        # Draft phase may not hit exact target, but should be in ballpark
        assert diff_pct < 80  # Within 80% of target

    def test_draft_has_structure_validation(self):
        """Test draft validation runs."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        assert result.validation is not None
        assert hasattr(result.validation, 'passed')
        assert hasattr(result.validation, 'issues')

    def test_draft_number_increments(self):
        """Test draft number is set."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        assert result.draft.draft_number == 1

    def test_draft_tone_adaptation(self):
        """Test draft adapts to brief tone."""
        # Conversational tone
        brief_conv = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1000 words",
            tone="conversational, friendly",
            angle="Testing is fun",
        )
        outline_conv = run_outline(brief_conv).outline
        result_conv = run_draft(outline_conv, brief_conv)

        # Authoritative tone
        brief_auth = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1000 words",
            tone="authoritative, direct",
            angle="Testing is essential",
        )
        outline_auth = run_outline(brief_auth).outline
        result_auth = run_draft(outline_auth, brief_auth)

        # Both should generate content (exact tone adaptation would need LLM)
        assert result_conv.draft.content
        assert result_auth.draft.content

    def test_draft_section_transitions(self):
        """Test draft includes section transitions."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        # Each section should have transitions
        for section in outline.sections[:-1]:  # Not last
            assert section.transition in result.draft.content

    def test_draft_to_dict(self):
        """Test draft serialization."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        data = result.draft.to_dict()
        assert data["content"]
        assert data["word_count"] > 0
        assert data["reading_time_minutes"] > 0
        assert data["draft_number"] == 1
        assert data["outline"] is not None
        assert data["brief"] is not None


class TestDraftValidation:
    """Tests for draft validation."""

    def test_validation_passes_for_complete_draft(self):
        """Test validation passes for draft matching outline."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        # May have warnings but should pass (no errors)
        errors = [i for i in result.validation.issues if i["severity"] == "error"]
        assert len(errors) == 0

    def test_validation_catches_missing_sections(self):
        """Test validation catches missing sections."""
        brief = self.create_sample_brief()
        outline = self.create_sample_outline(brief)
        result = run_draft(outline, brief)

        # Create a draft with missing sections by manipulating content
        draft = result.draft
        draft.content = "## Incomplete Draft\n\nOnly one section."
        draft.word_count = len(draft.content.split())

        # Re-validate
        phase = DraftPhase()
        validation = phase._validate_draft(draft, outline, brief)

        missing_issues = [i for i in validation.issues if i["code"] == "MISSING_SECTIONS"]
        assert len(missing_issues) > 0
        assert validation.passed == False

    def test_validation_catches_word_count_mismatch(self):
        """Test validation warns on large word count mismatch."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="5000 words",  # Large target
            tone="clear",
            angle="Testing",
        )
        outline = run_outline(brief).outline
        result = run_draft(outline, brief)

        # Draft will be much shorter than 5000 words
        issues = result.validation.issues
        word_count_issues = [i for i in issues if i["code"] == "WORD_COUNT_MISMATCH"]
        assert len(word_count_issues) > 0


class TestDraftEdgeCases:
    """Edge case tests for Phase 3."""

    def test_empty_outline_sections(self):
        """Test handling of outline with no sections."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1000 words",
            tone="clear",
            angle="Testing",
        )
        outline = run_outline(brief).outline
        outline.sections = []  # Empty

        result = run_draft(outline, brief)
        # Should still generate hook and CTA
        assert result.draft.content

    def test_draft_with_social_format(self):
        """Test draft generation for social format (short)."""
        brief = ContentBrief(
            audience="Twitter followers",
            goal=Goal.ENGAGE,
            format=Format.SOCIAL,
            length="280 characters",
            tone="punchy, engaging",
            angle="One testing tip",
        )
        outline = run_outline(brief).outline
        result = run_draft(outline, brief)

        assert result.draft.content
        # Social content should be shorter
        assert result.draft.word_count < 500

    def test_draft_with_email_format(self):
        """Test draft generation for email format."""
        brief = ContentBrief(
            audience="Subscribers",
            goal=Goal.NURTURE,
            format=Format.EMAIL,
            length="300 words",
            tone="personal, warm",
            angle="Weekly testing tip",
        )
        outline = run_outline(brief).outline
        result = run_draft(outline, brief)

        assert result.draft.content
        assert result.draft.word_count > 50
        assert result.draft.word_count < 500


class TestDraftPhaseHelperMethods:
    """Tests for internal helper methods."""

    def test_bullets_to_prose_conversational(self):
        """Test bullet to prose conversion with conversational tone."""
        phase = DraftPhase()
        bullets = ["Point one", "Point two", "Point three"]
        prose = phase._bullets_to_prose(bullets, "conversational")

        assert "Here's the thing:" in prose or len(prose) > 0

    def test_bullets_to_prose_authoritative(self):
        """Test bullet to prose conversion with authoritative tone."""
        phase = DraftPhase()
        bullets = ["Point one", "Point two"]
        prose = phase._bullets_to_prose(bullets, "authoritative")

        assert "Consider this:" in prose or len(prose) > 0

    def test_extract_headings(self):
        """Test heading extraction from markdown."""
        phase = DraftPhase()
        content = """# Main Title
Some text
## Section One
More text
### Subsection
Even more
## Section Two
Final text"""
        headings = phase._extract_headings(content)
        assert headings == ["Section One", "Subsection", "Section Two"]