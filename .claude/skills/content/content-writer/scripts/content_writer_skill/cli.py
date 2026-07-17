#!/usr/bin/env python3
"""
Content Writer CLI
==================
Command-line interface for the 5-phase content creation pipeline.

Usage:
    python -m content_writer_skill.cli --brief-file brief.json [options]
    python -m content_writer_skill.cli --brief-json '{"audience": "...", ...}' [options]
    echo '{"audience": "..."}' | python -m content_writer_skill.cli --stdin [options]
"""

import argparse
import sys
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

from content_writer_skill.pipeline import ContentPipeline
from content_writer_skill.models import OutputFormat, ContentBrief
from content_writer_skill.output_manager import create_cli_output, create_agent_output, OutputManager, OutputConfig


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="content-writer",
        description="5-phase AI content creation pipeline (Discover -> Outline -> Draft -> Revise -> Output)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input methods (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--brief-file", "-f",
        type=str,
        help="Path to JSON brief file"
    )
    input_group.add_argument(
        "--brief-json", "-j",
        type=str,
        help="Brief as JSON string"
    )
    input_group.add_argument(
        "--stdin", "-i",
        action="store_true",
        help="Read brief from stdin (JSON)"
    )
    input_group.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactive brief builder"
    )

    # Output options
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format: text (CLI) or json (agent envelope)"
    )
    parser.add_argument(
        "--color",
        action="store_true",
        help="Enable colored CLI output"
    )
    parser.add_argument(
        "--preview-only",
        action="store_true",
        help="Only show brief validation and outline, don't generate content"
    )
    parser.add_argument(
        "--max-preview",
        type=int,
        default=0,
        help="Max characters to show in content preview (0 = full)"
    )

    # Pipeline options
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: fail on missing brief fields instead of inferring"
    )
    parser.add_argument(
        "--strict-seo",
        action="store_true",
        help="Fail pipeline on SEO warnings"
    )
    parser.add_argument(
        "--strict-dei",
        action="store_true",
        help="Fail pipeline on DEI warnings"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="Max retries for failed validation gates (default: 2)"
    )
    parser.add_argument(
        "--no-lint",
        action="store_true",
        help="Skip lint validation (Gate 2)"
    )
    parser.add_argument(
        "--no-seo",
        action="store_true",
        help="Skip SEO validation (Gate 4)"
    )
    parser.add_argument(
        "--no-dei",
        action="store_true",
        help="Skip DEI/accessibility validation (Gate 5)"
    )

    # Debug options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output with phase timing"
    )
    parser.add_argument(
        "--save-intermediate",
        type=str,
        help="Save intermediate artifacts (brief, outline, draft) to directory"
    )
    parser.add_argument(
        "--lint-config",
        type=str,
        help="Path to custom lint rules JSON file"
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="content-writer 2.1.0"
    )

    return parser


def load_brief_from_file(filepath: str) -> Dict[str, Any]:
    """Load brief from JSON file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Brief file not found: {filepath}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_brief_from_stdin() -> Dict[str, Any]:
    """Load brief from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from stdin: {e}")


def run_interactive_brief() -> Dict[str, Any]:
    """Run interactive brief builder."""
    print("=" * 60)
    print("INTERACTIVE CONTENT BRIEF BUILDER")
    print("=" * 60)
    print("Press Ctrl+C to cancel at any time.\n")

    brief = {}

    # Required fields
    brief["audience"] = input("Target audience (role, knowledge level, pain points): ").strip()
    if not brief["audience"]:
        raise ValueError("Audience is required")

    print("\nGoals: educate, persuade, inform, entertain, convert, nurture, reassure, warn")
    brief["goal"] = input("Primary goal: ").strip().lower()
    if brief["goal"] not in ["educate", "persuade", "inform", "entertain", "convert", "nurture", "reassure", "warn"]:
        raise ValueError(f"Invalid goal: {brief['goal']}")

    print("\nFormats: blog, landing-page, email, social, case-study, whitepaper, press-release, video-script")
    brief["format"] = input("Content format: ").strip().lower()
    if brief["format"] not in ["blog", "landing-page", "email", "social", "case-study", "whitepaper", "press-release", "video-script"]:
        raise ValueError(f"Invalid format: {brief['format']}")

    brief["length"] = input("Target length (e.g., '1200-1800 words', '500 words', '90 seconds'): ").strip()
    if not brief["length"]:
        raise ValueError("Length is required")

    brief["tone"] = input("Tone/voice (e.g., 'confident, practical', 'warm, personal', 'authoritative, direct'): ").strip()
    if not brief["tone"]:
        raise ValueError("Tone is required")

    brief["angle"] = input("Key angle / ONE thing reader must remember: ").strip()
    if not brief["angle"]:
        raise ValueError("Angle is required")

    # Optional fields
    brief["primary_keyword"] = input("Primary SEO keyword (optional): ").strip() or None
    brief["secondary_keywords"] = input("Secondary keywords comma-separated (optional): ").strip() or None
    brief["brand_voice"] = input("Brand voice notes (optional): ").strip() or None
    brief["cta_type"] = input("CTA type (optional): read-next, subscribe, download, sign-up, contact, buy, share, comment, reflect: ").strip() or None

    # Clean up None values
    brief = {k: v for k, v in brief.items() if v is not None}

    print("\n" + "=" * 60)
    print("BRIEF SUMMARY")
    print("=" * 60)
    print(json.dumps(brief, indent=2))

    confirm = input("\nProceed with generation? (y/N): ").strip().lower()
    if confirm != 'y':
        raise KeyboardCancelled("User cancelled")

    return brief


