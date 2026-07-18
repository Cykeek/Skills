#!/usr/bin/env python3
"""
Wix Support Skill CLI
=====================
Command-line interface for Wix platform diagnostics and utilities.

Usage:
    python -m wix_support_skill.cli --help
    python -m wix_support_skill.cli diagnose --editor classic --issue "mobile layout broken"
    python -m wix_support_skill.cli velo-check --element-id "#myButton" --code-file velo_code.js
    python -m wix_support_skill.cli cms-debug --collection "Products" --page-slug "/product/123"
    python -m wix_support_skill.cli dns-check --domain "example.com"
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

# Add scripts folder to sys.path for standalone execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import from our diagnostics module
from wix_support_skill.diagnostics import WixDiagnostics, validate_request, validate_response


class CLI:
    """Wix Support Skill CLI."""

    def __init__(self):
        self.diagnostics = WixDiagnostics()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog="wix-support",
            description="Wix Platform Diagnostic Toolkit",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__doc__
        )
        parser.add_argument(
            "--output", "-o",
            choices=["json", "text", "table"],
            default="json",
            help="Output format (default: json)"
        )
        parser.add_argument(
            "--validate",
            action="store_true",
            help="Validate request/response against JSON schemas"
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # diagnose command
        diagnose_parser = subparsers.add_parser("diagnose", help="Diagnose editor/layout issue")
        diagnose_parser.add_argument("--editor", required=True, choices=["classic", "studio", "editorx"],
                                    help="Wix editor type")
        diagnose_parser.add_argument("--issue", required=True, help="Description of the issue")

        # velo-check command
        velo_parser = subparsers.add_parser("velo-check", help="Check Velo code for issues")
        velo_parser.add_argument("--element-id", required=True, help="Element ID (e.g., #myButton)")
        velo_parser.add_argument("--code", help="Velo code to check")
        velo_parser.add_argument("--code-file", help="Path to file containing Velo code")
        velo_parser.add_argument("--error", help="Error message (optional)")

        # cms-debug command
        cms_parser = subparsers.add_parser("cms-debug", help="Diagnose CMS/dynamic page issue")
        cms_parser.add_argument("--collection", required=True, help="CMS collection name")
        cms_parser.add_argument("--page-slug", required=True, help="Page slug/URL path")

        # dns-check command
        dns_parser = subparsers.add_parser("dns-check", help="Check DNS configuration")
        dns_parser.add_argument("--domain", required=True, help="Domain to check")

        # editor-compare command
        subparsers.add_parser("editor-compare", help="Show Wix editor comparison")

        # ai-tools command
        subparsers.add_parser("ai-tools", help="Show Wix AI tools summary")

        # escalation command
        subparsers.add_parser("escalation", help="Show escalation guide for Wix Support")

        return parser

    def run(self, args: List[str]) -> int:
        """Run CLI with given arguments."""
        parsed = self.parser.parse_args(args)

        if not parsed.command:
            self.parser.print_help()
            return 1

        # Set output format
        self.diagnostics.output_manager.set_format(parsed.output)

        # Route to command handler
        if parsed.command == "diagnose":
            return self.cmd_diagnose(parsed)
        elif parsed.command == "velo-check":
            return self.cmd_velo_check(parsed)
        elif parsed.command == "cms-debug":
            return self.cmd_cms_debug(parsed)
        elif parsed.command == "dns-check":
            return self.cmd_dns_check(parsed)
        elif parsed.command == "editor-compare":
            return self.cmd_editor_compare(parsed)
        elif parsed.command == "ai-tools":
            return self.cmd_ai_tools(parsed)
        elif parsed.command == "escalation":
            return self.cmd_escalation(parsed)

        return 1

    def cmd_diagnose(self, args) -> int:
        """Diagnose editor issue."""
        result = self.diagnostics.diagnose_editor_issue(args.editor, args.issue)
        if args.validate:
            valid, errors = validate_response("diagnose-response", result)
            if not valid:
                self.diagnostics.output_manager.output({"validation_errors": errors})
                return 1
        self.diagnostics.output_manager.output(result)
        return 0

    def cmd_velo_check(self, args) -> int:
        """Check Velo code."""
        code = ""
        if args.code_file:
            with open(args.code_file, 'r') as f:
                code = f.read()
        elif args.code:
            code = args.code

        result = self.diagnostics.diagnose_velo_issue(args.element_id, code, args.error or "")
        if args.validate:
            valid, errors = validate_response("velo-check-response", result)
            if not valid:
                self.diagnostics.output_manager.output({"validation_errors": errors})
                return 1
        self.diagnostics.output_manager.output(result)
        return 0

    def cmd_cms_debug(self, args) -> int:
        """Diagnose CMS 404."""
        result = self.diagnostics.diagnose_cms_404(args.collection, args.page_slug)
        if args.validate:
            valid, errors = validate_response("cms-debug-response", result)
            if not valid:
                self.diagnostics.output_manager.output({"validation_errors": errors})
                return 1
        self.diagnostics.output_manager.output(result)
        return 0

    def cmd_dns_check(self, args) -> int:
        """Check DNS configuration."""
        result = self.diagnostics.check_dns(args.domain)
        if args.validate:
            valid, errors = validate_response("dns-check-response", result)
            if not valid:
                self.diagnostics.output_manager.output({"validation_errors": errors})
                return 1
        self.diagnostics.output_manager.output(result)
        return 0

    def cmd_editor_compare(self, args) -> int:
        """Show editor comparison."""
        result = self.diagnostics.get_editor_comparison()
        if args.validate:
            valid, errors = validate_response("editor-comparison", result)
            if not valid:
                self.diagnostics.output_manager.output({"validation_errors": errors})
                return 1
        self.diagnostics.output_manager.output(result)
        return 0

    def cmd_ai_tools(self, args) -> int:
        """Show AI tools."""
        result = self.diagnostics.get_ai_tools_summary()
        self.diagnostics.output_manager.output(result)
        return 0

    def cmd_escalation(self, args) -> int:
        """Show escalation guide."""
        result = self.diagnostics.get_escalation_guide()
        self.diagnostics.output_manager.output(result)
        return 0


def main():
    """Main CLI entry point."""
    cli = CLI()
    return cli.run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())