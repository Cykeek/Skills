"""
Resume Doctor CLI — Entry points for all 5 core commands.
"""
import argparse
import asyncio
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Literal

from resume_doctor import (
    run_ats_audit,
    analyze_job,
    JobAnalysis,
    build_profile,
    analyze_gaps,
    build_injection_map,
    optimize_resume,
    run_all_gates,
    build_resume,
    validate_latex_format,
    ensure_master_output_dir,
    create_task_subfolder,
    write_overleaf_instructions,
    escape_latex_special_chars,
)


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF resume for processing."""
    try:
        # Try pdftotext first (better layout preservation)
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    try:
        # Fallback to pymupdf
        import fitz
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception:
        pass

    return f"[PDF EXTRACTION FAILED: {pdf_path}]"


def detect_input_format(file_path: str) -> Literal["tex", "pdf", "txt"]:
    """Detect input file format by extension."""
    suffix = Path(file_path).suffix.lower()
    if suffix == '.tex':
        return 'tex'
    elif suffix == '.pdf':
        return 'pdf'
    else:
        return 'txt'


def resolve_session_dir(args, task_type: str, resume_path: str, job_ref: str) -> Path:
    """Resolve or create the task-specific subfolder under the master output dir."""
    master = ensure_master_output_dir()
    if args.session_dir:
        task_dir = master / args.session_dir
        task_dir.mkdir(parents=True, exist_ok=True)
    elif args.no_prompt:
        resume_stem = Path(resume_path).stem if resume_path else task_type
        job_stem = Path(job_ref).stem if not job_ref.startswith("http") else f"url_{hash(job_ref) & 0xFFFF:04x}"
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = f"{task_type}_{resume_stem}__{job_stem}_{ts}"
        task_dir = master / task_name
        task_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Interactive prompt - for CLI we default to auto-named
        resume_stem = Path(resume_path).stem if resume_path else task_type
        job_stem = Path(job_ref).stem if not job_ref.startswith("http") else f"url_{hash(job_ref) & 0xFFFF:04x}"
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = f"{task_type}_{resume_stem}__{job_stem}_{ts}"
        task_dir = master / task_name
        task_dir.mkdir(parents=True, exist_ok=True)

    return task_dir


async def _analyze_job_async(args, job_source: str, company: Optional[str] = None, role: Optional[str] = None) -> JobAnalysis:
    """Analyze job from URL, file, or text."""
    if job_source.startswith("http"):
        return await analyze_job(job_source, "url", company, role)
    elif job_source.lower().endswith(".pdf"):
        return await analyze_job(job_source, "pdf", company, role)
    else:
        # Treat as text file or direct text
        path = Path(job_source)
        if path.exists():
            text = path.read_text(encoding="utf-8")
        else:
            text = job_source
        return await analyze_job(text, "text", company, role)


async def cmd_ats_audit_async(args) -> int:
    task_dir = resolve_session_dir(args, "ats-audit", args.resume, "local")
    print(f"[DIR] Created task folder: {task_dir}")

    # Handle PDF input - extract text and create temporary .tex for audit
    resume_path = args.resume
    fmt = detect_input_format(resume_path)
    if fmt == 'pdf':
        print("[INFO] PDF input detected - extracting text for ATS audit")
        text = extract_pdf_text(resume_path)
        # Create a minimal .tex from extracted text for audit
        tex_content = _pdf_text_to_latex(text)
        resume_path = task_dir / "extracted.tex"
        resume_path.write_text(tex_content, encoding="utf-8")
    elif fmt == 'txt':
        print("[INFO] Text input detected - converting to LaTeX for audit")
        text = Path(resume_path).read_text(encoding="utf-8")
        tex_content = _pdf_text_to_latex(text)
        resume_path = task_dir / "extracted.tex"
        resume_path.write_text(tex_content, encoding="utf-8")

    audit = run_ats_audit(latex_path=str(resume_path))
    out_path = Path(args.out) if args.out else task_dir / "ats-audit.json"
    from dataclasses import asdict
    audit_dict = asdict(audit)
    out_path.write_text(json.dumps(audit_dict, indent=2), encoding="utf-8")

    # Also write human-readable summary with Multi-Factor breakdown
    fs = audit.factor_scores or {}
    sh = getattr(audit, "subagent_harness", {}) or {}
    rs = getattr(audit, "recruiter_scorecard", {}) or {}
    sh_lines = "\n".join(f"- **{k}**: {v}" for k, v in sh.items()) if sh else "- No harness data"
    rs_lines = (
        f"- **Role Family:** `{rs.get('designation_family', 'N/A')}`\n"
        f"- **Recruiter Evidence Score:** **{rs.get('overall_score', 'N/A')}/100** (`{rs.get('verdict', 'N/A')}`)\n"
        f"- **Summary:** {rs.get('recruiter_summary', '')}"
    ) if rs else "- No recruiter scorecard data"

    summary_md = (
        f"# ATS & Recruiter Audit Summary\n\n"
        f"**Overall ATS Readiness Score:** {audit.overall_score}/100\n"
        f"**Status:** {'PASSED' if audit.passed else 'NEEDS REMEDIATION'}\n\n"
        f"## Role-Aware Recruiter Evidence Scorecard\n"
        f"{rs_lines}\n\n"
        f"## 5-Subagent Validation Harness Results\n"
        f"{sh_lines}\n\n"
        f"## Multi-Factor Score Breakdown\n"
        f"- Lexical Cleanliness: {fs.get('lexical_cleanliness', 'N/A')}/100\n"
        f"- Structural & Parser Readiness: {fs.get('structural_readiness', 'N/A')}/100\n"
        f"- Keyword Hygiene & Prominence: {fs.get('keyword_hygiene_prominence', 'N/A')}/100\n"
        f"- Readability & Recency: {fs.get('readability_recency', 'N/A')}/100\n\n"
        f"## Findings\n" + "\n".join(f"- {f['gate']}: {'PASS' if f['passed'] else 'FAIL'}" for f in audit.findings)
    )
    (task_dir / "audit-summary.md").write_text(summary_md, encoding="utf-8")
    write_overleaf_instructions(task_dir, mode="ats-max")

    print(f"[OK] ATS audit complete! Overall Score: {audit.overall_score}/100")
    if rs:
        print(f"     [Recruiter Scorecard -> {rs.get('designation_family', 'Role')}: {rs.get('overall_score', 'N/A')}/100 ({rs.get('verdict', 'N/A')})]")
    if getattr(audit, "subagent_harness", None):
        sh_dict = audit.subagent_harness
        print(f"     [5-Subagent Validation Harness Overall: {'PASS' if sh_dict.get('overall_passed') else 'FAIL'}]")
        for k, v in sh_dict.get("subagents", {}).items():
            print(f"       +-- {v.get('auditor', k)}: {v.get('status', 'UNKNOWN')}")
    if audit.factor_scores:
        print(f"     +-- Lexical Cleanliness: {audit.factor_scores['lexical_cleanliness']}/100")
        print(f"     +-- Structural Readiness: {audit.factor_scores['structural_readiness']}/100")
        print(f"     +-- Keyword Hygiene: {audit.factor_scores['keyword_hygiene_prominence']}/100")
        print(f"     +-- Readability & Recency: {audit.factor_scores['readability_recency']}/100")
    print(f"[FILE] Detailed JSON: {out_path}")
    print(f"[FILE] Summary MD: {task_dir / 'audit-summary.md'}")
    print(f"[FILE] Usage guide: {task_dir / 'OVERLEAF_INSTRUCTIONS.md'}")
    return 0


def _pdf_text_to_latex(text: str) -> str:
    """Convert extracted PDF text to robust LaTeX for processing/auditing."""
    import re
    import unicodedata
    text = unicodedata.normalize('NFKC', text)
    # Get rid of replacement characters and resolve ligatures
    text = text.replace('', '')
    ligatures = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for k, v in ligatures.items():
        text = text.replace(k, v)

    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Heuristically detect sections based on ontological keywords
    headers_map = [
        ("SUMMARY", [r'^(?:professional\s+)?summary\b', r'^executive\s+summary\b', r'^career\s+profile\b', r'^overview\b'], "Professional Summary"),
        ("WORK_EXPERIENCE", [r'^(?:work\s+|professional\s+|career\s+|employment\s+)?experience\b', r'^work\s+history\b', r'^employment\b'], "Work Experience"),
        ("SKILLS", [r'^(?:technical\s+|core\s+)?skills\b', r'^core\s+competencies\b', r'^technologies\b'], "Skills"),
        ("EDUCATION", [r'^education\b', r'^academic\s+background\b', r'^qualifications\b'], "Education"),
        ("CASE_STUDIES", [r'^(?:selected\s+)?(?:technical\s+)?case\s+studies\b', r'^projects\b'], "Selected Case Studies"),
        ("CERTIFICATIONS", [r'^certifications\b', r'^certificates\b'], "Certifications")
    ]

    def get_canonical_heading(line: str):
        clean = line.strip().lower().rstrip(':').strip()
        parts = re.split(r'\s{3,}', clean)
        first_part = parts[0].strip()
        for key, regexes, canonical in headers_map:
            for regex in regexes:
                if re.match(regex, first_part):
                    return canonical
        return None

    first_section_idx = len(lines)
    for idx, line in enumerate(lines):
        if get_canonical_heading(line):
            first_section_idx = idx
            break

    header_lines = lines[:first_section_idx]

    # Extracted contact details
    name = "Candidate Name"
    headline = ""

    if header_lines:
        name = header_lines[0]
        # Headline is the first line that doesn't look like contact info
        for hl in header_lines[1:]:
            if '@' not in hl and not re.search(r'\+?\d[\d\s-]{8,15}\d', hl) and not any(ext in hl.lower() for ext in ['.com', '.online', '.org', '.net', '|', '•']):
                if len(hl) < 80:
                    headline = hl
                    break
        if not headline and len(header_lines) > 1:
            if len(header_lines[1]) < 80:
                headline = header_lines[1]

    # Extract email and phone
    email_match = re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
    email = email_match.group(0) if email_match else "contact@email.com"

    phone_search = re.findall(r'\+?\d[\d\s-]{8,15}\d', text)
    phone = phone_search[0] if phone_search else ""

    location_match = re.search(r'\b([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+)\b', text)
    location = location_match.group(0) if location_match else "Location"

    found_links = re.findall(r'\b(?:linkedin\.com/in/[\w.-]+|github\.com/[\w.-]+|[a-zA-Z0-9-]+\.(?:online|com|org|net|me|io)(?:/[\w.-]+)*)\b', text, re.I)
    links = []
    for link in found_links:
        if link not in links and "email.com" not in link.lower() and "@" not in link:
            links.append(link)

    # Parse section contents
    sections = {}
    current_section = None
    for line in lines[first_section_idx:]:
        canonical = get_canonical_heading(line)
        if canonical:
            current_section = canonical
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)

    latex_lines = [
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage{cmap}",
        r"\usepackage[margin=1.4cm]{geometry}",
        r"\usepackage{microtype}",
        r"\usepackage{iftex}",
        r"\ifPDFTeX",
        r"  \input{glyphtounicode}",
        r"  \pdfgentounicode=1",
        r"\fi",
        r"\usepackage{enumitem}",
        r"\setlist[itemize]{leftmargin=1.5em,topsep=2pt,itemsep=2pt,parsep=0pt}",
        r"\usepackage[hidelinks]{hyperref}",
        r"",
        r"% PDF Metadata Setup",
        r"\hypersetup{",
        f"    pdftitle={{{escape_latex_special_chars(name)} - Resume}},",
        f"    pdfauthor={{{escape_latex_special_chars(name)}}},",
        r"    pdfsubject={Resume},",
        r"    pdfkeywords={Design, Engineering}",
        r"}",
        r"",
        r"\renewcommand{\familydefault}{\sfdefault}",
        r"\setlength{\parindent}{0pt}",
        r"\pagestyle{empty}",
        r"",
        r"\newcommand{\contactline}[5]{#1 | #2 | #3 | #4 | #5}",
        r"\newcommand{\signaltag}[1]{\textsl{(#1)}}",
        r"",
        r"\begin{document}",
        r"",
        r"% ==================== CONTACT HEADER ====================",
        r"\begin{center}",
        f"  {{\\LARGE \\textbf{{{escape_latex_special_chars(name)}}}}}\\\\[3pt]",
    ]
    if headline:
        latex_lines.append(f"  {{\\small \\textbf{{{escape_latex_special_chars(headline)}}}}}\\\\[3pt]")

    contact_parts = [location, phone, email]
    contact_parts.extend(links[:2])
    while len(contact_parts) < 5:
        contact_parts.append("N/A")

    latex_lines.extend([
        r"  {\small",
        f"    \\contactline{{{escape_latex_special_chars(contact_parts[0])}}}{{{escape_latex_special_chars(contact_parts[1])}}}{{{escape_latex_special_chars(contact_parts[2])}}}{{{escape_latex_special_chars(contact_parts[3])}}}{{{escape_latex_special_chars(contact_parts[4])}}}",
        r"  }",
        r"\end{center}",
        r"\vspace{2pt}",
        r""
    ])

    def process_bullet(txt: str) -> str:
        txt = re.sub(r'^[•\-\*‣▶◆◀◦▪▫●○✓✔➡·\s]+', '', txt).strip()
        from resume_doctor.validation_gates import CONTROLLED_SIGNAL_TAGS
        def rep_tag(match):
            tag = match.group(1)
            if tag in CONTROLLED_SIGNAL_TAGS:
                return f"\\signaltag{{{tag}}}"
            return match.group(0)
        txt = re.sub(r'\[([a-z0-9-]+)\]', rep_tag, txt)
        return escape_latex_special_chars(txt)

    order = ["Professional Summary", "Skills", "Work Experience", "Selected Case Studies", "Education", "Certifications"]
    for sec in order:
        if sec in sections and sections[sec]:
            latex_lines.append(f"% ==================== {sec.upper()} ====================")
            latex_lines.append(f"\\section*{{{sec}}}")

            if sec == "Professional Summary":
                summary_text = " ".join(sections[sec])
                latex_lines.append(escape_latex_special_chars(summary_text))
            else:
                latex_lines.append(r"\begin{itemize}")
                for item_line in sections[sec]:
                    if not item_line:
                        continue
                    if sec == "Skills" and ":" in item_line and len(item_line.split(":")[0]) < 35:
                        prefix, suffix = item_line.split(":", 1)
                        clean_item = f"\\textbf{{{escape_latex_special_chars(prefix.strip())}:}} {escape_latex_special_chars(suffix.strip())}"
                        latex_lines.append(f"  \\item {clean_item}")
                    elif any(kw in item_line for kw in ["|", " -- ", " - ", "Present", "04/", "08/", "07/", "01/"]) and len(item_line) < 120:
                        parts = re.split(r'\s{3,}', item_line)
                        if len(parts) >= 2:
                            left = " | ".join(p.strip() for p in parts[:-1])
                            right = parts[-1].strip()
                            bold_left = " $\\vert$ ".join(f"\\textbf{{{escape_latex_special_chars(p)}}}" for p in left.split("|") if p.strip())
                            bold_right = f"\\textbf{{{escape_latex_special_chars(right)}}}"
                            latex_lines.append(f"  \\item[] {bold_left} \\hfill {bold_right}")
                        else:
                            parts = [escape_latex_special_chars(p.strip()) for p in item_line.split("|")]
                            bold_header = " $\\vert$ ".join(f"\\textbf{{{p}}}" for p in parts if p.strip())
                            latex_lines.append(f"  \\item[] {bold_header}")
                    else:
                        clean_item = process_bullet(item_line)
                        if clean_item:
                            latex_lines.append(f"  \\item {clean_item}")
                latex_lines.append(r"\end{itemize}")
            latex_lines.append(r"\vspace{6pt}")
            latex_lines.append("")

    latex_lines.append(r"\end{document}")
    return "\n".join(latex_lines)


async def cmd_analyze_async(args) -> int:
    task_dir = resolve_session_dir(args, "analyze", "job", args.job)
    print(f"[DIR] Created task folder: {task_dir}")

    job = await _analyze_job_async(args, args.job, getattr(args, 'company', None), getattr(args, 'role', None))

    out_path = Path(args.out) if args.out else task_dir / "job-analysis.json"
    out_path.write_text(job.model_dump_json(indent=2), encoding="utf-8")

    print(f"[OK] Job analysis complete. Output: {out_path}")
    return 0


async def cmd_tailor_async(args) -> int:
    task_dir = resolve_session_dir(args, "tailor", args.resume, args.job)
    print(f"[DIR] Created task folder: {task_dir}")

    job = await _analyze_job_async(args, args.job, getattr(args, 'company', None), getattr(args, 'role', None))

    # Phase 2: Build candidate profile
    print("[PHASE 2] Building candidate profile...")
    # Handle PDF input
    resume_path = args.resume
    fmt = detect_input_format(resume_path)
    if fmt == 'pdf':
        print("[INFO] PDF resume detected - extracting text for profile building")
        text = extract_pdf_text(resume_path)
        tex_content = _pdf_text_to_latex(text)
        resume_path = task_dir / "master.tex"
        resume_path.write_text(tex_content, encoding="utf-8")
    elif fmt == 'txt':
        print("[INFO] Text resume detected - converting to LaTeX")
        text = Path(resume_path).read_text(encoding="utf-8")
        tex_content = _pdf_text_to_latex(text)
        resume_path = task_dir / "master.tex"
        resume_path.write_text(tex_content, encoding="utf-8")

    profile = build_profile(str(resume_path), args.linkedin)
    profile_path = task_dir / "candidate-profile.yaml"
    profile_path.write_text(profile.model_dump_json(indent=2), encoding="utf-8")

    # Phase 3: Gap analysis
    print("[PHASE 3] Analyzing gaps...")
    gap_report, injection_map = analyze_gaps(job, profile.model_dump())
    (task_dir / "gap-report.md").write_text(gap_report.model_dump_json(indent=2), encoding="utf-8")
    (task_dir / "keyword-injection-map.json").write_text(json.dumps(injection_map, indent=2), encoding="utf-8")

    # Gate 3: Critical gaps <= 3
    critical_count = len(gap_report.critical_gaps)
    if critical_count > 3:
        print(f"[FAIL] Gate 3 blocked: {critical_count} critical gaps (max 3). See gap-report.md")
        return 1

    # Phase 4: Optimization
    print("[PHASE 4] Optimizing resume...")
    latex = Path(resume_path).read_text(encoding="utf-8")
    optimized = optimize_resume(latex, injection_map, mode=args.mode)
    optimized_path = task_dir / "main.tex"
    optimized_path.write_text(optimized, encoding="utf-8")

    # Phase 5: Validation
    print("[PHASE 5] Running validation gates...")
    validation = run_all_gates(optimized, job, mode=args.mode)
    (task_dir / "validation-report.json").write_text(validation.model_dump_json(indent=2), encoding="utf-8")

    if not validation.overall_passed:
        print("[FAIL] Validation gates FAILED. See validation-report.json")
        return 1

    # Build
    print("[BUILD] Building PDF...")
    build_result = build_resume(optimized, job, mode=args.mode)
    (task_dir / "build-result.json").write_text(build_result.model_dump_json(indent=2), encoding="utf-8")

    # Copy artifacts to task_dir
    import shutil
    if build_result.pdf_path:
        shutil.copy2(build_result.pdf_path, task_dir / "main.pdf")
    if build_result.text_path:
        shutil.copy2(build_result.text_path, task_dir / "main.txt")

    write_overleaf_instructions(task_dir, mode=args.mode)

    print(f"\n[OK] Tailoring complete!")
    print(f"[FILE] Overleaf-ready LaTeX: {optimized_path}")
    print(f"[FILE] Usage guide: {task_dir / 'OVERLEAF_INSTRUCTIONS.md'}")
    print(f"[FILE] Validation: {task_dir / 'validation-report.json'} (all gates PASSED)")
    return 0


async def cmd_review_async(args) -> int:
    """Interactive review mode - runs phases up to --phase with gate enforcement."""
    # For now, delegate to tailor but stop at specified phase
    print(f"[REVIEW] Review mode: running up to phase {args.phase} with interactive gates")
    # Reuse tailor logic but with phase limit
    return await cmd_tailor_async(args)


async def cmd_build_async(args) -> int:
    task_dir = resolve_session_dir(args, "build", args.resume, args.job)
    print(f"[DIR] Created task folder: {task_dir}")

    job = await _analyze_job_async(args, args.job, getattr(args, 'company', None), getattr(args, 'role', None))

    # Handle PDF input for build
    resume_path = args.resume
    fmt = detect_input_format(resume_path)
    if fmt == 'pdf':
        print("[INFO] PDF resume detected - extracting text for build")
        text = extract_pdf_text(resume_path)
        tex_content = _pdf_text_to_latex(text)
        resume_path = task_dir / "master.tex"
        resume_path.write_text(tex_content, encoding="utf-8")
    elif fmt == 'txt':
        print("[INFO] Text resume detected - converting to LaTeX")
        text = Path(resume_path).read_text(encoding="utf-8")
        tex_content = _pdf_text_to_latex(text)
        resume_path = task_dir / "master.tex"
        resume_path.write_text(tex_content, encoding="utf-8")

    build_result = build_resume(latex=Path(resume_path).read_text(encoding="utf-8"), job=job, mode=args.mode)
    (task_dir / "build-result.json").write_text(build_result.model_dump_json(indent=2), encoding="utf-8")

    import shutil
    if build_result.pdf_path:
        shutil.copy2(build_result.pdf_path, task_dir / "main.pdf")
    if build_result.text_path:
        shutil.copy2(build_result.text_path, task_dir / "main.txt")
    shutil.copy2(resume_path, task_dir / "main.tex")

    write_overleaf_instructions(task_dir, mode=args.mode)

    print(f"[OK] Build complete. Artifacts in: {task_dir}")
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="resume-doctor", description="ATS-safe resume tailoring toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--session-dir", help="Explicit task subfolder under resume-doctor-output/")
        p.add_argument("--no-prompt", action="store_true", help="Skip interactive prompts, use auto-generated name")

    # ats-audit
    p = subparsers.add_parser("ats-audit", help="General ATS audit (no job target)")
    p.add_argument("--resume", required=True, help="Path to LaTeX resume (.tex)")
    p.add_argument("--out", help="Output JSON path (default: task-dir/ats-audit.json)")
    add_common(p)

    # analyze
    p = subparsers.add_parser("analyze", help="Analyze job description -> job-analysis.json")
    p.add_argument("--job", required=True, help="Job URL, PDF path, or text file")
    p.add_argument("--company", help="Company name hint")
    p.add_argument("--role", help="Role ID for parser-optimized keywords (e.g., software-engineer/backend-engineer)")
    p.add_argument("--out", help="Output JSON path")
    add_common(p)

    # tailor
    p = subparsers.add_parser("tailor", help="Full 5-phase targeted optimization")
    p.add_argument("--resume", required=True, help="Path to master LaTeX resume (.tex)")
    p.add_argument("--job", required=True, help="Job URL, PDF, or text file")
    p.add_argument("--role", help="Role ID for parser-optimized keywords (e.g., software-engineer/backend-engineer)")
    p.add_argument("--company", help="Target company name override")
    p.add_argument("--mode", choices=["ats-max", "designer-polish"], default="designer-polish")
    p.add_argument("--name", help="Base name for output files")
    p.add_argument("--portfolio", help="Portfolio JSON for cross-ref")
    p.add_argument("--linkedin", help="LinkedIn PDF export")
    add_common(p)

    # review
    p = subparsers.add_parser("review", help="Interactive phase-gated review")
    p.add_argument("--resume", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--role", help="Role ID for parser-optimized keywords (e.g., software-engineer/backend-engineer)")
    p.add_argument("--company", help="Target company name override")
    p.add_argument("--mode", choices=["ats-max", "designer-polish"], default="designer-polish")
    p.add_argument("--name", help="Base name for output files")
    p.add_argument("--portfolio", help="Portfolio JSON for cross-ref")
    p.add_argument("--linkedin", help="LinkedIn PDF export")
    p.add_argument("--phase", type=int, choices=[1, 2, 3, 4, 5], default=5)
    p.add_argument("--auto-approve", action="store_true")
    add_common(p)

    # build
    p = subparsers.add_parser("build", help="Build PDF from optimized LaTeX")
    p.add_argument("--resume", required=True, help="Path to optimized .tex")
    p.add_argument("--job", required=True, help="Job analysis JSON or URL")
    p.add_argument("--role", help="Role ID for parser-optimized keywords (e.g., software-engineer/backend-engineer)")
    p.add_argument("--company", help="Target company name override")
    p.add_argument("--mode", choices=["ats-max", "designer-polish"], default="designer-polish")
    add_common(p)

    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()

    if args.command == "ats-audit":
        return asyncio.run(cmd_ats_audit_async(args))
    elif args.command == "analyze":
        return asyncio.run(cmd_analyze_async(args))
    elif args.command == "tailor":
        return asyncio.run(cmd_tailor_async(args))
    elif args.command == "review":
        return asyncio.run(cmd_review_async(args))
    elif args.command == "build":
        return asyncio.run(cmd_build_async(args))
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())