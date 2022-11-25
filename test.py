import requests
import pickle

# Define classes


class Event():
    def __init__(self, event_name, league, event_id, team1, team2, starts_at, event_status):
        self.league = league
        self.event_id = event_id
        self.team1 = team1
        self.team2 = team2
        self.starts_at = starts_at
        self.event_name = event_name
        self.event_status = event_status

    def __str__(self):
        return self.event_name


class Market():
    def __init__(self, event_id, market_id, market_group, market_name):
        self.event_id = event_id
        self.market_id = market_id
        self.market_group = market_group
        self.market_name = market_name

    def __str__(self):
        return self.market_name


class Selection():
    def __init__(self, market_id, selection_id, selection_name, odds, line):
        self.market_id = market_id
        self.selection_id = selection_id
        self.selection_name = selection_name
        self.odds = odds
        self.line = line

    def __str__(self):
        return self.selection_name

# Define helper functions to convert responses to custom objects


def translate_DK_to_match_dict(DK_dict):
    z = dict((k, DK_dict[k]) for k in ('name', 'eventGroupName', 'eventId',
             'teamName1', 'teamName2', 'startDate'))
    z['event_status'] = DK_dict['eventStatus']['state']

    z['league'] = z.pop('eventGroupName')
    z['event_id'] = z.pop('eventId')
    z['team1'] = z.pop('teamName1')
    z['team2'] = z.pop('teamName2')
    z['starts_at'] = z.pop('startDate')
    z['event_name'] = z.pop('name')

    new_object = Event(**z)
    return new_object


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


# hit api for NBA match list
competitionId = '88808'  # NFL
# 87637 = NCAAF
# 92483 = NCAAB
# 42133 = NHL
# 88808 = NFL
# '42648'  # NBA
DK_comp_URL = 'https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/'+competitionId
payload = {'format': 'json'}

r = requests.get(DK_comp_URL, params=payload)

content = r.json()

events = content['eventGroup']['events']

match_list = []
market_list = []
selection_list = []

for e in events:
    match = translate_DK_to_match_dict(e)
    match_list.append(match)

    # hit api for markets

    eventId = match.event_id
    DK_markets_URL = 'https://sportsbook.draftkings.com//sites/US-SB/api/v3/event/'+eventId
    payload2 = {'format': 'json'}

    r2 = requests.get(DK_markets_URL, params=payload2)

    content2 = r2.json()

    G = content2['eventCategories']

    categories_of_interest = []
    cats = ['Popular']

    for g in G:
        if g['name'] in cats:
            categories_of_interest.append(g['componentizedOffers'])

    categories_of_interest = categories_of_interest[0]

    for c in categories_of_interest:
        print('\n'+c['subcategoryName']+'\n')
        offers = c['offers'][0]

        for o in offers:
            if not o['isSuspended'] and o['isOpen']:

                market = translate_DK_to_market_dict(
                    o, eventId, c['subcategoryName'])
                market_list.append(market)

                print(market)
                outcomes = o['outcomes']

                for a in outcomes:

                    selection = translate_DK_to_selection_dict(
                        a, market.market_id)
                    selection_list.append(selection)

                    print('\t'+str(selection))

# Store data to files as pickled

with open('events.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(match_list, f, pickle.HIGHEST_PROTOCOL)

with open('markets.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(market_list, f, pickle.HIGHEST_PROTOCOL)


with open('selections.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(selection_list, f, pickle.HIGHEST_PROTOCOL)
