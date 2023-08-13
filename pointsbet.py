import re
import requests
from decimal import Decimal
from urllib.parse import urlparse

from odds_dataclasses import Market, Selection


def match_url_pattern(url):
    return ".pointsbet." in url and "/sports/" in url


def parse_location(url):
    parsed_url = urlparse(url)
    # Extracting the state from the subdomain (first two characters)
    state = parsed_url.hostname.split('.')[0].upper()
    return state


def extract_event_id_from_url(url):

    # Extract the digits between the last slash and the question mark (if any)

    last_slash_index = url.rfind('/')
    question_mark_index = url.find('?', last_slash_index)

    if question_mark_index != -1:
        event_id_str = url[last_slash_index + 1:question_mark_index]
    else:
        event_id_str = url[last_slash_index + 1:]

    return event_id_str


def request_event(event_id, sportsbook):
    jurisdiction = sportsbook[-2:].lower()
    markets_url = f'https://api.{jurisdiction}.pointsbet.com/api/mes/v3/events/{event_id}'
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
            "Expected application/json content type, but received " + response.headers['Content-Type'])


def get_event_name(json_response):
    return json_response["name"]


def get_odds(json_content):

    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    # Iterating through markets
    for market in json_content['fixedOddsMarkets']:
        if market['isOpenForBetting']:
            market_name = market['eventName']
            market_id = market['key']
            market_group = market['groupName']
            market_list.append(
                Market(market_id, market_group, market_name))
            # Iterating through outcomes
            for outcome in market['outcomes']:
                if not outcome['isHidden'] and outcome['isOpenForBetting']:
                    outcome_name = outcome['name']
                    outcome_id = outcome['fixedMarketId']
                    odds = outcome['price']
                    line = outcome.get('points', None)
                    selection_list.append(
                        Selection(market_id, outcome_id, outcome_name, odds, line))

    return (market_list, selection_list)
