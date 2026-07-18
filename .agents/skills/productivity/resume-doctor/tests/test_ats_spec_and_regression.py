import unittest
import tempfile
import os
from pathlib import Path

from resume_doctor.ats_audit import run_ats_audit
from resume_doctor.validation_gates import (
    ATS_SECTION_ONTOLOGY,
    validate_parser_simulation,
    repair_kerning_splits
)
from resume_doctor.latex_builder import ensure_engine_safe_preamble, escape_latex_special_chars
from resume_doctor.profile_builder import parse_latex_resume


class TestATSEngineSpecAndRegression(unittest.TestCase):
    def test_canonical_section_ontology(self):
        """Test that non-standard headers map properly to canonical ATS namespaces."""
        self.assertIn(r'Employment', ATS_SECTION_ONTOLOGY["WORK_EXPERIENCE"])
        self.assertIn(r'Career History', ATS_SECTION_ONTOLOGY["WORK_EXPERIENCE"])
        self.assertIn(r'Academic Background', ATS_SECTION_ONTOLOGY["EDUCATION"])
        self.assertIn(r'Executive Summary', ATS_SECTION_ONTOLOGY["SUMMARY"])

    def test_engine_safe_preamble_no_regex_escape_error(self):
        """Test ensure_engine_safe_preamble wraps glyphtounicode cleanly without re.sub escape errors."""
        raw_latex = r"""\documentclass{article}
\input{glyphtounicode}
\pdfgentounicode=1
\begin{document}
Test
\end{document}"""
        guarded = ensure_engine_safe_preamble(raw_latex)
        self.assertIn(r"\ifPDFTeX", guarded)
        self.assertIn(r"\input{glyphtounicode}", guarded)
        self.assertIn(r"\pdfgentounicode=1", guarded)
        self.assertIn(r"\fi", guarded)

    def test_escape_latex_special_chars(self):
        """Test escaping reserved special characters."""
        input_text = "C++ & Python % $ # _ test"
        escaped = escape_latex_special_chars(input_text)
        self.assertEqual(escaped, r"C++ \& Python \% \$ \# \_ test")

    def test_ats_audit_scoring_weights(self):
        """Test Multi-Factor Weighted ATS scoring formula (25% each factor)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, "test_resume.tex")
            content = r"""\documentclass{article}
\usepackage{microtype}
\usepackage{iftex}
\ifPDFTeX
  \input{glyphtounicode}
  \pdfgentounicode=1
\fi
\begin{document}
\section*{Professional Summary}
Senior software engineer with 10 years experience.
\section*{Work Experience}
\contactline{test@example.com}{555-0100}{Remote}{}{}
\item Led backend team using Python and Kubernetes.
\section*{Skills}
\item \textbf{Technical:} \kw{Python}, \kw{Kubernetes}
\section*{Education}
12/2018 BS Computer Science
\end{document}"""
            Path(tex_path).write_text(content, encoding="utf-8")
            audit = run_ats_audit(tex_path)
            self.assertIsNotNone(audit.factor_scores)
            self.assertIn("lexical_cleanliness", audit.factor_scores)
            self.assertIn("structural_readiness", audit.factor_scores)
            self.assertIn("keyword_hygiene_prominence", audit.factor_scores)
            self.assertIn("readability_recency", audit.factor_scores)
            # Verify overall_score equals equal weighting of the 4 factors
            fs = audit.factor_scores
            expected_score = int(
                0.25 * fs["lexical_cleanliness"] +
                0.25 * fs["structural_readiness"] +
                0.25 * fs["keyword_hygiene_prominence"] +
                0.25 * fs["readability_recency"]
            )
            self.assertEqual(audit.overall_score, expected_score)

    def test_profile_builder_fallback(self):
        """Test parse_latex_resume fallback behavior for standard sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, "standard.tex")
            content = r"""\documentclass{article}
\author{Jane Doe}
\begin{document}
\section*{Work Experience}
\item Architected distributed systems in Python.
\section*{Skills}
\item Python, Distributed Systems, SQL
\end{document}"""
            Path(tex_path).write_text(content, encoding="utf-8")
            data = parse_latex_resume(tex_path)
            self.assertEqual(data["name"], "Jane Doe")
            self.assertGreaterEqual(len(data["experience"]), 1)
            self.assertIn("Architected distributed systems in Python.", data["experience"][0]["bullets"])


if __name__ == "__main__":
    unittest.main()
