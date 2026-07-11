import sys
import os
import re

# Banned opening patterns (case-insensitive regex)
# These represent sentence or line openers.
BANNED_OPENERS = [
    (re.compile(r"(?:^|[\.\?\!]\s+)(in today's|in todays|in this article|in this post|in this blog|as we all know|it is important to understand|it is important to note|the \w+ landscape is evolving|landscape is evolving)\b", re.IGNORECASE),
     "Banned opening/filler pattern found: '{match}'"),
]

# Common robotic/filler tells
ROBOTIC_TELLS = [
    (re.compile(r"\bin order to\b", re.IGNORECASE), "Robotic/filler tell: 'in order to' (use 'to' instead)"),
    (re.compile(r"\bmoreover\b", re.IGNORECASE), "Robotic/filler tell: 'moreover'"),
    (re.compile(r"\bfurthermore\b", re.IGNORECASE), "Robotic/filler tell: 'furthermore'"),
    (re.compile(r"\butiliz\w*\b", re.IGNORECASE), "Robotic/filler tell: 'utilize' or one of its variants (use 'use' instead)"),
    (re.compile(r"\bleverag\w*\b", re.IGNORECASE), "Robotic/filler tell: 'leverage' or one of its variants as a verb"),
    (re.compile(r"\bfacilitat\w*\b", re.IGNORECASE), "Robotic/filler tell: 'facilitate' or one of its variants"),
]

# Formal structures (noncontractions)
FORMAL_PHRASES = [
    (re.compile(r"\bdo not\b", re.IGNORECASE), "do not"),
    (re.compile(r"\bwill not\b", re.IGNORECASE), "will not"),
    (re.compile(r"\bcannot\b", re.IGNORECASE), "cannot"),
    (re.compile(r"\bit is\b", re.IGNORECASE), "it is"),
]

def lintfile(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    print(f"Linting content in: {file_path}")
    print("-" * 60)

    warnings_count = 0
    formal_phrases_count = 0
    total_words = 0

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        clean_line = line.strip()
        # Count words
        words = clean_line.split()
        total_words += len(words)

        # 1. Check for em dashes (—)
        if "—" in line:
            # Exclude lines discussing the ban itself in reference files
            if "ban" in line.lower() or "forbidden" in line.lower() or "rule" in line.lower() or "exception" in line.lower() or "em dash" in line.lower():
                pass
            else:
                print(f"[{idx}] Warning: Em dash (—) found. Rephrase using commas, parentheses, colons, or periods.")
                warnings_count += 1

        # 2. Check for banned opening patterns
        for pattern, message_template in BANNED_OPENERS:
            for match in pattern.finditer(line):
                matched_text = match.group(1)
                print(f"[{idx}] Warning: {message_template.format(match=matched_text)}")
                warnings_count += 1

        # 3. Check for robotic tells
        for pattern, message in ROBOTIC_TELLS:
            if pattern.search(line):
                print(f"[{idx}] Warning: {message}")
                warnings_count += 1

        # 4. Check for formal structures/non-contractions
        for pattern, phrase in FORMAL_PHRASES:
            matches = pattern.findall(line)
            if matches:
                formal_phrases_count += len(matches)
                print(f"[{idx}] Alert: Formal structure '{phrase}' found. Consider using a contraction.")

    # Density analysis
    if total_words > 0:
        formal_density = (formal_phrases_count / total_words) * 100
    else:
        formal_density = 0.0

    print("-" * 60)
    print(f"Total Words: {total_words}")
    print(f"Total Warnings/Alerts: {warnings_count + formal_phrases_count}")
    print(f"Formal Non-Contraction count: {formal_phrases_count} ({formal_density:.2f}% density)")
    
    # Flag high density of formal structures (e.g. > 0.5% density)
    if formal_density > 0.5:
        print(f"Warning: High density of formal structures without contractions ({formal_density:.2f}%).")
        print("To sound more natural/conversational, aim for ~70-80% contraction usage for eligible phrases.")

    if warnings_count == 0 and formal_density <= 0.5:
        print("Linting passed cleanly!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_content.py <path_to_markdown_file>")
        sys.exit(1)
    
    lintfile(sys.argv[1])
