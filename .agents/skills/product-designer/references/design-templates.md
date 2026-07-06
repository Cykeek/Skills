# Design Templates — Briefs, Critique, Research & Handoff

Ready-to-use templates for common product design artifacts. Adapt these to your team's needs, but keep the structure: good templates improve decision quality, not just documentation quality.

---

## 1. Design Brief Template

Use this to align stakeholders at the start of a design project. A good brief prevents scope creep, surfaces assumptions, and keeps everyone focused on the same problem.

```text
# Design Brief: [Project Name]

## Problem Statement
[1-2 sentences describing the user problem. What's broken or missing? Include evidence.]

## Decision to Make
[What choice should this design work help the team make?]

## Success Metrics
How will we know this design is working?
| Metric | Current Baseline | Target |
|---|---|---|
| [Metric 1] | [Value] | [Value] |
| [Metric 2] | [Value] | [Value] |

## User Progress / JTBD
When [situation],
I want to [motivation],
So I can [expected outcome].

## Target Users
- **Primary:** [Who's this for? What's their context / goal?]
- **Secondary:** [Other segments]
- **Out of scope:** [Who we're NOT designing for]

## Design Scope
**In scope:**
- [Screens, flows, or decisions this work covers]
- [States: empty, loading, error, edge cases]

**Out of scope / non-goals:**
- [Explicitly not part of this project]
- [What we are choosing not to optimize right now]

## Constraints & Considerations
- **Technical:** [Platform, performance, existing components]
- **Timeline / appetite:** [How much time this is worth]
- **Accessibility:** [WCAG level target]
- **Design system:** [Existing components to use or extend]
- **Business / policy:** [Any legal, pricing, compliance, or support constraints]

## Assumptions & Unknowns
- [What we believe but have not validated]
- [Riskiest assumptions]
- [What could change the direction entirely]

## Trust / Ethics Considerations
- [Sensitive data, consent, billing, destructive actions, vulnerable users, AI behavior]

## References
- [Competitive examples]
- [Previous research findings]
- [Related design work]
```

---

## 2. Design Critique Format

### Structured Critique (Group Session)

Use this for collaborative reviews. The goal is to improve the work, not judge the designer.

**Ground rules:**
- Everyone is critiquing the *design*, not the *designer*
- The designer frames the session and asks for the type of feedback they need
- Separate taste from evidence
- Default to "I wonder if..." over "You should..."

**Session structure:**

```text
1. **Context (designer speaks)**
   - What problem are we solving?
   - What decision does this work support?
   - Where is this in the user flow?
   - What stage is this design at? (early concept vs near-final)
   - What kind of feedback do I need? (strategy, flow, visual, trust, specific question)

2. **Walkthrough (designer demonstrates)**
   - Show the design and walk through the flow.

3. **Feedback round (participants speak)**
   - Start with what's working
   - Then: concerns, questions, suggestions
   - Tie feedback to goals, principles, or evidence

4. **Synthesis (designer closes)**
   - Summarize what you heard
   - Call out what you'll change, test, or ignore
```

### Principled Critique Rubric

Use this when you need critique with more rigor than personal reactions.

| Lens | Questions to ask |
|---|---|
| **Problem fit** | Are we solving the right problem, or polishing the wrong thing? |
| **User fit** | Does this match the user's context, job, and mental model? |
| **Flow / interaction** | Can the user understand what to do and recover if something goes wrong? |
| **Craft / hierarchy** | Does spacing, contrast, copy, and emphasis support the task? |
| **System fit** | Is this coherent with the broader product and design system? |
| **Trust / ethics** | Is anything manipulative, unclear, or difficult to reverse? |
| **Evidence** | What is observed, what is inferred, and what still needs validation? |

### The "I Like, I Wish, What If" Method

A gentle critique format that encourages constructive feedback.

