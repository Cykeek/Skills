#!/usr/bin/env python3
"""
Wix Support Skill - Contract Tests
===================================
Contract tests for the Wix Support Skill CLI.
"""

import json
import subprocess
import sys
import os
from pathlib import Path


class ContractTester:
    """Run contract tests for the Wix Support Skill CLI."""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.skill_dir = self.script_dir.parent
        self.cli_module = "wix_support_skill.cli"
        self.passed = 0
        self.failed = 0

    def run_cli(self, args: list) -> subprocess.CompletedProcess:
        """Run the CLI with given arguments."""
        cmd = [sys.executable, "-m", self.cli_module] + args
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.skill_dir / "scripts"
        )

    def assert_json_output(self, result: subprocess.CompletedProcess, test_name: str) -> dict:
        """Assert output is valid JSON and return parsed data."""
        try:
            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError as e:
            self.fail(test_name, f"Invalid JSON output: {e}\nStdout: {result.stdout[:500]}\nStderr: {result.stderr[:500]}")
            return {}

    def assert_valid_response(self, data: dict, schema_name: str, test_name: str) -> bool:
        """Validate response against schema."""
        # Import validators
        sys.path.insert(0, str(self.skill_dir / "scripts" / "wix_support_skill"))
        from validators import validate_response

        valid, errors = validate_response(schema_name, data)
        if not valid:
            self.fail(test_name, f"Response validation failed: {errors}")
            return False
        return True

    def pass_test(self, test_name: str):
        """Mark test as passed."""
        self.passed += 1
        print(f"  [PASS] {test_name}")

    def fail(self, test_name: str, reason: str):
        """Mark test as failed."""
        self.failed += 1
        print(f"  [FAIL] {test_name}: {reason}")

    def run_tests(self):
        """Run all contract tests."""
        print("Running Wix Support Skill Contract Tests")
        print("=" * 50)

        # Test 1: CLI help
        self.test_help()

        # Test 2: diagnose command
        self.test_diagnose()

        # Test 3: velo-check command
        self.test_velo_check()

        # Test 4: cms-debug command
        self.test_cms_debug()

        # Test 5: dns-check command
        self.test_dns_check()

        # Test 6: editor-compare command
        self.test_editor_compare()

        # Test 7: ai-tools command
        self.test_ai_tools()

        # Test 8: escalation command
        self.test_escalation()

        # Test 9: validate schema
        self.test_schema_validation()

        # Test 10: output formats
        self.test_output_formats()

        # Summary
        print("\n" + "=" * 50)
        print(f"Tests passed: {self.passed}")
        print(f"Tests failed: {self.failed}")

        if self.failed > 0:
            sys.exit(1)

    def test_help(self):
        """Test CLI help command."""
        result = self.run_cli(["--help"])
        if result.returncode == 0 and "usage" in result.stdout.lower():
            self.pass_test("CLI --help")
        else:
            self.fail("CLI --help", f"Exit code: {result.returncode}, stdout: {result.stdout[:200]}")

    def test_diagnose(self):
        """Test diagnose command with valid input."""
        result = self.run_cli([
            "diagnose",
            "--editor", "studio",
            "--issue", "Mobile layout breaks on tablet breakpoint",
        ])
        if result.returncode != 0:
            self.fail("diagnose command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "diagnose output")
        if self.assert_valid_response(data, "diagnose-response", "diagnose response schema"):
            self.pass_test("diagnose command")

    def test_velo_check(self):
        """Test velo-check command with valid input."""
        result = self.run_cli([
            "velo-check",
            "--element-id", "#submitBtn",
            "--code", "$w('#submitBtn').onClick(() => { $w('#form1').submit(); });",
            "--error", "TypeError: $w(...) is undefined",
        ])
        if result.returncode != 0:
            self.fail("velo-check command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "velo-check output")
        if self.assert_valid_response(data, "velo-check-response", "velo-check response schema"):
            self.pass_test("velo-check command")

    def test_cms_debug(self):
        """Test cms-debug command with valid input."""
        result = self.run_cli([
            "cms-debug",
            "--collection", "BlogPosts",
            "--page-slug", "blog/post-title",
        ])
        if result.returncode != 0:
            self.fail("cms-debug command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "cms-debug output")
        if self.assert_valid_response(data, "cms-debug-response", "cms-debug response schema"):
            self.pass_test("cms-debug command")

    def test_dns_check(self):
        """Test dns-check command with valid input."""
        result = self.run_cli(["dns-check", "--domain", "example.com"])
        if result.returncode != 0:
            self.fail("dns-check command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "dns-check output")
        if self.assert_valid_response(data, "dns-check-response", "dns-check response schema"):
            self.pass_test("dns-check command")

    def test_editor_compare(self):
        """Test editor-compare command."""
        result = self.run_cli(["editor-compare"])
        if result.returncode != 0:
            self.fail("editor-compare command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "editor-compare output")
        if self.assert_valid_response(data, "editor-comparison", "editor-compare response schema"):
            self.pass_test("editor-compare command")

    def test_ai_tools(self):
        """Test ai-tools command."""
        result = self.run_cli(["ai-tools"])
        if result.returncode != 0:
            self.fail("ai-tools command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "ai-tools output")
        if "ai_site_generator" in data or "ai_tools" in data:
            self.pass_test("ai-tools command")
        else:
            self.fail("ai-tools command", "Missing expected keys in response")

    def test_escalation(self):
        """Test escalation command."""
        result = self.run_cli(["escalation"])
        if result.returncode != 0:
            self.fail("escalation command", f"Exit code: {result.returncode}, stderr: {result.stderr}")
            return

        data = self.assert_json_output(result, "escalation output")
        if "escalate_to_wix_support" in data or "escalation_guide" in data:
            self.pass_test("escalation command")
        else:
            self.fail("escalation command", "Missing expected keys in response")

    def test_schema_validation(self):
        """Test schema validation functions."""
        sys.path.insert(0, str(self.skill_dir / "scripts" / "wix_support_skill"))
        from validators import validate_request, validate_response

        # Test valid diagnose request
        valid_req = {"editor": "studio", "issue": "test issue"}
        valid, errors = validate_request("diagnose-request", valid_req)
        if valid:
            self.pass_test("validate valid diagnose request")
        else:
            self.fail("validate valid diagnose request", f"Errors: {errors}")

        # Test invalid diagnose request (missing required field)
        invalid_req = {"editor": "studio"}
        valid, errors = validate_request("diagnose-request", invalid_req)
        if not valid and errors:
            self.pass_test("validate invalid diagnose request")
        else:
            self.fail("validate invalid diagnose request", "Should have failed validation")

    def test_output_formats(self):
        """Test different output formats."""
        # Test text output
        result = self.run_cli(["--output", "text", "diagnose", "--editor", "studio", "--issue", "test"])
        if result.returncode == 0 and result.stdout.strip():
            self.pass_test("output format: text")
        else:
            self.fail("output format: text", f"Exit code: {result.returncode}, stderr: {result.stderr}")

        # Test table output
        result = self.run_cli(["--output", "table", "editor-compare"])
        if result.returncode == 0 and result.stdout.strip():
            self.pass_test("output format: table")
        else:
            self.fail("output format: table", f"Exit code: {result.returncode}, stderr: {result.stderr}")


if __name__ == "__main__":
    tester = ContractTester()
    tester.run_tests()