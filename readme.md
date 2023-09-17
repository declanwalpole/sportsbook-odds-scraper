# Sportsbook Odds Scraper

## Overview

sportsbook-odds-scraper is a Python library that fetches the current odds being offered by various different sportsbooks in North America and Australia.

The user inputs a match URL from a supported sportsbook and the library returns all available markets and odds in a normalized pandas dataframe. There is also an option to write to CSV format.

Every visible market type and selection is queried, not just core markets. Suspended/hidden betting options are ignored.

Instead of parsing the html, data is requested through the sportsbooks' (undocumented) APIs. Accordingly, no SLA can be given as the sites may change without warning or block your traffic.

Can be run using the GUI app. Alternatively, the EventScraper class can be used as part of a larger analysis workflow.

### Supported Sportsbooks

- DraftKings
- BetMGM
- Caesars
- BetRivers/Sugarhouse
- PointsBet
- Superbook
- Bovada
- SportsBet (Aus)^
- TAB (Aus)
- Ladbrokes (Aus)

_NB: Sportsbooks may reject http requests based on your IP location. Use a VPN when trying to scrape odds from overseas._

_^SportsBet is very slow to scrape because you have to make a separate http request for each market grouping_

## Getting Started

### Clone the Repository

Assuming you have [Git](https://git-scm.com/) installed on your computer, open your terminal and run:

```bash
git clone https://github.com/declanwalpole/sportsbook-odds-scraper.git
```

### Navigate to the Directory

```bash
cd sportsbook-odds-scraper
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

# Usage

## Running the GUI

```powershell
python app.py
```

## Running the code

```python
# Import the EventScraper class
from event_scraper import EventScraper

# Create an instance of the EventScraper class
scraper = EventScraper()

# Set scraper input parameters
url = "www.example_sportsbook.com/event-123"
csv_outfile = "odds.csv"

# Scrape method returns a pandas dataframe of odds
odds_df = scraper.scrape(url, csv_outfile)
```
