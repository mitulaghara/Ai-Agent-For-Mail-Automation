# Bulk Mail Sender (simple)

This project provides a minimal Flask web UI and a CLI to send bulk emails from a CSV file.

Setup

1. Create a virtualenv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set your SMTP credentials.

Usage - Web UI

```bash
export FLASK_APP=app.py
flask run
# or: python app.py
```
Open http://localhost:5000 in your browser, upload a CSV with an `email` column, enter subject and body, then send. Use `{{name}}` in the body to personalize from the `name` column.

Usage - CLI

```bash
python send_bulk.py recipients.csv --subject "Hello" --body "Hi {{name}}, ..."
```

Notes and next steps

- For production, use an email provider API (SendGrid, Mailgun) or implement OAuth for Gmail to avoid storing passwords.
- Be mindful of SMTP rate limits and spam rules.
- This is a simple starter; ask me to add scheduling, retry logic, or provider integrations.
