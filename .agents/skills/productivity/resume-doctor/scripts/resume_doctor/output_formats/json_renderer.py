"""
JSON Renderer — Canonical ResumeData serialization.

Outputs the complete structured data for API integration, programmatic use, or as source of truth.
"""
import json
from pathlib import Path
from typing import List, Dict, Any

from resume_doctor.models.resume_data import ResumeData
from resume_doctor.output_formats import BaseRenderer, OutputFormat


class JSONRenderer(BaseRenderer):
    """Render ResumeData to JSON (canonical format)."""

    format = OutputFormat.JSON
    extension = ".json"

    def render(self, resume: ResumeData) -> str:
        """Serialize ResumeData to pretty JSON."""
        return resume.to_json(indent=2)

    def get_instructions(self, resume: ResumeData) -> str:
        name = resume.contact.name or "Your Name"
        return f"""# How to Use Your JSON Resume

## Overview
The `{name.lower().replace(' ', '_')}_resume.json` file is the **canonical structured representation** of your resume — the single source of truth that all other formats are derived from.

## Quick Start
```bash
# View structure
cat resume.json | jq .

# Extract specific sections
cat resume.json | jq '.experience'
cat resume.json | jq '.skills.categories[].skills[].name'
```

## Programmatic Access

### Python
```python
import json
from resume_doctor.models.resume_data import ResumeData

# Load from file
with open('resume.json') as f:
    data = json.load(f)

resume = ResumeData.from_dict(data)

# Access structured data
print(resume.contact.name)
print(resume.contact.email)
for exp in resume.experience:
    print(f"{exp.role} at {exp.company}")
    for bullet in exp.bullets:
        print(f"  - {bullet}")

# Get all keywords for ATS
keywords = resume.get_all_keywords()
print(f"Total keywords: {{len(keywords)}}")
```

### JavaScript/TypeScript
```javascript
import resumeData from './resume.json' assert {{ type: 'json' }};

console.log(resumeData.contact.name);
console.log(resumeData.experience.map(e => e.role));

// React component example
function ResumeSection({{ data }}) {{
  return (
    <section>
      <h1>{{data.contact.name}}</h1>
      <p>{{data.contact.headline}}</p>
      {{data.experience.map(exp => (
        <article key={{exp.company + exp.role}}>
          <h3>{{exp.role}} at {{exp.company}}</h3>
          <ul>
            {{exp.bullets.map((bullet, i) => (
              <li key={{i}}>{{bullet}}</li>
            ))}}
          </ul>
        </article>
      ))}
    </section>
  );
}}
```

## API Integration

### Submit to Job Boards
```python
import requests

with open('resume.json') as f:
    payload = json.load(f)

# Transform to job board API format
ats_payload = {{
    "personal_info": {{
        "name": payload["contact"]["name"],
        "email": payload["contact"]["email"],
        "phone": payload["contact"]["phone"],
        "location": payload["contact"]["location"],
        "links": [{{"label": l["label"], "url": l["url"]}} for l in payload["contact"]["links"]],
    }},
    "summary": payload["summary"],
    "experience": [
        {{
            "title": exp["role"],
            "company": exp["company"],
            "location": exp["location"],
            "start_date": exp["start_date"],
            "end_date": exp["end_date"],
            "description": exp["description"],
            "bullets": exp["bullets"],
        }}
        for exp in payload["experience"]
    ],
    "skills": [
        skill["name"]
        for cat in payload["skills"]["categories"]
        for skill in cat["skills"]
    ],
    "education": payload["education"],
    "certifications": payload["certifications"],
}}

response = requests.post(
    "https://api.jobboard.com/v1/resumes",
    json=ats_payload,
    headers={{"Authorization": "Bearer YOUR_TOKEN"}}
)
```

### Feed to LLM for Cover Letters
```python
import openai

with open('resume.json') as f:
    resume = json.load(f)

prompt = f\"\"\"
Write a tailored cover letter for this candidate applying to {{job_description}}.

Candidate Profile:
- Name: {{resume['contact']['name']}}
- Headline: {{resume['contact']['headline']}}
- Summary: {{resume['summary']}}
- Key Skills: {{', '.join(s['name'] for c in resume['skills']['categories'] for s in c['skills'][:10])}}
- Recent Roles:
{{chr(10).join(f\"  - {{exp['role']}} at {{exp['company']}} ({{exp['date_range']}})\" for exp in resume['experience'][:3])}}
- Key Achievements:
{{chr(10).join(f\"  - {{bullet}}\" for exp in resume['experience'][:3] for bullet in exp['bullets'][:2])}}
\"\"\"

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{{"role": "user", "content": prompt}}]
)
```

## Schema Reference
The JSON follows the `ResumeData` schema:
```json
{{
  "contact": {{
    "name": "string",
    "headline": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "links": [{{"label": "string", "url": "string", "icon": "string?"}}]
  }},
  "summary": "string",
  "skills": {{
    "categories": [
      {{
        "name": "string",
        "skills": [
          {{"name": "string", "category": "string", "proficiency": "string?", "years_experience": "number?", "keywords": "string[]"}}
        ],
        "description": "string"
      }}
    ],
    "summary": "string"
  }},
  "experience": [
    {{
      "role": "string",
      "company": "string",
      "location": "string",
      "start_date": "string",
      "end_date": "string",
      "description": "string",
      "bullets": "string[]",
      "technologies": "string[]",
      "metrics": "string[]",
      "signal_tags": "string[]",
      "nda_level": "L0|L1|L2|L3|L4"
    }}
  ],
  "projects": [...],
  "education": [...],
  "certifications": [...],
  "meta": {{
    "target_role": "string",
    "target_company": "string",
    "ats_keywords": {{"keyword": "density"}},
    "signal_tags": "string[]",
    "nda_level": "L0|L1|L2|L3|L4",
    "mode": "ats-max|designer-polish",
    "created_at": "ISO8601",
    "updated_at": "ISO8601",
    "source_format": "string"
  }}
}}
```

## Validation
```bash
# Validate against schema (if using JSON Schema)
pip install jsonschema
python -c "
import json, jsonschema
with open('resume.json') as f: data = json.load(f)
with open('schemas/resume-data.json') as f: schema = json.load(f)
jsonschema.validate(data, schema)
print('✓ Valid')
"
```

## Conversion Pipeline
The JSON is the **source of truth** — all other formats are derived from it:

```
resume.json (canonical)
    │
    ├── resume-doctor build --format latex  → main.tex
    ├── resume-doctor build --format markdown → resume.md
    ├── resume-doctor build --format html   → resume.html
    ├── resume-doctor build --format docx   → resume.docx
    └── resume-doctor build --format pdf    → resume.pdf
```

## Version Control
```bash
# Track changes meaningfully
git add resume.json
git commit -m "feat: Added React 18 + Next.js 14 to skills; updated metrics for Acme Corp role"

# Diff shows exactly what changed
git diff resume.json
```

## Companion Files
- `resume.md` — Human-editable Markdown (round-trippable)
- `resume.html` — Web-ready HTML
- `latex/main.tex` — Overleaf-ready LaTeX
- `docx/resume.docx` — Word format for recruiters
- `pdf/resume.pdf` — Final distribution PDF
- `validation-report.json` — Quality gates (all should PASS)
- `job-analysis.json` — Target job requirements
- `gap-report.md` / `keyword-injection-map.json` — Audit trail

## Next Steps
- **Tailor for another job**: `resume-doctor tailor --resume resume.json --job <url> --format json`
- **Export any format**: `resume-doctor build --resume resume.json --format <latex|markdown|html|docx|pdf>`
- **Validate**: `resume-doctor ats-audit --resume resume.json --format json`
"""


from resume_doctor.output_formats import RendererRegistry
RendererRegistry.register(OutputFormat.JSON, JSONRenderer)