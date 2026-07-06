# UX Research — Methods, Testing & Synthesis

A practical guide to understanding users through research — from framing the decision and choosing the right method to synthesizing findings into actionable design decisions.

---

## 1. The Research Process

Good research follows a repeatable process:

```
Define → Choose Method → Plan → Conduct → Analyze → Share → Act
  │          │           │        │         │        │       │
  ↓          ↓           ↓        ↓         ↓        ↓       ↓
Decision   Which      Recruit,  Collect  Synthesize  Report  Design
or risk?   method?    schedule   data    findings   insights decisions
```

**Key principle:** Start with the question, *then* choose the method. Never pick a method and try to force a question into it.

### Frame the Decision Before the Study

Before you plan any research, answer these questions:

| Question | Why it matters |
|---|---|
| **What decision will this research support?** | Research is only useful if it changes a product, design, or business decision. |
| **What is unknown right now?** | Name the uncertainty clearly: behavior, motivation, comprehension, preference, or prevalence. |
| **What evidence already exists?** | Look at analytics, support tickets, prior studies, sales calls, reviews, or logs before running new work. |
| **What is the riskiest assumption?** | Test the most dangerous unknown first, not the easiest one. |
| **What would change based on the answer?** | If no action changes, the research may be unnecessary or too vague. |
| **What level of confidence do we need?** | A directional decision needs less rigor than a big bet affecting revenue, trust, or compliance. |

### Types of Unknowns

| Unknown type | Example | Best methods |
|---|---|---|
| **Behavioral** | What do users actually do in context? | Field study, diary study, analytics, session replay |
| **Attitudinal** | What do users think or feel? | Interviews, surveys |
| **Evaluative** | Can users use or understand this design? | Usability testing, comprehension testing |
| **Causal** | Did change X cause outcome Y? | A/B test, controlled experiment |
| **Strategic** | Are we solving the right problem for the right segment? | Discovery interviews, JTBD interviews, mixed methods |

### Minimum Useful Research Prompt

If you are unsure where to start, frame the work like this:

```text
We need to decide [decision].
We currently assume [assumption].
We need to learn [question].
If we learn [answer A], we will [action A].
If we learn [answer B], we will [action B].
```

---

## 2. When to Use Which Research Method

### By Product Stage

| Stage | Goal | Recommended methods |
|---|---|---|
| **Discovery** | Understand user needs, find opportunities | Field studies, diary studies, 1:1 interviews, JTBD interviews, competitive analysis |
| **Definition** | Frame the problem, validate assumptions | Contextual inquiry, surveys, card sorting, assumption mapping |
| **Development** | Test concepts, iterate on design | Usability testing, prototype testing, first-click testing, comprehension testing |
| **Delivery** | Validate before ship, catch issues | Usability testing, accessibility audit, trust/comprehension check |
| **Live** | Monitor, measure, improve | Analytics, surveys (NPS/CSAT), log analysis, A/B testing, churn interviews |

### By Decision Type

| Decision | Best method |
|---|---|
| **What problem should we solve?** | Discovery interviews, JTBD interviews, field study |
| **Why are users stuck, switching, or churning?** | JTBD interviews, support review, analytics, diary study |
| **Can users understand this?** | Comprehension test, moderated usability test |
| **Can users complete this task?** | Usability testing |
| **Which of these options is stronger?** | Preference test, first-click test, A/B test |
| **How should content or navigation be organized?** | Card sort, tree test |
| **Do users trust this flow?** | Trust interview, comprehension test, consent review |
| **How common is this behavior or opinion?** | Survey, analytics |

### By Question Type

| Question | Best method |
|---|---|
| **What do users actually do?** (not what they say) | Field study, diary study, analytics |
| **Why do users do that?** | 1:1 interview, contextual inquiry, JTBD interview |
| **Can users complete this task?** | Moderated usability testing |
| **Which design is better?** | A/B test, preference test, first-click test |
| **How should I organize this?** | Card sort, tree test |
| **How do users feel?** | Survey, interview |
| **Do they understand what they're agreeing to?** | Comprehension test, trust interview |
| **Is this accessible?** | Accessibility audit, screen reader testing |

### Qualitative vs Quantitative

