"""
HTML Renderer — Semantic, accessible HTML output.

Clean HTML5 with semantic elements, ready for web portfolios, email, or further styling.
"""
from pathlib import Path
from typing import List

from resume_doctor.models.resume_data import ResumeData, NDALevel
from resume_doctor.output_formats import BaseRenderer, OutputFormat


class HTMLRenderer(BaseRenderer):
    """Render ResumeData to semantic HTML5."""

    format = OutputFormat.HTML
    extension = ".html"

    def _apply_nda(self, text: str, level: NDALevel) -> str:
        if level == NDALevel.L0:
            return text
        import re
        if level == NDALevel.L1:
            return re.sub(r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Technologies|Systems|Labs)\b', '[Company]', text)
        elif level == NDALevel.L2:
            return re.sub(r'\b(?:Senior|Lead|Principal|Staff)\s+\w+', '[Role]', text)
        return text

    def _escape_html(self, text: str) -> str:
        return (text
            .replace('&', '&')
            .replace('<', '<')
            .replace('>', '>')
            .replace('"', '"')
            .replace("'", '''))

    def _render_contact(self, contact) -> str:
        parts = []
        if contact.location:
            parts.append(f'<span class="location">{self._escape_html(contact.location)}</span>')
        if contact.phone:
            parts.append(f'<a href="tel:{self._escape_html(contact.phone)}" class="phone">{self._escape_html(contact.phone)}</a>')
        if contact.email:
            parts.append(f'<a href="mailto:{self._escape_html(contact.email)}" class="email">{self._escape_html(contact.email)}</a>')
        for link in contact.links[:3]:
            if link.url:
                label = self._escape_html(link.label or link.url)
                parts.append(f'<a href="{self._escape_html(link.url)}" class="link">{label}</a>')

        headline = f'<p class="headline">{self._escape_html(contact.headline)}</p>' if contact.headline else ''

        return f'''
<header class="contact-header">
  <h1 class="name">{self._escape_html(contact.name)}</h1>
  {headline}
  <div class="contact-links">
    {' | '.join(parts)}
  </div>
</header>'''

    def _render_summary(self, summary: str) -> str:
        if not summary:
            return ''
        return f'''
<section class="summary">
  <h2>Professional Summary</h2>
  <p>{self._escape_html(summary)}</p>
</section>'''

    def _render_skills(self, skills_section) -> str:
        if not skills_section.categories and not skills_section.summary:
            return ''

        html = ['<section class="skills">', '<h2>Skills & Technical Proficiency</h2>']

        if skills_section.summary:
            html.append(f'<p class="skills-summary">{self._escape_html(skills_section.summary)}</p>')

        if skills_section.categories:
            html.append('<div class="skill-categories">')
            for cat in skills_section.categories:
                if cat.skills:
                    skill_names = [self._escape_html(s.name) for s in cat.skills]
                    html.append(f'''
  <div class="skill-category">
    <h3>{self._escape_html(cat.name)}</h3>
    <ul class="skill-list">
      {''.join(f'<li>{name}</li>' for name in skill_names)}
    </ul>
  </div>''')
            html.append('</div>')

        html.append('</section>')
        return '\n'.join(html)

    def _render_experience(self, exp: List) -> str:
        if not exp:
            return ''

        html = ['<section class="experience">', '<h2>Experience</h2>']

        for entry in exp:
            header_parts = [
                f'<span class="role">{self._escape_html(entry.role)}</span>',
                f'<span class="company">{self._escape_html(entry.company)}</span>',
            ]
            if entry.location:
                header_parts.append(f'<span class="location">{self._escape_html(entry.location)}</span>')
            header_parts.append(f'<span class="date-range">{self._escape_html(entry.date_range)}</span>')

            bullets_html = ''
            if entry.bullets:
                bullets = [f'<li>{self._escape_html(self._apply_nda(b, entry.nda_level))}</li>' for b in entry.bullets]
                bullets_html = f'<ul class="bullets">{"".join(bullets)}</ul>'

            tech_html = ''
            if entry.technologies:
                tech_list = ', '.join(self._escape_html(t) for t in entry.technologies)
                tech_html = f'<p class="technologies"><strong>Technologies:</strong> {tech_list}</p>'

            metrics_html = ''
            if entry.metrics:
                metrics_list = '; '.join(self._escape_html(m) for m in entry.metrics)
                metrics_html = f'<p class="metrics"><strong>Key Metrics:</strong> {metrics_list}</p>'

            html.append(f'''
<article class="experience-entry">
  <header class="entry-header">
    {' | '.join(header_parts)}
  </header>
  {f'<p class="description">{self._escape_html(entry.description)}</p>' if entry.description else ''}
  {bullets_html}
  {tech_html}
  {metrics_html}
</article>''')

        html.append('</section>')
        return '\n'.join(html)

    def _render_projects(self, projects: List) -> str:
        if not projects:
            return ''

        html = ['<section class="projects">', '<h2>Selected Projects</h2>']

        for proj in projects:
            header = f'<h3>{self._escape_html(proj.name)}</h3>'
            if proj.role:
                header += f'<p class="project-role">{self._escape_html(proj.role)}</p>'

            bullets_html = ''
            if proj.bullets:
                bullets = [f'<li>{self._escape_html(self._apply_nda(b, proj.nda_level))}</li>' for b in proj.bullets]
                bullets_html = f'<ul class="bullets">{"".join(bullets)}</ul>'

            tech_html = ''
            if proj.technologies:
                tech_list = ', '.join(self._escape_html(t) for t in proj.technologies)
                tech_html = f'<p class="technologies"><strong>Stack:</strong> {tech_list}</p>'

            link_html = ''
            if proj.link:
                link_html = f'<p class="project-link"><a href="{self._escape_html(proj.link)}">View Project</a></p>'

            html.append(f'''
<article class="project-entry">
  {header}
  {f'<p class="description">{self._escape_html(proj.description)}</p>' if proj.description else ''}
  {bullets_html}
  {tech_html}
  {link_html}
</article>''')

        html.append('</section>')
        return '\n'.join(html)

    def _render_education(self, education: List) -> str:
        if not education:
            return ''

        html = ['<section class="education">', '<h2>Education & Certifications</h2>']

        for edu in education:
            parts = [
                f'<span class="degree">{self._escape_html(edu.degree)}</span>',
                f'<span class="institution">{self._escape_html(edu.institution)}</span>',
            ]
            if edu.location:
                parts.append(f'<span class="location">{self._escape_html(edu.location)}</span>')
            if edu.graduation_date:
                parts.append(f'<span class="date">{self._escape_html(edu.graduation_date)}</span>')

            honors_html = ''
            if edu.honors:
                honors_html = f'<p class="honors"><strong>Honors:</strong> {", ".join(self._escape_html(h) for h in edu.honors)}</p>'

            coursework_html = ''
            if edu.relevant_coursework:
                coursework_html = f'<p class="coursework"><strong>Coursework:</strong> {", ".join(self._escape_html(c) for c in edu.relevant_coursework)}</p>'

            html.append(f'''
<article class="education-entry">
  <header>{' | '.join(parts)}</header>
  {honors_html}
  {coursework_html}
</article>''')

        html.append('</section>')
        return '\n'.join(html)

    def _render_certifications(self, certs: List) -> str:
        if not certs:
            return ''

        html = ['<section class="certifications">', '<h2>Certifications</h2>', '<ul>']

        for cert in certs:
            parts = [f'<strong>{self._escape_html(cert.name)}</strong>', f'{self._escape_html(cert.issuer)}']
            if cert.date_earned:
                parts.append(self._escape_html(cert.date_earned))
            if cert.credential_url:
                parts.append(f'<a href="{self._escape_html(cert.credential_url)}">Verify</a>')
            html.append(f'<li>{" | ".join(parts)}</li>')

        html.extend(['</ul>', '</section>'])
        return '\n'.join(html)

    def _get_css(self) -> str:
        return '''
<style>
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem 1rem; color: #1a1a2e; }
  .contact-header { text-align: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #e0e0e0; }
  .name { font-size: 2.5rem; font-weight: 700; margin: 0 0 0.5rem; color: #1a1a2e; }
  .headline { font-size: 1.25rem; color: #4a4a6a; margin: 0 0 1rem; font-weight: 400; }
  .contact-links { font-size: 0.95rem; color: #555; }
  .contact-links a { color: #2563eb; text-decoration: none; }
  .contact-links a:hover { text-decoration: underline; }
  section { margin-bottom: 2.5rem; }
  h2 { font-size: 1.5rem; font-weight: 600; color: #1a1a2e; border-bottom: 2px solid #2563eb; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
  h3 { font-size: 1.1rem; font-weight: 600; color: #2d2d4a; margin: 1rem 0 0.5rem; }
  .skills-summary { color: #444; margin-bottom: 1rem; }
  .skill-categories { display: grid; gap: 1rem; }
  .skill-category h3 { font-size: 1rem; color: #2563eb; border: none; padding: 0; margin: 0 0 0.5rem; }
  .skill-list { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .skill-list li { background: #f0f4ff; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.9rem; }
  .experience-entry, .project-entry, .education-entry { margin-bottom: 2rem; }
  .entry-header { display: flex; flex-wrap: wrap; gap: 1rem; align-items: baseline; margin-bottom: 0.5rem; }
  .role { font-weight: 600; font-size: 1.1rem; }
  .company { color: #2563eb; font-weight: 500; }
  .location { color: #666; font-size: 0.9rem; }
  .date-range { color: #666; font-size: 0.9rem; margin-left: auto; white-space: nowrap; }
  .description { color: #333; margin: 0.5rem 0; }
  .bullets { margin: 0.75rem 0; padding-left: 1.5rem; }
  .bullets li { margin: 0.5rem 0; }
  .technologies, .metrics { font-size: 0.9rem; color: #555; margin: 0.5rem 0; }
  .project-role { color: #2563eb; font-weight: 500; margin: 0.25rem 0; }
  .project-link a { color: #2563eb; }
  .honors, .coursework { font-size: 0.9rem; color: #555; margin: 0.25rem 0; }
  .certifications ul { list-style: none; padding: 0; }
  .certifications li { padding: 0.5rem 0; border-bottom: 1px solid #eee; }
  @media print { body { padding: 0; max-width: none; } .contact-links a { color: inherit; } }
</style>'''

    def render(self, resume: ResumeData) -> str:
        html = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta charset="UTF-8>',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<title>{self._escape_html(resume.contact.name)} - Resume</title>',
            '<meta name="description" content="Professional resume">',
            self._get_css(),
            '</head>',
            '<body>',
            self._render_contact(resume.contact),
        ]

        if resume.summary:
            html.append(self._render_summary(resume.summary))
        if resume.skills.categories or resume.skills.summary:
            html.append(self._render_skills(resume.skills))
        if resume.experience:
            html.append(self._render_experience(resume.experience))
        if resume.projects:
            html.append(self._render_projects(resume.projects))
        if resume.education:
            html.append(self._render_education(resume.education))
        if resume.certifications:
            html.append(self._render_certifications(resume.certifications))

        html.extend([
            '<footer style="text-align:center; margin-top:3rem; padding-top:1rem; border-top:1px solid #eee; color:#888; font-size:0.85rem;">',
            'Generated with <a href="https://github.com/resume-doctor" style="color:#2563eb;">resume-doctor</a>',
            '</footer>',
            '</body>',
            '</html>',
        ])

        return '\n'.join(html)

    def get_instructions(self, resume: ResumeData) -> str:
        name = resume.contact.name or "Your Name"
        return f"""# How to Use Your HTML Resume

## Quick Start
The generated `.html` file is a complete, self-contained webpage:

1. **Open in browser**: Double-click `resume.html`
2. **Print to PDF**: Ctrl/Cmd+P → Save as PDF
3. **Deploy to web**: Upload to GitHub Pages, Netlify, Vercel, or any static host

## Web Portfolio Integration
```html
<!-- Embed in your portfolio -->
<iframe src="resume.html" style="width:100%; height:800px; border:none;"></iframe>

<!-- Or link directly -->
<a href="resume.html" target="_blank">View My Resume</a>
```

## Email to Recruiters
- **Attach the `.html` file** — most email clients render it inline
- **Or host online** and send the link (more professional)

## Customization
### Styling
The HTML includes embedded CSS. To customize:
1. Extract the `<style>` block to `resume.css`
2. Link it: `<link rel="stylesheet" href="resume.css">`
3. Modify colors, fonts, spacing as needed

### Color Themes
```css
/* Dark mode */
@media (prefers-color-scheme: dark) {{
  body {{ background: #1a1a2e; color: #e0e0e0; }}
  .skill-list li {{ background: #2d2d5a; }}
}}

/* Brand colors */
:root {{
  --primary: #your-brand-color;
  --secondary: #your-secondary-color;
}}
```

### Add Analytics
```html
<!-- Before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Conversion to Other Formats
```bash
# PDF (best with headless Chrome)
npx puppeteer resume.html -o resume.pdf

# Or use wkhtmltopdf
wkhtmltopdf resume.html resume.pdf

# DOCX via Pandoc
pandoc resume.html -o resume.docx
```

## Semantic HTML Features
- **`<header>`** for contact info
- **`<section>`** for each resume section
- **`<article>`** for each experience/project entry
- **`<h1>`-`<h3>`** proper heading hierarchy
- **ARIA-ready** class names for accessibility
- **Print stylesheet** included (`@media print`)

## ATS Compatibility
- Clean text extraction (no tables/columns)
- Proper heading structure for parser segmentation
- All content in reading order
- Links have descriptive text

## Companion Files
- `resume_data.json` — Canonical structured data
- `validation-report.json` — Quality gates
- Other formats in sibling folders

## Next Steps
- **Deploy**: `git add resume.html && git push` (GitHub Pages auto-deploys)
- **Tailor for another job**: `resume-doctor tailor --resume resume_data.json --job <url> --format html`
- **Export other formats**: `resume-doctor build --resume resume_data.json --format pdf|docx|latex|markdown`
"""


from resume_doctor.output_formats import RendererRegistry
RendererRegistry.register(OutputFormat.HTML, HTMLRenderer)