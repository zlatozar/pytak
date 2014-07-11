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
expected_data = {u'components.0.menu.0.title': u'menu_title1', u'title': u'main_title', u'components.1.menu.1.id': 400, u'components.0.menu.2.id': 200, u'components.1.menu.0.title': u'menu_title1', u'components.0.component_id': 100, u'components.1.component_id': 300, u'components.0.menu.1.title2': u'menu_title2'}

def test_converter():
    assert expected_data == convert_to_dotted(json.loads(data))
