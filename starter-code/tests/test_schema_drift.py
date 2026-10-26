"""Tests for src/schema_utils.py (Task 4, and Task 6 once you modify the
skill). Stubs only."""
import pytest


@pytest.mark.skip(reason="TODO: implement once schema_utils is written")
def test_batch_3_loyalty_tier_detected_and_backfilled(spark, tmp_path):
    # TODO: ingest Batch 1 customers, then
    # data/sample_batches/batch_3_schema_drift/customers_batch3_loyalty_tier.csv,
    # assert loyalty_tier exists, is null for pre-Batch-3 rows, and populated
    # for Batch 3 rows.
    pass


@pytest.mark.skip(reason="TODO: implement after modifying .claude/skills/schema_drift/SKILL.md (Task 6)")
def test_batch_4_second_drift_preserves_loyalty_tier(spark, tmp_path):
    # TODO: after Batch 3, ingest
    # data/sample_batches/batch_4_schema_drift_skill_update/customers_batch4_unexpected_column.csv
    # and assert BOTH loyalty_tier (unaffected) and marketing_opt_in (new,
    # backfilled null for earlier rows) are correct in bronze customers.
    pass
