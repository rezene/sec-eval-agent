"""Input guard: sanitization + prompt-injection defenses.

The agent's input is untrusted code, which may contain embedded instructions
aimed at the LLM (e.g. a comment saying "ignore previous instructions").
This module is the single choke point responsible for:
  - delimiting/spotlighting untrusted content before it reaches a prompt
  - stripping or flagging suspicious instruction-like patterns
  - validating that model output stays within the expected schema/shape
"""

import re

# Coarse heuristics as a first line of defense; not a substitute for
# instruction/data separation in the prompt itself.
_INJECTION_PATTERNS = [
    r"ignore (all|previous|prior|above) instructions",
    r"disregard (all|previous|prior|above)",
    r"you are now",
    r"system prompt",
    r"act as (?!a security)",
]


def spotlight(untrusted_text: str) -> str:
    """Wrap untrusted content in explicit delimiters for the prompt.

    Spotlighting makes the boundary between instructions and data explicit
    to the model, reducing (not eliminating) the chance that embedded text
    is interpreted as a command.
    """
    return f"<untrusted_code>\n{untrusted_text}\n</untrusted_code>"


def flag_suspicious_content(text: str) -> list[str]:
    """Return a list of matched injection-like patterns found in `text`."""
    hits = []
    for pattern in _INJECTION_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def sanitize_input(code: str) -> str:
    """Normalize input before it reaches the model (encoding, length, etc.)."""
    return code.strip()
