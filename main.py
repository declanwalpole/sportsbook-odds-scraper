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
# "https://nj.superbook.com/sports/event/290697.1"
# "https://www.tab.com.au/sports/betting/AFL%20Football/competitions/AFL/matches/Essendon%20v%20Collingwood"
# "https://www.sportsbet.com.au/betting/basketball-aus-other/fiba-world-cup-men/finland-v-australia-7544081"
# "https://www.ladbrokes.com.au/sports/baseball/mlb/houston-astros-vs-boston-red-sox/ab06e453-8752-41a5-96b3-6ed70b31bdce"

url = "https://pa.betrivers.com/?page=sportsbook#event/1019666239"
csv_outfile = "odds.csv"

# Invoke the scrape method for the first scrape
odds_df = scraper.scrape(url, csv_outfile)
