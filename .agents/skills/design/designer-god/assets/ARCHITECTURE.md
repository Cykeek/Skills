# Product Designer Skill Architecture

## Overview

The Product Designer Skill provides a comprehensive CLI and programmatic interface for product design tasks including design reviews, problem framing, research planning, design briefs, critique templates, and design checklists.

## Component Structure

```
product-designer/
├── SKILL.md                    # Main skill documentation (≤500 lines)
├── scripts/
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # CLI entry point with argparse
│   ├── output_manager.py       # Output formatting (JSON/TEXT/TABLE)
│   ├── validators.py           # JSON schema validation
│   └── diagnostics.py          # Core diagnostic logic
├── schemas/
│   ├── design-review-request.json
│   ├── design-review-response.json
│   ├── problem-framing-request.json
│   ├── problem-framing-response.json
│   ├── research-plan-request.json
│   ├── research-plan-response.json
│   ├── design-brief-request.json
│   ├── design-brief-response.json
│   ├── critique-template.json
│   └── checklist.json
├── references/
│   ├── design-craft.md         # Visual design, interaction, IA, accessibility, systems, prototyping, emotional design, trust
│   ├── design-thinking.md      # Foundational principles, operating models, critique models, JTBD, design process
│   ├── design-templates.md     # Design brief, critique templates, research plans, handoff checklists, scope shaping
│   └── ux-research.md          # Research methods, JTBD interviews, usability testing, card sorting, tree testing, surveys, analytics
├── assets/
│   └── ARCHITECTURE.md         # This file
└── tests/
    └── test_contract.py        # Contract tests for all CLI commands
```

## Data Flow

### CLI Command Flow

```
User Input (CLI args)
       │
       ▼
┌──────────────────┐
│  argparse Parser │  (cli.py)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ OutputManager    │  (output_manager.py)
│ .set_format()    │
└────────┬─────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ Command Handlers (CLI class)           │
│ • cmd_design_review                    │
│ • cmd_problem_framing                  │
│ • cmd_research_plan                    │
│ • cmd_design_brief                     │
│ • cmd_critique_template                │
│ • cmd_checklist                        │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ ProductDesignerDiagnostics             │  (diagnostics.py)
│ • design_review()                      │
│ • problem_framing()                    │
│ • research_plan()                      │
│ • design_brief()                       │
│ • get_critique_template()              │
│ • get_design_checklist()               │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ Schema Validation (optional --validate)│  (validators.py)
│ • validate_request()                   │
│ • validate_response()                  │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│ OutputManager.output()                 │  (output_manager.py)
│ • _output_json()                       │
│ • _output_text()                       │
│ • _output_table()                      │
└────────┬───────────────────────────────┘
         │
         ▼
      STDOUT
```

### Programmatic Usage Flow

```python
from product_designer.diagnostics import ProductDesignerDiagnostics
from product_designer.output_manager import OutputManager, OutputFormat
from product_designer.validators import validate_response

# Initialize
diagnostics = ProductDesignerDiagnostics()
output = OutputManager(OutputFormat.JSON)

# Run diagnostic
result = diagnostics.design_review("Onboarding", "Mobile app", ["Activate users"])

# Optional validation
valid, errors = validate_response("design-review-response", result)

# Output
output.output(result)
```

## Core Classes

### OutputManager (output_manager.py)
- **Purpose**: Format-agnostic output rendering
- **Formats**: JSON (default), TEXT, TABLE
- **Methods**:
  - `set_format(format)` - Set output format (enum or string)
  - `output(data)` - Render data in current format
  - `error(message, code, details)` - Error output with exit
  - `success(message, data)` - Success output

### SchemaValidator (validators.py)
- **Purpose**: Validate JSON data against schemas without external dependencies
- **Features**:
  - Recursive object/array validation
  - Type checking (object, array, string, boolean, number)
  - Required field validation
  - Enum validation
  - Schema caching
- **Methods**:
  - `validate(schema_name, data)` → `(bool, errors[])`
  - `_load_schema(schema_name)` - Load and cache schema
  - `_validate_object(schema, data, path)` - Recursive validation

### ProductDesignerDiagnostics (diagnostics.py)
- **Purpose**: Core business logic for all design operations
- **Methods**:
  - `design_review(design, context, goals)` → Design review with breakdowns
  - `problem_framing(user, context, progress, evidence, assumptions)` → Problem frame
  - `research_plan(decision, goal, constraints)` → Research plan with method rationale
  - `design_brief(problem, user, constraints, scope)` → Complete design brief
  - `get_critique_template()` → Principled critique template with example
  - `get_design_checklist(type)` → Handoff/accessibility/trust checklists

### CLI (cli.py)
- **Purpose**: Command-line interface with argparse
- **Commands**: design-review, problem-framing, research-plan, design-brief, critique-template, checklist
- **Options**: --output (json/text/table), --validate
- **Validation**: Optional schema validation on responses

## JSON Schemas

All schemas are in `schemas/` directory following JSON Schema Draft 7:

| Schema | Description |
|--------|-------------|
| design-review-request.json | Input for design review |
| design-review-response.json | Output from design review |
| problem-framing-request.json | Input for problem framing |
| problem-framing-response.json | Output from problem framing |
| research-plan-request.json | Input for research plan |
| research-plan-response.json | Output from research plan |
| design-brief-request.json | Input for design brief |
| design-brief-response.json | Output from design brief |
| critique-template.json | Critique template structure |
| checklist.json | Checklist structure |

## Reference Files

The `references/` directory contains deep content read on-demand:

| File | Content |
|------|---------|
| design-craft.md | Visual design, interaction, IA, accessibility, systems, prototyping, emotional design, trust patterns |
| design-thinking.md | Principles, operating models, critique models, JTBD, design process, decision trees |
| design-templates.md | Design brief, critique templates, research plans, handoff checklists, scope shaping |
| ux-research.md | Research methods, JTBD interviews, usability testing, card sorting, tree testing, surveys, analytics |

## Testing

### Contract Tests (tests/test_contract.py)
- Tests all 6 CLI commands against their response schemas
- Tests all 3 output formats (json, text, table)
- Tests help command
- Runs with `--validate` flag to verify schema compliance

```bash
# Run from skill directory
python -m tests.test_contract
```

### Validation
```bash
# Test with validation
product-designer design-review --design "Test" --context "Web" --goals "Convert" --validate
```

## Extending the Skill

### Adding a New Command

1. Add method to `ProductDesignerDiagnostics` in `diagnostics.py`
2. Add command handler to `CLI` class in `cli.py`
3. Create request/response schemas in `schemas/`
4. Add test case in `tests/test_contract.py`
5. Run tests to verify

### Adding a New Reference File

1. Create `.md` file in `references/`
2. Add to SKILL.md Reference Files Index table
3. Reference in diagnostic methods via `reference_files` output field

## Quality Gates

1. **Schema Compliance** - All responses validate against JSON schemas
2. **Output Formats** - All commands support json/text/table
3. **Help Text** - All commands have descriptive help
4. **Contract Tests** - 8 tests covering all commands and formats
5. **Skill Architecture** - Follows Skill Authoring Standard v1.0.0

## Dependencies

- Python 3.8+
- Standard library only (json, argparse, sys, os, pathlib, typing, enum, subprocess)
- No external dependencies