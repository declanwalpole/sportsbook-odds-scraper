import requests
import pandas as pd

from markets_and_selection_classes import translate_DK_to_market_dict, translate_DK_to_selection_dict, convert_market_list_to_df, convert_selection_list_to_df


def request_draftkings_event(event_id):
    DK_markets_url = f'https://sportsbook.draftkings.com/sites/US-SB/api/v3/event/{event_id}'
    params = {'format': 'json'}

    try:
        response = requests.get(DK_markets_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        content = response.json()
        return content
    except requests.exceptions.RequestException as e:
        print(
            f"Error occurred while fetching DraftKings event {event_id}: {e}")
        return None


def parse_draftkings_json(json_content):
    # Extract event information
    event_info = json_content['event']
    event_id = event_info["eventId"]
    event_name = event_info["name"]

    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    # Extract event categories
    event_categories = json_content['eventCategories']

    # Process each category and its offers
    for category in event_categories:
        market_groupings = category['componentizedOffers']

        for market_grouping in market_groupings:

            market_grouping_name = market_grouping['subcategoryName']
            offers = market_grouping['offers'][0]

            for offer in offers:
                if not offer['isSuspended'] and offer['isOpen']:
                    # Translate offer to market object
                    market = translate_DK_to_market_dict(
                        offer, event_id, market_grouping_name)
                    market_list.append(market)

                    # Extract outcomes and translate to selection objects
                    outcomes = offer['outcomes']

                    for outcome in outcomes:
                        if not outcome.get('hidden'):
                            selection = translate_DK_to_selection_dict(
                                outcome, market.market_id)
                            selection_list.append(selection)

    return (event_id, event_name, market_list, selection_list)


def convert_draftkings_info_to_df(market_list, selection_list):
    if not market_list or not selection_list:
        # Return an empty DataFrame if any of the input lists are empty.
        return pd.DataFrame()

    market_df = convert_market_list_to_df(market_list)
    selection_df = convert_selection_list_to_df(selection_list)
    merged_df = market_df.merge(
        selection_df, on='market_id', how='inner').drop_duplicates()
    return merged_df
