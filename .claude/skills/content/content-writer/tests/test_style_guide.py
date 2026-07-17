"""Tests for style guide rules from references/style-guide.md."""
import re
from pathlib import Path

import pytest


STYLE_GUIDE_PATH = Path(__file__).parent.parent / "references" / "style-guide.md"
STYLE_GUIDE_TEXT = STYLE_GUIDE_PATH.read_text(encoding="utf-8")


class TestContractionTarget:
    """Test contraction target of ~70-80%."""

    def test_contraction_rule_documented(self):
        assert "Use contractions in ~70–80% of eligible spots" in STYLE_GUIDE_TEXT
        assert "Reserve full forms for emphasis or formal disclaimers" in STYLE_GUIDE_TEXT

    def test_contraction_examples_present(self):
        assert "You'll need" in STYLE_GUIDE_TEXT
        assert "It's important" in STYLE_GUIDE_TEXT
        assert "They can't" in STYLE_GUIDE_TEXT

    def test_robotic_no_contraction_examples_present(self):
        assert "You will need to configure" in STYLE_GUIDE_TEXT
        assert "It is important that we do not" in STYLE_GUIDE_TEXT
        assert "They are not able to" in STYLE_GUIDE_TEXT


class TestSentenceVariety:
    """Test sentence variety check - not all same opener."""

    def test_sentence_variety_rule_documented(self):
        assert "Humans mix lengths" in STYLE_GUIDE_TEXT
        assert "The robotic pattern is uniform length + uniform structure" in STYLE_GUIDE_TEXT
        assert "Vary sentence openings" in STYLE_GUIDE_TEXT
        assert "Not every sentence starts with" in STYLE_GUIDE_TEXT
        assert '"The / This / It / There."' in STYLE_GUIDE_TEXT
        assert "Drop in a one-sentence paragraph for emphasis" in STYLE_GUIDE_TEXT

    def test_robotic_example_uniform(self):
        robotic = STYLE_GUIDE_TEXT.split("❌ Robotic:")[1].split("✅")[0]
        # The example should show uniform sentence structure
        assert "The system requires authentication" in robotic
        assert "You must provide a valid token" in robotic
        assert "Tokens expire after 24 hours" in robotic
        assert "You can refresh them using the endpoint" in robotic

    def test_humane_example_varied(self):
        humane = STYLE_GUIDE_TEXT.split("✅ Humane:")[1].split("```")[0]
        assert "The system requires authentication via a valid token" in humane
        assert "Tokens expire\nafter 24 hours" in humane
        assert "refresh them using the endpoint" in humane
        assert "Here's how" in humane


class TestHedgingDensity:
    """Test hedging density > 2/paragraph flagged."""

    def test_hedging_density_rule_documented(self):
        # Check the robotic tells checklist for hedging density
        robotic_checklist = STYLE_GUIDE_TEXT.split("## 8. The \"Robotic Tells\" Checklist")[1].split("##")[0]
        assert "Hedging density > 2 per paragraph" in robotic_checklist
        assert "might" in robotic_checklist
        assert "possibly" in robotic_checklist
        assert "perhaps" in robotic_checklist

    def test_robotic_tells_includes_hedging(self):
        robotic_checklist = STYLE_GUIDE_TEXT.split("## 8. The \"Robotic Tells\" Checklist")[1].split("##")[0]
        assert "Hedging density > 2 per paragraph" in robotic_checklist
        assert "might" in robotic_checklist
        assert "possibly" in robotic_checklist
        assert "perhaps" in robotic_checklist


class TestVoiceDriftDetection:
    """Test voice drift detection."""

    def test_voice_drift_section_exists(self):
        assert "### Voice drift detection" in STYLE_GUIDE_TEXT

    def test_voice_drift_check_method(self):
        drift_section = STYLE_GUIDE_TEXT.split("### Voice drift detection")[1].split("###")[0]
        assert "Read three non-adjacent paragraphs" in drift_section
        assert "sounds like a different writer" in drift_section

    def test_common_drift_triggers_listed(self):
        drift_section = STYLE_GUIDE_TEXT.split("### Voice drift detection")[1].split("###")[0]
        assert "it's worth noting that" in drift_section
        assert "use" in drift_section.lower()
        assert "help" in drift_section.lower()
        assert 'switches from "you" to "one" or "users"' in drift_section


