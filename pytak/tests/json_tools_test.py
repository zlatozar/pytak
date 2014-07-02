# -*- coding: utf-8 -*-

from pytak import json_tools

from pytak.call import randomize_text

json_data = {
    "title" : "New Employee - [XXXX]",
    "body"  : "Please welcome our new employee. [XXXX]",
    "type"  : "TEXT",
    "tags"  : [ {"name" :
                 {"inner_name" :
                  [ { "inner_key1" : "inner_value1"},
                    { "inner_key2" : "inner_value2"}]} },
                {"name" : "tag2" },
                {"name" : "tag3" } ],
    "tag2" : { "name2" : { "inner_key3" : "inner_value3" }}
}

key_json_data = {
    "title" : "New Employee - [XXXX]",
    "body"  : "Please welcome our new employee. [XXXX]",
    "type"  : "TEXT",
    "tags"  : [ {"name" :
                 {"inner_name" :
                  [ { "inner_key1" : "inner_value1"},
                    { "inner_key2" : "inner_value2"}]} },
                {"name" : "tag-z" },
                {"name" : "tag-z" } ],
    "tag2" : { "name2" : { "inner_key3" : "inner_value3" }}
}

value_json_data = {
    "title" : "New Employee - [----]",
    "body"  : "Please welcome our new employee. [----]",
    "type"  : "TEXT",
    "tags"  : [ {"name" :
                 {"inner_name" :
                  [ { "inner_key1" : "inner_value1"},
                    { "inner_key2" : "inner_value2"}]} },
                {"name" : "tag-z" },
                {"name" : "tag-z" } ],
    "tag2" : { "name2" : { "inner_key3" : "inner_value3" }}
}

assign_json_data = {
    "name" : "tag - [XXXX]"
}


nested_dict = {
    "title" : "New Employee [XXXXX]",
    "body"  : "Please welcome our new employee. Kajmu tag - [DDDD]",
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

value_nested_dict = {
    "title" : "New Employee [----]",
    "body"  : "Please welcome our new employee. Kajmu tag - [DDDD]",
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


# ___________________________________________________________
#                                                      Tests

def test_extract_paths_dict():
    assert [['body'], ['permissions', 'permissionFlags', 'edit'], ['permissions', 'permissionFlags', 'comment'], ['permissions', 'permissionFlags', 'share'], ['permissions', 'permissionFlags', 'authorize'], ['permissions', 'permissionFlags', 'view'], ['permissions', 'permissionFlags'], ['permissions', 'principal', 'resource'], ['permissions', 'principal', 'id'], ['permissions', 'principal'], ['permissions'], ['type'], ['tags', 0, 'name'], ['tags', 0], ['tags', 1, 'name'], ['tags', 1], ['tags', 2, 'name'], ['tags', 2], ['tags'], ['title']] == json_tools.extract_paths(nested_dict)

def test_update():
    assert key_json_data == json_tools.update_leaf(json_data, "name", "tag-z")

def test_update_if_value():
    assert value_json_data == json_tools.update_leaf_if_value(json_data, r'\[X{4}X*\]', "[----]")

def test_update_if_simple_value():
    assert { "name" : "tag - [----]" } == json_tools.update_leaf_if_value(assign_json_data, r'\[X{4}X*\]', "[----]")

def test_update_if_simple_value_func():
    assert { "name" : "tag - [XXXX]" } != json_tools.update_leaf_if_value_func(assign_json_data, randomize_text)

def test_nested_dict():
    assert value_nested_dict == json_tools.update_leaf_if_value(nested_dict, r'\[X{4}X*\]', "[----]")
