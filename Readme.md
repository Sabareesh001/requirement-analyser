# Requirements Analyzer 🤖

AI-powered automation that reads a project requirements file, analyses it with
**Groq Cloud (openai/gpt-oss-120b)**, and emails a beautifully formatted HTML report via
**Gmail SMTP**.

---

## Project Structure

```
req_analyzer/
├── main.py                  ← Entry point
├── requirements.txt         ← Python dependencies
├── env.example              ← Template for secrets (copy → .env)
├── src/
│   ├── analyzer.py          ← Reads file + calls Groq Cloud API
│   └── email_sender.py      ← Builds HTML email + sends via SMTP
└── sample/
    └── requirements.txt     ← Demo requirements file
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp env.example .env
# Then open .env and fill in your real values
```

Your `.env` file needs:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq Cloud API key |
| `GMAIL_SENDER` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | 16-char Gmail App Password (not your login password) |
| `RECIPIENT_EMAIL` | Email address to send the report to |

> **Gmail App Password:**  
> Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords),
> generate a password for "Mail", and paste it into `.env`.
> Two-Factor Authentication must be enabled on your Google account.

---

## Usage

```bash
# Use the bundled sample requirements file
python main.py

# Use your own file
python main.py path/to/your_requirements.txt
```

---

## What the AI generates

| Section | Description |
|---|---|
| ⚙️ Functional Requirements | What the system must do |
| 🛡️ Non-Functional Requirements | Performance, security, availability etc. |
| ⚠️ Risks | Potential issues & blockers |
| 💡 Assumptions | Things taken for granted |
| ❓ Questions to Client | Clarifications needed |

---

## Security Notes

- **Never commit `.env`** – it's already listed in `.gitignore`
- Use a **Gmail App Password**, never your real Gmail password
- The `GROQ_API_KEY` is read only at runtime from the environment