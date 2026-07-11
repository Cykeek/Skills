---
name: optimization-patterns
description: Bullet rewriting patterns, keyword injection strategies, density calibration, section reordering, and ATS validation recipes.
---

# Optimization Patterns — Deep Reference

**Purpose:** Battle-tested transformations for converting weak resume content into ATS-optimized, recruiter-compelling narratives.

---

## 1. Bullet Rewriting Patterns (STAR/CAR → Optimized)

### 1.1 Pattern Library

| Pattern | Before | After | Signal Tag |
|---------|--------|-------|------------|
| **Scope + Metric** | Worked on checkout redesign | **Led** checkout redesign for **15M+ merchants**: **+9pp conversion (18%→27%)**, **$460K ARR** | `Data-Informed Iteration` |
| **Technical Fluency** | Collaborated with engineers | **Pair-programmed React/TypeScript** components with **2 E5 engineers**; cut handoff **3.2 days→0.8 days** | `Technical Fluency` |
| **Systems Thinking** | Built design system components | **Architected Design System v2** token architecture: **12 teams, 87% UI coverage, 0 breaking changes in 18mo** | `Systems Thinking` |
| **0→1 Ambiguity** | Designed new features | **Defined 0→1 product strategy** for B2B marketplace (Series A, $12M): **IA, design language, component library from scratch** | `0→1 Ambiguity` |
| **Cross-functional Leadership** | Worked with PMs and engineers | **Directed 3D/2E/1PM** through **quarterly roadmap prioritization** (RICE); **established design review rituals** adopted org-wide | `Cross-functional Leadership` |
| **User Research Rigor** | Did user research | **Established JTBD research practice**: **52 interviews/year**, insights logged in Dovetail, **directly informed 3 product pivots** | `User Research Rigor` |
| **Mentorship & Culture** | Mentored junior designers | **Mentored 2 junior designers → both promoted within 18mo**; created **design critique framework** adopted by 8 teams | `Mentorship & Culture` |
| **Accessibility Advocacy** | Made things accessible | **Championed WCAG 2.2 AA compliance**: audited **240 components**, **trained 15 engineers**, **reduced a11y bugs 78%** | `Accessibility Advocacy` |
| **Strategic Influence** | Presented to leadership | **Authored design strategy memo** adopted by **VP Product**; shifted **Q3 roadmap** to prioritize **enterprise billing** ($2.1M ARR) | `Strategic Influence` |

### 1.2 Verb Tier Enforcement

```
TIER 1 (Leadership):    Spearheaded, Orchestrated, Directed, Championed, Pioneered, Established, Architected
TIER 2 (Execution):     Delivered, Built, Designed, Developed, Implemented, Launched, Shipped, Reduced, Increased, Cut, Accelerated
TIER 3 (Support):       Assisted, Supported, Helped, Participated, Contributed, Worked on  ← REWRITE TO TIER 2
```

**Rule:** Every bullet must start with Tier 1 or Tier 2 verb. Zero Tier 3 allowed.

---

## 2. Keyword Injection Strategies

### 2.1 Placement Priority Matrix

| Section | Must-Have Keywords | Nice-to-Have | Max Density |
|---------|-------------------|--------------|-------------|
| **Professional Summary** | Top 3-5 critical | 1-2 | 3-5% each |
| **Core Competencies / Skills** | ALL (categorized) | ALL | N/A (list format) |
| **Experience (Current Role)** | Top 5-8 | 3-5 | 2-3% each |
| **Experience (Prior Roles)** | Top 3-5 | 2-3 | 1-2% each |
| **Projects** | 1-2 per project | 1-2 | 1-2% each |

### 2.2 Injection Techniques

