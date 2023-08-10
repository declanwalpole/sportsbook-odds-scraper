import requests
from odds_dataclasses import Market, Selection


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
    DK_markets_url = f'https://sportsbook.draftkings.com/sites/US-SB/api/v3/event/{event_id}'
    params = {'format': 'json'}

    try:
        response = requests.get(DK_markets_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        content = response.json()
        return content
    except requests.exceptions.RequestException as error:
        print(
            f"Error occurred while fetching DraftKings event {event_id}: {error}")
        return None


def get_event_name(json_response):
    return json_response['event']["name"]


def get_odds(json_content):

    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    # Process each category and its offers
    for category in json_content['eventCategories']:
        for market_grouping in category['componentizedOffers']:

            market_grouping_name = market_grouping['subcategoryName']
            markets = market_grouping['offers'][0]

            for market in markets:
                if not market['isSuspended'] and market['isOpen']:
                    # Translate offer to market object
                    market_output = translate_DK_to_market_dict(
                        market, market_grouping_name)
                    market_list.append(market_output)

                    # Extract outcomes and translate to selection objects
                    outcomes = market['outcomes']

                    for outcome in outcomes:
                        if not outcome.get('hidden'):
                            selection = translate_DK_to_selection_dict(
                                outcome, market_output.market_id)
                            selection_list.append(selection)

    return (market_list, selection_list)


def translate_DK_to_market_dict(DK_dict, subcategoryName):
    dict_for_translation = {
        'market_id': DK_dict['providerOfferId'],
        'market_group': subcategoryName,
        'market_name': DK_dict['label']
    }
    return Market(**dict_for_translation)


def translate_DK_to_selection_dict(DK_dict, market_id):
    if "line" in DK_dict:
        line = DK_dict['line']
    else:
        line = None

    dict_for_translation = {
        'market_id': market_id,
        'selection_id': DK_dict['providerOutcomeId'],
        'selection_name': DK_dict['label'],
        'odds': DK_dict['oddsDecimal'],
        'line': line,
    }
    return Selection(**dict_for_translation)
