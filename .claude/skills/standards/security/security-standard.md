# Security Standard

**Version:** 1.0.0 | **Applies to:** All skills, scripts, and repository practices

---

## Core Principles

1. **No secrets in code** — ever
2. **Least privilege** — scripts read only what they need
3. **Input validation** — all external input sanitized
4. **Audit trail** — security-relevant actions logged

---

## Secrets Management

### Prohibited
- API keys, tokens, passwords in any file
- `.env` files committed
- Hardcoded credentials in scripts
- Secrets in comments or docs

### Required
- **Environment variables** for all secrets
- **`.env.example`** with placeholder names (committed)
- **`settings.local.json`** for local config (gitignored)
- **CI secrets** via platform secret store (GitHub Actions, GitLab CI)

### Skill Scripts
```python
# ✅ Good: Read from env
api_key = os.environ.get("CAL_COM_API_KEY")
if not api_key:
    raise ValidationError("CAL_COM_API_KEY not set")

# ❌ Bad: Hardcoded
api_key = "cal_live_abc123"
```

---

## Input Validation

### All Scripts Must Validate
```python
def validate_input(path: str) -> Path:
    p = Path(path).resolve()
    # Restrict to allowed directories
    allowed = [Path.cwd(), Path.cwd() / "data"]
    if not any(p.is_relative_to(a) for a in allowed):
        raise ValidationError(f"Path outside allowed directories: {p}")
    return p
```

### File Operations
- **Read:** Validate path, check extension, limit size (≤ 10MB default)
- **Write:** Validate path, ensure directory exists, no overwrite without flag
- **Execute:** Never `subprocess` with user input; if needed, allowlist commands

---

## Network Calls (If Needed)

### Stdlib Only — Use `urllib`
```python
import urllib.request, json

def fetch_json(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "claude-skills/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)
```

### Rules
- **Timeouts mandatory** (default 10s)
- **Validate SSL** (default behavior)
- **No auth in URLs** — use headers from env
- **Rate limit** — respect `Retry-After`, implement backoff

---

## File System Safety

### Path Traversal Prevention
```python
def safe_join(base: Path, *parts: str) -> Path:
    target = (base / Path(*parts)).resolve()
    base_resolved = base.resolve()
    if not target.is_relative_to(base_resolved):
        raise ValidationError("Path traversal attempt")
    return target
```

### Temporary Files
```python
import tempfile

with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(data, f)
    temp_path = f.name
# Process, then clean up
Path(temp_path).unlink(missing_ok=True)
```

---

## Skill-Specific Security

### SKILL.md Must Document
- What data the skill reads/writes
- What external services it calls (if any)
- What permissions it needs
- What user data it processes

### Example Security Section in SKILL.md
```markdown
## Security Profile

**Data Access:**
- Reads: User-provided content files (opt-in)
- Writes: Output artifacts to `./output/` (user-controlled)
- Network: None (offline skill)

**Permissions Required:**
- File read/write in working directory
- No environment variables required

**User Data Handling:**
- Input content processed in memory only
- No logging of user content
- No telemetry
```

---

## CI Security Gates

| Gate | Tool | Fail On |
|------|------|---------|
| Secrets scan | `gitleaks` | Any secret pattern |
| Dependency audit | `pip-audit` (if deps added) | CVE ≥ HIGH |
| Path traversal | Custom lint | `../` in user-controlled paths |
| Shell injection | Custom lint | `subprocess` with `shell=True` |

---

## Incident Response

1. **Detect:** CI gate fails or user reports
2. **Contain:** Revert commit, rotate exposed secrets
3. **Assess:** Scope of exposure
4. **Remediate:** Fix root cause, add regression test
5. **Document:** Update this standard if new pattern

---

## Compliance Notes

- **No PII** in skills, scripts, or references
- **No regulated data** (HIPAA, PCI, etc.) without explicit domain approval
- **Export control:** Stdlib-only ensures no restricted crypto

---

*Security is a feature, not a checkbox. Build it in from line 1.*