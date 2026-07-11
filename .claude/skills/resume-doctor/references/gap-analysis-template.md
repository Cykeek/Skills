---
name: gap-analysis-template
description: Structured template for comparing candidate profile against job requirements — skills, experience, keywords, education, and cultural fit.
---

# Gap Analysis Template — Deep Reference

**Purpose:** Systematic comparison of candidate inventory vs. job requirements. Outputs prioritized remediation plan for resume tailoring.

---

## 1. Input Schemas

### 1.1 Job Requirements (from `job-analysis.json`)

```yaml
job_requirements:
  must_have:
    hard_skills: [Figma, Design Systems, React, TypeScript, A/B Testing]
    soft_skills: [Cross-functional Leadership, Ambiguity Navigation, Stakeholder Management]
    tools: [Figma, Jira, Mixpanel, Looker, Git]
    domain_knowledge: [Payments, KYC/AML, PCI-DSS]
    years_experience: "5+"
    education: "Bachelor's Design/HCI/CS or equivalent"
  nice_to_have:
    hard_skills: [iOS/Android, Motion Design, SQL, Python, Node.js]
    certifications: [Pragmatic Marketing, CUxD, AWS]
    domain: [B2B SaaS, Marketplace, Developer Tools]
  keyword_targets:
    design systems: {min: 2.0, max: 3.5, priority: critical}
    a/b testing: {min: 1.5, max: 3.0, priority: high}
    stakeholder: {min: 1.0, max: 2.5, priority: high}
    figma: {min: 1.5, max: 3.0, priority: high}
    payments: {min: 1.0, max: 2.0, priority: medium}
    cross-functional: {min: 1.0, max: 2.0, priority: medium}
    prototyping: {min: 0.5, max: 1.5, priority: medium}
    accessibility: {min: 0.5, max: 1.5, priority: medium}
```

### 1.2 Candidate Profile (master inventory)

```yaml
candidate_profile:
  name: "Maya Chen"
  headline: "Senior Product Designer — FinTech & Design Systems"
  total_years: 7
  target_roles: ["Senior Product Designer", "Staff Product Designer"]
  skills:
    hard_skills: [Figma, Design Systems, Prototyping, User Research, A/B Testing, Accessibility, Design Tokens]
    soft_skills: [Cross-functional Leadership, Stakeholder Management, Mentorship, Design Ops]
    tools: [Figma, FigJam, Jira, Linear, Mixpanel, Amplitude, Looker, Git, GitHub, Storybook, Zeroheight, Notion, Miro, Dovetail]
    domain_knowledge: [E-commerce, Marketplace, B2B SaaS, Design Systems]
    technical: [React, TypeScript, HTML/CSS, Tailwind, Storybook, Design Tokens, CI/CD, GraphQL]
  experience:
    - company: "Stripe"
      role: "Senior Product Designer (Lead)"
      dates: "07/2022 – Present"
      bullets: [...]
    - company: "Airbnb"
      role: "Product Designer"
      dates: "07/2020 – 06/2022"
      bullets: [...]
    - company: "Early-Stage Startup"
      role: "Founding Designer"
      dates: "01/2018 – 06/2020"
      bullets: [...]
  education:
    - degree: "M.S. Human-Computer Interaction"
      school: "Stanford University"
      years: "2018–2020"
    - degree: "B.S. Design Engineering"
      school: "University of Washington"
      years: "2014–2018"
  certifications:
    - "Certified Usability Analyst (CUA) — Human Factors International, 2021"
    - "AWS Certified Cloud Practitioner — 2023"
  projects:
    - name: "Unified Billing Dashboard"
      context: "Internal Platform"
      dates: "01/2023 – 06/2023"
      role: "Lead Designer (3D, 2E, 1PM, 1R)"
      stack: [Figma, Storybook, React, BigQuery]
      signals: ["Systems Thinking", "0→1 Ambiguity", "Cross-functional Leadership"]
```

---

## 2. Gap Categories & Scoring

| Category | Weight | Severity Scale |
|----------|--------|----------------|
| **Hard Skills** | 30% | Critical (missing must-have) / High (missing nice-to-have) |
| **Tools/Technologies** | 20% | High / Medium |
| **Domain Knowledge** | 15% | High / Medium |
| **Keyword Density** | 20% | Critical (below min) / Medium (above max) |
| **Experience Years** | 10% | High (gap > 2yr) / Medium (gap 1-2yr) |
| **Education** | 5% | Medium / Low |

**Severity Rank:** Critical > High > Medium > Low

---

## 3. Gap Analysis Output: `gap-report.md`

