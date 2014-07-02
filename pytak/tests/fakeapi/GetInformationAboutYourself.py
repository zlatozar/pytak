from pytak.call import REST

class GetInformationAboutYourself(REST):

    def fill_call_data(self):
        self.uri = "/api/muad/rest/users/@me[?query_parameters]"
