"""spark_session.py - Reusable SparkSession factory with Windows Hadoop compatibility."""
import os
from pyspark.sql import SparkSession

# Ensure HADOOP_HOME is set before JVM launch
if "HADOOP_HOME" not in os.environ:
    os.environ["HADOOP_HOME"] = "C:\\hadoop"
if "C:\\hadoop\\bin" not in os.environ.get("PATH", ""):
    os.environ["PATH"] = "C:\\hadoop\\bin;" + os.environ.get("PATH", "")


def get_spark_session(app_name: str = "TigerRetailBronzeIngestion") -> SparkSession:
    """Creates or retrieves a local SparkSession configured for local execution."""
    builder = (
        SparkSession.builder.master("local[*]")
        .appName(app_name)
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.driver.memory", "2g")
        .config("spark.ui.enabled", "false")
        .config("spark.ui.showConsoleProgress", "false")
    )
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


# Alias to match pipeline.py import
get_spark = get_spark_session