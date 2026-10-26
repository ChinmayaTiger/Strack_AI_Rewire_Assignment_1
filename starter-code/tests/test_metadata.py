"""Tests for src/metadata.py (Task 2)."""
from pyspark.sql.functions import col, lit
from src.metadata import add_ingestion_metadata, METADATA_COLUMNS


def test_metadata_columns_present_and_populated(spark):
    """Assert batch_id, source_file, and ingestion_timestamp are present and non-null."""
    df_raw = (
        spark.range(2)
        .withColumn("customer_id", col("id").cast("string"))
        .withColumn("name", lit("sample_customer"))
        .drop("id")
    )

    enriched_df = add_ingestion_metadata(df_raw, "batch_1", "customers.csv")

    for col_name in METADATA_COLUMNS:
        assert col_name in enriched_df.columns, f"Missing metadata column: {col_name}"
        null_count = enriched_df.filter(col(col_name).isNull()).count()
        assert null_count == 0, f"Found {null_count} nulls in {col_name}"

    assert "customer_id" in enriched_df.columns
    assert "name" in enriched_df.columns

    assert enriched_df.filter(col("batch_id") == "batch_1").count() == 2
    assert enriched_df.filter(col("source_file") == "customers.csv").count() == 2


def test_metadata_never_overwrites_a_source_column(spark):
    """Assert collision renames original source column to source_<col>."""
    df_collision = (
        spark.range(1)
        .withColumn("customer_id", lit("C001"))
        .withColumn("batch_id", lit("legacy_source_batch_val"))
        .drop("id")
    )

    enriched_df = add_ingestion_metadata(df_collision, "authoritative_batch_1", "customers.csv")

    assert enriched_df.filter(col("batch_id") == "authoritative_batch_1").count() == 1
    assert "source_batch_id" in enriched_df.columns
    assert enriched_df.filter(col("source_batch_id") == "legacy_source_batch_val").count() == 1
    assert "customer_id" in enriched_df.columns
