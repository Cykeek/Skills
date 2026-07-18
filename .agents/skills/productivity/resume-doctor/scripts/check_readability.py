import sys
import re
import os

sys.path.append(os.path.abspath('.'))
from resume_doctor.validation_gates import latex_to_plain_text, count_syllables, read_file

latex_path = "D:/AI-Workflows/resumes/main_honest_final.tex"
text = latex_to_plain_text(read_file(latex_path))
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
