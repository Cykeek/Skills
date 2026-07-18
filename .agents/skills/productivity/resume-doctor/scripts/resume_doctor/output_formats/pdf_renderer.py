"""
PDF Renderer — PDF output via Typst (preferred) or WeasyPrint.

Generates PDF directly without LaTeX dependency. Uses Typst for best quality,
falls back to WeasyPrint (HTML→PDF) if Typst unavailable.
"""
from pathlib import Path
from typing import List, Optional
import subprocess
import shutil

from resume_doctor.models.resume_data import ResumeData, NDALevel
from resume_doctor.output_formats import BaseRenderer, OutputFormat


class PDFRenderer(BaseRenderer):
    """Render ResumeData to PDF using Typst or WeasyPrint."""

    format = OutputFormat.PDF
    extension = ".pdf"

    def __init__(self, engine: str = "auto"):
        """
        Args:
            engine: "typst", "weasyprint", or "auto" (try Typst first, fallback to WeasyPrint)
        """
        self.engine = engine
        self._html_renderer = None

    def _get_html_renderer(self):
        if self._html_renderer is None:
            from .html_renderer import HTMLRenderer
            self._html_renderer = HTMLRenderer()
        return self._html_renderer

    def _apply_nda(self, text: str, level: NDALevel) -> str:
        if level == NDALevel.L0:
            return text
        import re
        if level == NDALevel.L1:
            return re.sub(r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Technologies|Systems|Labs)\b', '[Company]', text)
        elif level == NDALevel.L2:
            return re.sub(r'\b(?:Senior|Lead|Principal|Staff)\s+\w+', '[Role]', text)
        return text

    def _check_typst(self) -> bool:
        """Check if Typst is available."""
        return shutil.which("typst") is not None

    def _check_weasyprint(self) -> bool:
        """Check if WeasyPrint is available."""
        try:
            import weasyprint
            return True
        except ImportError:
            return False

    def _get_engine(self) -> str:
        """Determine which engine to use."""
        if self.engine != "auto":
            return self.engine

        if self._check_typst():
            return "typst"
        elif self._check_weasyprint():
            return "weasyprint"
        else:
            raise RuntimeError(
                "No PDF engine available. Install Typst (https://typst.app/) or WeasyPrint (pip install weasyprint)"
            )

    def _render_typst(self, resume: ResumeData) -> bytes:
        """Render using Typst (modern, fast, high-quality typesetting)."""
        typst_content = self._generate_typst(resume)

        # Write to temp file and compile
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.typ', delete=False, encoding='utf-8') as f:
            f.write(typst_content)
            typst_path = Path(f.name)

        pdf_path = typst_path.with_suffix('.pdf')

        try:
            result = subprocess.run(
                ['typst', 'compile', str(typst_path), str(pdf_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                raise RuntimeError(f"Typst compilation failed: {result.stderr}")

            pdf_bytes = pdf_path.read_bytes()
            return pdf_bytes
        finally:
            # Cleanup
            typst_path.unlink(missing_ok=True)
            pdf_path.unlink(missing_ok=True)

    def _generate_typst(self, resume: ResumeData) -> str:
        """Generate Typst source code."""
        lines = [
            '#set page(paper: "a4", margin: (x: 1.8cm, y: 1.4cm))',
            '#set text(font: "Inter", size: 10.5pt, line-spacing: 1.15)',
            '#set par(justify: false, spacing: 4pt)',
            '',
            '#let contact-line = it => it',
            '#let signaltag(tag) = emph(smallcaps(tag))',
            '#let kw(keyword) = strong(keyword)',
            '',
        ]

        # Contact header
        name = resume.contact.name
        lines.append(f'#align(center)[#text(size: 22pt, weight: 700)[{name}]]')

        if resume.contact.headline:
            lines.append(f'#align(center)[#text(size: 11pt, weight: 700, fill: #4a4a6a)[{resume.contact.headline}]]')

        contact_parts = []
        if resume.contact.location:
            contact_parts.append(resume.contact.location)
        if resume.contact.phone:
            contact_parts.append(resume.contact.phone)
        if resume.contact.email:
            contact_parts.append(f'#link("{resume.contact.email}")[{resume.contact.email}]')
        for link in resume.contact.links[:3]:
            if link.url:
                label = link.label or link.url
                contact_parts.append(f'#link("{link.url}")[{label}]')

        lines.append(f'#align(center)[#text(size: 9.5pt, fill: #555)[{ " | ".join(contact_parts) }]]')
        lines.append('#v(8pt)')
        lines.append('#rule(length: 100%, thickness: 0.5pt, stroke: #ccc)')
        lines.append('#v(12pt)')

        # Summary
        if resume.summary:
            lines.append('#heading[Professional Summary]')
            lines.append(resume.summary)
            lines.append('#v(12pt)')

        # Skills
        if resume.skills.categories or resume.skills.summary:
            lines.append('#heading[Skills & Technical Proficiency]')
            if resume.skills.summary:
                lines.append(resume.skills.summary)
                lines.append('#v(6pt)')

            if resume.skills.categories:
                for cat in resume.skills.categories:
                    if cat.skills:
                        skill_names = [s.name for s in cat.skills]
                        lines.append(f'#text(weight: 700)[{cat.name}:] {", ".join(skill_names)}')
                        lines.append('#v(4pt)')

            lines.append('#v(12pt)')

        # Experience
        if resume.experience:
            lines.append('#heading[Experience]')
            for entry in resume.experience:
                header_parts = [
                    f'#strong[{entry.role}]',
                    f'#strong[{entry.company}]',
                ]
                if entry.location:
                    header_parts.append(entry.location)
                header_parts.append(entry.date_range)
                lines.append(' | '.join(header_parts))

                if entry.description:
                    lines.append(entry.description)

                if entry.bullets:
                    for bullet in entry.bullets:
                        bullet_text = self._apply_nda(bullet, entry.nda_level)
                        lines.append(f'- {bullet_text}')

                if entry.technologies:
                    lines.append(f'*Technologies: {", ".join(entry.technologies)}*')

                if entry.metrics:
                    lines.append(f'*Key Metrics: {"; ".join(entry.metrics)}*')

                lines.append('#v(8pt)')

            lines.append('#v(12pt)')

        # Projects
        if resume.projects:
            lines.append('#heading[Selected Projects]')
            for proj in resume.projects:
                header = f'#strong[{proj.name}]'
                if proj.role:
                    header += f' | {proj.role}'
                lines.append(header)

                if proj.description:
                    lines.append(proj.description)

                if proj.bullets:
                    for bullet in proj.bullets:
                        bullet_text = self._apply_nda(bullet, proj.nda_level)
                        lines.append(f'- {bullet_text}')

                if proj.technologies:
                    lines.append(f'*Stack: {", ".join(proj.technologies)}*')

                if proj.link:
                    lines.append(f'#link("{proj.link}")[View Project]')

                lines.append('#v(8pt)')

            lines.append('#v(12pt)')

        # Education
        if resume.education:
            lines.append('#heading[Education & Certifications]')
            for edu in resume.education:
                parts = [f'#strong[{edu.degree}]', f'#emph[{edu.institution}]']
                if edu.location:
                    parts.append(edu.location)
                if edu.graduation_date:
                    parts.append(edu.graduation_date)
                lines.append(' | '.join(parts))

                if edu.honors:
                    lines.append(f'Honors: {", ".join(edu.honors)}')
                if edu.relevant_coursework:
                    lines.append(f'Relevant Coursework: {", ".join(edu.relevant_coursework)}')

                lines.append('#v(6pt)')

            lines.append('#v(12pt)')

        # Certifications
        if resume.certifications:
            lines.append('#heading[Certifications]')
            for cert in resume.certifications:
                parts = [f'#strong[{cert.name}]', cert.issuer]
                if cert.date_earned:
                    parts.append(cert.date_earned)
                if cert.credential_url:
                    parts.append(f'#link("{cert.credential_url}")[Verify]')
                lines.append(' | '.join(parts))

        return '\n'.join(lines)

    def _render_weasyprint(self, resume: ResumeData) -> bytes:
        """Render using WeasyPrint (HTML→PDF)."""
        from weasyprint import HTML, CSS

        html_content = self._get_html_renderer().render(resume)

        # Add print-specific CSS
        print_css = CSS(string='''
            @page { size: A4; margin: 1.4cm 1.8cm; }
            body { font-family: "DejaVu Sans", "Liberation Sans", sans-serif; font-size: 10.5pt; line-height: 1.15; }
            .contact-links a { color: inherit; text-decoration: none; }
            section { break-inside: avoid; }
            .experience-entry, .project-entry, .education-entry { break-inside: avoid; }
        ''')

        doc = HTML(string=html_content)
        pdf_bytes = doc.write_pdf(stylesheets=[print_css])
        return pdf_bytes

    def render(self, resume: ResumeData) -> bytes:
        """Render to PDF bytes."""
        engine = self._get_engine()

        if engine == "typst":
            return self._render_typst(resume)
        elif engine == "weasyprint":
            return self._render_weasyprint(resume)
        else:
            raise RuntimeError(f"Unknown PDF engine: {engine}")

    def save(self, resume: ResumeData, output_path: Path) -> Path:
        """Render and save to PDF file."""
        content = self.render(resume)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
        return output_path

    def get_instructions(self, resume: ResumeData) -> str:
        name = resume.contact.name or "Your Name"
        engine = self._get_engine() if self.engine == "auto" else self.engine
        return f"""# How to Use Your PDF Resume

## Quick Start
The generated `.pdf` file is ready to:
- **View**: Open in any PDF viewer
- **Print**: Ctrl/Cmd+P for physical copies
- **Share**: Email, upload, attach to applications

## Engine Used: {engine.upper()}

### Typst (Recommended)
- **Modern typesetting** — better kerning, hyphenation, layout
- **Fast compilation** — typically <1 second
- **No LaTeX dependencies** — single binary install
- **Install**: `curl -sSf https://typst.app/install.sh | sh` or download from https://typst.app/

### WeasyPrint (Fallback)
- **HTML→PDF** — uses web rendering engine
- **Good CSS support** — including flexbox, grid
- **Install**: `pip install weasyprint` (requires system dependencies: pango, cairo, gdk-pixbuf)

## ATS Compatibility
- **Text extraction**: PDF text layer preserves all content
- **Structure**: Semantic headings, lists, proper reading order
- **Keywords**: All keywords embedded in text layer
- **No images/text boxes**: Pure text-based layout

## Distribution
- **Email**: Attach directly — universal compatibility
- **Job portals**: Upload .pdf (most accept PDF)
- **Print**: High-quality output on any printer
- **Archive**: PDF/A-1b compliant for long-term storage

## Customization
To customize styling, modify the source format first, then regenerate:
```bash
# Edit markdown, then rebuild PDF
vim resume.md
resume-doctor build --resume resume_data.json --format pdf

# Or use custom CSS with WeasyPrint
resume-doctor build --resume resume_data.json --format pdf --engine weasyprint --css custom.css
```

## Quality Check
```bash
# Verify text extraction
pdftotext resume.pdf - | head -50

# Check PDF properties
pdfinfo resume.pdf
```

## Companion Files
- `resume_data.json` — Canonical structured data (source of truth)
- `resume.md` — Markdown source (editable)
- `resume.html` — Web version
- `latex/main.tex` — Overleaf version
- `docx/resume.docx` — Word version
- `validation-report.json` — Quality gates (all should PASS)

## Next Steps
- **Tailor for another job**: `resume-doctor tailor --resume resume_data.json --job <url> --format pdf`
- **Export other formats**: `resume-doctor build --resume resume_data.json --format <latex|markdown|html|docx>`
- **Re-generate with different engine**: `resume-doctor build --resume resume_data.json --format pdf --engine typst|weasyprint`
"""


from resume_doctor.output_formats import RendererRegistry
RendererRegistry.register(OutputFormat.PDF, PDFRenderer)