class TestEmDashBan:
    """Test em dash ban in body prose."""

    def test_em_dash_absolute_rule(self):
        assert "Em dashes are **banned in body prose**" in STYLE_GUIDE_TEXT
        assert "explicit user requests" in STYLE_GUIDE_TEXT
        assert "Don't ask" in STYLE_GUIDE_TEXT
        assert "The answer is always no" in STYLE_GUIDE_TEXT

    def test_em_dash_anti_patterns_documented(self):
        table_section = STYLE_GUIDE_TEXT.split("### 🔹 Em Dash Anti-Patterns")[1].split("##")[0]
        assert "For Appositives/Parentheticals" in table_section
        assert "To Introduce Explanations/Lists" in table_section
        assert "As a General Connector/Glue" in table_section
        assert "For Simple Enumeration" in table_section

    def test_em_dash_alternatives_documented(self):
        table_section = STYLE_GUIDE_TEXT.split("### 🔹 Em Dash Anti-Patterns & Human-Preferred Alternatives")[1].split("##")[0]
        assert "period" in table_section.lower()
        assert "comma" in table_section.lower()
        assert "colon" in table_section.lower()
        assert "parentheses" in table_section.lower()
        assert "rephrase" in table_section.lower()

    def test_final_em_dash_rule(self):
        assert "Final Rule (no exceptions in prose)" in STYLE_GUIDE_TEXT
        assert "When you find an em dash in something you have written, replace it" in STYLE_GUIDE_TEXT
        assert "don't evaluate whether it was justified" in STYLE_GUIDE_TEXT
        assert "The evaluation is already done" in STYLE_GUIDE_TEXT


class TestBannedOpenings:
    """Test banned opening patterns."""

    def test_banned_openings_table_exists(self):
        assert "### Opening sentence quality rules" in STYLE_GUIDE_TEXT
        assert "Banned opening patterns" in STYLE_GUIDE_TEXT
        assert "| Banned pattern | Why it fails | Fix |" in STYLE_GUIDE_TEXT

    def test_all_7_banned_patterns_present(self):
        banned_table = STYLE_GUIDE_TEXT.split("### Opening sentence quality rules")[1].split("###")[0]
        patterns = [
            "In today's [X] landscape",
            "In this article, I will",
            "It is important to understand that",
            "As we all know",
            "[Topic] is a critical component",
            "In recent years, [trends]",
        ]
        for pattern in patterns:
            assert pattern in banned_table, f"Missing banned pattern: {pattern}"

    def test_strong_opening_patterns_documented(self):
        assert "**Strong opening patterns (use these instead):**" in STYLE_GUIDE_TEXT
        strong_section = STYLE_GUIDE_TEXT.split("**Strong opening patterns (use these instead):**")[1].split("###")[0]
        patterns = [
            "Drop into the reader's situation",
            "Subvert an expectation",
            "State the thesis directly",
            "Pose the question the reader is already asking",
            "Open in medias res",
        ]
        for pattern in patterns:
            assert pattern in strong_section


class TestEmpathyPatterns:
    """Test empathy patterns."""

    def test_acknowledge_before_inform(self):
        assert "### Acknowledge before you inform" in STYLE_GUIDE_TEXT
        empathy_section = STYLE_GUIDE_TEXT.split("### Acknowledge before you inform")[1].split("###")[0]
        assert "Forgetting passwords is frustrating" in empathy_section
        assert "Looks like something's missing" in empathy_section
        assert "You've got a few good paths forward" in empathy_section

    def test_validate_before_correct(self):
        assert "### Validate before you correct" in STYLE_GUIDE_TEXT
        validate_section = STYLE_GUIDE_TEXT.split("### Validate before you correct")[1].split("###")[0]
        assert "That's a logical approach" in validate_section
        assert "it *would* work if the API used REST" in validate_section
        assert "However, this one uses GraphQL" in validate_section


