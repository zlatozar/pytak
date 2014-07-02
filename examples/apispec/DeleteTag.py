from pytak.call import REST

class DeleteTag(REST):
    """Deletes a given tag in my web application"""

    def fill_call_data(self):
        self.call_type = "DELETE"
        self.uri = "/api/rest/tags/${name}"
        self.response_code = 204
