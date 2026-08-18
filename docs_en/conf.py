# Configuration file for the Sphinx documentation builder.
# English version configuration

# -- Project information -----------------------------------------------------

project = 'DuIvyTools'
copyright = '2022-2024, CharlesHahn, DuIvy'
author = 'CharlesHahn, DuIvy'
version = '0.6.0'
release = '0.6.0'

# -- General configuration ---------------------------------------------------

extensions = ['recommonmark', "sphinx.ext.mathjax"]

templates_path = ['templates']

language = "en"

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['../static']

from recommonmark.parser import CommonMarkParser
source_parsers = {
    ".md": CommonMarkParser,
}
source_suffix = [".rst", ".md"]