#### A. Summary Injection (Natural Flow)
```
BEFORE: Senior Product Designer with 7 years building FinTech and B2B SaaS products.
AFTER:  Senior Product Designer with 7 years building **FinTech** and **B2B SaaS** products at scale. 
        Led **design systems** adoption across 12 teams (87% coverage, 0 breaking changes in 18mo). 
        Drove **+9pp activation** via checkout redesign validated through **A/B testing** (n=24k, p<0.01). 
        Fluently collaborate with **React/TypeScript** engineers; ship production prototypes in **Storybook**.
```

#### B. Bullet Injection (Contextual)
```
BEFORE: - Led checkout redesign for 15M+ merchants delivering +9pp activation
AFTER:  - **Spearheaded** checkout redesign for **15M+ merchants** delivering **+9pp activation (18%→27%)**, 
        **$460K ARR retained**; validated via **A/B test** (n=24,847, p<0.01, holdout confirmed) 
        [`Data-Informed Iteration` `Cross-functional Leadership`]
```

#### C. Skills Section Injection (Exact Match)
```
BEFORE: - Design Tools: Figma, Sketch, Principle
AFTER:  - **Design:** Product Design, **Design Systems**, Design Operations, User Research (JTBD, Usability), 
        Prototyping (Figma, React, Framer), **Accessibility (WCAG 2.2 AA)**, **A/B Testing**, Analytics (Mixpanel, Looker)
```

#### D. Variant Coverage (Semantic Expansion)
| Primary Keyword | Variants to Include |
|-----------------|---------------------|
| `design systems` | "design system", "component library", "design tokens", "Storybook", "Zeroheight" |
| `a/b testing` | "experimentation", "split testing", "statistical significance", "p-value", "holdout" |
| `figma` | "Figma", "FigJam", "DevMode", "auto layout", "components", "variants" |
| `accessibility` | "WCAG", "WCAG 2.2 AA", "screen reader", "keyboard navigation", "inclusive design" |

---

## 3. Density Calibration Algorithm

```python
def calculate_density(resume_text: str, keywords: list[str]) -> dict:
    words = resume_text.lower().split()
    total = len(words)
    results = {}
    for kw in keywords:
        # Count exact phrase occurrences
        count = resume_text.lower().count(kw.lower())
        # Density = (keyword_word_count * occurrences) / total_words * 100
        kw_words = len(kw.split())
        density = (count * kw_words / total) * 100
        results[kw] = {"count": count, "density": round(density, 2)}
    return results

def check_targets(density_results: dict, targets: dict) -> ValidationReport:
    issues = []
    for kw, target in targets.items():
        actual = density_results.get(kw, {"density": 0})["density"]
        if actual < target["min"]:
            issues.append(f"⚠️ {kw}: {actual}% (target ≥ {target['min']}%) — UNDER")
        elif actual > target["max"]:
            issues.append(f"⚠️ {kw}: {actual}% (target ≤ {target['max']}%) — OVER (stuffing risk)")
        else:
            issues.append(f"✅ {kw}: {actual}%")
    return ValidationReport(issues)

# Target bands (from job-analysis.json keyword_targets)
TARGETS = {
    "design systems": {"min": 2.0, "max": 3.5},
    "a/b testing": {"min": 1.5, "max": 3.0},
    "figma": {"min": 1.5, "max": 3.0},
    "stakeholder": {"min": 1.0, "max": 2.5},
    "react": {"min": 1.0, "max": 2.0},
    "typescript": {"min": 0.5, "max": 1.5},
}
```

### 3.3 Density Fix Commands

| Issue | Fix |
|-------|-----|
| **UNDER** (below min) | Add keyword to Summary (+1), Skills (+1), 1-2 Experience bullets (+1-2) |
| **OVER** (above max) | Replace exact matches with variants; remove from Skills if listed multiple times |
| **MISSING** (0 count) | Inject in Summary + Skills + 2 bullets minimum |

---

## 4. Section Reordering Rules

### 4.1 By Career Stage

