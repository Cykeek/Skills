# Role-Signal Mapping — Deep Reference

This reference maps target roles to the specific portfolio signals, case study emphasis, and narrative framing that hiring managers at top companies (FAANG, Series A–C, design-forward orgs) explicitly evaluate. Use when auditing a portfolio against a target role or coaching a candidate on role alignment.

---

## 1. Role × Signal Matrix

| Target Role | Must-Have Signals (2–3) | Differentiating Signals (1–2) | Case Study Emphasis | Anti-Signals (Avoid) |
|---|---|---|---|---|
| **Junior Product Designer (0–2)** | `User Research Rigor`, `Quality & Craft` | `Cross-functional Partnership` | Process fidelity, artifact quality, mentor receptivity | `Systems Thinking`, `Strategic Influence`, `0→1 Ambiguity` |
| **Mid Product Designer (3–5)** | `Data-Informed Design`, `Cross-functional Partnership` | `Systems Thinking`, `Conversion Optimization` | End-to-end ownership, metric movement, design system contribution | `Mentorship & Growth`, `Design Operations` |
| **Senior Product Designer (5–7)** | `Systems Thinking`, `0→1 Ambiguity`, `Cross-functional Leadership` | `Strategic Influence`, `Platform Design` | Problem discovery, strategic trade-offs, org-wide patterns, enabling others | `Quality & Craft` (as primary — assumed) |
| **Staff / Principal Designer (8+)** | `Systems Thinking`, `Strategic Influence`, `Platform Design` | `Innovation & R&D`, `Design Operations` | Portfolio-level impact, architecture decisions, capability building, industry voice | Any single-feature focus without system context |
| **Design Lead / Manager** | `Cross-functional Leadership`, `Mentorship & Growth`, `Design Operations` | `Strategic Influence`, `Design Systems` | Team outcomes, hiring/retention, process design, quality bar, budget/scope | `0→1 Ambiguity` (as primary — show you enable it in others) |
| **Design Engineer** | `Technical Partnership`, `Quality & Craft`, `Design Systems` | `Innovation & R&D`, `Platform Design` | Component architecture, token systems, Figma↔Code parity, performance, a11y | `User Research Rigor` (unless hybrid) |
| **Product Designer — Growth** | `Conversion Optimization`, `Data-Informed Design`, `Experimentation` | `Retention & Engagement`, `Strategic Influence` | Experiment velocity, win rate, funnel optimization, statistical rigor | `Systems Thinking` (unless growth platform) |
| **Product Designer — Platform/Infra** | `Systems Thinking`, `Platform Design`, `Technical Partnership` | `Design Operations`, `Innovation & R&D` | Internal developer experience, API design, component architecture, governance | `Conversion Optimization`, `Brand/Marketing` |

---

## 2. Signal Definitions & Evidence Standards

Each signal requires **specific, verifiable evidence** in the portfolio. Generic claims ("I do systems thinking") are insufficient.

### 2.1 Systems Thinking
**Definition:** Designing for coherence across surfaces, time, and scale. Seeing second- and third-order effects.
**Evidence Required:**
- Design system contribution with adoption metrics (coverage %, teams consuming, time saved)
- Cross-product pattern library or shared component architecture
- Platform-level case study (not a single feature)
- Explicit trade-off documentation: "Chose X over Y because it enables Z future capability"
- Information architecture work: taxonomy, navigation systems, data models

### 2.2 0→1 Ambiguity
**Definition:** Operating in high-uncertainty spaces — no clear problem, no clear solution, no clear user.
**Evidence Required:**
- Problem framing artifact: opportunity sizing, JTBD landscape, assumption map
- Multiple divergent concepts explored (not iterations of one idea)
- Validation methodology: painted door, Wizard of Oz, concierge, fake door, smoke test
- Kill criteria defined *before* build: "We stop if <20% say they'd pay $X"
- Pivot narrative: "Discovered X, abandoned Y, redirected to Z"
- Stakeholder alignment in ambiguity: decision memos, executive briefings

