# -*- coding: utf-8 -*-

from jsonschema import validate

json = {
    "title": "Example Schema",
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

example_data = {
    "first_name" : "Pytak",
    "last_name" : "Pytakov",
    "age" : 1
}

def test_jsonschema():
    validate(example_data, json)
