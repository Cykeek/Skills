"""Tests for persuasion framework selection logic from references/persuasion-frameworks.md."""
import re
from pathlib import Path

import pytest

PERSUASION_PATH = Path(__file__).parent.parent / "references" / "persuasion-frameworks.md"
PERSUASION_TEXT = PERSUASION_PATH.read_text(encoding="utf-8")


def get_section_text(section_number: int, title_contains: str = None) -> str:
    """Extract a section by its number and optional title match."""
    pattern = rf"^## {section_number}\. "
    if title_contains:
        pattern += re.escape(title_contains)
    pattern += r".*?(?=^## \d+\. |\Z)"
    match = re.search(pattern, PERSUASION_TEXT, flags=re.MULTILINE | re.DOTALL)
    if not match:
        # Try without title
        pattern = rf"^## {section_number}\. .*?(?=^## \d+\. |\Z)"
        match = re.search(pattern, PERSUASION_TEXT, flags=re.MULTILINE | re.DOTALL)
    assert match, f"Section {section_number} not found"
    return match.group(0)


def get_markdown_table_row(section_text: str, label: str) -> str:
    """Return the Markdown table row containing a bold label."""
    for line in section_text.splitlines():
        if f"**{label}**" in line:
            return line
    raise AssertionError(f"Table row not found: {label}")


FRAMEWORK_TABLE = get_section_text(1, "Choosing the Right Framework")


class TestFrameworkSelectionTable:
    """Test the framework selection table accuracy."""

    def test_pas_for_pain_aware_audiences(self):
        """PAS for pain-aware audiences (landing pages, email opens)."""
        assert "PAS" in FRAMEWORK_TABLE
        assert "Problem-Agitate-Solution" in FRAMEWORK_TABLE
        assert "feel a problem urgently" in FRAMEWORK_TABLE.lower() or "To feel a problem urgently" in FRAMEWORK_TABLE
        assert "Landing pages" in FRAMEWORK_TABLE
        assert "email opens" in FRAMEWORK_TABLE.lower()

    def test_bab_for_transformation_aspirational(self):
        """BAB for transformation/aspirational content."""
        assert "BAB" in FRAMEWORK_TABLE
        assert "Before-After-Bridge" in FRAMEWORK_TABLE
        assert "imagine a better state" in FRAMEWORK_TABLE.lower() or "To imagine a better state" in FRAMEWORK_TABLE
        assert "Case studies" in FRAMEWORK_TABLE
        assert "aspirational content" in FRAMEWORK_TABLE.lower()

    def test_aida_for_long_form_sales(self):
        """AIDA for long-form sales pages."""
        assert "AIDA" in FRAMEWORK_TABLE
        assert "Attention-Interest-Desire-Action" in FRAMEWORK_TABLE
        assert "walked through a decision" in FRAMEWORK_TABLE.lower() or "To be walked through a decision" in FRAMEWORK_TABLE
        assert "Long-form sales pages" in FRAMEWORK_TABLE
        assert "email sequences" in FRAMEWORK_TABLE.lower()

    def test_fab_for_technical_rational_buyers(self):
        """FAB for technical/rational buyers."""
        assert "FAB" in FRAMEWORK_TABLE
        assert "Features-Advantages-Benefits" in FRAMEWORK_TABLE
        assert "understand why something works" in FRAMEWORK_TABLE.lower() or "To understand why something works" in FRAMEWORK_TABLE
        assert "Product docs" in FRAMEWORK_TABLE
        assert "feature pages" in FRAMEWORK_TABLE.lower()
        assert "comparison content" in FRAMEWORK_TABLE.lower()

    def test_storybrand_for_brand_messaging(self):
        """Storybrand for brand messaging."""
        assert "Storybrand" in FRAMEWORK_TABLE
        assert "7-part framework" in FRAMEWORK_TABLE
        assert "real emotional need" in FRAMEWORK_TABLE.lower() or "To address the real emotional need" in FRAMEWORK_TABLE
        assert "Brand messaging" in FRAMEWORK_TABLE
        assert "homepage" in FRAMEWORK_TABLE.lower()
        assert "about page" in FRAMEWORK_TABLE.lower()

    def test_four_ps_for_low_friction_action(self):
        """4Ps for low-friction actions."""
        assert "4Ps" in FRAMEWORK_TABLE
        assert "Picture-Promise-Prove-Push" in FRAMEWORK_TABLE
        assert "low-friction action" in FRAMEWORK_TABLE.lower() or "To take a low-friction action" in FRAMEWORK_TABLE
        assert "Landing pages" in FRAMEWORK_TABLE
        assert "CTA optimization" in FRAMEWORK_TABLE

    def test_ssa_for_overcoming_skepticism(self):
        """SSA for overcoming skepticism."""
        assert "SSA" in FRAMEWORK_TABLE
        assert "Star-Story-Solution" in FRAMEWORK_TABLE
        assert "overcome skepticism" in FRAMEWORK_TABLE.lower() or "To overcome skepticism" in FRAMEWORK_TABLE
        assert "Case studies" in FRAMEWORK_TABLE
        assert "testimonials" in FRAMEWORK_TABLE.lower()

    def test_social_proof_framework(self):
        """Social Proof framework listed."""
        assert "Social Proof" in FRAMEWORK_TABLE
        assert "feel compelled by social proof" in FRAMEWORK_TABLE.lower() or "To feel compelled by social proof" in FRAMEWORK_TABLE


