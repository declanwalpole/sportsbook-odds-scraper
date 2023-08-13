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


def get_odds(json_content):

    return NotImplementedError
