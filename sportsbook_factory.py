from draftkings import DraftKings


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [DraftKings()]
        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
