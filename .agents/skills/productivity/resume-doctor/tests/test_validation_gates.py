import os
import tempfile
import unittest
import sys

# Ensure package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from resume_doctor.validation_gates import validate_latex_format, _is_in_pdf_guard


BASE_VALID_LATEX = r"""\documentclass[10pt,a4paper]{article}
\usepackage{cmap}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={Resume}}
\emergencystretch=3em

~GUARD_SECTION~

\begin{document}
\contactline{test@example.com}
\section*{Professional Summary}
Senior Software Engineer with 10+ years experience.
\section*{Skills}
Python, LaTeX, ATS optimization.
\section*{Work Experience}
01/2020 – Present: Lead Engineer at Tech Corp.
\section*{Education}
09/2015 – 05/2019: BS in Computer Science.
~BODY_EXTRA~
\end{document}
"""


class TestValidateLatexFormat(unittest.TestCase):
    def _run_validate(self, latex_content: str):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
            f.write(latex_content)
            temp_path = f.name
        try:
            return validate_latex_format(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_clean_ifpdf_guard_passes(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", "")
        result = self._run_validate(latex)
        self.assertTrue(result.passed, f"Expected clean \\ifpdf guard to pass, got issues: {result.details['issues']}")

    def test_clean_ifpdftex_guard_passes(self):
        guard = r"""\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", "")
        result = self._run_validate(latex)
        self.assertTrue(result.passed, f"Expected clean \\ifPDFTeX guard to pass, got issues: {result.details['issues']}")

    def test_unguarded_glyphtounicode_fails(self):
        guard = r"""\input{glyphtounicode}
\pdfgentounicode=1"""
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", "")
        result = self._run_validate(latex)
        self.assertFalse(result.passed)
        self.assertTrue(any("glyphtounicode" in s for s in result.details["issues"]))

    def test_unescaped_ampersand_in_body_fails(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        body_extra = "Led engineering teams at AT&T with high impact."
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        self.assertFalse(result.passed)
        self.assertTrue(any("Unescaped '&'" in s for s in result.details["issues"]), f"Issues found: {result.details['issues']}")

    def test_escaped_ampersand_in_body_passes(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        body_extra = r"Led engineering teams at AT\&T with high impact."
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        self.assertTrue(result.passed, f"Expected escaped ampersand to pass, got: {result.details['issues']}")

    def test_ampersand_inside_tabular_passes(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        # Note: tabular environment itself triggers ATS layout warning/issue if present,
        # but let's verify that the Unescaped '&' check specifically does not trigger inside tabular.
        body_extra = r"""\begin{tabular}{ll}
ColA & ColB \\
\end{tabular}"""
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        # Should not have any "Unescaped '&'" issue
        self.assertFalse(any("Unescaped '&'" in s for s in result.details["issues"]), f"Issues: {result.details['issues']}")

    def test_unescaped_percent_in_body_fails(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        body_extra = "Increased profit by 25% across all teams."
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        self.assertFalse(result.passed)
        self.assertTrue(any("Unescaped '%'" in s for s in result.details["issues"]), f"Issues found: {result.details['issues']}")

    def test_escaped_percent_in_body_passes(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        body_extra = r"Increased profit by 25\% across all teams."
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        self.assertTrue(result.passed, f"Expected escaped percent to pass, got: {result.details['issues']}")

    def test_comment_line_percent_passes(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        body_extra = "% This is a comment line explaining next section"
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        self.assertTrue(result.passed, f"Expected comment line to pass, got: {result.details['issues']}")

    def test_unescaped_hash_in_body_fails(self):
        guard = r"""\ifpdf
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        body_extra = "Ranked #1 engineer across division."
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", body_extra)
        result = self._run_validate(latex)
        self.assertFalse(result.passed)
        self.assertTrue(any("Unescaped '#'" in s for s in result.details["issues"]), f"Issues found: {result.details['issues']}")


class TestOverleafCompilationHelpers(unittest.TestCase):
    def test_escape_latex_special_chars(self):
        from resume_doctor import escape_latex_special_chars
        sample = "R&D engineer with 50% increase $100k budget #1 ranking file_name"
        escaped = escape_latex_special_chars(sample)
        self.assertIn(r"\&", escaped)
        self.assertIn(r"\%", escaped)
        self.assertIn(r"\$", escaped)
        self.assertIn(r"\#", escaped)
        self.assertIn(r"\_", escaped)
        # Double escaping check
        re_escaped = escape_latex_special_chars(escaped)
        self.assertEqual(escaped, re_escaped)

    def test_ensure_engine_safe_preamble(self):
        from resume_doctor import ensure_engine_safe_preamble
        raw_latex = r"""\documentclass{article}
\input{glyphtounicode}
\pdfgentounicode=1
\begin{document}
Test
\end{document}"""
        safe = ensure_engine_safe_preamble(raw_latex)
        self.assertIn(r"\usepackage{iftex}", safe)
        self.assertIn(r"\ifPDFTeX", safe)
        self.assertIn(r"\usepackage{microtype}", safe)


class TestKerningRepair(unittest.TestCase):
    def test_repair_kerning_splits_consonants(self):
        from resume_doctor.latex_builder import repair_kerning_splits
        input_text = "T echnical & F rontend Fluency: M anagement of systems. A great team where I am lead."
        expected = "Technical & Frontend Fluency: Management of systems. A great team where I am lead."
        self.assertEqual(repair_kerning_splits(input_text), expected)

    def test_repair_kerning_splits_A_and_I_stems(self):
        from resume_doctor.latex_builder import repair_kerning_splits
        input_text = "A rchitecture & A ccessibility with I nteractive I nformation."
        expected = "Architecture & Accessibility with Interactive Information."
        self.assertEqual(repair_kerning_splits(input_text), expected)

    def test_normalize_extracted_text_fixes_kerning(self):
        from resume_doctor.validation_gates import normalize_extracted_text
        raw_text = "T echnical & F rontend Fluency\n\nA rchitecture"
        normalized = normalize_extracted_text(raw_text)
        self.assertIn("Technical & Frontend Fluency", normalized)
        self.assertIn("Architecture", normalized)


class TestSubagentHarness(unittest.TestCase):
    def _run_harness(self, latex_content: str):
        from resume_doctor.validation_gates import validate_subagent_harness
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
            f.write(latex_content)
            temp_path = f.name
        try:
            return validate_subagent_harness(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            norm = temp_path.replace(".tex", ".normalized.txt")
            if os.path.exists(norm):
                os.unlink(norm)

    def test_clean_latex_passes_all_subagents(self):
        guard = r"""\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", r"Clean text with AT\&T and 100\% metric.")
        report = self._run_harness(latex)
        self.assertTrue(report["overall_passed"], f"Expected overall_passed=True, got subagent results: {report['subagents']}")

    def test_unescaped_char_fails_s2(self):
        guard = r"""\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi"""
        latex = BASE_VALID_LATEX.replace("~GUARD_SECTION~", guard).replace("~BODY_EXTRA~", "Clean text with AT&T unescaped.")
        report = self._run_harness(latex)
        self.assertFalse(report["overall_passed"])
        self.assertEqual(report["subagents"]["char_escaping"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