class TestPASFramework:
    """Test PAS framework section."""

    def test_pas_section_exists(self):
        pas_section = get_section_text(2, "PAS")
        assert "PAS (Problem-Agitate-Solution)" in pas_section

    def test_pas_table_structure(self):
        pas_section = get_section_text(2, "PAS")
        assert "| Stage | Job | Example |" in pas_section
        assert "Problem" in pas_section
        assert "Agitate" in pas_section
        assert "Solution" in pas_section

    def test_pas_when_to_use(self):
        pas_section = get_section_text(2, "PAS")
        assert "When to use" in pas_section
        when_use = pas_section.split("When to use")[1].split("###")[0]
        assert "Pain-point-focused content" in when_use
        assert "Before-PAS" in when_use
        assert "After-PAS" in when_use

    def test_pas_when_not_to_use(self):
        pas_section = get_section_text(2, "PAS")
        assert "When NOT to use" in pas_section
        when_not = pas_section.split("When NOT to use")[1].split("###")[0]
        assert "doesn't believe they have a problem" in when_not
        assert "research mode, not purchase mode" in when_not
        assert "problem is too trivial" in when_not

    def test_pas_variations(self):
        pas_section = get_section_text(2, "PAS")
        assert "PAS variations" in pas_section
        assert "SAP (Solution-Agitate-Problem)" in pas_section
        assert "PPS (Problem-Preview-Solution)" in pas_section


class TestBABFramework:
    """Test BAB framework section."""

    def test_bab_section_exists(self):
        bab_section = get_section_text(3, "BAB")
        assert "BAB (Before-After-Bridge)" in bab_section

    def test_bab_table_structure(self):
        bab_section = get_section_text(3, "BAB")
        assert "| Stage | Job | Example |" in bab_section
        assert "Before" in bab_section
        assert "After" in bab_section
        assert "Bridge" in bab_section

    def test_bab_when_to_use(self):
        bab_section = get_section_text(3, "BAB")
        assert "When to use" in bab_section
        when_use = bab_section.split("When to use")[1].split("###")[0]
        assert "Case studies and success stories" in when_use
        assert "Before/after content" in when_use
        assert "Aspirational products" in when_use
        assert "reader knows the \"before\" but can't see the \"after\"" in when_use

    def test_bab_why_it_works(self):
        bab_section = get_section_text(3, "BAB")
        assert "Why it works" in bab_section
        why = bab_section.split("Why it works")[1].split("###")[0]
        assert "narrative (change over time)" in why
        assert "tension" in why.lower()

    def test_bab_tip(self):
        bab_section = get_section_text(3, "BAB")
        assert "BAB tip" in bab_section
        tip = bab_section.split("BAB tip")[1].split("###")[0]
        assert "Make the After so specific" in tip


