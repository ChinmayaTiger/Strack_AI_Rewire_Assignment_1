"""Idempotent bronze write logic.

Guided by .claude/skills/idempotency/SKILL.md (Task 3).
"""
from pathlib import Path
from typing import Optional
from pyspark.sql import DataFrame, SparkSession


def read_existing_keys(spark: SparkSession, bronze_path: str, business_key: str) -> Optional[DataFrame]:
    """Return DataFrame containing only distinct business keys already present
    in bronze for this entity, or None if the bronze table does not exist yet.
    """
    p = Path(bronze_path)
    if not p.exists():
        return None

    has_parquet = any(p.glob("*.parquet")) or any(p.glob("**/*.parquet"))
    if not has_parquet:
        return None

    try:
        # Read parquet with schema merging enabled
        existing_df = (
            spark.read
            .option("mergeSchema", "true")
            .parquet(bronze_path)
        )
        if business_key in existing_df.columns:
            return existing_df.select(business_key).distinct()
        return None
    except Exception:
        return None


def dedup_against_existing(incoming_df: DataFrame, existing_keys: Optional[DataFrame], business_key: str) -> DataFrame:
    """Filter out rows from incoming_df whose business_key already exists in existing_keys.
    Uses left_anti join to drop redelivered keys.
    """
    if existing_keys is None:
        return incoming_df

    return incoming_df.join(
        existing_keys,
        on=business_key,
        how="left_anti"
    )


def write_bronze(df: DataFrame, bronze_path: str) -> None:
    """Append the deduplicated batch to the bronze Parquet storage.
    Enables mergeSchema on write path.
    """
    if df.limit(1).count() == 0:
        return

    (
        df.write
        .mode("append")
        .option("mergeSchema", "true")
        .format("parquet")
        .save(bronze_path)
    )