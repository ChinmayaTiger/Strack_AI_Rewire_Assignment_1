"""Shared pytest fixtures. This file is complete boilerplate - no need to
change it (see Helper Guide's testing tips: keep shuffle partitions low for
fast local unit tests)."""
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .appName("bronze-ingestion-tests")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    yield spark
    spark.stop()
