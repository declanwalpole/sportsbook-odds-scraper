from urllib.parse import urlparse
from utils import infer_sportsbook_of_url, extract_event_id_from_url, request_event, get_event_name, get_odds, convert_odds_to_df, preview_df_contents, write_to_csv


def scrape_event(url, csv_outfile=None, preview_head=None):

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL provided.")
        return None

    print(f"Scraping {url}...")

    try:
        sportsbook = infer_sportsbook_of_url(url)
        event_id = extract_event_id_from_url(url, sportsbook)
        json_response = request_event(event_id, sportsbook)
        event_name = get_event_name(json_response, sportsbook, event_id)
        odds_df = convert_odds_to_df(get_odds(json_response, sportsbook))
    except Exception as error:
        print(f"An error occurred during scraping: {error}")
        return None

    if preview_head:
        preview_df_contents(odds_df, preview_head)

    if csv_outfile:
        write_to_csv(odds_df, csv_outfile)

    print(
        f"Scrape completed.\nSportsbook: {sportsbook}\nEvent: {event_name} ({event_id})")

    return odds_df
