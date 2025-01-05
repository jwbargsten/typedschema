pyspark-typedschema documentation
=================================

This is minimally intrusive library to type or annotate pyspark data frames.

There are existing projects which try to change how you interact with pyspark, but this
is not the goal of this library. Goals:

* Create a simple way to define a schema for a pyspark DataFrame.
* Supply some utility functions to test if the DataFrame adheres to a predefined schema.
* Enable schema column autocompletion in your editor
* Re-use existing stuff, such as `StructField`, from pyspark

In pyspark you have 3 ways of referencing a column:

.. code-block:: python

   df.col
   df['col']
   F.col('col')

All have their `advantages and disadvantages
<https://stackoverflow.com/questions/55105363/pyspark-dataframe-column-reference-df-col-vs-dfcol-vs-f-colcol>`_,
but a consistent way of dealing with column names, pyspark columns and schemas
in general feels patchy. typedschema tries to make it a bit more natural.

Define a schema

.. literalinclude:: snippets/examples-01-teaser.py
   :language: python

Because ``MySchema`` is a normal Python class, it can be auto-completed by
almost all editors. Additionally ``myschema.name`` is also a string. You can
use it more naturally:

.. literalinclude:: snippets/examples-02-teaser.py
   :language: python


Installation
------------

.. code-block:: sh

   pip install pyspark-typedschema


Tour
----

Definition
^^^^^^^^^^

You define a new schema by inheriting from :class:`typedschema.Schema`:

.. literalinclude:: snippets/examples-import.py
   :language: python

Now you can use ``myschema`` to generate a :class:`~pyspark.sql.DataFrame`:

.. literalinclude:: snippets/examples-create-df.py
   :language: python


.. literalinclude:: snippets/create-df.show.txt
   :language: none

.. literalinclude:: snippets/create-df.schema.txt
   :language: none

A :class:`~typedschema.Column` is also a string, so it behaves like a string.
If needed, you can also get a :class:`pyspark.sql.column.Column` object using
``.col`` or ``.c``.

.. literalinclude:: snippets/examples-col-is-string.py
   :language: python

.. literalinclude:: snippets/examples-col-ops.py
   :language: python

.. literalinclude:: snippets/col.show.txt
   :language: none

Comparing Schemas
^^^^^^^^^^^^^^^^^

I can test schema equality using `Python's set operations <https://docs.python.org/3/library/stdtypes.html#set>`_.

Implemented are ``issubset``, ``issuperset``, ``isequal`` and ``contains``.

.. literalinclude:: snippets/examples-set-ops-no-subset-missing-col.py
   :language: python

.. attention::

   Make sure that the typed schema object (or class) is on the left:

   .. code:: python

      myschema >= df.schema # WORKS
      myschema <= df.schema # WORKS

      df.schema >= myschema # will not work
      df.schema <= myschema # will not work


It can be difficult to see what exactly is different, therefore
:func:`~typedschema.diff_schemas` is available:

.. literalinclude:: snippets/examples-schema-diff.py
   :language: python

.. literalinclude:: snippets/schema-diff.print.txt
   :language: none

You can also dump it in a DataFrame if you want:

.. literalinclude:: snippets/examples-schema-diff-df.py
   :language: python

.. literalinclude:: snippets/schema-diff-df.show.txt
   :language: none

Often nullability is not so important, you can disable it via a function param
(this won't work with the operators, though):

.. literalinclude:: snippets/examples-set-ops-nullable.py
   :language: python

Code Generation
^^^^^^^^^^^^^^^

Most developers are relatively lazy, so typedschema has the functionality to
generate a class definiton from an existing schema or data frame:

.. literalinclude:: snippets/examples-codegen.py
   :language: python

will output

.. literalinclude:: snippets/examples-class-def.py
   :language: python

Related Projects
----------------

* `GitHub - kaiko-ai/typedspark: Column-wise type annotations for pyspark DataFrames <https://github.com/kaiko-ai/typedspark>`_
* `GitHub - getyourguide/TypedPyspark: Type-annotate your spark dataframes and validate them <https://github.com/getyourguide/TypedPyspark>`_

API Reference
-------------

.. toctree::
   :maxdepth: 2

   typedschema
