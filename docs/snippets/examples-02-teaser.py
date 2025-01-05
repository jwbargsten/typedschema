df.select(myschema.name)  # used as string
df.select(myschema.name.col)  # used as pyspark column
df.withColumn(f"{myschema.name}_uc", F.upper(myschema.name.col))
df.withColumnRenamed(myschema.name, f"{myschema.name}_old")
df.show()

df.createOrReplaceTempView("friends")
# for pyspark sql use "`" (backticks) to deal with space in column names
sqldf = spark.sql(f"SELECT `{myschema.favourite_animal}` FROM friends")