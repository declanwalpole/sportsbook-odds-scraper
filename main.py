# Import the EventScraper class
from event_scraper import EventScraper

# Create an instance of the EventScraper class
scraper = EventScraper()

# "https://sportsbook.draftkings.com/event/det-lions-%40-kc-chiefs/28867533"
# "https://sports.co.betmgm.com/en/sports/events/philadelphia-phillies-at-washington-nationals-ne-14541429"
# "https://pa.betrivers.com/?page=sportsbook#event/1020034569"
# "https://www.bovada.lv/sports/soccer/south-america/argentina/copa-de-la-liga-profesional/huracan-banfield-202308211700"
# "https://sportsbook.caesars.com/us/co/bet/baseball/420f7c5a-95d3-46ae-a523-7b7c86b8e563/chicago-cubs-at-detroit-tigers"
# "https://oh.pointsbet.com/sports/tennis/WTA-Cleveland/168426"

url = "https://nj.superbook.com/sports/event/290697.1"
csv_outfile = "odds.csv"

# Invoke the scrape method for the first scrape
odds_df = scraper.scrape(url, csv_outfile)
