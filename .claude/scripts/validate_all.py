#!/usr/bin/env python3
"""Validate all skills in the skills library."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def find_skills(skills_root: Path) -> List[Path]:
    """Find all skill directories."""
    skills = []
    for skill_dir in skills_root.iterdir():
        if not skill_dir.is_dir() or skill_dir.name.startswith('.') or skill_dir.name in {"templates", "standards"}:
            continue
        if (skill_dir / "SKILL.md").exists():
            skills.append(skill_dir)
    return sorted(skills)


def validate_skill(skill_path: Path, strict: bool = False) -> Dict[str, Any]:
    """Run validation on a single skill."""
    script_path = Path(__file__).parent / "validate_skill.py"
    cmd = [sys.executable, str(script_path), str(skill_path), "--json"]
    if strict:
        cmd.append("--strict")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.stdout:
            return json.loads(result.stdout)
        else:
            return {
                "valid": False,
                "errors": [result.stderr or "No output from validator"],
                "warnings": [],
                "skill": skill_path.name,
                "domain": skill_path.parent.name
            }
    except subprocess.TimeoutExpired:
        return {
            "valid": False,
            "errors": ["Validation timed out"],
            "warnings": [],
            "skill": skill_path.name,
            "domain": skill_path.parent.name
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "errors": [f"Validator output not valid JSON: {e}", result.stdout[:500]],
            "warnings": [],
            "skill": skill_path.name,
            "domain": skill_path.parent.name
        }


def main():
    parser = argparse.ArgumentParser(description="Validate all skills in the library")
    parser.add_argument("--skills-root", default=".claude/skills", help="Skills root directory")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"Error: Skills root not found: {skills_root}", file=sys.stderr)
        sys.exit(1)

    skills = find_skills(skills_root)

    if args.domain:
        skills = [s for s in skills if s.parent.name == args.domain]

    if not skills:
        print("No skills found to validate")
        sys.exit(0)

    print(f"Validating {len(skills)} skill(s)...\n")

    results = []
    failed = 0
    total_errors = 0
    total_warnings = 0

    for skill_path in skills:
        result = validate_skill(skill_path, args.strict)
        results.append(result)

        if result["valid"]:
            print(f"✅ {result['domain']}/{result['skill']}")
        else:
            print(f"❌ {result['domain']}/{result['skill']}: {len(result['errors'])} error(s)")
            for e in result["errors"]:
                print(f"   - {e}")
            failed += 1
            total_errors += len(result["errors"])

        if result["warnings"]:
            total_warnings += len(result["warnings"])
            for w in result["warnings"]:
                print(f"   ⚠️  {w}")

        if args.fail_fast and not result["valid"]:
            break

    print(f"\n{'='*50}")
    print(f"Summary: {len(skills) - failed}/{len(skills)} passed, {failed} failed")
    print(f"Errors: {total_errors}, Warnings: {total_warnings}")

    if args.json:
        summary = {
            "total": len(skills),
            "passed": len(skills) - failed,
            "failed": failed,
            "errors": total_errors,
            "warnings": total_warnings,
            "skills": results
        }
        print(json.dumps(summary, indent=2))

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()