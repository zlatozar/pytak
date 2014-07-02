# -*- coding: utf-8 -*-

"""
    logconf
    ~~~~~~~

    Setup logging framework and configure console messages
"""

import sys
import socket
import logging

host = socket.gethostname()

def setup_logging(loglevel, logfile):

    numeric_level = getattr(logging, loglevel.upper(), None)

    if numeric_level is None:
        raise ValueError("Invalid log level: %s" % loglevel)

    log_format = "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(host)
    logging.basicConfig(level=numeric_level, filename=logfile, format=log_format)

    sys.stderr = StdErrWrapper()
    sys.stdout = StdOutWrapper()

stdout_logger = logging.getLogger("stdout")
stderr_logger = logging.getLogger("stderr")

class StdOutWrapper(object):
    def write(self, s):
        stdout_logger.info(s.strip())

class StdErrWrapper(object):
    def write(self, s):
        stderr_logger.error(s.strip())

console_logger = logging.getLogger("console_logger")

# create console handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# formatter that doesn't include anything but the message
handler.setFormatter(logging.Formatter('%(message)s'))
console_logger.addHandler(handler)
console_logger.propagate = False
