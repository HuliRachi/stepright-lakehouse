
import os
import sys
 
import pytest
from pyspark.sql import SparkSession

_TRANSFORMATIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "transformations")
sys.path.insert(0, os.path.abspath(_TRANSFORMATIONS_DIR))

@pytest.fixture(scope="session")
def local_spark():
   
    active = SparkSession.getActiveSession()
    if active is not None:
        yield active
        # Don't stop() a session we didn't create — Databricks owns its
        # own ambient session's lifecycle, not this fixture.
        return
    
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("stepright-unit-tests")
        .config("spark.sql.shuffle.partitions", "2")  # small fixtures, no need for 200 default partitions
        .getOrCreate()
    )
    yield spark
    spark.stop()
