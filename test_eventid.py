import requests
import pickle
import json
import csv
import pandas as pd

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

    # Perform the join operation
    merged_df = market_df.merge(
        selection_df, left_on='market_id', right_on='market_id')

    return merged_df


z = scrape_DK_event('28993126')
print(z)
