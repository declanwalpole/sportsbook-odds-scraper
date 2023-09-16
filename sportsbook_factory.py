from sportsbook_implementations.draftkings import DraftKings
from sportsbook_implementations.betmgm import BetMGM
from sportsbook_implementations.betrivers import BetRivers
from sportsbook_implementations.bovada import Bovada
from sportsbook_implementations.caesars import Caesars
from sportsbook_implementations.ladbrokes import Ladbrokes
from sportsbook_implementations.pointsbet import PointsBet
from sportsbook_implementations.sportsbet import Sportsbet
from sportsbook_implementations.superbook import Superbook
from sportsbook_implementations.tab import TAB


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

        raise ValueError(
            """Invalid sportsbook URL. Sportsbook may not be supported. If sportsbook is supported, check the URL itself and make sure it is for the event, not the league/sport page.""")
