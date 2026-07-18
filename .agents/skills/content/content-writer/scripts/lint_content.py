#!/usr/bin/env python3
"""Lint content for AI tells, formal phrasing, and banned punctuation.

Supports multiple files and directories.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, List

# Import workspace utilities for standardized output management
# workspace_utils.py is copied to this skill's scripts/ directory by scaffold_skill.py
sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace_utils import get_skill_output_dir, create_task_dir


# ─── Patterns ────────────────────────────────────────────────────────────────

BANNED_OPENERS = [
    (
        re.compile(
            r"(?:^|[.!?]\s+)(in today's|in todays|in this article|in this post|in this blog|"
            r"as we all know|it is important to understand|it is important to note|"
            r"the \w+ landscape is evolving|landscape is evolving)\b",
            re.IGNORECASE,
        ),
        "Banned opening/filler pattern found: '{match}'",
    ),
]

ROBOTIC_TELLS = [
    (re.compile(r"\bin order to\b", re.IGNORECASE), "Robotic/filler tell: 'in order to' (use 'to' instead)"),
    (re.compile(r"\bmoreover\b", re.IGNORECASE), "Robotic/filler tell: 'moreover'"),
    (re.compile(r"\bfurthermore\b", re.IGNORECASE), "Robotic/filler tell: 'furthermore'"),
    (re.compile(r"\butiliz\w*\b", re.IGNORECASE), "Robotic/filler tell: 'utilize' or variant (use 'use' instead)"),
    (re.compile(r"\bleverag\w*\b", re.IGNORECASE), "Robotic/filler tell: 'leverage' or variant as verb"),
    (re.compile(r"\bfacilitat\w*\b", re.IGNORECASE), "Robotic/filler tell: 'facilitate' or variant"),
]

FORMAL_PHRASES = [
    (re.compile(r"\bdo not\b", re.IGNORECASE), "do not"),
    (re.compile(r"\bwill not\b", re.IGNORECASE), "will not"),
    (re.compile(r"\bcannot\b", re.IGNORECASE), "cannot"),
    (re.compile(r"\bit is\b", re.IGNORECASE), "it is"),
]

# Fix replacements (order matters)
_FIXES: List[tuple[re.Pattern[str], str | Callable[[re.Match], str]]] = [
    # Banned openers - remove the filler phrase at start of sentence
    (re.compile(r"(?:^|[.!?]\s+)(in today's|in todays|in this article|in this post|in this blog|"
                r"as we all know|it is important to understand|it is important to note|"
                r"the \w+ landscape is evolving|landscape is evolving)\b,?\s*", re.IGNORECASE), ""),
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
    (re.compile(r"\bmoreover\b", re.IGNORECASE), "also"),
    (re.compile(r"\bfurthermore\b", re.IGNORECASE), "also"),
    (re.compile(r"\butiliz\w*\b", re.IGNORECASE), lambda m: m.group(0).replace("utiliz", "us")),
    (re.compile(r"\bleverag\w*\b", re.IGNORECASE), lambda m: m.group(0).replace("leverag", "us")),
    (re.compile(r"\bfacilitat\w*\b", re.IGNORECASE), "help"),
    (re.compile(r"\bdo not\b", re.IGNORECASE), "don't"),
    (re.compile(r"\bwill not\b", re.IGNORECASE), "won't"),
    (re.compile(r"\bcannot\b", re.IGNORECASE), "can't"),
    (re.compile(r"\bit is\b", re.IGNORECASE), "it's"),
    (re.compile(r"\s+\."), "."),
    (re.compile(r"\.\.+"), "."),
    (re.compile(r"\s+,"), ","),
]

_EM_DASH_RULE_PATTERNS = [
    re.compile(r"^#.*\bem[- ]?dash\b.*\b(ban|banned|rule|forbidden)\b", re.IGNORECASE),
    re.compile(r"\bem[- ]?dash\w*\b.*\b(ban|banned|forbidden)\b", re.IGNORECASE),
    re.compile(r"^\|.*\banti[- ]?pattern\b.*\|$", re.IGNORECASE),
]


def is_markdown_table_row(line: str) -> bool:
    """Check if a line is a markdown table row (not a header separator)."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    # Skip header separator rows like |---|---|---|
    if re.match(r"^\|\s*[-:]+", stripped):
        return False
    return True


