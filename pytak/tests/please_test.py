# -*- coding: utf-8 -*-

import pytest

import pytak.please as please

json_one = {
    "title": "Example Schema JSON_ONE",
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "age": {
            "description": "Age in years",
            "type": "integer",
            "minimum": 0
        }
    },
    "required": ["first_name", "last_name"]
}


json_two = {
    "title": 42,
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "age": {
            "description": "Age in years",
            "type": "integer",
            "minimum": 0
        }
    },
    "required": ["first_name", "last_name"]
}

def test_json_compare_equal():
    please.compare_json(json_one, json_one)

def test_json_compare_diff():
    with pytest.raises(AssertionError):
        please.compare_json(json_one, json_two)
