"""Reusable SparkSession factory.

Scaffolding only - fill in the config you need. Keep it a single shared
factory so every module/test gets a SparkSession the same way (see
Helper Guide Section 1 / 2).
"""
from pyspark.sql import SparkSession


def get_spark(app_name: str = "bronze-ingestion") -> SparkSession:
    """Return a local SparkSession suitable for this assignment.

    TODO:
      - Set a sensible spark.sql.shuffle.partitions for local runs (the
        default of 200 is wasteful on a laptop-sized dataset).
      - Add any other config your implementation needs (e.g. timezone).
    """
    builder = SparkSession.builder.appName(app_name)
    # TODO: builder = builder.config(...)
    return builder.getOrCreate()
