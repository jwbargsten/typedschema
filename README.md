# typedschema

This is minimally intrusive library to type or annotate pyspark data frames.

There are existing projects which try to change how you interact with pyspark, but this
is not the goal of this library. Goals:

* Create a simple way to define a schema for a pyspark DataFrame.
* Supply some utility functions to test if the DataFrame adheres to a predefined schema.
* Enable schema column autocompletion in your editor
* Re-use existing stuff, such as `StructField`, from pyspark

**For full documentation see [typedschema documentation](https://jwbargsten.github.io/typedschema/)**
