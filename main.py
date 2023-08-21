# Import the EventScraper class
from event_scraper import EventScraper

# Create an instance of the EventScraper class
scraper = EventScraper()

# Define the URL and optional CSV output file for the first scrape
# "https://sportsbook.draftkings.com/event/det-lions-%40-kc-chiefs/28867533"
# "https://sports.co.betmgm.com/en/sports/events/philadelphia-phillies-at-washington-nationals-ne-14541429"
url = "https://pa.betrivers.com/?page=sportsbook#event/1020034569"
csv_outfile = "odds.csv"

# Invoke the scrape method for the first scrape
odds_df = scraper.scrape(url, csv_outfile)
