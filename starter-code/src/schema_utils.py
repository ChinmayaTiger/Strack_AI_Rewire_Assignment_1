"""Schema-drift detection and reconciliation utilities.

Scaffolding only - read .claude/skills/schema_drift/SKILL.md before filling these in
(Task 4). For Task 6 you will modify that skill; make sure this module keeps
working with your modified guidance too, not just the original.
"""
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType


def compare_schemas(existing_schema: StructType, incoming_schema: StructType) -> dict:
    """Return the differences between an existing (bronze) schema and an
    incoming batch's schema.

    TODO: implement, returning something like
        {"added_columns": [...], "missing_columns": [...], "type_changes": [...]}
    Compare by column NAME, not position (see skill's Common Mistakes).
    """
    raise NotImplementedError("compare_schemas: see .claude/skills/schema_drift/SKILL.md")


def reconcile_schema(incoming_df: DataFrame, existing_schema: StructType) -> DataFrame:
    """Normalize an incoming DataFrame against the existing bronze schema:
    add missing columns as typed nulls, and decide what to do with new
    columns (Batch 3's loyalty_tier, and - after you modify the skill -
    Batch 4's marketing_opt_in on top of an already-evolved schema).

    TODO: implement.
    """
    raise NotImplementedError("reconcile_schema: see .claude/skills/schema_drift/SKILL.md")


def log_drift_event(entity: str, batch_id: str, diff: dict) -> dict:
    """Build a structured drift-event record for the audit log (Task 4/5).

    TODO: implement and wire into src/audit.py.
    """
    raise NotImplementedError("log_drift_event: see .claude/skills/schema_drift/SKILL.md")
