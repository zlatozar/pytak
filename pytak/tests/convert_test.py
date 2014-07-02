# -*- coding: utf-8 -*-

from __future__ import print_function

import json

from pytak.please import convert_to_dotted

data = """
{
    "title": "main_title",
    "components": [
        {
            "component_id": 100,
            "menu": [
                {
                    "title": "menu_title1"
                },
                {
                    "title2": "menu_title2"
                },
                {
                    "id": 200
                }
            ]
        },
        {
            "component_id": 300,
            "menu": [
                {
                    "title": "menu_title1"
                },
                {
                    "id": 400
                }
            ]
        }
    ]
}
"""

def test_converter():
    print(convert_to_dotted(json.loads(data)))
