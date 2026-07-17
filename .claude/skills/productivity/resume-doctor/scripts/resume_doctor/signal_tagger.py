"""
Signal Tagger — Injects controlled signal tags into resume bullets.
Uses controlled vocabulary from references/signals.json.
"""
import re
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Literal


@dataclass
class SignalTag:
    key: str
    display: str
    triggers: list[str]
    required_evidence: list[str]


SIGNALS_PATH = Path(__file__).parent.parent / "references" / "signals.json"


def load_signals() -> list[SignalTag]:
    if SIGNALS_PATH.exists():
        with open(SIGNALS_PATH) as f:
            data = json.load(f)
        return [SignalTag(**s) for s in data.get('signals', [])]
    return []


def add_signal_tags(latex: str, mode: Literal["ats-max", "designer-polish"] = "designer-polish") -> str:
    """Inject \\signaltag{} macros into experience bullets based on signal triggers."""
    signals = load_signals()
    if not signals:
        return latex

    # Find experience section
    exp_match = re.search(r'(\\section\*\{Work Experience\}(?:.*?))(?=\\section\*\{|$)', latex, re.DOTALL)
    if not exp_match:
        return latex

    exp_text = exp_match.group(1)

    # Process each bullet
    def process_bullet(match):
        bullet = match.group(0)
        text = bullet.lower()

        matched_signals = []
        for signal in signals:
            for trigger in signal.triggers:
                if trigger.lower() in text:
                    # Check required evidence
                    has_evidence = any(e.lower() in text for e in signal.required_evidence) if signal.required_evidence else True
                    if has_evidence and signal.key not in matched_signals:
                        matched_signals.append(signal.key)
                        break

        if matched_signals:
            # Inject \signaltag{} macro at end of bullet
            tags = ''.join(f'\\signaltag{{{s}}}' for s in matched_signals)
            return bullet.rstrip('.') + f' {tags}.'

        return bullet

    bullet_pattern = r'\\item\s+.*?(?=\\item|\\end\{itemize\}|$)'
    new_exp = re.sub(bullet_pattern, process_bullet, exp_text, flags=re.DOTALL)

    return latex.replace(exp_text, new_exp)


def add_signal_tags_to_latex(latex: str) -> str:
    """Convenience wrapper with default mode."""
    return add_signal_tags(latex, "designer-polish")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    latex = Path(args.resume).read_text()
    result = add_signal_tags(latex)
    Path(args.out).write_text(result)
    print(f"Signal tags injected, written to {args.out}")