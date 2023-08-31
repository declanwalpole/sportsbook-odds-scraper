from urllib.parse import urlparse
import re
import requests
from decimal import Decimal
from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class Bovada(Sportsbook):

    def get_name(self):
        return "Bovada"

    def match_url_pattern(self, url):
        return "bovada.lv/sports" in url

    def extract_parameters_from_url(self, url):

        return {'event_id': self._extract_event_id_from_url(url)}

    def _extract_event_id_from_url(self, url):

        pattern = re.compile(r'/sports/([^?]*)')

        match = pattern.search(url)

        if match:
            return match.group(1)
        else:
            return None

    def concatenate_api_url(self, event_id, jurisdiction=None):
        return f'https://www.bovada.lv/services/sports/event/coupon/events/A/description/{event_id}?lang=en'

    def parse_event_name(self, json_response, Event_id=None):
        return json_response[0]['events'][0]["description"]

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Iterating through display groups
        for display_group in json_response[0]['events'][0]['displayGroups']:
            market_group = display_group["description"]
            # Iterating through markets
            for market in display_group['markets']:
                if market["status"] == "O":
                    market_name = market['description']
                    market_id = market['id']
                    market_list.append(
                        Market(market_id, market_group, market_name))
                    # Iterating through outcomes
                    for outcome in market['outcomes']:
                        if outcome['status'] == "O":
                            outcome_name = outcome['description']
                            outcome_id = outcome['id']
                            odds = outcome['price']['decimal']
                            line = outcome['price'].get('handicap', None)
                            selection_list.append(
                                Selection(market_id, outcome_id, outcome_name, odds, line))

        return self.convert_odds_to_df(market_list, selection_list)
