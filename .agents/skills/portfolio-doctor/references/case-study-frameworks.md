# Case Study Frameworks — Deep Reference

This reference defines the structural anatomy of a high-signal portfolio case study. Use when auditing, rewriting, or creating case studies.

---

## 1. The 7-Section Canonical Structure

Every case study targeting senior IC, lead, or manager roles **must** contain all seven sections. Missing sections = incomplete narrative.

| Section | Purpose | Minimum Content | Senior/Lead Differentiator |
|---|---|---|---|
| **1. Problem & Opportunity** | Frame the "why" | User/business problem, trigger, stakes, north-star metric | Systems view: second-order effects, org constraints |
| **2. Research & Discovery** | Prove user-centeredness | 3–5 insights with evidence type (qual/quant) | Research strategy: methods chosen, biases mitigated, synthesis framework |
| **3. Exploration & Alternatives** | Show design thinking breadth | 2–3 distinct directions + rejection rationale | Decision matrix: criteria, weights, trade-off transparency |
| **4. Design Decisions & Trade-offs** | Demonstrate judgment | 3–5 key decisions with explicit alternatives considered | Risk mitigation, scalability, platform implications |
| **5. Execution & Craft** | Prove delivery capability | Artifacts delivered, fidelity, system contributions, handoff quality | Design system governance, token architecture, cross-platform consistency |
| **6. Impact & Results** | Prove outcome orientation | Primary + 2–3 secondary metrics with source/timeframe | Leading vs lagging indicators, cohort analysis, longitudinal view |
| **7. Reflection** | Show growth mindset | What surprised you, what you'd change, practice evolution | Teaching moment: how this changed your process/mental models |

---

## 2. Section Deep-Dives

### 2.1 Problem & Opportunity — The Hook

**Formula:** `[User Pain] + [Business Consequence] + [Why Now] + [North Star Metric]`

**Template:**
> **[User segment]** struggled to **[core job]** because **[root cause]**. This resulted in **[business impact: churn, revenue loss, support cost, adoption failure]**. With **[trigger: new regulation, competitor launch, platform shift, strategic pivot]**, we needed to **[desired outcome]** — measured by **[north star metric]**.

**Weak:** "We redesigned the dashboard."
**Strong:** "Enterprise admins couldn't diagnose billing anomalies across 50+ accounts — each investigation took 45+ minutes via SQL. This caused 23% monthly churn in the $2M ARR segment. With the Q3 pricing model launch, we needed to cut investigation time to <5 minutes, measured by median time-to-resolution."

**Tagline for Project Card:** "Cut billing investigation time 45min → 4min for enterprise admins, retaining $460K ARR."

---

### 2.2 Research & Discovery — Evidence Over Opinion

**Insight Card Format (repeat 3–5×):**

```markdown
- **Insight:** [One crisp finding]
- **Evidence:** [Method + sample + artifact reference]
- **Implication:** [How this shaped design direction]
```

**Evidence Hierarchy (strongest → weakest):**
1. Direct user observation (usability test, field study) — *quote + timestamp*
2. Behavioral analytics (funnel drop-off, heatmap, path analysis) — *screenshot + query*
3. Support/sales feedback (tagged tickets, Gong calls) — *volume + verbatim*
4. Stakeholder interviews — *attributed quote*
5. Competitive audit — *comparison matrix*
6. Heuristic/expert review — *annotated screenshots*

**Red Flags:**
- "Users told us they wanted X" (no method, no sample, no verbatim)
- "Research showed..." (passive voice, no ownership)
- Zero quantitative backup for a claimed "major pain point"

---

### 2.3 Exploration & Alternatives — The Rejection Portfolio

**Required:** Show at least **two distinct directions** that were genuinely explored and rejected.

**Direction Card Format:**

```markdown
### Direction [A/B/C]: [Name]
**Concept:** [1-sentence summary]
**Key Screens/Flows:** [Links or embedded thumbnails]
**Why It Failed:**
- [Criterion 1]: [Evidence or reasoning]
- [Criterion 2]: [Evidence or reasoning]
**What We Salvaged:** [Pattern, component, or insight carried forward]
```

