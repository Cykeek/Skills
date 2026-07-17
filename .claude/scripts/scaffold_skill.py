#!/usr/bin/env python3
"""Scaffold a new skill from template."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Dict, Any, Optional


TEMPLATE_PATH = Path(__file__).parent.parent / "skills" / "templates" / "SKILL.md"

DOMAINS = ["engineering", "content", "design", "productivity", "business", "standards"]


def slugify(name: str) -> str:
    """Convert to kebab-case skill name."""
    s = re.sub(r'[^a-z0-9]+', '-', name.lower().strip())
    return s.strip('-')


def validate_domain(domain: str) -> str:
    """Validate and normalize domain."""
    domain = domain.lower()
    if domain not in DOMAINS:
        raise ValueError(f"Invalid domain: {domain}. Must be one of: {', '.join(DOMAINS)}")
    return domain


def validate_skill_name(name: str) -> str:
    """Validate skill name is kebab-case."""
    slug = slugify(name)
    if slug != name.lower():
        raise ValueError(f"Skill name must be kebab-case (lowercase, hyphens only): '{slug}'")
    if not re.match(r'^[a-z0-9-]+$', name):
        raise ValueError(f"Skill name must contain only lowercase letters, numbers, hyphens: '{name}'")
    return name


def read_template() -> str:
    """Read the skill template."""
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding='utf-8')


def render_template(template: str, vars: Dict[str, str]) -> str:
    """Simple template rendering with {{VAR}} placeholders."""
    result = template
    for key, value in vars.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def create_skill_spec_interactive() -> Dict[str, Any]:
    """Interactive wizard to create skill spec."""
    print("=== Skill Scaffold Wizard ===\n")

    spec = {}

    # Domain
    print(f"Available domains: {', '.join(DOMAINS)}")
    while True:
        domain = input("Domain: ").strip().lower()
        try:
            spec['domain'] = validate_domain(domain)
            break
        except ValueError as e:
            print(f"  {e}")

    # Name
    while True:
        name = input("Skill name (kebab-case, e.g., my-skill): ").strip()
        try:
            spec['name'] = validate_skill_name(name)
            break
        except ValueError as e:
            print(f"  {e}")

    # Description
    while True:
        desc = input("Description (must include 'Use when' or 'Use for'): ").strip()
        if "Use when" in desc or "Use for" in desc:
            spec['description'] = desc
            break
        print("  Description must contain 'Use when' or 'Use for' trigger phrase")

    # Triggers (optional)
    triggers = input("Additional trigger phrases (comma-separated, optional): ").strip()
    if triggers:
        spec['triggers'] = [t.strip() for t in triggers.split(',')]

    # References (optional)
    refs = input("Reference files (comma-separated, optional): ").strip()
    if refs:
        spec['references'] = [r.strip() for r in refs.split(',')]

    return spec


def create_skill_spec_from_file(path: Path) -> Dict[str, Any]:
    """Load skill spec from JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Spec file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def scaffold_skill(spec: Dict[str, Any], skills_root: Path, dry_run: bool = False) -> Optional[Path]:
    """Create skill directory structure from spec."""
    domain = spec['domain']
    skill_name = spec['name']
    skill_path = skills_root / domain / skill_name

    if skill_path.exists():
        raise FileExistsError(f"Skill already exists: {skill_path}")

    # Prepare template variables
    triggers = spec.get('triggers', [])
    if not triggers:
        # Extract from description
        desc = spec['description']
        if "Use when" in desc:
            triggers = [desc.split("Use when")[1].split('.')[0].strip()]
        elif "Use for" in desc:
            triggers = [desc.split("Use for")[1].split('.')[0].strip()]

    refs = spec.get('references', [])
    if not refs:
        refs = ["topic-playbook.md", "topic-framework.md", "topic-checklist.md"]
    refs = [r + '.md' if not r.endswith('.md') else r for r in refs]

    today = date.today().isoformat()

    # Build related skills placeholder table
    related_skills = """| Skill | When to Use | When Not to Use |
|-------|-------------|-----------------|
| `domain/skill` | Trigger phrase | Opposite trigger |
| `domain/skill` | Trigger phrase | Opposite trigger |
| `domain/skill` | Trigger phrase | Opposite trigger |"""

    template_vars = {
        "NAME": skill_name,
        "DOMAIN": domain,
        "DESCRIPTION": spec['description'],
        "TRIGGERS": ', '.join(f'"{t}"' for t in triggers),
        "REFERENCES": ', '.join(refs),
        "DATE": today,
        "RELATED_SKILLS_TABLE": related_skills,
        "ASSETS": "template.md, schema.json",
    }

    # Read and render template
    template = read_template()
    rendered = render_template(template, template_vars)

    if dry_run:
        print(f"Would create: {skill_path}/")
        print(f"  SKILL.md ({len(rendered)} chars)")
        print(f"  scripts/{skill_name}.py")
        print(f"  references/{skill_name}-playbook.md")
        print(f"  assets/template.md")
        print("\n--- SKILL.md preview ---")
        print(rendered[:500] + "..." if len(rendered) > 500 else rendered)
        return None

    # Create directory structure
    skill_path.mkdir(parents=True, exist_ok=True)
    (skill_path / "scripts").mkdir(exist_ok=True)
    (skill_path / "references").mkdir(exist_ok=True)
    (skill_path / "assets").mkdir(exist_ok=True)

    # Write SKILL.md
    (skill_path / "SKILL.md").write_text(rendered, encoding='utf-8')

    # Create placeholder script with workspace output management
    script_content = f'''#!/usr/bin/env python3
"""{{{{DESCRIPTION}}}} - CLI tool for {skill_name} skill."""
import argparse
import json
import sys
from pathlib import Path

# Import workspace utilities for standardized output management.
# workspace_utils.py is copied to this skill's scripts/ directory by scaffold_skill.py.
# For shared updates, run scaffold again or copy from .claude/scripts/workspace_utils.py
from workspace_utils import get_skill_output_dir, create_task_dir


def main():
    parser = argparse.ArgumentParser(description="{{DESCRIPTION}}")
    parser.add_argument("--input", help="Input file or value")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--task-type", default="run", help="Task type for output subfolder")
    args = parser.parse_args()

    # Initialize skill output directory (creates outputs/<skill-name>/)
    skill_output_dir = get_skill_output_dir("{skill_name}")
    # Create timestamped task subfolder (outputs/<skill-name>/<task-type>_YYYYMMDD_HHMMSS/)
    task_dir = create_task_dir("{skill_name}", args.task_type)

    # TODO: Implement skill logic
    result = {{
        "skill": "{skill_name}",
        "status": "implemented",
        "message": "TODO: Implement skill logic",
        "output_dir": str(task_dir)
    }}

    if args.format == "json":
        output = json.dumps(result, indent=2)
    else:
        output = str(result)

    if args.output:
        output_path = Path(args.output)
    else:
        # Default: write to task directory
        output_path = task_dir / "output.json"

    output_path.write_text(output, encoding='utf-8')
    print(f"Output written to: {{output_path}}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    script_content = render_template(script_content, template_vars)
    (skill_path / "scripts" / f"{skill_name}.py").write_text(script_content, encoding='utf-8')

    # Create placeholder reference
    ref_content = f'''# {skill_name.replace('-', ' ').title()} Playbook

