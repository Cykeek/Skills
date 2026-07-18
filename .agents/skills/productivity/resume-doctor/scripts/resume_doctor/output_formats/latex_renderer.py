"""
LaTeX Renderer — Overleaf-safe, ATS-optimized LaTeX output.

Generates self-contained .tex that compiles on Overleaf (pdfLaTeX, XeLaTeX, LuaLaTeX)
with proper Unicode handling, glyph-to-unicode mapping, and ATS-friendly structure.
"""
import re
from pathlib import Path
from typing import List

from resume_doctor.models.resume_data import ResumeData, NDALevel
from resume_doctor.output_formats import BaseRenderer, OutputFormat


class LaTeXRenderer(BaseRenderer):
    """Render ResumeData to Overleaf-compatible LaTeX."""

    format = OutputFormat.LATEX
    extension = ".tex"

    # LaTeX special characters that need escaping
    LATEX_ESCAPES = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }

    # Ligatures to avoid (ATS extraction issues)
    LIGATURES = {
        'ﬀ': 'ff',
        'ﬁ': 'fi',
        'ﬂ': 'fl',
        'ﬃ': 'ffi',
        'ﬄ': 'ffl',
    }

    def __init__(self, mode: str = "designer-polish"):
        self.mode = mode  # "ats-max" or "designer-polish"

    def _escape(self, text: str) -> str:
        """Escape LaTeX special characters."""
        if not text:
            return ""
        # Replace ligatures first
        for lig, repl in self.LIGATURES.items():
            text = text.replace(lig, repl)
        # Escape special chars (but not already escaped ones)
        for char, esc in self.LATEX_ESCAPES.items():
            text = re.sub(r'(?<!\\)' + re.escape(char), esc, text)
        return text

    def _escape_url(self, url: str) -> str:
        """Escape for URL context (less aggressive)."""
        return url.replace('_', r'\_').replace('%', r'\%').replace('#', r'\#')

    def _apply_nda(self, text: str, level: NDALevel) -> str:
        """Apply NDA abstraction level to text."""
        # This is a simplified version - in production would use more sophisticated replacement
        if level == NDALevel.L0:
            return text
        elif level == NDALevel.L1:
            # Replace company names with generic descriptors
            return re.sub(r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Technologies|Systems|Labs)\b', 'Major Company', text)
        elif level == NDALevel.L2:
            return re.sub(r'\b(?:Senior|Lead|Principal|Staff)\s+\w+', 'Senior Role', text)
        elif level == NDALevel.L3:
            return re.sub(r'\d+%', 'significant percentage', text)
            # Would apply more pattern-based abstraction
        return text

    def _render_contact(self, contact) -> str:
        lines = [
            r"\begin{center}",
            f"  {{\\LARGE \\textbf{{{self._escape(contact.name)}}}}}\\\\[3pt]",
        ]
        if contact.headline:
            lines.append(f"  {{\\small \\textbf{{{self._escape(contact.headline)}}}}}\\\\[3pt]")

        # Build contact line
        parts = []
        if contact.location:
            parts.append(self._escape(contact.location))
        if contact.phone:
            parts.append(self._escape(contact.phone))
        if contact.email:
            parts.append(f"\\href{{mailto:{contact.email}}}{{{self._escape(contact.email)}}}")
        for link in contact.links[:2]:
            if link.url:
                label = link.label if link.label else link.url
                parts.append(f"\\href{{{self._escape_url(link.url)}}}{{{self._escape(label)}}}")

        while len(parts) < 5:
            parts.append("N/A")

        lines.extend([
            r"  {\small",
            f"    \\contactline{{{self._escape(parts[0])}}}{{{self._escape(parts[1])}}}{{{self._escape(parts[2])}}}{{{self._escape(parts[3])}}}{{{self._escape(parts[4])}}}",
            r"  }",
            r"\end{center}",
            r"\vspace{2pt}",
            r"",
        ])
        return "\n".join(lines)

    def _render_summary(self, summary: str) -> str:
        if not summary:
            return ""
        return "\n".join([
            r"% ==================== PROFESSIONAL SUMMARY ====================",
            r"\section*{Professional Summary}",
            self._escape(summary),
            r"\vspace{6pt}",
            r"",
        ])

    def _render_skills(self, skills_section) -> str:
        if not skills_section.categories and not skills_section.summary:
            return ""

        lines = [
            r"% ==================== SKILLS ====================",
            r"\section*{Skills \& Technical Proficiency}",
        ]

        if skills_section.summary:
            lines.append(self._escape(skills_section.summary))
            lines.append(r"")

        if skills_section.categories:
            lines.append(r"\begin{itemize}")
            for cat in skills_section.categories:
                if cat.skills:
                    skill_names = [self._escape(s.name) for s in cat.skills]
                    cat_line = f"  \\item \\textbf{{{self._escape(cat.name)}:}} {', '.join(skill_names)}"
                    lines.append(cat_line)
            lines.append(r"\end{itemize}")

        lines.extend([r"\vspace{6pt}", r""])
        return "\n".join(lines)

    def _render_experience(self, exp: List) -> str:
        if not exp:
            return ""

        lines = [
            r"% ==================== EXPERIENCE ====================",
            r"\section*{Experience}",
            r"\begin{itemize}",
        ]

        for entry in exp:
            # Role | Company | Location | Dates
            header_parts = [
                f"\\textbf{{{self._escape(entry.role)}}}",
                f"\\textbf{{{self._escape(entry.company)}}}",
            ]
            if entry.location:
                header_parts.append(self._escape(entry.location))
            header_parts.append(self._escape(entry.date_range))

            header = " $\\vert$ ".join(header_parts)
            lines.append(f"  \\item[] {header}")

            if entry.description:
                lines.append(f"  \\item[] {self._escape(entry.description)}")

            # Bullets
            if entry.bullets:
                lines.append(r"  \begin{itemize}")
                for bullet in entry.bullets:
                    # Apply NDA abstraction
                    bullet_text = self._apply_nda(bullet, entry.nda_level)
                    # Handle signal tags inline
                    for tag in entry.signal_tags:
                        bullet_text = bullet_text.replace(f"[{tag}]", f"\\signaltag{{{tag}}}")
                    lines.append(f"    \\item {self._escape(bullet_text)}")
                lines.append(r"  \end{itemize}")

            # Technologies
            if entry.technologies:
                tech_str = ", ".join(self._escape(t) for t in entry.technologies)
                lines.append(f"  \\item[] \\textit{{Technologies:}} {tech_str}")

            # Metrics
            if entry.metrics:
                metrics_str = "; ".join(self._escape(m) for m in entry.metrics)
                lines.append(f"  \\item[] \\textit{{Key Metrics:}} {metrics_str}")

        lines.extend([
            r"\end{itemize}",
            r"\vspace{6pt}",
            r"",
        ])
        return "\n".join(lines)

    def _render_projects(self, projects: List) -> str:
        if not projects:
            return ""

        lines = [
            r"% ==================== PROJECTS ====================",
            r"\section*{Selected Projects}",
            r"\begin{itemize}",
        ]

        for proj in projects:
            header = f"\\textbf{{{self._escape(proj.name)}}}"
            if proj.role:
                header += f" $\\vert$ {self._escape(proj.role)}"
            lines.append(f"  \\item[] {header}")

            if proj.description:
                lines.append(f"  \\item[] {self._escape(proj.description)}")

            if proj.bullets:
                lines.append(r"  \begin{itemize}")
                for bullet in proj.bullets:
                    bullet_text = self._apply_nda(bullet, proj.nda_level)
                    lines.append(f"    \\item {self._escape(bullet_text)}")
                lines.append(r"  \end{itemize}")

            if proj.technologies:
                tech_str = ", ".join(self._escape(t) for t in proj.technologies)
                lines.append(f"  \\item[] \\textit{{Stack:}} {tech_str}")

            if proj.link:
                lines.append(f"  \\item[] \\href{{{self._escape_url(proj.link)}}}{{Project Link}}")

        lines.extend([
            r"\end{itemize}",
            r"\vspace{6pt}",
            r"",
        ])
        return "\n".join(lines)

    def _render_education(self, education: List) -> str:
        if not education:
            return ""

        lines = [
            r"% ==================== EDUCATION ====================",
            r"\section*{Education \& Certifications}",
            r"\begin{itemize}",
        ]

        for edu in education:
            parts = [
                f"\\textbf{{{self._escape(edu.degree)}}}",
                f"\\textit{{{self._escape(edu.institution)}}}",
            ]
            if edu.location:
                parts.append(self._escape(edu.location))
            if edu.graduation_date:
                parts.append(self._escape(edu.graduation_date))

            lines.append(f"  \\item[] {' $\\vert$ '.join(parts)}")

            if edu.honors:
                honors = ", ".join(self._escape(h) for h in edu.honors)
                lines.append(f"  \\item[] Honors: {honors}")

            if edu.relevant_coursework:
                cw = ", ".join(self._escape(c) for c in edu.relevant_coursework)
                lines.append(f"  \\item[] Relevant Coursework: {cw}")

        lines.extend([
            r"\end{itemize}",
            r"\vspace{6pt}",
            r"",
        ])
        return "\n".join(lines)

    def _render_certifications(self, certs: List) -> str:
        if not certs:
            return ""

        lines = [
            r"% ==================== CERTIFICATIONS ====================",
            r"\section*{Certifications}",
            r"\begin{itemize}",
        ]

        for cert in certs:
            line = f"  \\item \\textbf{{{self._escape(cert.name)}}} $\\vert$ {self._escape(cert.issuer)}"
            if cert.date_earned:
                line += f" $\\vert$ {self._escape(cert.date_earned)}"
            if cert.credential_url:
                line += f" $\\vert$ \\href{{{self._escape_url(cert.credential_url)}}}{{Verify}}"
            lines.append(line)

        lines.extend([
            r"\end{itemize}",
            r"",
        ])
        return "\n".join(lines)

    def _build_preamble(self, resume: ResumeData) -> List[str]:
        """Build LaTeX preamble with engine-safe guards."""
        name = self._escape(resume.contact.name)
        lines = [
            r"\documentclass[10pt,a4paper]{article}",
            r"\usepackage{iftex}",
            r"\ifPDFTeX",
            r"  \usepackage[T1]{fontenc}",
            r"  \usepackage[utf8]{inputenc}",
            r"  \input{glyphtounicode}",
            r"  \pdfgentounicode=1",
            r"\fi",
            r"\usepackage[margin=1.4cm]{geometry}",
            r"\usepackage{microtype}",
            r"\usepackage{enumitem}",
            r"\setlist[itemize]{leftmargin=1.5em,topsep=2pt,itemsep=2pt,parsep=0pt}",
            r"\usepackage[hidelinks]{hyperref}",
            r"",
            r"% PDF Metadata",
            r"\hypersetup{",
            f"    pdftitle={{{name} - Resume}},",
            f"    pdfauthor={{{name}}},",
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
            r"\newcommand{\kw}[1]{\textbf{#1}}",
            r"",
        ]

        # Mode-specific adjustments
        if self.mode == "ats-max":
            lines.append(r"\renewcommand{\baselinestretch}{1.02}")
            lines.append(r"\setlength{\parskip}{1pt}")
        else:
            lines.append(r"\renewcommand{\baselinestretch}{1.08}")
            lines.append(r"\setlength{\parskip}{2pt}")

        return lines

    def render(self, resume: ResumeData) -> str:
        """Render complete LaTeX document."""
        lines = self._build_preamble(resume)
        lines.append(r"\begin{document}")
        lines.append(r"")

        # Contact header
        lines.append(self._render_contact(resume.contact))

        # Summary
        if resume.summary:
            lines.append(self._render_summary(resume.summary))

        # Skills
        if resume.skills.categories or resume.skills.summary:
            lines.append(self._render_skills(resume.skills))

        # Experience
        if resume.experience:
            lines.append(self._render_experience(resume.experience))

        # Projects
        if resume.projects:
            lines.append(self._render_projects(resume.projects))

        # Education
        if resume.education:
            lines.append(self._render_education(resume.education))

        # Certifications
        if resume.certifications:
            lines.append(self._render_certifications(resume.certifications))

        lines.append(r"\end{document}")
        return "\n".join(lines)

    def get_instructions(self, resume: ResumeData) -> str:
        name = resume.contact.name or "Your Name"
        return f"""# How to Use Your LaTeX Resume on Overleaf

## Quick Start
1. **Open Overleaf**: Go to https://www.overleaf.com and sign in
2. **Create Blank Project**: Click "New Project" → "Blank Project"
3. **Name it**: e.g., "{name} Resume - {{company}}"
4. **Replace main.tex**: Click `main.tex` in file panel, delete contents, paste the generated `.tex`
5. **Recompile**: Click green "Recompile" button (top-left)
6. **Download PDF**: Click "Download PDF" from toolbar

## Why Overleaf?
- **No local LaTeX install needed** — runs TeX Live in the cloud
- **Three engines supported**: pdfLaTeX (default), XeLaTeX, LuaLaTeX
- **Auto-saves & version history** — never lose changes
- **Shareable link** — send read-only or edit access to reviewers

## Engine Compatibility
This `.tex` includes engine-safe guards (`\\ifPDFTeX`):
- **pdfLaTeX**: Loads `glyphtounicode` for proper ATS text extraction
- **XeLaTeX/LuaLaTeX**: Native UTF-8, skips pdfTeX primitives

## Companion Files in Output Folder
- `main.pdf` — Pre-compiled reference (identical to Overleaf output)
- `main.txt` — Plain text extraction (what ATS parsers actually see)
- `validation-report.json` — All 10 quality gates (should all PASS)
- `job-analysis.json` — Target job requirements
- `gap-report.md` / `keyword-injection-map.json` — Audit trail

## Customization
- **Edit metrics**: Change `\\metric{{...}}` values in `.tex`, recompile
- **Switch density**: Re-run with `--mode ats-max` (1-page) or `--mode designer-polish` (2-page)
- **Update for new job**: `resume-doctor tailor --resume main.tex --job <url> --format latex`

## Troubleshooting
| Issue | Fix |
|-------|-----|
| "Undefined control sequence" | Ensure you pasted the ENTIRE `.tex` including preamble |
| "Font not found" | Use pdfLaTeX engine (Menu → Settings → Compiler → pdfLaTeX) |
| Special chars broken | Check `& % $ # _` are escaped as `\\& \\% \\$ \\# \\_` |
| PDF looks different | Overleaf uses TeX Live 2024; matches local `pdflatex` output |

## Next Steps
- **Tailor for another job**: `resume-doctor tailor --resume main.tex --job <new-url> --format latex`
- **Export other formats**: `resume-doctor build --resume resume_data.json --format markdown|html|docx|pdf`
"""


# Register this renderer
from resume_doctor.output_formats import RendererRegistry
RendererRegistry.register(OutputFormat.LATEX, LaTeXRenderer)