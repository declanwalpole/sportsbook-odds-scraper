import re
import requests
import pandas as pd
import argparse

# Define classes


class Market():
    def __init__(self, event_id, market_id, market_group, market_name):
        self.id = ""
        self.event_id = event_id
        self.market_id = market_id
        self.market_group = market_group
        self.market_name = market_name

    def __str__(self):
        return self.market_name


class Selection():
    def __init__(self, market_id, selection_id, selection_name, odds, line):
        self.id = ""
        self.market_id = market_id
        self.selection_id = selection_id
        self.selection_name = selection_name
        self.odds = odds
        self.line = line

    def __str__(self):
        return self.selection_name

# Define helper functions to convert responses to custom objects


def translate_DK_to_market_dict(DK_dict, eventId, subcategoryName):

    z = {
        'event_id': eventId,
        'market_id': DK_dict['providerOfferId'],
        'market_group': subcategoryName,
        'market_name': DK_dict['label']
    }

    new_object = Market(**z)
    return new_object


def translate_DK_to_selection_dict(DK_dict, market_id):
    if "line" in DK_dict.keys():
        line = DK_dict['line']
    else:
        line = None

    z = {
        'market_id': market_id,
        'selection_id': DK_dict['providerOutcomeId'],
        'selection_name': DK_dict['label'],
        'odds': DK_dict['oddsDecimal'],
        'line': line,
    }

    new_object = Selection(**z)
    return new_object


def scrape_DK_event(eventid):

    market_list = []
    selection_list = []

    # hit api for markets

    eventId = eventid
    DK_markets_URL = 'https://sportsbook.draftkings.com//sites/US-SB/api/v3/event/'+eventId
    payload2 = {'format': 'json'}

    r2 = requests.get(DK_markets_URL, params=payload2)

    content2 = r2.json()

    G = content2['eventCategories']

    categories_of_interest = []

    for g in G:
        categories_of_interest = g['componentizedOffers']

        #categories_of_interest = categories_of_interest[0]

        for c in categories_of_interest:
            # print('\n'+c['subcategoryName']+'\n')
            offers = c['offers'][0]

            for o in offers:
                if not o['isSuspended'] and o['isOpen']:

                    market = translate_DK_to_market_dict(
                        o, eventId, c['subcategoryName'])
                    market_list.append(market)

                    # print(market)
                    outcomes = o['outcomes']

                    for a in outcomes:

                        if not a.get('hidden'):
                            selection = translate_DK_to_selection_dict(
                                a, market.market_id)
                            selection_list.append(selection)

                            # print('\t'+str(selection))

    # Convert market_list to a DataFrame
    market_data = [{'event_id': market.event_id,
                    'market_id': market.market_id,
                    'market_group': market.market_group,
                    'market_name': market.market_name}
                   for market in market_list]
    market_df = pd.DataFrame(market_data)

    # Convert selection_list to a DataFrame
    selection_data = [{'market_id': selection.market_id,
                       'selection_id': selection.selection_id,
                       'selection_name': selection.selection_name,
                       'odds': selection.odds,
                       'line': selection.line}
                      for selection in selection_list]
    selection_df = pd.DataFrame(selection_data)

    # Perform the join operation and remove duplicates
    merged_df = market_df.merge(
        selection_df, left_on='market_id', right_on='market_id').drop_duplicates()

    return merged_df


def write_to_csv(df, outfilename):

    try:
        df.to_csv(outfilename, index=False)
        print(
            f"DataFrame successfully written to '{outfilename}' as a CSV file.")
    except Exception as err:
        print(f"Error occurred while writing DataFrame to CSV: {err}")


def extract_event_id_from_url(url):
    """
    Extract the eventId from the given URL.

    Parameters:
        url (str): The URL from which to extract the eventId.

    Returns:
        int or None: The extracted eventId as an integer if found, otherwise None.
    """
    # Find the last occurrence of "/"
    last_slash_index = url.rfind('/')

    # Find the first "?" after the last slash
    question_mark_index = url.find('?', last_slash_index)

    # Extract the substring containing the digits between the last slash and the question mark (if any)
    if question_mark_index != -1:
        event_id_str = url[last_slash_index + 1:question_mark_index]
    else:
        event_id_str = url[last_slash_index + 1:]

    return event_id_str


def overarching_method(url, csvOutFileName):
    eventId = extract_event_id_from_url(url)
    print(f"Scraping for: {eventId}...")
    df = scrape_DK_event(eventId)
    write_to_csv(df, csvOutFileName)
    print("Here is a snippet of the first 5 records...")
    return (df.head(5))


def main():
    parser = argparse.ArgumentParser(
        description='Script that scrapes a DK URL and returns a csv of odds.')
    parser.add_argument('url', type=str, help='URL of Draftkings match')
    parser.add_argument('csvOutFileName', type=str,
                        help='File to write the CSV to')
    args = parser.parse_args()

    # Call your custom function with the parsed arguments
    result = overarching_method(args.url, args.csvOutFileName)
    print(f"Result: {result}")


if __name__ == '__main__':
    main()
