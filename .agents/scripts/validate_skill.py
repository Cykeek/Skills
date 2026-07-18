#!/usr/bin/env python3
"""Validate a single skill structure and content."""
import argparse
import json
import re
import sys
try:
    import yaml
except ImportError:
    yaml = None
from pathlib import Path
from typing import Dict, List, Tuple, Any

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

class SkillValidator:
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.skill_md = skill_path / "SKILL.md"
        self.content = ""
        self.frontmatter = {}

    def run_all(self) -> Dict[str, Any]:
        """Run all validation checks."""
        self._check_structure()
        self._check_frontmatter()
        self._check_content_sections()
        self._check_prose_quality()
        self._check_cross_references()
        self._check_scripts()
        self._check_references()
        self._check_output_management()

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "skill": self.skill_path.name,
            "domain": self.skill_path.parent.name
        }

    def _check_structure(self):
        """Validate folder structure."""
        required_dirs = ["scripts", "references", "assets"]
        for d in required_dirs:
            if not (self.skill_path / d).exists():
                self.warnings.append(f"Missing directory: {d}/")

        if not self.skill_md.exists():
            self.errors.append("Missing SKILL.md")

    def _check_frontmatter(self):
        """Validate YAML frontmatter."""
        if not self.skill_md.exists():
            return

        self.content = self.skill_md.read_text(encoding='utf-8')

        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---', self.content, re.DOTALL)
        if not match:
            self.errors.append("Missing or invalid YAML frontmatter (must start with ---)")
            return

        try:
            if yaml:
                self.frontmatter = yaml.safe_load(match.group(1)) or {}
            else:
                raw_fm = match.group(1)
                self.frontmatter = {}
                for line in raw_fm.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if ':' in line:
                        k, v = line.split(':', 1)
                        k = k.strip()
                        v = v.strip()
                        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                            v = v[1:-1]
                        self.frontmatter[k] = v
        except Exception as e:
            self.errors.append(f"Invalid YAML frontmatter: {e}")
            return

        # Required fields
        if 'name' not in self.frontmatter:
            self.errors.append("Frontmatter missing 'name' field")
        elif not re.match(r'^[a-z0-9-]+$', self.frontmatter['name']):
            self.errors.append(f"Skill name must be kebab-case: {self.frontmatter['name']}")

        if 'description' not in self.frontmatter:
            self.errors.append("Frontmatter missing 'description' field")
        else:
            desc = self.frontmatter['description']
            if 'Use when' not in desc and 'Use for' not in desc:
                self.errors.append("Description must contain 'Use when' or 'Use for' trigger phrase")
            if len(desc) > 300:
                self.warnings.append(f"Description long ({len(desc)} chars), consider shortening")

    def _check_content_sections(self):
        """Validate required content sections."""
        if not self.content:
            return

        required_sections = [
            ("Anti-Patterns", r"##\s+\d*\.?\s*Anti[- ]?Patterns?"),
            ("Short-Circuit", r"##\s+\d*\.?\s*Short[- ]?Circuit"),
            ("Related Skills", r"##\s+\d*\.?\s*Related Skills?"),
            ("Reference Files", r"##\s+\d*\.?\s*Reference Files?"),
            ("Quality Loop", r"##\s+\d*\.?\s*Quality Loop"),
        ]

        for name, pattern in required_sections:
            if not re.search(pattern, self.content, re.IGNORECASE):
                self.errors.append(f"Missing required section: {name}")

        # Check Related Skills table has 3-7 entries
        related_match = re.search(r'\| Skill \|.*?\n((?:\|.*?\n)+)', self.content, re.IGNORECASE)
        if related_match:
            rows = [r for r in related_match.group(1).split('\n') if '|' in r and '---' not in r]
            if len(rows) < 3:
                self.warnings.append(f"Related Skills table has only {len(rows)} entries (recommended: 3-7)")
            elif len(rows) > 7:
                self.warnings.append(f"Related Skills table has {len(rows)} entries (recommended: max 7)")

    def _check_prose_quality(self):
        """Check for em dashes and other prose issues."""
        if not self.content:
            return

        # Find em dashes in prose (not in code blocks)
        lines = self.content.split('\n')
        in_code_block = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if not in_code_block and '—' in line:
                # Skip frontmatter
                if i < 20 and line.strip().startswith('---'):
                    continue
                self.errors.append(f"Line {i}: Em dash (—) in prose - replace with . , : or ()")

        # Check line count
        total_lines = len(lines)
        if total_lines > 500:
            self.errors.append(f"SKILL.md exceeds 500 lines ({total_lines})")

    def _check_cross_references(self):
        """Validate cross-references in Related Skills table."""
        if not self.content:
            return

        # Extract skill references from Related Skills table
        related_match = re.search(r'##\s+\d*\.?\s*Related Skills?.*?\n\| Skill \|.*?\n((?:\|.*?\n)+)', self.content, re.IGNORECASE | re.DOTALL)
        table_text = related_match.group(1) if related_match else ""
        refs = re.findall(r'\| `([^`]+)` \|', table_text)
        for ref in refs:
            # Check if it's a valid domain/skill path
            clean_ref = ref.replace('skills/', '').strip('/')
            if '/' not in clean_ref:
                self.warnings.append(f"Related skill reference missing domain: {ref}")
            else:
                parts = [p for p in clean_ref.split('/') if p]
                if len(parts) >= 2:
                    domain, skill = parts[-2], parts[-1]
                    skill_path = self.skill_path.parent.parent / domain / skill / "SKILL.md"
                    if not skill_path.exists():
                        self.warnings.append(f"Referenced skill not found: {ref}")

    def _check_scripts(self):
        """Validate Python scripts in scripts/."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        # Find all local modules/packages and requirements
        local_names = {f.stem for f in scripts_dir.glob("*.py")} | {d.name for d in scripts_dir.iterdir() if d.is_dir()}
        reqs = set()
        for req_file in [scripts_dir / "requirements.txt", self.skill_path / "requirements.txt"]:
            if req_file.exists():
                for line in req_file.read_text(encoding='utf-8').splitlines():
                    clean_line = re.split(r'[=<>~!]', line.strip())[0].strip()
                    if clean_line and not clean_line.startswith('#'):
                        reqs.add(clean_line.lower())
                        reqs.add(clean_line.split('-')[0].lower())
                        reqs.add(clean_line.replace('-', '_').lower())

        for script in scripts_dir.glob("*.py"):
            try:
                content = script.read_text(encoding='utf-8')
                is_entry_point = ('__main__' in content) or (script.name in {'cli.py', 'main.py'}) and script.name != '__init__.py'

                if is_entry_point:
                    # Check for shebang
                    if not content.startswith('#!/usr/bin/env python3'):
                        self.warnings.append(f"{script.name}: Missing shebang")

                    # Check for argparse
                    if 'argparse' not in content:
                        self.warnings.append(f"{script.name}: No argparse (CLI interface recommended)")

                    # Check for JSON output
                    if 'json.dumps' not in content and 'print(json' not in content:
                        self.warnings.append(f"{script.name}: No JSON output detected")

                # Check for external imports (non-stdlib)
                stdlib_modules = {'argparse', 'json', 'sys', 'os', 'pathlib', 'typing',
                                 're', 'datetime', 'collections', 'itertools', 'functools',
                                 'subprocess', 'tempfile', 'hashlib', 'uuid', 'dataclasses',
                                 'asyncio', 'time', 'enum', 'urllib', 'textwrap', 'hmac',
                                 'math', 'copy', 'io', 'shutil', 'inspect', 'abc', 'contextlib',
                                 'logging', 'urllib.parse', 'urllib.request', '__future__', 'traceback'}
                if hasattr(sys, 'stdlib_module_names'):
                    stdlib_modules.update(sys.stdlib_module_names)

                imports = re.findall(r'^(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)', content, re.MULTILINE)
                for imp in imports:
                    if imp not in stdlib_modules and imp not in local_names and not imp.startswith('.'):
                        if imp.lower() not in reqs and imp.replace('_', '-').lower() not in reqs:
                            self.warnings.append(f"{script.name}: Possible non-stdlib import: {imp}")

                # Check --help works (basic syntax check)
                try:
                    compile(content, script, 'exec')
                except SyntaxError as e:
                    self.errors.append(f"{script.name}: Syntax error - {e}")

            except Exception as e:
                self.warnings.append(f"Could not validate {script.name}: {e}")

    def _check_references(self):
        """Validate reference files exist and are listed."""
        refs_dir = self.skill_path / "references"
        if not refs_dir.exists():
            return

        # Find all .md files in references
        actual_refs = {f.name for f in refs_dir.glob("*.md")}

        # Extract from Reference Files Index table
        listed_refs = set()
        table_match = re.search(r'##\s+\d*\.?\s*Reference Files?.*?\n\| File \|.*?\n((?:\|.*?\n)+)', self.content, re.IGNORECASE | re.DOTALL)
        if not table_match:
            table_match = re.search(r'\| File \|.*?\n((?:\|.*?\n)+)', self.content, re.IGNORECASE)
        if table_match:
            for line in table_match.group(1).split('\n'):
                if '|' in line and '---' not in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 2:
                        file_ref = parts[1].strip()
                        if file_ref.startswith('`') and file_ref.endswith('`'):
                            listed_refs.add(file_ref[1:-1])

        # Check for unlisted reference files
        for ref in actual_refs:
            if ref not in listed_refs:
                self.warnings.append(f"Reference file not in index: {ref}")

        # Check for listed but missing files
        for ref in listed_refs:
            if ref not in actual_refs:
                self.warnings.append(f"Listed reference file missing: {ref}")

    def _check_output_management(self):
        """Validate skill uses standardized workspace output management."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        # Check for output management patterns in scripts
        has_output_management = False
        has_workspace_utils = False

        for script in scripts_dir.glob("*.py"):
            if script.name == "__init__.py":
                continue
            try:
                content = script.read_text(encoding='utf-8')
                # Check for workspace_utils import or get_skill_output_dir/create_task_dir usage
                if "workspace_utils" in content or "get_skill_output_dir" in content or "create_task_dir" in content:
                    has_workspace_utils = True
                # Check for any output directory management
                if "output" in content.lower() and ("mkdir" in content or "Path(" in content or "write" in content):
                    has_output_management = True
            except Exception:
                pass

        if not has_workspace_utils:
            self.warnings.append(f"Skill scripts should import workspace_utils for standardized output management (get_skill_output_dir, create_task_dir)")

        if has_output_management and not has_workspace_utils:
            self.warnings.append(f"Skill writes output files but doesn't use workspace_utils - outputs may go to non-standard directory")


def main():
    parser = argparse.ArgumentParser(description="Validate skill structure and content")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"Error: Path not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    validator = SkillValidator(skill_path)
    result = validator.run_all()

    if args.strict and result["warnings"]:
        result["errors"].extend(result["warnings"])
        result["warnings"] = []

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print(f"✅ {result['domain']}/{result['skill']}: Valid")
        else:
            print(f"❌ {result['domain']}/{result['skill']}: {len(result['errors'])} errors")
            for e in result["errors"]:
                print(f"  - {e}")

        if result["warnings"]:
            print(f"⚠️  {len(result['warnings'])} warnings:")
            for w in result["warnings"]:
                print(f"  - {w}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()