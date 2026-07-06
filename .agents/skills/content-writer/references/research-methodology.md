# Research Methodology

This is the deep reference for content research — gathering, verifying, and synthesizing information. Read this when the user asks you to research a topic, find statistics, gather data, or fact-check claims.

**The principle:** Research serves the reader's trust. Cite sources the reader can verify. Be honest about what's known, what's estimated, and what's unknown. The most valuable research rarely comes from the first page of Google.

---

## 1. Source Credibility Tiers

Use this hierarchy. Higher tier = more authoritative.

### Tier 1 — Primary sources (gold standard)
- Original research (peer-reviewed studies, government statistics, official datasets).
- Direct quotes from named experts with verifiable credentials.
- Original documents (filings, legal judgments, terms of service).
- First-party data (the user's own analytics, customer interviews).

### Tier 2 — Quality secondary sources
- Reputable journalism (NYT, WSJ, Reuters, AP, FT, specialist trade press).
- Established analyst firms (Gartner, Forrester, McKinsey, IDC).
- Industry reports from recognized bodies.
- Books from established authors via reputable publishers.

### Tier 3 — Useful but verify
- Wikipedia (use as a *starting point* — never as a citation; chase the underlying source).
- Industry blogs from known brands (Stripe blog, GitHub engineering, etc.).
- Conference talks and podcasts (great for ideas; verify specifics).

### Tier 4 — Use with caution
- Vendor-sponsored research (often methodology is biased toward the vendor's product).
- Press releases (the company's framing — find a second source).
- Social media posts, even from experts (verify specifics elsewhere).

### Tier 5 — Don't cite, but can spark leads
- AI-generated summaries (use only to find primary sources — never as a citation).
- SEO content farms.
- Forum threads (Reddit, HN — fine for surfacing perspectives, not as evidence).

---

## 2. The Research Workflow

### Step 1 — Define what you actually need
Before researching, ask:
- What specific question does the user need answered?
- What level of evidence does the piece require? (A blog post needs less rigor than a whitepaper.)
- Are there constraints? (e.g., date range, region, sample size.)

Vague research requests waste time. "Find stats on remote work" → unclear. "Remote work productivity studies from the last 5 years with sample sizes >1,000" → actionable.

### Step 2 — Go to primary sources first
- For statistics: government datasets (BLS, Census, Eurostat), international bodies (OECD, World Bank, WHO), academic databases (Google Scholar, PubMed for medical).
- For industry data: trade associations, regulator reports, public SaaS company filings (10-Ks, earnings calls).
- For technical claims: official documentation, RFCs, standards bodies.

### Step 3 — Verify each claim with at least 2 sources
- Find the original. If a stat is widely cited, find where it originated — secondary citations often mangle the original.
- A claim x2 sources ≠ 2x as reliable. Look for *independent* corroboration (not 2 articles citing the same study).

### Step 4 — Note the limitations
- Sample size (n=30 ≠ n=3,000).
- Methodology (self-reported survey vs. observed behavior).
- Population studied (US college students ≠ global workforce).
- Date (a 2018 stat about remote work has limited relevance in 2025).
- Funding source (industry-funded studies skew toward industry conclusions).

### Step 5 — Synthesize, don't stack
- ❌ "Study A says X. Study B says X. Study C says X." (Stack)
- ✅ "Three independent studies converge on X — though they differ on magnitude. Study A found 20% improvement; Study B, 15%; Study C, 35%. The variation likely reflects methodology: A used self-report, while B and C observed behavior." (Synthesis)

---

## 3. Fact-Checking Workflow

When asked to fact-check a claim:

1. **Restate the claim precisely.** "Productivity drops 50% when remote" → vague. Restate: "Remote workers are 50% less productive than office workers, per [source]."
2. **Find the source.** Where did the claim originate?
3. **Check the original.** Did it actually say what's claimed? Common distortions:
   - Correlation reported as causation.
   - Findings generalized beyond the studied population.
   - Stat reported out of context (e.g., "200% increase" without baseline).
   - Stat is outdated.
4. **Look for the counter-evidence.** What studies, data, or arguments contradict it?
5. **Surface what's uncertain.** If the evidence is mixed, say so. Don't cherry-pick.

### Output format for fact-checks
```
Claim: [Restated precisely]

Verdict: [Confirmed / Partly supported / Contradicted / Unverifiable]

What we found:
- [Source 1] (Tier 1/2/3): [what it actually says, with link or citation]
- [Source 2]: [what it says]

What's uncertain:
- [Limitations and gaps]

Bottom line:
[1–2 sentence honest summary]
```

---

## 4. Statistics — Special Care Required

Statistics are the most-mangled content type. Watch for these:

| Distortion | Example |
|---|---|
| **Missing baseline** | "Revenue grew 300%!" (From $1K to $4K.) |
| **Cherry-picked window** | "Stocks rose 20% in Q3" (after falling 40% in Q2). |
| **Out-of-date stat cited as current** | "86% of Americans have smartphones" (from a 2014 study, now >95%). |
| **Survey ≠ observed behavior** | "70% of workers say they're more productive remote" (self-report, not measured). |
| **Misleading average** | "Average salary is $200K" (median is $80K; a few outliers skew). |
| **Causation from correlation** | "Ice cream sales correlate with shark attacks" (both rise in summer). |
| **Survivorship bias** | "Dropouts make great entrepreneurs" (we only see the ones who succeeded). |

### What to cite with a stat
- The source (organization + report/study name).
- The year.
- The sample size and methodology (if known).
- The original page or section.

### What to do when the stat can't be verified
- Say so. "This statistic is widely cited but I could not locate a primary source."
- Don't make up a number to fill the gap. Find a different stat or state the qualitative claim.

---

## 5. Synthesis Without Plagiarism

- **Paraphrase with attribution.** "As [Source] found, [paraphrased claim]." Don't copy sentence structure or unique phrasing.
- **Quote sparingly.** Direct quotes only when the original phrasing is itself the point. Quote <5% of any piece.
- **Cite as you go**, not as a stack at the end. Inline links or footnotes.
- **Synthesis is additive.** Add your interpretation, comparison, or framework — don't just aggregate others' takes.

---

## 6. Citation Standards

### Inline (web/blogosphere standard)
- Hyperlink the source on the relevant phrase: "according to [BLS data](url)."
- Name the source in the text: "A 2024 Stanford study found…"
- For data: include year and sample where relevant: "A 2024 Stanford study (n=2,500) found…"

### Footnotes (whitepapers, formal writing)
- Numeric footnotes at the bottom of the page or end of the doc.
- Include: author, title, publisher/site, year, URL, access date.

### When to cite
- Anytime you state a fact that isn't common knowledge or your own original analysis.
- Anytime you quote directly.
- Anytime you paraphrase someone's specific argument.
- When in doubt, cite. Over-citing is a minor flaw; under-citing is plagiarism or misinformation.

### When NOT to cite
- Common knowledge ("The Earth orbits the Sun").
- Your own original observations or arguments.
- The user's own data (with their permission).

---

## 7. Research Output Templates

### Topic summary
```
**The question:** [What we set out to answer]
**TL;DR:** [1–3 sentences — the answer]

**Key findings:**
1. [Finding] — [Source, tier, year]
2. [Finding] — [Source, tier, year]
3. [Finding] — [Source, tier, year]

**Where sources disagree:**
- [Disagreement] — [Why it likely varies]

**What's uncertain / unknown:**
- [Gaps in the research]

**Best sources to cite in the final piece:**
- [Source 1]: [Why it's strongest]
- [Source 2]: [Why]
```

### Statistics gathering
```
**Topic:** [e.g., "remote work productivity statistics"]

**Stat 1:** [The number, with full context]
- Source: [Org + report name]
- Year: [Year]
- Tier: [1/2/3]
- Methodology: [Survey/observation/etc. + sample size]
- Notes: [Caveats — date, region, population studied]
- URL: [Direct link]

[Repeat per stat]

**Recommended use:**
[Which 2–3 stats are most credible and useful for the user's piece, and why]
```

### Fact-check result
(See Section 3 above.)

---

## 8. Research Pitfalls

- ❌ **Citing the first result.** Quality research often lives on page 2–3 of search, in PDFs, or in databases.
- ❌ **Citing AI summaries as sources.** Use them to find primary sources, not as the citation.
- ❌ **Treating all sources as equal.** A peer-reviewed study ≠ a vendor blog.
- ❌ **Cherry-picking.** Surface the evidence that contradicts your thesis, not just the evidence that supports it.
- ❌ **Confirmation bias in search.** Don't only search terms that will confirm what you want to find. Search the counter-arguments too.
- ❌ **Outdated statistics.** Average age of a cited stat matters — for fast-moving fields, prefer last 2–3 years.
- ❌ **Misrepresenting methodology.** A self-reported preference ≠ an observed behavior. State which.
- ❌ **Uncited paraphrasing.** Even if you reworded it, credit the original — and add your own synthesis.
- ❌ **Inflating certainty.** If the evidence is mixed or limited, say so. "% overstate confidence" is a common error.

---

## 9. When Research Isn't Possible

Be honest with the user about what you can and can't do:
- If you can't access credible sources for a claim, say so and recommend where they could look.
- If a widely-cited statistic has no traceable primary source, flag it.
- If the evidence is genuinely mixed, present the strongest version of each side and let the user pick the framing.
- Don't fabricate a stat to fill a gap. The piece is better with an honest "this is hard to measure" than a fake number.
