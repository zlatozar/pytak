# -*- coding: utf-8 -*-

"""
    please
    ~~~~~~

    Helper functions for the end user

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import pexpect
import logging

__all__ = ['validate', 'show_needed_params', 'send_remote_command',
           'compare_json', 'compare_dict', 'convert_to_dotted']

PROMPT = ['# ', '>>> ', '> ', '\$ ']

log = logging.getLogger(__name__)


def show_needed_params(api_object):
    """Shows parameters that should be filled"""
    log.info("All needed parameters that must be filled are: ", api_object.needed_params())

def send_remote_command(user, host, password, cmd, split_symbol='\n'):
    """Send BASH command using 'expect' and returns command result as list"""
    child = __connect(user, host, password)
    result = __send_command(child, cmd, split_symbol)
    return result

def validate(json_data, json_schema):
    log.info("Validating output... ")
    return json_data

def compare_json(json_master, json_slave):
    """Compares two JSON structures."""

    master = convert_to_dotted(json_master)
    slave = convert_to_dotted(json_slave)

    compare_dict(master, slave)

    for key in master:
        if not slave[key] == master[key]:
            log.info("'%s' != '%s' for key '%s'" % (slave[key], master[key], key))
            raise AssertionError("Expected data is '%s'" % master[key])

    log.info("Done")

def compare_dict(master, slave):
    """
    Compares two flat JSON structures(dictionaries).
    It is not fatal if master contains more data than slave.
    """
    unmatched_items = set(master.items()) ^ set(slave.items())
    if len(unmatched_items) > 0:
        log.info(unmatched_items)
        return False

    log.info("JSONs are equal")
    return True

def _remove_trailing(full_path, symbol='/'):
    if full_path.endswith(symbol):
        return full_path[:-1]

    return full_path

def convert_to_dotted(data, class_name=None):
    """
    Converts JSON format to flat dictionary structure that will be saved in stack environment

    To represent nested JSON structure we use dots e.g. { 'b.0.c': 2, 'b.1.d': 3 }.
    Argument 'class' is used to mark who produced result.
    """

    flat = {}
    if class_name:
        flat.update({'class': class_name})

    def inner_prefix(json, prefix=None):

        if isinstance(json, dict):
            for key, value in json.iteritems():
                inner_prefix(value, prefix + key + "." if prefix else key + ".")

        elif isinstance(json, list):
            for idx, value in enumerate(json):
                inner_prefix(value, prefix + str(idx) + "." if prefix else str(idx) + ".")

        else:
            # remove trailing dot
            flat[prefix[:-1]] = json

        return flat

    return inner_prefix(data)

# ___________________________________________________________
#                                           Helper functions

def __send_command(child, cmd, split_symbol='\n'):
    child.sendline(cmd)
    child.expect(PROMPT)
    slices = child.before.split(split_symbol)[1:-1]

    return split_symbol.join(slices)

def __connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'

    conn_cmd = 'ssh ' + user + '@' + host
    child = pexpect.spawn(conn_cmd)

    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        log.info('[-] Error Connecting')
        return

    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])

    if ret == 0:
        log.info('[-] Error Connecting')
        return

    child.sendline(password)
    child.expect(PROMPT)

    return child
