from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import (
    StringType,
)

from typedschema import Column, Schema


spark = SparkSession.builder.master("local[*]").appName("typedspark").getOrCreate()


# :snx 01-teaser
class MySchema(Schema):
    name = Column(StringType(), nullable=False)
    # you can decouple the attribute name from the column name
    favourite_animal = Column(StringType(), nullable=False, name="favourite animal")


myschema = MySchema()

df = spark.createDataFrame(
    [
        ("Carl", "Cat"),
        ("Homer", "Pig"),
    ],
    schema=myschema.spark_schema,
)
# :xns
df.show()
df.printSchema()

# :snx 02-teaser
df.select(myschema.name)  # used as string
df.select(myschema.name.col)  # used as pyspark column
df.withColumn(f"{myschema.name}_uc", F.upper(myschema.name.col))
df.withColumnRenamed(myschema.name, f"{myschema.name}_old")
df.show()

df.createOrReplaceTempView("friends")
# for pyspark sql use "`" (backticks) to deal with space in column names
sqldf = spark.sql(f"SELECT `{myschema.favourite_animal}` FROM friends")
# :xns
sqldf.show()