| | Qualitative | Quantitative |
|---|---|---|
| **Question** | Why? How? | How many? How often? |
| **Sample** | Small (5-20) | Large (100+) |
| **Output** | Themes, quotes, observations | Numbers, statistics, charts |
| **Strength** | Depth of understanding | Breadth and generalizability |
| **Best for** | Discovery, understanding, hypothesis generation | Validation, benchmarking, measurement |
| **Risk** | Observer bias, can't generalize | Missing context, survey bias |

**Best practice:** Use both when the decision is important. Qualitative work tells you *why* something is happening; quantitative work tells you *how much it matters*.

---

## 3. User Interviews

### Types of Interviews

| Type | Description | When to use |
|---|---|---|
| **Structured** | Fixed script, same questions every time | Multi-user comparative research |
| **Semi-structured** | Guide with flexible follow-ups (most common) | Most product research |
| **Unstructured** | Conversational, no fixed script | Discovery, early exploration |
| **Contextual inquiry** | Interview + observation in user's environment | Complex workflows, B2B products |
| **JTBD / switch interview** | Reconstruct the moment a user adopted, rejected, or switched tools | Adoption, churn, motivation, market understanding |

### Interview Best Practices

**Before the interview:**
- Define 3-5 research questions you need to answer
- Write a discussion guide (not a script — topics to cover, not exact wording)
- Recruit people who match your target user profile, not friends/family
- Pilot test your guide with a colleague
- Be explicit about the decision this interview will support

**During the interview:**
- **Ask about specific past events** ("Tell me about the last time you did X") instead of hypotheticals ("What would you do if...")
- **Use the "5 Whys"** — when a user gives an answer, ask "why?" at least 3-5 times to get to the root motivation
- **Listen > talk** — aim for 80% user talking, 20% you asking
- **Don't lead** — avoid "Would you prefer X?" Ask "Tell me about your experience" instead
- **Watch for "that's nice" vs "I need this"** — polite enthusiasm isn't validation. Look for specific past struggles.
- **Capture verbatim quotes** — they're the richest output
- **Separate signal from suggestion** — users are great at describing problems, less reliable at inventing solutions

**After the interview:**
- Debrief immediately — capture impressions while fresh
- Transcribe or take structured notes
- Pull out 3-5 key observations per session
- Note what was observed vs what is inferred

### JTBD / Switch Interviewing

Use this format when you need to understand why someone adopted, rejected, or abandoned a product.

#### The job story frame

```text
When [situation],
I want to [motivation],
So I can [expected outcome].
```

#### What to listen for

| Signal | What it reveals |
|---|---|
| **Push** | What frustration or unmet need made the user open to change |
| **Pull** | What looked attractive about the new solution |
| **Anxiety** | What almost stopped them from switching |
| **Habit / inertia** | What kept them in the old behavior |
| **Workarounds** | What they used before your product, including doing nothing |
| **Progress** | What better outcome they were trying to reach |

#### Good JTBD prompts
- "Tell me about the moment you realized your old way wasn't working."
- "What were you doing before you tried this?"
- "What almost stopped you from switching?"
- "How did you decide this was worth trying?"
- "What would success have looked like for you at that moment?"

### Common Interview Mistakes

| Mistake | Why it's bad | Fix |
|---|---|---|
| **Asking leading questions** | Biases the answer | "Tell me about..." not "Don't you think...?" |
| **Confirmation bias** | Only hearing what supports your idea | Actively look for disconfirming evidence |
| **Too many hypotheticals** | What people *say* they'd do ≠ what they *do* | Ask about past behavior |
| **Not asking "why" enough** | Surface-level answers | Ask "why" iteratively |
| **Interviewing your own team** | They know too much and aren't representative | Recruit from outside |
| **Solutionizing during interviews** | Thinking about solutions instead of listening | Stay in the problem space |
| **Confusing a quote with a pattern** | One strong statement can distort the whole picture | Look for repeated evidence across participants |

**Sample size:** For generative research, 15-20 users per segment often reaches saturation. For JTBD or switching interviews, 8-12 strong interviews can reveal consistent patterns if the segment is narrow.

---

## 4. Usability Testing

### Moderated vs Unmoderated

| | Moderated | Unmoderated |
|---|---|---|
| **How it works** | Researcher guides the session in real-time | User completes tasks alone on a platform |
| **Pros** | Rich insights, can probe, catch surprises | Scale, speed, cost-effective, unbiased |
| **Cons** | Time-intensive, requires facilitator | No clarification, technical issues |
| **Best for** | Complex tasks, early testing, trust-sensitive flows | Simple tasks, later-stage validation, quantitative metrics |
| **Tools** | UserTesting, Lookback, Zoom | UserTesting, Maze, UserZoom |

