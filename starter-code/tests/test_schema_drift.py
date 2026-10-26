"""Tests for src/schema_utils.py (Task 4 & Task 6)."""
from pyspark.sql.functions import col
from src.config import BATCH_1_FILES, BATCH_3_DIR, BATCH_4_DIR
from src.ingest import ingest_entity
from src.idempotent_writer import write_bronze
from src.schema_utils import compare_schemas, reconcile_schema, log_drift_event


def test_batch_3_loyalty_tier_detected_and_backfilled(spark, tmp_path):
    """Ingest Batch 1 then Batch 3; verify loyalty_tier is backfilled null for Batch 1."""
    cust_file = str(BATCH_1_FILES["customers"])
    b3_file = str(BATCH_3_DIR / "customers_batch3_loyalty_tier.csv")
    bronze_path = str(tmp_path / "customers")

    # Ingest Batch 1
    df_b1 = ingest_entity(spark, "customers", cust_file, "batch_1")
    write_bronze(df_b1, bronze_path)

    # Ingest Batch 3 with schema drift
    df_b3 = ingest_entity(spark, "customers", b3_file, "batch_3")
    existing_bronze = spark.read.option("mergeSchema", "true").parquet(bronze_path)

    diff = compare_schemas(existing_bronze.schema, df_b3.schema)
    assert "loyalty_tier" in diff["added_columns"]

    reconciled_b3 = reconcile_schema(df_b3, existing_bronze.schema)
    write_bronze(reconciled_b3, bronze_path)

    # Validate merged Bronze
    merged_df = spark.read.option("mergeSchema", "true").parquet(bronze_path)
    assert "loyalty_tier" in merged_df.columns
    assert merged_df.count() == 83

    # 80 rows from Batch 1 should have null loyalty_tier
    b1_null_count = merged_df.filter((col("batch_id") == "batch_1") & col("loyalty_tier").isNull()).count()
    assert b1_null_count == 80

    # 3 rows from Batch 3 should have populated loyalty_tier
    b3_pop_count = merged_df.filter((col("batch_id") == "batch_3") & col("loyalty_tier").isNotNull()).count()
    assert b3_pop_count == 3


def test_batch_4_second_drift_preserves_loyalty_tier(spark, tmp_path):
    """Ingest Batch 1, Batch 3, then Batch 4; assert both loyalty_tier and marketing_opt_in are reconciled."""
    cust_file = str(BATCH_1_FILES["customers"])
    b3_file = str(BATCH_3_DIR / "customers_batch3_loyalty_tier.csv")
    b4_file = str(BATCH_4_DIR / "customers_batch4_unexpected_column.csv")
    bronze_path = str(tmp_path / "customers")

    # Batch 1
    df_b1 = ingest_entity(spark, "customers", cust_file, "batch_1")
    write_bronze(df_b1, bronze_path)

    # Batch 3
    df_b3 = ingest_entity(spark, "customers", b3_file, "batch_3")
    bronze_b1 = spark.read.option("mergeSchema", "true").parquet(bronze_path)
    reconciled_b3 = reconcile_schema(df_b3, bronze_b1.schema)
    write_bronze(reconciled_b3, bronze_path)

    # Batch 4
    df_b4 = ingest_entity(spark, "customers", b4_file, "batch_4")
    bronze_b3 = spark.read.option("mergeSchema", "true").parquet(bronze_path)
    diff = compare_schemas(bronze_b3.schema, df_b4.schema)
    assert "marketing_opt_in" in diff["added_columns"]

    reconciled_b4 = reconcile_schema(df_b4, bronze_b3.schema)
    write_bronze(reconciled_b4, bronze_path)

    merged = spark.read.option("mergeSchema", "true").parquet(bronze_path)
    assert "loyalty_tier" in merged.columns
    assert "marketing_opt_in" in merged.columns
    assert merged.count() == 86

    # Verify marketing_opt_in nullability for historical batches
    assert merged.filter((col("batch_id") == "batch_1") & col("marketing_opt_in").isNull()).count() == 80
    assert merged.filter((col("batch_id") == "batch_3") & col("marketing_opt_in").isNull()).count() == 3
    assert merged.filter((col("batch_id") == "batch_4") & col("marketing_opt_in").isNotNull()).count() == 3