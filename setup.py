# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages

sys.path.append('.')
from pytak import metadata

# Helper function
def __read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()

# See here for more options:
#     http://pythonhosted.org/setuptools/setuptools.html
setup_dict = dict(

    license=metadata.license,
    name=metadata.package,
    description=metadata.description,
    long_description=__read('README'),
    version=metadata.version,

    author=metadata.authors[0],
    author_email=metadata.emails[0],

    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],

    url=metadata.url,
    download_url=metadata.url,

    # Find a list of classifiers here:
    #     http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
    ],

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'Sphinx',
        'httplib2',
        'requests',
        'oauth2',
        'pytest',
        'pexpect',
        'jsonschema',
        'texttable',
        'colorama'
    ],

    platforms='any',
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'pytak-project = pytak.main:project',
            'pytak-run = pytak.main:run'
        ]
    }
)

def main():
    setup(**setup_dict)

if __name__ == '__main__':
    main()
