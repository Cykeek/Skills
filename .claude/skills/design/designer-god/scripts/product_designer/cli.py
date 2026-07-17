#!/usr/bin/env python3
"""
Product Designer Skill CLI
==========================
Command-line interface for Product Designer skill operations.
"""

import argparse
import json
import sys
from typing import Any, Dict, List
from pathlib import Path

# Add parent directory to path for workspace_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from product_designer.output_manager import OutputManager, OutputFormat
from product_designer.validators import validate_request, validate_response
from product_designer.diagnostics import ProductDesignerDiagnostics


class CLI:
    """Product Designer Skill CLI."""

    def __init__(self):
        self.diagnostics = ProductDesignerDiagnostics()
        self.output_manager = OutputManager(OutputFormat.JSON, skill_name="designer-god")
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog="product-designer",
            description="Product Designer Skill - Design review, problem framing, research planning, and design briefs",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  product-designer design-review --design "Onboarding flow" --context "Mobile app" --goals "Activate users,Reduce churn"
  product-designer problem-framing --user "New freelancer" --context "Setting up first project" --progress "Get first client"
  product-designer research-plan --decision "Which onboarding pattern" --goal "Validate user comprehension"
  product-designer design-brief --problem "High drop-off at payment step" --user "Mobile shopper" --scope "2-week sprint"
  product-designer critique-template
  product-designer checklist --type handoff
            """
        )
        parser.add_argument(
            "--output", "-o",
            choices=["json", "text", "table"],
            default="json",
            help="Output format (default: json)"
        )
        parser.add_argument(
            "--task-type",
            default="run",
            help="Task type for output subfolder (review, framing, research, brief, critique, checklist)"
        )
        parser.add_argument(
            "--validate",
            action="store_true",
            help="Validate request/response against JSON schemas"
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # design-review command
        review_parser = subparsers.add_parser("design-review", help="Conduct a design review")
        review_parser.add_argument("--design", required=True, help="Design name/description")
        review_parser.add_argument("--context", required=True, help="Context of the design")
        review_parser.add_argument("--goals", required=True, help="Comma-separated design goals")

        # problem-framing command
        frame_parser = subparsers.add_parser("problem-framing", help="Frame a design problem")
        frame_parser.add_argument("--user", required=True, help="Target user description")
        frame_parser.add_argument("--context", required=True, help="User context/situation")
        frame_parser.add_argument("--progress", required=True, help="Desired progress/job to be done")
        frame_parser.add_argument("--evidence", help="Comma-separated evidence points")
        frame_parser.add_argument("--assumptions", help="Comma-separated riskiest assumptions")

        # research-plan command
        research_parser = subparsers.add_parser("research-plan", help="Create a research plan")
        research_parser.add_argument("--decision", required=True, help="Decision this research supports")
        research_parser.add_argument("--goal", required=True, help="Research goal")
        research_parser.add_argument("--constraints", help="Comma-separated constraints")

        # design-brief command
        brief_parser = subparsers.add_parser("design-brief", help="Create a design brief")
        brief_parser.add_argument("--problem", required=True, help="Problem statement")
        brief_parser.add_argument("--user", required=True, help="Target user")
        brief_parser.add_argument("--constraints", help="Comma-separated constraints")
        brief_parser.add_argument("--scope", required=True, help="Scope/appetite (e.g., 2-week sprint)")

        # critique-template command
        subparsers.add_parser("critique-template", help="Get critique template")

        # checklist command
        checklist_parser = subparsers.add_parser("checklist", help="Get design review checklist")
        checklist_parser.add_argument("--type", choices=["handoff", "accessibility", "trust"], default="handoff",
                                     help="Checklist type (default: handoff)")

        return parser

    def run(self, args: List[str]) -> int:
        """Run CLI with given arguments."""
        parsed = self.parser.parse_args(args)

        if not parsed.command:
            self.parser.print_help()
            return 1

        # Set output format and task type
        self.output_manager.set_format(parsed.output)
        self.output_manager.task_type = parsed.task_type

        # Route to command handler
        if parsed.command == "design-review":
            return self.cmd_design_review(parsed)
        elif parsed.command == "problem-framing":
            return self.cmd_problem_framing(parsed)
        elif parsed.command == "research-plan":
            return self.cmd_research_plan(parsed)
        elif parsed.command == "design-brief":
            return self.cmd_design_brief(parsed)
        elif parsed.command == "critique-template":
            return self.cmd_critique_template(parsed)
        elif parsed.command == "checklist":
            return self.cmd_checklist(parsed)

        return 1

    def cmd_design_review(self, args) -> int:
        """Conduct design review."""
        goals = [g.strip() for g in args.goals.split(",")]
        result = self.diagnostics.design_review(args.design, args.context, goals)

        if args.validate:
            valid, errors = validate_response("design-review-response", result)
            if not valid:
                self.output_manager.output({"validation_errors": errors}, write_file=True)
                return 1

        self.output_manager.output(result, write_file=True)
        return 0

    def cmd_problem_framing(self, args) -> int:
        """Frame a design problem."""
        evidence = [e.strip() for e in args.evidence.split(",")] if args.evidence else []
        assumptions = [a.strip() for a in args.assumptions.split(",")] if args.assumptions else []

        result = self.diagnostics.problem_framing(
            args.user, args.context, args.progress, evidence, assumptions
        )

        if args.validate:
            valid, errors = validate_response("problem-framing-response", result)
            if not valid:
                self.output_manager.output({"validation_errors": errors}, write_file=True)
                return 1

        self.output_manager.output(result, write_file=True)
        return 0

    def cmd_research_plan(self, args) -> int:
        """Create a research plan."""
        constraints = [c.strip() for c in args.constraints.split(",")] if args.constraints else []

        result = self.diagnostics.research_plan(args.decision, args.goal, constraints)

        if args.validate:
            valid, errors = validate_response("research-plan-response", result)
            if not valid:
                self.output_manager.output({"validation_errors": errors}, write_file=True)
                return 1

        self.output_manager.output(result, write_file=True)
        return 0

    def cmd_design_brief(self, args) -> int:
        """Create a design brief."""
        constraints = [c.strip() for c in args.constraints.split(",")] if args.constraints else []

        result = self.diagnostics.design_brief(args.problem, args.user, constraints, args.scope)

        if args.validate:
            valid, errors = validate_response("design-brief-response", result)
            if not valid:
                self.output_manager.output({"validation_errors": errors}, write_file=True)
                return 1

        self.output_manager.output(result, write_file=True)
        return 0

    def cmd_critique_template(self, args) -> int:
        """Get critique template."""
        result = self.diagnostics.get_critique_template()

        if args.validate:
            valid, errors = validate_response("critique-template", result)
            if not valid:
                self.output_manager.output({"validation_errors": errors}, write_file=True)
                return 1

        self.output_manager.output(result, write_file=True)
        return 0

    def cmd_checklist(self, args) -> int:
        """Get design review checklist."""
        result = self.diagnostics.get_design_checklist(args.type)
        self.output_manager.output(result, write_file=True)
        return 0


def main():
    """Main CLI entry point."""
    cli = CLI()
    return cli.run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())