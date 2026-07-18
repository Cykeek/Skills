"""
Contract Tests: SEO Audit Validation
=====================================
Tests for Gate 4 - SEO/Conversion validation.
"""

import pytest
from content_writer_skill.validation import SEOValidator
from content_writer_skill.models import (
    ContentBrief, ContentOutline, ContentDraft, OutlineSection, Hook, CTA, SEOElements,
    Goal, Format, HookType, StructurePattern, PersuasionFramework, CTAType, CTACommitmentLevel,
)
from content_writer_skill.models.validation_results import SEOAudit


class TestSEOValidator:
    """Tests for SEOValidator."""

    def create_brief(self, **kwargs) -> ContentBrief:
        defaults = {
            "audience": "Developers",
            "goal": Goal.EDUCATE,
            "format": Format.BLOG,
            "length": "1500 words",
            "tone": "clear, practical",
            "angle": "Start testing early to catch bugs sooner",
        }
        defaults.update(kwargs)
        return ContentBrief(**defaults)

    def create_outline(self, brief: ContentBrief, primary_kw: str = "testing") -> ContentOutline:
        sections = [
            OutlineSection(heading="Why Testing Matters", level=2, key_points=["Bugs cost more later", "Early testing saves time"], target_words=400),
            OutlineSection(heading="How to Start", level=2, key_points=["Write first test", "Run it", "Repeat"], target_words=400),
            OutlineSection(heading="Common Patterns", level=2, key_points=["Unit tests", "Integration tests", "E2E tests"], target_words=400),
        ]
        return ContentOutline(
            title="Early Testing Guide for Developers",
            structure_pattern=StructurePattern.PROBLEM_SOLUTION,
            persuasion_framework=PersuasionFramework.PAS,
            sections=sections,
            hook=Hook(type=HookType.PAIN_POINT, text="Most developers skip testing until bugs appear."),
            cta=CTA(type=CTAType.READ_NEXT, text="Read the full testing guide", commitment_level=CTACommitmentLevel.LOW),
            seo=SEOElements(primary_keyword=primary_kw, secondary_keywords=["unit testing", "TDD", "bugs"]),
        )

    def create_draft(self, content: str, brief: ContentBrief, outline: ContentOutline) -> ContentDraft:
        return ContentDraft(
            content=content,
            outline=outline,
            brief=brief,
            draft_number=1,
        )

    def test_audit_passes_well_optimized_content(self):
        """Test audit passes for well-optimized content."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# Early Testing Guide for Developers

Most developers skip testing until bugs appear. This costs time and money.

## Why Testing Matters

Testing early catches bugs when they're cheap to fix. A bug found in production costs 100x more than one caught in development.

## How to Start

Write your first test today. Run it. Watch it pass. Then write another.

## Common Patterns

Unit tests check individual functions. Integration tests verify components work together. E2E tests simulate real user flows.

Start testing early. Your future self will thank you.

**Next up:** Read the full testing guide"""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.overall_score >= 70
        assert audit.primary_keyword == "testing"
        assert audit.primary_keyword_count > 0
        assert audit.primary_keyword_in_h1 is True
        assert audit.h1_count == 1
        assert audit.heading_structure_valid is True

    def test_audit_catches_missing_h1(self):
        """Test audit catches missing H1."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """## Why Testing Matters

Testing early catches bugs.

## How to Start

Write your first test today."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.h1_count == 0
        assert any(i["code"] == "MISSING_H1" for i in audit.issues)
        assert audit.structure_score < 100

    def test_audit_catches_multiple_h1(self):
        """Test audit catches multiple H1s."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# First Title

Content here.

# Second Title

More content."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.h1_count == 2
        assert any(i["code"] == "MULTIPLE_H1" for i in audit.issues)

    def test_audit_catches_heading_hierarchy_skip(self):
        """Test audit catches skipped heading levels."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# Title

## Section

#### Skipped H3

Content."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert any(i["code"] == "HEADING_HIERARCHY_SKIP" for i in audit.issues)

    def test_audit_checks_keyword_density(self):
        """Test audit checks keyword density."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief, primary_kw="testing")
        # Low density content
        content = """# Early Testing Guide for Developers

