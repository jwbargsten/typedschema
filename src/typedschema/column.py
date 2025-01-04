from typing import (
    Any,
    Dict,
    Optional,
    Hashable,
)

import pyspark.sql.functions as F
from pyspark.sql.column import Column as PysparkColumn
from pyspark.sql.types import DataType, StructField


class Column(str):
    """
    A column in a named schema. Behaves like a string, but you can call :func:`pyspark.sql.functions.col` on it.

    :param dtype: the :class:`DataType`
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
        meta: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
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
    def fcol(self) -> PysparkColumn:
        """
        Transform the column to a pyspark column
        """
        return F.col(self)

    def cast(self, dtype: str | DataType) -> PysparkColumn:
        """
        Cast this column to a different data type.

        Shortcut for F.col().cast()
        """
        return self.fcol.cast(dtype)

    def alias(self, name: "Column" | str) -> PysparkColumn:
        """
        Alias this column.

        Shortcut for F.col().alias()
        """
        return self.fcol.alias(name)

    @property
    def name(self) -> str:
        """The name of the column"""
        return self.field.name

    @property
    def dtype(self) -> DataType:
        """The data type of the column"""
        return self.field.dataType
