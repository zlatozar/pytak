"""
With this scenario will be checked if application is functional.
Script will be run every hour.
"""

# type of runners
from pytak.runners import run
from pytak.runners import weak_run
from pytak.runners import test

from pytak.runners import basic_login
from pytak.runners import select
from pytak.predicates import created_before_delta

# REST calls specification
from project.apispec import GetInformationAboutYourself
from project.apispec import HardDelete
from project.apispec import CreateAPost
from project.apispec import AddAttachmentsToAPost

# complex searches as separate calls
from project.apispec.queries import GetOnlyMyPosts
from project.apispec.queries import SearchPostByTitleName

def main():
    """Scenario(10 steps) that verifies if application works:

    1. Login with 'test' user
    2. Get personal information
    3. Verify returned JSON schema
    4. Get user activity using personal information from previous call
    5. Delete all activities that are before 2 hours
    6. Create a post with unique name
    7. Modify it as attaching a picture
    8. Wait 2 minutes
    9. Search the post
    10. Try to delete post using returned id from previous call
    """

    basic_login('test', 'test')

    # Use '+' to add key=values
    who_am_i = GetInformationAboutYourself() + "fields=id,screenName,fullName"
    test(who_am_i)

    # 'assign' when hard code, 'bind' when take value from previous calls
    my_posts = GetOnlyMyPosts(assign={"count" : 100}, bind={"user_id" : "entry.0.data.id"})
    run(my_posts)

    my_old_posts = select("GetOnlyMyPosts").iff(created_before_delta("entry.*.data.createDate", hours_before=2)) \
                                           .then_key("entry.*.data.id")

    # cycle
    for id in my_old_posts:
        run(HardDelete({"post_id" : id}))

    # Use '<<' to form request body
    # NOTE: [XXXX] will be replaced with random string, [DDDDDD] random digits
    create_post = CreateAPost() << {
        "title" : "New company office - [XXXX]",
        "body"  : "First images from our new office - [DDDDDD]",
        "type"  : "TEXT",
        "tags"  : [{"name":"office"}, {"name":"company"}, {"name":"work place"}]
    }

    # 'upload' points file that should be attached
    attach_file = AddAttachmentsToAPost(upload="new_office.jpg", bind={"post_id" : "entry.0.data.id"})
    run([create_post, attach_file])

    print "Wait 2 min for newly created post to be search-able"

    import time
    time.sleep(120)

    search_post = SearchPostByTitleName(bind={"post_title" : "entry.0.data.title"})
    run(search_post)

    delete_created_post = HardDelete(bind={"post_id" : "feed.entry.id"})

    # Errors are acceptable
    weak_run(delete_created_post)
