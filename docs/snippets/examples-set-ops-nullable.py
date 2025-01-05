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