# -*- coding: utf-8 -*-

from pytak import __version__

"""Information describing the project."""


# The package name, which is also the "UNIX name" for the project.
package = 'pytak'

project = "An Awesome Python Module to create scenarios that test REST API"
project_no_spaces = project.replace(' ', '')

version = __version__
description = 'Orchestration of REST API call are now easy'

authors = ['Zlatozar Zhelyazkov']
authors_string = ', '.join(authors)
emails = ['zlatozar@gmail.com']

license = 'BSD'
copyright = '2014 ' + authors_string

url = 'https://github.com/zlatozar/pytak'
