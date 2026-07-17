#!/usr/bin/env python3
"""Validate no em dashes in prose files."""
import sys
import re
from pathlib import Path

def check_file(file_path: str) -> tuple[bool, list[str]]:
    """Check file for em dashes. Returns (is_clean, violations)."""
    path = Path(file_path)
    if not path.exists():
        return True, []

    # Only check markdown and text files
    if path.suffix not in ['.md', '.txt', '.py']:
        return True, []

    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return True, []

    violations = []
    for i, line in enumerate(content.splitlines(), 1):
        # Find em dashes not in code blocks
        if '—' in line:
            # Simple check: if line has backticks, might be code
            if '`' not in line or line.count('`') % 2 == 0:
                violations.append(f"Line {i}: {line.strip()[:80]}")

    return len(violations) == 0, violations

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_no_em_dash.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    is_clean, violations = check_file(file_path)

    if not is_clean:
        print(f"❌ Em dashes found in {file_path}:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        print("Replace '—' with '.', ':', ',', or '()' in prose.", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()