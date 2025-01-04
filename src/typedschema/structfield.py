from typing import (
    Callable,
    Sequence,
    Set,
    TypeVar,
)

from pyspark.sql.types import StructField

T = TypeVar("T")


def sf_with_lc_colname(sf):
    return StructField(
        name=sf.name.lower(),
        dataType=sf.dataType,
        nullable=sf.nullable,
        metadata=sf.metadata,
    )


def sf_with_nullable(sf):
    return StructField(
        name=sf.name,
        dataType=sf.dataType,
        nullable=True,
        metadata=sf.metadata,
    )


def sf_without_metadata(sf):
    return StructField(
        name=sf.name,
        dataType=sf.dataType,
        nullable=sf.nullable,
        metadata=None,
    )


def sf_apply(
    xs: Sequence[StructField],
    ys: Sequence[StructField],
    fn: Callable[[Set[StructField], Set[StructField]], T],
    *,
    case_sensitive: bool = False,
    strict_null: bool = True,
) -> T:
    """Apply fn to two sets (xs, ys) of structfields.

    Mostly to compare stuff, e.g. fn can be ``==`` to test if xs and ys are equal.

    Parameters
    ----------
    xs :
        xs
    ys :
        ys
    fn :
        A function that gets normalised versions xs and ys. Example would be ``fn=lambda xs, ys: xs == ys``
    case_sensitive :
        the StructField names are case-sensitive ?
    strict_null :
        if yes, keep the ``nullable`` field as is, otherwise (if False) set nullable always to True.
    """
    # we don't use metadata for anything
    xs = [sf_without_metadata(x) for x in xs]
    ys = [sf_without_metadata(y) for y in ys]

    if not case_sensitive:
        xs = [sf_with_lc_colname(x) for x in xs]
        ys = [sf_with_lc_colname(y) for y in ys]

    if not strict_null:
        xs = [sf_with_nullable(x) for x in xs]
        ys = [sf_with_nullable(y) for y in ys]

    return fn(set(xs), set(ys))
