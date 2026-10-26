"""Tests for src/idempotent_writer.py (Task 3)."""
from pathlib import Path
from src.config import BATCH_1_FILES, BATCH_2_DIR
from src.ingest import ingest_entity
from src.idempotent_writer import read_existing_keys, dedup_against_existing, write_bronze


def test_batch_1_rerun_leaves_row_count_unchanged(spark, tmp_path):
    """Ingest Batch 1 customers twice and verify row count remains 80."""
    cust_file = str(BATCH_1_FILES["customers"])
    bronze_path = str(tmp_path / "customers")
    key = "customer_id"

    # First run
    df_run1 = ingest_entity(spark, "customers", cust_file, "batch_1")
    write_bronze(df_run1, bronze_path)
    count_after_run1 = spark.read.parquet(bronze_path).count()
    assert count_after_run1 == 80

    # Second run (exact rerun)
    df_run2 = ingest_entity(spark, "customers", cust_file, "batch_1")
    existing_keys = read_existing_keys(spark, bronze_path, key)
    deduped_df = dedup_against_existing(df_run2, existing_keys, key)
    write_bronze(deduped_df, bronze_path)

    count_after_run2 = spark.read.parquet(bronze_path).count()
    assert count_after_run2 == 80, f"Rerun changed row count: {count_after_run2}"


def test_batch_2_redelivered_rows_are_not_duplicated(spark, tmp_path):
    """Ingest sales_transactions then redelivered batch_2; verify row count stays 360."""
    tx_file = str(BATCH_1_FILES["sales_transactions"])
    batch2_file = str(BATCH_2_DIR / "sales_transactions_batch2_duplicate.csv")
    bronze_path = str(tmp_path / "sales_transactions")
    key = "order_id"

    # Baseline Batch 1
    df_tx = ingest_entity(spark, "sales_transactions", tx_file, "batch_1")
    write_bronze(df_tx, bronze_path)
    assert spark.read.parquet(bronze_path).count() == 360

    # Batch 2 duplicate redelivery
    df_b2 = ingest_entity(spark, "sales_transactions", batch2_file, "batch_2")
    existing_keys = read_existing_keys(spark, bronze_path, key)
    deduped_b2 = dedup_against_existing(df_b2, existing_keys, key)

    assert deduped_b2.count() == 0, "Duplicate rows were not skipped"

    write_bronze(deduped_b2, bronze_path)
    final_count = spark.read.parquet(bronze_path).count()
    assert final_count == 360, f"Row count increased unexpectedly to {final_count}"