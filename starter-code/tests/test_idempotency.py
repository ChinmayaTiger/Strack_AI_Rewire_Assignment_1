"""Tests for src/idempotent_writer.py (Task 3). Stubs only."""
import pytest


@pytest.mark.skip(reason="TODO: implement once idempotent_writer is written")
def test_batch_1_rerun_leaves_row_count_unchanged(spark, tmp_path):
    # TODO: run Batch 1 ingestion twice against a tmp bronze path and assert
    # the row count is identical after both runs.
    pass


@pytest.mark.skip(reason="TODO: implement once idempotent_writer is written")
def test_batch_2_redelivered_rows_are_not_duplicated(spark, tmp_path):
    # TODO: ingest data/sales_transactions.csv, then
    # data/sample_batches/batch_2_duplicate_redelivery/..., and assert the
    # bronze sales_transactions row count did not increase.
    pass
