"""Batch ingestion entry point for a single entity/file (Task 1-2).
"""
from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from src.metadata import add_ingestion_metadata


def read_source_csv(spark: SparkSession, path: str) -> DataFrame:
    """Read one source CSV file preserving types using inferSchema and header."""
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(path)
    )


def ingest_entity(
    spark: SparkSession,
    entity: str,
    source_path: str,
    batch_id: str,
) -> DataFrame:
    """Read + tag one entity's file for one batch."""
    df_raw = read_source_csv(spark, source_path)
    file_name = Path(source_path).name
    return add_ingestion_metadata(df_raw, batch_id=batch_id, source_file=file_name)