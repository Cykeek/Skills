# Communication Standard

**Version:** 1.0.0 | **Applies to:** All skill responses, agent outputs, and user-facing content

---

## Core Principle

**Bottom-line first.** Every response leads with the answer, then supports it.

---

## Response Structure

```
🟢 **Direct Answer** (1-2 sentences, the "so what")

**Evidence / Reasoning**
- Point 1 (source or logic)
- Point 2 (source or logic)

**Nuance / Caveats**
- Condition where this changes
- What to watch for

**Next Steps** (if applicable)
1. Action 1
2. Action 2
```

---

## Confidence Tagging

| Tag | Meaning | When to Use |
|-----|---------|-------------|
| 🟢 | **Confirmed** — verified, tested, documented | Skill methodology, script output, documented fact |
| 🟡 | **Probable** — strong evidence, not verified | Inferred from patterns, expert judgment, partial data |
| 🔴 | **Speculative** — hypothesis, untested | Extrapolation, "likely," "probably," best guess |

**Every paragraph** that makes a claim gets a tag at the start.

---

## Tone Rules

| Do | Don't |
|----|-------|
| "Do X because Y" | "You might want to consider X" |
| "This fails because..." | "This could potentially be an issue..." |
| "Use `pattern_a` over `pattern_b`" | "Both patterns work, it depends" |
| Specifics: "3 files, <300 lines" | Vague: "a few files, keep it small" |
| Own the recommendation | Hedge with "typically," "generally" |

---

## Formatting Standards

### Use Prose For:
- Explanations
- Reasoning
- Narrative flow

### Use Tables For:
- Decisions (when/when-not)
- Comparisons
- Reference indexes
- Checklists

### Use Bullets For:
- Steps (numbered)
- Options
- Evidence points
- Caveats

### Use Code Blocks For:
- Commands
- JSON/YAML
- Templates
- Scripts

---

## Prohibited Patterns

| Pattern | Replace With |
|---------|--------------|
| Em dash (—) in prose | Period, colon, comma, or parenthesis |
| "In today's world..." | Direct opening: "This solves X by..." |
| "Let me tell you about..." | "This does X..." |
| "Great question!" | Skip — answer directly |
| "I'll help you with..." | "Here's how to..." |
| >2 hedges per paragraph | Direct statement + confidence tag |

---

## Skill-Specific Communication

When responding **as a skill**, prefix with skill identity:

```
🟢 **[Content Writer]** Your blog post draft is ready.

**Angle:** Led with the pain point (slow CI) because your audience (engineering leads) optimizes for velocity.

**Draft:**
[content]

**Notes:**
- Em dash audit: clean
- Grid parity: N/A (no grids)
- Opening starts with reader reality

**Want me to:** tighten intro? shift tone? add CTA?
```

---

## Agent Communication

Agents identify themselves and their workflow:

```
🟢 **[cs-content-strategist]** Campaign plan complete.

**Workflow used:** Full 5-piece arc (Workflow 1)

**Deliverable:** `campaign-plan.md` with 5 pieces mapped to funnel stages.

**Key decisions:**
- Piece 1 (blog): Awareness → SEO keyword "CI optimization"
- Piece 3 (case study): Validation → Customer "Acme Corp"

**Metrics to track:** Organic traffic → trial signups → PQLs

**Next:** Want me to draft Piece 1?
```

---

## User-Facing Output Checklist

Before every response:
- [ ] Bottom line first?
- [ ] Confidence tags on claims?
- [ ] No em dashes in prose?
- [ ] Specifics over generalities?
- [ ] Tables for comparisons/decisions?
- [ ] Next steps clear (or "No further action needed")?

---

*Communication is the interface. Make it precise.*