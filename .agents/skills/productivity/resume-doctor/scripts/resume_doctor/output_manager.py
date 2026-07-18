"""
Master output directory management for resume-doctor.

Uses shared workspace_utils for workspace detection and standardized output folders.
Every CLI command and Python module should use `get_skill_output_dir()` and `create_task_dir()`.
"""

from pathlib import Path
from typing import Optional
import sys

# Add .agents/scripts to path for workspace_utils
SCRIPTS_DIR = Path(__file__).resolve().parents[5] / "scripts"
if SCRIPTS_DIR.exists():
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from workspace_utils import (
        get_workspace_root,
        get_skill_output_dir,
        create_task_dir,
    )
except ImportError:
    # Fallback for when workspace_utils is not available
    def get_workspace_root(start: Optional[Path] = None) -> Path:
        current = (start or Path.cwd()).resolve()
        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                return parent
        return Path("D:/AI-Workflows")

    def get_skill_output_dir(skill_name: str, workspace_root: Optional[Path] = None) -> Path:
        root = workspace_root or get_workspace_root()
        skill_dir = root / "outputs" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        return skill_dir

    def create_task_dir(skill_name: str, task_type: str, workspace_root: Optional[Path] = None, timestamp: Optional[str] = None) -> Path:
        from datetime import datetime
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        skill_dir = get_skill_output_dir(skill_name, workspace_root)
        safe_task_type = "".join(c if c.isalnum() or c in "-_" else "_" for c in task_type)
        task_dir = skill_dir / f"{safe_task_type}_{timestamp}"
        task_dir.mkdir(parents=True, exist_ok=True)
        return task_dir


# Backward compatibility aliases
MASTER_FOLDER_NAME = "resume-doctor-output"

def find_workspace_root(start: Optional[Path] = None) -> Path:
    """Locate the workspace root (deprecated: use workspace_utils.get_workspace_root)."""
    return get_workspace_root(start)

def ensure_master_output_dir(workspace_root: Optional[Path] = None) -> Path:
    """Ensure the master output folder exists (deprecated: use get_skill_output_dir)."""
    return get_skill_output_dir("resume-doctor", workspace_root)


def create_task_subfolder(
    master_dir: Path,
    task_type: str,
    resume_stem: str,
    job_stem: str,
    timestamp: str,
) -> Path:
    """
    Create a dated task subfolder under the master output directory.

    DEPRECATED: Use create_task_dir(skill_name, task_type) instead.
    This signature is kept for backward compatibility.
    """
    skill_dir = master_dir.parent if master_dir.name == "resume-doctor-output" else master_dir
    return create_task_dir("resume-doctor", task_type, timestamp=timestamp)


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