#!/usr/bin/env python3
"""Email the premarket report via AgentMail (https://agentmail.to).

Converts the report markdown to HTML (markdown lib, plain-text fallback)
and sends it through the AgentMail API. Needs in .env or the environment:
  AGENTMAIL_API_KEY   - API key from the AgentMail console
  AGENTMAIL_INBOX     - sending inbox id, e.g. zenith@agentmail.to
  REPORT_EMAIL_TO     - optional, defaults to Quy's gmail

No key = exit 0 with a clear message, never a crash: the workflow then
falls back to a Gmail draft via the connector and says so in Telegram.

Usage: send_report.py reports/premarket_YYYY-MM-DD.md ["Subject line"]
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TO = "thienquypham05@gmail.com"
API = "https://api.agentmail.to/v0"


def load_env():
    envfile = REPO / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: send_report.py <report.md> [subject]")
    path = Path(sys.argv[1])
    if not path.exists():
        raise SystemExit(f"report not found: {path}")
    text = path.read_text()
    subject = (sys.argv[2] if len(sys.argv) > 2
               else f"Zenith premarket report - {path.stem.replace('premarket_', '')}")

    load_env()
    key = os.environ.get("AGENTMAIL_API_KEY")
    inbox = os.environ.get("AGENTMAIL_INBOX")
    to = os.environ.get("REPORT_EMAIL_TO", DEFAULT_TO)
    if not key or not inbox:
        print("send_report: skipped, AGENTMAIL_API_KEY/AGENTMAIL_INBOX not "
              "set. Create an inbox at agentmail.to and add both to .env; "
              "until then use the Gmail-draft fallback.")
        return

    try:
        import markdown
        html = markdown.markdown(text, extensions=["tables"])
        html = f'<div style="font-family:sans-serif;max-width:720px">{html}</div>'
    except ImportError:
        html = None

    payload = {"to": [to], "subject": subject, "text": text}
    if html:
        payload["html"] = html
    req = urllib.request.Request(
        f"{API}/inboxes/{inbox}/messages/send",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.load(r)
        print(f"send_report: sent to {to} "
              f"(message_id {resp.get('message_id', '?')})")
    except Exception as e:
        # never crash the workflow over a notification; the report is
        # already committed to the repo either way
        print(f"send_report: FAILED - {e}. Report stays in the repo; "
              "use the Gmail-draft fallback.")


if __name__ == "__main__":
    main()
