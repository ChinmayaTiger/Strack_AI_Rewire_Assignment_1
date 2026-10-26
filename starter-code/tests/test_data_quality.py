"""Tests for src/data_quality.py (Task 7)."""
from pyspark.sql.functions import col
from src.config import BATCH_5_DIR
from src.ingest import ingest_entity
from src.data_quality import validate_data_quality
from src.idempotent_writer import write_bronze


def test_batch_5_null_customer_id_is_quarantined_not_dropped(spark, tmp_path):
    """Assert Batch 5 produces exactly 3 valid rows and 2 quarantined rows with reason."""
    b5_file = str(BATCH_5_DIR / "customers_batch5_null_customer_id.csv")
    df_raw = ingest_entity(spark, "customers", b5_file, "batch_5")

    assert df_raw.count() == 5

    valid_df, quarantined_df = validate_data_quality(df_raw, "customer_id")

    assert valid_df.count() == 3
    assert quarantined_df.count() == 2

    # Quarantine must retain metadata and include quarantine_reason
    assert "quarantine_reason" in quarantined_df.columns
    assert "batch_id" in quarantined_df.columns
    assert "source_file" in quarantined_df.columns

    reasons = [row["quarantine_reason"] for row in quarantined_df.collect()]
    for r in reasons:
        assert "Null or blank business key" in r


def test_batch_5_does_not_fail_the_whole_job(spark, tmp_path):
    """Assert valid rows can be written to Bronze and quarantined rows to quarantine without failure."""
    b5_file = str(BATCH_5_DIR / "customers_batch5_null_customer_id.csv")
    bronze_path = str(tmp_path / "bronze" / "customers")
    quarantine_path = str(tmp_path / "quarantine" / "customers")

    df_raw = ingest_entity(spark, "customers", b5_file, "batch_5")
    valid_df, quarantined_df = validate_data_quality(df_raw, "customer_id")

    # Both writes must complete cleanly without exception
    write_bronze(valid_df, bronze_path)
    (
        quarantined_df.write
        .mode("append")
        .option("mergeSchema", "true")
        .format("parquet")
        .save(quarantine_path)
    )

    assert spark.read.parquet(bronze_path).count() == 3
    assert spark.read.parquet(quarantine_path).count() == 2