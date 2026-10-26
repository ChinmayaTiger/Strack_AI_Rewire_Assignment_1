"""Ingestion audit / evidence logging (Task 5).

Scaffolding only - append one JSON line per batch/entity run to
config.AUDIT_LOG_PATH.
"""
import json
import time
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
    """Append one audit record. Keep this append-only and idempotent-safe
    (one record per actual run - do not silently overwrite history).

    TODO: implement the write; consider creating AUDIT_LOG_PATH.parent if it
    does not exist yet.
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
    raise NotImplementedError("write_audit_record: append `record` as one JSON line to AUDIT_LOG_PATH")