| Prompt | What it's for |
|---|---|
| **I like...** | Surface strengths worth preserving |
| **I wish...** | Frame concerns as improvements, not failures |
| **What if...** | Explore alternatives without over-prescribing |

### Self-Critique Checklist

Before asking others to critique your work, run through this yourself:

```text
□ What problem is this solving?
□ What decision is this work meant to support?
□ Who is the user and what progress are they trying to make?
□ What is the primary action on this screen, and is it obvious?
□ Have I designed empty, loading, error, and recovery states?
□ Does the visual hierarchy match the user's priorities?
□ Is anything here decorative without helping understanding or trust?
□ Does this meet accessibility targets?
□ Is there anything I can remove without hurting the experience?
□ What part of this design is least certain and needs feedback or testing?
```

---

## 3. User Research Plan Template

```text
# Research Plan: [Project Name]

## Background
[Why are we doing this research? What context matters?]

## Decision to Inform
[What choice should the findings help us make?]

## Research Questions
1. [Primary question]
2. [Secondary question]
3. [Secondary question]

## Assumptions / Hypotheses
- [What we currently believe]
- [Riskiest assumption]
- [What result would change our direction]

## Methodology
- **Method:** [Interview / usability test / survey / field study / etc.]
- **Why this method:** [Why it is the minimum sufficient method for this question]
- **Format:** [Moderated / unmoderated / in-person / remote]
- **Duration:** [Minutes per session]
- **Total participants:** [Number]

## Participant Criteria
**Must have:**
- [Criteria 1]
- [Criteria 2]

**Nice to have:**
- [Criteria 3]

**Exclude:**
- [Who we don't want]

## Discussion Guide Topics
1. [Warm-up / context]
2. [Topic 1]
3. [Topic 2]
4. [Topic 3]
5. [Closing]

## Tasks (for usability or comprehension testing)
1. [Task 1 — scenario + success criteria]
2. [Task 2]
3. [Task 3]

## What Changes Based on the Findings?
- If we learn [A], we will [action A]
- If we learn [B], we will [action B]

## Analysis Plan
- How will we capture data?
- How will we synthesize it?
- How will we share findings?
- How will we rate confidence / evidence quality?

## Timeline
| Date | Activity |
|---|---|
| [Date] | Recruit participants |
| [Date] | Pilot session |
| [Date - Date] | Research sessions |
| [Date] | Analysis and readout |

## Ethics & Logistics
- Incentive: [$ per participant]
- Consent form: [Link]
- Recording: [Yes/No — how stored, when deleted]
```

---

## 4. JTBD / Job Story Worksheet

Use this when the real question is motivation, switching, adoption, or churn rather than interface mechanics alone.

```text
# JTBD Worksheet: [Feature / Product / Segment]

## Situation
When [what is happening in the user's world?]

## Motivation
I want to [what are they trying to make happen?]

## Expected Outcome
So I can [what better state are they trying to reach?]

## Functional Job
[Practical task]

## Emotional Job
[How they want to feel]

## Social Job
[How they want to be perceived]

## Forces of Progress
- **Push:** [What frustration made change possible]
- **Pull:** [What felt attractive about the new option]
- **Anxiety:** [What made them hesitate]
- **Habit:** [What kept the old behavior sticky]

## Current Alternatives / Workarounds
- [What they do today]
- [Competitors or manual solutions]
- [Doing nothing]

## Design Implications
- [Implication 1]
- [Implication 2]
- [Implication 3]
```

---

## 5. Usability Test Report Template

