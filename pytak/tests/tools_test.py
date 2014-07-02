# -*- coding: utf-8 -*-

"""
Test methods that work on parametrised 'apispec' classes
"""

import pytak.runners.tools as tools

from fakeapi import CreateTag
from fakeapi import DeleteTag


def test_needed_params():
    ct = CreateTag()
    assert ct.request_body == {'name': '${name}'}

def test_get_uri():
    dt = DeleteTag()
    assert dt.uri == '/api/muad/rest/tags/${name}'

def test_request_body_assign():
    ct = CreateTag(assign={'name':'pytest'})
    tools.form_request_body(ct)
    assert ct.request_body == {'name':'pytest'}

def test_request_body_bind_wrong():
    ct = CreateTag()
    tools.form_request_body(ct)
    assert ct.request_body == {'name': '${name}'}

def test_request_body_assign_and_bind():
    ct = CreateTag(assign={'name':'pytest'}, bind={'id':4224})
    tools.form_request_body(ct)
    assert ct.request_body == {'name':'pytest'}