def is_heading(line: str) -> bool:
    """Check if a line is a markdown heading."""
    return line.strip().startswith("#")


# ─── Data structures ─────────────────────────────────────────────────────────

@dataclass
class Issue:
    line: int
    column: int
    code: str
    message: str
    severity: str  # "warning" | "alert"
    fixable: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LintResult:
    file: str
    issues: List[Issue]
    total_words: int
    formal_count: int
    formal_density: float
    fixed: bool = False

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "issues": [i.to_dict() for i in self.issues],
            "total_words": self.total_words,
            "formal_count": self.formal_count,
            "formal_density_pct": round(self.formal_density, 2),
            "fixed": self.fixed,
            "exit_code": self.exit_code,
        }

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def alert_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "alert")

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0

    @property
    def exit_code(self) -> int:
        if self.fixed:
            return 3
        if self.issues:
            return 1
        return 0


# ─── Helpers ─────────────────────────────────────────────────────────────────

def is_em_dash_rule_reference(line: str) -> bool:
    stripped = line.strip()
    return any(p.search(stripped) for p in _EM_DASH_RULE_PATTERNS)


def replace_em_dashes_smart(line: str) -> str:
    """Replace em-dashes with context-appropriate punctuation."""
    if "—" not in line:
        return line

    result = []
    index = 0
    for match in re.finditer("—", line):
        before = line[: match.start()]
        after = line[match.end() :]

        # Choose replacement based on context
        repl = choose_em_dash_replacement(before, after)
        result.append(line[index : match.start()])
        result.append(repl)
        index = match.end()

    result.append(line[index:])
    return "".join(result)


def choose_em_dash_replacement(before: str, after: str) -> str:
    """Choose a conservative punctuation replacement for an em dash."""
    before = before.rstrip()
    after = after.lstrip()

    if not before or not after:
        return ""

    # If next word is lowercase and we're mid-sentence, use comma
    if after[:1].islower() and before[-1:].isalnum():
        return ", "
    # If introducing an explanation/elaboration, use colon
    if re.match(r"^(namely|specifically|including|for example|for instance|because|when|where|why|how)\b", after, re.IGNORECASE):
        return ": "
    # If preceding ends with conjunction, use space
    if re.search(r"\b(and|but|or|so|yet)\s*$", before, re.IGNORECASE):
        return " "
    # If next starts uppercase, likely new sentence
    if after[:1].isupper():
        return ". "
    # Default: semicolon for closely related clauses
    return "; "


def is_in_anti_pattern_context(line: str, in_section: bool, in_table: bool, in_checklist: bool) -> tuple[bool, bool, bool, bool]:
    """Track anti-pattern context and return (new_in_section, new_in_table, new_in_checklist, should_skip)."""
    stripped = line.strip()

    # Track anti-pattern section (markdown headers)
    if stripped.startswith("#") and "anti-pattern" in stripped.lower():
        return True, False, False, False
    elif stripped.startswith("#") and in_section:
        return False, False, False, False

    # Track checklist/example sections (like "Robotic Tells Checklist")
    if stripped.startswith("#") and any(kw in stripped.lower() for kw in ["checklist", "robotic tells", "banned openings", "before/after"]):
        return False, False, True, False
    elif stripped.startswith("#") and in_checklist:
        return False, False, False, False

    # Track anti-pattern table
    if in_section and stripped.startswith("|"):
        return True, True, in_checklist, True
    elif in_table and stripped.startswith("|"):
        return True, True, in_checklist, True
    elif in_table and not stripped.startswith("|"):
        return True, False, in_checklist, False

    # Track any markdown table (not just anti-pattern ones)
    if is_markdown_table_row(line):
        return in_section, True, in_checklist, True

    # Also skip any markdown table row (they're examples, not prose)
    if stripped.startswith("|") and not re.match(r"^\|\s*-", stripped):
        return in_section, in_table, in_checklist, True

    # Skip bullet list items in checklist sections (they're examples, not prose)
    if in_checklist and stripped.startswith("-"):
        return in_section, in_table, in_checklist, True

    return in_section, in_table, in_checklist, False


