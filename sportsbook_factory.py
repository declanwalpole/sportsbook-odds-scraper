from draftkings import DraftKings
from betmgm import BetMGM


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [DraftKings(), BetMGM()]
        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
