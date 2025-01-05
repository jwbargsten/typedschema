from typing import (
    Any,
    Hashable,
)
from typing_extensions import Self

import pyspark.sql.functions as F
from pyspark.sql.column import Column as PysparkColumn
from pyspark.sql.types import DataType, StructField


class Column(str):
    """
    A column in a named schema. It is also a string, so it behaves like a string.

    You can call e.g. :func:`~pyspark.sql.functions.col` on it.

    .. code-block:: python

        import pyspark.sql.functions as F
        from typedschema import Column

        name = Column(StringType(), nullable=True)

        F.col(name) # works like a string
        name.col    # also works
        name.c      # alias for name.col -> for the lazy ones

    Common PySpark functions, such as :func:`~Column.cast` or :func:`~Column.dtype`, are aliased.

    :param dtype: the :class:`~pyspark.sql.types.DataType`
    :param nullable: is it nullable?
    :param meta: meta information
    :param name: usually not needed, only for name classes. See :class:`Schema` for more info
    """

    # https://stackoverflow.com/questions/2673651/inheritance-from-str-or-int
    field: StructField

    def __new__(
        cls,
        dtype: DataType,
        nullable: bool = False,
        meta: dict[str, Any] | None = None,
        name: str | None = None,
    ):
        if name is None:
            name = ""
        obj = str.__new__(cls, name)
        obj.field = StructField(name, dtype, nullable, metadata=meta)
        return obj

    def __init__(
        self,
        dtype: DataType,
        nullable: bool = False,
        meta: dict[Hashable, Any] | None = None,
        name: str = None,
    ):
        # placeholder to have the completion show the right args
        pass

    def _with_name_if_unnamed(self, name):
        if self.field.name:
            return self
        return self._with_name(name)

    def _with_name(self, name):
        cls = type(self)
        f = self.field
        return cls(f.dataType, f.nullable, meta=f.metadata, name=name)

    @classmethod
    def from_structfield(cls, field: StructField):
        return cls(field.dataType, nullable=field.nullable, meta=field.metadata, name=field.name)

    @property
    def col(self) -> PysparkColumn:
        """
        Transform the column to a pyspark column
        """
        return F.col(self)

    @property
    def c(self) -> PysparkColumn:
        """Alias for as col"""
        return self.col

    def cast(self, dtype: str | DataType) -> PysparkColumn:
        """
        Cast this column to a different data type.

        Shortcut for F.col().cast()
        """
        return self.col.cast(dtype)

    def alias(self, name: Self | str) -> PysparkColumn:
        """
        Alias this column.

        Shortcut for F.col().alias()
        """
        return self.col.alias(name)

    @property
    def name(self) -> str:
        """The name of the column"""
        return self.field.name

    @property
    def dtype(self) -> DataType:
        """The data type of the column"""
        return self.field.dataType