### 2.3 Cross-functional Leadership
**Definition:** Driving alignment and decisions across PM, Eng, Research, Data, Marketing, Sales, Legal.
**Evidence Required:**
- Specific collaborators named with roles: "Partnered with Sarah (PM), Miguel (Tech Lead), Priya (Research)"
- Decision-making artifacts: RFCs, design reviews, trade-off docs, consensus records
- Conflict resolution: "Engineering pushed back on timeline; we co-designed phased rollout saving 3 weeks"
- Enabling others: "Created design brief template adopted by 5 PMs", "Ran sketching workshop for 12 engineers"
- Metric co-ownership: "Shared OKR with PM: activation +15%"

### 2.4 Strategic Influence
**Definition:** Shaping product/design strategy beyond your immediate scope. Changing how the org thinks.
**Evidence Required:**
- Strategy documents authored: "Wrote 6-quarter design strategy for Platform group"
- Executive presentations: "Presented to VP Eng + CPO — secured 3-headcount investment"
- Org-wide initiatives: "Led design system adoption across 12 teams", "Defined design quality rubric for perf reviews"
- External influence: Conference talks, published articles, open-source contributions adopted externally
- Mentorship at scale: "Mentored 8 designers across 3 teams; 3 promoted in 18 months"

### 2.5 Platform Design
**Definition:** Designing primitives, APIs, and foundations that other teams build upon.
**Evidence Required:**
- Component/token architecture diagrams
- Consumer (internal team) feedback loops: RFC process, office hours, migration support
- Governance model: versioning, deprecation, breaking change policy
- Adoption metrics: "12 teams, 87% coverage, 0 breaking changes in 18 months"
- Developer experience artifacts: Storybook, playground, migration codemods, TypeScript types

### 2.6 User Research Rigor
**Definition:** Systematic, ethical, actionable user understanding — not just "talking to users."
**Evidence Required:**
- Research plan: questions, hypotheses, methods, sample criteria, recruiting screener
- Synthesis framework: thematic analysis, affinity mapping, JTBD forces, opportunity solution tree
- Artifacts: insight reports, journey maps, service blueprints, persona updates (with expiration dates)
- Decision traceability: "Insight X → Decision Y → Metric Z"
- Continuous discovery: "Weekly 1-hour interviews, 52 weeks/year, insights logged in Dovetail"

### 2.7 Data-Informed Design
**Definition:** Using quantitative evidence to frame problems, prioritize, and validate — not just "checking analytics."
**Evidence Required:**
- Funnel analysis with segment breakdowns: "Enterprise mobile drop-off at step 3: 42% vs 18% desktop"
- Experiment design: hypothesis, primary/guardrail metrics, sample size calc, p-value threshold
- Dashboard ownership: "Built Mixpanel board tracking activation → retention cohort curves"
- Counter-metric awareness: "Conversion +12% but support tickets +30% — investigated, found false affordance"

### 2.8 Conversion Optimization
**Definition:** Systematic improvement of business-critical funnels through experimentation.
**Evidence Required:**
- Experiment log: 5+ tests with hypothesis, variant screenshots, results, learnings
- Statistical literacy: "p=0.03, 95% CI [+4%, +18%], powered at 80% for 5% MDE"
- Baymard/heuristic audit baseline: "Fixed 17/19 checkout violations → -23% abandonment"
- Segmentation: "Mobile +18%, Desktop +8%, Tablet flat — responsive fix prioritized"

### 2.9 Retention & Engagement
**Definition:** Designing for long-term value, habit formation, and churn prevention.
**Evidence Required:**
- Cohort curves: "D30 retention 42% → 51% after onboarding redesign"
- Feature adoption depth: "Power user threshold: 3+ reports/week → 34% of active users"
- Churn signal detection: "Built 'at-risk' dashboard — enabled CSM intervention saving 12 accounts/Q"
- Lifecycle design: "Empty states, progressive disclosure, re-engagement flows — all instrumented"

### 2.10 Quality & Craft
**Definition:** Pixel-perfect execution, motion polish, micro-interactions, accessibility baseline — the "it feels right" layer.
**Evidence Required:**
- Motion specs: easing, duration, choreography — implemented, not just designed
- Dark mode: full semantic token coverage, not color inversion
- Responsive: 4+ breakpoints tested, no horizontal scroll at 320px
- Accessibility: axe 0 violations, keyboard flow documented, screen-reader tested
- Design↔Code parity: "Storybook stories for every variant; visual regression testing in CI"

