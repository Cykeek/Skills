# Git Standard

**Version:** 1.0.0 | **Applies to:** All commits, branches, and PRs in this repository

---

## Branch Strategy

```
main (protected)
  ↑
dev (integration branch — PRs target here)
  ↑
feature/<domain>-<skill>-<short-desc>  (short-lived)
```

### Rules
- **Never commit directly to `main` or `dev`**
- **All work on feature branches** from `dev`
- **PRs target `dev`**, never `main`
- **Feature branch naming:** `feature/<domain>-<skill>-<kebab-desc>`
  - Examples: `feature/engineering-zero-hallucination-coder-add-verify-phase`
  - `feature/content-content-writer-add-email-templates`

---

## Commit Convention

**Format:** `<type>(<scope>): <subject>`

### Types
| Type | Meaning |
|------|---------|
| `feat` | New skill, new capability, new reference file |
| `fix` | Bug fix in skill, script, or reference |
| `docs` | Documentation only (README, references, standards) |
| `refactor` | Code restructure without behavior change |
| `style` | Formatting, linting, no logic change |
| `test` | Adding tests for scripts |
| `chore` | Maintenance, deps, config, scaffolding |

### Scope
- Domain name: `engineering`, `content`, `design`, `productivity`, `business`
- Or skill name: `zero-hallucination-coder`, `content-writer`

### Subject
- Imperative mood: "add" not "added"
- Lowercase, no period
- ≤ 72 chars

### Examples
```
feat(engineering): add agent-harness skill with manifest builder
fix(content): correct em-dash replacement in editing checklist
docs(standards): add communication standard with confidence tags
refactor(resume-doctor): extract ATS parser to separate module
chore(templates): update SKILL.md template with quality loop
```

---

## Commit Body (Optional)
- Explain *why* not *what*
- Reference issues: `Fixes #123`, `Relates to #456`
- Separate from subject with blank line

---

## PR Requirements

### Before Opening PR
- [ ] Branch from current `dev`
- [ ] All scripts pass: `python scripts/*.py --help`
- [ ] SKILL.md ≤ 500 lines
- [ ] Frontmatter valid (name, description with "Use when")
- [ ] Related skills table updated bidirectionally
- [ ] Reference index table complete

### PR Template
```markdown
## Summary
<1-2 sentences: what changed and why>

## Type
- [ ] New skill
- [ ] Skill enhancement
- [ ] Bug fix
- [ ] Documentation
- [ ] Standard update

## Testing
- [ ] Skill loads in Claude Code
- [ ] Scripts execute without error
- [ ] References render correctly
- [ ] Related skills still reference correctly

## Checklist
- [ ] SKILL.md structure compliant
- [ ] Anti-patterns section present
- [ ] Quality loop checklist in skill
- [ ] No em dashes in prose
- [ ] Naming conventions followed
```

### Review Gates
1. **Automated:** Lint, structure validation, line count
2. **Peer:** Domain owner + 1 other
3. **Integration:** Skill loads, triggers correctly

---

## Merge Strategy
- **Squash and merge** to `dev`
- **Delete branch** after merge
- **Release tags** on `main` only: `v<major>.<minor>.<patch>`

---

## Release Versioning

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Skill improvement, ref fix | Patch (x.y.z → x.y.z+1) | 2.1.0 → 2.1.1 |
| New skill in domain | Minor (x.y.z → x.y+1.0) | 2.1.1 → 2.2.0 |
| Breaking SKILL.md structure | Major (x.y.z → x+1.0.0) | 2.2.0 → 3.0.0 |

---

*Enforced by CI. Non-compliant commits blocked at PR gate.*