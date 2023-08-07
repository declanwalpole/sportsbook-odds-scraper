from datetime import datetime
import pandas as pd

from draftkings_api import request_draftkings_event, parse_draftkings_json, convert_draftkings_info_to_df


def extract_event_id_from_url(url):

    # Extract the digits between the last slash and the question mark (if any)

    last_slash_index = url.rfind('/')
    question_mark_index = url.find('?', last_slash_index)

    if question_mark_index != -1:
        event_id_str = url[last_slash_index + 1:question_mark_index]
    else:
        event_id_str = url[last_slash_index + 1:]

    return event_id_str


def scrape_DK_event(eventId):

    json_response = request_draftkings_event(eventId)

    (eventId, eventName, market_list,
     selection_list) = parse_draftkings_json(json_response)

    merged_df = convert_draftkings_info_to_df(market_list, selection_list)

    return (eventId, eventName, merged_df)


def preview_df_contents(df, num_rows=5):
    # Set display options for Pandas
    # Display all columns (None means unlimited)
    pd.set_option('display.max_columns', None)
    # Set the width of the display (None means auto-detect)
    pd.set_option('display.width', None)

    # Print the DataFrame nicely
    print(f"Here are the first {num_rows} rows of data:")
    print(df.head(num_rows).to_string(index=False))


def write_to_csv(eventId, eventName, df):

    timestamp_suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    outfilename = f"{eventId} {eventName} {timestamp_suffix}.csv"
    print(f"Writing to {outfilename}")

    try:
        df.to_csv(outfilename, index=False)
        print(
            f"CSV successfully written to '{outfilename}'.")
    except Exception as err:
        print(f"Error occurred while writing to CSV: {err}")