### 2.11 Accessibility Champion
**Definition:** Proactive inclusive design — not retroactive compliance.
**Evidence Required:**
- Inclusive design process: "Co-designed with 3 screen-reader users from discovery"
- VPAT/ACR authorship: "Authored WCAG 2.2 AA conformance report for FedRAMP audit"
- Training: "Ran a11y workshop for 40 engineers; reduced violations 60% in 2 sprints"
- Innovation: "Built accessible data viz pattern library (ARIA + sonification)"

### 2.12 Design Operations
**Definition:** Scaling design capacity through tools, processes, and governance.
**Evidence Required:**
- Tooling: "Built Figma plugin auto-generating redlines — saved 5 hrs/week/designer"
- Process: "Redesigned design review cadence — cut meeting time 40%, improved decision clarity"
- Hiring/Onboarding: "Created design interview rubric + onboarding curriculum — 3 hires, 100% pass rate"
- Budget/Vendor: "Negotiated Figma Enterprise — $40K savings, added branching/history"

---

## 3. Case Study Signal Mapping

For each case study in the portfolio, explicitly tag **which signals it proves**. This creates the mapping hiring managers mentally perform.

### 3.1 Tagging Template (add to case study frontmatter)

```yaml
signalsProven:
  - primary: "Systems Thinking"
    evidence: "Design system v2 token architecture — 12 teams, 87% coverage, 0 breaking changes"
  - primary: "Cross-functional Leadership"
    evidence: "Co-led with PM/Eng; authored RFC; phased rollout plan"
  - secondary: "Data-Informed Design"
    evidence: "Funnel analysis drove scope; A/B test validated (p=0.02)"
  - secondary: "Quality & Craft"
    evidence: "Dark mode, motion specs, a11y audit — all shipped"
```

### 3.2 Required Signal Coverage by Role Target

| Role | Minimum Distinct Signals Across Portfolio | Primary Signals per Case Study |
|---|---|---|
| Junior | 3 | 1–2 |
| Mid | 4 | 2 |
| Senior | 5 | 2–3 |
| Staff/Principal | 6 | 3 |
| Lead/Manager | 5 (incl. Leadership) | 2–3 (1 must be Leadership) |

**Rule:** No single signal should carry the entire portfolio. Breadth + depth.

---

## 4. Narrative Framing by Role

The *same project* can be framed differently for different target roles. The portfolio must match the **target role narrative**, not just the historical role.

### 4.1 Same Project, Three Framings

**Project:** Redesigned enterprise billing dashboard.

| Target Role | Hero Tagline | Case Study Lead | Signals Highlighted |
|---|---|---|---|
| **Senior Product Designer** | "Cut billing investigation 45min → 4min, retaining $460K ARR" | Problem → Research → Decision → Impact | `Systems Thinking`, `0→1 Ambiguity`, `Cross-functional Leadership` |
| **Design Lead** | "Led 3 designers + 2 eng on billing platform — established review cadence, hired 1" | Team outcomes, process, hiring, quality bar | `Cross-functional Leadership`, `Mentorship & Growth`, `Design Operations` |
| **Staff Designer** | "Architected billing platform design system — 12 teams, 0 breaking changes in 18mo" | Architecture, governance, adoption, enablement | `Platform Design`, `Systems Thinking`, `Strategic Influence` |

### 4.2 Role-Specific Portfolio Curation

| Role | Projects to Lead With | Projects to Minimize/Reframe |
|---|---|---|
| **Senior IC** | 0→1, complex systems, metric-moving features | Pure production work, marketing pages, static brand |
| **Lead/Manager** | Team initiatives, process design, hiring, design system rollout | Solo IC deep-dives (keep 1 for craft cred) |
| **Staff/Principal** | Platform, architecture, org capability, external influence | Feature-level work (reframe as "enabled by platform") |
| **Growth** | Experiment logs, funnel optimization, retention loops | Brand, research-heavy without metric tie |
| **Platform** | Internal tools, component library, API design, DX | Consumer-facing marketing/landing pages |

