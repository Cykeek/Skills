# Agent Template

**Purpose:** Starting point for creating cs-* prefixed agents that orchestrate skills.

---

## Agent File Structure

Save as: `.claude/agents/<domain>/cs-<agent-name>.md`

```markdown
---
name: cs-<agent-name>
description: "Use when <specific trigger condition>. Example: 'User wants to <action>.'"
skills:
  - <domain>/<skill-1>
  - <domain>/<skill-2>
  - <other-domain>/<skill-3>
domain: <domain-name>
model: sonnet
tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task", "Agent"]
---

# cs-<agent-name>

## Purpose

<1-2 sentences: what this agent achieves that skills alone cannot. "Orchestrates X to achieve Y.">

## Skill Integration

This agent coordinates the following skills:

| Skill | Role in Workflow | When Invoked |
|-------|------------------|--------------|
| `<domain>/<skill-1>` | <e.g., "Primary executor"> | <trigger> |
| `<domain>/<skill-2>` | <e.g., "Validator"> | <trigger> |
| `<other-domain>/<skill-3>` | <e.g., "Cross-cutting concern"> | <trigger> |

**Path Convention:** Skills referenced via relative paths from agent file:
- Same domain: `../../skills/<domain>/<skill-name>`
- Other domain: `../../skills/<other-domain>/<skill-name>`

## Workflows

### Workflow 1: <Primary Use Case>

**Trigger:** <User says / condition>

**Steps:**
1. <Step 1: invoke skill X with...>
2. <Step 2: invoke skill Y with...>
3. <Step 3: synthesize results...>

**Output:** <Concrete deliverable>

### Workflow 2: <Secondary Use Case>

**Trigger:** <User says / condition>

**Steps:**
1. ...
2. ...

**Output:** <Concrete deliverable>

### Workflow 3: <Tertiary / Edge Case>

**Trigger:** <User says / condition>

**Steps:**
1. ...
2. ...

**Output:** <Concrete deliverable>

## Integration Examples

### Example 1: <Scenario>

**User:** "<User request>"

**Agent executes:**
```
1. Read ../../skills/<domain>/<skill>/SKILL.md
2. Invoke skill with parameters: {...}
3. Read reference: ../../skills/<domain>/<skill>/references/<ref>.md
4. Synthesize and present
```

**Result:** <What user receives>

### Example 2: <Scenario>

...

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task completion rate | > 90% | User confirms done |
| Skill selection accuracy | > 95% | Right skill for request |
| Output quality | > 4/5 | User rating |
| Turn count | < 5 | Avg turns to completion |

## Related Agents

| Agent | Relationship | When to Delegate |
|-------|--------------|------------------|
| `cs-<other-agent>` | <complementary/overlaps> | <condition> |

## References

- `../../skills/<domain>/<skill>/references/<file>.md`
- `../../standards/<standard>.md`
- `../../templates/<template>.md`
```

---

## Agent Creation Checklist

- [ ] YAML frontmatter complete (name, description with "Use when", skills, domain, model, tools)
- [ ] Purpose statement clear and differentiated from skills
- [ ] Skill integration table with roles and triggers
- [ ] Relative paths use `../../skills/` pattern
- [ ] Minimum 3 workflows documented
- [ ] 2+ integration examples with concrete user quotes
- [ ] Success metrics table defined
- [ ] Related agents listed
- [ ] References section points to actual files
- [ ] No hardcoded absolute paths
- [ ] Tested: agent loads and invokes skills correctly

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Agent duplicates skill logic | Agent ONLY orchestrates; skills do the work |
| Absolute paths in skill refs | Use `../../skills/<domain>/<skill>` |
| Missing "Use when" in description | Add concrete trigger example |
| Too many skills (>7) | Split into multiple agents |
| No integration examples | Add 2+ realistic user scenarios |
| Skills not in same repo | All skills must be local |

---

## Publishing to ClawHub

When ready for marketplace:

1. Ensure `plugin.json` in `.claude-plugin/` at skill level
2. `cs-` prefix only needed for slug conflicts
3. Local folder/skill names stay unchanged
4. Rate limit: 5 skills/hour
5. No paid/commercial dependencies allowed

---

*Based on claude-skills agent development guide. Adapted for D:\AI-Workflows.*