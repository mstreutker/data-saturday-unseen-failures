from behave import given, then, when  # type: ignore
from pyspark.sql.types import StructType  # type: ignore
from utils import table_to_spark  # type: ignore

from localpyspark.stockmanagement.stockmanagement import determine_current_stock, process_stock

FILE_PATH_LANDING_ZONE = "/workspaces/local-pyspark/data/"
FILE_PATH_BRONZE_ZONE = "/workspaces/local-pyspark/datalake/bronze"
FILE_PATH_SILVER_ZONE = "/workspaces/local-pyspark/testresults/"


@given("a stock from warehouse {warehouse} with the following state")
def given_a_file(context, warehouse) -> None:
    """Arrange: Prepare data for the test."""

    df = table_to_spark(context.spark, context.table)

    context.tablenaam = "bronze_stock"
    df.createOrReplaceTempView(context.tablenaam)
    return None


@when("the stock is being processed")
def stock_process(context) -> None:
    spark = context.spark

    try:
        df_bronze = context.spark.sql("select * from bronze_stock")
        context.silver_stock = process_stock(
            spark, df_bronze, f"{FILE_PATH_SILVER_ZONE}/{context.scenario}"
        )

        context.exception = None
    except Exception as e:
        context.exception = e


@when("I retrieve the current state")
def haal_stock_op(context) -> None:
    spark = context.spark

    context.gold_stock = determine_current_stock(
        spark, f"{FILE_PATH_SILVER_ZONE}/{context.scenario}/Stock"
    )


@then("I expect a total stock of {current_stock_quantity}")
def then_expect_the_following_result(context, current_stock_quantity) -> None:
    actual_result = context.gold_stock
    expected_result = current_stock_quantity

    assert int(actual_result) == int(expected_result)


@given("nothing is delivered")
def nothing_is_delivered(context):
    df = context.spark.createDataFrame([], StructType([]))

    context.tablenaam = "bronze_stock"
    df.createOrReplaceTempView(context.tablenaam)


@then("I expect an error")
def then_expected_an_error(context):
    assert context.exception is not None
    assert isinstance(
        context.exception, ValueError
    ), f"Unexpected exception type: {type(context.exception)}"