```text
# Usability Test Report: [Project Name]

## Executive Summary
[1-2 paragraph summary of what was tested, key findings, and recommendations]

## Decision Supported
[What choice this research informs]

## Method
- **Method:** Moderated / Unmoderated usability test
- **Participants:** [Number] target users
- **Duration:** [Minutes per session]
- **Date:** [Date range]

## Participant Overview
| # | Segment | Key characteristics |
|---|---|---|
| P1 | [Segment] | [Relevant context] |
| P2 | [Segment] | [Relevant context] |

## Key Findings
### Finding 1: [Title]
- **Evidence:** [Quote or observation]
- **Severity:** [Critical / High / Medium / Low]
- **Frequency:** [X of Y participants]
- **Recommendation:** [Suggested fix]

### Finding 2: [Title]
- **Evidence:** [Quote or observation]
- **Severity:** [Critical / High / Medium / Low]
- **Frequency:** [X of Y participants]
- **Recommendation:** [Suggested fix]

## Task Success Rates
| Task | Success Rate | Avg Time | Issues |
|---|---|---|---|
| [Task 1] | X% | [Time] | [Issues] |
| [Task 2] | X% | [Time] | [Issues] |

## Confidence Level
[High / Medium / Low — and why]

## Recommendations (Priority Order)
1. **[Fix]** — Severity: Critical — [Rationale]
2. **[Fix]** — Severity: High — [Rationale]
3. **[Fix]** — Severity: Medium — [Rationale]

## Appendix
- Discussion guide: [Link]
- Raw notes: [Link]
- Session recordings: [Link]
```

---

## 6. Scope Shaping / Thin Slice Worksheet

Use this when the problem is too broad, the concept is promising but fuzzy, or the team needs a smallest coherent version.

```text
# Scope Shaping Worksheet: [Initiative]

## Core Outcome
[What user or business outcome should improve?]

## Appetite
[How much time is this worth? e.g. 1 week, 2 weeks, 1 sprint, 6 weeks]

## Must Be True at the End
- [What absolutely must work for this to count as successful]

## Thin Slice
What is the smallest version that still delivers a coherent experience?
- [Minimum path / minimum flow / minimum states]

## Not Included in This Slice
- [Nice-to-haves, extensions, admin surfaces, secondary settings]

## Key Risks
- **User risk:** [Will users want or understand it?]
- **Scope risk:** [What might balloon?]
- **Trust risk:** [Any billing, consent, or irreversible behavior?]
- **Technical risk:** [Any constraints that threaten coherence?]

## Validation Plan
[How will we know this slice was enough?]
```

---

## 7. Design Specification / Handoff Template

Use for engineering handoff. The goal is to answer every question a developer might have before they have to ask.

```text
# Design Spec: [Feature / Component Name]

**Version:** [X.X]
**Last updated:** [Date]

## Overview
[Brief description of the feature and its user goal]

## Design Rationale
[Why this approach was chosen over alternatives]

## Open Questions / Assumptions
- [What is still uncertain]
- [What should be instrumented or watched after launch]

## Related Design System Components
- [Existing component] — [variant / usage]
- [Existing component] — [variant / usage]
- New component: [Name] — see specs below

## Screens / States
### Screen 1: [Screen name]
**User goal:** [What the user accomplishes here]

| State | Description | Reference |
|---|---|---|
| Default | [First view] | [Figma link] |
| Empty | [No data] | [Figma link] |
| Loading | [Placeholder / spinner] | [Figma link] |
| Error | [Failure state] | [Figma link] |
| Edge case | [Unusual state] | [Figma link] |

**Behavior notes:**
- [What happens on load]
- [What happens on each interaction]
- [Transitions / timing]
- [Keyboard shortcuts or key behavior]

## Interactive Specifications
| Element | State | Visual spec | Behavior |
|---|---|---|---|
| [Button] | Default | [Fill, text, radius] | — |
| [Button] | Hover | [Change] | Cursor: pointer |
| [Button] | Disabled | [Opacity / color] | No click handler |
| [Input] | Focus | [Border / shadow] | Tab key activates |

## Responsive Behavior
| Breakpoint | Layout changes |
|---|---|
| Desktop | [Layout] |
| Tablet | [Changes] |
| Mobile | [Stack / collapse / reorder] |

## Accessibility Notes
- [ARIA labels]
- [Tab order]
- [Focus indicator specs]
- [Screen reader expectations]

## Trust / Risk Notes
- [Consent or data-use disclosure]
- [Irreversible actions and safeguards]
- [Pricing or sensitive information cues]

## Dev Notes
- [Edge cases not handled by design]
- [Performance considerations]
- [Analytics events to track]
```

