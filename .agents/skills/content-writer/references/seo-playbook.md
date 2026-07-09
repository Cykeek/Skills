# SEO Playbook

This is the deep reference for search optimization. Read this when the user asks for SEO work, keyword strategy, content auditing, or wants their content to rank.

**The guiding principle:** SEO serves the reader, not the other way around. Write for humans first, optimize for search second. Search engines reward content that genuinely satisfies the reader's intent.

---

## 1. Search Intent: Start Here

Before writing or optimizing, identify the reader's *actual* search intent. Intent determines format, length, and structure.

### The 4 intent types

| Intent | What the reader wants | Best format | Example query |
|---|---|---|---|
| **Informational** | To learn / understand | Tutorial, guide, explainer, FAQ | "what is a webhook" |
| **Commercial** | To evaluate options before buying | Comparison, listicle, review | "best CRM for startups" |
| **Transactional** | To buy / sign up now | Landing page, pricing page, product page | "buy iphone 15 pro" |
| **Navigational** | To find a specific site/page | Usually a brand search: minimal content needed | "stripe login" |

### Intent-matching test
Before finalizing, ask: **If someone Googles this phrase and lands here, will they leave satisfied?**
- If yes → intent match ✅
- If "they wanted a tutorial and I wrote a thought piece" → mismatch ❌, fix the format

