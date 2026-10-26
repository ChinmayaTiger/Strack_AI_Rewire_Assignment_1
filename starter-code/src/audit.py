"""Ingestion audit / evidence logging (Task 5).

Appends one JSON line per batch/entity run to config.AUDIT_LOG_PATH.
"""
import json
import time
from pathlib import Path
from .config import AUDIT_LOG_PATH


def write_audit_record(
    batch_id: str,
    entity: str,
    source_file: str,
    rows_read: int,
    rows_written: int,
    duplicates_skipped: int,
    drift_events: list,
    quarantined: int = 0,
) -> None:
    """Append one audit record as a single JSON line to AUDIT_LOG_PATH.
    Append-only and thread-safe.
    """
    record = {
        "batch_id": batch_id,
        "entity": entity,
        "source_file": source_file,
        "rows_read": rows_read,
        "rows_written": rows_written,
        "duplicates_skipped": duplicates_skipped,
        "quarantined": quarantined,
        "drift_events": drift_events,
        "logged_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    path = Path(AUDIT_LOG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")