**Decision Matrix (for Lead+ roles):**

| Criterion | Weight | Dir A | Dir B | Dir C |
|---|---|---|---|---|
| Solves core user problem | 30% | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Engineering feasibility (6 wk) | 25% | ⭐⭐ | ⭐⭐⭐ | ⭐ |
| Design system alignment | 15% | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| Scalability to 10x users | 15% | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Accessibility compliance | 15% | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

### 2.4 Design Decisions & Trade-offs — Judgment Under Constraints

**Decision Card Format:**

```markdown
| Decision | Alternative Considered | Why This Won | Risk Mitigated |
|---|---|---|---|
| Single-page checkout with progressive disclosure | Multi-step wizard (current) | Baymard: 18% lower abandonment; matches mobile mental model | Added inline validation + save-for-later + error recovery |
| Custom select component vs native `<select>` | Native select (accessible by default) | Needed search + multi-select + grouped options; native lacks search | Built on top of `<select>` with ARIA combobox pattern; full keyboard support |
```

**Senior Signal:** Every decision names the **constraint** (timeline, tech debt, platform, regulatory) and the **mitigation** for the downside.

---

### 2.5 Execution & Craft — Delivery Evidence

**Artifact Inventory (be specific):**

| Artifact Type | Count / Scope | Fidelity | Tool | Handoff Notes |
|---|---|---|---|---|
| High-fidelity screens | 47 across 4 breakpoints | Pixel-perfect | Figma | Auto-layout, component variants, dev mode ready |
| Interactive prototype | 3 flows, 12 screens | Clickable + conditional logic | Figma | Shared with PM/Eng for usability test n=8 |
| Design system contributions | 12 new components, 8 updated | Production-ready | Figma + Storybook | Tokens synced via Style Dictionary; a11y audit passed |
| Accessibility annotations | All interactive states | WCAG 2.2 AA | Figma plugin | Focus order, ARIA labels, color contrast, motion reduction |
| Developer handoff package | 1 spec doc + token export | Implementation-ready | Zeroheight / Notion | Responsive behavior, loading/error/empty states, edge cases |

**Lead/Manager Addition:** Process artifacts — design critique cadence, decision log, retrospective notes, onboarding docs for new designers.

---

### 2.6 Impact & Results — The Receipts

**Metric Card Format:**

```markdown
### Primary Metric: [North Star Name]
**Before:** [Value + timeframe + source]
**After:** [Value + timeframe + source]
**Change:** [Absolute + Relative %, statistical significance if applicable]
**Attribution:** [How much of this change is credibly yours vs. other factors]
**Cohort/Context:** [Segment, channel, device, geography if relevant]
```

**Metric Categories to Cover:**
- **Business:** Revenue, ARR, conversion, retention, LTV, CAC payback
- **Product:** Activation, adoption, feature usage, time-to-value, NPS
- **User:** Task success rate, time-on-task, error rate, satisfaction (SEQ/SUS)
- **Engineering/Quality:** Bug regression, build time, bundle size, a11y score
- **Process:** Cycle time, design→dev handoff rework, research-to-decision latency

**When Exact Numbers Are Unavailable (NDA, pre-launch, no analytics):**
> "Projected 15–20% reduction in onboarding drop-off based on usability test (n=12, 83% task success vs 41% baseline). Validated with PM/Analytics — tracking plan approved for launch."

**Never:** "Improved user experience." "Increased engagement." "Positive feedback."

---

### 2.7 Reflection — The Growth Signal

**Required Prompts (answer 2–3):**

```markdown
## Reflection

**What surprised me most:** [Counter-intuitive finding or constraint discovery]

**If I had 2 more weeks:** [Specific scope, not "polish"]

**How this changed my practice:** [New method, mental model, or tool adopted]

**Advice to my past self at project start:** [Tactical, specific]

**What I'd do differently in a different context:** [Enterprise vs consumer, B2B vs B2C, regulated vs unregulated]
```

