"""
LaTeX Builder — Compiles optimized .tex to PDF + extracted text artifacts.

Public API:
    build_resume(latex, job_analysis, mode) -> BuildResult
"""
from dataclasses import dataclass, asdict
import subprocess
import os
import json
from pathlib import Path
from datetime import datetime


@dataclass
class BuildResult:
    success: bool
    pdf_path: str
    txt_path: str
    normalized_txt_path: str
    docx_path: str
    compilation_log: str
    pdflatex_exit_code: int
    warnings: list[str]
    errors: list[str]
    page_count: int


def build_resume(latex: str, job_analysis: str, mode: str = "designer-polish",
                 output_dir: str = None, base_name: str = None) -> BuildResult:
    """Compile LaTeX → PDF → text extraction pipeline"""

    if output_dir is None:
        output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    if base_name is None:
        with open(job_analysis) as f:
            job = json.load(f)
        company = job.get('company', 'company').replace(' ', '-').lower()
        role = job.get('role_title', 'role').replace(' ', '-').lower()
        base_name = f"{company}-{role}-{datetime.now().strftime('%Y%m%d')}"

    tex_path = os.path.join(output_dir, f"{base_name}.tex")
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
    txt_path = os.path.join(output_dir, f"{base_name}.txt")
    normalized_txt_path = os.path.join(output_dir, f"{base_name}.normalized.txt")
    docx_path = os.path.join(output_dir, f"{base_name}.docx")

    # Write .tex file
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(latex)

    # Run pdflatex (2 passes for cross-refs)
    log = ""
    warnings = []
    errors = []
    exit_code = 0

    for pass_num in range(1, 3):
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex_path],
            cwd=output_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        log += f"\n=== PASS {pass_num} ===\n{result.stdout}\n{result.stderr}"
        exit_code = result.returncode

        if result.returncode != 0:
            errors.append(f"pdflatex pass {pass_num} failed: {result.stderr[:500]}")
            break

    if exit_code == 0 and os.path.exists(pdf_path):
        # Extract text with layout preservation
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, txt_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            warnings.append(f"pdftotext failed: {result.stderr}")
        else:
            # Create normalized version
            normalized = normalize_for_parsing(read_file(txt_path))
            with open(normalized_txt_path, 'w', encoding='utf-8') as f:
                f.write(normalized)

        # Generate DOCX fallback via pandoc
        try:
            subprocess.run(
                ['pandoc', tex_path, '-o', docx_path],
                capture_output=True,
                timeout=30
            )
        except (subprocess.SubprocessError, FileNotFoundError):
            warnings.append("pandoc not available — DOCX fallback not generated")

        # Count pages
        try:
            result = subprocess.run(
                ['pdftotext', pdf_path, '-'],  # stdout
                capture_output=True,
                text=True,
                timeout=10
            )
            page_count = result.stdout.count('\f') + 1
        except:
            page_count = 1

        # Collect warnings from log
        log_path = os.path.join(output_dir, f"{base_name}.log")
        if os.path.exists(log_path):
            log_text = read_file(log_path)
            if 'Overfull' in log_text:
                warnings.append("Overfull hbox warnings present")
            if 'Missing character' in log_text:
                warnings.append("Missing character warnings (Unicode glyphs)")

        success = True
    else:
        success = False
        pdf_path = ""
        txt_path = ""
        normalized_txt_path = ""
        docx_path = ""
        page_count = 0

    return BuildResult(
        success=success,
        pdf_path=pdf_path,
        txt_path=txt_path,
        normalized_txt_path=normalized_txt_path,
        docx_path=docx_path if os.path.exists(docx_path) else "",
        compilation_log=log,
        pdflatex_exit_code=exit_code,
        warnings=warnings,
        errors=errors,
        page_count=page_count
    )


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def normalize_for_parsing(text: str) -> str:
    """NFKC + ligature/bullet/dash normalization for parser fidelity"""
    import unicodedata
    import re

    text = unicodedata.normalize('NFKC', text)
    ligatures = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for k, v in ligatures.items():
        text = text.replace(k, v)
    text = re.sub(r'[•‣▶◆◀◦▪▫●○✓✔➡\-–—*●]+', '-', text)
    text = re.sub(r'[–—]', '--', text)
    return text


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--mode", default="designer-polish")
    parser.add_argument("--out-dir", default="output")
    parser.add_argument("--name", default=None)
    args = parser.parse_args()

    latex = Path(args.resume).read_text()
    result = build_resume(latex, args.job, args.mode, args.out_dir, args.name)

    print(json.dumps(asdict(result), indent=2))
    if not result.success:
        exit(1)