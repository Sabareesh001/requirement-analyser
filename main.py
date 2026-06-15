"""
req_analyzer/main.py
─────────────────────
Entry point.  Usage:

    python main.py                               # uses sample/example_input.txt
    python main.py path/to/your_requirements.txt
"""

from __future__ import annotations

import importlib.util
import json
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

# Load .env before anything that reads env vars
load_dotenv()

# ── inline imports from src (avoids ModuleNotFoundError) ─────────────────────
def _import_from(rel_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(
        module_name,
        Path(__file__).parent / rel_path,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_analyzer     = _import_from("src/analyzer.py",      "analyzer")
_email_sender = _import_from("src/email_sender.py",  "email_sender")

read_requirements   = _analyzer.read_requirements
analyze_requirements = _analyzer.analyze_requirements
build_html_email    = _email_sender.build_html_email
send_email          = _email_sender.send_email

# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) > 1:
        req_file = Path(sys.argv[1])
    else:
        req_file = Path(__file__).parent / "sample" / "example_input.txt"

    print(f"\n{'='*60}")
    print("  Requirements Analyzer  –  AI-Powered Analysis & Email")
    print(f"{'='*60}\n")
    print(f"📄  Reading requirements from: {req_file}\n")

    requirements_text = read_requirements(req_file)

    first_line = next(
        (line.strip() for line in requirements_text.splitlines() if line.strip()),
        "Project"
    )
    project_name = (
        first_line.replace("Project:", "").replace("project:", "").strip()
        or "Requirements Analysis"
    )

    analysis = analyze_requirements(requirements_text)
    _print_summary(analysis)

    html = build_html_email(project_name, analysis)
    subject = f"[Requirements Analysis] {project_name}"
    send_email(subject, html)

    print(f"\n{'='*60}")
    print("  All done! ✨")
    print(f"{'='*60}\n")


def _print_summary(analysis: dict) -> None:
    labels = {
        "functional_requirements":     ("⚙️ ",  "Functional Requirements"),
        "non_functional_requirements": ("🛡️ ",  "Non-Functional Requirements"),
        "risks":                       ("⚠️ ",  "Risks"),
        "assumptions":                 ("💡 ",  "Assumptions"),
        "questions_to_client":         ("❓ ",  "Questions to Client"),
    }
    print()
    for key, (emoji, title) in labels.items():
        print(f"{emoji} {title}")
        for item in analysis[key]:
            print(f"   • {item}")
        print()


if __name__ == "__main__":
    main()