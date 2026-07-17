"""
Contract Tests: DEI / Accessibility Validation
===============================================
Tests for Gate 5 - DEI/Accessibility validation.
"""

import pytest
from content_writer_skill.validation import DEIValidator
from content_writer_skill.models import ContentBrief, Goal, Format, LintSeverity
from content_writer_skill.models.validation_results import DEIResult, DEIFinding


class TestDEIValidator:
    """Tests for DEIValidator."""

    def create_brief(self) -> ContentBrief:
        return ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1000 words",
            tone="clear, inclusive",
            angle="Testing matters",
        )

    def test_validate_passes_clean_content(self):
        """Test validator passes for clean, inclusive content."""
        validator = DEIValidator()
        content = """# Testing Guide

Testing early saves time for everyone on the team.
Write tests that cover the main use cases.
Your colleagues will appreciate the safety net."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        # Should have no alerts, maybe some info
        assert result.get_alert_count() == 0
        assert result.passed is True

    def test_catches_gendered_language(self):
        """Test catches gendered terms."""
        validator = DEIValidator()
        content = """# Testing Guide

Hey guys, let's talk about testing.
The chairman of the board agreed.
We need more manpower for this project."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        gendered = [f for f in result.findings if f.category == "inclusive_language" and "gendered" in f.rule_id.lower()]
        assert len(gendered) >= 2
        terms = [f.message for f in gendered]
        assert any("guys" in t.lower() for t in terms)
        assert any("chairman" in t.lower() or "manpower" in t.lower() for t in terms)

    def test_catches_ableist_language(self):
        """Test catches ableist terms."""
        validator = DEIValidator()
        content = """# Testing Guide

That's a crazy idea. Don't be dumb about it.
The code is lame. It's a blind spot in our coverage.
We need to sanitize the input."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        ableist = [f for f in result.findings if f.category == "inclusive_language" and "ableist" in f.rule_id.lower()]
        assert len(ableist) >= 3
        terms = [f.message for f in ableist]
        assert any("crazy" in t.lower() for t in terms)
        assert any("dumb" in t.lower() for t in terms)
        assert any("lame" in t.lower() for t in terms)

    def test_catches_racialized_terms(self):
        """Test catches racialized terminology."""
        validator = DEIValidator()
        content = """# Testing Guide

Add the master branch to the whitelist.
Remove the blacklist entries.
Check the slave process status."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        racial = [f for f in result.findings if f.category == "inclusive_language" and "racial" in f.rule_id.lower()]
        assert len(racial) >= 2
        terms = [f.message for f in racial]
        assert any("master" in t.lower() or "whitelist" in t.lower() for t in terms)
        assert any("blacklist" in t.lower() for t in terms)

    def test_catches_cultural_appropriation(self):
        """Test catches culturally appropriative terms."""
        validator = DEIValidator()
        content = """# Testing Guide

Our ninja developers are rockstars.
They're gurus of the craft.
Let's have a powwow about this.
Don't go off the reservation."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        cultural = [f for f in result.findings if f.category == "inclusive_language" and "cultural" in f.rule_id.lower()]
        assert len(cultural) >= 2
        terms = [f.message for f in cultural]
        assert any("ninja" in t.lower() or "guru" in t.lower() for t in terms)

    def test_catches_ageist_language(self):
        """Test catches ageist language."""
        validator = DEIValidator()
        content = """# Testing Guide

The elderly developers struggle with new tools.
Digital natives pick it up fast.
We need young and naive perspectives."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        age_bias = [f for f in result.findings if f.category == "bias" and "age" in f.rule_id.lower()]
        assert len(age_bias) >= 2

    def test_catches_gender_bias(self):
        """Test catches gender bias patterns."""
        validator = DEIValidator()
        content = """# Testing Guide

He should write tests. She must review them.
Men are better at debugging. Women are better at documentation."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        gender_bias = [f for f in result.findings if f.category == "bias" and "gender" in f.rule_id.lower()]
        assert len(gender_bias) >= 2

    def test_catches_vague_link_text(self):
        """Test catches vague link text (accessibility)."""
        validator = DEIValidator()
        content = """# Testing Guide