---

## 5. Company-Stage Calibration

Signals weight differently by company stage. Adjust portfolio emphasis.

| Stage | Prioritized Signals | De-Prioritized |
|---|---|---|
| **Pre-Seed / Seed (0–20)** | `0→1 Ambiguity`, `Cross-functional Partnership`, `Speed to Ship`, `Quality & Craft` | `Design Operations`, `Platform Design`, `Strategic Influence` |
| **Series A–B (20–200)** | `Data-Informed Design`, `Systems Thinking`, `Conversion Optimization`, `User Research Rigor` | `Design Operations` (early), `Innovation & R&D` |
| **Series C–D / Pre-IPO (200–1000)** | `Systems Thinking`, `Platform Design`, `Design Operations`, `Strategic Influence`, `Mentorship & Growth` | `0→1 Ambiguity` (unless new product line) |
| **Public / Enterprise (1000+)** | `Platform Design`, `Design Operations`, `Accessibility Champion`, `Strategic Influence`, `Innovation & R&D` | `Speed to Ship` (alone), `Conversion Optimization` (unless growth org) |
| **Agency / Consulting** | `Cross-functional Partnership`, `User Research Rigor`, `Quality & Craft`, `Strategic Influence` | `Platform Design`, `Design Operations` (internal) |

---

## 6. Role-Signal Audit Checklist (Agent Use)

When reviewing a portfolio against a target role:

- [ ] **Target role explicitly stated** on home page hero and `/about`.
- [ ] **Minimum distinct signals** met per Section 3.2.
- [ ] **Each case study tagged** with `signalsProven` + evidence per Section 3.1.
- [ ] **Lead projects** (top 3) map to role's prioritized signals per Section 1.
- [ ] **No anti-signals** featured prominently per Section 1.
- [ ] **Narrative framing** matches target role per Section 4 (not historical role).
- [ ] **Company-stage calibration** applied per Section 5.
- [ ] **Signal evidence is specific** — no generic claims ("I do systems thinking" → "Design system v2: 12 teams, 87% coverage").
- [ ] **Leadership/Manager portfolios** include team outcomes, not just personal IC work.
- [ ] **Staff+ portfolios** show architecture/governance artifacts, not just screens.

---

## 7. Quick Reference: Signal → Hiring Manager Question

| Signal | What the Hiring Manager Is Asking |
|---|---|
| `Systems Thinking` | "Can this person design something that lasts and scales beyond their immediate feature?" |
| `0→1 Ambiguity` | "Can they operate when nobody knows the answer — including me?" |
| `Cross-functional Leadership` | "Will they drive alignment or wait for tickets?" |
| `Strategic Influence` | "Can they change how the org thinks, not just what it ships?" |
| `Platform Design` | "Can they build foundations others rely on — without becoming a bottleneck?" |
| `User Research Rigor` | "Do they validate or assume?" |
| `Data-Informed Design` | "Do they use data to decide, or to decorate decisions already made?" |
| `Conversion Optimization` | "Can they move the needle on revenue?" |
| `Retention & Engagement` | "Do they design for the long game?" |
| `Quality & Craft` | "Is the bar high even when nobody's watching?" |
| `Accessibility Champion` | "Is inclusion baked in or bolted on?" |
| `Design Operations` | "Can they scale the team's capacity, not just their own output?" |
| `Mentorship & Growth` | "Do they make others better?" |
| `Technical Partnership` | "Do engineers trust them?" |
| `Innovation & R&D` | "Are they pushing the boundary of what's possible?" |

---

## 8. Anti-Pattern: The "Everything Portfolio"

**Symptom:** 15 projects, each tagged with 6 signals, no clear lead, junior and senior work mixed equally.

**Diagnosis:** Candidate doesn't know their own level or target.

**Prescription:**
1. Delete or archive bottom 50% of projects.
2. Pick **one target role** (max two adjacent).
3. Reframe remaining 5–7 projects for that role using Section 4.
4. Lead with 3 projects that *perfectly* match the role's top signals.
5. Add explicit "Target Role" declaration on home page.