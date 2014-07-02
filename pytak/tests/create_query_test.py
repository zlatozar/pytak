from __future__ import print_function

import json

def create_query(data, query):
    """Prototype my complicated function"""
    def select(json, query):
        return json[query]

    return reduce(select, query, data)

def test_create_query():
    new_value = 'new value'

    data = json.loads(""" { "a": 1, "b": [ { "c": 2 }, { "d": 3 } ], "xy": [ { "x": 4 }, { "y": [{ "y1": 5}, { "y2": [{"y22": 6}] }] } ] } """)
    query = ['b', 0, 'c']

    selected = create_query(data, query[:-1])
    selected[query[-1:][0]] = new_value
    assert data['b'][0]['c'] == new_value
