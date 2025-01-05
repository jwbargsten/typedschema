from pyspark.sql.types import StructField, StringType
from typedschema import generate_schema_def


def test_happy():
    actual = generate_schema_def([StructField("street", StringType(), True)], name="MySchema")
    expected = """\
class MySchema(Schema):
    street = Column(StringType(), True)
my_schema = MySchema()
"""
    assert actual == expected


def test_reserved():
    actual = generate_schema_def([StructField("cols", StringType(), True)], name="MySchema")
    expected = """\
class MySchema(Schema):
    cols_ = Column(StringType(), True, name='cols')
my_schema = MySchema()
"""
    assert actual == expected


def test_space():
    actual = generate_schema_def([StructField("my lovely pet", StringType(), True)], name="MySchema")
    expected = """\
class MySchema(Schema):
    my_lovely_pet = Column(StringType(), True, name='my lovely pet')
my_schema = MySchema()
"""
    assert actual == expected
