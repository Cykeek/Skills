# Writing Rules — Deep Reference

This is the deep reference for copy and content optimization. Use this when auditing raw text, adjusting professional tone, implementing keyword alignment, or rewriting descriptions.

---

## 1. Tone and Voice

### 1.1 Objective & Professional
A resume is an objective highlight reel, not a narrative biography. The tone must be authoritative, factual, and professional.
- **No Personal Pronouns:** Never use "I", "me", "my", "we", "our", "you", or "us".
  - *Incorrect:* I led a team of 4 engineers to design our mobile app.
  - *Correct:* Led a 4-person engineering team to design a mobile application.
- **Third-Person Implicit:** Begin sentences directly with action verbs, omitting pronouns and filler subjects.
  - *Incorrect:* Candidates will find that I developed new schemas...
  - *Correct:* Developed new data schemas...
- **Active Voice:** Focus on what the subject did, rather than what happened to them.
  - *Incorrect:* New APIs were developed under my supervision.
  - *Correct:* Engineered new REST APIs to improve data sync.

---

## 2. Formatting Numbers & Measuring Impact

Always convert text numbers to digits (numbers) for readability and space efficiency.
- **Numeric over Text:** Use "5" instead of "five," "12%" instead of "twelve percent."
- **Estimates:** If exact metrics are unavailable, request estimates from the candidate or list conservative ranges (e.g. "Optimized codebase, saving 15-20 hours of runtime monthly").
- **Metrics Placement:** Try to place the numeric impact at either the very beginning or the very end of the bullet point to catch a recruiter's eye.

| Weak Bullet | Improved Bullet with Metric |
|---|---|
| Handled cloud migration projects | **Migrated** 15 legacy databases to AWS Cloud infrastructure, reducing downtime to **0.01%**. |
| Made system load fast | **Decreased** median page load speeds by **34%** using visual caching. |
| Supported high call volumes | **Resolved** an average of **60+** tech support cases daily while maintaining a **98%** CSAT score. |

---

## 3. ATS Spelling, Acronyms, and Keyword Alignment

ATS systems search for exact character strings. A candidate who knows a skill but spells it incorrectly or abbreviates it non-standardly may be ignored.

### 3.1 Acronym Expansion Rule
List both the acronym and the spelling out of technical/process phrases at least once to capture both search methods.
- **Example:** "Search Engine Optimization (SEO)"
- **Example:** "Software Development Life Cycle (SDLC)"
- **Example:** "Annual Recurring Revenue (ARR)"

### 3.2 Exact Keyword Formatting
Do not alter technical spelling or capitalization. Match the syntax of the job description exactly.

| Correct Industry Term | Incorrect Variants |
|---|---|
| React | react, ReactJS |
| JavaScript | javascript, JS, Java Script |
| Product Manager | product management, PM, PMer |
| Scrum Master | Scrummaster, agile scrum leader |
| SaaS | saas, S.a.a.S. |
| SQL | Sql Database, SQL querying |

---

## 4. Keyword Placement & Density

### 4.1 Placement Priority
Optimize keyword presence by spreading words across these strategic locations:
1. **Resume Title (under Header):** Matches the target position EXACTLY (e.g., "Senior Full-Stack Engineer").
2. **Professional Summary:** Place 2-3 most important hard skills or industry frameworks here.
3. **Skills Section:** Standard storage location for technical languages, systems, and platforms.
4. **Professional Experience:** Re-contextualize the skills in actual usage scenarios. An ATS parser will verify how recently and for how long the skill was applied.

### 4.2 Avoiding Keyword Stuffing
Do not dump a massive, unformatted block of keywords at the bottom of the page or in hidden (white) font text. Modern parsers flag hidden text and list indexing, and human recruiters instantly reject resumes with meaningless skill blocks. Integrate skills naturally into bullet points:
- *Bad:* Skills used: React, CSS, HTML, Webpack, Git, Agile, JIRA.
- *Good:* Built **React** components styled with modern **CSS/HTML** and bundled using **Webpack**, managing tasks inside an **Agile** environment using **Jira**.

---

## 5. Plain Language for Non-Technical Audiences (HR, CEO, Leads)

**Purpose:** Resumes are first read by HR, then hiring managers, then technical leads, and sometimes CEOs. Every bullet must be understandable by all audiences without losing technical precision.

### 5.1 Translation Principle
> **Lead with the business outcome, then the method.** Non-technical readers scan for impact first; technical readers verify the how.

| Audience | What They Scan For | What They Need |
|----------|-------------------|----------------|
| **HR / Recruiter** | Keywords, titles, years, clear impact | "Increased conversion 9pp" — recognizable metric |
| **CEO / VP** | Strategic value, scale, revenue, risk | "$460K ARR retained" — business outcome |
| **Hiring Manager** | Relevant scope, team size, process | "15M+ merchants, 12 teams" — scope context |
| **Technical Lead** | Tools, architecture, complexity | "React/TypeScript, A/B test (n=24k, p<0.01)" — technical proof |

