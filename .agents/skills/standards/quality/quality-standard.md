# Quality Standard

**Version:** 1.0.0 | **Applies to:** All skills, scripts, and outputs

---

## Quality Gates (Mandatory)

Every skill must pass these gates before publish:

| Gate | Criteria | Tool |
|------|----------|------|
| **Structure** | Folder layout, naming, required files | `scripts/validate_structure.py` |
| **Frontmatter** | name + description with "Use when" | `scripts/validate_frontmatter.py` |
| **Line Count** | SKILL.md ≤ 500 lines | `wc -l` |
| **File Size** | SKILL.md ≤ 10 KB | `stat` |
| **References Index** | All `references/` files listed in SKILL.md | `scripts/validate_refs.py` |
| **Anti-Patterns** | Table present, ≥3 rows | `scripts/validate_antipatterns.py` |
| **Related Skills** | 3-7 entries, bidirectional | `scripts/validate_related.py` |
| **Quality Loop** | Checklist + confidence tag present | `scripts/validate_quality_loop.py` |
| **No Em Dashes** | Zero `—` in prose (code exempt) | `grep -r "—" --include="*.md"` |
| **Scripts** | Stdlib only, JSON output, --help | `python script.py --help` |

---

## Skill Quality Levels

| Level | Description | Requirements |
|-------|-------------|--------------|
| **🟢 Production** | Ready for any workflow | All gates pass, peer reviewed |
| **🟡 Beta** | Functional, known gaps | Core gates pass, documented limitations |
| **🔴 Draft** | Work in progress | Structure only, content incomplete |

**Default:** New skills start at 🟡 Beta. Promote to 🟢 after 2 weeks real usage + 0 critical issues.

---

## Script Quality Standards

### Required
- **Stdlib only** — No `pip install` needed
- **CLI interface** — `argparse`, `--help` works
- **JSON output** — `--output json` (default), machine-parseable
- **Exit codes** — 0=success, 1=error, 2=validation fail
- **Scoring** — 0-100 where applicable
- **Type hints** — Full annotation

### Template
```python
#!/usr/bin/env python3
"""<One-line description>"""
import argparse, json, sys
from pathlib import Path
from typing import Dict, Any

def analyze(input_path: Path) -> Dict[str, Any]:
    """Core logic. Returns dict for JSON output."""
    # ... implementation
    return {"score": 85, "issues": [], "details": {}}

def main():
    parser = argparse.ArgumentParser(description="<description>")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", choices=["json", "text"], default="json")
    args = parser.parse_args()

    try:
        result = analyze(args.input)
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            # Human-readable summary
            print(f"Score: {result['score']}/100")
        sys.exit(0)
    except FileNotFoundError:
        print(json.dumps({"error": "Input not found"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Output Quality

### Skill Responses
- **Confidence tag** on every claim (🟢/🟡/🔴)
- **Bottom-line first** structure
- **Artifact delivered** — not just advice
- **Self-review note** — what was checked

### Script Outputs
```json
{
  "score": 87,
  "status": "pass",
  "issues": [
    {"severity": "warning", "code": "LINE_LENGTH", "line": 42, "message": "Line exceeds 100 chars"}
  ],
  "details": {
    "lines": 234,
    "functions": 12,
    "complexity": 3.2
  },
  "meta": {
    "script": "code_quality.py",
    "version": "1.0.0",
    "timestamp": "2026-07-15T10:30:00Z"
  }
}
```

---

## Continuous Validation

### Pre-Commit (Local)
```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: skill-structure
        name: Validate skill structure
        entry: python scripts/validate_all.py
        language: system
        files: ^skills/
```

### CI Pipeline
```yaml
# .github/workflows/quality.yml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate all skills
        run: python scripts/validate_all.py --strict
      - name: Test all scripts
        run: python scripts/test_all_scripts.py
      - name: Check cross-references
        run: python scripts/validate_xrefs.py
```

---

## Metrics & SLIs

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Skill load time | < 500ms | > 1s |
| Script execution | < 2s | > 5s |
| Reference accuracy | 100% | < 99% |
| Cross-ref integrity | 100% | < 100% |
| User-reported issues | 0/month | > 2/month |

---

## Incident Response

| Severity | Response | Example |
|----------|----------|---------|
| **P0** | Fix in 4h, hotfix release | Skill crashes Claude Code |
| **P1** | Fix in 24h, patch release | Script returns wrong score |
| **P2** | Fix in next minor | Reference link broken |
| **P3** | Backlog | Typo in reference |

---

*Quality is not a gate — it's the product.*