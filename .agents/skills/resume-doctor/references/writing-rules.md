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
