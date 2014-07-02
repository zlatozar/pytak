"""
Creates a tag with random name then deletes it
"""

from pytak.runners import basic_login
from pytak.runners import run

from project.apispec import CreateTag
from project.apispec import DeleteTag

def main():

    basic_login('test', 'test')

    scenario = [
        CreateTag(assign={"name" : "pytak-[XXXX]"}),
        DeleteTag(bind={"name" : "entry.0.data.name"})
    ]

    run(scenario)
