from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

# Load variables from a local .env if present
load_dotenv()


# OAuth scopes required for this app
OAUTH_SCOPES: List[str] = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "t", "yes", "y"}


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    # OAuth client JSON and user token cache
    credentials_file: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    token_file: str = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

    # Gmail
    gmail_user_id: str = os.getenv("GMAIL_USER_ID", "me")
    gmail_query: str = os.getenv("GMAIL_QUERY", "is:unread")
    gmail_max_messages: int = _as_int(os.getenv("GMAIL_MAX_MESSAGES"), 20)
    gmail_processed_label: str | None = os.getenv("GMAIL_PROCESSED_LABEL")

    # Google Sheets
    spreadsheet_id: str = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
    sheet_range: str = os.getenv("GOOGLE_SHEETS_RANGE", "Sheet1!A1")
    value_input_option: str = os.getenv("GOOGLE_SHEETS_VALUE_INPUT_OPTION", "USER_ENTERED")

    # Behavior flags
    dry_run: bool = _as_bool(os.getenv("DRY_RUN"), False)


def load_settings() -> Settings:
    settings = Settings()
    # Allow missing spreadsheet when running in dry-run mode
    if not settings.spreadsheet_id and not settings.dry_run:
        raise RuntimeError(
            "GOOGLE_SHEETS_SPREADSHEET_ID is required (omit only when DRY_RUN=1)."
        )
    return settings
