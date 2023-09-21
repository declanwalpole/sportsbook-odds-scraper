from datetime import datetime
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from sportsbook_factory import SportsbookFactory
from scraper_exception import ScraperException


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
        self.error_message = None
        self.timestamp_scrape_invoked = None
        self.timestamp_api_invoked = None
        self.timestamp_api_completed = None

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
            raise ScraperException(ScraperException.INVALID_URL_ERROR)

    def infer_api_endpoint(self):
        params = self.sportsbook.extract_parameters_from_url(self.url)
        self.event_id = params.get('event_id')
        self.jurisdiction = params.get('jurisdiction', "Not applicable")
        self.api_url = self.sportsbook.concatenate_api_url(
            self.event_id, self.jurisdiction)

    def get_odds(self):
        try:
            self.event_name = self.sportsbook.parse_event_name(
                self.json_response, self.event_id)
            self.odds_df = self.sportsbook.parse_odds(
                self.json_response, self.event_id, self.jurisdiction)
        except Exception:
            raise ScraperException(ScraperException.ODDS_PARSING_ERROR)

    def request_event_api(self, timeout=10, params=None):
        self.request_start_timestamp = datetime.now()
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }

        try:
            response = self.session.get(
                self.api_url,
                timeout=timeout,
                headers=headers,
                params=params if params else self.sportsbook.get_api_params())

            response.raise_for_status()
            self.json_response = response.json()
            self.request_end_timestamp = datetime.now()

        except requests.HTTPError as ex:
            self.request_end_timestamp = datetime.now()
            raise ScraperException(ScraperException.SERVER_ERROR)

        except requests.Timeout:
            self.request_end_timestamp = datetime.now()
            raise ScraperException(ScraperException.TIMEOUT_ERROR)

        except requests.ConnectionError:
            self.request_end_timestamp = datetime.now()
            raise ScraperException(ScraperException.CONNECTION_ERROR)

    def write_odds_to_csv(self, csv_outfile):
        self.csv_outfile = csv_outfile
        self.odds_df.to_csv(csv_outfile, index=False)

    def get_summary(self):
        if self.error_message:
            return {
                "URL": self.url,
                "Error": self.error_message,
                "Scrape Timestamp": self.timestamp_scrape_invoked,
                "Request Start Timestamp": self.request_start_timestamp,
                "Request End Timestamp": self.request_end_timestamp
            }
        else:
            summary = {
                "URL": self.url,
                "Scrape Timestamp": self.timestamp_scrape_invoked,
                "Request Start Timestamp": self.request_start_timestamp,
                "Request End Timestamp": self.request_end_timestamp,
                "Sportsbook": f"{self.sportsbook.get_name()} {self.jurisdiction if self.jurisdiction != 'Not applicable' else ''}",
                "Event": self.event_name,
                "Markets": self.odds_df['market_id'].nunique(),
                "Selections": len(self.odds_df)
            }
            if self.csv_outfile:
                summary["Filename"] = self.csv_outfile
            return summary

    def scrape(self, url, csv_outfile=None):
        self.timestamp_scrape_invoked = datetime.now()

        try:
            self.validate_url(url)
            self.sportsbook = SportsbookFactory.create(self.url)
            self.infer_api_endpoint()
            self.request_event_api()
            self.get_odds()
        except ScraperException as e:
            self.error_message = str(e)
            self.odds_df = None
            self.event_name = None
            return self

        if csv_outfile:
            try:
                self.write_odds_to_csv(csv_outfile)
            except (PermissionError, IOError):
                self.error_message = "Permission or IO Error while writing to CSV file"

        return self

    def retry_write_csv(self, csv_outfile):
        if not self.odds_df:
            self.error_message = "No odds data available for writing"
            return

        try:
            self.write_odds_to_csv(csv_outfile)
            self.error_message = None
        except (PermissionError, IOError):
            self.error_message = "Permission or IO Error while writing to CSV file"
