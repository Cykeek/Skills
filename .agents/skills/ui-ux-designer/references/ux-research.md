# UX Research — Deep Reference

This is the deep reference for user research methods, participant recruitment, synthesis techniques, and research operations. Read this when planning user research, analyzing findings, or deciding what to learn next.

---

## 1. Research Planning Framework

### 1.1 Start with the Decision

Every research activity should inform a specific decision. Before choosing a method:

1. **What decision will this research support?** — What question will the team be able to answer?
2. **What is currently unknown or assumed?** — What uncertainty are we reducing?
3. **What level of confidence is needed?** — Is this an exploratory direction or a ship/no-ship decision?
4. **What would change based on the answer?** — Some answers don't change anything; those questions shouldn't be researched.

### 1.2 The Research Question Matrix

| Type | Question format | Example | Suitable methods |
|---|---|---|---|
| **Exploratory** | What/how/why do users currently...? | "How do people currently track their expenses?" | Field study, contextual inquiry, diary study, interviews |
| **Evaluative** | Can users complete [task] successfully? | "Can users find and book a flight in under 3 minutes?" | Usability testing, first-click test, tree test |
| **Comparative** | Which option performs better on [metric]? | "Does option A or option B result in higher task completion?" | A/B test, preference test, usability test with comparison |
| **Descriptive** | How many/what proportion of users...? | "What percentage of users use the search feature weekly?" | Survey, analytics, log analysis |
| **Generative** | What are users' needs around [topic]? | "What are the unmet needs in expense tracking?" | Interviews, card sorting, diary studies, co-creation |
| **Causal** | Does [change] cause [outcome]? | "Does removing the sidebar reduce time to complete checkout?" | Controlled experiment, A/B test |

---

## 2. Research Methods Detailed Guide

### 2.1 User Interviews

**Best for**: Understanding motivations, attitudes, mental models, pain points, and needs.

**Sample size**: 5-8 per user segment for thematic saturation (Bertaux, 1981; Guest et al., 2006)

**When to use**: Discovery, generative research, understanding "why" behind behavior

**Types**:
- **Structured**: Fixed script, same questions in same order for every participant. Comparable data, less flexible.
- **Semi-structured**: Topic guide with open-ended questions. Most common method. Good balance of flexibility and comparability.
- **Unstructured**: Minimal script, conversational. Deep exploration but hard to compare across participants.

**Interview guide structure**:
1. **Warm-up** (5 min): Hello, purpose, consent, background context
2. **Current behavior** (15-20 min): How they do things now, walk me through last time
3. **Pain points & needs** (10-15 min): What frustrates them, what they wish existed
4. **Future state** (10 min): If you could wave a magic wand...
5. **Wrap-up** (5 min): Anything else, thank you

**Pro tips**:
- Ask "Tell me about the last time you..." rather than "How often do you..." — concrete stories over abstract estimates
- Ask "What would you change if you could?" — reveals unmet needs
- 5 second rule: If the participant pauses for 5+ seconds, stay silent. They're about to say something important.
- Avoid leading questions ("Wouldn't it be better if..."). Use open-ended prompts.
- Ask for contrary evidence: "What do your coworkers dislike about this approach?"

### 2.2 Contextual Inquiry

**Best for**: Understanding behavior in real-world context, complex workflows, uncovering gaps between what people say and what they do.

**Method**: Observe users in their natural environment (home, office, on-the-go) while they perform tasks. Ask questions during observation.

**The four principles** (Beyer & Holtzblatt):
1. **Context**: Go to the user's workplace. Don't bring them into a lab.
2. **Partnership**: User is the expert; you're learning from them. Collaborate to understand.
3. **Interpretation**: Your observations are hypotheses. Validate with the user.
4. **Focus**: Have a clear focus (what do you want to learn?) but stay open to surprises.

**Sample size**: 4-6 per role/segment

### 2.3 Diary Studies

**Best for**: Understanding longitudinal behavior, habits, context, and frequency over time.

**Method**: Participants log activities, experiences, or behaviors over a period (typically 5-14 days). Can be structured (specific prompts) or unstructured (open journal).

**Sample size**: 8-12 participants minimum (more drop-out than other methods)

**Log types**:
- **Notification-based**: Prompts sent at intervals throughout the day
- **Event-based**: Participant logs when a specific event occurs
- **End-of-day**: Summary reflection at the end of each day

### 2.4 Moderated Usability Testing

