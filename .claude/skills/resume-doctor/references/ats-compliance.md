# ATS Compliance — Deep Reference

This is the deep reference for ensuring resume document structure, styling, and formatting are strictly compliant with modern Applicant Tracking Systems (ATS). Use this guide when auditing resumes for parsing errors or styling layout bugs.

---

## 1. How ATS Parsers Work

Applicant Tracking Systems use text parsers to convert uploaded resume files (PDF, DOCX, TXT) into a structured JSON or XML schema. The parser scans the text looking for landmarks:
- **Contact Information Parser:** Identifies sequences containing email patterns (e.g. `@`), phone number formats, ZIP/postal codes, and links (e.g. LinkedIn).
- **Work History Parser:** Looks for chronological dates (Month/Year), company names, job titles, and bullet lists containing action verbs.
- **Skills Parser:** Matches words on the page against a dictionary of cataloged skills/technologies.
- **Education Parser:** Extracts degree acronyms (BS, MS, MBA, PhD), university names, and graduation years.

### 1.1 The Scrambling Hazard (Multi-Column Layouts)
Most basic ATS parsers read direct text left-to-right across the entire width of the page, ignoring visual grid splits. 
*If a resume uses a 2-column layout (e.g., Experience on the left, Skills/Education on the right), the parser will merge the lines horizontally, resulting in garbled text like:*
> **Senior Engineer** | *June 2022 – Present* **Education**
> **Google LLC** — *Mountain View, CA* **BS Computer Science**

**Rule:** Always default to a single-column, top-to-bottom layout for maximum ATS compatibility.

---

## 2. Document Formats & Compatibility

| Format | ATS Compatibility | Placement & Recommendation |
|---|---|---|
| **DOCX** | 100% | The safest option. Simplest for almost every legacy and modern parser to parse. |
| **PDF** | 95% | Excellent for human readers to maintain design structure. However, if created from images or without text structures, it fails completely. Selectable text must exist. |
| **RTF / TXT** | 100% | Highly parseable but looks visually unprofessional to human recruiters. Avoid. |
| **Pages / LaTeX** | Low | High risk of parsing failure. LaTeX often compiles with unusual font ligatures that render text unreadable to standard OCR engines. |

*Action:* Advise candidates to save and upload in PDF (ensuring it is NOT scanned/flat image text) or DOCX.

---

## 3. Formatting Landmines to Eliminate

- **Text Boxes:** Never wrap text, contact details, or skills lists in text boxes. Most parsers simply skip all content styled inside text boxes.
- **Tables:** Do not use tables for structural layouts or grids. While simple borderless tables can sometimes be read, complex tables with nested grids or merged columns will scramble dates and text boundaries.
- **Headers & Footers:** Do not place vital info (like contact credentials or email address) in the header/footer zones of word processor files. Some parsers ignore the header and footer margins entirely.
- **Graphics, Icons, & Emojis:** Do not include progress bars for skills (e.g., "Python: 80%"), graphs, logos, icons next to phone/email, or checkmark/star emojis as bullet points. Use standard solid round or square bullets.
- **Special Characters:** Do not use creative bullet shapes, non-standard arrows, or geometric dividers. Stick to basic ASCII/system characters.

---

## 4. Typography & Fonts

### 4.1 ATS-Friendly Fonts
Use standard, system-default fonts that have clear character spacing (kerning) and are built into every computer. Avoid decorative or downloaded custom web fonts.

- **Sans-serif (Modern/Tech/Clean):** Arial, Calibri, Helvetica, Trebuchet MS, Verdana.
- **Serif (Traditional/Formal/Executive):** Georgia, Garamond, Times New Roman, Cambria.

### 4.2 Size & Spacing Guidelines
- **Body Text:** 10pt to 12pt (never below 10pt, as it fails OCR scanning).
- **Section Headers:** 14pt to 16pt, bold.
- **Candidate Name:** 20pt to 24pt, bold.
- **Line Spacing:** 1.15 to 1.5, to prevent characters on adjacent lines from overlapping visually.
- **Margins:** 0.5 inches (minimum) to 1.0 inch (optimal) on all sides.
