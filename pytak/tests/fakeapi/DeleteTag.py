from pytak.call import REST

class DeleteTag(REST):

    def fill_call_data(self):
        self.call_type = "DELETE"
        self.uri = "/api/muad/rest/tags/${name}"
        self.response_code = 204
