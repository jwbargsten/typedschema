from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from datetime import datetime, date
from pyspark.sql.types import (
    DoubleType,
    StringType,
    LongType,
    DateType,
    TimestampType,
)

from typedschema import Column, Schema, diff_schemas


class MySchema(Schema):
    a = Column(LongType(), nullable=False)
    b = Column(DoubleType(), nullable=False)
    c = Column(StringType(), nullable=False)
    d = Column(DateType(), nullable=False)
    e = Column(TimestampType(), nullable=False)


myschema = MySchema()

spark = SparkSession.builder.master("local[*]").appName("typedspark").getOrCreate()