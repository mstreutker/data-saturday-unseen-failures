from pyspark.sql import SparkSession  # type: ignore

from localpyspark.voorraadbeheer.voorraadbeheer import lees_voorraad, verwerk_voorraad

spark = SparkSession.builder.getOrCreate()

FILE_PATH_LANDING_ZONE = "/workspaces/local-pyspark/data/"
FILE_PATH_BRONS_ZONE = "/workspaces/local-pyspark/datalake/brons"
FILE_PATH_ZILVER_ZONE = "/workspaces/local-pyspark/datalake/zilver"

df_brons = lees_voorraad(spark, FILE_PATH_LANDING_ZONE)
df_zilver = verwerk_voorraad(spark, df_brons, FILE_PATH_ZILVER_ZONE)

df_zilver.show()
print(df_zilver.count())
