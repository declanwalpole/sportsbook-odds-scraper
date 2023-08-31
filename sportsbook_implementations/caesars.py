import re
import requests
from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class Caesars(Sportsbook):

    def get_name(self):
        return "Caesars"

    def match_url_pattern(self, url):
        pattern = r"https://sportsbook\.caesars\.com/us/(\w+)/bet"
        return re.match(pattern, url)

    def extract_parameters_from_url(self, url):
        return {'event_id': self._extract_event_id_from_url(url),
                'jurisdiction': self._extract_jurisdiction_from_url(url)}

    def _extract_event_id_from_url(self, url):
        pattern = r"/([a-f0-9-]+)/[^/]*$"
        match = re.search(pattern, url)

        if match:
            return match.group(1)
        else:
            return None

    def _extract_jurisdiction_from_url(self, url):
        return self.match_url_pattern(url).group(1)

    def concatenate_api_url(self, event_id, jurisdiction):
        return f'https://api.americanwagering.com/regions/us/locations/{jurisdiction}/brands/czr/sb/v3/events/{event_id}'

    def _remove_bars(self, string):
        return string.replace("|", "")

    def parse_event_name(self, json_response, event_id=None):
        return self._remove_bars(json_response['name'])

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Iterating through markets
        for market in json_response['markets']:
            if market["display"] and market['active']:
                market_name = self._remove_bars(market['name'])
                market_id = market['id']
                market_group = None
                market_list.append(
                    Market(market_id, market_group, market_name))
                # Iterating through outcomes
                for outcome in market['selections']:
                    if outcome["display"] and outcome['active']:
                        outcome_name = self._remove_bars(outcome['name'])
                        outcome_id = outcome['id']
                        odds = outcome['price']['d']
                        line = market.get('line', None)
                        selection_list.append(
                            Selection(market_id, outcome_id, outcome_name, odds, line))

        return self.convert_odds_to_df(market_list, selection_list)