class TestAudienceToneAdaptation:
    """Test audience-specific tone adaptation."""

    def test_developer_tone(self):
        assert "### 👩‍💻 Developers" in STYLE_GUIDE_TEXT
        dev_section = STYLE_GUIDE_TEXT.split("### 👩‍💻 Developers")[1].split("###")[0]
        assert "Precise, technical, peer-to-peer" in dev_section
        assert "Show code" in dev_section
        assert "name the actual function/API" in dev_section
        assert "acknowledge trade-offs" in dev_section

    def test_executive_tone(self):
        assert "### 💼 Executives" in STYLE_GUIDE_TEXT
        exec_section = STYLE_GUIDE_TEXT.split("### 💼 Executives")[1].split("###")[0]
        assert "Crisp, results-first, scannable" in exec_section
        assert "Lead with the business outcome" in exec_section
        assert "quantify impact" in exec_section

    def test_consumer_tone(self):
        assert "### 🛒 Consumers" in STYLE_GUIDE_TEXT
        consumer_section = STYLE_GUIDE_TEXT.split("### 🛒 Consumers")[1].split("###")[0]
        assert "Relatable, story-driven, warm" in consumer_section
        assert 'Use "you,"' in consumer_section
        assert "frame features as benefits" in consumer_section

    def test_first_time_visitor_tone(self):
        assert "### 🆕 First-time visitors" in STYLE_GUIDE_TEXT
        visitor_section = STYLE_GUIDE_TEXT.split("### 🆕 First-time visitors")[1].split("###")[0]
        assert "Orient, reassure, don't assume jargon knowledge" in visitor_section
        assert "Define terms on first use" in visitor_section
        assert 'point to the "start here" resource' in visitor_section

    def test_technical_non_dev_tone(self):
        assert "### 🎓 Technical-but-not-developer" in STYLE_GUIDE_TEXT
        tech_section = STYLE_GUIDE_TEXT.split("### 🎓 Technical-but-not-developer")[1].split("###")[0]
        assert "Bridge: technical enough to be useful, plain enough to be clear" in tech_section
        assert "Explain *why* a technical choice matters" in tech_section

    def test_stressed_frustrated_tone(self):
        assert "### 🚨 Stressed / frustrated readers" in STYLE_GUIDE_TEXT
        stressed_section = STYLE_GUIDE_TEXT.split("### 🚨 Stressed / frustrated readers")[1].split("###")[0]
        assert "Calm, brief, action-first" in stressed_section
        assert "Acknowledge the friction" in stressed_section
        assert "give the fix in one sentence" in stressed_section


class TestBrandVoiceMapping:
    """Test brand voice mapping framework."""

    def test_four_voice_dimensions(self):
        assert "### The 4 voice dimensions" in STYLE_GUIDE_TEXT
        dim_section = STYLE_GUIDE_TEXT.split("### The 4 voice dimensions")[1].split("###")[0]
        assert "Formal ↔ Casual" in dim_section
        assert "Serious ↔ Playful" in dim_section
        assert "Respectful ↔ Irreverent" in dim_section
        assert "Matter-of-fact ↔ Visionary" in dim_section

    def test_brand_mapping_5_minutes(self):
        assert "### Mapping a brand in 5 minutes" in STYLE_GUIDE_TEXT
        map_section = STYLE_GUIDE_TEXT.split("### Mapping a brand in 5 minutes")[1].split("###")[0]
        assert "Pick 3 adjectives" in map_section
        assert "Pick 3 adjectives it's NOT" in map_section
        assert "Three sample sentences" in map_section

    def test_voice_examples_present(self):
        assert "### Voice examples" in STYLE_GUIDE_TEXT
        examples = STYLE_GUIDE_TEXT.split("### Voice examples")[1].split("\n## ")[0]
        assert "Stripe" in examples
        assert "Mailchimp" in examples
        assert "Basecamp" in examples
        assert "Notion" in examples


