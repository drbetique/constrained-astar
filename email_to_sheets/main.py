from __future__ import annotations

import argparse
import os
from typing import List

from .config import load_settings
from .gmail_client import GmailClient
from .sheets_client import SheetsClient
from .parser import email_to_row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Email to Google Sheets automation")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to Sheets; print rows")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.dry_run:
        os.environ["DRY_RUN"] = "1"

    settings = load_settings()

    gmail = GmailClient(settings)
    message_ids: List[str] = []
    try:
        message_ids = gmail.list_message_ids()
    except Exception as exc:
        print(f"Failed to list messages: {exc}")
        return 2

    rows: List[List[str]] = []
    processed_ids: List[str] = []
    for mid in message_ids:
        try:
            em = gmail.get_message(mid)
            rows.append(email_to_row(em))
            processed_ids.append(mid)
        except Exception as exc:
            print(f"Failed to fetch/parse message {mid}: {exc}")

    if settings.dry_run:
        print("Dry run - rows that would be appended:")
        for r in rows:
            print(r)
        return 0

    if rows:
        try:
            sheets = SheetsClient(settings)
            resp = sheets.append_rows(rows)
            updated = resp.get("updates", {}).get("updatedRows", 0)
            print(f"Appended {updated} rows to {settings.sheet_range}")
        except Exception as exc:
            print(f"Failed to append to sheet: {exc}")
            return 3

    # Post-process: add label and mark as read
    if settings.gmail_processed_label:
        for mid in processed_ids:
            try:
                gmail.add_label(mid, settings.gmail_processed_label)
                gmail.mark_as_read(mid)
            except Exception as exc:
                print(f"Failed to post-process message {mid}: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