### Common mismatch failures
- Writing a 2,000-word essay for a query that wants a quick answer
- Writing a listicle for a query that wants depth
- Writing a salesy landing page for an informational query (Google won't rank it)

---

## 2. Keyword Workflow

### Step 1: Find the primary keyword
- Use the user's existing data if available (Search Console, Ahrefs, SEMrush, etc.).
- If no tools, use: Google Autocomplete, "People Also Ask," related searches at the bottom of the SERP, and competitor titles.
- Pick **one primary keyword** per page. Trying to rank one page for 5 different keywords usually fails.

### Step 2: Validate the keyword
- Is there search volume? (Ask the user or check tools.)
- What's ranking now? Google it. The top 3 results tell you what Google thinks the intent is.
- Can you realistically compete? A brand-new site won't rank for "how to lose weight": go long-tail first.

### Step 3: Map related keywords
- **Synonyms and variations**: use these naturally, don't repeat the primary keyword 30 times.
- **LSI / semantic terms**: words that *should* appear on a page about this topic (e.g., a page about "running shoes" should mention "cushioning," "stride," "pronation").
- **Question keywords**: turn these into H2s. They often map to "People Also Ask" boxes.

---

## 3. On-Page SEO Elements

### Title tag (60 characters max)
- The single most important on-page element.
- Put the primary keyword near the front.
- Include a benefit or hook if it fits.
- Write 5–10 options, pick the best.
- Examples:
  - ✅ "Webhooks: The No-BS Guide for Developers (2025)"
  - ✅ "How to Write a Landing Page That Converts (with Examples)"
  - ❌ "Welcome to our blog about webhooks and related topics"

### Meta description (155 characters max)
- Doesn't directly affect ranking, but affects click-through rate.
- Treat it like ad copy: include the keyword, a benefit, and a reason to click.
- Example: "Learn how webhooks work, when to use them vs polling, and how to build your first one in 10 minutes. Code examples included."

### URL slug
- Short, keyword-rich, hyphen-separated.
- ✅ `/webhooks-guide` ❌ `/2024/03/14/category/marketing-stuff/article123`

### H1 (one per page)
- Should align with the title tag (not identical: the H1 can be slightly longer).
- Must contain the primary keyword naturally.

### H2 / H3 structure
- Use H2s for major sections, H3s for subsections. Don't skip levels (no H2 → H4).
- Each H2 should answer a sub-question the reader might have.
- Keywords in subheadings help: but only when natural.

### First paragraph
- The primary keyword should appear in the first 100 words. Naturally.
- Don't force it: "In this article about webhooks, we will discuss webhooks…" ❌

### Image alt text
- Describe the image. If it naturally includes a keyword, great. Don't stuff.
- ✅ "Diagram showing how a webhook delivers an event payload to an endpoint"
- ❌ "webhook webhook webhook diagram"

---

## 4. Content Depth & Structure

### The "10x content" principle
Don't just match what's ranking: be meaningfully better. Ask:
- Is it more thorough?
- Is it better structured (scannable, clear sections)?
- Does it have something original (data, examples, perspective)?
- Is it more current?
- Does it load and read better on mobile?

### Structural best practices
- **Short paragraphs**: 2–4 sentences max. Walls of text hurt mobile.
- **Front-load each paragraph**: the key idea in the first sentence.
- **Scannability aids**: bullet points, bold for key terms, callout boxes, tables for comparisons.
- **Use examples and visuals**: break up text with code blocks, diagrams, screenshots, real numbers.
- **Answer the question early**: don't make the reader wait 800 words for the answer. Provide it, then elaborate.

### Content depth benchmark
Look at the top 3 results for the target keyword. If they average 2,000 words, yours should be in that range: *but only if depth adds value*. Don't pad.

---

## 5. E-E-A-T Signals (Experience, Expertise, Authoritativeness, Trustworthiness)

Google's quality guidelines emphasize E-E-A-T. Bake these into content:

| Signal | How to demonstrate it in content |
|---|---|
| **Experience** | "We tested this with 50 customers…" / "After 3 years building this…" |
| **Expertise** | Use correct terminology, cite specialty sources, show you know the nuance |
| **Authoritativeness** | Author bio with credentials, links to your other authoritative work, citations from reputable sources |
| **Trustworthiness** | Cite sources, link to primary research, acknowledge limitations, don't overclaim, fix errors transparently |

### Practical moves
- Add an author bio with real credentials.
- Cite primary sources (link to the study, not the article about the study).
- Acknowledge trade-offs and counterpoints: it builds trust.
- Update content with dates when revised ("Updated July 2025").
- Display review/testimonial evidence, not just claims.

---

## 6. Internal Linking

### Why it matters
- Helps Google understand site structure and topical relationships.
- Distributes page authority.
- Keeps readers on the site longer.

### Best practices
- Link to **relevant** pages, not just any page. The linked page should genuinely help the reader.
- Use **descriptive anchor text**: not "click here" or "learn more."
  - ✅ "our deep dive on webhooks" ❌ "click here to learn more"
- Link **from** new content **to** older authoritative content: and **from** older content **to** new content when relevant.
- Aim for 3–8 internal links per long-form post. Don't force.
- Don't link to the same page twice in one piece.

---

## 7. External Links

- Link out to authoritative sources (original research, official docs, primary sources).
- This signals to Google that you've done research and your content is part of a credible ecosystem.
- Open external links in a new tab (UX best practice: note this for the user if relevant).
- Don't link to direct competitors for commercial-intent queries.

---

## 8. Schema Markup (Structured Data)

For the user to add to the page (mention when relevant, especially for technical/blogging audiences):

| Schema type | When to use |
|---|---|
| `Article` / `BlogPosting` | Blog posts, news articles |
| `HowTo` | Step-by-step tutorials |
| `FAQPage` | FAQ pages and FAQ sections in articles |
| `Product` | Product pages (with `Offer`, `AggregateRating`) |
| `Recipe` | Recipe content |
| `Review` | Reviews |
| `Organization` | Site-wide, in the footer |
| `BreadcrumbList` | Helps Google understand site hierarchy |

If the user is technical, suggest specific JSON-LD. If they're not, mention schema conceptually and offer to provide the markup.

---

## 9. Meta Tag Templates

### Title tag (60 chars)
```
[Primary keyword]: [Hook/benefit] | [Brand]
```
Examples:
- "Webhooks: The No-BS Guide (2025) | Acme"
- "How to Write a Landing Page That Converts | Acme"

### Meta description (155 chars)
```
[Primary keyword phrase]. [Benefit / what they'll get]. [Specific detail / reason to click].
```
Example: "Learn how webhooks work, when to use them vs polling, and how to build your first one in 10 minutes. Code examples included."

---

## 10. SEO Audit Checklist

When the user asks you to audit content for SEO:

- [ ] Is the search intent matched to the content format?
- [ ] Is there one clear primary keyword?
- [ ] Is the primary keyword in the title tag (front-loaded if possible)?
- [ ] Is the primary keyword in the H1?
- [ ] Is the primary keyword in the first 100 words?
- [ ] Are there related/LSI keywords naturally integrated?
- [ ] Are H2/H3s structured logically (no level skipping)?
- [ ] Are paragraphs short and scannable?
- [ ] Is there enough depth vs. ranking competitors?
- [ ] Are there 3–8 relevant internal links?
- [ ] Are external links pointing to authoritative sources?
- [ ] Is there an E-E-A-T signal (author bio, citations, original data, experience markers)?
- [ ] Is the meta description compelling and within 155 chars?
- [ ] Are images described with natural alt text?
- [ ] Does the page answer the question quickly (no burying the lede)?
- [ ] Is the content current (dated, refreshed)?

Return audit findings as a prioritized list (top 5 impactful fixes first), not an exhaustive checklist dump.

---

## 11. SEO Pitfalls to Avoid

- ❌ **Keyword stuffing**: anywhere. Search engines penalize; readers bounce.
- ❌ **Writing for a different intent than the query**: Google won't rank it.
- ❌ **Thin content**: 200 words on a topic that deserves 1,500.
- ❌ **Duplicate or near-duplicate content** across pages.
- ❌ **Ignoring the title tag and meta description**: they're your SERP ad copy.
- ❌ **Treating SEO as separate from quality**: the best SEO *is* great content. Done right, they don't compete.
- ❌ **Chasing volume over intent**: 1,000 visits from the wrong intent ≠ 100 from the right intent.
- ❌ **Forgetting mobile**: most readers are on phones. Test the reading experience.
- ❌ **Clickbait titles** that the content doesn't deliver. High bounce rate kills rankings.
