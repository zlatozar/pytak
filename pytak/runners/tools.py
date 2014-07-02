# -*- coding: utf-8 -*-

"""
    tools
    ~~~~~

    Functions that are used to prepare REST call
    Flat JSON is used to refer and change JSON values

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import re

def needed_params(api_object):
    """Return needed parameters that need to be assigned or bind.

    Return format is: {'uri': ['${tag_id}'], 'request_body': ['${name}']}
    """
    needed = {}
    pattern = "\$\{.*\}"

    def __collect(line, key):
        found = re.search(pattern, line)
        if found:
            needed.setdefault(key,[]).append(found.group(0))

    def __prefix(json):

        if isinstance(json, dict):
            for key, value in json.iteritems():
                __prefix(value)

        elif isinstance(json, list):
            for value in json:
                __prefix(value)

        else:
            if '$' in json:
                __collect(json, "request_body")

    # Check URI
    if '$' in api_object.uri:
        __collect(api_object.uri, "uri")

    # Check body payload
    __prefix(api_object.request_body)

    return needed


def __find_in_env(env, key):
    """Returns string representing value in environment"""
    for state in env:
        if key in state:
            return str(state.get(key))

    env.view()
    raise ValueError("Can't find value for key '%s' in environment" % key)

def form_uri(api_object, env=None):
    """Function with side effects - change 'uri' field"""

    # Remove optional parameters
    api_object.uri = api_object.uri.replace("[?query_parameters]", "")

    if '$' not in api_object.uri:
        return

    # Take from direct assign e.g. CreateTag(assign={'name':'pytak'}
    # NOTE: Space should be replaced with '\ ' in URL
    if api_object.assign:
        for assign_key, assign_value in api_object.assign.iteritems():
            for template in re.findall('\$\{' + re.escape(assign_key) + '\}', api_object.uri):
                api_object.uri = re.sub(re.escape(template), re.sub(' ', '\ ', str(assign_value)), api_object.uri)

    # Take from bind e.g. DeleteTag(bind={'name':'b.0.c'})
    if api_object.bind:
        for bind_key, bind_value in api_object.bind.iteritems():
            for template in re.findall('\$\{' + re.escape(bind_key) + '\}', api_object.uri):
                api_object.uri = re.sub(re.escape(template), re.sub(' ', '\ ', __find_in_env(env, bind_value)), api_object.uri)

    return api_object.uri

def form_request_body(api_object, env=None):
    """Function with side effects - change 'request_body' field"""

    # ___________________________________________________________
    #                                     Helper inner functions

    def __convert_to_dotted(data):
        """Converts JSON format to flat dictionary structure.

        To represent nested JSON structure we use dots e.g. { 'b.0.c': 2, 'b.1.d': 3 }
        """

        flat = {}

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

    def select(data, query):

        def __select(json, query):
            return json[query]

        return reduce(__select, query, data)

    query = []

    def __to_query_list(flat):
        """Converts flat JSON structure to list e.g. 'b.0.c' to ['b', 0, 'c']

        It is used to select key that contains parameter.
        For example ['b', 0, 'c'] will change ${to_be_changed}:

                    { "a": 1, "b": [ { "c": ${to_be_changed} }, { "d": 3 } ] }
        """
        if not flat:
            return query

        dot = flat.find('.')

        if dot > -1:
            part = flat[:dot]
            if part.isdigit():
                query.append(int(part))
            else:
                query.append(part)

            __to_query_list(flat[dot + 1:])

        else:
            query.append(flat)

        return query

    # ___________________________________________________________
    #                              Method logic starts from here

    flat_request_body = __convert_to_dotted(api_object.request_body)

    # Take from direct assign e.g. CreateTag(assign={'name':'zlatozar'})
    if api_object.assign:
        for assign_key, assign_value in api_object.assign.iteritems():
            for flat_key, flat_value in flat_request_body.iteritems():
                if flat_value == "${" + assign_key + "}":
                    # find query that will change template
                    query = __to_query_list(flat_key)
                    selected = select(api_object.request_body, query[:-1])
                    selected[query[-1]] = assign_value

    # Take from bind e.g. DeleteTag(bind={'name':'b.0.c'})
    if api_object.bind:
        for bind_key, bind_value in api_object.bind.iteritems():
            for flat_key, flat_value in flat_request_body.iteritems():
                if flat_value == "${" + bind_key + "}":
                    # find query that will change template
                    query = __to_query_list(flat_key)
                    selected = select(api_object.request_body, query[:-1])

                    # Start searching environment
                    selected[query[-1]] = __find_in_env(env, bind_value)

    # TODO: Check if there is left templates

    return api_object.request_body

# ___________________________________________________________
#                                               Memorization

from functools import wraps

# note that this decorator ignores **kwargs
def memoize(obj):
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer

def memoize_all(obj):
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)

        return cache[key]

    return memoizer
