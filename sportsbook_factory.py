from draftkings import DraftKings
from betmgm import BetMGM
from betrivers import BetRivers
from bovada import Bovada
from caesars import Caesars
from ladbrokes import Ladbrokes
from pointsbet import PointsBet
from sportsbet import Sportsbet
from superbook import Superbook
from tab import TAB


class SportsbookFactory:
    @staticmethod
    def create(url):
        sportsbooks = [BetMGM(), BetRivers(), Bovada(),
                       Caesars(), DraftKings(), Ladbrokes(),
                       PointsBet(), Sportsbet(), Superbook(),
                       TAB()]

        for sportsbook in sportsbooks:
            if sportsbook.match_url_pattern(url):
                return sportsbook

        raise ValueError("Invalid sportsbook URL")