class TestRoboticTellsChecklist:
    """Test robotic tells checklist completeness."""

    def test_all_15_robotic_tells_present(self):
        checklist = STYLE_GUIDE_TEXT.split("## 8. The \"Robotic Tells\" Checklist")[1].split("##")[0]
        tells = [
            "Every sentence is the same length",
            "Every paragraph starts with",
            "No contractions anywhere",
            "\"Utilize\" instead of \"use\"",
            "\"to\" instead of \"to\"",
            "\"it's important to note that\"",
            "At the end of the day",
            "Passive voice where the actor is known",
            "Em dashes are misused",
            "Bullet points where prose would flow better",
            "A short explanatory block has been broken into bullets",
            "Prose where bullet points would scan better",
            "Hedging density > 2 per paragraph",
            "Zero hedging where uncertainty exists",
            "Generic praise",
            "\"Leverage\" as a verb",
        ]
        for tell in tells:
            assert tell in checklist, f"Missing robotic tell: {tell}"


class TestQuickVoiceCalibration:
    """Test quick voice calibration test."""

    def test_calibration_question(self):
        assert "## 9. Quick Voice Calibration Test" in STYLE_GUIDE_TEXT
        cal_section = STYLE_GUIDE_TEXT.split("## 9. Quick Voice Calibration Test")[1].split("##")[0]
        assert '"Would I say this out loud to a smart colleague?"' in cal_section
        assert "If yes → ship it" in cal_section
        assert "I'd say it differently out loud" in cal_section
        assert "I'd never say this out loud" in cal_section


class TestHumanCraftDecisionRules:
    """Test human-craft decision rules."""

    def test_give_skimmer_early_win(self):
        assert "### Give the skimmer an early win" in STYLE_GUIDE_TEXT
        skimmer = STYLE_GUIDE_TEXT.split("### Give the skimmer an early win")[1].split("###")[0]
        assert "TL;DR verdict" in skimmer
        assert "comparison table" in skimmer
        assert "quick answer" in skimmer
        assert "summary box" in skimmer
        assert "list of takeaways" in skimmer
        assert '"who this is for" line' in skimmer

    def test_translate_facts_consequences(self):
        assert "### Translate facts into consequences" in STYLE_GUIDE_TEXT
        facts = STYLE_GUIDE_TEXT.split("### Translate facts into consequences")[1].split("###")[0]
        assert "50 integrations" in facts
        assert "keep their existing stack" in facts
        assert "1.2 seconds" in facts
        assert "mobile visitors aren't stuck waiting" in facts

    def test_cta_timing_trust(self):
        assert "### Match CTA timing to trust earned" in STYLE_GUIDE_TEXT
        cta = STYLE_GUIDE_TEXT.split("### Match CTA timing to trust earned")[1].split("###")[0]
        assert "Low-friction CTA after hero" in cta
        assert "Mid-friction CTA after proof" in cta
        assert "High-friction CTA after deeper validation" in cta

    def test_transitions_as_momentum(self):
        assert "### Use transitions as momentum, not decoration" in STYLE_GUIDE_TEXT
        trans = STYLE_GUIDE_TEXT.split("### Use transitions as momentum, not decoration")[1].split("###")[0]
        assert "planning problem" in trans
        assert "calendar alive after week one" in trans
        assert "pricing looks simple until team size" in trans
        assert "claim is clear" in trans
        assert "evidence behind it" in trans

    def test_ending_shapes(self):
        assert "### Choose the ending shape intentionally" in STYLE_GUIDE_TEXT
        endings = STYLE_GUIDE_TEXT.split("### Choose the ending shape intentionally")[1].split("###")[0]
        assert "**Practical guide:** roadmap, checklist, next step" in endings
        assert "**Landing page:** earned CTA" in endings
        assert "**Thought leadership:** sharpened takeaway or challenge" in endings
        assert "**Journalistic/explanatory piece:** image, unresolved question, callback, or warning" in endings
        assert "**Comparison:** recommendation by use case" in endings

    def test_specificity_engine(self):
        assert "### Specificity is the main engine of human credibility" in STYLE_GUIDE_TEXT
        spec = STYLE_GUIDE_TEXT.split("### Specificity is the main engine of human credibility")[1].split("###")[0]
        assert "a named example" in spec
        assert "a concrete scenario" in spec
        assert "a number with context" in spec
        assert "a quote in a real person's language" in spec
        assert "a before/after contrast" in spec
        assert "a constraint, trade-off, or edge case" in spec

    def test_prefer_paragraphs_over_reflex_bullets(self):
        assert "### Prefer paragraphs over reflex bullets" in STYLE_GUIDE_TEXT
        bullets = STYLE_GUIDE_TEXT.split("### Prefer paragraphs over reflex bullets")[1].split("##")[0]
        assert "Many AI drafts turn every idea into a list" in bullets
        assert "Human writers usually don't" in bullets
        assert "Good uses for bullets" in bullets
        assert "steps, checklists, specs" in bullets
        assert "Poor uses" in bullets
        assert "intro copy" in bullets
        assert "single supporting ideas" in bullets
        assert "3x3 feature grid" in bullets


