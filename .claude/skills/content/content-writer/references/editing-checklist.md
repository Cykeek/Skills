# Editing Checklist: The Senior Editor's Rubric

This is the deep reference for editing, critiquing, and revising content. Read this when the user asks you to edit, rewrite, critique, or improve any content.

**The principle:** Senior editing isn't line-by-line fixing: it's diagnosing *what's not working* and *why*, then making the fewest, highest-impact changes. Don't rewrite everything; fix what matters.

---

## 1. The Three Editorial Phases

Edit in sequence. don't proofread commas when the structure is broken. Aligning work into these three distinct phases ensures editing effort is spent where it matters most:

1. **Phase 1: Developmental Editing** (auditing structure, logical flow, value of the hook, and argument strength).
2. **Phase 2: Copyediting** (polishing tone, readability, sentence variety, contraction levels, and enforcing the em-dash ban).
3. **Phase 3: Proofreading** (addressing spelling, mechanics, spaces, grammar).

---

## 2. Phase 1: Developmental Editing

Auditing the core structure, flow, and argument strength of the content.

### Structure & Flow
- [ ] **Does the opening earn the next sentence?** The first 50 words decide whether the reader continues.
- [ ] **Is the lede buried?** Real insight should be near the top, not in paragraph 4.
- [ ] **Does each section deliver on what its heading promises?** No bait-and-switch.
- [ ] **Is the structure scannable?** Subheadings, short paragraphs, lists where appropriate.
- [ ] **Are lists doing real work?** If a section expresses one idea, it probably wants prose, not bullets.
- [ ] **In cards, grids, or compact UI copy, would heading + short paragraph feel more natural than mini-bullets?**
- [ ] **Do sections flow logically?** Each section should set up the next. No jarring jumps.
- [ ] **Is there a clear takeaway?** Reader should leave knowing the one thing the piece wanted to say.
- [ ] **Does the closing land?** Last sentence lingers: does it leave the reader with something specific to act on, think about, or feel?

### Clarity & Argument Strength
- [ ] **Is the core argument clear?** Summarize it in one sentence. If you can't, the piece isn't clear.
- [ ] **Is every claim supported?** Either with data, an example, or a clear line of reasoning.
- [ ] **Are generalities specific?** "Many businesses struggle" → "73% of mid-market SaaS companies report churn above 5%" (or cut the claim).
- [ ] **Is jargon defined on first use?** Don't assume the reader knows it.
- [ ] **Are examples concrete?** "A customer" → "Acme Co., a 200-person fintech" (when allowed).
- [ ] **Are counterarguments acknowledged?** It builds trust and preempts objections.
- [ ] **Does each paragraph make one point?** If a paragraph does three things, split it.

---

## 3. Phase 2: Copyediting

Polishing sentence structure, tone, readability, concision, and mechanics.

### Concision (the 10–20% cut)
- [ ] **Are there filler words?** "to" → "to." "Due to the fact that" → "because." "At this point in time" → "now."
- [ ] **Are adverbs and adjectives earning their place?** "Very," "really," "actually," "essentially": cut almost all of them.
- [ ] **Are there redundant pairings?** "Each and every," "first and foremost," "future plans": pick one.
- [ ] **Is repetition doing work?** Repeating for emphasis is fine. Repeating because you didn't notice is not.
- [ ] **Are there throat-clearing openers?** "it's important to note that…" → just note it.
- [ ] **Could the piece lose 10–20% of its words and be better?** Almost always yes.

