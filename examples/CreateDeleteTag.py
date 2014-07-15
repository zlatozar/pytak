"""
Creates a tag with random name then deletes it
"""

from pytak.runners import xauth_login
from pytak.runners import run

from project.apispec import CreateTag
from project.apispec import DeleteTag

def main():

    xauth_login()

    scenario = [
        # First argument is 'assign'
        CreateTag({"name" : "pytak-[XXXX]"}),
        DeleteTag(bind={"name" : "entry.0.data.name"})
    ]

    run(scenario)
