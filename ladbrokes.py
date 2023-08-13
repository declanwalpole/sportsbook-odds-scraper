import re
import requests
from decimal import Decimal
from urllib.parse import urlparse

from odds_dataclasses import Market, Selection


def match_url_pattern(url):
    return "ladbrokes.com.au/sports/" in url


def extract_event_id_from_url(url):
    # Extract the digits between the last slash and the question mark (if any)

    last_slash_index = url.rfind('/')
    question_mark_index = url.find('?', last_slash_index)

    if question_mark_index != -1:
        event_id_str = url[last_slash_index + 1:question_mark_index]
    else:
        event_id_str = url[last_slash_index + 1:]

    return event_id_str


def request_event(event_id):
    markets_url = f'https://api.ladbrokes.com.au/v2/sport/event-card?id={event_id}'

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
            "Expected application/json content type, but received " + response.headers['Content-Type'] + ". This may be due to Ladbrokes (australia) geo-blocking outside of Australia. Use VPN to resolve this error.")


def get_event_name(json_response, event_id):
    return json_response["events"][event_id]['name']


class EntrantSummary:
    def __init__(self, **kwargs):
        self.odds = None
        self.line = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class MarketSummary:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class PriceSummary:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def join_everything_together(all_entrants, all_markets, all_prices):

    # Create a dictionary with selection_id as the key and odds as the value
    selection_id_to_odds = {
        price.selection_id: price.odds for price in all_prices}

    # Iterate through all_entrants and add the corresponding odds
    for entrant in all_entrants:
        entrant_odds = selection_id_to_odds.get(entrant.selection_id)
        if entrant_odds is not None:
            entrant.odds = entrant_odds  # Assumes that 'odds' is an attribute of EntrantSummary

    # Create a dictionary with market_id as the key and line as the value
    market_id_to_line = {
        market.market_id: market.line for market in all_markets}

    # Iterate through all_entrants and add the corresponding line
    for entrant in all_entrants:
        market_line = market_id_to_line.get(entrant.market_id)
        if market_line is not None:
            entrant.line = market_line  # Assumes that 'line' is an attribute of EntrantSummary

    return all_entrants


def get_odds(json_content):

    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    all_entrants = []
    all_markets = []
    all_prices = []

    for key, entrant in json_content['entrants'].items():
        if entrant['visible']:
            entrant_summary = EntrantSummary(selection_id=entrant['id'],
                                             name=entrant['name'],
                                             market_id=entrant['market_id'])
            all_entrants.append(entrant_summary)

    for key, market in json_content['markets'].items():
        if market['visible']:

            market_summary = MarketSummary(
                market_id=market['id'],
                name=market['name'],
                line=market.get('handicap', None))
            all_markets.append(market_summary)

    for key, price in json_content['prices'].items():
        price_summary = PriceSummary(
            selection_id=key.split(':', 1)[0],
            odds=price['odds']['numerator']/price['odds']['denominator']
        )
        all_prices.append(price_summary)

    # Iterating through markets
    for m in all_markets:
        market_list.append(
            Market(m.market_id, None, m.name))

    combo = join_everything_together(all_entrants, all_markets, all_prices)

    for combination in combo:
        selection_list.append(
            Selection(market_id=combination.market_id, selection_id=combination.selection_id, selection_name=combination.name, odds=combination.odds, line=combination.line))

    return market_list, selection_list