def apply_fixes(text: str) -> str:
    lines = text.splitlines(keepends=True)
    fixed_lines = []
    in_anti_pattern_section = False
    in_anti_pattern_table = False
    in_checklist = False

    for line in lines:
        in_anti_pattern_section, in_anti_pattern_table, in_checklist, should_skip = is_in_anti_pattern_context(
            line, in_anti_pattern_section, in_anti_pattern_table, in_checklist
        )

        # Don't apply ANY fixes in rule reference lines, anti-pattern table examples, checklist examples, or headings
        if is_em_dash_rule_reference(line) or should_skip or is_heading(line) or is_markdown_table_row(line):
            fixed_lines.append(line)
            continue

        result = line
        for pattern, repl in _FIXES:
            if callable(repl):
                result = pattern.sub(repl, result)
            else:
                result = pattern.sub(repl, result)

        # Smart em-dash replacement for non-excluded lines
        result = replace_em_dashes_smart(result)
        fixed_lines.append(result)
    return "".join(fixed_lines)


def lint_text(text: str, filepath: str) -> LintResult:
    issues: List[Issue] = []
    total_words = 0
    formal_count = 0
    in_anti_pattern_section = False
    in_anti_pattern_table = False
    in_checklist = False
    in_code_block = False

    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block

        words = line.strip().split()
        total_words += len(words)
        in_anti_pattern_section, in_anti_pattern_table, in_checklist, should_skip = is_in_anti_pattern_context(
            line, in_anti_pattern_section, in_anti_pattern_table, in_checklist
        )

        # Skip headings, markdown tables, checklist/examples, anti-pattern tables, and rule references
        if should_skip or is_heading(line) or is_markdown_table_row(line) or in_code_block:
            continue

        # Em dash (skip in code blocks and rule references)
        if "—" in line and not in_code_block and not is_em_dash_rule_reference(line):
            for match in re.finditer("—", line):
                issues.append(Issue(
                    line=line_no,
                    column=match.start() + 1,
                    code="EM_DASH",
                    message="Em dash (—) found. Rephrase using commas, parentheses, colons, or periods.",
                    severity="warning",
                    fixable=True,
                ))

        # Banned openers
        for pattern, msg_tpl in BANNED_OPENERS:
            for match in pattern.finditer(line):
                issues.append(Issue(
                    line=line_no,
                    column=match.start(1) + 1,
                    code="BANNED_OPENER",
                    message=msg_tpl.format(match=match.group(1)),
                    severity="warning",
                    fixable=False,
                ))

        # Robotic tells
        for pattern, msg in ROBOTIC_TELLS:
            for match in pattern.finditer(line):
                issues.append(Issue(
                    line=line_no,
                    column=match.start() + 1,
                    code="ROBOTIC_TELL",
                    message=msg,
                    severity="warning",
                    fixable=True,
                ))

        # Formal phrases
        for pattern, phrase in FORMAL_PHRASES:
            for match in pattern.finditer(line):
                formal_count += 1
                issues.append(Issue(
                    line=line_no,
                    column=match.start() + 1,
                    code="FORMAL_PHRASE",
                    message=f"Formal structure '{phrase}' found. Consider using a contraction.",
                    severity="alert",
                    fixable=True,
                ))

    formal_density = (formal_count / total_words * 100) if total_words > 0 else 0.0
    if formal_density > 0.5:
        issues.append(Issue(
            line=0,
            column=0,
            code="FORMAL_DENSITY",
            message=f"High density of formal structures without contractions ({formal_density:.2f}%).",
            severity="warning",
            fixable=True,
        ))

    return LintResult(
        file=filepath,
        issues=issues,
        total_words=total_words,
        formal_count=formal_count,
        formal_density=formal_density,
    )


def lint_file(path: Path, fix: bool = False, in_place: bool = False, strict: bool = False) -> LintResult:
    text = path.read_text(encoding="utf-8")

    if fix:
        fixed_text = apply_fixes(text)
        if fixed_text != text:
            if in_place:
                path.write_text(fixed_text, encoding="utf-8")
            result = lint_text(fixed_text, str(path))
            result.fixed = True
            return result

    return lint_text(text, str(path))


