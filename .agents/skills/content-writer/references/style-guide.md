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

### 🔹 Dash restraint

Em dashes are useful when a sentence needs a turn, interruption, or compact contrast. They start sounding synthetic when they become the default glue between simple clauses.

| Overdone | Better |
|---|---|
| "The product is fast: easy to set up: simple to share: built for teams." | "The product is fast, easy to set up, and simple to share. It's built for teams." |
| "You get one dashboard: one workflow: one place to manage everything." | "You get one dashboard and one workflow in a single place to manage everything." |
| "Fermy Lab, an innovative fermented food brand, bridges traditional Indian culinary wisdom with modern design." | "Fermy Lab brings traditional Indian culinary wisdom into a modern design system." |
| "The platform is flexible: and it scales with your team." | "The platform is flexible, and it scales with your team." |

**Rule:** In normal body prose, default to zero em dashes. If a dash can be replaced with a period, comma, or colon without losing force, replace it.

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
2. **Pick 3 adjectives it is NOT** (e.g., "corporate, fluffy, edgy")
3. **Three sample sentences** in that voice: write them and check they feel right

### Voice examples (for reference)
- **Stripe:** Developer peer. Precise, confident, no marketing fluff.
- **Mailchimp:** Friendly, slightly cheeky, plain-spoken. Treats the reader like a small-business friend.
- **Basecamp:** Direct, opinionated, contrarian-friendly. Argues a position.
- **Notion:** Warm, slightly playful, tool-agnostic language ("docs," "pages").

---

## 7. Before/After Rewrite Library

### Example 1: Robotic tech doc → humane
❌ "The system utilizes machine learning algorithms to generate predictions."
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
- [ ] "In order to" instead of "to"
- [ ] "It is important to note that" (just note it)
- [ ] "At the end of the day" / "in today's fast-paced world" / other cliché openers
- [ ] Passive voice where the actor is known
- [ ] Dashes are doing the work of full stops or commas across the paragraph
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

### Lead with the reader's tension
Don't open with background unless the background is the tension. Start where the reader already feels friction, curiosity, fear, hope, or urgency.

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