class TestAIDAFramework:
    """Test AIDA framework section."""

    def test_aida_section_exists(self):
        aida_section = get_section_text(4, "AIDA")
        assert "AIDA (Attention-Interest-Desire-Action)" in aida_section

    def test_aida_table_structure(self):
        aida_section = get_section_text(4, "AIDA")
        assert "| Stage | Job | Techniques |" in aida_section
        assert "Attention" in aida_section
        assert "Interest" in aida_section
        assert "Desire" in aida_section
        assert "Action" in aida_section

    def test_aida_full_example(self):
        aida_section = get_section_text(4, "AIDA")
        assert "Full example" in aida_section
        example = aida_section.split("Full example")[1].split("###")[0]
        assert "losing customers 2 days before they churn" in example
        assert "warning signs are sitting in your data" in example
        assert "40% reduction in churn" in example
        assert "Start your free trial" in example

    def test_aida_when_to_use(self):
        aida_section = get_section_text(4, "AIDA")
        assert "When to use" in aida_section
        when_use = aida_section.split("When to use")[1].split("###")[0]
        assert "Full landing pages and sales pages" in when_use
        assert "Email sequences" in when_use
        assert "Webinar or event promotion" in when_use

    def test_aida_when_not_to_use(self):
        aida_section = get_section_text(4, "AIDA")
        assert "When NOT to use" in aida_section
        when_not = aida_section.split("When NOT to use")[1].split("###")[0]
        assert "Short social posts" in when_not
        assert "Transactional copy where the reader already knows they want to buy" in when_not
        assert "Internal communications or enablement content" in when_not


class TestFABFramework:
    """Test FAB framework section."""

    def test_fab_section_exists(self):
        fab_section = get_section_text(5, "FAB")
        assert "FAB (Features-Advantages-Benefits)" in fab_section

    def test_fab_table_structure(self):
        fab_section = get_section_text(5, "FAB")
        assert "| Layer | Job | Example |" in fab_section
        assert "Feature" in fab_section
        assert "Advantage" in fab_section
        assert "Benefit" in fab_section

    def test_fab_test(self):
        fab_section = get_section_text(5, "FAB")
        assert "The FAB test" in fab_section
        test = fab_section.split("The FAB test")[1].split("###")[0]
        assert "\"So what?\"" in test
        assert "256-bit AES encryption" in test
        assert "Your data is encrypted in transit and at rest" in test
        assert "protected from breach liability" in test

    def test_fab_when_to_use(self):
        fab_section = get_section_text(5, "FAB")
        assert "When to use" in fab_section
        when_use = fab_section.split("When to use")[1].split("###")[0]
        assert "Feature pages and product comparisons" in when_use
        assert "Technical audiences" in when_use
        assert "Competitive content" in when_use
        assert "rational buyer" in when_use

    def test_fab_audience_adaptation(self):
        fab_section = get_section_text(5, "FAB")
        assert "FAB + audience" in fab_section
        audience = fab_section.split("FAB + audience")[1].split("###")[0]
        assert "**Consumer**: Emphasize benefits heavily" in audience
        assert "**Technical**: Show features, then advantages" in audience
        assert "**Executive**: Show advantages and benefits" in audience


class TestStoryBrandFramework:
    """Test StoryBrand framework section."""

    def test_storybrand_section_exists(self):
        sb_section = get_section_text(6, "Storybrand")
        assert "Storybrand (7-Part Framework)" in sb_section

    def test_storybrand_7_parts(self):
        sb_section = get_section_text(6, "Storybrand")
        parts = [
            "**A Hero** (the customer, not your brand)",
            "**Has a Problem** (external / internal / philosophical)",
            "**Meets a Guide** (your brand: not the hero, but the Yoda)",
            "**Who Gives Them a Plan** (clear steps)",
            "**And Calls Them to Action** (direct, no ambiguity)",
            "**That Helps Them Avoid Failure** (the stakes of inaction)",
            "**And Ends in Success** (the transformed state)",
        ]
        for part in parts:
            assert part in sb_section

    def test_storybrand_when_to_use(self):
        sb_section = get_section_text(6, "Storybrand")
        assert "When to use" in sb_section
        when_use = sb_section.split("When to use")[1].split("###")[0]
        assert "Homepage and brand messaging" in when_use
        assert "About page and mission statements" in when_use
        assert "brand needs to position itself as a guide, not a hero" in when_use

    def test_storybrand_how_to_apply(self):
        sb_section = get_section_text(6, "Storybrand")
        assert "How to apply to content" in sb_section
        apply = sb_section.split("How to apply to content")[1].split("###")[0]
        assert "Instead of \"we built this amazing feature\"" in apply
        assert "you (the hero) were struggling" in apply


class TestFourPsFramework:
    """Test 4Ps framework section."""

    def test_four_ps_section_exists(self):
        fourp_section = get_section_text(7, "4Ps")
        assert "4Ps (Picture-Promise-Prove-Push)" in fourp_section

    def test_four_ps_table(self):
        fourp_section = get_section_text(7, "4Ps")
        assert "| Stage | Job |" in fourp_section
        assert "Picture" in fourp_section
        assert "Promise" in fourp_section
        assert "Prove" in fourp_section
        assert "Push" in fourp_section