| Stage | Order |
|-------|-------|
| **Entry (0-2 yr)** | Header → Summary → **Skills** → Projects → Education → Experience → Certifications |
| **Mid (3-7 yr)** | Header → Summary → **Skills** → Experience → Education → Certifications → Projects |
| **Senior (8+ yr)** | Header → Executive Summary → **Core Competencies** → Experience → Selected Achievements → Education → Board/Pubs |

### 4.2 By Target Role

| Role | Skills Position | Projects Position |
|------|-----------------|-------------------|
| **Engineering** | After Summary (critical) | After Experience (evidence) |
| **Design** | After Summary (tools matter) | After Experience (portfolio link) |
| **Product** | After Experience (contextual) | After Experience (outcomes) |
| **Data/AI** | After Summary (technical gate) | After Experience (methodology) |

**Rule:** Skills section must appear in top 1/3 of resume for ATS skills parsing.

---

## 5. ATS Validation Recipes (LaTeX)

### 5.1 Format Compliance Checklist (Hard Gates)

```python
def validate_latex_format(resume_tex: str) -> list[str]:
    issues = []
    if not resume_tex.startswith('\\documentclass'):
        issues.append("Missing documentclass")
    if '\\tabular' in resume_tex or '\\tabularx' in resume_tex:
        issues.append("Table detected — remove, use \\roleentry + \\hfill")
    if '\\includegraphics' in resume_tex or 'tikzpicture' in resume_tex:
        issues.append("Graphics/TikZ detected — remove")
    if 'fontspec' in resume_tex:
        issues.append("fontspec detected — use pdflatex + mathptmx only")
    if '\\documentclass{' in resume_tex and 'article' not in resume_tex:
        issues.append("Custom .cls file detected — use article class only")
    # Check for cmap + glyphtounicode before font packages
    cmap_pos = resume_tex.find('\\usepackage{cmap}')
    glyphtounicode_pos = resume_tex.find('\\input{glyphtounicode}')
    mathptmx_pos = resume_tex.find('\\usepackage{mathptmx}')
    if cmap_pos == -1 or glyphtounicode_pos == -1:
        issues.append("Missing cmap/glyphtounicode — required for Unicode extraction")
    if cmap_pos > mathptmx_pos or glyphtounicode_pos > mathptmx_pos:
        issues.append("cmap/glyphtounicode must appear BEFORE font packages")
    dates = re.findall(r'\\dates\{.*?(\d{2}/\d{4}\s*[–-]\s*(\d{2}/\d{4}|Present)).*?\}', resume_tex)
    if not dates:
        issues.append("No valid MM/YYYY date format found in \\dates{}")
    return issues
```

### 5.2 Parser Simulation (Greenhouse/Lever/Workday)

```bash
# Test with actual parsers (pdflatex pipeline)
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex  # 2nd pass for refs
pdftotext -layout main.pdf main.txt

# Check extracted text
grep -i "design systems" main.txt
grep -i "figma" main.txt
grep -i "react" main.txt
```

### 5.3 Readability Gates

| Metric | Threshold | Tool |
|--------|-----------|------|
| Flesch-Kincaid Grade | ≤ 12 | `textstat` |
| Avg Sentence Length | ≤ 20 words | `textstat` |
| Active Voice | ≥ 80% | `proselint` / manual |
| Passive Constructions | 0 | `proselint` |

---

## 6. Common Transformation Recipes

### 6.1 "Responsible for" → Action + Result

| Weak | Strong |
|------|--------|
| Responsible for design system | **Architected** design system v2: **240 components, 12 teams, 0 breaking changes** |
| Managed design team | **Directed** 3 designers → **2 promotions**; established **design review cadence** |
| Helped with user research | **Conducted** 12 usability studies; **synthesized** findings into **journey maps** driving **Q3 roadmap** |
| Worked on mobile app | **Delivered** 4.8★ iOS/Android app (**200K MAU**); **reduced** onboarding **45min→12min** |

### 6.2 Soft Skill → Behavioral Evidence

