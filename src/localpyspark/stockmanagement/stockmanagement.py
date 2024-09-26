from delta.tables import DeltaTable  # type: ignore
from pyspark.sql import DataFrame, SparkSession  # type: ignore
from pyspark.sql.functions import (
    input_file_name,  # type: ignore
    regexp_extract,  # type: ignore
)
from pyspark.sql.functions import max as spark_max
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql.types import IntegerType, StringType, StructField, StructType  # type: ignore

ENTITY_NAME = "Stock"
ENTITY_SCHEMA = StructType(
    [
        StructField("SKU_ID", StringType(), True),
        StructField("Current_Stock_Quantity", IntegerType(), True),
        StructField("Units", StringType(), True),
        StructField("Average_Lead_Time_in_days", IntegerType(), True),
        StructField("Maximum_Lead_Time_in_days", IntegerType(), True),
        StructField("Unit_Price", StringType(), True),
        StructField("Date", StringType(), True),  # Will parse the date later
    ]
)


def read_stock(spark: SparkSession, file_path: str) -> DataFrame:
    df = (spark.read.option("header", True).option("sep", ";").option("locale", "en_US")).csv(
        file_path, schema=ENTITY_SCHEMA
    )

    df = df.withColumn(
        "warehouse", regexp_extract(input_file_name(), r"warehouse_inventory_([^.]+)\.csv$", 1)
    )

    return df


def process_stock(spark: SparkSession, source_df: DataFrame, file_path_delta: str) -> DataFrame:
    delta_table_path = f"{file_path_delta}/{ENTITY_NAME}"

    if source_df.isEmpty():
        raise ValueError("The DataFrame is empty. No data found in the Delta table.")

    if not DeltaTable.isDeltaTable(spark, delta_table_path):
        source_df.write.format("delta").partitionBy("Warehouse").save(delta_table_path)
    else:
        merge_condition = "target.Warehouse = source.Warehouse AND target.Date = source.Date"

        delta_table = DeltaTable.forPath(spark, delta_table_path)
        delta_table.alias("target").merge(
            source=source_df.alias("source"), condition=merge_condition
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

    # Return the Delta table as a DataFrame
    return spark.read.format("delta").load(delta_table_path)


def determine_current_stock(spark: SparkSession, delta_table_path: str) -> int:
    df = spark.read.format("delta").load(delta_table_path)

    # Find the maximum Current_Stock_Quantity per Warehouse and sum the results
    actual_result = (
        df.groupBy("Warehouse")
        .agg(spark_max("Current_Stock_Quantity").alias("Max_Stock"))
        .agg(spark_sum("Max_Stock").alias("Total_Stock"))
        .collect()
    )

    # Extract the total stock value
    total_stock = actual_result[0]["Total_Stock"]

    # Return the result as an integer
    return int(total_stock)
