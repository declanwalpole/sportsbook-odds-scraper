from draftkings import DraftKings
from betmgm import BetMGM
from betrivers import BetRivers


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [DraftKings(), BetMGM(), BetRivers()]
        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
