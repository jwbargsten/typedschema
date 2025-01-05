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
    "sphinx.ext.viewcode",
    # "sphinx_design",
    # "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
]

autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jwbargsten/typedschema",  # required
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        }
    ],
    "analytics": {
        "plausible_analytics_domain": "jwbargsten.github.io/typedschema",
        "plausible_analytics_url": "https://plausible.io/js/script.js",
    },
    "use_edit_page_button": False,
}

html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]
html_title = "typedschema"

autodoc_typehints = "description"
autodoc_class_signature = "separated"

html_context = {
    # "github_url": "https://github.com", # or your GitHub Enterprise site
    "github_user": "jwbargsten",
    "github_repo": "typedschema",
    "github_version": "main",
    "doc_path": "docs",
}

intersphinx_mapping = {
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "pyspark": ("https://spark.apache.org/docs/latest/api/python/", None),
}


# html_sidebars = {
#     "**": ["sidebar-nav-bs"],
#     "index": [],
# }
