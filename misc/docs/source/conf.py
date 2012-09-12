# -*- coding: utf-8 -*-
#
# ObsPy Tutorial documentation build configuration file
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import glob
import os
import sys


import pprint
pprint.pprint(sys.path)
tmp = ['/home/docs/sites/readthedocs.org/bin',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/distribute-0.6.28-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.sh-0.5.2.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.segy-0.5.2.dev-py2.7-linux-x86_64.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.mseed-0.7.0.dev-py2.7-linux-x86_64.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.earthworm-0.1.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.realtime-0.1.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.xseed-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.seedlink-0.0.4.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.sac-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.imaging-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.neries-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/suds-0.4-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.wav-0.5.1.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.datamark-0.1.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.signal-0.7.0.dev-py2.7-linux-x86_64.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.seisan-0.5.1.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.iris-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.gse2-0.7.0.dev-py2.7-linux-x86_64.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.db-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/SQLAlchemy-0.7.8-py2.7-linux-x86_64.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.seg2-0.7.0.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.seishub-0.5.1.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.arclink-0.7.1.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages/obspy.core-0.7.1.dev-py2.7.egg',
 '/home/docs/sites/readthedocs.org/lib/python2.7',
 '/home/docs/sites/readthedocs.org/lib/python2.7/plat-linux2',
 '/home/docs/sites/readthedocs.org/lib/python2.7/lib-tk',
 '/home/docs/sites/readthedocs.org/lib/python2.7/lib-old',
 '/home/docs/sites/readthedocs.org/lib/python2.7/lib-dynload',
 '/usr/lib/python2.7',
 '/usr/lib/python2.7/plat-linux2',
 '/usr/lib/python2.7/lib-tk',
 '/home/docs/sites/readthedocs.org/lib/python2.7/site-packages',
 '/usr/local/lib/python2.7/site-packages',
 '/usr/local/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages',
 '/usr/lib/python2.7/dist-packages/PIL',
 '/usr/lib/python2.7/dist-packages/gtk-2.0',
 '/usr/lib/pymodules/python2.7'] + sys.path
sys.path = tmp
pprint.pprint(sys.path)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.1'

# Add extensions into path
sys.path = [os.path.dirname(__file__) + os.sep + '_ext'] + sys.path

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.intersphinx',
              'sphinx.ext.doctest',
              'sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'matplotlib.sphinxext.only_directives',
              # local extensions
              'autosummary',
              'plot_directive',
              'obspydoc'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf - 8 - sig'

# The master toctree document.
master_doc = 'contents'

# General information about the project.
project = u'ObsPy Documentation'
copyright = u'2012, The ObsPy Development Team (devs@obspy.org)'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.3'
# The full version, including alpha/beta/rc tags.
release = '0.3'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%B %d %H o'clock, %Y"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['**/.svn', '_build', '_templates', '_ext']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['obspy.']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "ObsPy Documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo =

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%dT%H:%M:%S'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}
html_sidebars = {
   '**': ['localtoc.html', 'sourcelink.html', 'searchbox.html']
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
html_additional_pages = {'index': 'index.html'}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'ObsPyDocumentation'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'ObsPyDocumentation.tex', u'ObsPy Tutorial',
   u'The ObsPy Development Team (devs@obspy.org)', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'obspydocumentation', u'ObsPy Documentation',
     [u'The ObsPy Development Team (devs@obspy.org)'], 1)
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('http://docs.python.org/2.7/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
    'matplotlib': ('http://matplotlib.sourceforge.net/', None),
    'sqlalchemy': ('http://docs.sqlalchemy.org/en/latest/', None),
}

# generate automatically stubs
autosummary_generate = glob.glob("packages" + os.sep + "*.rst")

# Don't merge __init__ method in auoclass content
autoclass_content = 'class'

# This value is a list of autodoc directive flags that should be automatically
# applied to all autodoc directives. The supported flags are 'members',
# 'undoc-members', 'private-members', 'special-members', 'inherited-members' and
# 'show-inheritance'. Don't set it to anything !
autodoc_default_flags = ['show-inheritance']
