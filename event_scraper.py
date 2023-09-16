from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from sportsbook_factory import SportsbookFactory


class EventScraper():

    def __init__(self):
        self.url = None
        self.csv_outfile = None
        self.sportsbook = None
        self.event_id = None
        self.jurisdiction = None
        self.api_url = None
        self.json_response = None
        self.event_name = None
        self.odds_df = None

        # Configure the session for retries
        self.session = requests.Session()
        retry_strategy = Retry(total=3)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def validate_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            self.url = url
        else:
            raise ValueError("Invalid URL input")

    def infer_api_endpoint(self):
        params = self.sportsbook.extract_parameters_from_url(self.url)
        self.event_id = params.get('event_id')
        self.jurisdiction = params.get('jurisdiction', "Not applicable")
        self.api_url = self.sportsbook.concatenate_api_url(
            self.event_id, self.jurisdiction)

    def get_odds(self):
        self.event_name = self.sportsbook.parse_event_name(
            self.json_response, self.event_id)
        self.odds_df = self.sportsbook.parse_odds(
            self.json_response, self.event_id, self.jurisdiction)

    def request_event_api(self, timeout=10, params=None):
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }

        try:
            response = self.session.get(
                self.api_url, timeout=timeout, headers=headers, params=params)
            response.raise_for_status()
            self.json_response = response.json()
        except requests.RequestException as ex:
            print(f"An error occurred when requesting the api: {ex}")

    def write_odds_to_csv(self, csv_outfile):
        self.csv_outfile = csv_outfile
        self.odds_df.to_csv(csv_outfile, index=False)

    def get_summary(self):
        summary = {
            "URL": self.url,
            "Sportsbook": f"{self.sportsbook.get_name()} {self.jurisdiction if self.jurisdiction != 'Not applicable' else ''}",
            "Event": self.event_name,
            "Markets": self.odds_df['market_id'].nunique(),
            "Selections": len(self.odds_df),
        }
        if self.csv_outfile:
            summary["Filename"] = self.csv_outfile
        return summary

    def print_summary(self):
        summary = self.get_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")

    def scrape(self, url, csv_outfile=None, verbose=True):

        self.validate_url(url)
        self.sportsbook = SportsbookFactory.create(self.url)
        self.infer_api_endpoint()
        self.request_event_api(params=self.sportsbook.get_api_params())
        self.get_odds()

        if (csv_outfile):
            self.write_odds_to_csv(csv_outfile)

        if (verbose):
            self.print_summary()

        return self
