# -*- coding: utf-8 -*-

"""
    runners
    ~~~~~~~

    Contains various scenarios runners

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import re
import sys
import json
import operator
import logging

from pytak.please import convert_to_dotted, validate
from pytak.runners import tools
from pytak.runners.auth import XAuth
from pytak.runners.auth import BasicAuth

from pytak.runners.stack import Stack
from pytak.runners.parameters import read_config

__all__ = ['xauth_login', 'basic_login', 'trace',
           'run', 'run_function', 'perf', 'test', 'parallel']

log = logging.getLogger(__name__)

login_fn = None

def xauth_login():
    global login_fn
    login_fn = _login()

def basic_login(user_name, password):
    global login_fn
    login_fn = _login(user_name, password)

def _login(user_name=None, password=None):
    """Memorize the how to connect in a given host"""
    _env = Stack()

    # _rest_client exist? -> XAuth, else BasicAuth
    _rest_client = None
    _user_name = None
    _password = None

    if user_name and password:
        log.info("Use '%s' user" % user_name)
        _base_url = read_config()['server']
        _user_name = user_name
        _password = password

    else:
        log.info("Use Synthetic Monitor user")
        _base_url, _rest_client = XAuth.init_client(read_config())

    def login_closure():
        return (_base_url, _rest_client, _user_name, _password, _env)

    return login_closure

def trace(key=None):
    """
    Could be used during development from developers to see piled data in stack.
    """
    env = login_fn()[4]

    env.view(key)
    log.info("Normal exit after 'trace' function")
    sys.exit()

# ___________________________________________________________
#                                                    Runners

def run(scenario):
    """Call REST API nothing else"""
    env = login_fn()[4]

    if isinstance(scenario, list):
        for api in scenario:
            if hasattr(api, '__call__'):
                api = api.__call__()

            env.push(make_call(api, login_fn))

    else:
        if hasattr(scenario, '__call__'):
            scenario = scenario.__call__()

        env.push(make_call(scenario, login_fn))

    return env

def run_function(func, env=None):
    """Run function that use environment stack as data"""
    return func.__call__(env)

def test(scenario):
    """Call REST API and test returned JSON against JSONSchema"""
    env = login_fn()[4]

    if isinstance(scenario, list):
        for api in scenario:
            if hasattr(api, '__call__'):
                api = api.__call__()

            env.push(validate(make_call(api, login_fn)))

    else:
        if hasattr(scenario, '__call__'):
            scenario = scenario.__call__()

        env.push(validate(make_call(scenario, login_fn)))

    return env

def perf(scenario):
    """Call REST API and save time in stack so statistical functions could be run on top of it"""

    log.error("Not implemented")
    return {}

def parallel(scenario):
    """Call REST APIs at once"""

    log.error("Not implemented")
    return {}

# ___________________________________________________________
#                                                   Selector

class select(object):

    def __init__(self, clazz):
        self.env = login_fn()[4]

        self.regex = None
        self.clazz = str(clazz)
        self.all_predicates = []
        self.any_predicates = []

    def then_key(self, id):
        log.info("Have to select: %s" % id)

        self.regex = re.sub('\*', '([0-9]+)', id)
        log.info("RegEx is: %s" % self.regex)

        matched_keys = []
        for a_class in self.env:
            if a_class['class'] == self.clazz:
                for key, value in a_class.iteritems():
                    # stored in UNICODE
                    match = re.match(self.regex, key, re.UNICODE)

                    all = True
                    any = True

                    if match:
                        # Here is the idea: We connect two keys using first index.
                        #
                        # For example:
                        # We check value of key 'entry.15.data.createDate' with predicate,
                        # if succeeds we select value of 'entry.15.data.id'. Both have index 15.

                        # all
                        if self.all_predicates:
                            idx = match.group(1)
                            all = reduce(operator.and_, [f(a_class, idx) for f in self.all_predicates])

                        # any
                        if self.any_predicates:
                            idx = match.group(1)
                            any = reduce(operator.or_, [f(a_class, idx) for f in self.any_predicates])

                        if all and any:
                            matched_keys.append(value)

                        else:
                            log.debug("Skip '%s' because predicate returns: False" % value)

        log.info("Selected are: %s" % matched_keys)
        return matched_keys

    def iff(self, *predicate_func):
        """select().iff().then_key()"""

        for func in predicate_func:
            self.all_predicates.append(func)

        return self

    def if_any(self, *predicate_func):
        """select().if_any().then_key()"""

        for func in predicate_func:
            self.any_predicates.append(func)

        return self

# ___________________________________________________________
#                                           Helper functions

def make_call(api_object, login_func):
    base_url, rest_client, user_name, password, env = login_func()

    # prepare for REAL call
    tools.form_request_body(api_object, env)
    tools.form_uri(api_object, env)

    log.info("Do HTTP call using '%s' object. Expected response code %s" % (api_object, api_object.response_code))
    log.info("%s : %s" % (api_object.call_type, base_url + api_object.uri))

    if hasattr(api_object, 'upload'):
        body, headers = XAuth.encode_multipart_formdata(api_object.upload)

    else:
        body = json.dumps(api_object.request_body)
        headers = api_object.headers
        if api_object.request_body:
            log.info("REQUEST BODY:")
            log.info(json.dumps(api_object.request_body, indent=4) + "\n")


    try:

        if rest_client:
            content = XAuth.handle_reponse(rest_client.request(base_url + api_object.uri,
                                                               method  = api_object.call_type,
                                                               # body could be empty
                                                               body    = body,
                                                               headers = headers), True)
        else:
            content = BasicAuth.handle_reponse(BasicAuth.call(base_url + api_object.uri, user_name, password,
                                                              method  = api_object.call_type,
                                                              # body could be empty
                                                              body    = body,
                                                              headers = headers), True)
    except:
        env.view()
        raise

    try:
        valuable_content = json.loads(content) if len(content) > 0 else None

    except:
        valuable_content = json.loads(content)

    return convert_to_dotted(valuable_content, str(api_object)) \
        if valuable_content else {"class" : api_object}
