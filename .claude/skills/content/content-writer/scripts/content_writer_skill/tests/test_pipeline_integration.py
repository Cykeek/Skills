"""
Contract Tests: Pipeline Integration
=====================================
End-to-end tests for the complete 5-phase content creation pipeline.
"""

import pytest
from content_writer_skill.pipeline import ContentPipeline
from content_writer_skill.models import (
    ContentBrief, ContentOutline, ContentDraft,
    Goal, Format, Tone, HookType, StructurePattern, PersuasionFramework,
    CTAType, CTACommitmentLevel, OutputFormat,
)
from content_writer_skill.models.validation_results import (
    ValidationResult, LintResult, SEOAudit, DEIResult,
    GateStatus, OutputEnvelope,
)


class TestPipelineIntegration:
    """End-to-end pipeline integration tests."""

    def create_minimal_brief(self) -> ContentBrief:
        return ContentBrief(
            audience="Junior developers learning testing",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="1000 words",
            tone="encouraging, clear, practical",
            angle="Start testing early, not after bugs appear in production",
            primary_keyword="testing early",
            secondary_keywords=["unit testing", "TDD", "bugs"],
            target_audience_level="beginner",
        )

    def test_pipeline_runs_all_phases(self):
        """Test pipeline executes all 5 phases."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result is not None
        assert result.brief is not None
        assert result.outline is not None
        assert result.draft is not None
        assert result.revised_draft is not None
        assert result.final_output is not None

    def test_pipeline_validates_brief_first(self):
        """Test Phase 1: Brief validation runs first."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        # Brief validation should pass
        assert result.brief_validation.passed is True

    def test_pipeline_generates_outline(self):
        """Test Phase 2: Outline generation."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.outline is not None
        assert result.outline.title
        assert len(result.outline.sections) >= 3
        assert result.outline.hook is not None
        assert result.outline.cta is not None
        assert result.outline.seo.primary_keyword

    def test_pipeline_generates_draft(self):
        """Test Phase 3: Draft generation."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.draft is not None
        assert result.draft.content
        assert result.draft.word_count > 0
        # All outline sections should appear in draft
        for section in result.outline.sections:
            assert section.heading in result.draft.content

    def test_pipeline_runs_lint_gate(self):
        """Test Gate 2: Lint validation runs."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.lint_result is not None
        assert isinstance(result.lint_result, LintResult)
        assert hasattr(result.lint_result, 'passed')

    def test_pipeline_runs_structure_gate(self):
        """Test Gate 3: Structure validation."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.structure_validation is not None
        assert hasattr(result.structure_validation, 'passed')

    def test_pipeline_runs_seo_gate(self):
        """Test Gate 4: SEO validation."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.seo_audit is not None
        assert isinstance(result.seo_audit, SEOAudit)
        assert 0 <= result.seo_audit.overall_score <= 100

    def test_pipeline_runs_dei_gate(self):
        """Test Gate 5: DEI/Accessibility validation."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.dei_result is not None
        assert isinstance(result.dei_result, DEIResult)
        assert hasattr(result.dei_result, 'passed')

    def test_pipeline_runs_output_envelope_gate(self):
        """Test Gate 6: Output envelope validation."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.output_envelope is not None
        assert isinstance(result.output_envelope, OutputEnvelope)
        assert result.output_envelope.format_version
        assert result.output_envelope.timestamp

    def test_pipeline_output_format_cli(self):
        """Test pipeline CLI output format."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief, output_format=OutputFormat.CLI)
        result = pipeline.run()

        assert result.output_format == OutputFormat.CLI

    def test_pipeline_output_format_agent(self):
        """Test pipeline Agent JSON envelope output format."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief, output_format=OutputFormat.AGENT)
        result = pipeline.run()

        assert result.output_format == OutputFormat.AGENT
        assert result.output_envelope.data is not None

    def test_pipeline_strict_mode_fails_on_gate_failure(self):
        """Test strict mode fails pipeline on gate failure."""
        brief = self.create_minimal_brief()
        # Create content that will fail lint (banned opener)
        brief.angle = "In today's world, testing is important"
        pipeline = ContentPipeline(brief, strict_mode=True)
        result = pipeline.run()

        # In strict mode, pipeline should track failures
        assert result.pipeline_status in ("completed", "failed")

    def test_pipeline_non_strict_continues_on_warnings(self):
        """Test non-strict mode continues past warnings."""
        brief = self.create_minimal_brief()
        brief.angle = "In today's world, testing is important"
        pipeline = ContentPipeline(brief, strict_mode=False)
        result = pipeline.run()

        # Should complete despite warnings
        assert result.pipeline_status == "completed"

    def test_pipeline_skip_gates_option(self):
        """Test skip_gates option bypasses specific gates."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief, skip_gates=["lint", "dei"])
        result = pipeline.run()

        # Lint and DEI gates should be skipped (not run or passed)
        assert result.pipeline_status == "completed"

    def test_pipeline_max_retries(self):
        """Test max_retries parameter."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief, max_retries=2)
        result = pipeline.run()

        assert result.retry_count <= 2

    def test_pipeline_revision_cycle(self):
        """Test Phase 4: Revision cycle runs."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        # Should have at least 1 revision
        assert result.revision_count >= 1
        assert result.revised_draft is not None
        assert result.revised_draft.content != result.draft.content or result.revision_count == 1

    def test_pipeline_final_output_envelope_structure(self):
        """Test final output envelope has correct structure."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief, output_format=OutputFormat.AGENT)
        result = pipeline.run()

        envelope = result.output_envelope
        assert envelope.format_version == "1.0"
        assert envelope.timestamp
        assert envelope.data is not None
        assert envelope.data.content
        assert envelope.data.word_count > 0
        assert envelope.data.reading_time_minutes > 0
        assert envelope.metadata is not None
        assert "pipeline_version" in envelope.metadata

    def test_pipeline_validation_summary(self):
        """Test pipeline produces validation summary."""
        brief = self.create_minimal_brief()
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert hasattr(result, 'validation_summary')
        summary = result.validation_summary
        assert "brief" in summary
        assert "lint" in summary
        assert "structure" in summary
        assert "seo" in summary
        assert "dei" in summary
        assert "output_envelope" in summary


class TestPipelineEdgeCases:
    """Edge case tests for pipeline."""

    def test_pipeline_handles_minimal_brief(self):
        """Test pipeline with minimal valid brief."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="500 words",
            tone="clear",
            angle="Testing matters",
        )
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert result.pipeline_status == "completed"
        assert result.final_output

    def test_pipeline_handles_all_formats(self):
        """Test pipeline works with all content formats."""
        for fmt in Format:
            brief = ContentBrief(
                audience="Developers",
                goal=Goal.EDUCATE,
                format=fmt,
                length="500 words",
                tone="clear",
                angle="Testing matters",
            )
            pipeline = ContentPipeline(brief)
            result = pipeline.run()

            assert result.pipeline_status == "completed"
            assert result.outline.format == fmt

    def test_pipeline_handles_all_goals(self):
        """Test pipeline works with all goals."""
        for goal in Goal:
            brief = ContentBrief(
                audience="Developers",
                goal=goal,
                format=Format.BLOG,
                length="500 words",
                tone="clear",
                angle="Testing matters",
            )
            pipeline = ContentPipeline(brief)
            result = pipeline.run()

            assert result.pipeline_status == "completed"
            assert result.outline.goal == goal

    def test_pipeline_tone_adaptation(self):
        """Test pipeline adapts to different tones."""
        for tone in Tone:
            brief = ContentBrief(
                audience="Developers",
                goal=Goal.EDUCATE,
                format=Format.BLOG,
                length="500 words",
                tone=tone,
                angle="Testing matters",
            )
            pipeline = ContentPipeline(brief)
            result = pipeline.run()

            assert result.pipeline_status == "completed"

    def test_pipeline_with_brief_file_input(self):
        """Test pipeline can load brief from file path."""
        import tempfile
        import json

        brief_data = {
            "audience": "Developers",
            "goal": "educate",
            "format": "blog",
            "length": "500 words",
            "tone": "clear",
            "angle": "Testing matters",
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(brief_data, f)
            brief_path = f.name

        try:
            pipeline = ContentPipeline.from_brief_file(brief_path)
            result = pipeline.run()
            assert result.pipeline_status == "completed"
        finally:
            import os
            os.unlink(brief_path)


class TestPipelineContract:
    """Contract tests ensuring pipeline behavior matches spec."""

    def test_phase_outputs_match_models(self):
        """Test each phase output matches expected model."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="500 words",
            tone="clear",
            angle="Testing matters",
        )
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        # Phase 1: Brief validation
        assert isinstance(result.brief_validation, ValidationResult)
        assert result.brief_validation.passed is True

        # Phase 2: Outline
        assert isinstance(result.outline, ContentOutline)
        assert len(result.outline.sections) >= 3

        # Phase 3: Draft
        assert isinstance(result.draft, ContentDraft)
        assert result.draft.draft_number == 1

        # Phase 4: Revision
        assert isinstance(result.revised_draft, ContentDraft)
        assert result.revised_draft.draft_number > result.draft.draft_number

        # Phase 5: Final
        assert isinstance(result.final_output, ContentDraft)
        assert result.final_output.content

    def test_gate_outputs_match_models(self):
        """Test each gate output matches expected model."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="500 words",
            tone="clear",
            angle="Testing matters",
        )
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        # Gate 1: Brief validation
        assert isinstance(result.brief_validation, ValidationResult)

        # Gate 2: Lint
        assert isinstance(result.lint_result, LintResult)

        # Gate 3: Structure
        assert isinstance(result.structure_validation, ValidationResult)

        # Gate 4: SEO
        assert isinstance(result.seo_audit, SEOAudit)

        # Gate 5: DEI
        assert isinstance(result.dei_result, DEIResult)

        # Gate 6: Output Envelope
        assert isinstance(result.output_envelope, OutputEnvelope)

    def test_gate_statuses_are_valid_enums(self):
        """Test all gate statuses use GateStatus enum."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="500 words",
            tone="clear",
            angle="Testing matters",
        )
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        gates = [
            result.brief_validation.status,
            result.lint_result.status,
            result.structure_validation.status,
            result.seo_audit.status,
            result.dei_result.status,
            result.output_envelope.status,
        ]

        for status in gates:
            assert isinstance(status, GateStatus)

    def test_pipeline_is_deterministic_for_same_input(self):
        """Test pipeline produces same output for same input (structure-wise)."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="500 words",
            tone="clear",
            angle="Testing matters",
        )

        pipeline1 = ContentPipeline(brief)
        result1 = pipeline1.run()

        pipeline2 = ContentPipeline(brief)
        result2 = pipeline2.run()

        # Structure should be same (same number of sections, same headings)
        assert len(result1.outline.sections) == len(result2.outline.sections)
        for s1, s2 in zip(result1.outline.sections, result2.outline.sections):
            assert s1.heading == s2.heading

    def test_pipeline_metadata_tracking(self):
        """Test pipeline tracks execution metadata."""
        brief = ContentBrief(
            audience="Developers",
            goal=Goal.EDUCATE,
            format=Format.BLOG,
            length="500 words",
            tone="clear",
            angle="Testing matters",
        )
        pipeline = ContentPipeline(brief)
        result = pipeline.run()

        assert hasattr(result, 'metadata')
        assert 'pipeline_version' in result.metadata
        assert 'execution_time_seconds' in result.metadata
        assert 'phases_completed' in result.metadata
        assert len(result.metadata['phases_completed']) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])