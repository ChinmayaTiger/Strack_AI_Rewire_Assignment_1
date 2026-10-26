"""Idempotent bronze write logic.

Scaffolding only - read .claude/skills/idempotency/SKILL.md before filling this in
(Task 3).
"""
from pyspark.sql import DataFrame, SparkSession


def read_existing_keys(spark: SparkSession, bronze_path: str, business_key: str):
    """Return the set/DataFrame of business-key values already present in
    bronze for this entity (empty/none if the bronze table does not exist
    yet - handle the very first write).

    TODO: implement.
    """
    raise NotImplementedError("read_existing_keys: see .claude/skills/idempotency/SKILL.md")


def dedup_against_existing(incoming_df: DataFrame, existing_keys, business_key: str) -> DataFrame:
    """Given the incoming batch and the keys already in bronze, return only
    the rows that should actually be written (i.e. drop redelivered rows
    whose key already exists) - see Task 3's explicit redelivery scenario.

    TODO: implement.
    """
    raise NotImplementedError("dedup_against_existing: see .claude/skills/idempotency/SKILL.md")


def write_bronze(df: DataFrame, bronze_path: str) -> None:
    """Write the deduplicated batch to the bronze output for this entity.

    TODO: implement. Consider what happens if the write target is also the
    read source for this run (combine-then-rewrite) - do not read and
    overwrite the same path in one lazy Spark plan.
    """
    raise NotImplementedError("write_bronze: see .claude/skills/idempotency/SKILL.md")