class KeyboardCancelled(Exception):
    """Raised when user cancels interactive mode."""
    pass


def load_lint_config(filepath: str) -> Dict[str, Any]:
    """Load custom lint configuration from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_intermediate(artifacts_dir: str, brief: ContentBrief, outline, draft, pipeline_result) -> None:
    """Save intermediate artifacts to directory."""
    path = Path(artifacts_dir)
    path.mkdir(parents=True, exist_ok=True)

    # Save brief
    with open(path / "brief.json", 'w', encoding='utf-8') as f:
        json.dump(brief.to_dict(), f, indent=2, ensure_ascii=False)

    # Save outline
    if outline:
        with open(path / "outline.json", 'w', encoding='utf-8') as f:
            json.dump(outline.to_dict(), f, indent=2, ensure_ascii=False)

    # Save draft
    if draft:
        with open(path / "draft.json", 'w', encoding='utf-8') as f:
            json.dump(draft.to_dict(), f, indent=2, ensure_ascii=False)

    # Save pipeline result
    if pipeline_result:
        with open(path / "pipeline_result.json", 'w', encoding='utf-8') as f:
            json.dump(pipeline_result.to_dict(), f, indent=2, ensure_ascii=False)

    print(f"\nIntermediate artifacts saved to: {path}")


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Load brief
        if args.interactive:
            brief_data = run_interactive_brief()
        elif args.brief_file:
            brief_data = load_brief_from_file(args.brief_file)
        elif args.brief_json:
            brief_data = json.loads(args.brief_json)
        elif args.stdin:
            brief_data = load_brief_from_stdin()
        else:
            parser.error("No input method specified")

        # Load custom lint config if provided
        lint_config = None
        if args.lint_config:
            lint_config = load_lint_config(args.lint_config)

        # Configure pipeline
        output_format = OutputFormat.JSON if args.output_format == "json" else OutputFormat.TEXT

        pipeline = ContentPipeline(
            strict_mode=args.strict,
            lint_config=lint_config,
            strict_seo=args.strict_seo,
            strict_dei=args.strict_dei,
            output_format=output_format,
            max_retries=args.max_retries,
        )

        # Run pipeline
        if args.verbose:
            print("Starting content pipeline...", file=sys.stderr)

        result = pipeline.run(brief_data)

        if args.verbose:
            print(f"Pipeline completed in {result.total_time_ms}ms", file=sys.stderr)
            for phase, time_ms in result.phase_times.items():
                print(f"  {phase}: {time_ms}ms", file=sys.stderr)

        # Handle preview mode
        if args.preview_only:
            preview_output = f"BRIEF:\n{json.dumps(result.brief.to_dict(), indent=2)}\n\n"
            if result.outline:
                preview_output += f"OUTLINE:\n{json.dumps(result.outline.to_dict(), indent=2)}"
            output = preview_output
        else:
            # Generate output
            brief_id = getattr(result.brief, 'source_file', 'brief-1')
            if args.output_format == "json":
                output = create_agent_output(
                    result.draft,
                    execution_time_ms=result.total_time_ms,
                    brief_id=brief_id,
                )
            else:
                output = create_cli_output(
                    result.draft,
                    execution_time_ms=result.total_time_ms,
                    brief_id=brief_id,
                    color=args.color,
                )

        # Save intermediate artifacts if requested
        if args.save_intermediate and not args.preview_only:
            save_intermediate(args.save_intermediate, result.brief, result.outline, result.draft, result)

        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            if args.verbose:
                print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output)

        # Exit code based on success
        if not result.success and not args.preview_only:
            return 1

        return 0

    except KeyboardCancelled:
        print("\nCancelled.", file=sys.stderr)
        return 130
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 3
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 4
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())