# -*- coding: utf-8 -*-

"""
    XAuth
    ~~~~~

    Interprets configuration and provides REST client

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import json
import urllib
import urlparse
import oauth2 as oauth

import mimetools
import mimetypes
import logging

from os.path import basename
from colorama import Fore, Style

from pytak import config

CALL_TIMEOUT = 60
CALL_TIMEOUT_TOKEN = 30

log = logging.getLogger(__name__)

def init_client(usr_cred):
    """Initialize xauth client"""
    log.info("Let's create REST client")

    base_url = usr_cred['server']
    XAUTH_URI = usr_cred['xauth_uri']

    url = base_url + XAUTH_URI
    log.info("Hit %s" % url)

    user_name = usr_cred['user']
    password = usr_cred['password']
    consumer_key = usr_cred['consumer_key']
    consumer_secret = usr_cred['consumer_secret']
    domain = usr_cred['domain']

    consumer = oauth.Consumer(consumer_key, consumer_secret)

    def __obtain_token(name=None):
        if not name:
            name = user_name

        client = oauth.Client(consumer, timeout=CALL_TIMEOUT_TOKEN)
        client.add_credentials(name, password)
        client.disable_ssl_certificate_validation = True

        params = {
            'x_auth_username' : name,
            'x_auth_password' : password,
            'x_auth_mode'     : 'client_auth'
        }

        content = handle_reponse(client.request(url, method='POST', body=urllib.urlencode(params)))

        log.info("Successful login! PyTak rocks!")

        # Convert JSON to dictionary to ease elements selection
        return dict(urlparse.parse_qsl(content))

    def __obtain_token_with_retry():
        try:
            token = __obtain_token()

        except Exception:
            log.info("Fails with '%s'" % user_name)
            log.info("User: %s, Password: %s" % (user_name, password))
            name = user_name[:user_name.find('@')] if user_name.find('@') > 0 else user_name + domain
            log.info("Will try to login changing name from '%s' to '%s'" % (user_name, name))
            token = __obtain_token(name)

        return token

    access = __obtain_token_with_retry()
    access_token = oauth.Token(access['oauth_token'], access['oauth_token_secret'])

    rest_client = oauth.Client(consumer, access_token, timeout=CALL_TIMEOUT)
    rest_client.disable_ssl_certificate_validation = True

    return base_url, rest_client

# ___________________________________________________________
#                                           Helper functions

def handle_reponse(response, is_json=False):
    resp, content = response

    if is_json:
        log.info("Server Response Content:")
        try:
            log.info(json.dumps(json.loads(content), indent=4))
        except:
            log.info("<no content>")

    if code_is_OK(resp):
        return content

    raise ValueError(Fore.RED + "ERROR: %s %s" % (resp.status, resp.reason) + Style.RESET_ALL)

def code_is_OK(resp):
    return True if resp.status >= 200 and resp.status <= 299 else False

def code_is_200_or_500(resp):
    return True if resp.status == 200 or resp.status == 500 else False

def encode_multipart_formdata(filename):

    BOUNDARY = mimetools.choose_boundary()

    fpath = config.project_path + "/resources/" + filename
    file_name = basename(fpath)

    form_header = []
    form_header.append('--' + BOUNDARY)
    form_header.append('Content-Disposition: form-data; name="file"; filename="%s"' % file_name)
    form_header.append('Content-Type: %s' % mimetypes.guess_type(file_name)[0] or 'application/octet-stream')
    form_header.append('')
    # relative path
    form_header.append(open(fpath, 'rb').read())
    form_header.append('--' + BOUNDARY + '--')
    form_header.append('')

    body = '\r\n'.join(form_header)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

    headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
    return body, headers

def encode_multipart_formdata_params(filename, params=None, accept = 'application/json'):

    if params is None:
        params = {}

    myboundary = '--402B88190O37e4cacU20137eN6ab592bD0041RY'
    CRLF = '\r\n'

    ctype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    basefilename = basename(filename)

    filecontent = open(config.project_path + "/resources/" + filename, 'rb').read()

    lines = []
    for(key, value) in params.items():
        lines.append('--' + myboundary)
        lines.append('Content-Disposition: form-data; name="%s"' % key)
        lines.append('')
        lines.append(value)

    lines.append('--' + myboundary)
    lines.append('Content-Disposition: form-data; name="file"; filename="%s"' % basefilename)
    lines.append('Content-Type: %s' % ctype)
    lines.append('')
    lines.append(filecontent)
    lines.append('--' + myboundary + '--')

    upload_body = CRLF.join(lines)
    upload_headers = {'Content-Type':'multipart/form-data; boundary=' + myboundary, 'Accept': accept}

    return upload_body, upload_headers

# Simple test
if __name__ == '__main__':
    oauth.debuglevel = 1