| Soft Skill Claim | Behavioral Bullet |
|------------------|-------------------|
| "Excellent communicator" | **Presented** design strategy to **VP Product**; secured **$200K budget** for design system migration |
| "Team player" | **Collaborated** with **3D/2E/1PM** through **weekly design reviews**; **resolved** 47 design→dev handoff issues |
| "Problem solver" | **Diagnosed** 40% drop-off at checkout step 3; **designed** progressive disclosure flow → **+23% completion** |
| "Fast learner" | **Self-taught React/TypeScript** in 6 weeks; **shipped** production prototypes in **Storybook** for 3 features |

### 6.3 NDA Project → Sanitized Case Study

| Constraint | Transformation |
|------------|----------------|
| Can't name client | "Fortune 100 FinTech" / "Series C B2B Payments Platform" |
| Can't share metrics | "~40% task time reduction (n=12, p<0.05)" / "directional improvement" |
| Can't show screens | Wireframe sketches + annotated flow diagram (recreated in Figma) |
| Full blackout | Process retrospective: "How we ran 0→1 discovery under NDA: method template" |

---

## 6.4 Audience-Aware Rewrite Patterns (HR / CEO / Lead Readable)

**Principle:** Every bullet must be understood by HR (keywords), CEO (business value), Hiring Manager (scope), and Technical Lead (proof) — in that order.

### 6.4.1 Pattern: Lead with Business Outcome
| Technical-Heavy | Audience-Balanced |
|-----------------|-------------------|
| Architected Design System v2 token architecture: 12 teams, 87% UI coverage, 0 breaking changes in 18mo | **Built unified design standards (Design System v2) adopted by 12 teams covering 87% of product UI — zero breaking changes in 18 months** [`Systems Thinking` `Technical Fluency`] |
| Spearheaded checkout redesign for 15M+ merchants delivering +9pp activation (18%→27%), $460K ARR retained; validated via A/B test (n=24,847, p<0.01) | **Led checkout redesign for 15+ million merchants, increasing completion rate by 9 percentage points (18% to 27%) and retaining $460K in annual revenue; proven through controlled experiment with 24,847 users** [`Data-Informed Iteration` `Cross-functional Leadership`] |
| Pair-programmed React/TypeScript components with 2 E5 engineers; cut handoff 3.2 days→0.8 days | **Collaborated directly with senior engineers to build production-ready components in React/TypeScript, reducing design-to-engineering handoff from 3.2 days to 0.8 days** [`Technical Fluency` `Cross-functional Leadership`] |

### 6.4.2 Pattern: Inline Technical Translation (First Mention)
| Acronym/Term | First-Mention Format | Subsequent Uses |
|--------------|---------------------|-----------------|
| A/B testing | "A/B testing (controlled experiments comparing two versions)" | "A/B testing" |
| Design system | "design system (unified design standards across products)" | "design system" |
| Design tokens | "design tokens (centralized design values like colors and spacing)" | "design tokens" |
| PCI-DSS | "PCI-DSS (payment security standard)" | "PCI-DSS" |
| WCAG 2.2 AA | "WCAG 2.2 AA (accessibility standard, level AA)" | "WCAG 2.2 AA" |
| JTBD | "JTBD (Jobs to Be Done — user needs research framework)" | "JTBD" |
| 0→1 | "0→1 (building from scratch)" | "0→1" |
| CI/CD | "CI/CD (automated testing and deployment)" | "CI/CD" |

### 6.4.3 Pattern: Scale Context for Non-Domain Experts
| Bare Number | With Context |
|-------------|--------------|
| 15M+ merchants | 15+ million merchants (payment processing scale) |
| 12 teams | 12 cross-functional product teams |
| 240 components | 240 reusable UI components |
| 52 interviews/year | 52 user interviews per year |
| 47→10 bugs/quarter | accessibility bugs reduced from 47 to 10 per quarter |
| $460K ARR | $460K in annual recurring revenue |
| n=24,847 | tested with 24,847 users |

