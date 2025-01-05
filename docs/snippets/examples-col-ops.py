df1 = (
    spark.range(3)
    .withColumnsRenamed({"id": myschema.a})
    .withColumn(myschema.b, F.upper(F.concat(myschema.a.col, F.lit("_"), myschema.a.col)))
)
df1.show()