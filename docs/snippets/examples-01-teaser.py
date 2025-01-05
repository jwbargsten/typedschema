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