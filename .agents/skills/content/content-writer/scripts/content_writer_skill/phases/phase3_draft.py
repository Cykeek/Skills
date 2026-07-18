"""
Phase 3: Draft
==============
Content generation from outline - section by section writing.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import json

from content_writer_skill.models import ContentBrief, ContentOutline, ContentDraft, ValidationGateResult
from content_writer_skill.phases.phase2_outline import OutlinePhase


@dataclass
class Phase3Result:
    """Result of Phase 3: Draft."""
    draft: ContentDraft
    validation: ValidationGateResult


class DraftPhase:
    """
    Phase 3: Draft

    Inputs: ContentOutline from Phase 2, ContentBrief from Phase 1
    Outputs: ContentDraft with full written content
    """

    # Section writing templates by structure pattern
    SECTION_TEMPLATES = {
        "problem": "## {heading}\n\n{opening}\n\n{points}\n\n{transition}",
        "agitation": "## {heading}\n\n{opening}\n\n{evidence}\n\n{impact}\n\n{transition}",
        "solution": "## {heading}\n\n{opening}\n\n{methodology}\n\n{steps}\n\n{transition}",
        "implementation": "## {heading}\n\n{opening}\n\n{steps}\n\n{tips}\n\n{transition}",
        "pitfalls": "## {heading}\n\n{opening}\n\n{pitfalls}\n\n{transition}",
        "conclusion": "## {heading}\n\n{summary}\n\n{cta_setup}\n\n{transition}",
    }

    def __init__(self, llm_client=None):
        """
        Initialize Draft Phase.

        Args:
            llm_client: Optional LLM client for generation (if None, uses template-based)
        """
        self.llm_client = llm_client

    def run(self, outline: ContentOutline, brief: ContentBrief) -> Phase3Result:
        """
        Execute Phase 3: Draft content from outline.

        Args:
            outline: ContentOutline from Phase 2
            brief: ContentBrief from Phase 1

        Returns:
            Phase3Result with drafted content
        """
        # Build content section by section
        content_parts = []

        # Add H1 title from outline
        if outline.title:
            content_parts.append(f"# {outline.title}")

        # Add hook
        hook_text = self._write_hook(outline.hook, brief)
        content_parts.append(hook_text)

        # Write each section
        for i, section in enumerate(outline.sections):
            section_text = self._write_section(section, brief, outline, i)
            content_parts.append(section_text)

        # Add CTA
        cta_text = self._write_cta(outline.cta, brief)
        content_parts.append(cta_text)

        # Combine
        full_content = "\n\n".join(content_parts)

        # Create draft object
        draft = ContentDraft(
            content=full_content,
            outline=outline,
            brief=brief,
            draft_number=1,
            template_used=outline.template_used,
        )

        # Validate draft structure
        validation = self._validate_draft(draft, outline, brief)

        return Phase3Result(draft=draft, validation=validation)

    def _write_hook(self, hook, brief: ContentBrief) -> str:
        """Write the opening hook."""
        hook_templates = {
            "question": "{text}\n\n{promise}",
            "bold-claim": "**{text}**\n\n{promise}",
            "story": "{text}\n\n{promise}",
            "statistic": "**{text}**\n\n{promise}",
            "contrarian": "{text}\n\n{promise}",
            "pain-point": "{text}\n\n{promise}",
            "curiosity-gap": "{text}\n\n{promise}",
            "direct-benefit": "{text}\n\n{promise}",
        }

        template = hook_templates.get(hook.type.value if hasattr(hook.type, 'value') else str(hook.type), "{text}")
        return template.format(text=hook.text, promise=hook.promise)

    def _write_section(self, section: 'OutlineSection', brief: ContentBrief,
                       outline: ContentOutline, index: int) -> str:
        """Write a single section."""
        # Build bullet points into prose
        points_text = self._bullets_to_prose(section.key_points, brief.tone)

        # Determine section type from heading
        heading_lower = section.heading.lower()
        section_type = "general"

        if any(kw in heading_lower for kw in ["problem", "challenge", "struggle", "issue"]):
            section_type = "problem"
        elif any(kw in heading_lower for kw in ["why", "matters", "impact", "cost", "risk"]):
            section_type = "agitation"
        elif any(kw in heading_lower for kw in ["solution", "approach", "method", "framework", "answer"]):
            section_type = "solution"
        elif any(kw in heading_lower for kw in ["how", "implement", "step", "execute", "apply"]):
            section_type = "implementation"
        elif any(kw in heading_lower for kw in ["pitfall", "mistake", "avoid", "wrong", "trap"]):
            section_type = "pitfalls"
        elif any(kw in heading_lower for kw in ["conclusion", "summary", "final", "wrap", "next"]):
            section_type = "conclusion"

        # Generate section content based on type
        if section_type == "problem":
            return self._write_problem_section(section, points_text, brief)
        elif section_type == "agitation":
            return self._write_agitation_section(section, points_text, brief)
        elif section_type == "solution":
            return self._write_solution_section(section, points_text, brief)
        elif section_type == "implementation":
            return self._write_implementation_section(section, points_text, brief)
        elif section_type == "pitfalls":
            return self._write_pitfalls_section(section, points_text, brief)
        elif section_type == "conclusion":
            return self._write_conclusion_section(section, points_text, brief, outline.cta)
        else:
            return self._write_general_section(section, points_text, brief)

    def _bullets_to_prose(self, bullets: List[str], tone: str) -> str:
        """Convert bullet points to flowing prose."""
        if not bullets:
            return ""

        # Simple conversion - in practice this would use LLM
        prose_parts = []
        for bullet in bullets:
            # Add transition words based on tone
            if tone and "conversational" in tone.lower():
                prose_parts.append(f"Here's the thing: {bullet}")
            elif tone and "authoritative" in tone.lower():
                prose_parts.append(f"Consider this: {bullet}")
            else:
                prose_parts.append(bullet)

        return "\n\n".join(prose_parts)

    def _write_problem_section(self, section, points_text: str, brief: ContentBrief) -> str:
        """Write a problem-focused section."""
        return f"## {section.heading}\n\n{points_text}\n\n{section.transition}"

    def _write_agitation_section(self, section, points_text: str, brief: ContentBrief) -> str:
        """Write an agitation/impact section."""
        return f"## {section.heading}\n\n{points_text}\n\n{section.transition}"

    def _write_solution_section(self, section, points_text: str, brief: ContentBrief) -> str:
        """Write a solution section."""
        return f"## {section.heading}\n\n{points_text}\n\n{section.transition}"

    def _write_implementation_section(self, section, points_text: str, brief: ContentBrief) -> str:
        """Write an implementation/how-to section."""
        return f"## {section.heading}\n\n{points_text}\n\n{section.transition}"

    def _write_pitfalls_section(self, section, points_text: str, brief: ContentBrief) -> str:
        """Write a pitfalls/warnings section."""
        return f"## {section.heading}\n\n{points_text}\n\n{section.transition}"

    def _write_conclusion_section(self, section, points_text: str, brief: ContentBrief, cta) -> str:
        """Write conclusion with CTA setup."""
        cta_setup = f"\n\n{cta.text}" if cta.text else ""
        return f"## {section.heading}\n\n{points_text}{cta_setup}\n\n{section.transition}"

    def _write_general_section(self, section, points_text: str, brief: ContentBrief) -> str:
        """Write a general section."""
        return f"## {section.heading}\n\n{points_text}\n\n{section.transition}"

    def _write_cta(self, cta, brief: ContentBrief) -> str:
        """Write the call to action."""
        if not cta.text:
            return ""

        cta_templates = {
            "read-next": "**Next up:** {text}",
            "subscribe": "**Stay updated:** {text}",
            "download": "**Get the guide:** {text}",
            "sign-up": "**Ready to start?** {text}",
            "contact": "**Let's talk:** {text}",
            "buy": "**Get started:** {text}",
            "share": "**Found this useful?** {text}",
            "comment": "**Your thoughts?** {text}",
            "reflect": "**Take a moment:** {text}",
        }

        template = cta_templates.get(cta.type.value if hasattr(cta.type, 'value') else str(cta.type), "{text}")
        return template.format(text=cta.text)

    def _validate_draft(self, draft: ContentDraft, outline: ContentOutline,
                        brief: ContentBrief) -> ValidationGateResult:
        """Validate draft against outline and brief."""
        issues = []
        metrics = {}

        # Word count check
        target_words = self._parse_target_words(brief.length)
        if target_words > 0:
            diff_pct = abs(draft.word_count - target_words) / target_words * 100
            metrics["word_count"] = draft.word_count
            metrics["target_word_count"] = target_words
            metrics["word_count_diff_pct"] = round(diff_pct, 1)

            if diff_pct > 40:
                issues.append({
                    "code": "WORD_COUNT_MISMATCH",
                    "message": f"Draft word count ({draft.word_count}) differs from target ({target_words}) by {diff_pct:.0f}%",
                    "severity": "warning",
                    "suggestion": "Expand or condense sections to match target length",
                })

        # Section coverage check
        outline_headings = [s.heading for s in outline.sections]
        content_headings = self._extract_headings(draft.content)
        missing_sections = [h for h in outline_headings if h not in content_headings]
        if missing_sections:
            issues.append({
                "code": "MISSING_SECTIONS",
                "message": f"Draft missing {len(missing_sections)} planned sections: {', '.join(missing_sections[:3])}",
                "severity": "error",
                "suggestion": "Ensure all outline sections are written",
            })

        # Hook presence
        if outline.hook.text and outline.hook.text not in draft.content[:500]:
            issues.append({
                "code": "MISSING_HOOK",
                "message": "Hook from outline not found in draft opening",
                "severity": "warning",
            })

        # CTA presence
        if outline.cta.text and outline.cta.text not in draft.content[-500:]:
            issues.append({
                "code": "MISSING_CTA",
                "message": "CTA from outline not found in draft conclusion",
                "severity": "warning",
            })

        metrics["section_coverage"] = f"{len(outline_headings) - len(missing_sections)}/{len(outline_headings)}"

        passed = len([i for i in issues if i["severity"] == "error"]) == 0

        return ValidationGateResult(
            gate=3,
            gate_name="structure-validation",
            passed=passed,
            issues=issues,
            metrics=metrics,
        )

    def _parse_target_words(self, length: str) -> int:
        """Parse target word count from length string."""
        import re
        if not length:
            return 1200
        match = re.search(r'(\d+[,-]?\d*)', length.replace(',', ''))
        if match:
            return int(match.group(1))
        return 1200

    def _extract_headings(self, content: str) -> List[str]:
        """Extract markdown headings from content."""
        import re
        return [h.strip('# ').strip() for h in re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)]


def run_draft(outline: ContentOutline, brief: ContentBrief) -> Phase3Result:
    """Convenience function to run Phase 3."""
    phase = DraftPhase()
    return phase.run(outline, brief)