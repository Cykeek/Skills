"""
Markdown Renderer — GitHub-flavored Markdown output.

Clean, version-control friendly format for GitHub, Notion, Obsidian, etc.
"""
from pathlib import Path
from typing import List

from resume_doctor.models.resume_data import ResumeData, NDALevel
from resume_doctor.output_formats import BaseRenderer, OutputFormat


class MarkdownRenderer(BaseRenderer):
    """Render ResumeData to GitHub-flavored Markdown."""

    format = OutputFormat.MARKDOWN
    extension = ".md"

    def _apply_nda(self, text: str, level: NDALevel) -> str:
        """Apply NDA abstraction level to text."""
        if level == NDALevel.L0:
            return text
        elif level == NDALevel.L1:
            import re
            return re.sub(r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Technologies|Systems|Labs)\b', '[Company]', text)
        elif level == NDALevel.L2:
            return re.sub(r'\b(?:Senior|Lead|Principal|Staff)\s+\w+', '[Role]', text)
        return text

    def _render_contact(self, contact) -> str:
        lines = [f"# {contact.name}", ""]
        if contact.headline:
            lines.append(f"**{contact.headline}**")
            lines.append("")

        contact_parts = []
        if contact.location:
            contact_parts.append(contact.location)
        if contact.phone:
            contact_parts.append(contact.phone)
        if contact.email:
            contact_parts.append(f"[{contact.email}](mailto:{contact.email})")
        for link in contact.links[:3]:
            if link.url:
                label = link.label or link.url
                contact_parts.append(f"[{label}]({link.url})")

        lines.append(" | ".join(contact_parts))
        lines.append("")
        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    def _render_summary(self, summary: str) -> str:
        if not summary:
            return ""
        return "\n".join([
            "## Professional Summary",
            "",
            summary,
            "",
            "---",
            "",
        ])

    def _render_skills(self, skills_section) -> str:
        if not skills_section.categories and not skills_section.summary:
            return ""

        lines = ["## Skills & Technical Proficiency", ""]

        if skills_section.summary:
            lines.append(skills_section.summary)
            lines.append("")

        if skills_section.categories:
            for cat in skills_section.categories:
                if cat.skills:
                    skill_names = [s.name for s in cat.skills]
                    lines.append(f"**{cat.name}**: {', '.join(skill_names)}")
                    lines.append("")

        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    def _render_experience(self, exp: List) -> str:
        if not exp:
            return ""

        lines = ["## Experience", ""]

        for entry in exp:
            # Header line
            header_parts = [f"**{entry.role}**", f"**{entry.company}**"]
            if entry.location:
                header_parts.append(entry.location)
            header_parts.append(entry.date_range)
            lines.append(" | ".join(header_parts))
            lines.append("")

            if entry.description:
                lines.append(entry.description)
                lines.append("")

            if entry.bullets:
                for bullet in entry.bullets:
                    bullet_text = self._apply_nda(bullet, entry.nda_level)
                    lines.append(f"- {bullet_text}")
                lines.append("")

            if entry.technologies:
                lines.append(f"*Technologies: {', '.join(entry.technologies)}*")
                lines.append("")

            if entry.metrics:
                lines.append(f"*Key Metrics: {'; '.join(entry.metrics)}*")
                lines.append("")

        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    def _render_projects(self, projects: List) -> str:
        if not projects:
            return ""

        lines = ["## Selected Projects", ""]

        for proj in projects:
            header = f"**{proj.name}**"
            if proj.role:
                header += f" | {proj.role}"
            lines.append(header)
            lines.append("")

            if proj.description:
                lines.append(proj.description)
                lines.append("")

            if proj.bullets:
                for bullet in proj.bullets:
                    bullet_text = self._apply_nda(bullet, proj.nda_level)
                    lines.append(f"- {bullet_text}")
                lines.append("")

            if proj.technologies:
                lines.append(f"*Stack: {', '.join(proj.technologies)}*")
                lines.append("")

            if proj.link:
                lines.append(f"[Project Link]({proj.link})")
                lines.append("")

        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    def _render_education(self, education: List) -> str:
        if not education:
            return ""

        lines = ["## Education & Certifications", ""]

        for edu in education:
            parts = [f"**{edu.degree}**", f"*{edu.institution}*"]
            if edu.location:
                parts.append(edu.location)
            if edu.graduation_date:
                parts.append(edu.graduation_date)
            lines.append(" | ".join(parts))

            if edu.honors:
                lines.append(f"Honors: {', '.join(edu.honors)}")

            if edu.relevant_coursework:
                lines.append(f"Relevant Coursework: {', '.join(edu.relevant_coursework)}")

            lines.append("")

        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    def _render_certifications(self, certs: List) -> str:
        if not certs:
            return ""

        lines = ["## Certifications", ""]

        for cert in certs:
            line = f"- **{cert.name}** | {cert.issuer}"
            if cert.date_earned:
                line += f" | {cert.date_earned}"
            if cert.credential_url:
                line += f" | [Verify]({cert.credential_url})"
            lines.append(line)

        lines.append("")
        return "\n".join(lines)

    def render(self, resume: ResumeData) -> str:
        lines = [f"<!-- Resume for {resume.contact.name} -->", ""]

        lines.append(self._render_contact(resume.contact))

        if resume.summary:
            lines.append(self._render_summary(resume.summary))

        if resume.skills.categories or resume.skills.summary:
            lines.append(self._render_skills(resume.skills))

        if resume.experience:
            lines.append(self._render_experience(resume.experience))

        if resume.projects:
            lines.append(self._render_projects(resume.projects))

        if resume.education:
            lines.append(self._render_education(resume.education))

        if resume.certifications:
            lines.append(self._render_certifications(resume.certifications))

        # Footer with metadata
        lines.append("---")
        lines.append("")
        lines.append("*Generated with resume-doctor*")
        if resume.meta.target_role:
            lines.append(f"*Target Role: {resume.meta.target_role}*")
        if resume.meta.target_company:
            lines.append(f"*Target Company: {resume.meta.target_company}*")
        if resume.meta.mode:
            lines.append(f"*Mode: {resume.meta.mode}*")

        return "\n".join(lines)

    def get_instructions(self, resume: ResumeData) -> str:
        name = resume.contact.name or "Your Name"
        return f"""# How to Use Your Markdown Resume

## Quick Start
The generated `.md` file is ready to use immediately:

1. **Open in any editor**: VS Code, Obsidian, Notion, Typora, etc.
2. **Version control**: Commit to Git — Markdown diffs beautifully
3. **Convert to other formats**: Use Pandoc for PDF, DOCX, HTML

## Common Workflows

### GitHub Profile / Portfolio
```bash
# Copy to your profile repo
cp resume.md ~/github-profile/README.md
```

### Notion / Obsidian
- Drag & drop the `.md` file into Notion/Obsidian
- Renders with full formatting preserved

### Convert to PDF (via Pandoc)
```bash
# Install pandoc first: brew install pandoc
pandoc resume.md -o resume.pdf --pdf-engine=weasyprint
# Or with custom styling:
pandoc resume.md -o resume.pdf -V geometry:margin=1in
```

### Convert to DOCX (for recruiters)
```bash
pandoc resume.md -o resume.docx
```

### Convert to HTML (for web portfolio)
```bash
pandoc resume.md -o resume.html --standalone --css=style.css
```

## Markdown Features Used
- **Headings**: `##` for sections (ATS-friendly structure)
- **Bold**: `**Role**`, `**Company**` for emphasis
- **Italics**: `*Technologies:*` for metadata
- **Links**: `[Email](mailto:...)`, `[LinkedIn](https://...)`
- **Lists**: `- Bullet` for experience points
- **Horizontal rules**: `---` for section separation

## Customization
- **Edit directly**: Any text editor, changes tracked by Git
- **Add sections**: Copy/paste heading + content blocks
- **Styling**: Use CSS when converting to HTML/PDF

## ATS Compatibility
Markdown extracts cleanly to plain text:
- Headings become clear section delimiters
- No tables, columns, or graphics to confuse parsers
- Keywords preserved naturally in context

## Companion Files
- `resume_data.json` — Canonical structured data (source of truth)
- `validation-report.json` — Quality gates (all should PASS)
- `job-analysis.json` — Target job requirements
- Other formats in sibling folders: `latex/`, `html/`, `docx/`, `pdf/`

## Next Steps
- **Tailor for another job**: `resume-doctor tailor --resume resume_data.json --job <url> --format markdown`
- **Export LaTeX for Overleaf**: `resume-doctor build --resume resume_data.json --format latex`
- **Export DOCX for recruiters**: `resume-doctor build --resume resume_data.json --format docx`
"""


from resume_doctor.output_formats import RendererRegistry
RendererRegistry.register(OutputFormat.MARKDOWN, MarkdownRenderer)