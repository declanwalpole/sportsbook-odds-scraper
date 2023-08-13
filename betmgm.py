import re
import requests
from decimal import Decimal
from urllib.parse import urlparse

from odds_dataclasses import Market, Selection

# https://sports.on.betmgm.ca/en/sports?trackerId=0&btag=&tdpeh=&pid=
# https://sports.co.betmgm.com/en/sports?wm=&btag=&tdpeh=&pid=


def match_url_pattern(url):
    match = re.search(
        pattern=r"sports\.([a-z]{2})\.betmgm\.(ca|com)", string=url)
    return match


def extract_state_code(url):

    return match_url_pattern(url).group(1).upper()


def extract_event_id_from_url(url):
    # Extract the digits between the last slash and the question mark (if any)
    question_mark_index = url.find('?')

    if question_mark_index != -1:
        event_id_str = url[question_mark_index-8:question_mark_index]
    else:
        event_id_str = url[-8:]

    return event_id_str


def request_event(event_id, sportsbook):
    state_code = sportsbook[-2:]
    markets_url = f'https://sports.{state_code}.betmgm.com/cds-api/bettingoffer/fixture-view?x-bwin-accessid=OTU4NDk3MzEtOTAyNS00MjQzLWIxNWEtNTI2MjdhNWM3Zjk3&offerMapping=All&lang=en-us&country=US&fixtureIds={event_id}'

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


def get_event_name(json_response):
    return json_response["fixture"]['name']['value']


def get_odds(json_content):
    # Initialize lists to store markets and selections
    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    # Iterating through markets
    for market in json_content['fixture']['games']:
        if market["visibility"] == "Visible":
            market_name = market['name']['value']
            market_id = market['id']
            market_group = market['grouping']['detailed'][0].get('name', None)
            market_list.append(
                Market(market_id, market_group, market_name))
            # Iterating through outcomes
            for outcome in market['results']:
                if outcome["visibility"] == "Visible":
                    outcome_name = outcome['name']['value']
                    outcome_id = outcome['id']
                    odds = outcome['odds']
                    line = outcome.get('attr', None)
                    if not line:
                        line = market.get('attr', None)
                    selection_list.append(
                        Selection(market_id, outcome_id, outcome_name, odds, line))

    return (market_list, selection_list)
