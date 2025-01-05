import pyspark.sql.functions as F
import pytest
from pyspark.sql import Row
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from testkit import df_assert_equal

from typedschema import Column, Schema


def test_schema_table_name_cls():
    class TestSchema1(Schema):
        pass

    s = TestSchema1()
    assert s.table_name is None
    with pytest.raises(TypeError):

        class TestSchemaErr1(Schema):
            meta = "abc"

    with pytest.raises(TypeError):

        class TestSchemaErr2(Schema):
            meta = 3

    class TestSchema2(Schema):
        meta = None

    assert TestSchema2().table_name is None


def test_schema_field_clash():
    with pytest.raises(TypeError):

        class TestSchemaErr(Schema):
            cols = Column(StringType(), True)

    class TestSchema(Schema):
        cols_ = Column(StringType(), True, name="cols")

    s = TestSchema()
    assert s["cols_"] == "cols"


def test_field_workaround():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True)
        GRID = Column(StringType(), True)
        BIC = Column(StringType(), True)
        NAME = Column(StringType(), True)
        cols_ = Column(StringType(), True, name="cols")
        meta = {"name": "abc"}

    s = TestSchema()

    assert s.fields == [
        StructField("IBAN", StringType(), True),
        StructField("GRID", StringType(), True),
        StructField("BIC", StringType(), True),
        StructField("NAME", StringType(), True),
        StructField("cols", StringType(), True),
    ]

    assert s.meta["name"] == "abc"
    assert s.table_name == "abc"
    assert s.get_field("cols") == StructField("cols", StringType(), True)
    assert s.cols_.field == StructField("cols", StringType(), True)

    assert s.cols == ["IBAN", "GRID", "BIC", "NAME", "cols"]


def test_schema_ci():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True)
        GRID = Column(StringType(), True)
        BIC = Column(StringType(), True)
        NAME = Column(StringType(), True)

    s = TestSchema()
    assert s.name.name == "NAME"
    assert s.name == "NAME"
    assert s.name.field == StructField("NAME", StringType(), True)
    assert s.nAmE.field == StructField("NAME", StringType(), True)
    assert s["NAME"] == "NAME"
    assert s["nAMe"] == "NAME"
    assert s["NAME"].field == StructField("NAME", StringType(), True)
    assert s["nAMe"].field == StructField("NAME", StringType(), True)
    assert s[3].field == StructField("NAME", StringType(), True)
    assert s[3] == "NAME"
    assert len(s) == 4
    assert [f for f in s] == ["IBAN", "GRID", "BIC", "NAME"]


def test_schema_cs():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True)
        GRID = Column(StringType(), True)
        BiC = Column(StringType(), True)
        NAME = Column(StringType(), True)
        case_sensitive = True

    s = TestSchema()
    with pytest.raises(AttributeError):
        print(s.name)
    with pytest.raises(AttributeError):
        s.nAmE
    assert s.NAME == "NAME"
    assert s.NAME.field == StructField("NAME", StringType(), True)

    with pytest.raises(KeyError):
        s["nAMe"]
    assert s["NAME"] == "NAME"
    assert s["NAME"].field == StructField("NAME", StringType(), True)


def test_strict_null():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True)
        NAME = Column(StringType(), False)

    s = TestSchema()
    cols = [
        StructField("IBAN", StringType(), True),
        StructField("NAME", StringType(), True),
    ]

    assert not s.isequal(cols)
    assert s.isequal(cols, strict_null=False)


def test_set_x_str_col():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True)
        GRID = Column(StringType(), False)
        NAME = Column(StringType(), True)

    s = TestSchema()
    cols = set(s.cols) - {s.iban}
    assert cols == {"GRID", "NAME"}


def test_set_ops():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True, meta={"abc": "def"})
        GRID = Column(StringType(), False)
        NAME = Column(StringType(), True)

    s = TestSchema()

    class TestSchemaA(Schema):
        IBAN = Column(StringType(), True)
        name = Column(StringType(), True)

    sa = TestSchemaA()

    class TestSchemaB(Schema):
        IBAN = Column(StringType(), True)
        BIC = Column(StringType(), True)

    sb = TestSchemaB()

    f = StructField("iban", StringType(), True)

    cols1 = [
        StructField("IBAN", StringType(), True),
        StructField("GRID", StringType(), False),
        StructField("NAME", StringType(), True),
    ]
    cols2 = [
        StructField("IBAN", StringType(), True),
        StructField("NAME", StringType(), False),
    ]
    assert f in s
    assert sa <= s
    assert s >= sa
    assert not sa >= s
    assert not sb <= s
    assert not s <= sa
    assert sa <= cols1
    assert not sa <= cols2
    assert not s <= cols2
    assert s == cols1
    with pytest.raises(ValueError):
        s <= [1, 2, 3]


def test_set_ops_case_sensitive():
    class TestSchema(Schema):
        IBAN = Column(StringType(), True)
        GRID = Column(StringType(), False)
        NAME = Column(StringType(), True)
        case_sensitive = True

    s = TestSchema()

    class TestSchemaSA1(Schema):
        IBAN = Column(StringType(), True)
        name = Column(StringType(), True)
        case_sensitive = True

    sa1 = TestSchemaSA1()

    class TestSchemaSA2(Schema):
        IBAN = Column(StringType(), True)
        NAME = Column(StringType(), True)
        case_sensitive = True

    sa2 = TestSchemaSA2()

    class TestSchemaSB(Schema):
        IBAN = Column(StringType(), True)
        BIC = Column(StringType(), True)
        case_sensitive = True

    sb = TestSchemaSB()
    f = StructField("iban", StringType(), True)

    cols = [
        StructField("IBAN", StringType(), True),
        StructField("GRID", StringType(), False),
        StructField("NAME", StringType(), True),
    ]
    assert f not in s
    assert not sa1 <= s
    assert sa2 <= s
    assert not sb <= s
    assert not s <= sa1
    assert sa2 <= cols
    assert not sa1 <= cols


def test_get_attr_case_insensitive():
    class FinancialDataSchema(Schema):
        capture_datetime = Column(StringType(), True, name="timestamp")

    fds = FinancialDataSchema()

    assert fds.CAPTURE_DATETIME == fds.capture_datetime
    with pytest.raises(AttributeError):
        fds.timestamp


def test_contains_nullable1():
    class FinancialDataSchema(Schema):
        prob = Column(DoubleType(), False)

    fds = FinancialDataSchema()

    c1 = Column(DoubleType(), True, name="prob")
    c2 = Column(DoubleType(), False, name="prob")
    assert c1 not in fds
    assert c2 in fds


def test_contains_nullable2():
    class FinancialDataSchema(Schema):
        prob = Column(StringType(), False)

    fds = FinancialDataSchema()

    c1 = Column(DoubleType(), True, name="prob")
    c2 = Column(DoubleType(), False, name="prob")
    assert c1 not in fds
    assert c2 not in fds


def test_with_spark(spark):
    df = spark.createDataFrame(
        [("Alice", 1), ("Bob", 2), ("Ken", None)],
        StructType(
            [
                StructField("A", StringType(), True),
                StructField("B", IntegerType(), True),
            ]
        ),
    )

    class TestSchema(Schema):
        A = Column(StringType(), True)
        B = Column(IntegerType(), True)

    s = TestSchema()
    assert s == df.schema
    res_df = df.select(F.upper(s.a.col).alias("name"), s.b).where((s.b.col == F.lit(1)) | s.b.col.isNull())
    df_assert_equal(res_df.collect(), [Row(name="ALICE", B=1), Row(name="KEN", B=None)])
