"""Shared pytest fixtures configured for Windows compatibility and isolated local execution."""
import os
import pytest
from pyspark.sql import SparkSession

# Ensure Windows Hadoop compatibility for PySpark in pytest
if "HADOOP_HOME" not in os.environ:
    os.environ["HADOOP_HOME"] = "C:\\hadoop"
if "C:\\hadoop\\bin" not in os.environ.get("PATH", ""):
    os.environ["PATH"] = "C:\\hadoop\\bin;" + os.environ.get("PATH", "")


@pytest.fixture(scope="session")
def spark():
    """Shared SparkSession fixture."""
    spark = (
        SparkSession.builder
        .appName("bronze-ingestion-tests")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    yield spark
    spark.stop()