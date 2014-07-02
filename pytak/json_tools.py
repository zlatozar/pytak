# -*- coding: utf-8 -*-

"""
    tools
    ~~~~~

    Contains functions that select and update JSON leafs

    :copyright: (c) 2014 by Zlatozar Zhelyazkov.
    :license: BSD, see LICENSE for more details.
"""

import re

def extract_paths(json):
    """Select all JSON keys using mutual recursion"""

    _path = []
    _query = []

    def __form_path(in_dict, in_list):
        if _path:
            _query.append(_path[:])
            del _path[:]

        if in_list:
            for el in in_list:
                _path.append(el)

        if in_dict:
            for el in in_dict:
                _path.append(el)

    def dict_update(json, in_list=None, in_dict=None):

        if isinstance(json, dict):
            for key, value in json.iteritems():
                _path.append(key)
                dict_update(value, in_dict=_path[:-1])

        if isinstance(json, list):
            list_update(json, in_list=_path[:-1])

        else:
            __form_path(in_dict, in_list)

        return _query

    def list_update(inner_list, in_list=None, in_dict=None):

        if isinstance(inner_list, list):
            for idx, value in enumerate(inner_list):
                _path.append(idx)
                list_update(value, in_list=_path[:-1])

        if isinstance(inner_list, dict):
            dict_update(inner_list, in_dict=_path[:-1])

        else:
            __form_path(in_dict, in_list)

        return _query

    return dict_update(json)

def update_leaf_if_value_func(json, change_func):
    """Apply 'change_func' to every leaf using the leaf as an argument"""

    all_leafs = [path for path in extract_paths(json)]
    for query in all_leafs:
        selected = __upto_key_for_change(json, query)
        if isinstance(selected[query[-1]], dict) or isinstance(selected[query[-1]], list):
            continue

        selected[query[-1]] = change_func(selected[query[-1]])

    return json

def update_leaf_if_value(json, value_pattern, new_value):
    """Replace 'value_pattern' in a JSON leaf with new_value"""

    all_leafs = [path for path in extract_paths(json)]
    for query in all_leafs:
        selected = __upto_key_for_change(json, query)
        if isinstance(selected[query[-1]], dict) or isinstance(selected[query[-1]], list):
            continue

        selected[query[-1]] = re.sub(value_pattern, new_value, selected[query[-1]])

    return json

def update_leaf(json, key, new_value):
    """Update *all* JSON leafs that match 'key' with a given 'value'

    Algorithm explanation:

        1. Select path to JSON leaf referred by the given key
        2. Fold the JSON structure up to this key (not included)
        3. Update the leaf of folded JSON using given key
    """

    matched = [path for path in extract_paths(json) if path[-1] == key]
    for query in matched:
        selected = __upto_key_for_change(json, query)
        # skip keys that refer dictionary or list
        if isinstance(selected[query[-1]], dict) or isinstance(selected[query[-1]], list):
            continue

        # update only leafs
        selected[query[-1]] = new_value

    return json

# General one
def update(json, key, new_value):
    """Update *all* JSON keys that match 'key' with a given 'value'

    Algorithm explanation:

        1. Select path to JSON key referred by the given key
        2. Fold the JSON structure up to this key (not included)
        3. Update the leaf of folded JSON using given key
    """

    matched = [path for path in extract_paths(json) if path[-1] == key]
    for query in matched:
        selected = __upto_key_for_change(json, query)
        selected[query[-1]] = new_value

    return json

# ___________________________________________________________
#                                           Helper functions

def __upto_key_for_change(data, query):
    def __select(data, query):
        return data[query]

    return reduce(__select, query[:-1], data)