### Voice, Tone & Readability
- [ ] **Does it sound like a human?** Use the "would I say this out loud?" test.
- [ ] **Are contractions used?** Should be ~70–80% of eligible spots (refer to `style-guide.md`).
- [ ] **Is the tone consistent?** Don't switch from peer-to-peer to formal-academic mid-piece.
- [ ] **Voice drift check:** Read only paragraphs 1, 3, and 5 (or a sample spread across the piece). Do they sound like the same writer in the same mood? If a middle paragraph sounds noticeably more corporate or robotic, rewrite it.
- [ ] **Is it the right tone for the audience?** Developers vs executives vs consumers: adjust accordingly.
- [ ] **Are sentences varied in length?** Mix short for punch with longer for flow. Ensure high readability.
- [ ] **Opening sentence quality:** Does the first sentence drop directly into the reader's situation, tension, or question, without scene-setting preamble? Red flags: "In today's world," "As we all know," "In this article, I will," "it's important to understand that," "The [X] landscape is evolving." If any of these appear, rewrite the opening sentence before presenting.
- [ ] **Is voice on-brand?** If the user has a brand voice, does this match? (See `style-guide.md` Section 6.)
- [ ] **Are hedging and overclaiming balanced?** >2 hedges per paragraph = too soft. Zero hedging where uncertain = too rigid.

### Sentence-Level Polish & Em-Dash Ban
- [ ] **Active voice by default.** Convert passive where the actor is known.
- [ ] **Strong verbs over adverbs.** "He ran quickly" → "He sprinted."
- [ ] **No "use" for "use."** No "use" as a verb (unless physics). No "incentivize" if "encourage" works.
- [ ] **Zero em dashes in body prose (non-negotiable).** Scan every paragraph for,  characters. Replace each one: use a period if it's a full stop, a comma for a light pause, a colon to introduce an explanation, or parentheses for an aside. An em dash is only permissible in a direct quote where the source used one. No other body-copy use is acceptable.

---

## 4. Phase 3: Proofreading

Addressing grammar, spelling, mechanics, spaces, and formatting.

