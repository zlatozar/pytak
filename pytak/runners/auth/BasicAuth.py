# -*- coding: utf-8 -*-

"""
    BaseAuth
    ~~~~~~~~

    Interprets configuration and provides REST client using basic authentication

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import json
import requests
import urllib2
import base64
import logging

from colorama import Fore, Style

CALL_TIMEOUT = 60

log = logging.getLogger(__name__)

call_methods = {'GET':requests.get, 'POST':requests.post, 'PUT':requests.put, 'DELETE':requests.delete}

def call(url, user_name, password, method, body, headers, filename=None):
    log.info("Hit %s (Basic Authentication)" % url)

    return call_methods[method](url, auth=(user_name, password), data=body, headers=headers,
                                verify=False, timeout=CALL_TIMEOUT)

def handle_reponse(response, is_json=False):

    if is_json:
        log.info("Server Response Content:")
        try:
            log.info(json.dumps(json.loads(response.content), indent=4))
        except:
            log.info("<no content>\n")

    if code_is_OK(response):
        return response.content

    raise ValueError(Fore.RED + "ERROR: %s %s" % (response.status_code, response.reason) + Style.RESET_ALL)

# ___________________________________________________________
#                                           Helper functions

def code_is_OK(resp):
    return True if resp.status_code >= 200 and resp.status_code <= 299 else False

def code_is_200_or_500(resp):
    return True if resp.status_code == 200 or resp.status_code == 500 else False

# def curl(url, user_name, password, call_type):
#     import pycurl
#     log.info("Hit %s" % url)

#     user_pwd = "%s:%s" % (user_name, password)

#     curl = pycurl.Curl()
#     curl.setopt(pycurl.URL, url)
#     curl.setopt(pycurl.USERPWD, user_pwd)

#     curl.setopt(pycurl.SSL_VERIFYPEER, 0)
#     curl.setopt(pycurl.SSL_VERIFYHOST, 0)

#     curl.setopt(pycurl.HTTPHEADER, ['Accept: application/xml', 'Content-Type: application/json'])

#     curl.setopt(pycurl.VERBOSE, 1)
#     curl.perform()

def check_auth(host, user_name, password):

    request = urllib2.Request(host)
    base64string = base64.encodestring('%s:%s' % (user_name, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)

    assert result.msg == 'OK'

# Simple test
if __name__ == '__main__':
    log.info(check_auth("http://localhost", 'test', 'test'))
