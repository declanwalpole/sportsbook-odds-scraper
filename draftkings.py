import requests
from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class DraftKings(Sportsbook):

    def get_name(self):
        return "DraftKings"

    def match_url_pattern(self, url):
        return "sportsbook.draftkings.com/event" in url

    def extract_parameters_from_url(self, url):

        return {'event_id': self._extract_event_id_from_url(url)}

    def _extract_event_id_from_url(self, url):
        # Extract the digits between the last slash and the question mark (if any)

        last_slash_index = url.rfind('/')
        question_mark_index = url.find('?', last_slash_index)

        if question_mark_index != -1:
            event_id_str = url[last_slash_index + 1:question_mark_index]
        else:
            event_id_str = url[last_slash_index + 1:]

        return event_id_str

    def request_event(self, event_id, jurisdiction=None):
        DK_markets_url = f"https://sportsbook.draftkings.com/sites/US-SB/api/v3/event/{event_id}"
        request_params = {'format': 'json'}

        try:
            response = requests.get(
                DK_markets_url, params=request_params, timeout=10)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            content = response.json()
            return content
        except requests.exceptions.RequestException as error:
            print(
                f"Error occurred while fetching DraftKings event {event_id}: {error}")
            return None

    def parse_event_name(self, json_response):
        return json_response['event']["name"]

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Process each category and its offers
        for category in json_response['eventCategories']:
            for market_grouping in category['componentizedOffers']:

                market_grouping_name = market_grouping['subcategoryName']
                markets = market_grouping['offers'][0]

                for market in markets:
                    if not market['isSuspended'] and market['isOpen']:
                        # Translate offer to market object
                        market_output = Market(
                            market_id=market['providerOfferId'], market_group=market_grouping_name, market_name=market['label'])
                        market_list.append(market_output)

                        # Extract outcomes and translate to selection objects
                        outcomes = market['outcomes']

                        for outcome in outcomes:
                            if not outcome.get('hidden'):
                                line = outcome.get('line')
                                selection = Selection(market_id=market_output.market_id, selection_id=outcome['providerOutcomeId'],
                                                      selection_name=outcome['label'], odds=outcome['oddsDecimal'], line=line)
                                selection_list.append(selection)

        return self.convert_odds_to_df(market_list, selection_list)
