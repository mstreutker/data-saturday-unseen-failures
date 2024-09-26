from behave import fixture, use_fixture  # pylint: disable=no-name-in-module
from delta import *
from pyspark.sql import SparkSession


@fixture
def sparksession(context):
    builder = (
        SparkSession.builder.appName("DeltaTableTest")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.catalogImplementation", "in-memory")
    )
    context.spark = configure_spark_with_delta_pip(builder).getOrCreate()
    yield context.spark

    # -- CLEANUP-FIXTURE PART:
    context.spark.stop()


def before_feature(context, feature):
    use_fixture(sparksession, context)


# def after_scenario(context, scenario):
#     spark = context.spark
#     spark.sql("DROP VIEW IF EXISTS brons_voorraad")
# spark.catalog.dropTempView("brons_voorraad")
