class Sportsbook:
    def get_name(self):
        raise NotImplementedError

    def match_url_pattern(self, url):
        raise NotImplementedError

    def extract_parameters_from_url(self, url):
        raise NotImplementedError

    def request_event(self, params):
        raise NotImplementedError

    def parse_event_name(self, json_response):
        raise NotImplementedError

    def parse_odds(self, json_response, params):
        raise NotImplementedError