**Weak:** "I learned a lot about stakeholders."
**Strong:** "Discovered that legal review cycles add 3 weeks non-negotiably. Now I involve legal at problem-framing stage, not handoff — saves 2 weeks per cycle."

---

## 3. Role-Level Calibration

| Element | Junior (0–2) | Mid (3–5) | Senior (5–7) | Staff/Principal (8+) | Lead/Manager |
|---|---|---|---|---|---|
| **Problem Framing** | Given | Refined | Discovered | Defined strategy | Org-level portfolio |
| **Research** | Executes plan | Designs + executes | Chooses method, synthesizes | Builds research ops | Funds & prioritizes |
| **Exploration** | 1–2 directions | 2–3 directions | 3+ with decision matrix | Frames option space | Sets evaluation criteria |
| **Decisions** | Documents | Explains trade-offs | Makes & mitigates | Sets principles | Governs system |
| **Execution** | Produces screens | End-to-end flows | System contributions | Architecture + tokens | Team standards |
| **Impact** | Output metrics | Outcome metrics | Business metrics | Portfolio metrics | Org metrics |
| **Reflection** | Personal | Team | Cross-functional | Industry | Organizational |

---

## 4. Common Anti-Patterns & Fixes

| Anti-Pattern | Diagnosis | Fix |
|---|---|---|
| **The Gallery** — 20 screens, no words | No narrative, no evidence | Rewrite to 7-section template; keep 5–7 key screens max |
| **The Diary** — "First I did X, then Y" | Process log, not design rationale | Restructure: Problem → Insight → Decision → Result |
| **The "We" Fog** — Collective ownership only | Contribution invisible | Add explicit "My Contribution" section + ownership tags |
| **The Metric Vacuum** — Zero numbers | Impact unproven | Add proxy metrics, qualitative evidence, or projected ranges |
| **The Cliffhanger** — Ends at hi-fi screens | No execution/impact proof | Add Execution & Impact sections even if post-launch data pending |
| **The Jargon Salad** — Buzzwords without substance | Signal without substance | Replace each buzzword with a concrete artifact or decision |
| **The Orphan Project** — No link to role target | Reviewer can't map to competency | Tag project with 2–3 role signals; lead with strongest match |
| **The Static PDF** — Unsearchable, unlinkable | Recruiter friction | Build web version; PDF as supplement only |

---

## 5. Project Card Micro-Format (For Index/Grid Views)

Every project in the portfolio index must display:

```markdown
## [Project Title]
**One-Line Impact:** [Metric + outcome in ≤ 12 words]
**Role:** [Exact title] | **Duration:** [Months] | **Team:** [Size]
**Signals:** `[Tag 1]` `[Tag 2]` `[Tag 3]`  ← Maps to target role competencies
**Stack:** [Figma, React, SQL, etc. — only if relevant to role]
**Link:** [Deep link to case study]
```

**Example:**
> **Unified Billing Dashboard**
> **One-Line Impact:** Cut enterprise billing investigation 45min → 4min, retaining $460K ARR
> **Role:** Senior Product Designer (Lead) | **Duration:** 6 months | **Team:** 3D, 2E, 1PM, 1Research
> **Signals:** `[Systems Thinking]` `[0→1 Ambiguity]` `[Cross-functional Leadership]`
> **Stack:** Figma, Storybook, React, BigQuery, Mixpanel
> **Link:** `/work/unified-billing-dashboard`

---

## 6. Case Study Length Guidelines

| Role Target | Total Words | Screens/Artifacts | Time to Read |
|---|---|---|---|
| Junior / Mid | 800–1,500 | 5–8 | 3–5 min |
| Senior | 1,500–2,500 | 8–12 | 5–8 min |
| Staff / Principal | 2,500–4,000 | 10–15 | 8–12 min |
| Lead / Manager | 2,000–3,500 + process artifacts | 8–12 + process docs | 7–10 min |

> **Rule:** If a hiring manager cannot extract the problem, your role, the approach, and the result in **90 seconds**, the case study fails the scan test.