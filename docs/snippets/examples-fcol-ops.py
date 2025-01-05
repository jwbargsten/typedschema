df1 = (
    spark.range(3)
    .withColumnsRenamed({"id": myschema.a})
    .withColumn(myschema.b, F.upper(F.concat(myschema.a.fcol, F.lit("_"), myschema.a.fcol)))
)
df1.show()