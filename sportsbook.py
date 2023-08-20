class Sportsbook:
    def get_name(self):
        raise NotImplementedError

    def match_url_pattern(self, url):
        raise NotImplementedError

    def get_jurisdiction(self, url):
        raise NotImplementedError

    def get_event_id(self, url):
        raise NotImplementedError

    def request_event(self, event_id, jurisdiction):
        raise NotImplementedError

    def get_event_name(self, json_response):
        raise NotImplementedError

    def get_odds(self, json_response):
        raise NotImplementedError
