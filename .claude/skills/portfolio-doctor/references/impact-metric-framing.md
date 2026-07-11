# Impact & Metric Framing — Deep Reference

This reference teaches how to translate design, product, and engineering work into credible, hiring-manager-ready metrics. Use when auditing case studies for impact evidence or coaching candidates to strengthen results sections.

---

## 1. The Metric Hierarchy

Not all metrics are equal. Hiring managers evaluate them in this order:

| Tier | Name | Examples | Credibility | When to Use |
|---|---|---|---|---|
| **1** | **Business Outcomes** | Revenue, ARR, Retention, Churn, CAC, LTV, Conversion Rate (trial→paid) | ★★★★★ | Always lead with at least one |
| **2** | **Product Outcomes** | Activation Rate, Feature Adoption, Time-to-Value, NPS, Task Success Rate | ★★★★☆ | When business metric is shared/indirect |
| **3** | **User Behavior** | Task Completion, Time-on-Task, Error Rate, Drop-off Points, Search Refinement | ★★★☆☆ | Support business/product metrics |
| **4** | **Process & Quality** | Cycle Time, Handoff Rework, Bug Regression, A11y Score, Design System Coverage | ★★☆☆☆ | Demonstrate craft & operational excellence |
| **5** | **Output / Vanity** | Screens Designed, Components Built, Figma Files, Hours Worked | ★☆☆☆☆ | Never use alone; only as context |

**Rule:** Every case study must have **≥1 Tier 1 or 2 metric**. Tier 3–4 are supporting evidence. Tier 5 is forbidden as primary impact.

---

## 2. Metric Framing Templates

### 2.1 The "Before → After → Attribution" Format

> **[Metric Name]**  
> **Before:** [Value] ([Timeframe], [Source])  
> **After:** [Value] ([Timeframe], [Source])  
> **Change:** [Absolute Δ] / [Relative %] [p-value / confidence if applicable]  
> **Attribution:** [Your specific contribution vs. other factors]  
> **Context:** [Cohort, segment, channel, device if relevant]

**Example:**
> **Enterprise Activation Rate (Trial → Paid)**  
> **Before:** 18% (Q2 2023, Mixpanel cohort n=2,400)  
> **After:** 27% (Q4 2023, Mixpanel cohort n=2,100)  
> **Change:** +9 pp / +50% relative (p < 0.01, χ²)  
> **Attribution:** Redesigned onboarding flow (my ownership) + pricing page copy change (marketing). Isolation test: flow variant held pricing constant → +6 pp.  
> **Context:** Enterprise segment only (>50 seats); SMB unchanged.

---

### 2.2 Proxy Metrics When Direct Business Data Is Unavailable

| Scenario | Proxy Metric | How to Frame |
|---|---|---|
| **Pre-launch / no analytics** | Usability task success rate | "Usability test (n=12): 92% task success vs. 41% baseline on current flow. Projected 15–20% activation lift per Nielsen Norman conversion model." |
| **NDA / confidential client** | Normalized index | "Client-reported 'onboarding efficiency index' improved 3.2× (internal survey, n=47). Absolute values redacted per NDA; methodology documented in case study appendix." |
| **Internal tool (no revenue)** | Time saved × headcount × loaded cost | "Automated reporting workflow: 22 hrs/mo saved × 8 analysts × $150/hr loaded = $316K annualized capacity recovery." |
| **Open source / community** | Adoption velocity | "v2.0 release: 1.2K stars in 30 days (vs 400 for v1.0), 47 contributors, 3 production adoptions confirmed via dependency graph." |
| **Design system** | Adoption coverage | "Component library covers 87% of product UI surface (up from 34%), reducing design→dev handoff cycles from 3.2 to 1.1 per feature." |

**Never invent numbers.** Always label: `Projected`, `Modeled`, `Proxy`, `Client-reported`, `Self-reported`.

---

### 2.3 Metric Translation Table (Design → Business)

| Design Action | Weak Metric | Strong Business Translation |
|---|---|---|
| Redesigned checkout | "Improved UX" | "Reduced checkout abandonment 23% (Baymard benchmark: avg 70% → our 54%), recovering ~$1.2M ARR annually" |
| Built design system | "Created 40 components" | "Design system v2 covers 87% of UI, cut feature design→dev cycle 40% (3.2 → 1.9 weeks), onboarded 12 engineers in 2 days vs 2 weeks" |
| Ran user research | "Interviewed 15 users" | "Identified 3 critical onboarding gaps causing 34% day-1 drop-off; fixes shipped in v3.1 → day-1 retention +12 pp" |
| Improved accessibility | "Fixed a11y issues" | "Achieved WCAG 2.2 AA (from 42 violations → 0), unlocked $400K government contract requiring VPAT, reduced support tickets 18%" |
| Prototyped new feature | "Made a prototype" | "Concept test (n=80): 78% preference vs. current; validated willingness-to-pay +$15/mo; greenlit for 6-engineer build" |
| Mentored designers | "Helped team grow" | "Mentored 3 mid-level → 2 promoted to senior in 18 mo; established critique cadence reducing design rework 30%" |

