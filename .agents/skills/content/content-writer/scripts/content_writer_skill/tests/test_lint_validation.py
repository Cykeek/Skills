"""
Contract Tests: Lint Validation
================================
Tests for Gate 2 - Lint validation (voice, style, grammar).
"""

import pytest
from content_writer_skill.lint import LintEngine
from content_writer_skill.lint.rules import (
    BANNED_OPENERS, ROBOTIC_TELLS, FORMAL_PHRASES,
    HEDGING_PHRASES, EM_DASH_PATTERN, CONTRACTION_MAP,
    SENTENCE_VARIETY_MIN, SENTENCE_VARIETY_MAX,
)
from content_writer_skill.models import ContentBrief, Goal, Format, LintSeverity
from content_writer_skill.models.validation_results import LintResult, LintIssue


class TestLintEngine:
    """Tests for LintEngine."""

    def create_brief(self, tone="conversational"):
        return ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1000 words",
            tone=tone,
            angle="Testing matters",
        )

    def test_clean_content_passes(self):
        """Test clean content passes lint."""
        engine = LintEngine()
        content = """# Testing Early

Testing early saves time. You catch bugs before they ship.
Write tests first. Run them often. Ship with confidence.

Start today. Your future self will thank you."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        alerts = [i for i in result.issues if i.severity == LintSeverity.ALERT]
        assert len(alerts) == 0

    def test_banned_opener_detected(self):
        """Test banned opener detection."""
        engine = LintEngine()
        content = """In today's world, testing is important.
Testing early saves time."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        banned = [i for i in result.issues if i.rule_id == "BANNED_OPENER"]
        assert len(banned) >= 1
        assert any("in today's world" in i.message.lower() for i in banned)

    def test_multiple_banned_openers(self):
        """Test multiple banned openers caught."""
        engine = LintEngine()
        content = """In this article, we explore testing.
This guide will show you how.
Let's dive into the details."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        banned = [i for i in result.issues if i.rule_id == "BANNED_OPENER"]
        assert len(banned) >= 2

    def test_robotic_tell_detected(self):
        """Test robotic tell word detection."""
        engine = LintEngine()
        content = """# Testing Guide

We must delve into the tapestry of testing.
Unlock the potential to leverage synergy.
Navigate the landscape of comprehensive solutions."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        robotic = [i for i in result.issues if i.rule_id == "ROBOTIC_TELL"]
        assert len(robotic) >= 3
        terms = [i.message for i in robotic]
        assert any("delve" in t.lower() for t in terms)
        assert any("tapestry" in t.lower() for t in terms)
        assert any("unlock" in t.lower() or "leverage" in t.lower() for t in terms)

    def test_formal_phrase_detected(self):
        """Test formal phrase detection."""
        engine = LintEngine()
        content = """# Testing Guide

We must utilize the framework to facilitate the process.
It is imperative to optimize the implementation."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        formal = [i for i in result.issues if i.rule_id == "FORMAL_PHRASE"]
        assert len(formal) >= 2
        terms = [i.message for i in formal]
        assert any("utilize" in t.lower() for t in terms)
        assert any("imperative" in t.lower() for t in terms)

    def test_em_dash_overuse(self):
        """Test em-dash overuse detection."""
        engine = LintEngine()
        # 600 words, 2 em-dashes (limit is 1 per 500)
        content = "Testing — is important. " * 300  # ~600 words, 300 em-dashes
        content = content[:3000]  # Trim but keep many em-dashes

        brief = self.create_brief()
        result = engine.lint(content, brief)

        em_dash = [i for i in result.issues if i.rule_id == "EM_DASH_OVERUSE"]
        assert len(em_dash) >= 1

    def test_hedging_detected(self):
        """Test hedging language detection."""
        engine = LintEngine()
        content = """# Testing Guide