### Mechanical Check
- [ ] **Spelling & Typos:** Watch for homophones (their/there/they're, your/you're, its/it's).
- [ ] **Punctuation:** Apostrophes correct; **no em dashes (; ) in body prose** (use commas, colons, or periods instead); en-dash (–) for numeric/date ranges only; hyphen (-) for compound modifiers.
- [ ] **Capitalization consistency:** Title case in H2s, sentence case in body: pick one and stick.
- [ ] **Numbers and dates formatting consistency.**
- [ ] **Links work** and point where intended.

### Grammar & Sentence Mechanics
- [ ] **Subject-verb agreement:** Especially in long sentences where the verb drifts.
- [ ] **Pronouns have clear antecedents:** "It" and "they" should point to one obvious noun.
- [ ] **Parallel structure in lists:** All bullets should match in form (all imperative, or all noun phrases: not mixed).
- [ ] **Spacing:** Ensure there are no double spaces or spacing inconsistencies.

### Automated Content Linter
- [ ] **Run the Python content linter script:** Validate the draft against the em-dash ban, transition starters, and robotic tells by running:
  ```bash
  python.agents/skills/content-writer/lint_content.py path/to/draft.md
  ```
  Ensure all warnings are resolved before submitting.

---

## 5. The "Read Aloud" Test

The single best edit pass. Read the piece aloud (or mouth it silently). Flag every place you:
- **stumble** → sentence is probably poorly constructed.
- **run out of breath** → sentence is too long. Break it.
- **sound robotic** → rewrite it the way you'd actually say it.
- **lose the thread** → the section needs an explicit transition or a clearer topic sentence.
- **bore yourself** → cut it or rewrite for impact.

---

## 6. The "10% Cut Rule"

Almost every draft gets better when you cut 10–20% of the words.

### How to cut without losing meaning
- Remove filler words ("to," "due to the fact that").
- Combine adjacent sentences that say nearly the same thing.
- Delete throat-clearing openers ("it's worth noting that…").
- Cut examples that don't add new information.
- Tighten verbose constructions ("make a decision" → "decide").
- Delete paragraphs that don't advance the argument.

### What NOT to cut
- Concrete examples and numbers (these convince).
- The reader's "why": the stakes and motivation.
- Transitions that genuinely aid flow.
- Proper pacing: don't cut everything to nothing; rhythm matters.

---

## 7. Diagnosing Common Problems

### "It feels flat"
- Likely cause: no specific examples, no stakes.
- Fix: Add a concrete example. State why the reader should care. Replace abstractions with names and numbers.

### "It's hard to follow"
- Likely cause: structure is muddled or sections jump.
- Fix: Outline the content first. Move sections to a logical order. Add transitions ("Here's why that matters:…") between sections.

### "It sounds like a corporate blog"
- Likely cause: robotic tells: no contractions, formal phrasing, hedge-overload.
- Fix: Apply `style-guide.md` Section 8 (Robotic Tells checklist). Rewrite as if explaining to a smart friend.

### "It feels AI-written"
- Likely cause: too many bullets, too many dash-connected clauses, and structure that reads like notes rather than finished prose.
- Fix: Merge weak lists into paragraphs, keep bullets only where scan value is real, and replace some dash-heavy sentences with simpler punctuation.

### "It's too long"
- Likely cause: padding to hit word count, OR trying to cover too much.
- Fix: Cut 10–20%. If still long, ask: "Is this one piece or two?" Split if needed.

### "It's too short / shallow"
- Likely cause: covered the topic at surface level only.
- Fix: Pick 1–2 sections to deepen with examples, data, or counterargument. Don't add fluff.

### "It doesn't convince"
- Likely cause: claims without evidence; objections not addressed.
- Fix: Add data, examples, or reasoning to back each major claim. Acknowledge the strongest counterargument and respond.

### "The opening is weak"
- Likely cause: started with context instead of a hook.
- Fix: Find the most interesting line in the piece (often buried in paragraph 3). Move it to the opening.

---

## 8. Delivering Edit Feedback

When the user asks you to "review" or "critique" their content, don't dump the full checklist. Prioritize.

### Format
```
**What I diagnosed:**
[1–2 sentences on the actual underlying issue: not just a list of fixes.
 The diagnosis matters more than the line edits.]

**Top 3 priorities (in order of impact):**
1. [Biggest issue]: [Why it matters]
2. [Next issue]: [Why]
3. [Next issue]: [Why]

**Revised version:**
[The rewrite, applying the fixes above]

**What changed and why:**
- [Change] → [Why it helps the reader]
- [Change] → [Why]

**Remaining optional polish:**
- [Nice-to-haves if they want to go further]
```

### Giving feedback well
- **Lead with the diagnosis**, not the line edits. "The argument lands in paragraph 4: readers will bounce before they get there" > "Consider restructuring paragraph 1."
- **Be specific.** "This is unclear" → "A reader doesn't know what 'use' refers to here: name the thing."
- **Show, don't tell.** Don't just say "make it more engaging": show the rewrite.
- **Praise sparingly and specifically.** "The opening line works because it names the reader's exact pain" beats "great opener!"
- **Don't rewrite everything.** Fix what matters. Over-editing destroys the writer's voice.

---

## 9. The Final Pass (Before Saying "Done")

- [ ] Title earns the click but the piece delivers on it.
- [ ] First sentence earns the second. Does not start with "In today's world," "In this article," "it's important," or any scene-setting preamble.
- [ ] Last sentence leaves the reader with something.
- [ ] The piece has at least one concrete example, number, or quote per major section.
- [ ] Every paragraph earns its place.
- [ ] Lists are used only where scanning, comparison, or sequence actually helps.
- [ ] Zero em dashes in body prose: scan the full text for "; " and replace every instance with a comma, period, colon, or parenthesis. No exceptions for "forceful contrast" in prose you generate.
- [ ] If the piece contains a card grid or feature grid: word count each card's body text. All cards in the same row must be within 15 words of each other. Heading lengths must be within 2-3 words of each other.
- [ ] Voice is consistent from first paragraph to last. No drift into formal, corporate, or academic register mid-piece.
- [ ] The piece passed the "read aloud" test.
- [ ] The takeaway is clear: could a reader summarize it in one sentence?
- [ ] It's 10–20% shorter than the first draft.
- [ ] It sounds like a human, not a manual.
