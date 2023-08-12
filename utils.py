from datetime import datetime
import pandas as pd
import re

import draftkings as DK
import caesars as CZ
import bovada as BV
from odds_dataclasses import convert_market_list_to_df, convert_selection_list_to_df


def infer_sportsbook_of_url(url):

    if DK.match_url_pattern(url):
        return "DraftKings"
    elif BV.match_url_pattern(url):
        return "Bovada"
    elif CZ.match_url_pattern(url):
        return f"Caesars {CZ.get_state_abbrev(url).upper()}"

    raise ValueError("Invalid sportsbook URL")


def extract_event_id_from_url(url, sportsbook):

    if sportsbook == "DraftKings":
        return DK.extract_event_id_from_url(url)
    elif sportsbook == "Bovada":
        return BV.extract_event_id_from_url(url)
    elif sportsbook.startswith("Caesars"):
        return CZ.extract_event_id_from_url(url)

    raise NotImplementedError(f"Method not yet implemented for {sportsbook}")


def request_event(event_id, sportsbook):

    if sportsbook == "DraftKings":
        return DK.request_event(event_id)
    elif sportsbook == "Bovada":
        return BV.request_event(event_id)

    raise NotImplementedError(f"Method not yet implemented for {sportsbook}")


def get_event_name(json_response, sportsbook):
    if sportsbook == "DraftKings":
        return DK.get_event_name(json_response)
    elif sportsbook == "Bovada":
        return BV.get_event_name(json_response)

    raise NotImplementedError(f"Method not yet implemented for {sportsbook}")


def get_odds(json_response, sportsbook):
    if sportsbook == "DraftKings":
        return DK.get_odds(json_response)
    elif sportsbook == "Bovada":
        return BV.get_odds(json_response)

    else:
        raise NotImplementedError(
            f"Method not yet implemented for {sportsbook}")


def convert_odds_to_df(odds):
    if not odds[0] or not odds[1]:
        # Return an empty DataFrame if any of the input lists are empty.
        return pd.DataFrame()

    market_df = convert_market_list_to_df(odds[0])
    selection_df = convert_selection_list_to_df(odds[1])
    merged_df = market_df.merge(
        selection_df, on='market_id', how='inner').drop_duplicates()
    return merged_df


def preview_df_contents(df, num_rows=5):
    # Set display options for Pandas
    # Display all columns (None means unlimited)
    pd.set_option('display.max_columns', None)
    # Set the width of the display (None means auto-detect)
    pd.set_option('display.width', None)

    # Print the DataFrame nicely
    print(f"Here is a preview of the first {num_rows} rows of data:")
    print(df.head(num_rows).to_string(index=False))


def write_to_csv(df, csv_outfile):

    try:
        df.to_csv(csv_outfile, index=False)
        print(
            f"CSV successfully written to '{csv_outfile}'.")
    except Exception as err:
        print(f"Error occurred while writing to CSV: {err}")