## Overview
Deep-dive reference for the {skill_name} skill.

## Frameworks
- Framework 1: Description
- Framework 2: Description

## Checklists
### Pre-check
- [ ] Item 1
- [ ] Item 2

### Post-check
- [ ] Item 1
- [ ] Item 2

## Examples
### Example 1
```markdown
Example content
```

## Anti-Patterns
- Anti-pattern 1: Description
- Anti-pattern 2: Description

---
*Part of {skill_name} skill references*
'''
    (skill_path / "references" / f"{skill_name}-playbook.md").write_text(ref_content, encoding='utf-8')

    # Copy workspace utilities to skill scripts for standalone execution
    import shutil
    workspace_utils_src = Path(__file__).parent / "workspace_utils.py"
    if workspace_utils_src.exists():
        shutil.copy2(workspace_utils_src, skill_path / "scripts" / "workspace_utils.py")

    # Create placeholder asset
    asset_content = f'''# {skill_name.replace('-', ' ').title()} Template

## Purpose
Template for {skill_name} deliverables.

## Structure
### Section 1
Content here.

### Section 2
Content here.

---
*Asset for {skill_name} skill*
'''
    (skill_path / "assets" / "template.md").write_text(asset_content, encoding='utf-8')

    print(f"✅ Created skill: {domain}/{skill_name}")
    print(f"   Path: {skill_path}")
    print(f"   Structure:")
    print(f"     SKILL.md")
    print(f"     scripts/{skill_name}.py")
    print(f"     references/{skill_name}-playbook.md")
    print(f"     assets/template.md")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_path}/SKILL.md - fill in Related Skills table, add content")
    print(f"  2. Edit {skill_path}/scripts/{skill_name}.py - implement CLI logic")
    print(f"  3. Add reference files to {skill_path}/references/")
    print(f"  4. Run validation: python .claude/scripts/validate_skill.py {skill_path}")

    return skill_path


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new skill from template")
    parser.add_argument("spec", nargs="?", help="Path to skill spec JSON file")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive wizard")
    parser.add_argument("--skills-root", default=".claude/skills", help="Skills root directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"Error: Skills root not found: {skills_root}", file=sys.stderr)
        sys.exit(1)

    # Load spec
    if args.interactive:
        spec = create_skill_spec_interactive()
    elif args.spec:
        spec = create_skill_spec_from_file(Path(args.spec))
    else:
        print("Error: Provide --interactive or a spec file path", file=sys.stderr)
        sys.exit(1)

    # Validate required fields
    required = ['domain', 'name', 'description']
    for field in required:
        if field not in spec or not spec[field]:
            print(f"Error: Missing required field: {field}", file=sys.stderr)
            sys.exit(1)

    spec['domain'] = validate_domain(spec['domain'])
    spec['name'] = validate_skill_name(spec['name'])

    # Scaffold
    try:
        scaffold_skill(spec, skills_root, args.dry_run)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()