**Best for**: In-depth understanding of usability issues, watching users interact, getting real-time feedback.

**Method**: Participant completes tasks while researcher observes and asks questions. Can be in-person or remote.

**Sample size**: 5-7 users per round (80% of issues found with 5 users, per Nielsen)

**Tasks should be**:
- Specific: "Find a pair of running shoes under $100 and add them to your cart"
- Not leading: Not "Click on the search bar and type 'running shoes'"
- Goal-oriented: Complete a task, not just click a button
- Realistic: Based on actual user goals

**Metrics to collect**:
- Task completion (success/failure/partial)
- Time on task
- Errors made
- Number of clicks/steps
- Satisfaction rating (after each task or overall)
- Verbal expressions of confusion/frustration

**The think-aloud protocol**: Ask participants to verbalize their thoughts as they work through tasks. This reveals cognitive processes, not just behavioral outcomes.

### 2.5 Unmoderated Usability Testing

**Best for**: Larger sample sizes, quantitative usability metrics, distributed participants.

**Method**: Participant completes tasks remotely without a moderator. Recorded for later analysis.

**Tools**: UserTesting, Maze, Lookback, UserZoom

**Trade-offs**:
- ✅ Larger sample sizes (20-40 participants)
- ✅ No scheduling overhead
- ✅ Geographic diversity
- ❌ No ability to probe or follow up
- ❌ Technical issues can invalidate sessions
- ❌ Lower data richness than moderated

### 2.6 Card Sorting

**Best for**: Understanding how users categorize and label information.

**Method**: Users sort labeled cards into groups that make sense to them.

**Types**:
- **Open card sort**: Users create and label their own groups. Best for new structures.
- **Closed card sort**: Users place cards into predefined categories. Best for testing existing structures.

**Sample size**: 15-30 participants for open sort, 30+ for closed sort

**Outputs**: Dendrograms, similarity matrices, category labels, content groupings

### 2.7 Tree Testing

**Best for**: Testing the findability of information in a hierarchical structure.

**Method**: Participants find items in a simplified text-only navigation tree (no visual design).

**Sample size**: 30+ participants

**Metrics**:
- **Findability**: Percentage of participants who found the item
- **Directness**: Percentage who went to the correct section without backtracking
- **Time**: How long it took to find items
- **First click**: Where participants clicked first

### 2.8 Surveys

**Best for**: Quantitative data collection at scale, attitudinal measurement, self-reported behavior.

**Best practices**:
- Keep surveys under 10 minutes (under 5 minutes is ideal)
- Avoid double-barreled questions ("How satisfied are you with the speed and design?")
- Use balanced scales (equal positive and negative options)
- Include "Prefer not to say" / "Not applicable" options
- Pre-test with 5-10 people
- Use validated scales where possible (SUS, NPS, CSAT, SUPR-Q)

**Common standardized scales**:
| Scale | Measures | Questions | Score range |
|---|---|---|---|
| **SUS** (System Usability Scale) | Perceived usability | 10 | 0-100 |
| **NPS** (Net Promoter Score) | Likelihood to recommend | 1 + follow-up | -100 to +100 |
| **CSAT** (Customer Satisfaction) | Satisfaction with a specific interaction | 1-3 | 0-100% |
| **SUPR-Q** (Standardized User Experience Percentile Rank) | Overall UX quality | 13 | Percentile |
| **UEQ** (User Experience Questionnaire) | Pragmatic & hedonic quality | 26 | -3 to +3 |

**Sample size**: 100+ minimum, 384+ for population estimates (95% CI, 5% MOE)

---

## 3. Participant Recruitment

### 3.1 Finding Participants

| Source | Pros | Cons |
|---|---|---|
| **Existing user base** | Actual users; product-specific feedback | Hard to reach; sample bias |
| **UserInterviews.com** | Large pool; screening built in | Paid; may not find specialist users |
| **Social media** (Reddit, Twitter, LinkedIn) | Niche communities; fast | Self-selection bias |
| **Craigslist / local boards** | Diverse, non-tech population | Lower response quality |
| **Customer support lists** | Users who care; may be power users or unhappy users | Bias toward extremes |
| **Recruitment agency** | Screened, reliable | Expensive |
| **Snowball sampling** | Access to hard-to-reach groups | Homogeneous sample |

### 3.2 Screening Criteria

Screen for characteristics that match your target users:
- Demographics (age, location, income for consumer; role, industry for B2B)
- Behavior (has purchased X in last 3 months, uses Y feature weekly)
- Tech proficiency (from novice to expert)
- Exclude: professional UX testers, competitors, friends/family

