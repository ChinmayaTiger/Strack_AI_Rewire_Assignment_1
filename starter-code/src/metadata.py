"""Ingestion metadata tagging.

Scaffolding only - read .claude/skills/ingestion_metadata/SKILL.md before filling
this in (Task 2).
"""
from pyspark.sql import DataFrame


def add_ingestion_metadata(
    df: DataFrame,
    batch_id: str,
    source_file: str,
) -> DataFrame:
    """Attach batch_id, source_file and ingestion_timestamp to every row,
    preserving all original columns unchanged.

    TODO: implement. Watch for the collision case the skill itself warns
    about under Common Mistakes: what should happen if a source column is
    already named batch_id/source_file/ingestion_timestamp?
    """
    raise NotImplementedError("add_ingestion_metadata: see .claude/skills/ingestion_metadata/SKILL.md")
