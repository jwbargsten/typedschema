from functools import cached_property
from .column import Column
from typing import (
    Any,
    Hashable,
    Iterator,
    Sequence,
)
from typing_extensions import Self

from pyspark.sql import DataFrame
from pyspark.sql.types import StructField, StructType
from .structfield import sf_apply, sf_without_metadata, sf_with_lc_colname


def _unpack_field(f):
    if isinstance(f, Column):
        return f.field
    if isinstance(f, StructField):
        return f
    raise ValueError(f"I can only process Column and StructField, got {f}")


def _unpack_schema(s):
    if isinstance(s, Schema):
        return s.fields
    if isinstance(s, StructType):
        return s.fields
    if isinstance(s, DataFrame):
        return s.schema.fields
    fields = list(iter(s))

    if not all(isinstance(field, StructField) for field in fields):
        raise ValueError("supplied schema type is not supported")
    return fields


RESERVED_FIELDS = [
    "cols",
    "spark_schema",
    "fields",
    "table_name",
    "dtypes",
    "isequal",
    "issubset",
    "contains",
    "issuperset",
    "meta",
    "case_sensitive",
]


class MetaSchema(type):
    def __new__(cls, name: str, bases: Any, dct: dict[str, Any]):
        cols = {
            k: v._with_name_if_unnamed(k)
            for k, v in dct.items()
            if not k.startswith("_") and isinstance(v, Column)
        }
        for c in RESERVED_FIELDS:
            if c in cols:
                raise TypeError(
                    f"column '{c}' is a reserved field, use ``{c}_ = Column(..., name=\"{c}\")`` as workaround"
                )
        dct = {
            "case_sensitive": False,
            "meta": None,
            **dct,
            **cols,
            "cols": list(cols.values()),
            "_attr_col_map": cols,
        }
        if dct["meta"] is not None and not isinstance(dct["meta"], dict):
            meta = dct["meta"]
            raise TypeError(f"meta should be None or a dict, was {type(meta)}")

        return type.__new__(cls, name, bases, dct)


