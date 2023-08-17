import requests

from odds_dataclasses import Market, Selection


def match_url_pattern(url):
    return "sportsbet.com.au/betting" in url


def extract_event_id_from_url(url):
    # Extract the digits between the last slash and the question mark (if any)
    question_mark_index = url.find('?')

    if question_mark_index != -1:
        event_id_str = url[question_mark_index-7:question_mark_index]
    else:
        event_id_str = url[-7:]

    return event_id_str


def request_event(event_id):
    markets_url = f'https://www.sportsbet.com.au/apigw/sportsbook-sports/Sportsbook/Sports/Events/{event_id}/SportCard?displayWinnersPriceMkt=true&includeLiveMarketGroupings=true&includeCollection=true'

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
            "Expected application/json content type, but received " + response.headers['Content-Type'] + ". This may be due to Sportsbet (australia) geo-blocking outside of Australia. Use VPN to resolve this error.")


def get_event_name(json_response):
    return json_response["displayName"]


def request_market_grouping(event_id, market_group_id):
    markets_url = f"https://www.sportsbet.com.au/apigw/sportsbook-sports/Sportsbook/Sports/Events/{event_id}/MarketGroupings/{market_group_id}/Markets"

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(markets_url, headers=headers)

    if response.headers['Content-Type'].startswith('application/json'):
        json_data = response.json()
        return json_data
    else:
        raise ValueError(
            "Expected application/json content type, but received " + response.headers['Content-Type'] + ". This may be due to Sportsbet (australia) geo-blocking outside of Australia. Use VPN to resolve this error.")


def get_odds(json_content):

    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    event_id = json_content["id"]

    for market_grouping in json_content["marketGrouping"]:
        market_group_id = market_grouping['id']
        market_group = market_grouping['name']

        market_grouping_json = request_market_grouping(
            event_id, market_group_id)

        for market in market_grouping_json:
            market_name = market['name']
            market_id = market['id']
            market_list.append(
                Market(market_id, market_group, market_name))
            for outcome in market['selections']:
                selection_id = outcome['id']
                selection_name = outcome['name']
                odds = outcome['price']['winPrice']
                line = outcome.get('displayHandicap', None)
                if line:
                    line = float(line)

                selection_list.append(
                    Selection(market_id, selection_id, selection_name, odds, line))

    return (market_list, selection_list)