### The 5-User Rule (Jakob Nielsen)

Testing with 5 users finds ~85% of usability problems. The ROI diminishes sharply after 5:
- 1 user → finds ~1/3 of issues
- 5 users → finds ~85% of issues
- 10 users → finds ~90% of issues
- 20+ → diminishing returns

**Run multiple rounds of 5 rather than one round of 10+.** Fix issues between rounds.

### How to Run a Usability Test

**1. Define tasks (not instructions)**
- ❌ "Click the 'Add to cart' button"
- ✅ "You're looking to buy a blue t-shirt in size M. Show me how you'd do that."

**2. Think-aloud protocol**
Ask users to verbalize their thoughts as they navigate. This reveals *what* they're thinking, *why* they're clicking, and *where* they're confused.

**3. Practice silence**
After giving a task, stay quiet. Count to 10 before prompting. Users often fill silence with valuable insights.

**4. Observe what they *do*, not what they *say***
Watch their clicks and navigation — not just their verbal feedback. Behavior trumps opinion.

**5. Capture severity**

| Severity | Definition | Action |
|---|---|---|
| **Critical** | Task cannot be completed | Fix before next round |
| **High** | Major friction, task takes too long, or breaks trust | Fix before launch |
| **Medium** | Friction but task eventually completed | Prioritize with team |
| **Low** | Minor confusion, cosmetic | Address if time permits |

### Comprehension and Trust Testing

Some flows are less about task completion and more about whether users understand what is happening.

Use targeted testing for:
- privacy or consent flows
- pricing and billing explanations
- AI-generated content or recommendations
- account deletion, destructive actions, irreversible changes
- permission prompts and data sharing

Ask users:
- "What do you think will happen if you click this?"
- "What information is this asking you for?"
- "Do you feel you have a real choice here?"
- "What, if anything, feels unclear or risky?"

A usable flow can still be untrustworthy. Treat comprehension and fairness as separate things to validate.

---

## 5. Surveys

### When to Use Surveys
- Need quantitative data from a large sample
- Measuring satisfaction (NPS, CSAT, SUS)
- Validating interview findings at scale
- Understanding user demographics and behaviors
- Measuring confidence, trust, or comprehension after an interaction

### Survey Best Practices
- **Keep it short** — Under 5 minutes. Long surveys = abandonment + bad data.
- **Use established scales** — NPS (0-10), Likert (1-5 or 1-7), SUS (System Usability Scale)
- **Avoid double-barreled questions** — "How easy and pleasant was the checkout?" → Ask each separately
- **Pilot test** — Run with 5 people to catch confusing wording
- **Consider timing** — In-app surveys capture immediate experience. Email surveys get more thoughtful responses but lower response rates
- **Don't ask for certainty users do not have** — People will answer confidently even when the experience was ambiguous

### Common Survey Types

| Type | Measure | Format |
|---|---|---|
| **NPS** | Overall loyalty | "How likely to recommend?" (0-10) |
| **CSAT** | Transaction satisfaction | "How satisfied were you?" (1-5) |
| **SUS** | System usability | 10-question standardized scale (1-5) |
| **SEQ** | Task-level ease | "How difficult was this task?" (1-7) |
| **Trust / confidence pulse** | Perceived safety or clarity | "I understood what would happen next" (Likert) |

---

## 6. Synthesis Methods

Synthesis is where raw research becomes actionable design insight.

### Affinity Mapping

Group individual observations/themes into clusters to find patterns.

**Process:**
1. Each observation goes on a sticky note (one per note)
2. Silently cluster notes by theme
3. Name each cluster (the insight)
4. Prioritize clusters by frequency/salience
5. Translate into design implications

**Best for:** Open-ended research, interviews, diary studies

### Journey Mapping

A visual timeline of the user's experience with your product, including touchpoints, emotions, and pain points.

**Components:**
```
Phase:   Discover → Evaluate → Purchase → Use → Support
Actions: [What user does at each stage]
Touchpoints: [Where they interact with the brand]
Emotions:   [😊 → 😕 → 😠 → 😊]
Pain points: [What's broken]
Opportunities: [Where we can improve]
```

**Best for:** Understanding the full experience, identifying handoff failures, aligning teams

### Jobs To Be Done Map

