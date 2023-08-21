# Import the EventScraper class
from event_scraper import EventScraper

# Create an instance of the EventScraper class
scraper = EventScraper()

# Define the URL and optional CSV output file for the first scrape
url = "https://sportsbook.draftkings.com/event/det-lions-%40-kc-chiefs/28867533"
csv_outfile = "odds.csv"

# Invoke the scrape method for the first scrape
odds_df = scraper.scrape(url, csv_outfile)
