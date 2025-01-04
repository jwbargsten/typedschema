from typing import Sequence
from pyspark.sql.types import StructField, StructType

from .schema import _unpack_schema, RESERVED_FIELDS, Schema
from .string import camel_to_snake


def as_named_schema_class_def(s: Sequence[StructField] | StructType | Schema, name="UnnamedSchema"):
    """
    Generate Python code for a Schema from a spark/sequence of structfields/Schema

    :param s: input schema information
    :param name: the name of the class
    :return: Python code for the Schema that can be copy/pasted into your project.
    """
    fields = _unpack_schema(s)
    res = [f"class {name}(Schema):"]
    for f in fields:
        args = [repr(f.dataType), repr(f.nullable)]

        if f.metadata:
            args.append(f"meta={repr(f.metadata)}")

        if f.name in RESERVED_FIELDS:
            attr_name = f"{f.name}_"
            args.append(f"name={repr(f.name)}")
        else:
            attr_name = f.name

        res.append(f"    {attr_name} = Column({', '.join(args)})")
    var_name = camel_to_snake(name)
    res.append(f"{var_name} = {name}()")

    return "\n".join(res)
