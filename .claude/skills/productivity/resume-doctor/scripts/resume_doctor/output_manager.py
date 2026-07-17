"""
Master output directory management for resume-doctor.

Every CLI command and Python module must call `ensure_master_output_dir()`
before writing any artifacts. This is idempotent and safe to call repeatedly.
"""

from pathlib import Path
from typing import Optional


MASTER_FOLDER_NAME = "resume-doctor-output"


def find_workspace_root(start: Optional[Path] = None) -> Path:
    """
    Locate the workspace root by walking up from `start` (default: cwd)
    looking for a .git directory. Falls back to current working directory.
    """
    current = (start or Path.cwd()).resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists():
            return parent
    # Fallback to project root if git not found
    return Path("D:/AI-Workflows")

def ensure_master_output_dir(workspace_root: Optional[Path] = None) -> Path:
    """
    Ensure the master output folder exists. Returns its path.

    Called by every CLI entry point and Python module before any file I/O.
    """
    root = find_workspace_root(workspace_root)
    master_dir = root / MASTER_FOLDER_NAME
    master_dir.mkdir(parents=True, exist_ok=True)
    return master_dir


def create_task_subfolder(
    master_dir: Path,
    task_type: str,
    resume_stem: str,
    job_stem: str,
    timestamp: str,
) -> Path:
    """
    Create a dated task subfolder under the master output directory.

    Args:
        master_dir: Path returned by `ensure_master_output_dir()`
        task_type: One of "ats-audit", "tailor", "review", "analyze", "build"
        resume_stem: Basename of resume file without extension (e.g., "main")
        job_stem: Basename of job source (e.g., "stripe-senior-pd" or "url_abc123")
        timestamp: ISO-like timestamp "YYYYMMDD_HHMMSS"

    Returns:
        Path to the created task subfolder.
    """
    folder_name = f"{task_type}_{resume_stem}__{job_stem}_{timestamp}"
    task_dir = master_dir / folder_name
    task_dir.mkdir(parents=True, exist_ok=True)
    return task_dir


def write_overleaf_instructions(task_dir: Path, mode: str = "designer-polish") -> Path:
    """
    Write the standard OVERLEAF_INSTRUCTIONS.md file to a task folder.

    Every task subfolder MUST contain this file.
    """
    content = f"""# How to Use Your Optimized Resume on Overleaf

## Quick Start (30 seconds)

1. **Open Overleaf:** Go to [https://www.overleaf.com](https://www.overleaf.com) and sign in (free account works).
2. **Create a blank project:** Click **"New Project"** → **"Blank Project"**. Name it (e.g., "My Resume - Stripe Senior PD").
3. **Replace `main.tex`:** In the left file panel, click `main.tex`, **delete all contents**, and **paste the entire contents of `main.tex` from this folder**.
4. **Recompile:** Click the green **"Recompile"** button (top-left). The PDF preview updates instantly.
5. **Download:** Click **"Download PDF"** from the toolbar to get your final resume.

> **No local LaTeX installation needed.** Overleaf runs TeX Live in the cloud. The `main.tex` here is self-contained—it includes all packages, fonts, and layout logic.

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `main.tex` | **← Copy this to Overleaf.** Your ATS-optimized, signal-tagged resume source. |
| `main.pdf` | Pre-compiled reference (identical to what Overleaf produces). |
| `main.txt` | Plain-text extraction via `pdftotext -layout`. **This is what ATS parsers actually see.** |
| `validation-report.json` | Machine-readable gate results. All 10 gates should show `"passed": true`. |
| `job-analysis.json` | Extracted keywords, density targets, company intel from the target posting. |
| `gap-report.md` | Human-readable audit of missing/weak keywords and where they were injected. |
| `keyword-injection-map.json` | Per-keyword injection plan (target density, locations, variants used). |
| `build-result.json` | Compilation metadata: exit code, page count, extraction rate, warnings. |
| `candidate-profile.yaml` | Your normalized skill taxonomy, experience years, NDA abstraction level. |
| `OVERLEAF_INSTRUCTIONS.md` | This file. |

---

## Understanding the Validation Report

Open `validation-report.json` and check `overall_passed: true`. The 10 gates:

| Gate | What It Checks | Target |
|------|----------------|--------|
| `latex_format` | Linear flow, cmap+glyphtounicode, T1/UTF8, no tables/columns | PASS |
| `keyword_density` | Each keyword within its min/max % range (critical 2-3.5%, high 1.5-3%, etc.) | PASS |
| `parser_simulation` | Greenhouse, Lever, Workday, iCIMS, Taleo all parse sections correctly | PASS |
| `unicode_extraction` | `pdftotext -layout` recovers ≥98% characters, ligatures resolved | PASS |
| `readability` | Flesch-Kincaid ≥30, Gunning Fog ≤14, avg sentence ≤25 words | PASS |
| `audience_comprehension` | HR (6s scan), Hiring Manager (30s), Tech Lead (credibility), Exec (business impact) | PASS |
| `metric_plausibility` | Numbers pass sanity checks (%/$, team size, timeline) | PASS |
| `single_role` | Resume targets one role level (no mixed seniority signals) | PASS |
| `summary_template` | Summary follows `[Role] + [Years] + [Domain] + [Top Metric] + [Signal Tag]` | PASS |
| `portfolio_crossref` | Portfolio links valid and cross-referenced to experience bullets | PASS |

---

## Layout Mode: `{mode}`

This resume was generated in **`{mode}`** mode:

| Property | `ats-max` | `designer-polish` |
|----------|-----------|-------------------|
| **Density** | Maximum (1.02 line stretch, tight margins) | Comfortable (1.08 line stretch, generous margins) |
| **Skills Position** | After Experience (ATS-first) | Top third (human scan) |
| **Signal Tags** | Inline `[Tag]` | Badged `\\signaltag{{Tag}}` (ATS-visible fallback) |
| **Typography** | System fonts only | `tgheros` (Helvetica-like) |
| **Color** | Monochrome | Semantic palette (muted, print-safe) |
| **Page Target** | 1 page (≤8 yr exp) | 2 pages max |

Both modes are **fully ATS-safe**: linear flow, Unicode extraction ≥98%, no tables/columns/graphics.

---

## Next Steps

- **Tailor for another job:**
  ```bash
  resume-doctor tailor --resume main.tex --job "https://jobs.company.com/..." --mode designer-polish
  ```
- **Update metrics:** Edit `\\metric{{...}}` commands in `main.tex` on Overleaf, then Recompile.
- **Switch mode:** Re-run with `--mode ats-max` for maximum density (1-page) or `--mode designer-polish` for visual polish (2-page).
- **Run a fresh ATS audit:** `resume-doctor ats-audit --resume main.tex`

---

*Generated by resume-doctor — your ATS-score-killing, Overleaf-ready resume agent.*
"""
    instructions_path = task_dir / "OVERLEAF_INSTRUCTIONS.md"
    instructions_path.write_text(content, encoding="utf-8")
    return instructions_path