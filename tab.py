from urllib.parse import urlparse
import re
import requests
from decimal import Decimal
from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class TAB(Sportsbook):

    def get_name(self):
        return "TAB"

    def match_url_pattern(self, url):
        return "tab.com.au/sports/betting" in url

    def extract_parameters_from_url(self, url):

        return {'event_id': self._extract_event_id_from_url(url)}

    def _extract_event_id_from_url(self, url):

        pattern = re.compile(r'/betting/([^?]*)')

        match = pattern.search(url)

        if match:
            return match.group(1)
        else:
            return None

    def request_event(self, event_id, jurisdiction=None):
        state = "NSW"  # NSW, VIC, ACT, QLD, SA, NT or TAS
        markets_url = f'https://api.beta.tab.com.au/v1/tab-info-service/sports/{event_id}?jurisdiction={state}'

        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(markets_url, headers=headers)

        # Check if the response is in JSON format
        if response.headers['Content-Type'].startswith('application/json'):
            json_data = response.json()
            return json_data
        else:
            raise ValueError(
                "Expected application/json content type, but received " + response.headers['Content-Type'] + ". This may be due to TAB geo-blocking outside of Australia. Use VPN to resolve this error.")

    def parse_event_name(self, json_response, event_id=None):
        return json_response["name"]

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Iterating through markets
        for market in json_response['markets']:
            if market['bettingStatus'] == "Open":
                market_name = market['betOption']
                market_id = market['marketUniqueId']
                market_group = None
                market_list.append(
                    Market(market_id, market_group, market_name))
                # Iterating through outcomes
                for outcome in market['propositions']:
                    if outcome['isOpen']:
                        outcome_name = outcome['name']
                        outcome_id = outcome['id']
                        odds = outcome['returnWin']
                        line = outcome.get('line', None)
                        selection_list.append(
                            Selection(market_id, outcome_id, outcome_name, odds, line))

        return self.convert_odds_to_df(market_list, selection_list)