Most developers skip testing until bugs appear. This costs time and money.

## Why Quality Matters

Quality saves effort later. Bugs in production are expensive.

## How to Begin

Write a test. Run it. Repeat.

Start now. Your future self will thank you."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        # Keyword "testing" appears once in ~100 words = 1% density (should pass)
        assert audit.primary_keyword_density >= 0.5

        # Test HIGH density (keyword stuffing)
        stuffed = content + " testing " * 100
        draft_stuffed = self.create_draft(stuffed, brief, outline)
        audit_stuffed = validator.audit(draft_stuffed.content, brief, outline)
        assert any(i["code"] == "HIGH_KEYWORD_DENSITY" for i in audit_stuffed.issues)

    def test_audit_checks_keyword_placement(self):
        """Test audit checks keyword in key positions."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief, primary_kw="testing")
        # No keyword in H1
        content = """# Early Guide for Developers

Most developers skip testing until bugs appear.

## Why Quality Matters

Quality saves effort later.

## How to Begin

Write a test. Run it. Repeat."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.primary_keyword_in_h1 is False
        # Should still find in title/first 100
        assert audit.primary_keyword_in_first_100 is True or audit.primary_keyword_in_title is True

    def test_audit_checks_meta_title_length(self):
        """Test audit validates meta title length."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        outline.seo.meta_title = "This is a very long meta title that exceeds the recommended sixty character limit for search engines"
        content = """# Early Testing Guide for Developers

Content here."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.meta_title_length > 60
        assert any(i["code"] == "META_TITLE_TOO_LONG" for i in audit.issues)

    def test_audit_checks_meta_title_short(self):
        """Test audit warns on too-short meta title."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        outline.seo.meta_title = "Short"
        content = """# Early Testing Guide for Developers

Content here."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.meta_title_length < 30
        assert any(i["code"] == "META_TITLE_TOO_SHORT" for i in audit.issues)

    def test_audit_checks_meta_description_length(self):
        """Test audit validates meta description length."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        outline.seo.meta_description = "Short"
        content = """# Early Testing Guide for Developers

Content here."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.meta_description_length < 120
        assert any(i["code"] == "META_DESC_TOO_SHORT" for i in audit.issues)

    def test_audit_checks_meta_description_long(self):
        """Test audit warns on too-long meta description."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        outline.seo.meta_description = "This is a very long meta description that goes well beyond the one hundred fifty five character limit that search engines typically display in search results and it just keeps going"
        content = """# Early Testing Guide for Developers

Content here."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.meta_description_length > 155
        assert any(i["code"] == "META_DESC_TOO_LONG" for i in audit.issues)

    def test_audit_calculates_readability(self):
        """Test audit calculates Flesch-Kincaid readability."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        # Simple, readable content
        content = """# Testing Guide

Test early. Save time. Write tests first. Run them often. Catch bugs early. Ship with confidence.

## Why It Matters

Bugs cost money. Early bugs cost less. Late bugs cost more.

## How To Do It

Write a test. Run it. Write another. Repeat.

Start now. Your future self will thank you."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.flesch_reading_ease is not None
        assert audit.flesch_kincaid_grade is not None
        assert audit.avg_sentence_length > 0
        assert audit.avg_syllables_per_word > 0

    def test_audit_catches_low_readability(self):
        """Test audit catches very difficult content."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        # Very complex sentences
        content = """# Testing Guide

The implementation of comprehensive testing methodologies necessitates the orchestration of multifaceted validation paradigms that systematically encompass the entirety of the software development lifecycle through the application of sophisticated automated verification frameworks.

## Why It Matters

