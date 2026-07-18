"""
Lint Engine
===========
Core linting engine for voice, style, and grammar validation.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import re

from content_writer_skill.models import ContentBrief
from content_writer_skill.models.validation_results import LintResult, LintIssue, LintSeverity
from content_writer_skill.lint.rules import (
    BANNED_OPENERS,
    ROBOTIC_TELLS,
    FORMAL_PHRASES,
    HEDGING_PHRASES,
    EM_DASH_PATTERN,
    CONTRACTION_MAP,
    SENTENCE_VARIETY_MIN,
    SENTENCE_VARIETY_MAX,
)


@dataclass
class LintEngine:
    """
    Lint engine for content validation.

    Checks:
    - Banned openers (no "In today's world", "In this article", etc.)
    - Robotic tells (no "delve", "tapestry", "unlock", etc.)
    - Formal phrase replacement (use contractions, simpler words)
    - Em-dash overuse (max 1 per 500 words)
    - Hedging language (minimize "may", "might", "could", "somewhat")
    - Sentence variety (min 30% short sentences, max 25% long sentences)
    - Voice drift detection (consistency with brief tone)
    - Grid parity (banned patterns vs target tone)
    """

    config: Optional[Dict[str, Any]] = None
    strict: bool = True

    def __post_init__(self):
        """Initialize with default config."""
        self.config = self.config or {}
        self.banned_openers = self.config.get("banned_openers", BANNED_OPENERS)
        self.robotic_tells = self.config.get("robotic_tells", ROBOTIC_TELLS)
        self.formal_phrases = self.config.get("formal_phrases", FORMAL_PHRASES)
        self.hedging_phrases = self.config.get("hedging_phrases", HEDGING_PHRASES)
        self.max_em_dash_per_500 = self.config.get("max_em_dash_per_500", 1)
        self.min_contraction_pct = self.config.get("min_contraction_pct", 5.0)
        self.max_hedging_density = self.config.get("max_hedging_density", 3.0)
        self.sentence_variety_short_min = self.config.get("sentence_variety_short_min", SENTENCE_VARIETY_MIN)
        self.sentence_variety_long_max = self.config.get("sentence_variety_long_max", SENTENCE_VARIETY_MAX)

    def lint(self, content: str, brief: Optional[ContentBrief] = None, strict: bool = True) -> LintResult:
        """
        Run all lint checks on content.

        Args:
            content: Content to lint
            brief: Optional brief for tone/voice validation
            strict: If True, ALERT severity fails validation; if False, ALERT becomes WARNING

        Returns:
            LintResult with all issues
        """
        result = LintResult()
        self.strict = strict

        # Check banned openers
        self._check_banned_openers(content, result)

        # Check robotic tells
        self._check_robotic_tells(content, result)

        # Check formal phrases
        self._check_formal_phrases(content, result)

        # Check em-dash usage
        self._check_em_dash(content, result)

        # Check hedging
        self._check_hedging(content, result)

        # Check sentence variety
        self._check_sentence_variety(content, result)

        # Check contractions
        self._check_contractions(content, result)

        # Check voice drift (if brief provided)
        if brief:
            self._check_voice_drift(content, brief, result)

        # Calculate metrics
        self._calculate_metrics(content, result)

        return result

    def _check_banned_openers(self, content: str, result: LintResult) -> None:
        """Check for banned opening phrases."""
        lines = content.split('\n')
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            line_lower = line.lower().strip()
            for opener in self.banned_openers:
                if line_lower.startswith(opener.lower()):
                    # In non-strict mode, downgrade ALERT to WARNING
                    severity = LintSeverity.ALERT if self.strict else LintSeverity.WARNING
                    result.add_issue(LintIssue(
                        rule_id="BANNED_OPENER",
                        message=f"Banned opener detected: '{opener}'",
                        severity=severity,
                        line=i + 1,
                        suggestion=f"Start with a hook: question, bold claim, story, or statistic",
                        auto_fixable=False,
                        context=line[:100],
                    ))

    def _check_robotic_tells(self, content: str, result: LintResult) -> None:
        """Check for AI/robotic tell words."""
        content_lower = content.lower()
        for tell in self.robotic_tells:
            pattern = r'\b' + re.escape(tell.lower()) + r'\b'
            matches = list(re.finditer(pattern, content_lower))
            for match in matches:
                start = max(0, match.start() - 40)
                end = min(len(content), match.end() + 40)
                context = content[start:end]

                result.add_issue(LintIssue(
                    rule_id="ROBOTIC_TELL",
                    message=f"Robotic tell detected: '{tell}'",
                    severity=LintSeverity.ALERT,
                    line=content[:match.start()].count('\n') + 1,
                    suggestion=f"Replace '{tell}' with simpler, more human language",
                    auto_fixable=True,
                    context=context,
                ))

    def _check_formal_phrases(self, content: str, result: LintResult) -> None:
        """Check for overly formal phrases that should be simplified."""
        content_lower = content.lower()
        for formal, simple in self.formal_phrases.items():
            pattern = r'\b' + re.escape(formal.lower()) + r'\b'
            matches = list(re.finditer(pattern, content_lower))
            for match in matches:
                start = max(0, match.start() - 40)
                end = min(len(content), match.end() + 40)
                context = content[start:end]

                result.add_issue(LintIssue(
                    rule_id="FORMAL_PHRASE",
                    message=f"Formal phrase: '{formal}' → use '{simple}'",
                    severity=LintSeverity.WARNING,
                    line=content[:match.start()].count('\n') + 1,
                    suggestion=f"Replace with '{simple}' for more conversational tone",
                    auto_fixable=True,
                    context=context,
                ))

    def _check_em_dash(self, content: str, result: LintResult) -> None:
        """Check for em-dash overuse."""
        em_dashes = re.findall(EM_DASH_PATTERN, content)
        word_count = len(content.split())
        max_allowed = max(1, word_count // 500 * self.max_em_dash_per_500)

        if len(em_dashes) > max_allowed:
            # Find positions
            for match in re.finditer(EM_DASH_PATTERN, content):
                start = max(0, match.start() - 40)
                end = min(len(content), match.end() + 40)
                context = content[start:end]

                result.add_issue(LintIssue(
                    rule_id="EM_DASH_OVERUSE",
                    message=f"Em-dash overuse: {len(em_dashes)} found (max {max_allowed} per 500 words)",
                    severity=LintSeverity.WARNING,
                    line=content[:match.start()].count('\n') + 1,
                    suggestion="Replace em-dashes with commas, periods, or parentheses",
                    auto_fixable=False,
                    context=context,
                ))
                break  # Just report once

    def _check_hedging(self, content: str, result: LintResult) -> None:
        """Check for hedging language overuse."""
        content_lower = content.lower()
        word_count = len(content.split())
        hedge_count = 0

        for hedge in self.hedging_phrases:
            pattern = r'\b' + re.escape(hedge.lower()) + r'\b'
            matches = list(re.finditer(pattern, content_lower))
            hedge_count += len(matches)

            for match in matches[:5]:  # Report first 5 per phrase
                start = max(0, match.start() - 40)
                end = min(len(content), match.end() + 40)
                context = content[start:end]

                result.add_issue(LintIssue(
                    rule_id="HEDGING",
                    message=f"Hedging language: '{hedge}' weakens authority",
                    severity=LintSeverity.WARNING,
                    line=content[:match.start()].count('\n') + 1,
                    suggestion=f"Remove '{hedge}' or replace with confident assertion",
                    auto_fixable=True,
                    context=context,
                ))

        # Calculate hedging density
        hedging_density = (hedge_count / word_count * 100) if word_count > 0 else 0
        if hedging_density > self.max_hedging_density:
            result.add_issue(LintIssue(
                rule_id="HEDGING_DENSITY",
                message=f"High hedging density: {hedging_density:.1f}% (max {self.max_hedging_density}%)",
                severity=LintSeverity.WARNING,
                line=1,
                suggestion="Reduce hedging phrases; state claims confidently with evidence",
                auto_fixable=False,
                context="",
            ))

    def _check_sentence_variety(self, content: str, result: LintResult) -> None:
        """Check for sentence length variety."""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return

        short_count = 0  # < 10 words
        long_count = 0   # > 25 words
        total = len(sentences)

        for sentence in sentences:
            word_count = len(sentence.split())
            if word_count < 10:
                short_count += 1
            elif word_count > 25:
                long_count += 1

        short_pct = (short_count / total * 100) if total > 0 else 0
        long_pct = (long_count / total * 100) if total > 0 else 0

        if short_pct < self.sentence_variety_short_min:
            result.add_issue(LintIssue(
                rule_id="LOW_SENTENCE_VARIETY_SHORT",
                message=f"Only {short_pct:.0f}% short sentences (min {self.sentence_variety_short_min}%)",
                severity=LintSeverity.WARNING,
                line=1,
                suggestion="Add more punchy, short sentences for rhythm and impact",
                auto_fixable=False,
                context="",
            ))

        if long_pct > self.sentence_variety_long_max:
            result.add_issue(LintIssue(
                rule_id="HIGH_SENTENCE_VARIETY_LONG",
                message=f"{long_pct:.0f}% long sentences (max {self.sentence_variety_long_max}%)",
                severity=LintSeverity.WARNING,
                line=1,
                suggestion="Break long sentences into shorter ones for readability",
                auto_fixable=False,
                context="",
            ))

    def _check_contractions(self, content: str, result: LintResult) -> None:
        """Check for appropriate contraction usage."""
        content_lower = content.lower()
        words = content_lower.split()

        if not words:
            return

        # Count contractions
        contraction_count = sum(1 for word in words if "'" in word and word in CONTRACTION_MAP)
        contraction_pct = (contraction_count / len(words) * 100) if words else 0

        if contraction_pct < self.min_contraction_pct:
            result.add_issue(LintIssue(
                rule_id="LOW_CONTRACTIONS",
                message=f"Low contraction usage: {contraction_pct:.1f}% (min {self.min_contraction_pct}%)",
                severity=LintSeverity.WARNING,
                line=1,
                suggestion="Use contractions (don't, can't, it's) for conversational tone",
                auto_fixable=False,
                context="",
            ))

    def _check_voice_drift(self, content: str, brief: ContentBrief, result: LintResult) -> None:
        """Check for voice drift from brief tone."""
        tone = brief.tone.lower() if brief.tone else ""

        # Define tone markers
        formal_markers = ["furthermore", "moreover", "additionally", "consequently",
                          "nevertheless", "accordingly", "subsequently"]
        casual_markers = ["gonna", "wanna", "kinda", "sorta", "yeah", "okay",
                          "cool", "awesome", "great", "nice", "sweet"]

        content_lower = content.lower()
        formal_count = sum(1 for m in formal_markers if m in content_lower)
        casual_count = sum(1 for m in casual_markers if m in content_lower)

        # Check against tone
        if "formal" in tone or "authoritative" in tone:
            if casual_count > 2:
                result.add_issue(LintIssue(
                    rule_id="VOICE_DRIFT_CASUAL",
                    message=f"Casual markers ({casual_count}) conflict with formal/authoritative tone",
                    severity=LintSeverity.WARNING,
                    line=1,
                    suggestion="Remove casual language; use formal transitions",
                    auto_fixable=False,
                    context="",
                ))
            result.voice_drift_score = max(0, 100 - casual_count * 10)

        elif "conversational" in tone or "warm" in tone or "friendly" in tone:
            if formal_count > 3:
                result.add_issue(LintIssue(
                    rule_id="VOICE_DRIFT_FORMAL",
                    message=f"Formal markers ({formal_count}) conflict with conversational tone",
                    severity=LintSeverity.WARNING,
                    line=1,
                    suggestion="Replace formal transitions with conversational ones",
                    auto_fixable=False,
                    context="",
                ))
            result.voice_drift_score = max(0, 100 - formal_count * 10)

        else:
            result.voice_drift_score = 100

        result.voice_drift_detected = result.voice_drift_score < 70

    def _calculate_metrics(self, content: str, result: LintResult) -> None:
        """Calculate overall metrics."""
        words = content.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]

        result.metrics = {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_words_per_sentence": round(len(words) / len(sentences), 1) if sentences else 0,
            "formal_density_pct": 0,  # Would need more sophisticated analysis
            "robotic_tell_count": len([i for i in result.issues if i.rule_id == "ROBOTIC_TELL"]),
            "em_dash_count": len(re.findall(EM_DASH_PATTERN, content)),
            "banned_opener_count": len([i for i in result.issues if i.rule_id == "BANNED_OPENER"]),
            "hedging_density": 0,  # Calculated in _check_hedging
        }