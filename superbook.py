from urllib.parse import urlparse
import re
import requests
from decimal import Decimal
from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class Superbook(Sportsbook):

    def get_name(self):
        return "Superbook"

    def match_url_pattern(self, url):
        return "superbook.com/sports/event" in url

    def extract_parameters_from_url(self, url):

        return {'event_id': self._extract_event_id_from_url(url),
                'jurisdiction': self._extract_jurisdiction_from_url(url)}

    def _extract_event_id_from_url(self, url):

        match = re.search(r'event/(\d+\.\d+)', url)

        if match:
            return match.group(1)
        else:
            return None

    def _extract_jurisdiction_from_url(self, url):
        parsed_url = urlparse(url)
        # Extracting the state from the subdomain (first two characters)
        state = parsed_url.hostname.split('.')[0].upper()
        return state

    def request_event(self, event_id, jurisdiction):
        markets_url = f'https://{jurisdiction}.superbook.com/cache/psevent/UK/1/false/{event_id}.json'
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(markets_url)

        # Check if the response is in JSON format
        if response.headers['Content-Type'].startswith('application/json'):
            json_data = response.json()
            return json_data
        else:
            raise ValueError(
                "Expected application/json content type, but received " + response.headers['Content-Type'] + ". This may be due to Ladbrokes (australia) geo-blocking outside of Australia. Use VPN to resolve this error.")

    def parse_event_name(self, json_response):
        return json_response["name"]

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Iterating through markets
        for market_groups in json_response['eventmarketgroups']:
            market_group = market_groups['name']
            for market in market_groups['markets']:
                if market["istradable"]:
                    market_name = market['name']
                    market_id = market['idfomarket']
                    market_list.append(
                        Market(market_id, market_group, market_name))
                    # Iterating through outcomes
                    for outcome in market['selections']:
                        outcome_name = outcome['name']
                        outcome_id = outcome['idfoselection']
                        odds = outcome['currentpriceup'] / \
                            outcome['currentpricedown']+1
                        line = outcome.get('currenthandicap', None)
                        selection_list.append(
                            Selection(market_id, outcome_id, outcome_name, odds, line))

        return self.convert_odds_to_df(market_list, selection_list)