---

## 3. Handling Constraints & Gaps

### 3.1 The "No Metrics" Protocol

If a project genuinely has zero measurable outcomes (speculative, cancelled, pre-launch, pure research):

1. **Lead with the decision enabled:** "Research de-risked $2M build investment — leadership killed initiative after finding 0/12 users would pay."
2. **Show rigor:** "Mixed-method study: 12 JTBD interviews + 300 survey responses + competitive matrix. Synthesis framework adopted by PM org."
3. **Name the artifact:** "Delivered: Problem Brief (8 pages), Opportunity Sizing Model (Excel), 3 Concept Prototypes (Figma), Decision Memo (2 pages)."
4. **Reflect:** "Would have run painted-door test before prototyping — saves 3 weeks."

**Template for "No Launch" Projects:**
```markdown
## Impact (Pre-Launch / Cancelled / Research)

**Decision Enabled:** [What choice did this work inform?]
**Rigor:** [Methods, sample, synthesis approach]
**Artifacts Delivered:** [Concrete outputs]
**Counterfactual:** [What would have happened without this work?]
**Learning Applied:** [How this changed your subsequent work]
```

---

### 3.2 The "Team Project" Attribution Protocol

**Never:** "We launched X, resulting in Y."
**Always:** Decompose.

| Your Role | Attribution Language |
|---|---|
| **Solo / Lead Designer** | "I led design end-to-end: research, strategy, execution, handoff. Primary driver of [metric]." |
| **Co-Lead (2 designers)** | "Co-led with [Name]. I owned [specific scope: research / systems / mobile / 0→1]. Jointly responsible for [shared metric]." |
| **Contributor (feature area)** | "Owned [specific flow: onboarding / settings / dashboard] within [larger project]. My scope directly influenced [sub-metric]." |
| **Design System / Platform** | "Built [component/pattern] adopted by [N] teams across [M] products. Enabled [downstream metric]." |
| **Manager / Lead** | "Directed [N] designers on [project]. Set strategy, review cadence, hiring. Team delivered [metric]." |

**Attribution Statement (include in every case study):**
```markdown
## My Contribution

- **Scope Owned:** [Exact flows, screens, systems, research]
- **Decisions Made:** [Key trade-offs you authored]
- **Artifacts Produced:** [Figma files, specs, prototypes, docs — with links]
- **Collaboration:** [Pairings: PM, Eng, Research, Data, Marketing — what you drove vs. supported]
- **Metric Ownership:** [Which metrics you directly influenced vs. shared]
```

---

## 4. Quantitative Storytelling Patterns

### 4.1 The "Ladder of Proof"

Stack metrics from user → business:

```markdown
**User Level:** Task success 92% (vs 41% baseline) — Usability test n=12
    ↓ enables
**Behavior Level:** Onboarding completion 68% → 83% — Mixpanel cohort n=4,200
    ↓ enables
**Product Level:** Trial activation 18% → 27% — Same cohort
    ↓ enables
**Business Level:** Enterprise ARR retention +$460K/yr — Finance model
```

### 4.2 Cohort & Segment Discipline

Always specify:
- **Cohort definition:** "Users who started trial in Q3 2023"
- **Segment:** "Enterprise (>50 seats), North America, Desktop"
- **Timeframe:** "Measured 30 days post-trial-start"
- **Sample size:** "n=2,100"

**Bad:** "Conversion improved."
**Good:** "Enterprise trial→paid conversion (NA, Desktop, 30-day window) rose 18% → 27% (+9 pp, +50% rel, p<0.01), n=2,100, Q3 2023 cohort."

---

### 4.3 Statistical Honesty

| Situation | Required Disclosure |
|---|---|
| A/B test | "p-value: 0.03", "95% CI: [+4%, +14%]", "Power: 80% at 5% MDE" |
| Pre/post (no control) | "Pre/post comparison — no control group. Confounding: [seasonality, marketing spend, pricing change]" |
| Small sample (n<30) | "Small sample (n=12) — qualitative confidence only. Directional signal." |
| Survey | "n=300, ±5.6% margin of error at 95% CI. Self-selection bias likely." |
| Modeled/projected | "Projected using [model/assumptions]. Not yet observed in production." |