class TestFourUFramework:
    """Test 4U Copywriting Formula section."""

    def test_four_u_section_exists(self):
        fouru_section = get_section_text(8, "4U")
        assert "4U Copywriting Formula" in fouru_section

    def test_four_u_dimensions_table(self):
        fouru_section = get_section_text(8, "4U")
        assert "| Dimension | What it measures | Low score | High score |" in fouru_section
        assert "Urgent" in fouru_section
        assert "Unique" in fouru_section
        assert "Useful" in fouru_section
        assert "Ultra-specific" in fouru_section

    def test_four_u_usage_note(self):
        fouru_section = get_section_text(8, "4U")
        assert "When feedback says copy is \"boring\" or \"doesn't convert,\"" in fouru_section
        assert "re-score on these 4 dimensions" in fouru_section
        assert "fix the lowest one" in fouru_section


class TestSSAFramework:
    """Test SSA framework section."""

    def test_ssa_section_exists(self):
        ssa_section = get_section_text(9, "SSA")
        assert "SSA (Star-Story-Solution)" in ssa_section

    def test_ssa_table(self):
        ssa_section = get_section_text(9, "SSA")
        assert "| Stage | Job |" in ssa_section
        assert "Star" in ssa_section
        assert "Story" in ssa_section
        assert "Solution" in ssa_section

    def test_ssa_difference_from_pas_bab(self):
        ssa_section = get_section_text(9, "SSA")
        assert "key difference from PAS and BAB" in ssa_section
        assert "focus is on a specific person's journey" in ssa_section


class TestObjectionHandlingFrameworks:
    """Test the 5 objection-handling frameworks."""

    def test_objection_section_exists(self):
        obj_section = get_section_text(10, "Objection-Handling")
        assert "5 Objection-Handling Frameworks" in obj_section

    def test_all_5_frameworks_present(self):
        obj_section = get_section_text(10, "Objection-Handling")
        frameworks = [
            "Feel-Felt-Found",
            "Pros-Cons-Honest",
            "Even-If",
            "What-This-Isn't",
            "Liked-Loved-Loathed",
        ]
        for fw in frameworks:
            assert fw in obj_section

    def test_feel_felt_found_example(self):
        obj_section = get_section_text(10, "Objection-Handling")
        assert "Feel → felt → found" in obj_section
        assert "I get how you feel" in obj_section
        assert "Others felt that way" in obj_section
        assert "Here's what they found" in obj_section

    def test_pros_cons_honest(self):
        obj_section = get_section_text(10, "Objection-Handling")
        assert "Pros → cons → decision" in obj_section
        assert "Gains:" in obj_section
        assert "Losses:" in obj_section

    def test_even_if(self):
        obj_section = get_section_text(10, "Objection-Handling")
        assert "Even if scenario" in obj_section
        assert "Even with just this, it pays off" in obj_section

    def test_what_this_isnt(self):
        obj_section = get_section_text(10, "Objection-Handling")
        assert "Not about X" in obj_section
        assert "Not about replacing you" in obj_section
        assert "About removing tedious work" in obj_section

    def test_liked_loved_loathed(self):
        obj_section = get_section_text(10, "Objection-Handling")
        assert "Liked/loved/loathed" in obj_section
        assert "Liked:" in obj_section
        assert "Loved:" in obj_section
        assert "Loathed:" in obj_section


