# -*- coding: utf-8 -*-

from __future__ import print_function

import pytak.call as call
import pytak.runners.tools as tools

from fakeapi import CreateTag
from fakeapi import GetInformationAboutYourself
from fakeapi import CreateAPost

new_request_body = {
    "title" : "New Employee [XXXXX]",
    "body"  : "Please welcome our new employee. Pytak tag - [DDDD]",
    "type"  : "TEXT",
    "permissions" : {
        "principal" : {
            "id"       : "12345",
            "resource" : "http://example.com/schema/1.0/user"
        },
        "permissionFlags" : {
            "view"      : "true",
            "edit"      : "false",
            "comment"   : "true",
            "share"     : "true",
            "authorize" :"false"
        }
    },

    "tags" : [ {"name" : "tag2" }, { "name" : "tag3" }, { "name" : "tag4" } ]
}

def test_randomize_text():
    txt = "JSON value with [XXXX] and [DDDD]"
    assert txt != call.randomize_text(txt)

def test_random_int_leght():
    dig = call.__get_random_int(4)
    assert len(str(dig)) == 4

def test_random_alphanum_leght():
    alphnum = call.__get_random_alphanumeric(4)
    assert len(alphnum) == 4

def test_api_object_request_body_creation():
    ct = CreateTag()
    ct2 = CreateTag(assign={'name':'first'})
    assert ct.request_body == ct2.request_body

def test_api_object_request_body_manipulation_with_empty():
    ct = CreateTag()
    ct2 = CreateTag(assign={'name':'second'})

    tools.form_request_body(ct2)
    assert ct.request_body != ct2.request_body

def test_api_object_request_body_manipulation_with_change():
    ct = CreateTag(assign={'name':'one'})
    ct2 = CreateTag(assign={'name':'two'})

    tools.form_request_body(ct2)
    assert ct.request_body != ct2.request_body

def test_url_rewrite():
    your_information = GetInformationAboutYourself() + "fields=id,screenName,fullName"
    assert your_information.uri == "/api/muad/rest/users/@me?fields=id,screenName,fullName"

def test_request_body_rewrite():
    CreateAPost() << new_request_body

def test_assign_randomization():
    create_tag = CreateTag(assign={"name" : "pytak-[XXXX]"})
    assert create_tag.assign != {"name" : "pytak-[XXXX]"}

def test_request_body_randomization():
    create_post = CreateAPost() << new_request_body
    print(create_post.request_body)
