#!/usr/bin/env python3
"""
Product Designer Skill - Contract Tests
========================================
Contract tests for all CLI commands against JSON schemas.
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple


class ContractTest:
    """Contract tests for Product Designer Skill."""

    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.scripts_dir = self.skill_dir / "scripts"
        self.schemas_dir = self.skill_dir / "schemas"
        self.test_results = []

    def run_cli(self, args: List[str]) -> Tuple[int, str, str]:
        """Run CLI command and return exit code, stdout, stderr."""
        env = os.environ.copy()
        # The product_designer package is in scripts_dir, so add scripts_dir to PYTHONPATH
        env["PYTHONPATH"] = str(self.scripts_dir) + os.pathsep + env.get("PYTHONPATH", "")

        cmd = [sys.executable, "-m", "product_designer.cli"] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.scripts_dir.parent, env=env)
        return result.returncode, result.stdout, result.stderr

    def validate_json(self, json_str: str, schema_name: str) -> Tuple[bool, List[str]]:
        """Validate JSON against schema."""
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]

        # Import validators
        sys.path.insert(0, str(self.scripts_dir))
        from product_designer.validators import validate_response

        return validate_response(schema_name, data)

    def test_design_review(self) -> bool:
        """Test design-review command."""
        print("[PASS] Testing design-review command...")
        code, stdout, stderr = self.run_cli([
            "--output", "json",
            "--validate",
            "design-review",
            "--design", "Onboarding flow",
            "--context", "Mobile app",
            "--goals", "Activate users,Reduce churn",
        ])

        if code != 0:
            print(f"  [FAIL] Exit code: {code}")
            print(f"  stderr: {stderr}")
            return False

        valid, errors = self.validate_json(stdout, "design-review-response")
        if not valid:
            print(f"  [FAIL] Schema validation failed: {errors}")
            return False

        print("  [PASS] design-review command works and validates")
        return True

    def test_problem_framing(self) -> bool:
        """Test problem-framing command."""
        print("[PASS] Testing problem-framing command...")
        code, stdout, stderr = self.run_cli([
            "--output", "json",
            "--validate",
            "problem-framing",
            "--user", "New freelancer",
            "--context", "Setting up first project",
            "--progress", "Get first client",
            "--evidence", "Users drop off at step 3,Support tickets about confusion",
            "--assumptions", "Users understand project structure,Freelancers want clients fast",
        ])

        if code != 0:
            print(f"  [FAIL] Exit code: {code}")
            print(f"  stderr: {stderr}")
            return False

        valid, errors = self.validate_json(stdout, "problem-framing-response")
        if not valid:
            print(f"  [FAIL] Schema validation failed: {errors}")
            return False

        print("  [PASS] problem-framing command works and validates")
        return True

    def test_research_plan(self) -> bool:
        """Test research-plan command."""
        print("[PASS] Testing research-plan command...")
        code, stdout, stderr = self.run_cli([
            "--output", "json",
            "--validate",
            "research-plan",
            "--decision", "Which onboarding pattern",
            "--goal", "Validate user comprehension",
            "--constraints", "2 weeks,5 users,Remote only",
        ])

        if code != 0:
            print(f"  [FAIL] Exit code: {code}")
            print(f"  stderr: {stderr}")
            return False

        valid, errors = self.validate_json(stdout, "research-plan-response")
        if not valid:
            print(f"  [FAIL] Schema validation failed: {errors}")
            return False

        print("  [PASS] research-plan command works and validates")
        return True

    def test_design_brief(self) -> bool:
        """Test design-brief command."""
        print("[PASS] Testing design-brief command...")
        code, stdout, stderr = self.run_cli([
            "--output", "json",
            "--validate",
            "design-brief",
            "--problem", "High drop-off at payment step",
            "--user", "Mobile shopper",
            "--constraints", "Mobile only,2-week sprint,Existing design system",
            "--scope", "2-week sprint",
        ])

        if code != 0:
            print(f"  [FAIL] Exit code: {code}")
            print(f"  stderr: {stderr}")
            return False

        valid, errors = self.validate_json(stdout, "design-brief-response")
        if not valid:
            print(f"  [FAIL] Schema validation failed: {errors}")
            return False

        print("  [PASS] design-brief command works and validates")
        return True

    def test_critique_template(self) -> bool:
        """Test critique-template command."""
        print("[PASS] Testing critique-template command...")
        code, stdout, stderr = self.run_cli([
            "--output", "json",
            "--validate",
            "critique-template",
        ])

        if code != 0:
            print(f"  [FAIL] Exit code: {code}")
            print(f"  stderr: {stderr}")
            return False

        valid, errors = self.validate_json(stdout, "critique-template")
        if not valid:
            print(f"  [FAIL] Schema validation failed: {errors}")
            return False

        print("  [PASS] critique-template command works and validates")
        return True

    def test_checklist(self) -> bool:
        """Test checklist command."""
        print("[PASS] Testing checklist command...")
        for checklist_type in ["handoff", "accessibility", "trust"]:
            code, stdout, stderr = self.run_cli([
                "--output", "json",
                "checklist",
                "--type", checklist_type,
            ])

            if code != 0:
                print(f"  [FAIL] Exit code: {code} for type {checklist_type}")
                print(f"  stderr: {stderr}")
                return False

            try:
                data = json.loads(stdout)
                if "name" not in data or "items" not in data:
                    print(f"  [FAIL] Invalid checklist structure for {checklist_type}")
                    return False
            except json.JSONDecodeError:
                print(f"  [FAIL] Invalid JSON for {checklist_type}")
                return False

        print("  [PASS] checklist command works for all types")
        return True

    def test_output_formats(self) -> bool:
        """Test all output formats work."""
        print("[PASS] Testing output formats...")
        for fmt in ["json", "text", "table"]:
            code, stdout, stderr = self.run_cli([
                "--output", fmt,
                "critique-template",
            ])

            if code != 0:
                print(f"  [FAIL] Format {fmt} failed: {stderr}")
                return False

        print("  [PASS] All output formats work")
        return True

    def test_help(self) -> bool:
        """Test help command."""
        print("[PASS] Testing help command...")
        code, stdout, stderr = self.run_cli(["--help"])

        if code != 0:
            print(f"  [FAIL] Help command failed: {stderr}")
            return False

        if "product-designer" not in stdout:
            print(f"  [FAIL] Help output missing expected content")
            return False

        print("  [PASS] Help command works")
        return True

    def run_all_tests(self) -> bool:
        """Run all contract tests."""
        print("=" * 60)
        print("Product Designer Skill - Contract Tests")
        print("=" * 60)

        tests = [
            self.test_help,
            self.test_design_review,
            self.test_problem_framing,
            self.test_research_plan,
            self.test_design_brief,
            self.test_critique_template,
            self.test_checklist,
            self.test_output_formats,
        ]

        passed = 0
        failed = 0

        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  [FAIL] {test.__name__} raised exception: {e}")
                failed += 1

        print("=" * 60)
        print(f"Results: {passed} passed, {failed} failed")
        print("=" * 60)

        return failed == 0


def main():
    """Run contract tests."""
    test = ContractTest()
    success = test.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()