### 5.2 Technical → Plain Language Translation Table

| Technical Term | Plain Language Alternative | When to Use Plain Version |
|----------------|----------------------------|---------------------------|
| **A/B testing** | "tested two versions to find what works better" | Summary, first mention |
| **API** | "software connection" / "system interface" | First mention, non-tech bullets |
| **CI/CD** | "automated testing and deployment" | Summary, cross-functional bullets |
| **Component library** | "reusable design building blocks" | Skills, non-tech bullets |
| **Design system** | "unified design standards across products" | Summary, first mention |
| **Design tokens** | "centralized design values (colors, spacing)" | Technical bullets only |
| **End-to-end** | "complete, from start to finish" | All contexts |
| **Frontend / Backend** | "user-facing / behind-the-scenes" | First mention |
| **Full-stack** | "works across user interface and server" | Summary, Skills |
| **GraphQL** | "flexible data query system" | Technical bullets only |
| **JTBD (Jobs to Be Done)** | "user needs research" | First mention |
| **Microservices** | "independent service architecture" | Technical bullets only |
| **PCI-DSS** | "payment security standard" | Domain bullets |
| **Prototyping** | "building interactive mockups" | All contexts |
| **React / TypeScript** | "modern web development stack" | Summary, non-tech bullets |
| **REST API** | "standard web interface" | Technical bullets only |
| **Storybook** | "component documentation tool" | Technical bullets only |
| **WCAG 2.2 AA** | "accessibility standard (level AA)" | First mention |
| **Zero-to-one (0→1)** | "building from scratch" | All contexts |

### 5.3 Rewrite Patterns for Audience Clarity

#### Pattern A: Lead with Outcome (CEO/HR Friendly)
```
TECHNICAL:  Architected Design System v2 token architecture: 12 teams, 87% UI coverage, 0 breaking changes in 18mo
CLEAR:      Built unified design standards (Design System v2) adopted by 12 teams covering 87% of product UI — zero breaking changes in 18 months
SIGNAL:     [Systems Thinking] [Technical Fluency]
```

#### Pattern B: Translate Method Inline (Manager Friendly)
```
TECHNICAL:  Pair-programmed React/TypeScript components with 2 E5 engineers; cut handoff 3.2 days→0.8 days
CLEAR:      Collaborated directly with senior engineers to build production-ready components in React/TypeScript, reducing design-to-engineering handoff from 3.2 days to 0.8 days
SIGNAL:     [Technical Fluency] [Cross-functional Leadership]
```

#### Pattern C: Domain Context for Non-Domain Experts (HR Friendly)
```
TECHNICAL:  Spearheaded checkout redesign for 15M+ merchants delivering +9pp activation (18%→27%), $460K ARR retained; validated via A/B test (n=24,847, p<0.01, holdout confirmed)
CLEAR:      Led checkout redesign for 15+ million merchants, increasing completion rate by 9 percentage points (18% to 27%) and retaining $460K in annual revenue; proven through controlled experiment with 24,847 users
SIGNAL:     [Data-Informed Iteration] [Cross-functional Leadership]
```

### 5.4 Rules for Audience-Aware Writing

1. **First mention = plain + technical:** "A/B testing (controlled experiments comparing two versions)" — then use technical term subsequently
2. **Summary = 80% plain, 20% technical:** CEO/HR reads this first
3. **Skills section = exact technical terms:** ATS needs precise keywords
4. **Experience bullets = 50/50 balance:** Lead with outcome, include method
5. **Never assume domain knowledge:** "PCI-DSS (payment security standard)" not just "PCI-DSS"
6. **Scale = concrete numbers:** "15M+ merchants" not "millions of users"
7. **Time = calendar time:** "3.2 days → 0.8 days" not "75% faster"

### 5.5 Anti-Patterns for Mixed Audiences

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Pure jargon in Summary | HR/CEO can't parse | Lead with business outcome |
| Acronyms without expansion | Non-technical readers lost | Spell out first: "Design System (DS)" |
| Technical detail without impact | "So what?" for leaders | Always pair method → result |
| Vague scale ("large scale") | Not credible | Specific: "15M+ users, 12 teams" |
| Statistical notation only | "p<0.01" means nothing to HR | Add plain: "statistically significant (p<0.01)" |
| Tool lists without context | "Figma, React, Storybook" = skills dump | "Built in Figma, prototyped in React/Storybook" |

---

## 6. Quick Reference: Edit Commands for Clarity (LaTeX)

```bash
# Add plain language translation to bullet
agent latex inject --resume main.tex --bullet 3 --prepend-translation "A/B testing" "tested two versions to find what works better"

# Expand acronym at first use
agent latex inject --resume main.tex --bullet 1 --expand-acronym "PCI-DSS" "Payment Card Industry Data Security Standard (payment security standard)"

# Lead with outcome
agent latex audience --resume main.tex --bullet 2 --restructure outcome-first

# Add scale context
agent latex inject --resume main.tex --bullet 4 --add-scale "12 teams" "12 cross-functional product teams"
```
