from pytak.call import REST

class CreateTag(REST):

    def fill_call_data(self):
        self.call_type = "POST"
        self.uri = "/api/muad/rest/tags"

        self.request_body = {
            "name" : "${name}"
        }

        self.response_code = 201
