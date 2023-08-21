from draftkings import DraftKings
from betmgm import BetMGM
from betrivers import BetRivers
from bovada import Bovada
from caesars import Caesars
from pointsbet import PointsBet
from sportsbet import Sportsbet
from superbook import Superbook
from tab import TAB


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [DraftKings(), BetMGM(), BetRivers(),
                       Bovada(), Caesars(), PointsBet(), Superbook(), TAB(), Sportsbet()]
        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
