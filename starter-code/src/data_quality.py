"""Data quality validation - Task 7 (Required AI-Native Activity).

This module is intentionally just a placeholder. There is no
.claude/skills/data_quality_validation/SKILL.md provided - you must design and
create it yourself (see the Helper Guide, Section 5B) before filling in the
functions below. Do not implement this module before you have written the
skill; the skill's decision rules are what this module should implement.
"""
from pyspark.sql import DataFrame


def validate_data_quality(df: DataFrame, business_key: str) -> tuple[DataFrame, DataFrame]:
    """Split an incoming DataFrame into (valid_df, quarantined_df) according
    to the rule(s) you define in your own .claude/skills/data_quality_validation/SKILL.md
    (starting with: business_key must not be null/blank).

    TODO: implement once your SKILL.md exists. Quarantined rows should still
    carry a reason and full ingestion metadata (run this AFTER metadata.py,
    per the Helper Guide's Section 5B ordering).
    """
    raise NotImplementedError(
        "validate_data_quality: write .claude/skills/data_quality_validation/SKILL.md first"
    )
