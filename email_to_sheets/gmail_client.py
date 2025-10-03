from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Dict, List, Optional
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import OAUTH_SCOPES, Settings


@dataclass
class EmailMessage:
    id: str
    thread_id: str
    subject: str
    sender: str
    snippet: str
    body_plain: str


class GmailClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._service = None

    def _get_service(self):
        if self._service is not None:
            return self._service

        creds: Optional[Credentials] = None
        if os.path.exists(self.settings.token_file):
            creds = Credentials.from_authorized_user_file(self.settings.token_file, OAUTH_SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.settings.credentials_file, OAUTH_SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.settings.token_file, "w") as token:
                token.write(creds.to_json())

        self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def list_message_ids(self) -> List[str]:
        service = self._get_service()
        results = service.users().messages().list(
            userId=self.settings.gmail_user_id,
            q=self.settings.gmail_query,
            maxResults=self.settings.gmail_max_messages,
        ).execute()
        messages = results.get("messages", [])
        return [m["id"] for m in messages]

    def get_message(self, message_id: str) -> EmailMessage:
        service = self._get_service()
        msg = service.users().messages().get(
            userId=self.settings.gmail_user_id, id=message_id, format="full"
        ).execute()

        headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
        subject = headers.get("subject", "")
        sender = headers.get("from", "")
        snippet = msg.get("snippet", "")
        body_plain = self._extract_plain_text(msg.get("payload", {}))

        return EmailMessage(
            id=msg["id"],
            thread_id=msg.get("threadId", ""),
            subject=subject,
            sender=sender,
            snippet=snippet,
            body_plain=body_plain,
        )

    def _extract_plain_text(self, payload: Dict) -> str:
        # Walk MIME tree for text/plain
        def walk_parts(part: Dict) -> Optional[str]:
            mime_type = part.get("mimeType", "")
            body = part.get("body", {})
            data = body.get("data")
            if mime_type == "text/plain" and data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
            for sub in part.get("parts", []) or []:
                maybe = walk_parts(sub)
                if maybe:
                    return maybe
            return None

        text = walk_parts(payload)
        return text or ""

    def add_label(self, message_id: str, label_name: str) -> None:
        service = self._get_service()
        # Find or create label
        labels_resp = service.users().labels().list(userId=self.settings.gmail_user_id).execute()
        label_id = None
        for lbl in labels_resp.get("labels", []):
            if lbl.get("name") == label_name:
                label_id = lbl.get("id")
                break
        if not label_id:
            created = (
                service.users()
                .labels()
                .create(userId=self.settings.gmail_user_id, body={"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"})
                .execute()
            )
            label_id = created.get("id")

        service.users().messages().modify(
            userId=self.settings.gmail_user_id,
            id=message_id,
            body={"addLabelIds": [label_id]},
        ).execute()

    def mark_as_read(self, message_id: str) -> None:
        service = self._get_service()
        service.users().messages().modify(
            userId=self.settings.gmail_user_id,
            id=message_id,
            body={"removeLabelIds": ["UNREAD"]},
        ).execute()