```markdown
# Gap Analysis Report — Maya Chen → Stripe Senior Product Designer

**Generated:** 2024-01-15 | **Job Source:** Greenhouse #123456 | **Candidate:** Maya Chen

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Overall Match** | 78% |
| **Critical Gaps** | 2 |
| **High Gaps** | 3 |
| **Medium Gaps** | 4 |
| **Estimated Fix Time** | 45-60 min |

---

## Detailed Gap Matrix

### 🔴 Critical Gaps (Must Fix Before Apply)

| # | Category | Job Requires | Candidate Has | Gap | Remediation |
|---|----------|--------------|---------------|-----|-------------|
| 1 | Hard Skill | **React** | ❌ Not listed | Missing core technical fluency | Add "React" to Technical Skills; inject in 2 bullets (Stripe DS migration, Checkout prototypes) |
| 2 | Keyword Density | **design systems** ≥ 2.0% | Current: 0.8% (1 mention) | -1.2% density | Add "design systems" to Summary (+1), Skills (+1), 2 Experience bullets (+2) = 4 total → ~2.1% |

---

### 🟠 High Gaps (Strongly Recommended)

| # | Category | Job Requires | Candidate Has | Gap | Remediation |
|---|----------|--------------|---------------|-----|-------------|
| 3 | Hard Skill | **TypeScript** | ❌ Not listed | Missing | Add to Technical Skills; mention in Stripe DS bullet ("TypeScript migration") |
| 4 | Domain | **Payments / KYC / AML** | E-commerce, Marketplace | Partial match | Reframe Stripe Checkout as "payments infrastructure"; add "PCI-DSS compliance" to bullets |
| 5 | Keyword Density | **figma** ≥ 1.5% | Current: 0.6% (1 mention) | -0.9% | Add to Summary, Skills, 2 bullets = 4 total |
| 6 | Keyword Density | **a/b testing** ≥ 1.5% | Current: 0.4% (0 mentions) | -1.1% | Add to Summary, Skills, 2 bullets = 3 total |

---

### 🟡 Medium Gaps (Nice to Have)

| # | Category | Job Requires | Candidate Has | Gap | Remediation |
|---|----------|--------------|---------------|-----|-------------|
| 7 | Tool | **Jira** | Linear, GitHub | Partial | Add "Jira" to Tools; mention in Airbnb bullet |
| 8 | Keyword Density | **stakeholder** ≥ 1.0% | Current: 0.3% | -0.7% | Add to 2 bullets (cross-functional leadership) |
| 9 | Keyword Density | **cross-functional** ≥ 1.0% | Current: 0.5% | -0.5% | Add to 1 bullet |
| 10 | Certification | **AWS** (nice-to-have) | ✅ Has | — | Already covered |

---

## Remediation Priority Queue

| Priority | Action | Files to Edit | Est. Time |
|----------|--------|---------------|-----------|
| 1 | Add React + TypeScript to Technical Skills | `main.tex` Skills section | 2 min |
| 2 | Inject "design systems" in Summary, Skills, 2 bullets | `main.tex` Summary, Skills, Experience | 10 min |
| 3 | Inject "figma" in Summary, Skills, 2 bullets | `main.tex` Summary, Skills, Experience | 8 min |
| 4 | Reframe Stripe bullets for payments/KYC | `main.tex` Experience (Stripe) | 12 min |
| 5 | Inject "a/b testing" in Summary, Skills, 2 bullets | `main.tex` Summary, Skills, Experience | 8 min |
| 6 | Add "stakeholder" to 2 bullets | `main.tex` Experience | 5 min |

---

## Keyword Injection Map (Exact Locations)

| Keyword | Target Count | Current | Locations to Add |
|---------|--------------|---------|------------------|
| design systems | 4 | 1 | Summary, Skills, Stripe bullet 2, Airbnb bullet 2 |
| figma | 4 | 1 | Summary, Skills, Stripe bullet 1, Airbnb bullet 1 |
| a/b testing | 3 | 0 | Summary, Skills, Stripe bullet 3 |
| react | 2 | 0 | Skills, Stripe bullet 2 |
| typescript | 2 | 0 | Skills, Stripe bullet 2 |
| payments | 2 | 1 | Stripe bullet 1, Summary |
| stakeholder | 2 | 0 | Stripe bullet 4, Airbnb bullet 3 |
| cross-functional | 2 | 1 | Stripe bullet 4, Projects section |

---

## Reframing Suggestions (Domain Gap)

| Current Framing | Target Framing | Signal Activated |
|-----------------|----------------|------------------|
| "checkout redesign" | "payments infrastructure checkout redesign" | Payments domain |
| "design system migration" | "design system migration (React/TypeScript, PCI-DSS compliant)" | Technical fluency + Domain |
| "host onboarding" | "marketplace onboarding (KYC-adjacent identity verification)" | Domain proximity |
| "billing dashboard" | "enterprise billing dashboard (PCI-DSS scope)" | Domain + Compliance |

---

## Validation Checklist (Post-Edit)

- [ ] All Critical gaps resolved
- [ ] All High gaps resolved or documented with rationale
- [ ] Keyword densities within [min, max] for all targets
- [ ] No keyword stuffing (>5% any single keyword)
- [ ] All must-have hard skills present in Skills section
- [ ] All must-have tools present in Skills section
- [ ] Domain keywords appear in Summary + ≥2 Experience bullets
- [ ] Signal tags match target role requirements
- [ ] ATS validation passes (format, sections, dates, bullets)