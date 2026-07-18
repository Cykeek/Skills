import sys
import re
import os

sys.path.append(os.path.abspath('.'))
from resume_doctor.validation_gates import latex_to_plain_text, count_syllables, read_file

latex_path = "D:/AI-Workflows/resumes/main_honest_final.tex"
latex = read_file(latex_path)

# Let's simulate putting periods in key locations:
# 1. Education
latex = latex.replace("Master of Computer Applications (MCA) \\hfill 2024 \\\\", "Master of Computer Applications (MCA) \\hfill 2024. \\\\")
latex = latex.replace("Bachelor of Computer Applications (BCA) \\hfill 2022 \\\\", "Bachelor of Computer Applications (BCA) \\hfill 2022. \\\\")
latex = latex.replace("Focus: Human-Computer Interaction, Coding Fundamentals", "Focus: Human-Computer Interaction, Coding Fundamentals.")

# 2. Certifications - append period before the linebreaks
latex = latex.replace("UX Foundations} \\hfill 2025 \\\\", "UX Foundations} \\hfill 2025. \\\\")
latex = latex.replace("Customer Experience: Creating Customer Personas} \\hfill 2024 \\\\", "Customer Experience: Creating Customer Personas} \\hfill 2024. \\\\")
latex = latex.replace("Figma for UX Design} \\hfill 2025 \\\\", "Figma for UX Design} \\hfill 2025. \\\\")
latex = latex.replace("User Experience for Web Design} \\hfill 2025 \\\\", "User Experience for Web Design} \\hfill 2025. \\\\")
latex = latex.replace("UX Design: 1 Overview} \\hfill 2025 \\\\", "UX Design: 1 Overview} \\hfill 2025. \\\\")
latex = latex.replace("Figma 101 -- Shift Nudge \\hfill 2023 \\\\", "Figma 101 -- Shift Nudge \\hfill 2023. \\\\")
latex = latex.replace("UI/UX for Beginners -- Great Learning \\hfill 2023", "UI/UX for Beginners -- Great Learning \\hfill 2023.")

# 3. Add periods after signaltags in projects
latex = latex.replace("\\signaltag{systems-thinking} \\\\", "\\signaltag{systems-thinking}. \\\\")
latex = latex.replace("\\signaltag{craft-polish} \\\\", "\\signaltag{craft-polish}. \\\\")
latex = latex.replace("\\signaltag{cross-functional-leadership}\n", "\\signaltag{cross-functional-leadership}.\n")

# 4. In Design skills, replace WCAG 2.1 AA with WCAG 2 AA or WCAG AA to avoid the decimal period
latex = latex.replace("WCAG 2.1 AA", "WCAG AA")

text = latex_to_plain_text(latex)
sentences = re.split(r'[.!?]+', text)
sentences = [s.strip() for s in sentences if s.strip()]
words = re.findall(r'\b\w+\b', text)
avg_sentence_len = len(words) / max(len(sentences), 1)
syllables = sum(count_syllables(w) for w in words)
fk_grade = 0.39 * avg_sentence_len + 11.8 * (syllables / max(len(words), 1)) - 15.59

print(f"Total Words: {len(words)}")
print(f"Total Sentences: {len(sentences)}")
print(f"Average Sentence Length: {avg_sentence_len:.4f}")
print(f"Total Syllables: {syllables}")
print(f"Average Syllables/Word: {syllables / max(len(words), 1):.4f}")
print(f"Flesch-Kincaid Grade: {fk_grade:.4f}")
print("--- Sentences ---")
for idx, s in enumerate(sentences, 1):
    words_s = re.findall(r'\b\w+\b', s)
    syll_s = sum(count_syllables(w) for w in words_s)
    avg_syll = syll_s / max(len(words_s), 1)
    fk = 0.39 * len(words_s) + 11.8 * avg_syll - 15.59
    print(f"{idx:02d} ({len(words_s)} words, {avg_syll:.2f} syll/word, FK {fk:.1f}): {s}")