### 3.3 Incentives

| Study type | Typical incentive (per hour) |
|---|---|
| **Usability test** | $50-100/hr for consumers; $100-200/hr for professionals |
| **In-depth interview** | $50-75/hr for consumers; $100-150/hr for professionals |
| **Diary study** | $100-200 total (often with completion bonus) |
| **Survey** | $1-5 (or enter a drawing for a larger prize) |

---

## 4. Synthesis & Analysis

### 4.1 Affinity Mapping

A bottom-up approach to finding patterns.

**Process**:
1. Write every observation/insight/quote on a separate sticky note
2. Silently group related notes
3. Label each group with a theme statement
4. Group themes into higher-level categories
5. Identify key takeaways and actionable insights

**Do**:
- Use the participant's words for quotes
- One idea per note
- Work silently (reduces bias from loud voices)
- Keep grouping until the labels are meaningful

**Don't**:
- Force groups if an observation doesn't fit
- Pre-decide the categories
- Include "observations" that are really solutions

### 4.2 Journey Mapping

A visual representation of a user's experience over time and across touchpoints.

**Typical elements**:
- **Phases**: Stages of the journey (Discover → Learn → Buy → Use → Support)
- **Actions**: What the user does at each stage
- **Touchpoints**: Where they interact (website, app, phone, email, in-person)
- **Emotions**: How they feel (happy, frustrated, confused)
- **Pain points**: Where the experience breaks down
- **Opportunities**: Where improvements can be made

**Fidelity**: Start with a low-fidelity map (sticky notes on a wall) and refine. High-fidelity maps are for communication, not analysis.

### 4.3 Jobs-to-Be-Done (JTBD)

Focuses on the *progress* the user is trying to make, not just tasks.

**The JTBD formula**: "When [situation], I want to [motivation], so I can [expected outcome]."

**The Four Forces of Progress**:
```
Progress = Push (current frustration) + Pull (attraction of new solution)
         - Anxiety (fear of switching) - Habit (inertia of current behavior)
```

**JTBD interview structure**: Focus on past transitions — when did the user switch from one solution to another? What triggered the switch? What were they worried about?

---

## 5. Research Ethics

### 5.1 Informed Consent

Every participant must:
- Know the purpose of the research
- Understand what will happen during the session
- Know how their data will be used (and stored/deleted)
- Consent freely without pressure (no coercion)
- Be able to withdraw at any time without penalty

**Consent form should include**:
- Study purpose and procedures
- Risks and benefits (minimal for most UX research)
- Confidentiality and data handling
- Recording consent (including the right to stop recording)
- Contact information for questions

### 5.2 Data Privacy

- Anonymize data: Remove PII (name, email, phone, address) from research artifacts
- Secure storage: Limit access to research files
- Limit recording access: Restrict recorded sessions to the core research team
- Data retention policy: Delete recordings after analysis is complete (unless re-consented)
- GDPR/CCPA compliance: Users can request their data be exported or deleted

### 5.3 Ethical Testing Practices

- Participants can stop at any time for any reason
- Don't pressure participants to continue if they're frustrated or uncomfortable
- Debrief after the session: explain the purpose, answer questions
- If testing with vulnerable populations (children, elderly, cognitively impaired), additional safeguards apply
- Never mislead participants about the purpose of the research unless essential (and then debrief fully)

---

## 6. Research Operations

### 6.1 Research Repository

Maintain a searchable repository of:
- Research reports and summaries
- Raw data (anonymized)
- Participant recordings (restricted access only)
- Participant database (consented for re-contact)
- Research backlog and roadmap

### 6.2 Research ROI

- **How to measure**: Track decisions influenced, design changes made, usability issues found, user satisfaction improvements
- **Time spent in usability testing saves time downstream**: 1 hour of usability testing can save 10+ hours of development rework
- **Presentation matters**: Research findings are useless if not communicated. Frame findings as actionable recommendations tied to business outcomes.

---

## When to Read This File

Read `ux-research.md` when:
- Planning a user research study (method selection, participant recruitment)
- Analyzing and synthesizing research findings
- Preparing research reports and presentations
- Setting up research operations and repository
- Teaching or mentoring others on research methods
- Designing a research ethics and consent process

**Document reference**: UX research methods, synthesis techniques, participant recruitment, ethics
**Last updated**: July 2026
