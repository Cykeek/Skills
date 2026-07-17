# Style & Voice Guide

This is the deep reference for tone, voice, and style. Read this whenever you're writing or adapting tone for any audience.

---

## 1. The Humane Voice: Core Principles

Write like a smart, warm human talking to another smart human. Not a manual. Not a press release. Not a textbook.

### The four pillars

| Pillar | What it means | What it looks like |
|---|---|---|
| **Conversational** | Reads like speech, not like regulation | Contractions, discourse markers, sentence fragments where natural |
| **Specific** | Concrete beats abstract every time | Real numbers, named examples, sensory details |
| **Empathetic** | Acknowledges the reader's reality | "We know deadlines are tight: here's the 5-minute version" |
| **Confident but undogmatic** | Takes a position without preaching | "I'd recommend…" not "You must…" / "One might consider…" |

---

## 2. The High-Leverage Fixes

These single changes do the most to make writing sound human.

### 🔹 Contractions (the #1 fix)

| Robotic | Humane |
|---|---|
| "You will need to configure the API key." | "You'll need to configure the API key." |
| "It is important that we do not overlook…" | "It's important we don't overlook…" |
| "They are not able to process…" | "They can't process…" |

**Rule:** Use contractions in ~70–80% of eligible spots. Reserve full forms for emphasis or formal disclaimers.

### 🔹 Sentence variety

Humans mix lengths. The robotic pattern is uniform length + uniform structure.

```
❌ Robotic:
The system requires authentication. You must provide a valid token.
Tokens expire after 24 hours. You can refresh them using the endpoint.

✅ Humane:
The system requires authentication via a valid token. Tokens expire
after 24 hours: but don't worry, you can refresh them using the endpoint.
Here's how.
```

**Rule:** Vary sentence openings. Not every sentence starts with "The / This / It / There." Drop in a one-sentence paragraph for emphasis.

### 🔹 Active voice

| Passive (robotic) | Active (humane) |
|---|---|
| "The file is saved by the system." | "The system saves the file." |
| "A decision was made to…" | "We decided to…" |
| "It is recommended that users…" | "We recommend users…" |

**Rule:** Active by default. Passive only when the actor is unknown, irrelevant, or you deliberately want to soften blame.

### 🔹 Dash & Hyphen Usage (Em Dash = Banned in Body Prose)

Em dashes (; ), en dashes (–), and hyphens (-) each have distinct roles. Misuse, especially of the em dash, can make prose feel artificial.

| Punctuation | Recommended Use | Alternatives to Overused Forms / Common Errors |
|---|---|---|
| **Em dash (—)** | **Forbidden in body prose by default.** The only permitted uses are: (1) a direct quote where the source used one, (2) technical documentation that requires it specifically, (3) when the user explicitly requests it in writing. In all other cases, rephrase to avoid it entirely. | • **Period** – if the break is a full stop, split into two sentences.<br>• **Comma** – for a lighter pause or non-essential clause.<br>• **Colon** – to introduce an explanation or list.<br>• **Parentheses** – for a clarifying aside.<br>• **Rephrase** – restructure the sentence so no break is needed. |
| **En dash (–)** | Use for numeric or date ranges (e.g., pp. 23–25, 2020–2021). Also for indicating a connection or conflict between two things of equal weight (e.g., New York–London flight). | Do not substitute for a hyphen in compound adjectives (e.g., user-friendly, not user–friendly). |
| **Hyphen (-)** | Use for compound modifiers before a noun (e.g., a *user-friendly* interface) and for word breaks at the end of a line. Also used in some compound words (e.g., *co-worker*). | Do **not** substitute for en or em dashes. If a compound word is commonly used and understood, consider if the hyphen can be removed (e.g., *frontend* vs. *front-end*). |

**Absolute Rule:** Em dashes are **banned in body prose** with no exceptions other than direct quotes and explicit user requests. Don't ask "can I use one here?" The answer is always no unless one of those two conditions is met. Every time you write a sentence containing —, stop and replace it before proceeding.

