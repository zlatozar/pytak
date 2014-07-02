# -*- coding: utf-8 -*-

import os
from ..metadata import version, copyright, project_name

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

# autoclass options
#autoclass_content = "both"

# Add any paths that contain templates here, relative to this directory.
#templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General substitutions.
project = project_name
copyright = copyright

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.

# The full version, including alpha/beta/rc tags.
release = version

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

exclude_dirnames = ["tests"]

# Options for HTML output

html_show_sourcelink = False
html_file_suffix = ".html"

html_theme = 'haiku'
