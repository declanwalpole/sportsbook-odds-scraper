from urllib.parse import urlparse
import re
import requests
from decimal import Decimal
from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class BetRivers(Sportsbook):

    def get_name(self):
        return "Rush Street Interactive"

    def match_url_pattern(self, url):
        return ".betrivers." in url or "playsugarhouse." in url

    def extract_parameters_from_url(self, url):

        return {'event_id': self._extract_event_id_from_url(url),
                'jurisdiction': self._extract_jurisdiction_from_url(url)}

    def _extract_event_id_from_url(self, url):

        # Extract the digits between the last slash and the question mark (if any)

        last_slash_index = url.rfind('/')
        question_mark_index = url.find('?', last_slash_index)

        if question_mark_index != -1:
            event_id_str = url[last_slash_index + 1:question_mark_index]
        else:
            event_id_str = url[last_slash_index + 1:]

        return event_id_str

    def _extract_jurisdiction_from_url(self, url):
        parsed_url = urlparse(url)
        # Extracting the state from the subdomain (first two characters)
        state = parsed_url.hostname.split('.')[0].upper()
        # Determining the country based on the top-level domain
        country = "US" if parsed_url.hostname.endswith(
            '.com') else "CA" if parsed_url.hostname.endswith('.ca') else None
        # Concatenating the country and state codes
        if country and state:
            return country + state
        else:
            return None

    def request_event(self, event_id, jurisdiction):
        markets_url = f'https://eu-offering-api.kambicdn.com/offering/v2018/rsi{jurisdiction.lower()}/betoffer/event/{event_id}.json?lang=en_US&includeParticipants=true'
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(markets_url, headers=headers)

        # Check if the response is in JSON format
        if response.headers['Content-Type'] == 'application/json':
            json_data = response.json()
            return json_data
        else:
            raise ValueError(
                "Expected application/json content type, but received " + response.headers['Content-Type'])

    def parse_event_name(self, json_response):
        return json_response['events'][0]["name"]

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Iterating through markets
        for market in json_response['betOffers']:
            market_name = market['criterion']['label']
            market_id = market['id']
            market_group = market['betOfferType']['name']
            market_list.append(
                Market(market_id, market_group, market_name))
            # Iterating through outcomes
            for outcome in market['outcomes']:
                if outcome['status'] == "OPEN":
                    outcome_name = outcome['label']
                    outcome_id = outcome['id']
                    odds = outcome['odds']/1000
                    line_raw = outcome.get('line', None)
                    if line_raw:
                        line = line_raw/1000
                    else:
                        line = None
                    selection_list.append(
                        Selection(market_id, outcome_id, outcome_name, odds, line))

        return self.convert_odds_to_df(market_list, selection_list)
