"""Batch ingestion entry point for a single entity/file (Task 1-2).

Scaffolding only.
"""
from pyspark.sql import DataFrame, SparkSession


def read_source_csv(spark: SparkSession, path: str) -> DataFrame:
    """Read one source CSV file.

    TODO: decide on an explicit schema vs. inferSchema (see the schema-drift
    skill's guidance on why inference is risky for production ingestion) and
    implement accordingly.
    """
    raise NotImplementedError("read_source_csv: implement CSV read")


def ingest_entity(
    spark: SparkSession,
    entity: str,
    source_path: str,
    batch_id: str,
) -> DataFrame:
    """Read + tag one entity's file for one batch. Wire together
    read_source_csv -> schema_utils -> metadata.add_ingestion_metadata here,
    then hand the result to idempotent_writer / data_quality from
    pipeline.py.

    TODO: implement.
    """
    raise NotImplementedError("ingest_entity: wire read -> schema drift -> metadata")
