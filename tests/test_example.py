import pytest
from datetime import datetime, date
from pyspark.sql.types import (
    DoubleType,
    StringType,
    LongType,
    DateType,
    TimestampType,
)

from typedschema import Column, Schema, diff_schemas
import pyspark.sql.functions as F


@pytest.mark.skip(reason="only for example purposes")
def test_example(spark):
    class MySchema(Schema):
        a = Column(LongType(), nullable=False)
        b = Column(DoubleType(), nullable=False)
        c = Column(StringType(), nullable=False)
        d = Column(DateType(), nullable=False)
        e = Column(TimestampType(), nullable=False)

    myschema = MySchema()

    df1 = spark.createDataFrame(
        [
            (1, 2.0, "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
            (2, 3.0, "string2", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
            (3, 4.0, "string3", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0)),
        ],
        schema=myschema.spark_schema,
    )
    df1.show()
    df1.printSchema()
    df2 = spark.createDataFrame(
        [
            (1, 2.0, "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
            (2, 3.0, "string2", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
            (3, 4.0, "string3", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0)),
        ],
        schema="a long, z double, c string, d date, e timestamp",
    )
    # I can test using Python's set operations
    # https://docs.python.org/3/library/stdtypes.html#set
    # just make sure that the typed schema is on the left side
    for change, my, other in diff_schemas(myschema, df2.schema):
        print(f"{change} {my} {other}")
    assert myschema >= df2.schema
    assert myschema.issuperset(df2.schema)
    df1.select(myschema.a).show()
    df1.select(F.upper(myschema.a.fcol)).show()
    # instead of
    df1.select(F.upper(F.col("a"))).show()
