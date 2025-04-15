from odds_dataclasses import Market, Selection
from sportsbook import Sportsbook


class PointsBet(Sportsbook):

    def get_name(self):
        return "PointsBet"

    def match_url_pattern(self, url):
        return "pointsbet.com.au" in url

    def extract_parameters_from_url(self, url):

        return {'event_id': self._extract_event_id_from_url(url),
                'jurisdiction': self._extract_jurisdiction_from_url(url)}

    def _extract_event_id_from_url(self, url):

        # Extract the digits between the last slash and the question mark (if any)

        last_slash_index = url.rfind('/')
        question_mark_index = url.find('?', last_slash_index)

        if question_mark_index != -1:
            event_id_str = url[last_slash_index + 1:question_mark_index]
        else:
            event_id_str = url[last_slash_index + 1:]

        return event_id_str

    def _extract_jurisdiction_from_url(self, url):
        return ""

    def concatenate_api_url(self, event_id, jurisdiction):
        return f'https://api.pointsbet.com/api/mes/v3/events/{event_id}'

    def parse_event_name(self, json_response, event_id=None):
        return json_response["name"]

    def parse_odds(self, json_response, event_id, jurisdiction):

        # Initialize lists to store markets and selections
        market_list = []
        selection_list = []

        # Iterating through markets
        for market in json_response['fixedOddsMarkets']:
            if market['isOpenForBetting']:
                market_name = market['eventName']
                market_id = market['key']
                market_group = market['groupName']
                market_list.append(
                    Market(market_id, market_group, market_name))
                # Iterating through outcomes
                for outcome in market['outcomes']:
                    if not outcome['isHidden'] and outcome['isOpenForBetting']:
                        outcome_name = outcome['name']
                        outcome_id = outcome['fixedMarketId']
                        odds = outcome['price']
                        line = outcome.get('points', None)
                        selection_list.append(
                            Selection(market_id, outcome_id, outcome_name, odds, line))

        return self.convert_odds_to_df(market_list, selection_list)
