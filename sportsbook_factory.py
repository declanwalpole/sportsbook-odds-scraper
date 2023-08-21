from draftkings import DraftKings
from betmgm import BetMGM
from betrivers import BetRivers
from bovada import Bovada


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [DraftKings(), BetMGM(), BetRivers(), Bovada()]
        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