### 6.4.4 Pattern: Replace Jargon with Plain Verbs
| Jargon Verb | Plain Verb | When to Use |
|-------------|------------|-------------|
| Architected | Built / Designed | Non-tech bullets, Summary |
| Orchestrated | Led / Coordinated | Cross-functional bullets |
| Spearheaded | Led / Drove | All contexts |
| Engineered | Built / Developed | Technical bullets |
| Implemented | Built / Launched | All contexts |
| Optimized | Improved / Made faster | All contexts |
| Refactored | Restructured / Cleaned up | Technical bullets |
| Migrated | Moved / Transitioned | All contexts |
| Prototyped | Built interactive mockups | All contexts |
| Synthesized | Combined / Organized | Research bullets |

### 6.4.5 Audience Check Checklist (Per Bullet)
Before finalizing each bullet, verify:
- [ ] **HR** can identify 1-2 keywords from job description
- [ ] **CEO** sees business outcome (revenue, users, risk, speed)
- [ ] **Hiring Manager** sees scope (team size, budget, timeline, users)
- [ ] **Technical Lead** sees method/proof (tools, metrics, statistical rigor)
- [ ] First technical term is translated inline
- [ ] Acronyms expanded at first use
- [ ] Numbers have context (not just "12" but "12 teams")

---

## 7. Versioning Strategy (LaTeX)

### 7.1 File Naming

```
main.tex                              # Master LaTeX source
main-{company}-{role}-{YYYYMMDD}.tex  # Tailored version per application
main-{company}-{role}-{YYYYMMDD}.pdf  # Submission artifact (pdflatex)
main-{company}-{role}-{YYYYMMDD}.txt  # Plain text fallback (pdftotext)
```

### 7.2 Master Update Protocol

```bash
# Quarterly refresh
1. Update metrics in main.tex (new numbers, new projects)
2. Refresh keyword taxonomies (new tools, frameworks)
3. Regenerate all tailored versions from main.tex
4. Re-validate against current ATS parsers
5. Archive old versions (git tag: resume-v{YYYYMMDD})
```

---

## 8. Quick Reference: Edit Commands (LaTeX)

```bash
# Inject keyword into LaTeX bullet
agent latex inject --file main.tex --bullet 3 --keyword "design systems" --after "Spearheaded"

# Replace weak verb in LaTeX
agent latex verb --file main.tex --bullet 5 --from "Worked on" --to "Spearheaded"

# Add metric to LaTeX bullet
agent latex metric --file main.tex --bullet 2 --append "+23% conversion (n=4,200, p<0.01)"

# Add signal tag to LaTeX bullet
agent latex signal --file main.tex --bullet 1 --tags "Systems Thinking,Cross-functional Leadership"

# Apply NDA abstraction
agent latex nda --file main.tex --level pattern-abstracted

# Apply audience-aware transforms
agent latex audience --file main.tex --expand-acronyms --translate-jargon --lead-with-outcome --add-scale-context

# Validate LaTeX
agent validate latex-format --resume main.tex
agent validate density --resume main.tex --job job-analysis.json
agent validate parsers --resume main.tex --parsers all
agent validate unicode-extraction --resume main.tex
agent validate readability --resume main.tex
agent validate audience --resume main.tex --job job-analysis.json
```

---

## 9. Anti-Patterns (Auto-Reject in Validation)

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Keyword density > 5% | `density_check` | Reduce, use variants |
| Same keyword 5× in one bullet | `bullet_scan` | Distribute across sections |
| Hidden text (white on white) | `pdf_inspect` | Never do this |
| Keywords only in footer/header | `section_check` | Move to body |
| Acronyms only (no spell-out) | `acronym_check` | "TypeScript (TS)" |
| Tables for skills | `table_check` | Use simple list |
| "I led" / "My team" | `pronoun_check` | Third-person implicit |