# Content Writer Skill Architecture

## Overview

The content-writer skill implements a **5-phase content creation pipeline** with **6 validation gates**, following the resume-doctor architecture pattern. It provides both a **CLI tool** (`content-writer`) and an **agent-callable Python package** for programmatic content generation, editing, linting, and validation.

---

## Visual Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           CONTENT WRITER SKILL ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   CLI Entry  │    │  Agent Entry │    │  Config File │    │  Brief File  │          │
│  │  (content-   │    │  (import     │    │  (.content-  │    │  (briefs/    │          │
│  │   writer)    │    │   package)   │    │   writer.yml)│    │   *.json)    │          │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘          │
│         │                   │                   │                   │                   │
│         └───────────────────┼───────────────────┼───────────────────┘                   │
│                             ▼                                                   │
│                    ┌─────────────────────┐                                        │
│                    │   Pipeline Orchestrator                                    │
│                    │   (ContentPipeline)                                        │
│                    └──────────┬────────────┘                                        │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                       │
│  │  Phase 1:   │      │  Phase 2:   │      │  Phase 3:   │                       │
│  │  Discover & │──────│  Outline    │──────│  Draft      │                       │
│  │  Align      │      │             │      │             │                       │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                       │
│         │                    │                    │                               │
│         ▼                    ▼                    ▼                               │
│  ┌─────────────────────────────────────────────────────────────┐                  │
│  │                    GATE 1: Brief Validation                 │                  │
│  │  (4 required fields present, valid goal/format, angle set) │                  │
│  └─────────────────────────────────────────────────────────────┘                  │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                       │
│  │  Phase 4:   │      │  Phase 5:   │      │  Phase 6:   │                       │
│  │  Revise     │──────│  Pre-Output │──────│  Present &  │                       │
│  │             │      │  Scan       │      │  Iterate    │                       │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                       │
│         │                    │                    │                               │
│         ▼                    ▼                    ▼                               │
│  ┌─────────────────────────────────────────────────────────────┐                  │
│  │                    GATE 2: Lint Validation                  │                  │
│  │  (em-dash ban, robotic tells, formal density, banned openers)                      │
│  └─────────────────────────────────────────────────────────────┘                  │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐                  │
│  │                    GATE 3: Structure Validation             │                  │
│  │  (format-specific sections present, grid parity, CTA exists)                    │
│  └─────────────────────────────────────────────────────────────┘                  │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐                  │
│  │                    GATE 4: SEO/Conversion Validation        │                  │
│  │  (keyword presence, meta tags, CTA verb hierarchy, trust signals)              │
│  └─────────────────────────────────────────────────────────────┘                  │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐                  │
│  │                    GATE 5: DEI/Accessibility Validation    │                  │
│  │  (inclusive language, readability, screen-reader safe)     │                  │
│  └─────────────────────────────────────────────────────────────┘                  │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐                  │
│  │                    GATE 6: Output Envelope Validation       │                  │
│  │  (agent mode: timestamp, format_version, data envelope)    │                  │
│  └─────────────────────────────────────────────────────────────┘                  │
│                               │                                                     │
│         ┌─────────────────────┼─────────────────────┐                              │
│         ▼                     ▼                     ▼                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                      │
│  │  CLI Output  │     │ Agent Output │     │  Artifacts   │                      │
│  │  (stdout/    │     │  (JSON env-  │     │  (briefs/,   │                      │
│  │   files)     │     │   elope)     │     │   reports/)  │                      │
│  └──────────────┘     └──────────────┘     └──────────────┘                      │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase Definitions

### Phase 1: Discover & Align (`DiscoverAlignPhase`)
**Purpose**: Establish the 4 clarifying questions before any writing begins.

**Inputs**: User request (string or brief file), optional template name
**Outputs**: `ContentBrief` object with all 6 fields populated

**Operations**:
1. Parse request for explicit audience, goal, format, tone
2. If missing, apply template defaults (blog, landing-page, email, social, case-study, whitepaper, press-release, video-script)
3. If still missing and interactive mode: prompt user for 4 questions
4. Infer angle from audience + goal + format
5. Validate brief completeness (Gate 1)

**Gate 1 Criteria**:
- ✅ All 4 required fields present (audience, goal, format, length, tone)
- ✅ Goal ∈ {educate, persuade, inform, entertain, convert, nurture, reassure, warn}
- ✅ Format ∈ {blog, landing-page, email, social, case-study, whitepaper, press-release, video-script}
- ✅ Angle inferred or provided
- ✅ Length parseable (word count or range)

