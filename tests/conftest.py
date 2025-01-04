import pytest
from pyspark import SparkConf
from pyspark.sql import SparkSession
import os
from pathlib import Path


env_file = Path(".env")
if env_file.exists():
    with env_file.open("r") as fd:
        for entry in fd:
            k, v = entry.rstrip().split("=", 1)
            os.environ[k] = v


@pytest.fixture(scope="module")
def spark():
    """Initialize spark session."""

    conf = SparkConf()
    conf.set("spark.executorEnv.PYTHONPATH", "./tests")
    conf.set("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
    conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
    JAVA_HOME = os.environ.get("JAVA_HOME")
    if JAVA_HOME:
        conf.set("spark.executorEnv.JAVA_HOME", JAVA_HOME)
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("local-testing-pyspark-context")
        .config(conf=conf)
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sql("SET spark.sql.shuffle.partitions=1")
    spark.sql("SET spark.default.parallelism=1")
    spark.sql("SET spark.sql.legacy.timeParserPolicy=CORRECTED")

    yield spark
    spark.sql("RESET")
    spark.catalog.clearCache()
