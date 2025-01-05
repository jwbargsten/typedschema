from pathlib import Path
from pyspark.sql import DataFrame

# :snx import
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

from typedschema import Column, Schema, diff_schemas, generate_schema_def


class MySchema(Schema):
    a = Column(LongType(), nullable=False)
    b = Column(DoubleType(), nullable=False)
    c = Column(StringType(), nullable=False)
    d = Column(DateType(), nullable=False)
    e = Column(TimestampType(), nullable=False)


myschema = MySchema()

spark = SparkSession.builder.master("local[*]").appName("typedspark").getOrCreate()
# :xns


class DiffSchema(Schema):
    diff_type = Column(StringType())
    first_df = Column(StringType())
    second_df = Column(StringType())


diff_schema = DiffSchema()


def show_to_file(df: DataFrame, f: str | Path):
    f = Path(f)
    f.write_text(df._show_string(truncate=False))


def schema_to_file(df: DataFrame, f: str | Path):
    f = Path(f)
    f.write_text(df._jdf.schema().treeString())


def diff_to_file(a, b, f):
    f = Path(f)
    df = spark.createDataFrame(diff_schemas(a, b), schema=diff_schema)
    show_to_file(df)


# :snx create-df
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
# :xns
show_to_file(df1, "docs/snippets/create-df.show.txt")
schema_to_file(df1, "docs/snippets/create-df.schema.txt")

# :snx col-is-string
df1.select(F.col(myschema.a)).show()
df1.select(myschema.a).show()
df1.select(myschema.a.col).show()
df1.select(myschema.a.c).show()
# :xns

# :snx col-ops
df1 = (
    spark.range(3)
    .withColumnsRenamed({"id": myschema.a})
    .withColumn(myschema.b, F.upper(F.concat(myschema.a.col, F.lit("_"), myschema.a.col)))
)
df1.show()
# :xns
show_to_file(df1, "docs/snippets/col.show.txt")

# :snx set-ops-no-subset-missing-col
df2 = spark.createDataFrame(
    [
        (1, 2.0, "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
        (2, 3.0, "string2", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
        (3, 4.0, "string3", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0)),
    ],
    schema="a long, z double, c string, d date, e timestamp",
)
myschema <= df2.schema  # False, col b missing
# :xns

# :snx schema-diff
differences = diff_schemas(myschema, df2.schema)

for change, my, other in differences:
    print(f"{change} {my} {other}")
# :xns
with Path("docs/snippets/schema-diff.print.txt").open("w") as fd:
    for change, my, other in differences:
        fd.write(f"{change} {my} {other}\n")


# :snx schema-diff-df
differences_df = spark.createDataFrame(
    [(t, str(a), str(b)) for t, a, b in differences],
    schema="type string, myschema string, df2 string",
)
differences_df.show(truncate=False)
# :xns
show_to_file(differences_df, "docs/snippets/schema-diff-df.show.txt")

# :snx set-ops-nullable
df3 = spark.createDataFrame(
    [
        (1, 2.0, "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0), 10),
        (2, 3.0, "string2", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0), 20),
        (3, 4.0, "string3", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0), 30),
    ],
    schema="a long, b double, c string, d date, e timestamp, f long",
)
myschema <= df3.schema # False, differences in nullable
myschema.issubset(df3.schema, strict_null=False) # True, nullable ignored
# :xns
print("issubset (nonstrict):", myschema.issubset(df3.schema, strict_null=False))
print("issubset:", myschema <= df3.schema)

# :snx codegen
class_def = generate_schema_def(df3, name="CustomerDataSchema")
print(class_def)
# :xns
Path("docs/snippets//examples-class-def.py").write_text(class_def)