class TestCialdiniPrinciples:
    """Test Cialdini's 7 persuasion principles."""

    def test_cialdini_section_exists(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        assert "Adding Persuasion to Any Framework" in cialdini

    def test_all_7_principles_present(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        principles = [
            "Reciprocity",
            "Scarcity",
            "Authority",
            "Consistency",
            "Liking",
            "Social Proof",
            "Unity",
        ]
        for p in principles:
            assert p in cialdini

    def test_reciprocity_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        rec = get_markdown_table_row(cialdini, "Reciprocity")
        assert "Give valuable free content first" in rec
        assert "templates, guides" in rec
        assert "before asking for the sale" in rec

    def test_scarcity_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        scarc = get_markdown_table_row(cialdini, "Scarcity")
        assert "Genuine time limits" in scarc
        assert "limited spots" in scarc
        assert "exclusive access" in scarc

    def test_authority_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        auth = get_markdown_table_row(cialdini, "Authority")
        assert "Expert quotes" in auth
        assert "credentials" in auth
        assert "certifications" in auth
        assert "media mentions" in auth

    def test_consistency_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        cons = get_markdown_table_row(cialdini, "Consistency")
        assert "Remind them of previous actions" in cons
        assert "stated beliefs" in cons

    def test_liking_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        like = get_markdown_table_row(cialdini, "Liking")
        assert "Relatable voice" in like
        assert "shared values" in like
        assert "brand personality" in like

    def test_social_proof_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        sp = get_markdown_table_row(cialdini, "Social Proof")
        assert "Testimonials" in sp
        assert "customer counts" in sp
        assert "case studies" in sp
        assert "reviews" in sp

    def test_unity_usage(self):
        cialdini = get_section_text(11, "Adding Persuasion")
        unity = get_markdown_table_row(cialdini, "Unity")
        assert "We're in this together" in unity
        assert "community-driven brand" in unity
        assert "shared identity" in unity


class TestFrameworkSelectionQuickReference:
    """Test the quick reference table."""

    def test_quick_reference_table_exists(self):
        qr_section = get_section_text(12, "Framework Selection Quick Reference")
        assert "Framework Selection Quick Reference" in qr_section

    def test_quick_reference_mappings(self):
        qr_section = get_section_text(12, "Framework Selection Quick Reference")
        mappings = [
            ("Get someone to try a free trial", "PAS or 4Ps"),
            ("Sell to skeptical buyers", "BAB + SSA"),
            ("Present a case study", "BAB or SSA"),
            ("Write a homepage", "Storybrand or 4Ps"),
            ("Write a product/feature page", "FAB"),
            ("Write an email sequence", "AIDA"),
            ("Launch a new product", "BAB"),
            ("Write comparison content", "FAB"),
            ("Write thought leadership", "4U or contrast framework"),
            ("Overcome price objections", "Value reframe + FAB"),
        ]
        for goal, framework in mappings:
            assert goal in qr_section
            assert framework in qr_section


class TestFrameworkContentFixtures:
    """Test that the content fixtures in conftest.py match framework structures."""

    def test_pas_fixture_structure(self, pas_content):
        """PAS content has Problem, Agitate, Solution."""
        assert "manually compiling reports" in pas_content  # Problem
        assert "72 hours a year" in pas_content  # Agitate
        assert "ReportAI connects" in pas_content  # Solution

    def test_bab_fixture_structure(self, bab_content):
        """BAB content has Before, After, Bridge."""
        assert "Before Acme" in bab_content
        assert "Now, they respond" in bab_content
        assert "Acme's AI draft engine" in bab_content

    def test_aida_fixture_structure(self, aida_content):
        """AIDA content has Attention, Interest, Desire, Action."""
        assert "losing customers" in aida_content  # Attention
        assert "warning signs are sitting in your data" in aida_content  # Interest
        assert "40% reduction in churn" in aida_content  # Desire
        assert "Start your free trial" in aida_content  # Action

    def test_fab_fixture_structure(self, fab_content):
        """FAB content has Feature, Advantage, Benefit."""
        assert "Feature:" in fab_content
        assert "Advantage:" in fab_content
        assert "Benefit:" in fab_content
        assert "256-bit AES encryption" in fab_content
        assert "encrypted both in transit and at rest" in fab_content
        assert "customer data is unreadable" in fab_content

    def test_storybrand_fixture_structure(self, storybrand_content):
        """StoryBrand content has 7 parts."""
        assert "hero" in storybrand_content.lower()
        assert "problem" in storybrand_content.lower()
        assert "guide" in storybrand_content.lower()
        assert "plan" in storybrand_content.lower()
        assert "action" in storybrand_content.lower()
        assert "failure" in storybrand_content.lower()
        assert "success" in storybrand_content.lower()

    def test_four_u_fixture_scores(self, four_u_scores):
        """4U fixture has all 4 dimensions with high and low examples."""
        assert "high_urgent" in four_u_scores
        assert "high_unique" in four_u_scores
        assert "high_useful" in four_u_scores
        assert "high_ultra_specific" in four_u_scores
        assert "low_all" in four_u_scores

        # Check content quality
        assert "trial ends tomorrow" in four_u_scores["high_urgent"]
        assert "last 3 agencies couldn't" in four_u_scores["high_unique"]
        assert "6 hours to 30 minutes" in four_u_scores["high_useful"]
        assert "7.2% to 4.1% in 60 days" in four_u_scores["high_ultra_specific"]
        assert "quality service for your business needs" in four_u_scores["low_all"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])