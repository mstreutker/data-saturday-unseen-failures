from behave import given, then, when  # type: ignore
from pyspark.sql.types import StructType  # type: ignore
from utils import table_to_spark  # type: ignore

from localpyspark.voorraadbeheer.voorraadbeheer import bepaal_huidige_voorraad, verwerk_voorraad

FILE_PATH_LANDING_ZONE = "/workspaces/local-pyspark/data/"
FILE_PATH_BRONS_ZONE = "/workspaces/local-pyspark/datalake/brons"
FILE_PATH_ZILVER_ZONE = "/workspaces/local-pyspark/testresults/"


@given("a stock from warehouse {warehouse} with the following state")
def given_a_file(context, warehouse) -> None:
    """Arrange: Prepare data for the test."""

    df = table_to_spark(context.spark, context.table)

    context.tablenaam = "brons_voorraad"
    df.createOrReplaceTempView(context.tablenaam)
    return None


# @when("de voorraad wordt ingelezen")
# def voorraad_inlezen(context) -> None:
#     inlezen_voorraad()
#     return None


@when("the stock is being processed")
def voorraad_verwerken(context) -> None:
    spark = context.spark

    try:
        df_brons = context.spark.sql("select * from brons_voorraad")
        context.zilver_voorraad = verwerk_voorraad(
            spark, df_brons, f"{FILE_PATH_ZILVER_ZONE}/{context.scenario}"
        )

        context.exception = None
    except Exception as e:
        context.exception = e


@when("I retrieve the current state")
def haal_voorraad_op(context) -> None:
    spark = context.spark

    context.goud_voorraad = bepaal_huidige_voorraad(
        spark, f"{FILE_PATH_ZILVER_ZONE}/{context.scenario}/Voorraad"
    )


@then("I expect a stock of {current_stock_quantity} in warehouse amsterdam")
def then_expect_the_following_result(context, current_stock_quantity) -> None:
    actueel_resultaat = context.goud_voorraad
    verwacht_resultaat = current_stock_quantity

    assert int(actueel_resultaat) == int(verwacht_resultaat)


@given("nothing is delivered")
def er_is_niks_aangeleverd(context):
    df = context.spark.createDataFrame([], StructType([]))

    context.tablenaam = "brons_voorraad"
    df.createOrReplaceTempView(context.tablenaam)


@then("I expect an error")
def then_verwacht_een_fout(context):
    assert context.exception is not None
    assert isinstance(
        context.exception, ValueError
    ), f"Unexpected exception type: {type(context.exception)}"
