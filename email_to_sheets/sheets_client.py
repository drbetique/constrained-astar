from __future__ import annotations

import os
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import OAUTH_SCOPES, Settings


class SheetsClient:
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

        self._service = build("sheets", "v4", credentials=creds)
        return self._service

    def append_rows(self, values: List[List[str]]) -> dict:
        if not values:
            return {"updates": {"updatedRows": 0}}
        service = self._get_service()
        body = {"values": values}
        return (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.settings.spreadsheet_id,
                range=self.settings.sheet_range,
                valueInputOption=self.settings.value_input_option,
                body=body,
            )
            .execute()
        )
