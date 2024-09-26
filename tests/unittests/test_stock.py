import pytest
from delta import *
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

from localpyspark.stockmanagement.stockmanagement import (
    determine_current_stock,
    process_stock,
    read_stock,
)


@pytest.fixture(scope="session")
def spark():
    builder = (
        SparkSession.builder.appName("DeltaTableTest")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.catalogImplementation", "in-memory")
    )

    yield configure_spark_with_delta_pip(builder).getOrCreate()


def test_read_stock(spark):
    # Arrange
    file_path = "/workspaces/data-saturday-unseen-failures/data/warehouse_inventory_pytest.csv"
    # Arrange: Define the expected data
    expected_data = [
        ("1009AA", 50000, "L", 30, 48, "28,76326", "2024-09-07"),
        ("1077CA", 46516, "L", 45, 70, "22,9777", "2024-09-06"),
        ("1083AA", 48210, "L", 45, 68, "29,02", "2024-09-05"),
    ]
    expected_columns = [
        "SKU_ID",
        "Current_Stock_Quantity",
        "Units",
        "Average_Lead_Time_days",
        "Maximum_Lead_Time_days",
        "Unit_Price",
        "Date",
    ]
    expected_df = spark.createDataFrame(expected_data, expected_columns)

    # Act
    actual_df = read_stock(spark, file_path)

    # Assert
    assert expected_df.count() == actual_df.count()


def test_process_stock(spark):
    # Arrange
    df = spark.createDataFrame([], StructType([]))
    file_path_delta = ""

    # Act & Assert
    with pytest.raises(ValueError):
        process_stock(spark, df, file_path_delta)


def test_determine_current_stock(spark):
    # Arrange
    delta_table_path = "/workspaces/data-saturday-unseen-failures/testresults/pytest"

    expected_data = [
        ("1009AA", 50000, "L", 30, 48, "28,76326", "2024-09-07", "pytest"),
        ("1077CA", 46516, "L", 45, 70, "22,9777", "2024-09-06", "pytest"),
        ("1083AA", 48210, "L", 45, 68, "29,02", "2024-09-05", "pytest"),
    ]
    expected_columns = [
        "SKU_ID",
        "Current_Stock_Quantity",
        "Units",
        "Average_Lead_Time_days",
        "Maximum_Lead_Time_days",
        "Unit_Price",
        "Date",
        "Warehouse",
    ]
    expected_df = spark.createDataFrame(expected_data, expected_columns)
    expected_df.write.mode("overwrite").format("delta").partitionBy("Warehouse").save(
        delta_table_path
    )
    expected = 50000

    # Act
    actual = determine_current_stock(spark, delta_table_path)

    # Assert
    assert actual == expected