class TestBeforeAfterRewrites:
    """Test before/after rewrite library."""

    def test_7_examples_present(self):
        assert "## 7. Before/After Rewrite Library" in STYLE_GUIDE_TEXT
        # Split on level-2 headers only (## at start of line)
        library = STYLE_GUIDE_TEXT.split("## 7. Before/After Rewrite Library")[1].split("\n## ")[0]
        examples = [
            "Robotic tech doc → humane",
            "Stiff landing page → conversational",
            "Vague marketing → specific",
            "Hedging overload → confident",
            "Bury-the-lede → lead with it",
            "Consumer marketing, robotic → warm",
            "Supportive email, canned → real",
        ]
        for ex in examples:
            assert ex in library, f"Missing example: {ex}"

    def test_example_1_contraction_change(self):
        ex1 = STYLE_GUIDE_TEXT.split("### Example 1: Robotic tech doc → humane")[1].split("\n## ")[0]
        assert "uses machine learning algorithms" in ex1
        assert "uses machine learning" in ex1
        assert "gets better the more data you feed it" in ex1

    def test_example_2_contraction_change(self):
        ex2 = STYLE_GUIDE_TEXT.split("### Example 2: Stiff landing page → conversational")[1].split("###")[0]
        assert "Authentication is required" in ex2
        assert "You'll need to log in" in ex2

    def test_example_3_specificity(self):
        ex3 = STYLE_GUIDE_TEXT.split("### Example 3: Vague marketing → specific")[1].split("###")[0]
        assert "empowers businesses to achieve operational excellence" in ex3
        assert "cuts the average team's reporting time from 6 hours a week to under 30 minutes" in ex3

    def test_example_4_hedging_reduction(self):
        ex4 = STYLE_GUIDE_TEXT.split("### Example 4: Hedging overload → confident")[1].split("###")[0]
        assert "might possibly be the case that this could potentially improve" in ex4
        assert "This should improve performance" in ex4
        assert "If it doesn't, here's likely why" in ex4

    def test_example_5_bury_lede(self):
        ex5 = STYLE_GUIDE_TEXT.split("### Example 5: Bury-the-lede → lead with it")[1].split("###")[0]
        assert "In today's fast-paced digital landscape" in ex5
        assert "You're losing customers you don't have to" in ex5


class TestEditingChecklistIntegration:
    """Test that editing checklist references style guide correctly."""

    def test_checklist_references_linter(self):
        checklist_path = Path(__file__).parent.parent / "references" / "editing-checklist.md"
        checklist_text = checklist_path.read_text(encoding="utf-8")
        assert "Run the Python content linter script" in checklist_text
        assert "lint_content.py" in checklist_text
        assert "Validate the draft against the em-dash ban" in checklist_text
        assert "Ensure all warnings are resolved" in checklist_text

    def test_checklist_phases_documented(self):
        checklist_path = Path(__file__).parent.parent / "references" / "editing-checklist.md"
        checklist_text = checklist_path.read_text(encoding="utf-8")
        assert "Phase 1: Developmental Editing" in checklist_text
        assert "Phase 2: Copyediting" in checklist_text
        assert "Phase 3: Proofreading" in checklist_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])