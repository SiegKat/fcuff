# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../fcuff'))


# -- Project information -----------------------------------------------------

project = 'fcuff'
copyright = '2024, Thiago Costa'
author = 'Thiago'

release = '0.1'
version = '0.0.1'


# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

#intersphinx_disabled_domains = ['std']
templates_path = ['_templates']
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


master_doc = 'index'
# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
#html_js_files = [("readthedocs.js", {"defer": "defer"})]




