from pytak.call import REST

class CreateAPost(REST):

    def fill_call_data(self):
        self.uri = "/api/muad/rest/posts[?query_parameters]"
        self.call_type = "POST"
        self.response_code = 201
