# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

from typedschema._version import __version__

project = "pyspark-typedschema"
copyright = "2025, Joachim Bargsten"
author = "Joachim Bargsten"
version = __version__
release = __version__


extensions = [
    "myst_parser",
    # "myst_nb",
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]
html_title = "typedschema"

# html_theme_options = {"logo": {"text": "ABC"}}
autodoc_typehints = "description"
autodoc_class_signature = "separated"

html_context = {
    # "github_url": "https://github.com", # or your GitHub Enterprise site
    "github_user": "jwbargsten",
    "github_repo": "typedschema",
    "github_version": "main",
    "doc_path": "docs",
}