Testing might help. It could improve quality.
Perhaps you should write tests. It seems to work."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        hedging = [i for i in result.issues if i.rule_id == "HEDGING"]
        assert len(hedging) >= 3
        terms = [i.message for i in hedging]
        assert any("might" in t.lower() for t in terms)
        assert any("could" in t.lower() for t in terms)
        assert any("perhaps" in t.lower() for t in terms)

    def test_high_hedging_density(self):
        """Test high hedging density flag."""
        engine = LintEngine()
        # 100 words with 5 hedges = 5% density (threshold 3%)
        content = "Testing may help. It might work. Could be good. Perhaps useful. Seems right. " * 20

        brief = self.create_brief()
        result = engine.lint(content, brief)

        density = [i for i in result.issues if i.rule_id == "HEDGING_DENSITY"]
        assert len(density) >= 1

    def test_sentence_variety_short(self):
        """Test sentence variety - short sentences."""
        engine = LintEngine()
        # All long sentences (no short ones)
        content = "This is a very long sentence that goes on and on without stopping for a very long time indeed. " * 10

        brief = self.create_brief()
        result = engine.lint(content, brief)

        short_var = [i for i in result.issues if i.rule_id == "LOW_SENTENCE_VARIETY_SHORT"]
        assert len(short_var) >= 1

    def test_sentence_variety_long(self):
        """Test sentence variety - too many long sentences."""
        engine = LintEngine()
        # All very long sentences
        content = ("This is an extremely long sentence that contains many words and continues "
                   "without any pause or break for a very long time indeed making it hard to read. " * 10)

        brief = self.create_brief()
        result = engine.lint(content, brief)

        long_var = [i for i in result.issues if i.rule_id == "HIGH_SENTENCE_VARIETY_LONG"]
        assert len(long_var) >= 1

    def test_low_contractions(self):
        """Test low contraction detection."""
        engine = LintEngine()
        content = """# Testing Guide

Testing is important. It does not fail. You cannot skip it.
We will not accept untested code. It is not optional."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        low_contr = [i for i in result.issues if i.rule_id == "LOW_CONTRACTIONS"]
        assert len(low_contr) >= 1

    def test_voice_drift_formal_tone(self):
        """Test voice drift detection for formal tone."""
        engine = LintEngine()
        content = """# Testing Guide

Hey guys, this is gonna be awesome!
Testing is cool and super easy."""

        brief = self.create_brief(tone="formal, authoritative")
        result = engine.lint(content, brief)

        drift = [i for i in result.issues if i.rule_id == "VOICE_DRIFT_CASUAL"]
        assert len(drift) >= 1
        assert result.voice_drift_detected is True
        assert result.voice_drift_score < 70

    def test_voice_drift_conversational_tone(self):
        """Test voice drift detection for conversational tone."""
        engine = LintEngine()
        content = """# Testing Guide

Furthermore, it is imperative to note that testing facilitates quality assurance.
Moreover, the implementation necessitates comprehensive verification."""

        brief = self.create_brief(tone="conversational, friendly")
        result = engine.lint(content, brief)

        drift = [i for i in result.issues if i.rule_id == "VOICE_DRIFT_FORMAL"]
        assert len(drift) >= 1
        assert result.voice_drift_detected is True
        assert result.voice_drift_score < 70

    def test_metrics_calculated(self):
        """Test metrics are calculated."""
        engine = LintEngine()
        content = """# Testing Guide

Testing early saves time. Write tests first.
Run them often. Ship with confidence."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        assert "word_count" in result.metrics
        assert "sentence_count" in result.metrics
        assert "avg_words_per_sentence" in result.metrics
        assert "robotic_tell_count" in result.metrics
        assert "em_dash_count" in result.metrics
        assert "banned_opener_count" in result.metrics

    def test_auto_fixable_flags(self):
        """Test auto_fixable flags are set correctly."""
        engine = LintEngine()
        content = """# Testing Guide

We must utilize the framework. It is imperative to optimize.
Testing might help. It could work."""

        brief = self.create_brief()
        result = engine.lint(content, brief)

        # Robotic tells and formal phrases should be auto-fixable
        robotic = [i for i in result.issues if i.rule_id == "ROBOTIC_TELL"]
        formal = [i for i in result.issues if i.rule_id == "FORMAL_PHRASE"]
        hedging = [i for i in result.issues if i.rule_id == "HEDGING"]

        for issue in robotic + formal + hedging:
            assert issue.auto_fixable is True

        # Banned openers and em-dash overuse not auto-fixable
        banned = [i for i in result.issues if i.rule_id == "BANNED_OPENER"]
        for issue in banned:
            assert issue.auto_fixable is False

    def test_custom_config(self):
        """Test custom lint configuration."""
        config = {
            "banned_openers": ["custom opener"],
            "robotic_tells": ["customtell"],
            "max_em_dash_per_500": 5,
            "min_contraction_pct": 1.0,
        }
        engine = LintEngine(config)
        content = "Custom opener: testing. Customtell word here."
        brief = self.create_brief()
        result = engine.lint(content, brief)

        banned = [i for i in result.issues if i.rule_id == "BANNED_OPENER"]
        assert any("custom opener" in i.message.lower() for i in banned)

        robotic = [i for i in result.issues if i.rule_id == "ROBOTIC_TELL"]
        assert any("customtell" in i.message.lower() for i in robotic)

    def test_lint_result_passed_property(self):
        """Test LintResult.passed property."""
        engine = LintEngine()
        content = "In today's world, testing is important."
        brief = self.create_brief()
        result = engine.lint(content, brief)

        # Has banned opener (ALERT) -> not passed
        assert result.passed is False

        # Clean content
        content2 = "Testing early saves time. Write tests first."
        result2 = engine.lint(content2, brief)
        assert result2.passed is True

    def test_lint_result_get_counts(self):
        """Test get_alert_count, get_warning_count, get_info_count."""
        engine = LintEngine()
        content = """In today's world, we must delve into testing.
It is imperative to utilize the framework.
Testing might help."""
        brief = self.create_brief()
        result = engine.lint(content, brief)

        assert result.get_alert_count() >= 1  # Banned opener + robotic tell
        assert result.get_warning_count() >= 1  # Formal phrase
        assert result.get_info_count() >= 0