Map the functional, emotional, and social jobs your product is hired for.

**Format:**
```
When [situation],
I want to [motivation],
So I can [expected outcome].

Functional job: [practical task]
Emotional job: [how user wants to feel]
Social job: [how user wants to be perceived]
```

#### Go deeper with forces of progress

| Force | Question |
|---|---|
| **Push** | What was frustrating enough to make change possible? |
| **Pull** | What made the new option feel attractive or promising? |
| **Anxiety** | What almost prevented adoption? |
| **Habit** | What old behavior was hard to break? |

**Best for:** Understanding motivation, unmet needs, adoption, churn, and competitive positioning.

### Assumption Mapping and Learning Agenda

Not all unknowns are equal. Map assumptions by **importance** and **evidence**.

| Assumption | Importance | Evidence today | What we need to learn | Best method |
|---|---|---|---|---|
| [Assumption] | High / Medium / Low | Strong / Weak / None | [Question] | [Method] |

Focus first on assumptions that are:
- **high impact if wrong**
- **weakly supported today**
- **likely to change the design direction**

This creates a **learning agenda** — the ordered list of questions the team should answer before committing to more design or build.

### Mixed-Method Triangulation

The best research programs combine methods rather than trusting a single source.

Examples:
- **Interview + analytics** → understand both motivation and scale
- **Usability test + survey** → observe friction, then measure confidence or prevalence
- **Support tickets + JTBD interviews** → connect recurring complaints to deeper user progress and anxieties
- **Prototype test + A/B test** → learn fast qualitatively, then validate at scale

Rule of thumb: if the decision is expensive, controversial, or trust-sensitive, triangulate.

### Research Readout Structure

```text
**Decision supported:** What choice this research informs
**Background:** Why we did this research
**Method:** What we did and with whom
**Top 3 findings:**
1. [Finding] → [Implication]
2. [Finding] → [Implication]
3. [Finding] → [Implication]
**Evidence quality:** High / Medium / Low — and why
**Key quotes:** [2-3 verbatim quotes]
**Recommendations:** [3-5 concrete next steps]
```

---

## 7. Research Ops & Ethics

### Participant Recruitment

| Method | Pros | Cons |
|---|---|---|
| **Customer database** | Already users, context-rich | Sample bias, survey fatigue |
| **Third-party panels** | Fast, diverse | Expensive, less context |
| **Social media** | Cheap, broad | Self-selection bias |
| **Intercept (in-product)** | Captures users in-context | Intrusive if not careful |

**Incentives:** Always offer compensation. $50-75 for 30min, $100-150 for 60min (consumer). 2x for B2B or niche audiences.

### Research Ethics
- **Informed consent** — Participants should understand what they're agreeing to
- **Privacy** — Anonymize data. Don't share recordings outside the team without permission
- **No deception** — Be honest about what you're testing
- **Right to withdraw** — Participants can stop at any time
- **Avoid bias** — Don't recruit only people who already love your product

### Researching Trust, Consent, and Sensitive Flows

Participant ethics are not the same as product ethics. Some experiences require dedicated research on trust and fairness.

Use targeted research when the design includes:
- account deletion or irreversible actions
- payments, billing, or hidden costs
- privacy settings, permissions, or data sharing
- AI-generated recommendations or summaries
- onboarding that nudges behavior aggressively
- vulnerable users or high-stakes decisions

Questions to ask:
- "What do you think this screen is asking from you?"
- "Do you feel you have a real choice here?"
- "What feels unclear, risky, or pushy?"
- "What would make you trust this more?"
- "What would make you stop and leave?"

---

## Quick Reference: Choosing a Research Method

| You need to know... | Choose this method |
|---|---|
| What problem users are trying to solve | Discovery interview or JTBD interview |
| What problems users face in context | 1:1 interviews, field study, or diary study |
| Whether users can complete a task | Moderated usability test |
| Which design performs better quantitatively | A/B test |
| How users organize information naturally | Card sort or tree test |
| How users feel about your product at scale | Survey (NPS / CSAT / SUS) |
| How the full user experience feels | Journey mapping |
| Why users are switching or churning | JTBD interview + analytics + support review |
| If your navigation makes sense | Tree test |
| Whether accessibility issues exist | Accessibility audit |
| Whether users understand or trust a sensitive flow | Comprehension test or trust interview |
| What users actually do (vs say) | Diary study, field observation, or analytics |
