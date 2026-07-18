"""Pytest fixtures and configuration for content-writer tests."""
import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_md_file():
    """Create a temporary markdown file for testing."""
    def _create(content: str) -> str:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name
    return _create


@pytest.fixture
def clean_md_file():
    """A clean markdown file without lint issues."""
    return """# Clean Document

This is a clean document. It has no banned patterns or robotic tells.

The content flows naturally and uses contractions where appropriate.
It's well-structured and reads like a human wrote it.

## Section One

Here's a paragraph with concrete examples. You'll find it reads naturally.

## Section Two

Another section with varied sentence structures. Short. Medium length sentences. And longer ones that flow naturally with multiple clauses.

## Takeaway

The key takeaway is clear and actionable.
"""


@pytest.fixture
def dirty_md_file():
    """A markdown file with various lint issues."""
    return """# Dirty Document

In today's world, it is important to understand that AI is changing everything.

In order to leverage the power of AI, you must utilize the latest tools.
Moreover, furthermore, you should facilitate the integration of these systems.

It is important to note that you cannot simply ignore this trend.
The landscape is evolving rapidly.

As we all know, it is important to understand the landscape.

The system utilizes AI to facilitate the process. It leverages machine learning.
Moreover, it facilitates better outcomes.

We cannot emphasize this enough. You will not believe the results.
It is not optional; it is essential.
"""


@pytest.fixture
def em_dash_content():
    """Content with various em dash scenarios."""
    return """# Em Dash Test

This is a sentence with an em dash — which should be flagged.

Another sentence — with em dash in the middle.

Code block with em dash:
```python
# This is a comment — should not be flagged
print("Hello — world")
```

Quoted text with em dash:
> "This is a quote — from a source" — Author Name

Reference text with em dash:
[1] Smith, J. "Title — subtitle" Journal 2023.

Regular text — with em dash again.
"""


@pytest.fixture
def sample_landing_page():
    """A well-structured landing page template."""
    return """# Build docs your team actually reads.

Notion for product teams who hate Notion.

Trusted by 2,000+ teams

## What you get

### Faster onboarding
New hires find answers in seconds, not hours. Search across all your docs, specs, and decisions in one place.

### Fewer meetings
Async updates replace status syncs. Your team stays aligned without another calendar invite.

### Better decisions
Every decision lives with its context. No more "why did we choose this?" six months later.

## The objection you're afraid to ask

"Isn't this just another wiki?" No — it's a decision log. Wikis rot; decisions compound.

## How it works

Connect your tools. Import existing docs. Start writing decisions, not just docs.

Start free trial
"""


@pytest.fixture
def sample_email():
    """A well-structured marketing email."""
    return """Subject: Your churn report in 5 minutes
Preheader: Stop exporting CSVs. Get insights automatically.

Hi {{first_name}},

Your welcome email is killing signups. Here's the fix.

Most teams bury the value prop in paragraph three. We'll show you how to move it to the subject line and first sentence.

- 3 subject line formulas that worked for 50+ SaaS companies
- The one sentence that doubles open rates
- A template you can use today

Start writing better emails

Cheers,
Sarah

P.S. The template library is free forever. Grab it here.
"""


@pytest.fixture
def sample_case_study():
    """A well-structured case study with metrics."""
    return """# How Acme cut reporting time 90% with ReportAI

## The customer

Acme Corp, a 200-person fintech company processing $50M in transactions monthly.

## The problem

- Manual reporting took 6 hours per week
- Data lived in 5 different tools
- Errors meant re-running reports daily

## Why they chose ReportAI

Evaluated 4 alternatives. Chose ReportAI for native SQL integration and SOC2 compliance.

## The solution

Connected all 5 data sources in 2 days. Built 12 automated reports. Trained the team in one afternoon.

## The results

- Reporting time: 6 hours → 30 minutes per week (90% reduction)
- Error rate: 15% → 0.2%
- Team reclaimed 20+ hours/month for analysis

## In their words

"ReportAI paid for itself in week one. We finally have time for actual analysis."
— Sarah Chen, Head of Analytics

## What's next

Building predictive alerts for anomaly detection.

[Book a demo]
"""