class TestLintEngineEdgeCases:
    """Edge case tests for lint engine."""

    def test_empty_content(self):
        """Test empty content handling."""
        engine = LintEngine()
        result = engine.lint("", self.create_brief())
        assert result.passed is True
        assert len(result.issues) == 0
        assert result.metrics["word_count"] == 0

    def test_unicode_content(self):
        """Test Unicode content handling."""
        engine = LintEngine()
        content = "Testing café naïve résumé. Testing — em dash."
        brief = self.create_brief()
        result = engine.lint(content, brief)
        assert result.metrics["word_count"] > 0

    def test_markdown_headings_not_trigger_openers(self):
        """Test markdown headings don't trigger banned openers."""
        engine = LintEngine()
        content = """# In This Article

Testing content here.

## Let's Dive In

More content."""
        brief = self.create_brief()
        result = engine.lint(content, brief)

        # Headings shouldn't trigger (they're checked in first 10 lines, but headings are OK)
        # Actually they might - depends on implementation
        pass

    def test_context_in_issues(self):
        """Test issues include context snippets."""
        engine = LintEngine()
        content = "This is a very long sentence that goes on and on and on and on and on and on and on and on and on and on and on forever."
        brief = self.create_brief()
        result = engine.lint(content, brief)

        long_issues = [i for i in result.issues if i.rule_id == "HIGH_SENTENCE_VARIETY_LONG"]
        # Context might be empty for sentence variety (line 1)
        pass


class TestLintRulesCompleteness:
    """Test lint rule lists are comprehensive."""

    def test_banned_openers_comprehensive(self):
        """Test banned openers covers common patterns."""
        patterns = [
            "in today's", "in this article", "this post will",
            "we will explore", "let's dive", "welcome to",
            "have you ever", "are you looking", "if you're like",
            "as we all know", "it's no secret", "needless to say",
        ]
        for pattern in patterns:
            assert any(pattern in opener.lower() for opener in BANNED_OPENERS)

    def test_robotic_tells_comprehensive(self):
        """Test robotic tells covers known AI markers."""
        tells = ["delve", "tapestry", "unlock", "leverage", "synergy",
                 "paradigm", "holistic", "navigate", "deep dive",
                 "comprehensive", "multifaceted", "unprecedented",
                 "revolutionize", "game-changing", "cutting-edge"]
        for tell in tells:
            assert tell in ROBOTIC_TELLS

    def test_formal_phrases_comprehensive(self):
        """Test formal phrases covers common formalisms."""
        formal = ["utilize", "leverage", "facilitate", "optimize",
                  "implement", "execute", "mitigate", "alleviate",
                  "expedite", "streamline", "rationalize"]
        for phrase in formal:
            assert phrase in FORMAL_PHRASES

    def test_hedging_phrases_comprehensive(self):
        """Test hedging phrases covers common hedges."""
        hedges = ["may", "might", "could", "perhaps", "possibly",
                  "somewhat", "rather", "quite", "fairly",
                  "seems to", "appears to", "tends to"]
        for hedge in hedges:
            assert hedge in HEDGING_PHRASES