### 🔹 Em Dash Anti-Patterns & Human-Preferred Alternatives

AI often overuses em dashes in ways human writers avoid. Here's a guide to common misuses and how to fix them:

| AI Anti-Pattern (Overuse) | Human-Preferred Alternative | Example (AI Anti-Pattern) | Example (Human-Preferred) |
|---------------------------|-----------------------------|---------------------------|---------------------------|
| **For Appositives/Parentheticals:** Using em dashes where commas or parentheses suffice for non-essential information. | Use **commas** for lighter pauses, or **parentheses** for clarifying asides that don't need strong emphasis. | "ReModelUN—a high-profile AI podcast—needed a new brand." | "ReModelUN, a high-profile AI podcast, needed a new brand." OR "ReModelUN (a high-profile AI podcast) needed a new brand." |
| **To Introduce Explanations/Lists:** Replacing colons or periods for introducing an explanation, elaboration, or list. | Use a **colon** to introduce a list or explanation directly related to the preceding clause. Use a **period** if the explanation is a new sentence. | "The brand needed a framework—specifically addressing: visual consistency." | "The brand needed a framework: specifically addressing visual consistency." OR "The brand needed a framework. Specifically, it needed to address visual consistency." |
| **As a General Connector/Glue:** Linking closely related independent clauses or phrases when a comma, semicolon, or period is more natural. | Use a **comma** with a conjunction, a **semicolon** for closely related independent clauses without a conjunction, or a **period** for a clearer break. | "The system is agile—and it scales easily." | "The system is agile, and it scales easily." OR "The system is agile; it scales easily." |
| **For Simple Enumeration:** Using dashes to set off simple enumerations within a sentence. | Rephrase to use **commas** or present as a formal list. | "The solution featured: a logo—colors—typography." | "The solution featured a logo, colors, and typography." |

**Final Rule (no exceptions in prose):** When you find an em dash in something you have written, replace it. don't evaluate whether it was justified. Replace it with a period, colon, comma, semicolon, or parenthesis, or rephrase the sentence. The evaluation is already done: em dashes in prose are not permitted. The only non-replaceable cases are (1) verbatim external quotes and (2) explicit user instruction in that message. Neither of those is a prose decision you are making.

---

## 3. Rhetorical Devices That Add Warmth

