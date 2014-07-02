# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import argparse
import shutil

import metadata

from pytak import please
from pytak import config

from pytak.logconf import setup_logging

def parse_options(argv):
    """
    Parse command line options

    Args:
      argv (list): command-line arguments
    """

    author_strings = []
    for name, email in zip(metadata.authors, metadata.emails):
        author_strings.append('Author: {0} <{1}>'.format(name, email))

    epilog = '''
{project} {version}

{authors}
Source: {url}
'''.format(project=metadata.project, version=metadata.version,
           authors='\n'.join(author_strings), url=metadata.url)

    # Configure command line parser
    args = argparse.ArgumentParser(prog=argv[0],
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description=metadata.description,
                                   epilog=epilog)

    # Print version
    args.add_argument(
        '-v', '--version',
        action='version',
        version='{0}. {1}'.format(metadata.project, metadata.version))

    return args

# ___________________________________________________________
#                                    Command Line parameters

def parse_proj_options(arg_parser):

    arg_parser.add_argument(
        '-d', '--destination',
        dest='dest',
        default=".",
        help="Points where PyTak project will be created. \
        If it is not specified current directory will be used.")

    arg_parser.add_argument(
        '-n', '--name',
        dest='name',
        help="Specifies PyTak project name.")

    return arg_parser.parse_args()

def parse_run_options(arg_parser):

    arg_parser.add_argument(
        '-p', '--project',
        dest='project',
        default=None,
        help="Full path to pytak project")

    arg_parser.add_argument(
        '-c', '--section',
        dest='section',
        default='main',
        help="Point which section from configuration file should be used.\
        Default is [main] section.")

    arg_parser.add_argument(
        '-s', '--scenario',
        dest='scenario',
        default=None,
        help="Specifies scenario that will be run.")

    arg_parser.add_argument(
        '--loglevel', '-L',
        dest='loglevel',
        default='INFO',
        help="Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL. Default is INFO.")

    arg_parser.add_argument(
        '--logfile',
        dest='logfile',
        default=None,
        help="Path to log file. If not set, log will go to stdout/stderr")

    return arg_parser.parse_args()

def prepare_exec_for_file(filename):
    """
    Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    module = []

    # Chop off file extensions or package markers
    if filename.endswith('.py'):
        filename = filename[:-3]
    elif os.path.split(filename)[1] == '__init__.py':
        filename = os.path.dirname(filename)
    else:
        raise BaseException('The file provided (%s) does exist but is not a '
                            'valid Python file.  This means that it cannot '
                            'be used as application.  Please change the '
                            'extension to .py' % filename)
    filename = os.path.realpath(filename)

    dirpath = filename
    while True:
        dirpath, extra = os.path.split(dirpath)
        module.append(extra)
        if not os.path.isfile(os.path.join(dirpath, '__init__.py')):
            break

    sys.path.insert(0, dirpath)
    return '.'.join(module[::-1])

# ___________________________________________________________
#                                         PyTak entry points

def project():
    args = parse_proj_options(parse_options(sys.argv))

    if args.name:
        __copy("template", args.dest + args.name)
        print("Project '%s', was created in '%s'" % (args.name, args.dest))
    else:
        raise AttributeError("Please specify PyTak project name. For more information type: pytak-run --help")

    sys.exit(0)

def run():
    args = parse_run_options(parse_options(sys.argv))

    # Setup logging
    setup_logging(args.loglevel, args.logfile)

    # Set pointed section
    config.section = args.section

    # Dynamic loadings
    if args.project and args.scenario:

        # Load PyTak project using full path
        sys.path.append(os.path.dirname(args.project))

        try:
            project = __import__(os.path.basename(please._remove_trailing(args.project)))
            sys.modules['project'] = project
        finally:
            del sys.path[-1]

        config.project_path = args.project

        # Load encryption/decryption
        crypto = prepare_exec_for_file(args.project + '/crypto.py')
        __import__(crypto)
        config.decrypt = getattr(sys.modules[crypto], 'decrypt', None)

        # Load scenario
        scene = prepare_exec_for_file(args.scenario)
        __import__(scene)

        # Call main method of the scenario
        scenario = getattr(sys.modules[scene], 'main', None)
        scenario()

    else:
        raise AttributeError("Scenario and PyTak project should be passed. For more information type: pytak-run --help")

# ___________________________________________________________
#                                           Helper functions

def __copy(template, dest):
    shutil.copytree(template, dest)
    return dest + "template"
