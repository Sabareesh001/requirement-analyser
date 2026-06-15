"""
req_analyzer/src/analyzer.py
────────────────────────────
Reads a requirements text file and calls Groq Cloud (openai/gpt-oss-120b)
to produce structured analysis (FR, NFR, Risks, Assumptions,
Questions to Client).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from groq import Groq

# ── System prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are a Senior Business Analyst and Software Architect.
Analyse the project requirements provided by the user and respond with a
JSON object that has EXACTLY these five keys:

{
  "functional_requirements": ["..."],   // list of strings
  "non_functional_requirements": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "questions_to_client": ["..."]
}

Rules:
- Each list must contain at least 5 items.
- Write every item as a clear, concise sentence.
- Return ONLY the JSON object — no markdown, no commentary.
""".strip()


# ── Public API ────────────────────────────────────────────────────────────────

def read_requirements(file_path: str | Path) -> str:
    """Read the raw requirements text from *file_path*."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Requirements file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def analyze_requirements(requirements_text: str) -> dict:
    """
    Send *requirements_text* to Groq Cloud (openai/gpt-oss-120b) and return a
    structured dict with keys: functional_requirements,
    non_functional_requirements, risks, assumptions, questions_to_client.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set in the environment.")

    client = Groq(api_key=api_key)

    print("🤖  Sending requirements to Groq Cloud (openai/gpt-oss-120b) …")
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": requirements_text},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Groq returned non-JSON content:\n{raw}"
        ) from exc

    _validate_structure(result)
    print("✅  Analysis received and validated.")
    return result


# ── Internal helpers ──────────────────────────────────────────────────────────

REQUIRED_KEYS = {
    "functional_requirements",
    "non_functional_requirements",
    "risks",
    "assumptions",
    "questions_to_client",
}


def _validate_structure(data: dict) -> None:
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(f"AI response is missing keys: {missing}")
    for key in REQUIRED_KEYS:
        if not isinstance(data[key], list) or not data[key]:
            raise ValueError(f"'{key}' must be a non-empty list.")