"""
Validation Module
=================
SEO and DEI/Accessibility validators for the content pipeline.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import re
import json

from content_writer_skill.models import (
    ContentBrief, ContentOutline, ContentDraft,
    SEOAudit, DEIResult, DEIFinding, LintSeverity, ValidationGateResult
)


@dataclass
class SEOValidator:
    """
    SEO Audit Validator

    Checks:
    - Keyword placement and density
    - Heading structure (H1, H2, H3 hierarchy)
    - Meta title/description optimization
    - Readability (Flesch-Kincaid)
    - E-E-A-T signals
    """

    strict: bool = False

    def audit(self, content: str, brief: ContentBrief,
              outline: Optional[ContentOutline] = None) -> SEOAudit:
        """
        Run full SEO audit on content.

        Args:
            content: Drafted content
            brief: Content brief with target keywords
            outline: Optional outline for structure validation

        Returns:
            SEOAudit with scores and issues
        """
        audit = SEOAudit()

        # Extract primary keyword
        primary_kw = self._get_primary_keyword(brief, outline)
        audit.primary_keyword = primary_kw

        # Keyword analysis
        self._analyze_keywords(content, primary_kw, brief, outline, audit)

        # Structure analysis
        self._analyze_structure(content, outline, audit)

        # Metadata analysis
        self._analyze_metadata(content, brief, outline, audit)

        # Readability analysis
        self._analyze_readability(content, audit)

        # E-E-A-T signals
        self._analyze_eeat(content, brief, audit)

        # Calculate overall score
        audit.overall_score = self._calculate_overall_score(audit)

        return audit

    def _get_primary_keyword(self, brief: ContentBrief,
                             outline: Optional[ContentOutline]) -> str:
        """Extract primary keyword from brief/outline."""
        if outline and outline.seo and outline.seo.primary_keyword:
            return outline.seo.primary_keyword
        if brief and brief.primary_keyword:
            return brief.primary_keyword
        if brief and brief.metadata.get("primary_keyword"):
            return brief.metadata["primary_keyword"]
        # Fallback: extract from angle
        if brief and brief.angle:
            words = brief.angle.lower().split()
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                          'of', 'with', 'by', 'is', 'are', 'was', 'were', 'how', 'why', 'what',
                          "today's", "today", 'world', 'important', 'this', 'that', 'these', 'those',
                          'you', 'your', 'we', 'our', 'us', 'i', 'me', 'my', 'it', 'its', 'as'}
            for w in words:
                # Clean punctuation
                w_clean = w.strip(".,!?;:'\"()[]{}")
                if w_clean not in stop_words and len(w_clean) > 3 and w_clean.isalpha():
                    return w_clean
        return "topic"

    def _analyze_keywords(self, content: str, primary_kw: str,
                          brief: ContentBrief, outline: Optional[ContentOutline], audit: SEOAudit) -> None:
        """Analyze keyword usage."""
        content_lower = content.lower()
        word_count = len(content.split())

        # Primary keyword count
        primary_count = content_lower.count(primary_kw.lower())
        audit.primary_keyword_count = primary_count
        audit.primary_keyword_density = round(primary_count / word_count * 100, 2) if word_count > 0 else 0

        # Check placement
        audit.primary_keyword_in_title = primary_kw.lower() in content[:200].lower()
        audit.primary_keyword_in_h1 = primary_kw.lower() in self._get_h1(content).lower()
        audit.primary_keyword_in_first_100 = primary_kw.lower() in content[:500].lower()
        audit.primary_keyword_in_headings = self._count_keyword_in_headings(content, primary_kw)

        # Density checks
        if audit.primary_keyword_density < 0.5:
            audit.add_issue("LOW_KEYWORD_DENSITY",
                           f"Primary keyword '{primary_kw}' density is {audit.primary_keyword_density}% (target: 0.5-2%)",
                           "warning",
                           suggestion=f"Include '{primary_kw}' more naturally throughout content")
        elif audit.primary_keyword_density > 3.0:
            audit.add_issue("HIGH_KEYWORD_DENSITY",
                           f"Primary keyword '{primary_kw}' density is {audit.primary_keyword_density}% (may be keyword stuffing)",
                           "warning",
                           suggestion="Reduce keyword frequency, use variations")

        # Secondary keywords
        secondary = self._get_secondary_keywords(brief, outline)
        for kw in secondary:
            count = content_lower.count(kw.lower())
            if count > 0:
                audit.secondary_keywords_found[kw] = count
                audit.secondary_keyword_density[kw] = round(count / word_count * 100, 2)

        # Keyword score
        audit.keyword_score = self._score_keywords(audit)

    def _analyze_structure(self, content: str, outline: Optional[ContentOutline],
                           audit: SEOAudit) -> None:
        """Analyze heading structure."""
        headings = re.findall(r'^(#{1,3})\s+(.+)$', content, re.MULTILINE)

        h1_count = sum(1 for h, _ in headings if len(h) == 1)
        h2_count = sum(1 for h, _ in headings if len(h) == 2)
        h3_count = sum(1 for h, _ in headings if len(h) == 3)

        audit.h1_count = h1_count
        audit.h2_count = h2_count
        audit.h3_count = h3_count

        # Check hierarchy
        prev_level = 0
        hierarchy_valid = True
        for h, text in headings:
            level = len(h)
            if prev_level > 0 and level > prev_level + 1:
                hierarchy_valid = False
                audit.add_issue("HEADING_HIERARCHY_SKIP",
                               f"Heading jumps from H{prev_level} to H{level}: '{text}'",
                               "warning")
            prev_level = level

        audit.heading_structure_valid = hierarchy_valid

        if h1_count == 0:
            audit.add_issue("MISSING_H1", "No H1 heading found", "error")
        elif h1_count > 1:
            audit.add_issue("MULTIPLE_H1", f"Found {h1_count} H1 headings (should be 1)", "warning")

        # Compare with outline
        if outline:
            outline_headings = [s.heading for s in outline.sections]
            content_headings = [text for _, text in headings if len(_) >= 2]
            missing = [h for h in outline_headings if h not in content_headings]
            if missing:
                audit.add_issue("MISSING_OUTLINE_SECTIONS",
                               f"Missing {len(missing)} planned sections: {', '.join(missing[:3])}",
                               "error")

        audit.structure_score = 100 if hierarchy_valid and h1_count == 1 else 70

    def _analyze_metadata(self, content: str, brief: ContentBrief,
                          outline: Optional[ContentOutline], audit: SEOAudit) -> None:
        """Analyze meta title and description."""
        # Extract or generate meta title
        h1 = self._get_h1(content)
        if outline and outline.seo and outline.seo.meta_title:
            audit.meta_title = outline.seo.meta_title
        else:
            audit.meta_title = h1[:60] if h1 else "Untitled"

        audit.meta_title_length = len(audit.meta_title)
        if audit.meta_title_length > 60:
            audit.add_issue("META_TITLE_TOO_LONG",
                           f"Meta title is {audit.meta_title_length} chars (max 60)",
                           "warning",
                           suggestion="Shorten to under 60 characters")
        elif audit.meta_title_length < 30:
            audit.add_issue("META_TITLE_TOO_SHORT",
                           f"Meta title is {audit.meta_title_length} chars (min 30)",
                           "info",
                           suggestion="Expand to 30-60 characters")

        # Meta description
        if outline and outline.seo and outline.seo.meta_description:
            audit.meta_description = outline.seo.meta_description
        else:
            # Generate from first paragraph
            first_para = content.split('\n\n')[1] if '\n\n' in content else content[:160]
            audit.meta_description = first_para[:155]

        audit.meta_description_length = len(audit.meta_description)
        if audit.meta_description_length > 155:
            audit.add_issue("META_DESC_TOO_LONG",
                           f"Meta description is {audit.meta_description_length} chars (max 155)",
                           "warning")
        elif audit.meta_description_length < 120:
            audit.add_issue("META_DESC_TOO_SHORT",
                           f"Meta description is {audit.meta_description_length} chars (min 120)",
                           "info")

        # H1 matches title
        audit.h1_matches_title = h1.strip().lower() == audit.meta_title.strip().lower() if h1 else False
        audit.h1_present = bool(h1)

        audit.metadata_score = self._score_metadata(audit)

    def _analyze_readability(self, content: str, audit: SEOAudit) -> None:
        """Calculate readability scores (Flesch-Kincaid)."""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = content.split()
        syllables = sum(self._count_syllables(w) for w in words)

        if sentences and words:
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables_per_word = syllables / len(words)

            audit.avg_sentence_length = round(avg_sentence_length, 1)
            audit.avg_syllables_per_word = round(avg_syllables_per_word, 2)

            # Flesch Reading Ease
            audit.flesch_reading_ease = round(
                206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word, 1
            )

            # Flesch-Kincaid Grade Level
            audit.flesch_kincaid_grade = round(
                0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59, 1
            )

            # Score readability (target: grade 8-10, ease 60-70)
            if 60 <= audit.flesch_reading_ease <= 70:
                audit.readability_score = 100
            elif 50 <= audit.flesch_reading_ease < 60:
                audit.readability_score = 80
            elif audit.flesch_reading_ease < 30:
                audit.readability_score = 40
                audit.add_issue("LOW_READABILITY",
                               f"Flesch Reading Ease is {audit.flesch_reading_ease} (very difficult)",
                               "warning",
                               suggestion="Simplify sentences, use shorter words")
            else:
                audit.readability_score = 60

    def _analyze_eeat(self, content: str, brief: ContentBrief, audit: SEOAudit) -> None:
        """Analyze E-E-A-T signals."""
        signals = {}
        content_lower = content.lower()

        # Experience signals
        exp_patterns = ['i ', 'my ', 'we ', 'our ', 'in my experience', 'i found', 'i tested',
                        'case study', 'example:', 'for instance', 'specifically']
        exp_count = sum(1 for p in exp_patterns if p in content_lower)
        signals["experience_signals"] = exp_count

        # Expertise signals
        exp_patterns = ['research', 'study', 'data', 'according to', 'source:', 'citation',
                        'expert', 'specialist', 'certified', 'published', 'peer-reviewed']
        exp_count = sum(1 for p in exp_patterns if p in content_lower)
        signals["expertise_signals"] = exp_count

        # Authoritativeness signals
        auth_patterns = ['official', 'industry standard', 'best practice', 'framework',
                         'methodology', 'proven', 'benchmark', 'leading']
        auth_count = sum(1 for p in auth_patterns if p in content_lower)
        signals["authoritativeness_signals"] = auth_count

        # Trustworthiness signals
        trust_patterns = ['disclaimer', 'transparent', 'honest', 'limitation', 'caveat',
                          'however', 'note:', 'important:', 'warning:']
        trust_count = sum(1 for p in trust_patterns if p in content_lower)
        signals["trustworthiness_signals"] = trust_count

        audit.eeat_signals = signals
        audit.eeat_score = min(100, sum(signals.values()) * 2)

        if audit.eeat_score < 30:
            audit.add_issue("LOW_EEAT",
                           "Content lacks strong E-E-A-T signals (experience, expertise, authority, trust)",
                           "info",
                           suggestion="Add personal experience, cite sources, demonstrate expertise")

    def _calculate_overall_score(self, audit: SEOAudit) -> int:
        """Calculate weighted overall SEO score."""
        weights = {
            "keyword": 0.25,
            "structure": 0.20,
            "metadata": 0.15,
            "readability": 0.20,
            "eeat": 0.20,
        }

        scores = {
            "keyword": audit.keyword_score,
            "structure": audit.structure_score,
            "metadata": audit.metadata_score,
            "readability": audit.readability_score,
            "eeat": audit.eeat_score,
        }

        return int(sum(scores[k] * weights[k] for k in weights))

    def _score_keywords(self, audit: SEOAudit) -> int:
        """Score keyword optimization."""
        score = 50  # base

        # Primary keyword presence
        if audit.primary_keyword_count > 0:
            score += 20
        if audit.primary_keyword_in_h1:
            score += 10
        if audit.primary_keyword_in_first_100:
            score += 10

        # Density
        if 0.5 <= audit.primary_keyword_density <= 2.5:
            score += 10
        elif audit.primary_keyword_density > 3:
            score -= 20

        return max(0, min(100, score))

    def _score_metadata(self, audit: SEOAudit) -> int:
        """Score metadata optimization."""
        score = 50

        if audit.h1_present:
            score += 20
        if audit.h1_matches_title:
            score += 10
        if 30 <= audit.meta_title_length <= 60:
            score += 10
        if 120 <= audit.meta_description_length <= 155:
            score += 10

        return max(0, min(100, score))

    def _count_syllables(self, word: str) -> int:
        """Approximate syllable count for a word."""
        word = word.lower()
        if len(word) <= 3:
            return 1
        vowels = 'aeiouy'
        count = 0
        prev_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith('e'):
            count -= 1
        return max(1, count)

    def _get_h1(self, content: str) -> str:
        """Extract H1 from content."""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else ""

    def _count_keyword_in_headings(self, content: str, keyword: str) -> int:
        """Count keyword occurrences in headings."""
        headings = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
        return sum(1 for h in headings if keyword.lower() in h.lower())

    def _get_secondary_keywords(self, brief: ContentBrief,
                                 outline: Optional[ContentOutline]) -> List[str]:
        """Get secondary keywords."""
        keywords = []
        if outline and outline.seo and outline.seo.secondary_keywords:
            keywords.extend(outline.seo.secondary_keywords)
        if brief and brief.metadata.get("secondary_keywords"):
            keywords.extend(brief.metadata["secondary_keywords"])
        return list(set(keywords))[:10]


@dataclass
class DEIValidator:
    """
    DEI / Accessibility Validator

    Checks:
    - Inclusive language (gendered terms, ableist language, etc.)
    - Accessibility (heading structure, alt text hints, link text)
    - Bias detection (stereotypes, assumptions)
    - Readability for diverse audiences
    """

    strict: bool = False

    # Inclusive language patterns
    NON_INCLUSIVE_PATTERNS = {
        "guys": ("gendered", "folks, team, everyone, people"),
        "man hours": ("gendered", "person hours, work hours, effort hours"),
        "manpower": ("gendered", "workforce, staffing, personnel"),
        "chairman": ("gendered", "chair, chairperson"),
        "salesman": ("gendered", "salesperson, sales rep"),
        "policeman": ("gendered", "police officer"),
        "fireman": ("gendered", "firefighter"),
        "businessman": ("gendered", "business person, executive"),
        "craftsman": ("gendered", "artisan, craftsperson"),
        "middleman": ("gendered", "intermediary, go-between"),
        "spokesman": ("gendered", "spokesperson"),
        "layman": ("gendered", "layperson, non-expert"),
        "man-made": ("gendered", "artificial, synthetic, human-made"),
        "master": ("racial", "primary, main, leader, controller"),
        "slave": ("racial", "replica, follower, secondary"),
        "blacklist": ("racial", "blocklist, denylist, reject list"),
        "whitelist": ("racial", "allowlist, safelist, approve list"),
        "grandfather clause": ("racial", "legacy clause, existing condition"),
        "sanity check": ("ableist", "reality check, coherence check, validation"),
        "crazy": ("ableist", "wild, intense, extreme, unusual"),
        "insane": ("ableist", "incredible, unbelievable, extreme"),
        "lame": ("ableist", "weak, poor, ineffective"),
        "dumb": ("ableist", "unclear, confusing, silent"),
        "blind spot": ("ableist", "gap, oversight, missing perspective"),
        "turn a blind eye": ("ableist", "ignore, overlook"),
        "fall on deaf ears": ("ableist", "be ignored, go unheard"),
        "tone deaf": ("ableist", "insensitive, unaware"),
        "crippled": ("ableist", "disabled, impaired, broken"),
        "handicapped": ("ableist", "disabled, accessible"),
        "suffers from": ("ableist", "has, lives with, experiences"),
        "victim of": ("ableist", "person with, survivor of"),
        "confined to wheelchair": ("ableist", "uses a wheelchair, wheelchair user"),
        "normal": ("ableist", "typical, standard, average"),
        "healthy": ("ableist", "non-disabled, without disability"),
        "elderly": ("ageist", "older adults, seniors, older people"),
        "senile": ("ageist", "cognitive decline, dementia"),
        "young and naive": ("ageist", "inexperienced, new to"),
        "digital native": ("ageist", "tech-savvy, familiar with technology"),
        "cultural fit": ("bias", "values alignment, culture add"),
        "ninja": ("cultural", "expert, specialist, master"),
        "guru": ("cultural", "expert, authority, specialist"),
        "rockstar": ("cultural", "top performer, exceptional"),
        "hacker": ("cultural", "problem solver, innovator"),
        "tribe": ("cultural", "team, group, community"),
        "spirit animal": ("cultural", "kindred spirit, inspiration"),
        "powwow": ("cultural", "meeting, huddle, discussion"),
        "low on the totem pole": ("cultural", "junior, entry-level"),
        "circle the wagons": ("cultural", "regroup, align, coordinate"),
        "hold down the fort": ("cultural", "manage, maintain, oversee"),
        "off the reservation": ("cultural", "off script, unexpected"),
        "Indian giver": ("cultural", "someone who takes back a gift"),
        "peanut gallery": ("cultural", "audience, observers, critics"),
        "long time no see": ("cultural", "haven't seen you in a while"),
        "no can do": ("cultural", "can't do that, not possible"),
    }

    # Accessibility checks
    ACCESSIBILITY_RULES = {
        "vague_link_text": (
            r'\[.*?(?:click here|read more|learn more|here|this link|link)\].*?\]',
            "Link text should be descriptive, not 'click here' or 'read more'",
        ),
        "missing_alt_text": (
            r'!\[.*?\]\([^)]+\)',
            "Images should have descriptive alt text",
        ),
    }

    def validate(self, content: str, brief: ContentBrief) -> DEIResult:
        """
        Run DEI/accessibility validation.

        Args:
            content: Drafted content
            brief: Content brief

        Returns:
            DEIResult with findings and scores
        """
        result = DEIResult()
        content_lower = content.lower()

        # Check inclusive language
        self._check_inclusive_language(content, content_lower, result)

        # Check accessibility
        self._check_accessibility(content, result)

        # Check bias
        self._check_bias(content, content_lower, result)

        # Calculate scores
        result.inclusive_language_score = self._calc_inclusive_score(result)
        result.accessibility_score = self._calc_accessibility_score(result)
        result.bias_score = self._calc_bias_score(result)

        # Overall pass/fail
        result.passed = (result.get_alert_count() == 0 and
                        (not self.strict or result.get_warning_count() == 0))

        return result

    def _check_inclusive_language(self, content: str, content_lower: str, result: DEIResult) -> None:
        """Check for non-inclusive language."""
        for term, (category, suggestion) in self.NON_INCLUSIVE_PATTERNS.items():
            # Find all occurrences with context
            for match in re.finditer(re.escape(term), content_lower):
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end]

                result.findings.append(DEIFinding(
                    category="inclusive_language",
                    rule_id=f"NON_INCLUSIVE_{term.upper().replace(' ', '_')}",
                    message=f"Potentially non-inclusive term: '{term}'",
                    severity=LintSeverity.WARNING,
                    location=f"Position {match.start()}",
                    suggestion=f"Consider: {suggestion}",
                    auto_fixable=True,
                ))

    def _check_accessibility(self, content: str, result: DEIResult) -> None:
        """Check accessibility issues."""
        # Check link text
        link_pattern = r'\[([^\]]+)\]\([^)]+\)'
        for match in re.finditer(link_pattern, content):
            link_text = match.group(1).lower().strip()
            if link_text in ('click here', 'read more', 'learn more', 'here', 'this link', 'link'):
                result.findings.append(DEIFinding(
                    category="accessibility",
                    rule_id="VAGUE_LINK_TEXT",
                    message=f"Vague link text: '{match.group(1)}' - not accessible for screen readers",
                    severity=LintSeverity.ALERT,
                    location=f"Position {match.start()}",
                    suggestion="Use descriptive link text that explains the destination",
                    auto_fixable=False,
                ))

        # Check for images without alt text (markdown images)
        img_pattern = r'!\[([^\]]*)\]\([^)]+\)'
        for match in re.finditer(img_pattern, content):
            alt_text = match.group(1).strip()
            if not alt_text:
                result.findings.append(DEIFinding(
                    category="accessibility",
                    rule_id="MISSING_ALT_TEXT",
                    message="Image missing alt text",
                    severity=LintSeverity.ALERT,
                    location=f"Position {match.start()}",
                    suggestion="Add descriptive alt text for screen readers",
                    auto_fixable=False,
                ))
            elif len(alt_text) < 5:
                result.findings.append(DEIFinding(
                    category="accessibility",
                    rule_id="INSUFFICIENT_ALT_TEXT",
                    message=f"Image alt text too brief: '{alt_text}'",
                    severity=LintSeverity.WARNING,
                    location=f"Position {match.start()}",
                    suggestion="Provide more descriptive alt text (10+ chars)",
                    auto_fixable=False,
                ))

        # Check heading structure (already done in SEO but also accessibility)
        headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        prev_level = 0
        for hashes, text in headings:
            level = len(hashes)
            if prev_level > 0 and level > prev_level + 1:
                result.findings.append(DEIFinding(
                    category="accessibility",
                    rule_id="HEADING_SKIP",
                    message=f"Heading jumps from H{prev_level} to H{level}: '{text}'",
                    severity=LintSeverity.WARNING,
                    location=text,
                    suggestion="Use sequential heading levels for screen reader navigation",
                    auto_fixable=False,
                ))
            prev_level = level

    def _check_bias(self, content: str, content_lower: str, result: DEIResult) -> None:
        """Check for potential bias."""
        # Check for gender assumptions
        gender_assumptions = [
            (r'\b(he|she)\s+(should|must|needs to|has to)\b', "gender_assumption"),
            (r'\b(men|women)\s+(are|tend to|usually)\b', "gender_generalization"),
            (r'\b(guys|girls)\s+(who|that)\b', "gendered_group"),
        ]

        for pattern, category in gender_assumptions:
            for match in re.finditer(pattern, content_lower):
                result.findings.append(DEIFinding(
                    category="bias",
                    rule_id=f"GENDER_BIAS_{category.upper()}",
                    message=f"Potential gender bias: '{match.group()}'",
                    severity=LintSeverity.WARNING,
                    location=f"Position {match.start()}",
                    suggestion="Use gender-neutral language",
                    auto_fixable=False,
                ))

        # Check for age assumptions
        age_patterns = [
            (r'\b(digital native|tech-savvy|young)\s+(people|employees|workers)\b', "age_stereotype"),
            (r'\b(older|elderly|senior)\s+(people|employees|workers)\b', "age_stereotype"),
        ]

        for pattern, category in age_patterns:
            for match in re.finditer(pattern, content_lower):
                result.findings.append(DEIFinding(
                    category="bias",
                    rule_id=f"AGE_BIAS_{category.upper()}",
                    message=f"Potential age bias: '{match.group()}'",
                    severity=LintSeverity.WARNING,
                    location=f"Position {match.start()}",
                    suggestion="Focus on skills/experience, not age",
                    auto_fixable=False,
                ))

        # Check for cultural assumptions
        cultural_patterns = [
            (r'\b(american|western|standard)\s+(way|approach|method)\b', "cultural_bias"),
            (r'\b(everyone|anyone|nobody)\s+(knows|understands|does)\b', "universal_assumption"),
        ]

        for pattern, category in cultural_patterns:
            for match in re.finditer(pattern, content_lower):
                result.findings.append(DEIFinding(
                    category="bias",
                    rule_id=f"CULTURAL_BIAS_{category.upper()}",
                    message=f"Potential cultural assumption: '{match.group()}'",
                    severity=LintSeverity.INFO,
                    location=f"Position {match.start()}",
                    suggestion="Consider global audience, avoid universal claims",
                    auto_fixable=False,
                ))

    def _calc_inclusive_score(self, result: DEIResult) -> float:
        """Calculate inclusive language score."""
        lang_findings = [f for f in result.findings if f.category == "inclusive_language"]
        if not lang_findings:
            return 100.0
        alerts = sum(1 for f in lang_findings if f.severity == LintSeverity.ALERT)
        warnings = sum(1 for f in lang_findings if f.severity == LintSeverity.WARNING)
        return max(0, 100 - alerts * 20 - warnings * 10)

    def _calc_accessibility_score(self, result: DEIResult) -> float:
        """Calculate accessibility score."""
        a11y_findings = [f for f in result.findings if f.category == "accessibility"]
        if not a11y_findings:
            return 100.0
        alerts = sum(1 for f in a11y_findings if f.severity == LintSeverity.ALERT)
        warnings = sum(1 for f in a11y_findings if f.severity == LintSeverity.WARNING)
        return max(0, 100 - alerts * 15 - warnings * 5)

    def _calc_bias_score(self, result: DEIResult) -> float:
        """Calculate bias score."""
        bias_findings = [f for f in result.findings if f.category == "bias"]
        if not bias_findings:
            return 100.0
        alerts = sum(1 for f in bias_findings if f.severity == LintSeverity.ALERT)
        warnings = sum(1 for f in bias_findings if f.severity == LintSeverity.WARNING)
        info = sum(1 for f in bias_findings if f.severity == LintSeverity.INFO)
        return max(0, 100 - alerts * 25 - warnings * 10 - info * 5)


def validate_brief(brief: ContentBrief) -> ValidationGateResult:
    """Validate a ContentBrief (Phase 1 / Gate 1)."""
    from content_writer_skill.phases.phase1_discover import DiscoverAlignPhase
    return DiscoverAlignPhase()._validate_brief(brief)


def validate_outline(outline: ContentOutline, brief: ContentBrief) -> ValidationGateResult:
    """Validate a ContentOutline against the brief (Phase 2 / Gate 2)."""
    from content_writer_skill.phases.phase2_outline import OutlinePhase
    return OutlinePhase()._validate_outline(outline, brief)


def validate_draft(draft: ContentDraft, outline: ContentOutline,
                   brief: ContentBrief) -> ValidationGateResult:
    """Validate a ContentDraft against the outline and brief (Phase 3 / Gate 3)."""
    from content_writer_skill.phases.phase3_draft import DraftPhase
    return DraftPhase()._validate_draft(draft, outline, brief)


__all__ = [
    "SEOValidator",
    "DEIValidator",
    "validate_brief",
    "validate_outline",
    "validate_draft",
]