@pytest.fixture
def sample_comparison_page():
    """A well-structured comparison page."""
    return """# Tool A vs Tool B: which is right for you?

TL;DR: Tool A wins for teams needing deep integrations. Tool B wins for simple, fast setup.

## At a glance

| Feature | Tool A | Tool B |
|---|---|---|
| Integrations | 50+ | 10 |
| Setup time | 2 hours | 15 minutes |
| Price | $49/mo | $19/mo |
| API access | Full | Limited |

## Tool A

### Who it's for
Teams with complex workflows needing deep integrations.

### Pros
- 50+ native integrations
- Full API access
- Advanced workflows

### Cons
- Longer setup
- Higher price

## Tool B

### Who it's for
Small teams wanting quick setup.

### Pros
- 15-minute setup
- Lower price
- Simple UI

### Cons
- Limited integrations
- No API access

## Recommendation by use case

- If you need deep integrations, go with Tool A.
- If you need fast setup, go with Tool B.
- If you need both, consider Tool C: here's why.

## How we evaluated

Tested both tools with a 5-person team over 2 weeks using real workflows.
"""


@pytest.fixture
def sample_blog_post():
    """A well-structured blog post."""
    return """# Your best customers are the ones who complain. Here's why.

Most companies ignore complaints. The smart ones mine them for gold.

## The problem with ignoring complaints

Every complaint is a feature request in disguise. When a customer complains, they're telling you exactly what's broken.

## How to mine complaints

Set up a system to categorize every support ticket. Tag by feature, severity, and frequency.

## The payoff

One SaaS company found 40% of their roadmap came from support tickets. Their NPS jumped 20 points in six months.

## Takeaway

Don't silence complaints. Systematize them. Your roadmap will thank you.

[Read the full case study →]
"""


# ===== Persuasion Framework Fixtures =====

@pytest.fixture
def pas_content():
    """PAS framework content for pain-aware audience."""
    return """Every month, you spend 6 hours manually compiling reports from three different tools.

That's 72 hours a year. Hours your team could spend on actual analysis instead of data entry. And every hour spent copying data is an hour you're not catching the trends that matter.

ReportAI connects to your existing tools and generates a unified dashboard in one click. No more copy-paste. No more manual reconciliation.
"""


@pytest.fixture
def bab_content():
    """BAB framework content for transformation."""
    return """Before Acme, our support team spent 45 minutes per ticket writing responses from scratch.

Now, they respond in under 5 minutes per ticket. Customer satisfaction is up 30%. The team handles 2x the volume with the same headcount.

Acme's AI draft engine learns your team's tone and creates a personalized response in seconds. The agent reviews, tweaks, and hits send.
"""


@pytest.fixture
def aida_content():
    """AIDA framework content for long-form sales."""
    return """You're losing customers 2 days before they churn.

I see this with every SaaS at $50-200 MRR. The warning signs are sitting in your data, but most teams don't know what to look for.

Teams using Predictor see an average 40% reduction in churn within 60 days. Here's how one B2B SaaS cut churn from 7.2% to 4.1% in one quarter.

Start your free trial. No credit card required. Cancel anytime.
"""


@pytest.fixture
def fab_content():
    """FAB framework content for technical buyers."""
    return """**Feature:** 256-bit AES encryption

**Advantage:** Your data is encrypted both in transit and at rest.

**Benefit:** So even if there's a breach, your customer data is unreadable. You'll sleep better at night.
"""


@pytest.fixture
def storybrand_content():
    """StoryBrand framework content."""
    return """You're the hero. You had a Problem: fragmented data across five tools.

You met a Guide who gave you a Plan: connect everything in one dashboard.

You took Action. Now you avoid the Failure of missed insights and end in Success with unified visibility.
"""


