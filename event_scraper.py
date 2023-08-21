from urllib.parse import urlparse

from sportsbook_factory import SportsbookFactory


class EventScraper():

    def __init__(self):
        self.url = None
        self.csv_outfile = None
        self.sportsbook = None
        self.event_id = None
        self.jurisdiction = None
        self.json_response = None
        self.event_name = None
        self.odds_df = None

    def validate_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            self.url = url
        else:
            raise ValueError("Invalid URL")

    def get_odds(self):
        self.sportsbook = SportsbookFactory.create(self.url)
        params = self.sportsbook.extract_parameters_from_url(self.url)
        self.event_id = params.get('event_id')
        self.jurisdiction = params.get('jurisdiction', "Not applicable")
        self.json_response = self.sportsbook.request_event(
            self.event_id, self.jurisdiction)
        self.event_name = self.sportsbook.parse_event_name(
            self.json_response, self.event_id)
        self.odds_df = self.sportsbook.parse_odds(
            self.json_response, self.event_id, self.jurisdiction)

        return

    def write_odds_to_csv(self, csv_outfile):
        self.csv_outfile = csv_outfile
        self.odds_df.to_csv(csv_outfile, index=False)

    def print_summary(self):
        print(
            f"URL: {self.url}"
            f"\nSportsbook: {self.sportsbook.get_name()} {self.jurisdiction if self.jurisdiction!='Not applicable' else ''}"
            f"\nEvent: {self.event_name}"
            f"\nMarkets: {self.odds_df['market_id'].nunique()}"
            f"\nSelections: {len(self.odds_df)}"
        )
        if self.csv_outfile:
            print(
                f"Filename: {self.csv_outfile}"
            )

    def scrape(self, url, csv_outfile=None, verbose=True):

        self.validate_url(url)

        try:
            self.get_odds()
        except Exception as error:
            print(f"An error occurred during scraping: {error}")
            return None

        if (csv_outfile):
            self.write_odds_to_csv(csv_outfile)

        if (verbose):
            self.print_summary()

        return self.odds_df
