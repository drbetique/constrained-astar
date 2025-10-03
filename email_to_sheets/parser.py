from __future__ import annotations

from typing import List

from .gmail_client import EmailMessage


def email_to_row(email: EmailMessage) -> List[str]:
    subject = (email.subject or "").strip()
    sender = (email.sender or "").strip()
    body = (email.body_plain or email.snippet or "").strip()
    # Trim overly long bodies to keep sheets readable
    if len(body) > 2000:
        body = body[:2000] + "…"
    return [sender, subject, body]
