from draftkings import DraftKings
from betmgm import BetMGM
from betrivers import BetRivers
from bovada import Bovada
from caesars import Caesars
from pointsbet import PointsBet
from superbook import Superbook


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [DraftKings(), BetMGM(), BetRivers(),
                       Bovada(), Caesars(), PointsBet(), Superbook()]
        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
