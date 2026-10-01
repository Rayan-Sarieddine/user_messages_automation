"""File-backed persistence for triage records.

Stands in for "a Google Sheet or any persistent destination" per the
assessment (step 5) — a single JSON array is enough for this exercise and
keeps the demo dependency-free. Swapping this for a real database or a
Google Sheets append call later is a one-file change.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import List

from arcvault_ai.schemas import TriageRecord

_LOCK = threading.Lock()
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_DATA_FILE = _DATA_DIR / "records.json"


def _ensure_file() -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not _DATA_FILE.exists():
        _DATA_FILE.write_text("[]")


def save_record(record: TriageRecord) -> None:
    with _LOCK:
        _ensure_file()
        records = json.loads(_DATA_FILE.read_text())
        records.append(record.model_dump(mode="json"))
        _DATA_FILE.write_text(json.dumps(records, indent=2))


def list_records() -> List[dict]:
    _ensure_file()
    return json.loads(_DATA_FILE.read_text())