---

### Phase 2: Outline (`OutlinePhase`)
**Purpose**: Structure before prose. Get user sign-off on structure for pieces >600 words.

**Inputs**: Validated `ContentBrief`
**Outputs**: `ContentOutline` object

**Operations**:
1. Select structure pattern from `content-frameworks.md` based on format
2. Generate working title + hook angle
3. Create section-by-section structure with key argument per section
4. Define CTA/takeaway
5. For long-form (>600 words): present outline for user approval before drafting

**Gate 2 Criteria** (Lint Validation):
- ✅ No em dashes (—) in body prose (code/quotes exempt)
- ✅ Robotic tell density < threshold (utilize, leverage, facilitate, moreover, furthermore)
- ✅ Formal phrase density < 0.5% (do not, will not, cannot, it is without contractions)
- ✅ No banned openers (In today's world, In this article, As we all know...)

---

### Phase 3: Draft (`DraftPhase`)
**Purpose**: Write the full piece following the outline and style guide.

**Inputs**: Approved `ContentOutline`, `ContentBrief`
**Outputs**: `ContentDraft` object

**Operations**:
1. Apply tone/voice rules from `style-guide.md` for target audience
2. Follow format-specific rules from `templates.md`
3. For SEO work: apply `seo-playbook.md` during drafting (not afterthought)
4. For persuasion: apply framework from `persuasion-frameworks.md`
5. For conversion: apply `conversion-copywriting.md` layers

---

### Phase 4: Revise (`RevisePhase`)
**Purpose**: The most important stage - apply senior editor's rubric.

**Inputs**: `ContentDraft`
**Outputs**: `RevisedDraft` object

**Operations** (in order):
1. **Structure**: Does the piece achieve its job? (format-specific)
2. **Clarity**: Can reader follow without re-reading?
3. **Concision**: Cut 10-20% of words (editing checklist)
4. **Voice**: Em dash audit (scan entire draft for "—"), grid parity check
5. **Mechanics**: Read aloud test, first sentence check, voice drift check

**Mandatory Pre-Output Scan** (Gate 3 - Structure):
- ✅ Em dash audit: zero "—" in body prose
- ✅ Grid parity: card body texts within 15 words, headings within 2-3 words
- ✅ First sentence: starts with reader's reality, not writer's context
- ✅ Voice drift: no paragraph sounds notably more formal/robotic

---

### Phase 5: Pre-Output Scan (`PreOutputScanPhase`)
**Purpose**: Final quality gates before presentation.

**Inputs**: `RevisedDraft`
**Outputs**: `FinalContent` object

**Gate 4 - SEO/Conversion Validation**:
- ✅ Target keyword in title, H1, first 100 words, one H2
- ✅ Meta title ≤ 60 chars, meta description ≤ 155 chars
- ✅ CTA verb matches commitment level (try > start > get > learn)
- ✅ Trust signals present (testimonials, logos, numbers, guarantees)

**Gate 5 - DEI/Accessibility Validation**:
- ✅ No gendered defaults (they/them, not he/she)
- ✅ No ableist language (crazy, insane, blind to, deaf to)
- ✅ Readability: Flesch-Kincaid ≥ 60 for consumer, ≥ 50 for technical
- ✅ Alt text placeholders for images

**Gate 6 - Output Envelope Validation** (Agent Mode):
- ✅ JSON envelope contains: timestamp, format_version, data
- ✅ Data field matches expected schema for content type

---

## CLI Command Mapping

```
content-writer
├── brief                         # Phase 1: Generate/validate content brief
│   ├── --interactive             # Prompt for 4 questions
│   ├── --template <name>         # Pre-fill from template
│   ├── --from-file <file>        # Load existing brief
│   ├── --audit-existing <file>   # Reverse-engineer brief from content
│   ├── --save <filename>         # Save to briefs/
│   ├── --json                    # JSON output (agent mode)
│   └── --non-interactive         # Fail if fields missing (CI)
│
├── lint                          # Gate 2: Lint content
│   ├── <files...>                # Files or directories to lint
│   ├── --strict                  # Exit 1 on any issue
│   ├── --fix                     # Apply automatic fixes
│   ├── --in-place                # Write fixes to files
│   ├── --json                    # JSON output
│   └── --quiet                   # Suppress text output
│
├── outline                       # Phase 2: Generate outline from brief
│   ├── --brief <file>            # Brief file path
│   ├── --format <format>         # Override format
│   └── --json                    # JSON output
│
├── draft                         # Phase 3: Generate draft from outline
│   ├── --brief <file>            # Brief file path
│   ├── --outline <file>          # Outline file path (optional)
│   ├── --framework <name>        # Persuasion framework (PAS, BAB, AIDA, etc.)
│   ├── --json                    # JSON output
│   └── --stream                  # Stream output (for long content)
│
├── revise                        # Phase 4: Apply revision checklist
│   ├── --content <file>          # Content file to revise
│   ├── --brief <file>            # Brief for context
│   ├── --check <1-5>             # Specific checklist phase (default: all)
│   ├── --json                    # JSON output
│   └── --dry-run                 # Show changes without applying
│
├── validate                      # Gates 3-6: Full validation pipeline
│   ├── --content <file>          # Content file
│   ├── --brief <file>            # Brief for context
│   ├── --gate <1-6>              # Specific gate (default: all)
│   └── --json                    # JSON output
│
├── seo                           # SEO-specific operations
│   ├── audit <file>              # SEO audit of content
│   ├── keywords <topic>          # Keyword research suggestions
│   ├── optimize <file>           # Apply on-page SEO
│   └── --json                    # JSON output
│
├── repurpose                     # Content repurposing
│   ├── --source <file>           # Source content
│   ├── --targets <formats...>    # Target formats (social, email, etc.)
│   ├── --json                    # JSON output
│   └── --calendar                # Generate 6-week repurposing calendar
│
└── test-auth                     # Test skill configuration
    └── --json                    # JSON output
```

---

## Dual Output Modes

### CLI Mode (Human-facing)
```bash
$ content-writer brief --template blog
# Output: Human-readable brief with colored sections
```

```json
// stdout (no envelope)
{
  "audience": "Senior engineers...",
  "goal": "educate",
  "format": "blog",
  "length": "1500 words",
  "tone": "confident, practical",
  "angle": "The one insight..."
}
```

### Agent Mode (Programmatic)
```python
from content_writer_skill import ContentPipeline
pipeline = ContentPipeline(agent_mode=True)
result = await pipeline.generate_brief(template="blog")
```

```json
// stdout (structured envelope)
{
  "timestamp": "2026-07-15T10:30:00Z",
  "format_version": "1.0",
  "data": {
    "audience": "Senior engineers...",
    "goal": "educate",
    "format": "blog",
    "length": "1500 words",
    "tone": "confident, practical",
    "angle": "The one insight...",
    "assumptions": ["Inferred length from blog template"]
  }
}
```

---

## Artifact Flow & Directory Structure

```
.agents/skills/content-writer/
├── ARCHITECTURE.md              # This file
├── SKILL.md                     # Agent behavior guide
├── pyproject.toml               # Package config
├── Makefile                     # Build/lint/test commands
├── content_writer_skill/        # Python package
│   ├── __init__.py              # Exports, version
│   ├── cli.py                   # CLI entry point (argparse)
│   ├── pipeline.py              # Pipeline orchestrator
│   ├── phases/
│   │   ├── __init__.py
│   │   ├── discover_align.py    # Phase 1
│   │   ├── outline.py           # Phase 2
│   │   ├── draft.py             # Phase 3
│   │   ├── revise.py            # Phase 4
│   │   └── pre_output_scan.py   # Phase 5
│   ├── validation.py            # Schema validation (jsonschema)
│   ├── output_manager.py        # CLI/Agent output formatting
│   ├── models/
│   │   ├── __init__.py
│   │   ├── brief.py             # ContentBrief dataclass
│   │   ├── outline.py           # ContentOutline dataclass
│   │   ├── draft.py             # ContentDraft dataclass
│   │   └── enums.py             # Goal, Format, Tone enums
│   └── lint/
│       ├── __init__.py
│       ├── rules.py             # Lint rule definitions
│       ├── engine.py            # Lint engine
│       └── fixes.py             # Auto-fix logic
├── schemas/                     # JSON Schema files
│   ├── content-brief.json
│   ├── content-outline.json
│   ├── content-draft.json
│   ├── lint-result.json
│   ├── seo-audit.json
│   └── validation-result.json
├── references/                  # Reference documentation (15 files)
│   ├── style-guide.md
│   ├── content-frameworks.md
│   ├── seo-playbook.md
│   ├── templates.md
│   ├── editing-checklist.md
│   ├── research-methodology.md
│   ├── reverse-engineering.md
│   ├── persuasion-frameworks.md
│   ├── dashboard-ux-writing.md
│   ├── dei-writing.md
│   ├── localization-checklist.md
│   ├── topic-clusters.md
│   ├── website-dashboard-playbook.md
│   ├── conversion-copywriting.md
│   ├── storytelling-frameworks.md
│   ├── content-repurposing.md
│   ├── ai-content-ethics.md
│   ├── master-index.md
│   └── quick-reference.md
├── templates/                   # Content templates (markdown)
│   ├── blog.md
│   ├── landing-page.md
│   ├── email.md
│   ├── social.md
│   ├── case-study.md
│   ├── whitepaper.md
│   ├── press-release.md
│   └── video-script.md
├── briefs/                      # Generated briefs (gitignored)
│   └── *.json
├── reports/                     # Validation reports (gitignored)
│   └── *.json
└── tests/                       # Contract tests
    ├── conftest.py
    ├── test_schemas.py
    ├── test_pipeline.py
    ├── test_phases/
    │   ├── test_discover_align.py
    │   ├── test_outline.py
    │   ├── test_draft.py
    │   ├── test_revise.py
    │   └── test_pre_output_scan.py
    ├── test_validation.py
    ├── test_output_manager.py
    ├── test_lint/
    │   ├── test_rules.py
    │   ├── test_engine.py
    │   └── test_fixes.py
    └── test_integration.py
```

---

## Validation Gates Summary

| Gate | Phase | Validates | Failure Action |
|------|-------|-----------|----------------|
| 1 | Discover & Align | Brief completeness, valid enums, angle present | Return to user for clarification |
| 2 | Outline | Lint rules (em-dash, robotic tells, formal density, banned openers) | Auto-fix or return for revision |
| 3 | Revise | Structure (sections, grid parity, CTA, first sentence, voice drift) | Return to Phase 3 (Draft) |
| 4 | Pre-Output | SEO/Conversion (keywords, meta, CTA hierarchy, trust signals) | Return to Phase 4 (Revise) |
| 5 | Pre-Output | DEI/Accessibility (inclusive language, readability, alt text) | Return to Phase 4 (Revise) |
| 6 | Pre-Output | Output envelope (agent mode: timestamp, format_version, data) | Wrap/envelope before output |

---

## Configuration

### `.content-writer.yml` (Project root or skill dir)
```yaml
# Content Writer Skill Configuration
version: "1.0"

# Default templates
default_template: "blog"
templates_dir: ".agents/skills/content-writer/templates"

# Lint configuration
lint:
  strict_mode: false
  em_dash_ban: true
  robotic_tell_threshold: 3
  formal_density_max_pct: 0.5
  banned_openers: true

# Output
output:
  default_format: "text"  # text, json, markdown
  agent_mode: false
  color: true

# Validation gates
gates:
  gate_1_brief: true
  gate_2_lint: true
  gate_3_structure: true
  gate_4_seo: true
  gate_5_dei: true
  gate_6_envelope: true

# Briefs directory
briefs_dir: ".agents/skills/content-writer/briefs"

# Reports directory
reports_dir: ".agents/skills/content-writer/reports"
```

---

## First Invocation Walkthrough

### CLI User Creates a Blog Post

```bash
$ content-writer brief --template blog --save my-brief.json
```

1. **Pipeline starts** → `DiscoverAlignPhase`
2. **Template applied** → Blog template fills audience, goal, format, length, tone
3. **Interactive prompts** → User answers 4 questions (audience, goal, format/length, tone)
4. **Angle inferred** → "The one insight that changes how [audience] approaches [topic]"
5. **Gate 1 passes** → Brief saved to `briefs/my-brief.json`
6. **Output** → Human-readable brief printed

```bash
$ content-writer outline --brief briefs/my-brief.json
```

1. **Pipeline starts** → `OutlinePhase`
2. **Structure selected** → Blog post structure from `content-frameworks.md`
3. **Outline generated** → Working title, hook, sections, CTA
4. **Gate 2 (lint)** → Outline text linted (no prose yet, minimal)
5. **Output** → Outline presented for approval

```bash
$ content-writer draft --brief briefs/my-brief.json --outline outline.json
```

1. **Pipeline starts** → `DraftPhase`
2. **Tone applied** → Professional + warm + conversational (blog default)
2. **Framework applied** → If `--framework PAS`, structure follows Problem-Agitate-Solution
3. **SEO integrated** → Keywords woven naturally per `seo-playbook.md`
4. **Gate 2 (lint)** → Draft linted in real-time
5. **Output** → Full draft

```bash
$ content-writer revise --content draft.md --brief briefs/my-brief.json
```

1. **Pipeline starts** → `RevisePhase`
2. **Checklist applied** → Structure → Clarity → Concision → Voice → Mechanics
3. **Em dash audit** → All "—" replaced with appropriate punctuation
4. **Grid parity** → Any feature grids balanced
5. **Gate 3 (structure)** → Sections present, CTA exists, first sentence reader-first
6. **Gate 4 (SEO)** → Keywords in title/H1/first100/H2, meta tags, CTA verb
7. **Gate 5 (DEI)** → Inclusive language, readability ≥ 60
8. **Output** → Final polished content

```bash
$ content-writer validate --content final.md --brief briefs/my-brief.json --json
```

1. **All gates re-run** → Comprehensive validation report
2. **Agent envelope** → JSON with timestamp, format_version, data
3. **Exit code** → 0 if all gates pass, 1 if any fail

---

## Integration with Agent Loop

When invoked as an agent skill:

```python
from content_writer_skill import ContentPipeline, OutputFormat

pipeline = ContentPipeline(
    agent_mode=True,
    output_format=OutputFormat.JSON,
    config_path=".content-writer.yml"
)

# Generate brief programmatically
brief = await pipeline.generate_brief(
    audience="Senior engineers evaluating observability tools",
    goal="educate",
    format="blog",
    length="1500 words",
    tone="confident, practical, slightly conversational"
)

# Full pipeline
result = await pipeline.run_full_pipeline(brief)
# result contains: brief, outline, draft, revised, final, validation_report
```

The agent receives structured JSON at each stage, enabling:
- Checkpointing/resuming long content generation
- Programmatic quality gates in CI/CD
- Integration with content management systems
- Multi-agent content workflows (writer → editor → SEO → publisher)

---

## Error Handling Strategy

| Error Type | Phase | Handling |
|------------|-------|----------|
| `ValidationError` (schema) | All | Return structured error with field path, expected type, received value |
| `LintError` (gate 2) | Outline/Draft | Auto-fix if `--fix`, else return issues with line/column |
| `StructureError` (gate 3) | Revise | Return missing sections, parity violations, first-sentence issues |
| `SEOValidationError` (gate 4) | Pre-Output | Return keyword gaps, meta tag issues, CTA hierarchy violations |
| `DEIValidationError` (gate 5) | Pre-Output | Return specific inclusive language violations, readability score |
| `EnvelopeError` (gate 6) | Pre-Output | Wrap output in agent envelope automatically |

All errors include:
- `code`: Machine-readable error code
- `message`: Human-readable description
- `field`/`line`/`column`: Location (where applicable)
- `suggestion`: Actionable fix recommendation

---

## Testing Strategy

### Contract Tests (Schema Validation)
- `test_schemas.py`: Every JSON schema validates against valid/invalid fixtures
- Golden files in `tests/fixtures/` for each schema

### Unit Tests (Phase Logic)
- `test_phases/test_discover_align.py`: Brief generation, template application, inference
- `test_phases/test_outline.py`: Structure selection, section generation
- `test_phases/test_draft.py`: Tone application, framework integration
- `test_phases/test_revise.py`: Checklist application, em-dash audit, grid parity
- `test_phases/test_pre_output_scan.py`: All 6 gate validations

### Integration Tests
- `test_integration.py`: Full pipeline runs (brief → outline → draft → revise → validate)
- CLI command integration via `subprocess`
- Agent mode envelope validation

### Lint Tests
- `test_lint/test_rules.py`: Each rule detects/fixed correctly
- `test_lint/test_engine.py`: File/directory scanning, exclusion logic
- `test_lint/test_fixes.py`: In-place fixes produce expected output

### Reference Tests (Existing)
- `test_frameworks.py`: Persuasion framework reference accuracy
- `test_style_guide.md`: Style guide rule documentation accuracy
- `test_templates.py`: Template structure validation
- `test_lint_content.py`: Legacy linter behavior preservation