def lintfile(path: str | Path, fix: bool = False, in_place: bool = False, strict: bool = False) -> LintResult:
    """Alias for lint_file that accepts string or Path."""
    return lint_file(Path(path), fix=fix, in_place=in_place, strict=strict)


def lint_and_print(path: str | Path, fix: bool = False, in_place: bool = False, strict: bool = False, quiet: bool = False) -> LintResult:
    """Lint a file and print results to stdout (like CLI). Returns LintResult."""
    result = lint_file(Path(path), fix=fix, in_place=in_place, strict=strict)
    if not quiet:
        print(format_text(result, strict))
    return result


def find_markdown_files(paths: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_dir():
            files.extend(p.rglob("*.md"))
        elif p.is_file():
            files.append(p)
        else:
            expanded = list(Path(".").glob(p_str))
            if expanded:
                files.extend(expanded)
            else:
                print(f"Warning: Path not found: {p_str}", file=sys.stderr)
    # Deduplicate while preserving order
    seen = set()
    unique: List[Path] = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)
    return unique


def format_text(result: LintResult, strict: bool) -> str:
    lines = [f"Linting: {result.file}", "-" * 60]
    for issue in result.issues:
        if issue.line:
            lines.append(f"[{issue.line}:{issue.column}] {issue.severity.upper()}: {issue.message} [{issue.code}]")
        else:
            lines.append(f"{issue.severity.upper()}: {issue.message} [{issue.code}]")
    lines.extend([
        "-" * 60,
        f"Total words: {result.total_words}",
        f"Formal phrases: {result.formal_count} ({result.formal_density:.2f}% density)",
        f"Issues found: {len(result.issues)}",
    ])
    if result.formal_density > 0.5:
        lines.append(f"WARNING: High formal density ({result.formal_density:.2f}%) - consider more contractions")
    if result.fixed:
        lines.append("FIXED: File was modified")
    elif not result.issues and result.formal_density <= 0.5:
        lines.append("PASS: No issues found")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint content for AI tells, formal structures, and banned punctuation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lint_content.py file.md                    # Lint, exit 1 if issues
  lint_content.py file.md --json             # JSON output
  lint_content.py file.md --fix --in-place   # Fix in-place, exit 3 if changed
  lint_content.py --strict --json refs/      # CI mode (strict, json, dir ok)
  lint_content.py --strict refs/*.md templates/*.md  # Multiple files
        """,
    )
    parser.add_argument("files", nargs="+", help="Markdown files or directories to lint")
    parser.add_argument("--strict", action="store_true", help="Treat all issues as errors (exit 1 on any issue)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument("--fix", action="store_true", help="Apply fixes")
    parser.add_argument("--in-place", action="store_true", help="Write fixes to files (requires --fix)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress text output (JSON still prints)")
    parser.add_argument("--task-type", default="lint", help="Task type for output subfolder (lint, audit, fix)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    files = find_markdown_files(args.files)

    if not files:
        print("Error: No markdown files found", file=sys.stderr)
        return 1

    all_results: List[LintResult] = []
    any_fixed = False

    for f in files:
        try:
            # When --fix is used, always write in-place (implies --in-place)
            in_place = args.fix or args.in_place
            result = lint_file(f, fix=args.fix, in_place=in_place, strict=args.strict)
            all_results.append(result)
            if result.fixed:
                any_fixed = True
        except OSError as e:
            print(f"Error reading {f}: {e}", file=sys.stderr)
            return 1

    if args.json:
        # Write JSON output to task directory
        task_dir = create_task_dir("content-writer", args.task_type)
        output_path = task_dir / "lint_report.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in all_results], f, indent=2)
        print(f"JSON report saved to: {output_path}", file=sys.stderr)

    if not args.quiet and not args.json:
        for r in all_results:
            print(format_text(r, args.strict))

    # Exit code logic
    if any_fixed:
        return 3
    if args.strict and any(r.has_issues for r in all_results):
        return 1
    if not args.strict and any(r.warning_count > 0 or r.alert_count > 0 for r in all_results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())