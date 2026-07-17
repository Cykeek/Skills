# Validation & Scaffolding Scripts

Located in `.claude/scripts/`

## Scripts Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate_skill.py` | Validates single skill structure & content | `python validate_skill.py <skill-path> [--json] [--strict]` |
| `validate_all.py` | Batch validates all skills | `python validate_all.py [--domain <name>] [--json] [--strict] [--fail-fast]` |
| `scaffold_skill.py` | Creates new skill from template | `python scaffold_skill.py [--interactive] [--spec <file>] [--skills-root <path>] [--dry-run]` |

## Quick Start

### Validate a Skill
```bash
python .claude/scripts/validate_skill.py .claude/skills/content/content-writer/
```

### Validate All Skills (JSON output for CI)
```bash
python .claude/scripts/validate_all.py --json
```

### Scaffold New Skill (Interactive)
```bash
python .claude/scripts/scaffold_skill.py --interactive
```

### Scaffold from Spec File
```bash
python .claude/scripts/scaffold_skill.py .claude/skills/templates/example-api-contract-tester-spec.json
```

### Dry Run (Preview)
```bash
python .claude/scripts/scaffold_skill.py .claude/skills/templates/example-seo-optimizer-spec.json --dry-run
```

## Validation Checks

### validate_skill.py Checks

| Category | Checks |
|----------|--------|
| Structure | Required directories (scripts/, references/, assets/), SKILL.md exists |
| Frontmatter | Valid YAML, `name` (kebab-case), `description` with "Use when" trigger |
| Content | 5 required sections (Anti-Patterns, Short-Circuit, Related Skills, Reference Files, Quality Loop) |
| Prose Quality | No em dashes (—) in body text, ≤500 lines |
| Cross-References | Related skills table (3-7 entries, with when/when-not), references exist |
| Scripts | Shebang, argparse, JSON output, stdlib-only imports, syntax valid |
| References | All .md files listed in index, all indexed files exist |

### validate_all.py Features
- Auto-discovers skills in `.claude/skills/<domain>/<skill>/`
- Excludes `templates/` and `standards/` directories
- Domain filter: `--domain engineering`
- Fail-fast: `--fail-fast` stops on first failure
- Strict mode: `--strict` treats warnings as errors
- JSON output for CI integration

## Scaffold Skill Spec Format (JSON)

```json
{
  "domain": "engineering|content|design|productivity|business|standards",
  "name": "kebab-case-skill-name",
  "description": "Use when <trigger>. Example: '<user request>'. Delivers <output>.",
  "version": "1.0.0",
  "author": "Claude Code",
  "tags": ["tag1", "tag2"],
  "triggers": ["Trigger phrase 1", "Trigger phrase 2"],
  "anti_patterns": ["Anti-pattern 1", "Anti-pattern 2"],
  "short_circuits": ["Full Loop: ...", "Abbreviated: ...", "Direct: ..."],
  "quality_loop": ["Check 1", "Check 2", "Check 3"],
  "related_skills": [
    {"skill": "domain/skill", "when": "When to use", "when_not": "When to avoid"}
  ],
  "references": [
    {"file": "topic.md", "purpose": "Description", "sections": "Key sections"}
  ]
}
```

## Example Spec Files

| File | Domain | Skill |
|------|--------|-------|
| `example-api-contract-tester-spec.json` | engineering | API contract validation |
| `example-seo-optimizer-spec.json` | content | SEO optimization |
| `example-case-study-builder-spec.json` | content | Case study creation |
| `example-task-manager-spec.json` | productivity | GTD task management |

## CI Integration

### GitHub Actions Example
```yaml
- name: Validate Skills
  run: |
    python .claude/scripts/validate_all.py --json --strict > validation.json
    python -c "import json; data=json.load(open('validation.json')); exit(0 if data['failed']==0 else 1)"
```

### Pre-commit Hook
```yaml
- repo: local
  hooks:
    - id: validate-skills
      name: Validate Skills
      entry: python .claude/scripts/validate_all.py --fail-fast
      language: system
      pass_filenames: false
```

## Troubleshooting

### "No module named 'yaml'"
```bash
pip install pyyaml
```

### Permission Denied
```bash
chmod +x .claude/scripts/*.py
```

### Python Not Found
Ensure Python 3.10+ is installed and in PATH.

## Extending Validation

Add custom checks by extending `SkillValidator` class in `validate_skill.py`:

```python
class CustomValidator(SkillValidator):
    def _check_custom(self):
        # Your custom validation logic
        pass
    
    def run_all(self):
        super().run_all()
        self._check_custom()
        return self.results
```