| Device | Example |
|---|---|
| **Direct address** | "Here's what *you* need to know." |
| **Rhetorical questions** | "Why does this matter? Because…" |
| **Parenthetical asides** | "The config file (yes, the same one) lives at…" |
| **Softened imperatives** | "You'll want to verify the port first." (vs. "Verify the port.") |
| **Discourse markers** | "So," "Now," "Actually," "Of course," "After all," "Here's the thing" |
| **The "yet" framing** | "You can't do that *yet*." (Implies it's coming, not impossible.) |

---

## 4. Empathy Patterns

### Acknowledge before you inform
Start with the reader's frame of mind, not the system's capabilities.

| Robotic | Empathetic |
|---|---|
| "To reset your password, follow these steps." | "Forgetting passwords is frustrating: let's get you back in quickly." |
| "The error indicates a missing dependency." | "Looks like something's missing from your setup. Let's track it down." |
| "Here are the available options." | "You've got a few good paths forward here. Let's look at them." |

### Validate before you correct
When the user is wrong, lead with validation:

> "That's a logical approach, and it *would* work if the API used REST. However, this one uses GraphQL, so the query structure is a bit different. Let me show you the equivalent."

---

## 5. Audience-Specific Tone Adaptation

Tone isn't one-size-fits-all. Adjust these dials per audience.

### 👩‍💻 Developers
- **Tone:** Precise, technical, peer-to-peer, no fluff
- **Do:** Show code, name the actual function/API, acknowledge trade-offs, say "you'll hate this but…" when relevant
- **Avoid:** Marketing language, hand-waving, dumbed-down analogies that get the details wrong
- **Example:** "The `fetchUser()` call returns a Promise, so you'll want to `await` it: otherwise you get a pending state and the rest of your handler runs before the data lands."

### 💼 Executives
- **Tone:** Crisp, results-first, scannable, confident
- **Do:** Lead with the business outcome, use bullet points, quantify impact, get to the ask in the first paragraph
- **Avoid:** Process minutiae, jargon walls, hedging, anything they have to read twice
- **Example:** "Three options, ranked by ROI: Option A (6-month payback, $2M/yr upside), Option B (18-month payback, $5M/yr upside), Option C (strategic, no near-term ROI). My recommendation: A."

### 🛒 Consumers
- **Tone:** Relatable, story-driven, warm, benefits-first
- **Do:** Use "you," tell micro-stories, frame features as benefits, acknowledge their lives are busy
- **Avoid:** Spec sheets, internal jargon, condescending simplification, corporate voice
- **Example:** "No one sets out to spend their Saturday on hold with cable. That's why we built a setup that takes 5 minutes: and a real person to call if it doesn't."

### 🆕 First-time visitors
- **Tone:** Orient, reassure, don't assume jargon knowledge
- **Do:** Define terms on first use, point to the "start here" resource, keep sentences short
- **Avoid:** Inside baseball, acronyms without expansion, assuming they know your product's vocabulary
- **Example:** "Welcome! You're probably here because someone sent you a link. Here's what we do in one sentence, and here's where to start."

### 🎓 Technical-but-not-developer (PMs, analysts, designers)
- **Tone:** Bridge: technical enough to be useful, plain enough to be clear
- **Do:** Explain *why* a technical choice matters in terms of user/business impact
- **Avoid:** Either dumbing it down to "magic" or going full stack trace

### 🚨 Stressed / frustrated readers (support, error states)
- **Tone:** Calm, brief, action-first
- **Do:** Acknowledge the friction, give the fix in one sentence, offer the next step
- **Avoid:** Cheerfulness, long preambles, "we apologize for any inconvenience"

---

## 6. Brand Voice Mapping

When the user has a brand voice (or needs to build one), use this framework.

### The 4 voice dimensions

| Dimension | Range | Question to ask |
|---|---|---|
| **Formal ↔ Casual** | "Per our evaluation" ↔ "So we checked…" | How dressed-up is the language? |
| **Serious ↔ Playful** | "This matters" ↔ "This is fun" | How much levity is appropriate? |
| **Respectful ↔ Irreverent** | "Industry standard" ↔ "Industry 'standard'" | How much do you respect conventions? |
| **Matter-of-fact ↔ Visionary** | "Here's what we built" ↔ "Here's the future we're building" | How much do you lean on aspiration? |

### Mapping a brand in 5 minutes

Ask the user (or infer from their existing content):
1. **Pick 3 adjectives** that describe the brand (e.g., "warm, confident, no-nonsense")
2. **Pick 3 adjectives it's NOT** (e.g., "corporate, fluffy, edgy")
3. **Three sample sentences** in that voice: write them and check they feel right

### Voice examples (for reference)
- **Stripe:** Developer peer. Precise, confident, no marketing fluff.
- **Mailchimp:** Friendly, slightly cheeky, plain-spoken. Treats the reader like a small-business friend.
- **Basecamp:** Direct, opinionated, contrarian-friendly. Argues a position.
- **Notion:** Warm, slightly playful, tool-agnostic language ("docs," "pages").

---

## 7. Before/After Rewrite Library

### Example 1: Robotic tech doc → humane
❌ "The system uses machine learning algorithms to generate predictions."
✅ "The system uses machine learning to make predictions: and it gets better the more data you feed it."

### Example 2: Stiff landing page → conversational
❌ "Authentication is required before accessing the dashboard."
✅ "You'll need to log in before you can see the dashboard."

### Example 3: Vague marketing → specific
❌ "Our platform empowers businesses to achieve operational excellence."
✅ "Our platform cuts the average team's reporting time from 6 hours a week to under 30 minutes."

### Example 4: Hedging overload → confident
❌ "It might possibly be the case that this could potentially improve performance."
✅ "This should improve performance. If it doesn't, here's likely why."

### Example 5: Bury-the-lede → lead with it
❌ "In today's fast-paced digital landscape, businesses face many challenges. One such challenge is customer retention. Our solution…"
✅ "You're losing customers you don't have to. Here's the fix."

### Example 6: Consumer marketing, robotic → warm
❌ "Our coffee subscription service delivers premium beans to your doorstep on a monthly basis."
✅ "Fresh beans, every month, straight to your door. No more grocery-store coffee that's been sitting on a shelf since March."

### Example 7: Supportive email, canned → real
❌ "We apologize for any inconvenience this may have caused."
✅ "That shouldn't have happened: sorry. Here's what went wrong, and what we're doing to make sure it doesn't happen again."

---

## 8. The "Robotic Tells" Checklist

If you see these in a draft, fix them:

- [ ] Every sentence is the same length
- [ ] Every paragraph starts with "The," "This," "It," or "There"
- [ ] No contractions anywhere
- [ ] "Utilize" instead of "use"
- [ ] "to" instead of "to"
- [ ] "it's important to note that" (just note it)
- [ ] "At the end of the day" / "in today's fast-paced world" / other cliché openers
- [ ] Passive voice where the actor is known
- [ ] **Em dashes are misused:** (a) acting as generic connectors, (b) introducing lists/explanations where a colon/period is better, (c) for simple parentheticals where commas/parentheses suffice.
- [ ] Bullet points where prose would flow better
- [ ] A short explanatory block has been broken into bullets for no reader benefit
- [ ] Prose where bullet points would scan better
- [ ] Hedging density > 2 per paragraph ("might," "possibly," "perhaps")
- [ ] Zero hedging where uncertainty exists (sounds like a manual)
- [ ] Generic praise ("great question!") instead of specific response
- [ ] "Leverage" as a verb (use "use": unless you mean the physics definition)

---

## 9. Quick Voice Calibration Test

When in doubt, ask: **"Would I say this out loud to a smart colleague?"**
- If yes → ship it.
- If "I'd say it differently out loud" → rewrite it the way you'd say it.
- If "I'd never say this out loud" → it's too stiff. Rewrite.

---

## 10. Human-Craft Decision Rules

These rules come from reverse-engineering strong human-written SaaS blogs, landing pages, and long-form explanatory pieces. Use them while drafting and revising, not just during critique.

### Opening sentence quality rules
The first sentence is the most important sentence in any piece. Human readers make their "keep reading" decision within the first two sentences. AI-generated openings fail most often here.

**Banned opening patterns (rewrite immediately if you find these):**
| Banned pattern | Why it fails | Fix |
|---|---|---|
| "In today's [X] landscape..." | Throat-clearing. Reader already lives in today's landscape. | Start with what the reader is feeling or experiencing. |
| "In this article, I will..." | Table-setting. The reader can see what the article contains by reading it. | Cut it. Start with the first real idea. |
| "It is important to understand that..." | Stalling and condescending. It's all important or none of it is. | Just state the important thing. |
| "As we all know..." | Sets up the writer's comfort, not the reader's. | Either the reader knows (so skip it) or they don't (so teach it directly). |
| "[Topic] is a critical component of modern [field]." | Sounds like an essay introduction, not human writing. | Replace with a specific observation or a question the reader is already asking. |
| "In recent years, [trends]..." | Always vague, never urgent. | Replace with the specific trend and its consequence. |

**Strong opening patterns (use these instead):**
- Drop into the reader's situation: "You're three hours into debugging and the error message says nothing useful."
- Subvert an expectation: "Most dashboards show you everything except what you actually need."
- State the thesis directly: "The best landing pages don't sell products. They resolve anxiety."
- Pose the question the reader is already asking: "Should you write the blog post, the LinkedIn post, or the email series first?"
- Open in medias res: "The proposal was due Monday. The writer had a blank document."

### Voice drift detection
A piece "drifts" when the tone shifts noticeably between sections, usually because the writer (or AI) slipped into a more formal register mid-draft without noticing.

**How to check for it:** Read three non-adjacent paragraphs. If any paragraph sounds like a different writer (more corporate, more academic, more casual) it has drifted.

**Common drift triggers to watch for:**
- A paragraph that starts "it's worth noting that." when the rest of the piece uses contractions
- A paragraph that uses "use," "use," or "help" when the rest uses plain English
- A paragraph where every sentence starts with "The" or "This" when surrounding paragraphs vary their openings
- A paragraph of 6-8 bullet points nested inside a prose-first piece
- A paragraph that switches from "you" to "one" or "users"

**Fix:** Rewrite the drifted paragraph in the voice of the opening paragraph. Ask: "Would the first paragraph's writer have said this?"

| Weak opening | Stronger opening |
|---|---|
| "In today's digital landscape, teams need better workflows." | "Your review process got slower while the rest of development got faster." |
| "Email marketing is an important tool for businesses." | "So many tools, so much to sell. Sometimes the simplest place to start is email." |

### Give the skimmer an early win
Human-written web content often gives value before asking for attention. Use one of these near the top when useful:
- A TL;DR verdict
- A comparison table
- A quick answer
- A summary box
- A list of takeaways
- A "who this is for" line

### Translate facts into consequences
Don't stop at information. Tell the reader what it means in practice.

| Fact only | Fact + consequence |
|---|---|
| "The tool supports 50 integrations." | "The tool supports 50 integrations, which means most teams can keep their existing stack instead of rebuilding workflows from scratch." |
| "The page loads in 1.2 seconds." | "The page loads in 1.2 seconds, so mobile visitors aren't stuck waiting before they can act." |

### Match CTA timing to trust earned
Place calls to action after value, proof, or objection handling. The harder the ask, the more trust must come first.

- Low-friction CTA after hero: "Start free," "Try it," "Download template"
- Mid-friction CTA after proof: "Compare plans," "See examples"
- High-friction CTA after deeper validation: "Book a demo," "Talk to sales"

### Use transitions as momentum, not decoration
A good transition turns the previous section into a reason to read the next one.

Examples:
- "That solves the planning problem. The harder part is keeping the calendar alive after week one."
- "The pricing looks simple until team size enters the picture. Here's where the math changes."
- "Now that the claim is clear, let's look at the evidence behind it."

### Choose the ending shape intentionally
Endings should match the material:
- **Practical guide:** roadmap, checklist, next step
- **Landing page:** earned CTA
- **Thought leadership:** sharpened takeaway or challenge
- **Journalistic/explanatory piece:** image, unresolved question, callback, or warning
- **Comparison:** recommendation by use case

### Specificity is the main engine of human credibility
When a paragraph feels generic, add one of these:
- a named example
- a concrete scenario
- a number with context
- a quote in a real person's language
- a before/after contrast
- a constraint, trade-off, or edge case

### Prefer paragraphs over reflex bullets
Many AI drafts turn every idea into a list. Human writers usually don't. If the reader is taking in one idea or one supporting explanation, write a short paragraph. Use bullets only when the reader genuinely needs to scan, compare, follow sequence, or reference a set of distinct items later.

Good uses for bullets: steps, checklists, specs, side-by-side comparisons, option sets, or grouped facts. Poor uses: intro copy, single supporting ideas, short feature-card bodies, and small grid items that should read as heading plus body text.

For repeated surfaces like a 3x3 feature grid, the default pattern is:

```
[Heading]
[1-2 sentence body copy]
```

If each card only carries one idea, keep it in prose. Don't fracture that idea into three bullet fragments unless the card is truly acting as a checklist or spec module.
