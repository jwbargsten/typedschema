import re
from dataclasses import FrozenInstanceError
from typing_extensions import Self


class FQTN(str):
    """Short for Fully Qualified Table Name. Simplify table name handling.

    :param ns: The namespace aka schema aka keyspace (and sometimes aka database).
    :param name: The table name
    """

    def __new__(cls, ns: str, name: str):
        if ns is None:
            raise ValueError("namespace is None")
        if name is None:
            raise ValueError("name is None")

        fqtn = f"{ns}.{name}"

        obj = str.__new__(cls, fqtn)
        return obj

    def __init__(self, ns: str, name: str):
        object.__setattr__(self, "ns", ns)
        object.__setattr__(self, "name", name)

    def __setattr__(self, name, value):
        raise FrozenInstanceError(f"cannot assign to field {name!r}")

    def __delattr__(self, name):
        raise FrozenInstanceError(f"cannot assign to field {name!r}")

    @classmethod
    def of(cls, table_name: str | Self):
        if isinstance(table_name, FQTN):
            return cls(table_name.ns, table_name.name)

        table_name = str(table_name)
        if not re.search(r"^\w+\.\w+$", table_name):
            raise ValueError(f'Could not derive namespace and table from "{table_name}".')

        ns, name = table_name.split(".", maxsplit=1)
        if not (ns and name):
            raise ValueError(f'Could not derive namespace and table from "{table_name}".')
        return cls(ns, name)

    @property
    def namespace(self) -> str:
        return self.ns

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}(ns='{self.ns}', name='{self.name}')"
