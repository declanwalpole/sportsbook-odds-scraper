import pandas as pd
from dataclasses import dataclass


@dataclass
class Market:
    market_id: str
    market_group: str
    market_name: str

    def __str__(self):
        return self.market_name


@dataclass
class Selection:
    market_id: str
    selection_id: str
    selection_name: str
    odds: float
    line: float or None

    def __str__(self):
        return self.selection_name


def convert_market_list_to_df(market_list):
    market_data = [{'market_id': market.market_id,
                    'market_group': market.market_group,
                    'market_name': market.market_name}
                   for market in market_list]
    market_df = pd.DataFrame(market_data)
    return market_df


def convert_selection_list_to_df(selection_list):
    selection_data = [{'market_id': selection.market_id,
                       'selection_id': selection.selection_id,
                       'selection_name': selection.selection_name,
                       'odds': selection.odds,
                       'line': selection.line}
                      for selection in selection_list]
    selection_df = pd.DataFrame(selection_data)
    return selection_df
