differences_df = spark.createDataFrame(
    [(t, str(a), str(b)) for t, a, b in differences],
    schema="type string, myschema string, df2 string",
)
differences_df.show(truncate=False)