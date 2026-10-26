"""Tests for src/data_quality.py (Task 7 - your new skill). Stubs only.

Do not fill these in until you have written .claude/skills/data_quality_validation/
SKILL.md yourself - the assertions below should reflect the rule YOU define
in that skill, not a rule copied from here.
"""
import pytest


@pytest.mark.skip(reason="TODO: implement after creating .claude/skills/data_quality_validation/SKILL.md (Task 7)")
def test_batch_5_null_customer_id_is_quarantined_not_dropped(spark, tmp_path):
    # TODO: ingest
    # data/sample_batches/batch_5_data_quality/customers_batch5_null_customer_id.csv
    # and assert: bronze customers row count increases by exactly 3, and a
    # quarantine output/log contains exactly 2 rows with a reason recorded.
    pass


@pytest.mark.skip(reason="TODO: implement after creating .claude/skills/data_quality_validation/SKILL.md (Task 7)")
def test_batch_5_does_not_fail_the_whole_job(spark, tmp_path):
    # TODO: assert the pipeline run completes successfully even though 2 of
    # 5 rows are invalid.
    pass
