from urllib.parse import urlparse

from utils import convert_odds_to_df, write_to_csv
from sportsbook_factory import SportsbookFactory


def scrape_event(url, csv_outfile=None):

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL provided.")
        return None

    print(f"Scraping {url}...")

    try:
        sportsbook = SportsbookFactory.create(url)
        params = sportsbook.extract_parameters_from_url(url)
        json_response = sportsbook.request_event(params)
        event_name = sportsbook.parse_event_name(json_response)
        odds_df = convert_odds_to_df(
            sportsbook.parse_odds(json_response, params))
    except Exception as error:
        print(f"An error occurred during scraping: {error}")
        return None

    if csv_outfile:
        write_to_csv(odds_df, csv_outfile)

    print(
        f"Scrape completed.\n"
        f"Sportsbook: {sportsbook.get_name()}\n"
        f"Event: {event_name} ({params['event_id']})\n"
        f"Markets: {odds_df['market_id'].nunique()}\n"
        f"Selection: {len(odds_df)}"
    )

    return odds_df
