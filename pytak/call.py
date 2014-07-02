# -*- coding: utf-8 -*-

"""
    Call
    ~~~~

    Meta-classes definition that all REST call classes should inherit.
    Class for upload operation is different - RESTUpload all others should use REST.

    Here also we overwrite + and <<

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import re
import json
import random
import string
import logging

from uuid import uuid4

from pytak import json_tools

log = logging.getLogger(__name__)

class MetaInit(type):

    def __new__(cls, name, bases, attrs):

        def init(self, assign=None, bind=None):
            # User overwrite or add new e.g. {'tag': 1234, 'xy.1.y.0.y1': 5}
            self.assign = assign
            # Points out how to search in environment, value of the parameter
            # e.g. { 'tag_id': 'xy.1.y.0.y1' }
            self.bind = bind

            # Set default values. Case sensitive.
            self.call_type = "GET"
            self.response_code = 200
            self.headers = {
                'Content-Type' : 'application/json',
                'Accept'       : 'application/json'
            }
            self.uri = ""
            self.request_body = {}
            self.output_schema = {}

            # Propagate call specific
            self.fill_call_data()

        def setattr(self, name, value):
            if name == 'assign' and value:
                randomize(value)

            if name == 'request_body' and value:
                randomize(value)

            object.__setattr__(self, name, value)

        # Used in stack environment for better display
        def repr(self):
            return self.__class__.__name__

        attrs['__init__'] = init
        attrs['__setattr__'] = setattr
        attrs['__repr__'] = repr

        return super(MetaInit, cls).__new__(cls, name, bases, attrs)

# ___________________________________________________________
#                                          Inherit from this

class REST(object):

    # System variable
    __metaclass__ = MetaInit

    # Override plus
    def __add__(self, query_parameters):
        self.__url_concat(query_parameters)

        def __call_wrapper(assign=None, bind=None):

            def init(self, assign=None, bind=None):
                log.debug("Re-born object '%s' with new URI" % self)
                self.assign = assign
                self.bind = bind

            def setattr(self, name, value):
                if name == 'assign' and value:
                    randomize(value)

                if name == 'request_body' and value:
                    randomize(value)

                object.__setattr__(self, name, value)

            def repr(self):
                return self.__class__.__name__

            return type(self.__repr__(), (object,),
                        { '__init__'    : init,
                          '__setattr__' : setattr,
                          '__repr__'    : repr,

                          'call_type'     : self.call_type,
                          'response_code' : self.response_code,
                          'headers'       : self.headers,
                          'uri'           : self.uri,
                          'request_body'  : self.request_body,
                          'output_schema' : self.output_schema})

        return __call_wrapper(assign=None, bind=None)

    # Override left shift
    def __lshift__(self, new_request_body):
        json.dumps(new_request_body)

        if self.call_type in ("POST", "PUT", "PATCH"):
            self.request_body = new_request_body
        else:
            raise ValueError("Only POST, PUT, PATCH method can have JSON request body")

        def __call_wrapper(assign=None, bind=None):

            def init(self, assign=None, bind=None):
                log.debug("Re-born object '%s' with new injected Request Body" % self)
                self.assign = assign
                self.bind = bind

            def setattr(self, name, value):
                if name == 'assign' and value:
                    randomize(value)

                if name == 'request_body' and value:
                    randomize(value)

                object.__setattr__(self, name, value)

            def repr(self):
                return self.__class__.__name__

            return type(self.__repr__(), (object,),
                        { '__init__'    : init,
                          '__setattr__' : setattr,
                          '__repr__'    : repr,

                          'call_type'     : self.call_type,
                          'response_code' : self.response_code,
                          'headers'       : self.headers,
                          'uri'           : self.uri,
                          'request_body'  : self.request_body,
                          'output_schema' : self.output_schema})

        return __call_wrapper(assign=None, bind=None)

    def __url_concat(self, params):
        s = self.uri

        query = params if params.startswith("?") else "?" + params

        # remove [?query_parameters] placeholder
        if "[?query_parameters]" in s:
            self.uri = s[:s.index("[")] + query
            log.info("Rewritten URI is: %s" % self.uri)
        else:
            raise ValueError("Query parameters are not allowed")

# ___________________________________________________________
#                                           Helper functions

def randomize(json):
    """Search for [XXXX*] or [DDDD*] pattern and replace it.

    Args:
      json (json): JSON that should be added in request body.

    Returns:
      JSON which values containing [XXXX*] or [DDDD*] are replaced.
    """
    return json_tools.update_leaf_if_value_func(json, randomize_text)

def randomize_text(line):
    """Randomize only values that are strings.

    Args:
      line (str): JSON value.

    Returns:
      str where [XXXX*] or [DDDD*] are replaced.
    """
    if not isinstance(line, basestring):
        return line

    return __replace_xxxx(__replace_dddd(line))

def __replace_xxxx(line):
    """Replace [XXXX*] (not less than four) with alphanumeric value with the XXXX* length.

    Args:
      line (str): JSON value.

    Returns:
      str where [XXXX*] is replaced with alphanumeric.
    """
    new_line = line
    xxxx_pat = re.compile(r'\[X{4}X*\]', re.IGNORECASE)
    for a_match in re.finditer(xxxx_pat, line):
        new_line = re.sub(xxxx_pat,
                          __get_random_alphanumeric(len(a_match.group(0)) - 2),
                          new_line, count=1)

    return new_line

def __replace_dddd(line):
    """Replace [DDDD*] (not less than four) with random digits with the DDDD* length.

    Args:
      line (str): JSON value.

    Returns:
      str where [DDDD*] is replaced with digits.
    """
    new_line = line
    dddd_pat = re.compile(r'\[D{4}D*\]', re.IGNORECASE)

    for a_match in re.finditer(dddd_pat, line):
        new_line = re.sub(dddd_pat,
                          __get_random_int(len(a_match.group(0)) - 2),
                          new_line, count=1)

    return new_line

def __get_random_int(length):
    """Returns random integer with a given length.

    Args:
      length (int): define the random integer length.

    Returns:
      int with a given length.
    """
    rsize = '{0:0%s}' % length
    return rsize.format(random.randint(1, 10000000))[:length]

def __get_random_alphanumeric(length):
    return str(uuid4())[:length]

# Not used for now
def __get_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

# ___________________________________________________________
#                       Inherit from this if request uploads

class MetaInitUpload(type):

    def __new__(cls, name, bases, attrs):

        def init(self, upload, assign=None, bind=None):
            # File that should be attached
            self.upload = upload

            self.assign = assign
            self.bind = bind

            # Set default values. Case sensitive.
            self.call_type = "POST"
            self.response_code = 201
            self.headers = {}
            self.uri = ""
            self.request_body = {}
            self.output_schema = {}

            # Propagate call specific
            self.fill_call_data()

        def setattr(self, name, value):
            if name == 'assign' and value:
                randomize(value)

            if name == 'request_body' and value:
                randomize(value)

            object.__setattr__(self, name, value)

        def repr(self):
            return self.__class__.__name__

        attrs['__init__'] = init
        attrs['__setattr__'] = setattr
        attrs['__repr__'] = repr

        return super(MetaInitUpload, cls).__new__(cls, name, bases, attrs)

class RESTUpload(object):
    __metaclass__ = MetaInitUpload
