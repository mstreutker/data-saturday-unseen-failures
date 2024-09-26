"""Support functions for working with Spark and Delta"""

import time

from pyspark.sql import types as t


def string_to_type(s):
    tname = s.lower()
    if tname == "int":
        return t.IntegerType()
    elif tname == "long":
        return t.LongType()
    elif tname == "double":
        return t.DoubleType()
    elif tname == "date":
        return t.DateType()
    elif tname == "timestamp":
        return t.TimestampType()
    elif tname == "boolean":
        return t.BooleanType()
    else:
        return t.StringType()


def parse_ts(s):
    return int(time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S")))


def process_cells(cols, cells):
    data = list(zip(cols, cells))
    for (_, ftype), cell in data:
        # if "%RAND" in cell:
        #     yield random_cell(ftype, cell)
        if "null" in cell:
            yield cell
        elif ftype == "timestamp":
            yield parse_ts(cell)
        else:
            yield cell


def table_to_spark(spark, table):
    cols = [h.split(":") for h in table.headings]

    if len([c for c in cols if len(c) != 2]) > 0:
        raise ValueError(
            "You must specify name AND data type for columns like this 'my_field:string'"
        )

    schema = t.StructType(
        [t.StructField(name + "_str", t.StringType(), False) for (name, _) in cols]
    )
    rows = [list(process_cells(cols, row.cells)) for row in table]
    df = spark.createDataFrame(rows, schema=schema)

    for name, field_type in cols:
        df = df.withColumn(name, df[name + "_str"].cast(string_to_type(field_type))).drop(
            name + "_str"
        )

    return df
