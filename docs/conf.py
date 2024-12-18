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

release = '0.0.1'

# -- General configuration
   
extensions = [
    'sphinx.ext.autodoc',
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
#epub_show_urls = 'footnote'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
#html_js_files = [("readthedocs.js", {"defer": "defer"})]







if globals().get('websupport2_base_url', False):
    websupport2_base_url = 'https://readthedocs.org/websupport'
    websupport2_static_url = 'https://assets.readthedocs.org/static/'
# Define this variable in case it's not defined by the user.
# It defaults to `alabaster` which is the default from Sphinx.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme
project = type("Project", (object,), {"analytics_disabled": False})  # Define a mock object

context = {
    'using_theme': using_rtd_theme,
    'html_theme': html_theme,
    'current_version': "latest",
    'version_slug': "latest",
    'MEDIA_URL': "https://media.readthedocs.org/",
    'STATIC_URL': "https://assets.readthedocs.org/static/",
    'PRODUCTION_DOMAIN': "readthedocs.org",
    'versions': [
    ("latest", "/en/latest/"),
    ("stable", "/en/stable/"),
    ],
    'downloads': [ 
    ("pdf", "//fcuff.readthedocs.io/_/downloads/en/latest/pdf/"),
    ("html", "//fcuff.readthedocs.io/_/downloads/en/latest/htmlzip/"),
    ("epub", "//fcuff.readthedocs.io/_/downloads/en/latest/epub/"),
    ],
    'subprojects': [ 
    ],
    'slug': 'fcuff',
    'name': u'fcuff',
    'rtd_language': u'en',
    'programming_language': u'py',
    'canonical_url': 'https://fcuff.readthedocs.io/en/latest/',
    'analytics_code': 'None',
    'single_version': False,
    'conf_py_path': '/docs/',
    'api_host': 'https://readthedocs.org',
    'github_user': 'SiegKat',
    'proxied_api_host': '/_',
    'github_repo': 'fcuff',
    'github_version': 'main',
    'display_github': True,
    'bitbucket_user': 'None',
    'bitbucket_repo': 'None',
    'bitbucket_version': 'main',
    'display_bitbucket': False,
    'gitlab_user': 'None',
    'gitlab_repo': 'None',
    'gitlab_version': 'main',
    'display_gitlab': False,
    'READTHEDOCS': True,
    'using_theme': (html_theme == "default"),
    'new_theme': (html_theme == "sphinx_rtd_theme"),
    'source_suffix': SUFFIX,
    'ad_free': False,
    'docsearch_disabled': False,
    'user_analytics_code': '',
}

# For sphinx >=1.8 we can use html_baseurl to set the canonical URL.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_baseurl
# For sphinx >=1.8 we can use html_baseurl to set the canonical URL.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_baseurl
if version_info >= (1, 8):
    if not globals().get('html_baseurl'):
        html_baseurl = context['canonical_url']
    context['canonical_url'] = None

# Extend context data
# No direct replacement for {% block extra_context %}; remove or process externally

if 'html_context' in globals():
    for key in context:
        if key not in html_context:
            html_context[key] = context[key]
else:
    html_context = context

# Add External version warning banner to the external version documentation
if version_type == 'external':  # Replace '{{ version.type }}' with Python variable
    extensions.insert(1, "readthedocs_ext.external_version_warning")
    readthedocs_vcs_url = vcs_url  # Replace '{{ vcs_url }}' with Python variable
    readthedocs_build_url = build_url  # Replace '{{ build_url }}' with Python variable

project_language = project_language_var  # Replace '{{ project.language }}' with Python variable

# User's Sphinx configurations
language_user = globals().get('language', en)
latex_engine_user = globals().get('latex_engine', None)
latex_elements_user = globals().get('latex_elements', None)

# Remove this once xindy gets installed in Docker image and XINDYOPS
# env variable is supported
latex_use_xindy = False


# Make sure our build directory is always excluded
exclude_patterns = globals().get('exclude_patterns', [])
exclude_patterns.extend(['_build'])