---

## 8. Trust & Ethics Review Checklist

Use this for consent flows, billing, destructive actions, AI surfaces, permissions, onboarding pressure, or any feature where the UI could mislead or overreach.

```text
# Trust & Ethics Review: [Flow / Feature]

## What is the experience asking the user to do?
[Summary]

## Risk Areas
□ Hidden cost or hidden consequence
□ Unequal visual weighting of choices
□ Misleading urgency or scarcity
□ Hard-to-reverse action
□ Data collection or sharing not clearly explained
□ AI behavior presented with too much certainty
□ Vulnerable or first-time users may be pressured

## Review Questions
1. Does the user understand what will happen next?
2. Is the important information visible before commitment?
3. Can the user say no without punishment or shame?
4. Can the user reverse or recover?
5. Are defaults fair and proportionate?
6. Would a reasonable first-time user describe this as honest?

## Findings
- [Issue 1] — [Risk] — [Suggested fix]
- [Issue 2] — [Risk] — [Suggested fix]

## Overall Risk Level
[Low / Medium / High]
```

---

## 9. Emotional Design / Tone Review Template

Use this when the product's tone, personality, or reassurance level matters to the experience.

```text
# Emotional Design Review: [Feature / Flow]

## Desired Feeling
[How should the user feel here? calm, confident, reassured, delighted, in control, etc.]

## Actual Feeling Today
[What the current design likely communicates]

## Critical Moments
- First use:
- Waiting:
- Error:
- Success:
- Sensitive action:

## Tone Review
| Moment | Current tone | Better tone |
|---|---|---|
| [Moment] | [Current] | [Target] |

## Personality Check
- Does personality support clarity?
- Does playfulness distract from seriousness where consequences matter?
- Does the product sound human without becoming vague?

## Recommendations
- [Change 1]
- [Change 2]
- [Change 3]
```

---

## 10. Accessibility Audit Template

```text
# Accessibility Audit: [Page / Feature / Product]

**Audit date:** [Date]
**WCAG target:** [Level A / AA / AAA]

## Automated Checks
Tool used: [axe / WAVE / Lighthouse / etc.]

| Issue | Location | WCAG criteria | Severity |
|---|---|---|---|
| [Issue] | [Element] | [SC 1.4.3] | [H / M / L] |

## Manual Checks
### Keyboard Navigation
| Check | Pass/Fail | Notes |
|---|---|---|
| All interactive elements reachable via tab | ✅ / ❌ | |
| Tab order follows visual order | ✅ / ❌ | |
| No keyboard traps | ✅ / ❌ | |
| Visible focus indicator on all elements | ✅ / ❌ | |

### Color & Contrast
| Check | Pass/Fail | Notes |
|---|---|---|
| Body text contrast ≥ 4.5:1 | ✅ / ❌ | |
| Large text contrast ≥ 3:1 | ✅ / ❌ | |
| UI component contrast ≥ 3:1 | ✅ / ❌ | |
| Color not sole indicator of meaning | ✅ / ❌ | |

### Screen Reader
| Check | Pass/Fail | Notes |
|---|---|---|
| All images have meaningful alt text | ✅ / ❌ | |
| Icon-only buttons have aria-labels | ✅ / ❌ | |
| Heading hierarchy is logical | ✅ / ❌ | |
| Form inputs have associated labels | ✅ / ❌ | |

## Summary
**Critical issues:** [Count]
**High issues:** [Count]
**Medium issues:** [Count]
**Low issues:** [Count]

## Priority Fixes
1. [Fix] — Critical — [Rationale]
2. [Fix] — High — [Rationale]
3. [Fix] — High — [Rationale]
```