The ramifications of inadequate quality assurance protocols manifest as exponentially increasing remediation expenditures that correlate directly with the temporal proximity to production deployment environments."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.flesch_reading_ease < 30
        assert any(i["code"] == "LOW_READABILITY" for i in audit.issues)

    def test_audit_analyzes_eeat(self):
        """Test audit analyzes E-E-A-T signals."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# Testing Guide

In my experience, testing early saves time. I found this when I tested my own code.
According to research, bugs in production cost 100x more. A study by NIST confirms this.
Our industry standard methodology follows best practices. This framework is proven.
We're transparent about limitations: testing doesn't guarantee zero bugs. Note: this is important."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.eeat_signals["experience_signals"] > 0
        assert audit.eeat_signals["expertise_signals"] > 0
        assert audit.eeat_signals["authoritativeness_signals"] > 0
        assert audit.eeat_signals["trustworthiness_signals"] > 0
        assert audit.eeat_score > 0

    def test_audit_catches_missing_outline_sections(self):
        """Test audit catches sections missing from outline."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# Early Testing Guide for Developers

## Why Testing Matters

Content here.

## How to Start

Content here.

Missing the Common Patterns section."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert any(i["code"] == "MISSING_OUTLINE_SECTIONS" for i in audit.issues)

    def test_audit_scores_components(self):
        """Test audit produces component scores."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# Early Testing Guide for Developers

Most developers skip testing until bugs appear.

## Why Testing Matters

Testing early catches bugs when they're cheap to fix.

## How to Start

Write your first test today. Run it. Watch it pass.

## Common Patterns

Unit tests check functions. Integration tests verify components. E2E tests simulate users.

Start testing early. Your future self will thank you.

**Next up:** Read the full testing guide"""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert 0 <= audit.keyword_score <= 100
        assert 0 <= audit.structure_score <= 100
        assert 0 <= audit.metadata_score <= 100
        assert 0 <= audit.readability_score <= 100
        assert 0 <= audit.eeat_score <= 100
        assert 0 <= audit.overall_score <= 100


class TestSEOValidatorEdgeCases:
    """Edge case tests for SEO validator."""

    def test_empty_content(self):
        """Test empty content handling."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        audit = validator.audit("", brief, outline)
        assert audit.overall_score == 0

    def test_unicode_content(self):
        """Test Unicode content handling."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief, primary_kw="testing")
        content = "# Testing café naïve\n\nTesting résumé."
        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)
        assert audit.primary_keyword_count >= 0

    def test_strict_mode(self):
        """Test strict mode fails on warnings."""
        validator = SEOValidator(strict=True)
        brief = self.create_brief()
        outline = self.create_outline(brief)
        outline.seo.meta_title = "Short"
        content = """# Title

Content."""
        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert audit.overall_score < 100  # Should have penalty

    def test_secondary_keywords(self):
        """Test secondary keyword tracking."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief, primary_kw="testing")
        outline.seo.secondary_keywords = ["unit testing", "TDD", "bugs"]
        content = """# Early Testing Guide for Developers

Unit testing and TDD help catch bugs early.

## Why Testing Matters

Unit testing saves time. TDD improves design. Bugs are caught early.

## How to Start

Start with unit testing. Then TDD.

## Common Patterns

Unit testing patterns. TDD cycles. Bug prevention."""

        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        assert "unit testing" in audit.secondary_keywords_found
        assert "TDD" in audit.secondary_keywords_found
        assert "bugs" in audit.secondary_keywords_found

    def test_audit_to_dict(self):
        """Test audit serialization."""
        validator = SEOValidator()
        brief = self.create_brief()
        outline = self.create_outline(brief)
        content = """# Testing Guide

Content here."""
        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        data = audit.to_dict()
        assert data["primary_keyword"] == "testing"
        assert data["overall_score"] >= 0
        assert "issues" in data
        assert "eeat_signals" in data


class TestSEOValidatorStrict:
    """Tests for strict mode behavior."""

    def test_strict_mode_low_score_fails(self):
        """Test strict mode fails on low overall score."""
        validator = SEOValidator(strict=True)
        brief = self.create_brief()
        outline = self.create_outline(brief)
        outline.seo.meta_title = "Short"
        content = """# Title

Very bad content with no keyword placement or structure."""
        draft = self.create_draft(content, brief, outline)
        audit = validator.audit(draft.content, brief, outline)

        # In strict mode, low scores should result in failed audit
        assert audit.overall_score < 70