---

## 5. Metric Anti-Patterns & Rewrites

| Anti-Pattern | Why It Fails | Rewrite |
|---|---|---|
| "Improved UX" | Zero signal | "Reduced task completion time 42% (120s → 70s), n=15 usability test" |
| "Increased engagement" | Vanity, undefined | "Increased 7-day feature adoption 23% (12% → 14.8%), n=18K MAU" |
| "Designed 50+ screens" | Output, not outcome | "Delivered end-to-end checkout redesign (47 screens) → -23% abandonment, +$1.2M ARR" |
| "Positive user feedback" | Anecdotal, biased | "SUS score 82 (vs 58 baseline), n=40. NPS +34 (from -12)" |
| "Stakeholders loved it" | Political, not user | "PM/Eng/Research alignment: 0 scope changes post-handoff, 1.1 design→dev cycles avg" |
| "Best practices applied" | Generic | "Applied Baymard checkout heuristics: 17/19 violations fixed → -23% abandonment" |
| "Scalable design system" | Buzzword | "Design system v2: 87% UI coverage, 12 consuming teams, 40% faster feature delivery" |

---

## 6. Role-Specific Metric Expectations

| Role | Must-Have Metrics | Differentiating Metrics |
|---|---|---|
| **Product Designer (IC)** | Feature adoption, task success, usability scores | Activation lift, retention impact, experiment win rate |
| **Senior Product Designer** | Cross-feature journey metrics, system coverage | 0→1 validation, ambiguity resolution speed, org-wide pattern adoption |
| **Staff / Principal Designer** | Portfolio-level business impact, strategy-to-execution latency | Revenue influence, org capability building, industry leadership (talks, standards) |
| **Design Lead / Manager** | Team velocity, hiring/retention, career growth, quality bar | Design ops maturity, cross-func influence, budget efficiency, culture metrics |
| **Design Engineer** | Component adoption, bundle size, a11y score, dev satisfaction | Design token sync latency, Figma→code parity, innovation prototypes shipped |

---

## 7. Metric Audit Checklist (Agent Use)

When reviewing a case study's impact section, verify:

- [ ] **At least one Tier 1 or 2 metric** present and quantified
- [ ] **Before/After values** with timeframe and source
- [ ] **Attribution statement** decomposing your contribution
- [ ] **Cohort/segment context** specified
- [ ] **Statistical honesty** — no p-hacking, no causation claims without evidence
- [ ] **Proxy metrics labeled** as projected/modeled/client-reported
- [ ] **No Tier 5 metrics** standing alone as primary impact
- [ ] **Counterfactual considered** — "What if we didn't do this?"
- [ ] **Qualitative evidence** supports quantitative (quotes, session clips, survey verbatims)
- [ ] **Failed/negative results acknowledged** — shows intellectual honesty

---

## 8. Quick Reference: 20 High-Signal Metric Stems

Use these as starting points — always complete with Before/After/Attribution:

1. **Trial → Paid Conversion Rate** (by segment, channel, cohort)
2. **Activation Rate** (value moment achieved within [N] days)
3. **Feature Adoption Rate** (% of eligible users using [feature] weekly)
4. **Time-to-Value** (median days from signup to [core action])
5. **Task Success Rate** (usability test, % completing without help)
6. **Task Completion Time** (median, P90 — before/after)
7. **Error Rate** (user errors per session / per task)
8. **Support Ticket Volume** (for [feature/flow], % reduction)
9. **NPS / CSAT / SUS** (score, sample, confidence interval)
10. **Retention** (Day 1 / Day 7 / Day 30 / 90-day)
11. **Churn Rate** (logo / revenue / net revenue retention)
12. **Expansion Revenue** (upsell / cross-sell attributable to [feature])
13. **Design→Dev Cycle Time** (median days from handoff to merge)
14. **Handoff Rework Rate** (% of tickets returned to design)
15. **Design System Coverage** (% of product UI using system components)
16. **Accessibility Score** (axe violations: critical/high/medium/low)
17. **Research-to-Decision Latency** (days from insight to shipped decision)
18. **Experiment Velocity** (tests shipped / quarter, win rate)
19. **Onboarding Completion** (% reaching [milestone] in first session)
20. **Self-Serve Rate** (% of [task] completed without human support)