@pytest.fixture
def four_u_scores():
    """Content for testing 4U scoring."""
    return {
        "high_urgent": "Your trial ends tomorrow. Here's how to keep your data.",
        "high_unique": "We fix the problem your last 3 agencies couldn't.",
        "high_useful": "Cut reporting time from 6 hours to 30 minutes.",
        "high_ultra_specific": "Reduce churn from 7.2% to 4.1% in 60 days.",
        "low_all": "We provide quality service for your business needs.",
    }


# ===== Style Guide Fixtures =====

@pytest.fixture
def high_contraction_content():
    """Content with ~80% contraction usage."""
    return """You'll love this. It's simple and it works. You can't go wrong.
We've tested it extensively. It doesn't break. You won't regret it.
They're happy. We're confident. It's the best choice.
"""


@pytest.fixture
def low_contraction_content():
    """Content with ~20% contraction usage (too formal)."""
    return """You will love this. It is simple and it works. You cannot go wrong.
We have tested it extensively. It does not break. You will not regret it.
They are happy. We are confident. It is the best choice.
"""


@pytest.fixture
def uniform_sentence_content():
    """Content with uniform sentence structure (all start with 'The')."""
    return """The system requires authentication. The user must provide a valid token.
The tokens expire after 24 hours. The user can refresh them using the endpoint.
The documentation explains the process. The examples show the code.
"""


@pytest.fixture
def varied_sentence_content():
    """Content with varied sentence structure."""
    return """The system requires authentication via a valid token.
Tokens expire after 24 hours — but don't worry, you can refresh them using the endpoint.
Here's how it works. The documentation explains the process with clear examples.
"""


@pytest.fixture
def high_hedging_content():
    """Content with high hedging density (>2 hedges per paragraph)."""
    return """It seems like this might possibly work. Perhaps it could be useful.
We think it may help. It appears to be effective. There's a chance it might solve the problem.

This could potentially be the solution you're looking for. It's probably going to work.
"""


@pytest.fixture
def low_hedging_content():
    """Content with low hedging density."""
    return """This works. It solves the problem. You'll see results in week one.
The data proves it. No guesswork needed.
"""


@pytest.fixture
def voice_drift_content():
    """Content with voice drift (starts human, becomes corporate)."""
    return """Hey there! You're going to love this. It's super simple and it just works.

The system architecture utilizes a microservices-based infrastructure
leveraging containerized deployments for optimal scalability.
Furthermore, the platform facilitates seamless integration capabilities.

Anyway, give it a shot — you won't regret it!
"""


@pytest.fixture
def consistent_voice_content():
    """Content with consistent voice throughout."""
    return """Hey there! You're going to love this. It's super simple and it just works.

The system runs on microservices in containers, so it scales without you
lifting a finger. And it plugs into your existing tools in minutes.

Anyway, give it a shot — you won't regret it!
"""


# ===== Template structure validation fixtures =====

@pytest.fixture
def incomplete_landing_page():
    """Landing page missing required sections."""
    return """# Headline
Subhead

## What you get

### Benefit 1
Details

### Benefit 2
Details

[CTA]
"""


@pytest.fixture
def incomplete_email():
    """Email missing required elements."""
    return """Subject: Test

Hi there,

Here's some content.

Thanks,
Team
"""


@pytest.fixture
def incomplete_case_study():
    """Case study missing metrics section."""
    return """# How Customer Succeeded

## The customer
Details

## The problem
Details

## The solution
Details

## In their words
"Quote"

[CTA]
"""


@pytest.fixture
def incomplete_comparison_page():
    """Comparison page missing required sections."""
    return """# A vs B

## At a glance

| Feature | A | B |
|---|---|---|
| X | Y | Z |

## A
Details

## B
Details
"""


# ===== Fix mode test fixtures =====

@pytest.fixture
def fixable_content():
    """Content with issues that --fix should resolve."""
    return """In today's world, it is important to understand that you cannot ignore this.

In order to utilize the system, you must leverage the API.
Furthermore, it is important to note that you do not have a choice.
"""


@pytest.fixture
def expected_fixed_content():
    """Expected output after --fix."""
    return """Today, understand that you can't ignore this.

To use the system, you must use the API.
Also, note that you don't have a choice.
"""