import os
import sys

# Add paths for imports
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../fcuff'))

# Project information
project = 'fcuff'
copyright = '2024, Thiago Costa'
author = 'Thiago'
release = '0.1'
version = '0.0.1'

# Check if on Read the Docs
on_rtd = os.environ.get('READTHEDOCS', '').lower() == 'true'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
]

# Conditionally include Read the Docs extension
if on_rtd:
    try:
        import readthedocs_ext.readthedocs
        extensions.append("readthedocs_ext.readthedocs")
    except ImportError:
        print("readthedocs_ext not found - skipping")

# Paths and configuration
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
master_doc = 'index'

# Context and additional settings
commit = os.environ.get('COMMIT', '00000000')
version_type = os.environ.get('VERSION_TYPE', 'internal')
context = {
    'commit': commit[:8],
    'vcs_url': os.environ.get('VCS_URL', ''),
    'build_url': os.environ.get('BUILD_URL', ''),
}
html_context = globals().get('html_context', {})
html_context.update(context)
