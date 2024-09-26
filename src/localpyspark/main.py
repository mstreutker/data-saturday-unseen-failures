from pyspark.sql import SparkSession  # type: ignore

from localpyspark.stockmanagement.stockmanagement import process_stock, read_stock

spark = SparkSession.builder.getOrCreate()

FILE_PATH_LANDING_ZONE = "/workspaces/local-pyspark/data/"
FILE_PATH_BRONZE_ZONE = "/workspaces/local-pyspark/datalake/bronze"
FILE_PATH_SILVER_ZONE = "/workspaces/local-pyspark/datalake/silver"

df_bronze = read_stock(spark, FILE_PATH_LANDING_ZONE)
df_silver = process_stock(spark, df_bronze, FILE_PATH_SILVER_ZONE)

df_silver.show()
print(df_silver.count())
