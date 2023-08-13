import re
import requests

from odds_dataclasses import Market, Selection


def match_url_pattern(url):
    pattern = r"https://sportsbook\.caesars\.com/us/(\w+)/bet"
    return re.match(pattern, url)


def get_state_abbrev(url):
    return match_url_pattern(url).group(1)


def extract_event_id_from_url(url):

    pattern = r"/([a-f0-9-]+)/[^/]*$"
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None


def request_event(event_id, sportsbook):
    state_abbrev = sportsbook[-2:].lower()
    api_endpoint = f'https://api.americanwagering.com/regions/us/locations/{state_abbrev}/brands/czr/sb/v3/events/{event_id}'

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(api_endpoint, headers=headers)

    # Check if the response is in JSON format
    if response.headers['Content-Type'].startswith('application/json'):
        json_data = response.json()
        return json_data
    else:
        raise ValueError(
            "Expected application/json content type, but received " + response.headers['Content-Type'] + ". This may be due to Ladbrokes (australia) geo-blocking outside of Australia. Use VPN to resolve this error.")


def remove_bars(string):
    return string.replace("|", "")


def get_event_name(json_response):
    return remove_bars(json_response['name'])


def get_odds(json_content):
    # Initialize lists to store markets and selections
    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    # Iterating through markets
    for market in json_content['markets']:
        if market["display"] and market['active']:
            market_name = market['displayName']
            market_id = market['id']
            market_group = None
            market_list.append(
                Market(market_id, market_group, market_name))
            # Iterating through outcomes
            for outcome in market['selections']:
                if outcome["display"] and outcome['active']:
                    outcome_name = remove_bars(outcome['name'])
                    outcome_id = outcome['id']
                    odds = outcome['price']['d']
                    line = market.get('line', None)
                    selection_list.append(
                        Selection(market_id, outcome_id, outcome_name, odds, line))

    return (market_list, selection_list)
