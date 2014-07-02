# -*- coding: utf-8 -*-

"""
    parameters
    ~~~~~~~~~~

    Reads PyTak project configuration file

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import os
import logging

from ConfigParser import SafeConfigParser

import pytak.config
import pytak.please

from pytak.runners import tools

log = logging.getLogger(__name__)

@tools.memoize
def read_config(section=pytak.config.section):
    """Reads configuration from <path_to_pytak_project>/<project_name>.cfg"""

    file_parser = SafeConfigParser()

    project_path = pytak.please._remove_trailing(pytak.config.project_path)
    project_name = os.path.basename(project_path)

    log.info("Project path: %s, Name: %s, Section: %s" % (project_path, project_name, section))

    file_parser.read(os.path.expanduser(project_path + '/' + project_name + '.cfg'))

    decrypt_key = file_parser.get(pytak.config.section, 'key')

    if not decrypt_key:
        raise ValueError("ERROR: Can't find a key to decrypt passwords")

    config = {
        'server'   : file_parser.get(section, 'server'),
        'user'     : file_parser.get(section, 'user'),
        'password' : decrypt(file_parser.get(section, 'password'), decrypt_key),

        'consumer_key'    : file_parser.get(section, 'consumer_key'),
        'consumer_secret' : decrypt(file_parser.get(section, 'consumer_secret'), decrypt_key),
        'xauth_uri' :  file_parser.get(section, 'xauth_uri'),
        'domain' : file_parser.get(section, 'domain')
    }

    return config

# Proxy. Decryption could be configured by user
def decrypt(cypher, key):
    return pytak.config.decrypt(cypher, key)
