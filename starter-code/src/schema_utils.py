"""Schema-drift detection and reconciliation utilities.

Guided by .claude/skills/schema_drift/SKILL.md (Task 4 and Task 6).
"""
from typing import Dict, List, Any
from datetime import datetime
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from pyspark.sql.functions import lit


def compare_schemas(existing_schema: StructType, incoming_schema: StructType) -> Dict[str, List[Any]]:
    """Return the differences between an existing (bronze) schema and an
    incoming batch's schema by column name, not position.
    """
    existing_fields = {f.name: f.dataType for f in existing_schema.fields}
    incoming_fields = {f.name: f.dataType for f in incoming_schema.fields}

    existing_names = set(existing_fields.keys())
    incoming_names = set(incoming_fields.keys())

    added_columns = sorted(list(incoming_names - existing_names))
    missing_columns = sorted(list(existing_names - incoming_names))

    type_changes = []
    common_cols = existing_names.intersection(incoming_names)
    for col in sorted(list(common_cols)):
        existing_type = existing_fields[col]
        incoming_type = incoming_fields[col]
        if existing_type != incoming_type:
            type_changes.append({
                "column": col,
                "existing_type": str(existing_type),
                "incoming_type": str(incoming_type)
            })

    return {
        "added_columns": added_columns,
        "missing_columns": missing_columns,
        "type_changes": type_changes
    }


def reconcile_schema(incoming_df: DataFrame, existing_schema: StructType) -> DataFrame:
    """Normalize an incoming DataFrame against the existing bronze schema.
    Appends any columns in existing_schema that are missing from incoming_df as nulls.
    New columns in incoming_df are retained.
    """
    result_df = incoming_df
    incoming_cols = set(incoming_df.columns)

    for field in existing_schema.fields:
        if field.name not in incoming_cols:
            result_df = result_df.withColumn(field.name, lit(None).cast(field.dataType))

    return result_df


def log_drift_event(entity: str, batch_id: str, diff: dict) -> dict:
    """Build a structured drift-event record for the audit log."""
    event = {
        "entity": entity,
        "batch_id": batch_id,
        "timestamp": datetime.now().isoformat(),
        "has_drift": bool(diff.get("added_columns") or diff.get("type_changes")),
        "added_columns": diff.get("added_columns", []),
        "missing_columns": diff.get("missing_columns", []),
        "type_changes": diff.get("type_changes", [])
    }
    return event