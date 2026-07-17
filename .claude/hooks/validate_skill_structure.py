#!/usr/bin/env python3
"""Validate skill structure after write/edit."""
import sys
import re
from pathlib import Path

def validate_skill_structure(file_path: str) -> tuple[bool, list[str]]:
    """Validate skill file structure."""
    path = Path(file_path)
    errors = []

    # Only validate SKILL.md files
    if path.name != "SKILL.md":
        return True, []

    # Check it's in a skill directory
    skill_dir = path.parent
    if not (skill_dir / "scripts").exists() and not (skill_dir / "references").exists():
        # Allow during creation - just warn
        pass

    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return True, []

    # Check frontmatter
    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter (must start with ---)")

    # Check frontmatter has name and description
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        fm = frontmatter_match.group(1)
        if 'name:' not in fm:
            errors.append("Frontmatter missing 'name' field")
        if 'description:' not in fm:
            errors.append("Frontmatter missing 'description' field")
        elif 'Use when' not in fm:
            errors.append("Description must contain 'Use when' trigger phrase")

    # Check line count
    lines = content.count('\n')
    if lines > 500:
        errors.append(f"SKILL.md exceeds 500 lines ({lines})")

    # Check for em dashes in prose
    for i, line in enumerate(content.splitlines(), 1):
        if '—' in line and '`' not in line:
            # Allow in frontmatter and code
            if not (frontmatter_match and i <= frontmatter_match.end() + 1):
                errors.append(f"Line {i}: Em dash in prose (replace with . , : or ())")

    return len(errors) == 0, errors

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_skill_structure.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    is_valid, errors = validate_skill_structure(file_path)

    if not is_valid:
        print(f"⚠️  Skill structure warnings for {file_path}:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        # Warning only, don't block
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()