[Click here](https://example.com) for more info.
[Read more](https://example.com) about testing.
[Learn more](https://example.com) today."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        vague_links = [f for f in result.findings if f.rule_id == "VAGUE_LINK_TEXT"]
        assert len(vague_links) >= 3

    def test_catches_missing_alt_text(self):
        """Test catches images without alt text."""
        validator = DEIValidator()
        content = """# Testing Guide

![Chart showing test coverage](chart.png)
![](diagram.png)"""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        missing_alt = [f for f in result.findings if f.rule_id == "MISSING_ALT_TEXT"]
        assert len(missing_alt) >= 1

        insufficient_alt = [f for f in result.findings if f.rule_id == "INSUFFICIENT_ALT_TEXT"]
        assert len(insufficient_alt) >= 1

    def test_catches_heading_hierarchy_skip(self):
        """Test catches heading hierarchy skips (accessibility)."""
        validator = DEIValidator()
        content = """# Title

## Section

#### Skipped H3

Content."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        heading_skips = [f for f in result.findings if f.rule_id == "HEADING_SKIP"]
        assert len(heading_skips) >= 1

    def test_catches_cultural_bias(self):
        """Test catches cultural assumptions."""
        validator = DEIValidator()
        content = """# Testing Guide

The American way of testing is best.
Everyone knows this is the standard approach."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        cultural_bias = [f for f in result.findings if f.category == "bias" and "cultural" in f.rule_id.lower()]
        assert len(cultural_bias) >= 2

    def test_scores_calculated(self):
        """Test DEI scores are calculated."""
        validator = DEIValidator()
        content = """# Testing Guide

Testing early saves time for everyone.
Write inclusive tests."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        assert 0 <= result.inclusive_language_score <= 100
        assert 0 <= result.accessibility_score <= 100
        assert 0 <= result.bias_score <= 100

    def test_strict_mode_fails_on_warnings(self):
        """Test strict mode fails on warnings."""
        validator = DEIValidator(strict=True)
        content = """# Testing Guide

Hey guys, let's test."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        # Has warning for "guys", strict mode should fail
        assert result.passed is False

    def test_findings_have_required_fields(self):
        """Test all findings have required fields."""
        validator = DEIValidator()
        content = """# Testing Guide

Hey guys, that's crazy."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        for finding in result.findings:
            assert finding.category in ("inclusive_language", "accessibility", "bias")
            assert finding.rule_id
            assert finding.message
            assert finding.severity in LintSeverity
            assert finding.location
            assert finding.suggestion
            assert isinstance(finding.auto_fixable, bool)

    def test_get_alert_count(self):
        """Test alert count method."""
        validator = DEIValidator()
        content = """# Testing Guide

This is insane. That's lame.
![Image](img.png)"""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        alerts = result.get_alert_count()
        # "insane" and "lame" are warnings, missing alt is alert
        assert alerts >= 1

    def test_get_warning_count(self):
        """Test warning count method."""
        validator = DEIValidator()
        content = """# Testing Guide

Hey guys, that's crazy."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        warnings = result.get_warning_count()
        assert warnings >= 2

    def test_to_dict(self):
        """Test DEIResult serialization."""
        validator = DEIValidator()
        content = """# Testing Guide

Hey guys."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        data = result.to_dict()
        assert "passed" in data
        assert "inclusive_language_score" in data
        assert "accessibility_score" in data
        assert "bias_score" in data
        assert "findings" in data
        assert len(data["findings"]) > 0


class TestDEIValidatorEdgeCases:
    """Edge case tests for DEI validator."""

    def test_empty_content(self):
        """Test empty content handling."""
        validator = DEIValidator()
        result = validator.validate("", self.create_brief())
        assert result.passed is True
        assert len(result.findings) == 0

    def test_case_insensitive_matching(self):
        """Test case insensitive term matching."""
        validator = DEIValidator()
        content = """# Testing Guide

GUYS and GuYS and guys."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        guys_findings = [f for f in result.findings if "GUYS" in f.rule_id]
        assert len(guys_findings) == 3  # Each occurrence found

    def test_overlapping_patterns(self):
        """Test overlapping patterns don't double-count incorrectly."""
        validator = DEIValidator()
        content = """# Testing Guide

The master branch is on the whitelist."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        # Should find both terms
        racial_findings = [f for f in result.findings if "racial" in f.rule_id.lower()]
        assert len(racial_findings) >= 2

    def test_suggestion_provided(self):
        """Test suggestions are provided for fixes."""
        validator = DEIValidator()
        content = """# Testing Guide

Hey guys."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        for finding in result.findings:
            assert finding.suggestion
            assert len(finding.suggestion) > 0

    def test_auto_fixable_flag(self):
        """Test auto_fixable flag for language issues."""
        validator = DEIValidator()
        content = """# Testing Guide

Hey guys."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        lang_findings = [f for f in result.findings if f.category == "inclusive_language"]
        for f in lang_findings:
            assert f.auto_fixable is True

    def test_accessibility_not_auto_fixable(self):
        """Test accessibility issues are not auto-fixable."""
        validator = DEIValidator()
        content = """# Testing Guide

[Click here](link)
![](img.png)"""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        a11y_findings = [f for f in result.findings if f.category == "accessibility"]
        for f in a11y_findings:
            assert f.auto_fixable is False

    def test_bias_not_auto_fixable(self):
        """Test bias issues are not auto-fixable."""
        validator = DEIValidator()
        content = """# Testing Guide

He should do it. She must follow."""

        brief = self.create_brief()
        result = validator.validate(content, brief)

        bias_findings = [f for f in result.findings if f.category == "bias"]
        for f in bias_findings:
            assert f.auto_fixable is False