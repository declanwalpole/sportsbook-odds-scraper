# Import the EventScraper class
from event_scraper import EventScraper

# Create an instance of the EventScraper class
scraper = EventScraper()

# "https://sportsbook.draftkings.com/event/det-lions-%40-kc-chiefs/28867533"
# "https://sports.az.betmgm.com/en/sports/events/arizona-diamondbacks-at-los-angeles-dodgers-14545130"
# "https://co.betrivers.com/?page=sportsbook#event/live/1020060483"
# "https://www.bovada.lv/sports/football/college-football/nc-state-connecticut-202308311930"
# "https://sportsbook.caesars.com/us/co/bet/baseball/15bd01e4-8368-4df0-8bcf-61b222df30ee/arizona-diamondbacks-at-los-angeles-dodgers"
# "https://la.pointsbet.com/sports/baseball/MLB/283535"
# "https://nj.superbook.com/sports/event/290697.1"
# "https://www.tab.com.au/sports/betting/Soccer/competitions/UEFA%20Europa%20League/matches/FK%20Qarabag%20v%20Olimpija"
# "https://www.sportsbet.com.au/betting/basketball-aus-other/fiba-world-cup-men/angola-v-china-7600223"
# "https://www.ladbrokes.com.au/sports/rugby-league/nrl/brisbane-broncos-vs-melbourne-storm/bcdbdfbc-98d6-45e3-84a4-66a2b88e69fc"

url = "https://pointsbet.com.au/sports/rugby-league/NRL/2245825"

# Invoke the scrape method
scraper.scrape(url)

# summary of completed scrape
print(scraper.get_summary())

# preview the pandas df of scraped odds
print(scraper.odds_df.head())
