import re
from dataclasses import FrozenInstanceError


class FQTN(str):
    """Short for Fully Qualified Table Name. Simplify table name handling.

    Parameters
    ----------
    name : str
        The table name
    ns : str
        The namespace aka schema aka keyspace (and sometimes aka database).
    """

    def __new__(cls, name: str, ns: str):
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
    def from_any(cls, fqtn):
        if isinstance(fqtn, FQTN):
            return cls(fqtn.name, fqtn.ns)
        return cls.from_str(str(fqtn))

    @classmethod
    def from_str(cls, tableName: str):
        if not re.search(r"^\w+\.\w+$", tableName):
            raise ValueError(f'Could not derive namespace and table from "{tableName}".')

        ns, name = tableName.split(".", maxsplit=1)
        if not (ns and name):
            raise ValueError(f'Could not derive namespace and table from "{tableName}".')
        return cls(ns, name)

    @property
    def namespace(self):
        return self.ns

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}(ns='{self.ns}', name='{self.name}')"