class Schema(metaclass=MetaSchema):
    """A typed schema is a schema definition that has the
    field/column names as named attributes of the class definition.

    :param case_sensitive: are the columns/fields case sensitive?
    :param meta: key-value entries that are related to the schema. An example would be the table name.
        Actually, because the table name is needed quite frequently, the ``self.table_name``
        property is a shortcut for ``meta["name"]``.

    Examples:

    >>> from pyspark.sql.types import StructField, StringType, StringType
    >>> from typedschema import Schema, Column
    >>>
    >>> class ExampleSchema(Schema):
    ...     # syntax is Column(DATA_TYPE, IS_NULLABLE)
    ...     name = Column(StringType(), True)
    ...     city = Column(StringType(), True)
    ...     street = Column(StringType(), True)
    ...     # a name clash: the column is named "cols" but "cols" is also a reserved field
    ...     # (see `typedschema.RESERVED_FIELDS` for list)
    ...     # you can use a "_" as a workaround for the field and supply the name as arg to Column
    ...     cols_ = Column(StringType(), True, name="cols")
    ...     # meta is a dict. You can dump whatever you think is useful
    ...     # (you can also skip it, of course)
    ...     meta = {"default_values": {"name": "NA"}, "name": "customers"}
    ...     # the schema fields are considered case-insensitive
    ...     # in all functions, such as equality tests
    ...     # (case_sensitive is False by default)
    ...     case_sensitive = False
    >>>
    >>> # we have to create a object to use the full functionality
    >>> # (for e.g. testing schema equality with `==`)
    >>> exs = ExampleSchema()
    >>> exs.table_name
    'customers'
    >>> exs.cols
    ['name', 'city', 'street', 'cols']
    >>> [c.field for c in exs.cols]
    [
    StructField('name', StringType(), True),
    StructField('city', StringType(), True),
    StructField('street', StringType(), True),
    StructField('cols', StringType(), True)
    ]
    >>> exs.city.field
    StructField('city', StringType(), True)
    >>> exs.city
    'city'
    """

    meta: dict[Hashable, Any]
    case_sensitive: bool

    def __init__(self, *, case_sensitive: bool | None = None, meta: None | dict[Hashable, Any] = None):
        self._colmap = {
            **{attr.lower(): col for attr, col in self._attr_col_map.items()},
            **{attr: col for attr, col in self._attr_col_map.items()},
        }
        self._fieldmap = {**{f.lower(): f for f in self.cols}, **{f: f for f in self.cols}}

        if case_sensitive is not None:
            self.case_sensitive = case_sensitive

        if meta is not None:
            self.meta = meta

        if self.meta is not None and not isinstance(self.meta, dict):
            raise TypeError(f"meta should be None or a dict (got {self.meta}")

    @cached_property
    def spark_schema(self) -> StructType:
        """The spark schema

        Representation of a spark schema that can be used to construct DataFrames.
        """
        return StructType([c.field for c in self.cols])

    @property
    def fields(self) -> list[StructField]:
        """the list of columns/fields."""
        return self.spark_schema.fields

    @property
    def table_name(self):
        """returns ``meta["name"]``."""
        if not (self.meta and isinstance(self.meta, dict)):
            return None
        return self.meta.get("name")

    @property
    def dtypes(self) -> list[tuple[str, str]]:
        """Data types of the columns

        :return:
            a list of (column name, data type) tuples
        """
        return [(str(c), c.dtype.simpleString()) for c in self.cols]

    def get_field(self, name) -> StructField:
        if self.case_sensitive or isinstance(name, int):
            return self.spark_schema[name]
        else:
            return self.spark_schema[self._fieldmap[name.lower()]]

    def __iter__(self) -> Iterator[Column]:
        return iter(self.cols)

    def __getattr__(self, name) -> Column:
        if name == "case_sensitive":
            raise AttributeError("case_sensitive not defined")

        if self.case_sensitive:
            # __getattr__ is only called if the class attribute was not found earlier.
            # Which means that this class attribute does not exist. If we are case-sensitive,
            # then the col is indeed not part of the class.
            raise AttributeError(f"Column {name} does not exist")

        name_lc = name.lower()
        if name_lc not in self._colmap:
            raise AttributeError(f"Column {name} (or {name_lc}) does not exist")
        return self._colmap[name.lower()]

    def __len__(self) -> int:
        return len(self.cols)

    def __getitem__(self, key: str | int) -> Column:
        if isinstance(key, int):
            return self.cols[key]
        try:
            return getattr(self, key)
        except AttributeError as ex:
            raise KeyError(key) from ex

    def isequal(self, other: Sequence[StructField] | Self | StructType | DataFrame, strict_null=True):
        other_cols = _unpack_schema(other)
        return sf_apply(
            self.fields,
            other_cols,
            lambda xs, ys: xs == ys,
            case_sensitive=self.case_sensitive,
            strict_null=strict_null,
        )

    def __eq__(self, other: Sequence[StructField] | Self | StructType):
        return self.isequal(other)

    def issubset(self, other: Sequence[StructField] | Self | StructType | DataFrame, strict_null=True):
        other_cols = _unpack_schema(other)
        return sf_apply(
            self.fields,
            other_cols,
            lambda xs, ys: xs <= ys,
            case_sensitive=self.case_sensitive,
            strict_null=strict_null,
        )

    def __le__(self, other: Sequence[StructField] | Self | StructType):
        return self.issubset(other)

    def issuperset(self, other: Sequence[StructField] | Self | StructType | DataFrame, strict_null=True):
        other_cols = _unpack_schema(other)
        return sf_apply(
            self.fields,
            other_cols,
            lambda xs, ys: xs >= ys,
            case_sensitive=self.case_sensitive,
            strict_null=strict_null,
        )

    def __ge__(self, other: Sequence[StructField] | Self | StructType):
        return self.issuperset(other)

    def contains(self, other: StructField | str):
        if isinstance(other, StructField):
            field = other
        elif isinstance(other, Column):
            field = other.field
        else:
            try:
                field = self.get_field(other)
            except KeyError:
                return False

        field = sf_without_metadata(field)
        ref_fields = [sf_without_metadata(f) for f in self.fields]

        if not self.case_sensitive:
            field = sf_with_lc_colname(field)
            return any(sf_with_lc_colname(c) == field for c in ref_fields)

        return any(c == field for c in ref_fields)

    def __contains__(self, other: StructField | str):
        return self.contains(other)


def diff_schemas(
    a: Sequence[StructField] | StructType | Schema | DataFrame,
    b: Sequence[StructField] | StructType | Schema | DataFrame,
):
    """
    Diff two schemas

    :param a: the first schema
    :param b: the second schema
    :return: a list of tuples
        each tuple has the structure: (diffType, colname of a, colname of b)
        diffType can be

        ``+``
            a is missing this col, b has it extra

        ``-``
            a has this column extra, it is missing in b

        ``(space)``
            no difference

        ``>``
            the col is present in a and b, but the data type differs

        ``!``
            the col is present in a and b, but the nullable constraint differs
    """
    a_fields, b_fields = sf_apply(_unpack_schema(a), _unpack_schema(b), lambda xs, ys: (xs, ys))

    a_cols = {f.name: f for f in a_fields}
    b_cols = {f.name: f for f in b_fields}
    a_cols_ks = set(a_cols.keys())
    b_cols_ks = set(b_cols.keys())

    a_cols_uniq = a_cols_ks - b_cols_ks
    b_cols_uniq = b_cols_ks - a_cols_ks
    common = a_cols_ks & b_cols_ks

    common_diff = []
    for c in sorted(common):
        a_col = a_cols[c]
        b_col = b_cols[c]
        diff_char = " "
        if a_col.dataType != b_col.dataType:
            diff_char = ">"
        elif a_col.nullable != b_col.nullable:
            diff_char = "!"
        common_diff.append((diff_char, a_col, b_col))

    return (
        [("-", a_cols[c], None) for c in sorted(a_cols_uniq)]
        + [("+", None, b_cols[c]) for c in sorted(b_cols_uniq)]
        + common_diff
    )
