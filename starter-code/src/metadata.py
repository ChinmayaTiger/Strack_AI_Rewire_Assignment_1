"""Ingestion metadata tagging.

Guided by .claude/skills/ingestion_metadata/SKILL.md (Task 2).
"""
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, current_timestamp

METADATA_COLUMNS = ["batch_id", "source_file", "ingestion_timestamp"]


def add_ingestion_metadata(
    df: DataFrame,
    batch_id: str,
    source_file: str,
) -> DataFrame:
    """Attach batch_id, source_file and ingestion_timestamp to every row,
    preserving all original columns unchanged.
    """
    # Defensive check against collision with source columns
    for col_name in METADATA_COLUMNS:
        if col_name in df.columns:
            df = df.withColumnRenamed(col_name, f"source_{col_name}")

    return (
        df.withColumn("batch_id", lit(batch_id))
        .withColumn("source_file", lit(source_file))
        .withColumn("ingestion_timestamp", current_timestamp())
    )