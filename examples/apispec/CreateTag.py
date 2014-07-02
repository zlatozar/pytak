from pytak.call import REST

class CreateTag(REST):
    """Creates tag in my web application"""

    def fill_call_data(self):
        self.call_type = "POST"
        self.uri = "/api/rest/tags"

        self.request_body = {
            "name" : "${name}"
        }

        self.response_code = 201
