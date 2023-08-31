import pandas as pd
from odds_dataclasses import convert_market_list_to_df, convert_selection_list_to_df


class Sportsbook:
    def get_name(self):
        raise NotImplementedError

    def match_url_pattern(self, url):
        raise NotImplementedError

    def extract_parameters_from_url(self, url):
        raise NotImplementedError

    def concatenate_api_url(self, event_id, jurisdiction=None):
        raise NotImplementedError

    def parse_event_name(self, json_response, event_id=None):
        raise NotImplementedError

    def parse_odds(self, json_response, event_id, jurisdiction=None):
        raise NotImplementedError

    def convert_odds_to_df(self, market_list, selection_list):
        if market_list and selection_list:
            market_df = convert_market_list_to_df(market_list)
            selection_df = convert_selection_list_to_df(selection_list)
            merged_df = market_df.merge(
                selection_df, on='market_id', how='inner').drop_duplicates()
            return merged_df
        else:
            return pd.DataFrame()

    def get_api_params(self):
        return None
