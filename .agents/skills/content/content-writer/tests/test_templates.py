"""Tests for template structure from templates.md."""
import re
from pathlib import Path

import pytest

TEMPLATES_PATH = Path(__file__).parent.parent / "references" / "templates.md"
TEMPLATES_TEXT = TEMPLATES_PATH.read_text(encoding="utf-8")


def get_template_section(template_number: int) -> str:
    """Extract a specific template section by number."""
    # Find the start of the template - match only top-level template headers
    # Pattern: "## N. Title Case" (number + period + space + uppercase letter)
    pattern = rf"^## {template_number}\. [A-Z]"
    match = re.search(pattern, TEMPLATES_TEXT, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    # Find the next template header (## N. where N > template_number)
    next_num = template_number + 1
    next_match = re.search(rf"^## {next_num}\. [A-Z]", TEMPLATES_TEXT[start:], re.MULTILINE)
    if next_match:
        end = start + next_match.start()
    else:
        end = len(TEMPLATES_TEXT)
    return TEMPLATES_TEXT[start:end]


class TestLandingPageTemplate:
    """Test Landing Page template (Template 2)."""

    def test_landing_page_has_required_sections(self):
        landing = get_template_section(2)
        assert "HEADLINE" in landing
        assert "SUBHEAD" in landing
        assert "Social proof" in landing
        assert "What you get" in landing
        assert "Benefit 1" in landing
        assert "Benefit 2" in landing
        assert "Benefit 3" in landing
        assert "The objection you're afraid to ask" in landing
        assert "How it works" in landing
        assert "Final CTA" in landing

    def test_landing_page_exactly_3_benefits(self):
        landing = get_template_section(2)
        # Count benefit sections
        benefit_count = landing.count("### [Benefit")
        assert benefit_count == 3

    def test_landing_page_has_objection_section(self):
        landing = get_template_section(2)
        assert "The objection you're afraid to ask" in landing

    def test_landing_page_has_single_cta(self):
        landing = get_template_section(2)
        cta_count = landing.count("[Final CTA")
        assert cta_count == 1

    def test_landing_page_pitfalls_documented(self):
        landing = get_template_section(2)
        assert "Multiple competing CTAs" in landing
        assert "Specs-as-benefits" in landing
        assert "No objection handling" in landing


class TestEmailTemplate:
    """Test Email template (Template 3)."""

    def test_email_has_subject_preheader_cta_above_fold(self):
        email = get_template_section(3)
        assert "Subject:" in email
        assert "Preheader:" in email
        assert "CTA: clearly visible above the fold" in email
        assert "CTA" in email

    def test_email_structure_complete(self):
        email = get_template_section(3)
        assert "Salutation" in email
        assert "1-sentence opener" in email
        assert "The value" in email
        assert "Sign-off" in email
        assert "P.S." in email

    def test_email_subject_formulas_10_present(self):
        email = get_template_section(3)
        formulas = [
            "Formula 1: Direct benefit",
            "Formula 2: Curiosity gap",
            "Formula 3: The number",
            "Formula 4: We shipped something",
            "Formula 5: The honest admission",
            "Formula 6: The reader's problem",
            "Formula 7: The personal/conversational",
            "Formula 8: The contrast",
            "Formula 9: The tease",
            "Formula 10: Scarcity",
        ]
        for formula in formulas:
            assert formula in email

    def test_email_subject_quality_test_5_criteria(self):
        email = get_template_section(3)
        quality = email.split("Subject line quality test:")[1]
        criteria = [
            "Under 50 characters",
            "Specific enough that removing one word changes the meaning",
            "Pays off in the first sentence",
            "Could double as a headline",
            "Would the reader feel deceived",
        ]
        for criterion in criteria:
            assert criterion in quality


class TestCaseStudyTemplate:
    """Test Case Study template (Template 6)."""

    def test_case_study_has_metrics_section(self):
        case = get_template_section(6)
        assert "The results" in case
        assert "Before / after" in case
        assert "As many numbers as you have" in case

    def test_case_study_structure_complete(self):
        case = get_template_section(6)
        required = [
            "TITLE",
            "The customer",
            "The problem",
            "Why they chose",
            "The solution",
            "The results",
            "In their words",
            "What's next",
            "CTA",
        ]
        for section in required:
            assert section in case

    def test_case_study_pitfalls_documented(self):
        case = get_template_section(6)
        pitfalls = case.split("### Pitfalls")[1]
        assert "No metrics" in pitfalls
        assert "Customer-vague" in pitfalls
        assert "Sales-pitch disguised as case study" in pitfalls


class TestComparisonPageTemplate:
    """Test Comparison Page template (Template 12)."""

    def test_comparison_page_has_tldr(self):
        comp = get_template_section(12)
        assert "TL;DR" in comp
        assert "what's the verdict and why" in comp

    def test_comparison_page_has_feature_table(self):
        comp = get_template_section(12)
        assert "At a glance" in comp
        assert "Feature comparison table" in comp
        assert "| Feature |" in comp
        assert "|---|---|---|" in comp

    def test_comparison_page_has_product_sections(self):
        comp = get_template_section(12)
        assert "## [Product X]" in comp
        assert "Who it's for" in comp
        assert "Pros" in comp
        assert "Cons" in comp

    def test_comparison_page_has_recommendation_by_use_case(self):
        comp = get_template_section(12)
        assert "Recommendation by use case" in comp
        assert "If you need" in comp
        assert "go with" in comp

    def test_comparison_page_has_methodology(self):
        comp = get_template_section(12)
        assert "How we evaluated" in comp
        assert "methodology" in comp.lower()

    def test_comparison_page_pitfalls_documented(self):
        comp = get_template_section(12)
        pitfalls = comp.split("### Pitfalls")[1]
        assert "Pretending your product wins every category" in pitfalls
        assert "No verdict for the impatient" in pitfalls
        assert "No \"by use case\" recommendation" in pitfalls


class TestAll12TemplatesPresent:
    """Verify all 12 templates exist."""

    def test_12_templates_exist(self):
        templates = [
            "## 1. Blog Post Template",
            "## 2. Landing Page Template",
            "## 3. Marketing Email Template",
            "## 4. Social Post Templates",
            "## 5. Press Release Template",
            "## 6. Case Study Template",
            "## 7. Whitepaper Template",
            "## 8. Video Script Template",
            "## 9. Podcast Outline Template",
            "## 10. Technical Doc Template",
            "## 11. FAQ Template",
            "## 12. Comparison Page Template",
        ]
        for template in templates:
            assert template in TEMPLATES_TEXT, f"Missing template: {template}"

    def test_each_template_has_structure_and_pitfalls(self):
        """Each template should have Structure and Pitfalls sections.

        Template 4 (Social Post Templates) uses platform-specific structures
        instead of a single "### Structure" heading, and uses "**Pitfalls:**" (bold)
        instead of "### Pitfalls".

        Template 9 (Podcast Outline Template) does not have a Pitfalls section.

        Note: We match only the known template titles to avoid matching ## headers
        inside code blocks (like Whitepaper's "## 1. The problem...").
        """
        # Known template titles - match only these to avoid code block headers
        template_titles = [
            "Blog Post Template",
            "Landing Page Template",
            "Marketing Email Template",
            "Social Post Templates",
            "Press Release Template",
            "Case Study Template",
            "Whitepaper Template",
            "Video Script Template",
            "Podcast Outline Template",
            "Technical Doc Template",
            "FAQ Template",
            "Comparison Page Template",
        ]
        template_starts = []
        for title in template_titles:
            pattern = rf"^## \d+\. {re.escape(title)}"
            match = re.search(pattern, TEMPLATES_TEXT, re.MULTILINE)
            assert match, f"Template not found: {title}"
            template_starts.append(match.start())

        template_starts.sort()
        assert len(template_starts) == 12, f"Expected 12 templates, found {len(template_starts)}"

        # Templates that don't have a Pitfalls section
        templates_without_pitfalls = {9}  # Podcast Outline

        for i, start in enumerate(template_starts):
            end = template_starts[i + 1] if i + 1 < len(template_starts) else len(TEMPLATES_TEXT)
            template = TEMPLATES_TEXT[start:end]
            template_num = i + 1

            # Template 4 uses platform-specific structure sections instead of single "### Structure"
            if template_num == 4:
                assert "### Twitter / X" in template, f"Template {template_num} missing Twitter structure"
                assert "### LinkedIn" in template, f"Template {template_num} missing LinkedIn structure"
                assert "### Instagram" in template, f"Template {template_num} missing Instagram structure"
                assert "### Facebook" in template, f"Template {template_num} missing Facebook structure"
                assert "**Pitfalls:**" in template, f"Template {template_num} missing **Pitfalls:**"
            else:
                assert "### Structure" in template, f"Template {template_num} missing Structure"

                # Template 9 (Podcast Outline) doesn't have Pitfalls
                if template_num not in templates_without_pitfalls:
                    assert "### Pitfalls" in template, f"Template {template_num} missing Pitfalls"


class TestBlogPostTemplate:
    """Test Blog Post template (Template 1)."""

    def test_blog_structure_has_hook_stakes_sections_synthesis_cta(self):
        blog = get_template_section(1)
        assert "Hook:" in blog
        assert "Stakes:" in blog
        assert "## [Section 1: H2]" in blog
        assert "## [Synthesis:" in blog
        assert "CTA:" in blog

    def test_blog_pitfalls_documented(self):
        blog = get_template_section(1)
        pitfalls = blog.split("### Pitfalls")[1]
        assert "Burying the lede" in pitfalls
        assert "No concrete examples" in pitfalls
        assert "Forgetting the takeaway" in pitfalls


class TestSocialPostTemplates:
    """Test Social Post templates (Template 4)."""

    def test_twitter_x_structure(self):
        social = get_template_section(4)
        assert "Twitter / X" in social
        assert "Hook:" in social
        assert "Setup/context" in social
        assert "The insight or value" in social
        assert "Payoff" in social
        assert "question to drive replies" in social

    def test_linkedin_structure(self):
        social = get_template_section(4)
        assert "LinkedIn" in social
        assert "Hook: first 2 lines must earn \"see more.\"" in social
        assert "Body: short paragraphs" in social
        assert "Takeaway:" in social
        assert "CTA or question" in social

    def test_instagram_structure(self):
        social = get_template_section(4)
        assert "Instagram" in social
        assert "First line hooks the visual" in social
        assert "Hashtags: 5–10 relevant" in social

    def test_facebook_threads_structure(self):
        social = get_template_section(4)
        assert "Facebook / Threads" in social
        assert "Open question or relatable line" in social


class TestPressReleaseTemplate:
    """Test Press Release template (Template 5)."""

    def test_press_release_structure(self):
        press = get_template_section(5)
        assert "FOR IMMEDIATE RELEASE" in press
        assert "Headline:" in press
        assert "Subhead:" in press
        assert "DATLINE" in press
        assert "Lede:" in press
        assert "Why it matters" in press
        assert "Quote:" in press
        assert "About the company" in press
        assert "Media contact" in press

    def test_press_release_pitfalls(self):
        press = get_template_section(5)
        pitfalls = press.split("### Pitfalls")[1]
        assert "Burying the news" in pitfalls
        assert "We are thrilled" in pitfalls
        assert "Markety adjectives" in pitfalls
        assert "No boilerplate" in pitfalls


class TestWhitepaperTemplate:
    """Test Whitepaper template (Template 7)."""

    def test_whitepaper_structure(self):
        wp = get_template_section(7)
        assert "Executive summary:" in wp
        assert "The problem (or context)" in wp
        assert "Current approaches and their limits" in wp
        assert "The framework (your contribution)" in wp
        assert "How to apply it" in wp
        assert "Case examples" in wp
        assert "Risks and limitations" in wp
        assert "Conclusion and next steps" in wp
        assert "Appendix" in wp
        assert "Gated CTA" in wp

    def test_whitepaper_pitfalls(self):
        wp = get_template_section(7)
        pitfalls = wp.split("### Pitfalls")[1]
        assert "No original contribution" in pitfalls
        assert "Padding to hit length" in pitfalls
        assert "Ignoring limitations" in pitfalls


class TestVideoScriptTemplate:
    """Test Video Script template (Template 8)."""

    def test_video_script_structure_60_sec(self):
        video = get_template_section(8)
        assert "HOOK" in video
        assert "PROBLEM" in video
        assert "SOLUTION REVEAL" in video
        assert "HOW IT WORKS" in video
        assert "PROOF" in video
        assert "CTA" in video

    def test_video_word_count_guide(self):
        video = get_template_section(8)
        assert "60-second script ≈ 150–180 words" in video
        assert "90-second ≈ 225–270 words" in video
        assert "3-min explainer ≈ 450–550 words" in video


class TestPodcastOutlineTemplate:
    """Test Podcast Outline template (Template 9)."""

    def test_podcast_structure(self):
        podcast = get_template_section(9)
        assert "Cold open" in podcast
        assert "Intro:" in podcast
        assert "Section 1: Context" in podcast
        assert "Section 2: The core topic" in podcast
        assert "Section 3: Practical takeaways" in podcast
        assert "Closing:" in podcast
        assert "Outro:" in podcast


class TestTechnicalDocTemplate:
    """Test Technical Doc template (Template 10)."""

    def test_tech_doc_structure(self):
        tech = get_template_section(10)
        assert "TITLE:" in tech
        assert "1-sentence summary" in tech
        assert "Prerequisites" in tech
        assert "Step 1:" in tech
        assert "Action verb" in tech
        assert "Show expected output" in tech
        assert "Troubleshooting" in tech
        assert "Next steps" in tech


class TestFAQTemplate:
    """Test FAQ template (Template 11)."""

    def test_faq_structure(self):
        faq = get_template_section(11)
        assert "Question 1 (phrased as a human would ask)" in faq
        assert "Answer in 1–4 sentences" in faq
        assert "Optional: link to deeper resource" in faq

    def test_faq_pitfalls(self):
        faq = get_template_section(11)
        pitfalls = faq.split("### Pitfalls")[1]
        assert "Phrasing questions in marketing-speak" in pitfalls
        assert "Long answers when the user wants a fast" in pitfalls
        assert "Missing the questions users actually have" in pitfalls


if __name__ == "__main__":
    pytest.main([__file__, "-v"])