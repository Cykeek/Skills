#!/usr/bin/env python3
"""Tests for lint_content.py"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lint_content import lint_text, apply_fixes, find_markdown_files, LintResult


def test_banned_openers():
    text = "In today's world, AI is everywhere. In this article, we explore it."
    result = lint_text(text, "test.md")
    assert any(i.code == "BANNED_OPENER" for i in result.issues)
    assert result.warning_count >= 2


def test_robotic_tells():
    text = "We need to utilize this tool in order to leverage our assets and facilitate the process. Moreover, furthermore."
    result = lint_text(text, "test.md")
    codes = {i.code for i in result.issues}
    assert "ROBOTIC_TELL" in codes
    assert result.warning_count >= 5


def test_formal_phrases():
    text = "Do not worry. It is not a problem. We will not fail. Cannot happen."
    result = lint_text(text, "test.md")
    codes = {i.code for i in result.issues}
    assert "FORMAL_PHRASE" in codes
    assert result.alert_count >= 4


def test_em_dash():
    text = "This is a sentence—with an em dash."
    result = lint_text(text, "test.md")
    assert any(i.code == "EM_DASH" for i in result.issues)


def test_em_dash_exclusion():
    text = "# Em dash ban\nThis is a rule about em-dash banned content."
    result = lint_text(text, "test.md")
    # Should not flag the comment line
    em_dash_issues = [i for i in result.issues if i.code == "EM_DASH"]
    assert len(em_dash_issues) == 0


def test_formal_density():
    text = "Do not do this. It is not good. Will not work. Cannot fail."
    result = lint_text(text, "test.md")
    assert any(i.code == "FORMAL_DENSITY" for i in result.issues)


def test_apply_fixes():
    text = "We need to utilize this in order to leverage our tools. Moreover, we cannot fail. It is do not worry."
    fixed = apply_fixes(text)
    assert "use" in fixed
    assert "to" in fixed
    assert "help" in fixed or "also" in fixed
    assert "can't" in fixed
    assert "it's" in fixed
    assert "don't" in fixed


def test_find_markdown_files(tmp_path):
    (tmp_path / "refs").mkdir()
    (tmp_path / "refs" / "a.md").write_text("# A")
    (tmp_path / "refs" / "b.md").write_text("# B")
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "c.md").write_text("# C")

    import os
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        files = find_markdown_files(["refs/", "templates/"])
        assert len(files) == 3
    finally:
        os.chdir(old_cwd)


def test_json_output():
    text = "In this article, we utilize tools."
    result = lint_text(text, "test.md")
    json_str = json.dumps(result.to_dict(), indent=2)
    data = json.loads(json_str)
    assert data["file"] == "test.md"
    assert "issues" in data
    assert data["exit_code"] == 1


def test_clean_passes():
    text = "This is a clean sentence. You'll like it. It's great."
    result = lint_text(text, "test.md")
    assert result.exit_code == 0
    assert not result.issues


if __name__ == "__main__":
    # Run tests manually
    test_banned_openers()
    print("✓ test_banned_openers")
    test_robotic_tells()
    print("✓ test_robotic_tells")
    test_formal_phrases()
    print("✓ test_formal_phrases")
    test_em_dash()
    print("✓ test_em_dash")
    test_em_dash_exclusion()
    print("✓ test_em_dash_exclusion")
    test_formal_density()
    print("✓ test_formal_density")
    test_apply_fixes()
    print("✓ test_apply_fixes")
    test_find_markdown_files(Path("."))
    print("✓ test_find_markdown_files")
    test_json_output()
    print("✓ test_json_output")
    test_clean_passes()
    print("✓ test_clean_passes")
    print("\nAll tests passed!")