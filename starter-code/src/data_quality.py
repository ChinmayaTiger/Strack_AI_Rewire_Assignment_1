"""Data quality validation - Task 7 (Required AI-Native Activity).

Guided by .claude/skills/data_quality_validation/SKILL.md.
"""
from typing import Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim, lit, when


def validate_data_quality(df: DataFrame, business_key: str) -> Tuple[DataFrame, DataFrame]:
    """Split an incoming DataFrame into (valid_df, quarantined_df) according
    to the rule: business_key must not be null, empty, or whitespace-only.
    
    Quarantined rows retain all original columns, existing ingestion metadata,
    and gain a descriptive `quarantine_reason` column.
    """
    if business_key not in df.columns:
        # If business key is missing entirely, quarantine all rows
        quarantined_df = df.withColumn(
            "quarantine_reason", lit(f"Missing business key column: '{business_key}'")
        )
        empty_valid_df = df.filter(lit(False))
        return empty_valid_df, quarantined_df

    # Condition for null, empty string, or whitespace string
    is_null_or_blank = (
        col(business_key).isNull() | (trim(col(business_key).cast("string")) == "")
    )

    valid_df = df.filter(~is_null_or_blank)

    quarantined_df = (
        df.filter(is_null_or_blank)
        .withColumn(
            "quarantine_reason",
            lit(f"Null or blank business key: '{business_key}'")
        )
    )

    return valid_df, quarantined_df