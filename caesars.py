import requests
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from odds_dataclasses import Market, Selection


def match_url_pattern(url):
    pattern = r"https://sportsbook\.caesars\.com/us/(\w+)/bet"
    return re.match(pattern, url)


def get_state_abbrev(url):
    return match_url_pattern(url).group(1)


def extract_event_id_from_url(url):

    pattern = r"/([a-f0-9-]+)/[^/]*$"
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None


def request_event(url, event_id, sportsbook):
    state_abbrev = sportsbook[-2:]
    api_endpoint = f'https://api.americanwagering.com/regions/us/locations/{state_abbrev}/brands/czr/sb/v3/events/{event_id}'

    content = scrape_w_selenium(url, api_endpoint)
    return content


def scrape_w_selenium(url, api_endpoint):
    # Set up headless browsing with Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Needed for some systems
    chrome_options.add_argument("--ignore-certificate-errors")

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Initialize the browser
    browser = webdriver.Chrome(options=chrome_options,
                               desired_capabilities=desired_capabilities)

    # Load the webpage
    browser.get(url)
    # Access the network logs captured by the browser
    network_logs = browser.get_log("performance")

    # Find the relevant network request and extract its response
    for log_entry in network_logs:
        try:
            message = json.loads(log_entry["message"])["message"]
            if "Network.response" in message["method"]:
                response = message.get("params", {}).get("response", {})
                response_url = response.get("url", "")
                if "api.americanwagering.com" in response_url and "/events/6c2530fe-4794-4ae5-8406-e81618cbc125" in response_url:
                    print(response_url)
                    print(message["params"]["response"])
                    body = browser.execute_cdp_cmd('Network.getResponseBody', {
                        'requestId': message["params"]["requestId"]})
                    print(body)
        except (KeyError, json.JSONDecodeError):
            pass
            # response_url = message["params"]["request"]["url"]
            # if api_endpoint in response_url:
            #     api_response = message["params"]["response"]

    # Print or return the API response
    # if api_response:
    #     print(json.dumps(api_response, indent=2))
        # You can return the api_response if needed

    # Clean up
    browser.quit()
    # return json_response


def get_event_name(json_response):
    return json_response['event']["name"]


def get_odds(json_content):

    # Initialize lists to store markets and selections
    market_list = []
    selection_list = []

    # Process each category and its offers
    for category in json_content['eventCategories']:
        for market_grouping in category['componentizedOffers']:

            market_grouping_name = market_grouping['subcategoryName']
            markets = market_grouping['offers'][0]

            for market in markets:
                if not market['isSuspended'] and market['isOpen']:
                    # Translate offer to market object
                    market_output = translate_DK_to_market_dict(
                        market, market_grouping_name)
                    market_list.append(market_output)

                    # Extract outcomes and translate to selection objects
                    outcomes = market['outcomes']

                    for outcome in outcomes:
                        if not outcome.get('hidden'):
                            selection = translate_DK_to_selection_dict(
                                outcome, market_output.market_id)
                            selection_list.append(selection)

    return (market_list, selection_list)


def translate_DK_to_market_dict(DK_dict, subcategoryName):
    dict_for_translation = {
        'market_id': DK_dict['providerOfferId'],
        'market_group': subcategoryName,
        'market_name': DK_dict['label']
    }
    return Market(**dict_for_translation)


def translate_DK_to_selection_dict(DK_dict, market_id):
    if "line" in DK_dict:
        line = DK_dict['line']
    else:
        line = None

    dict_for_translation = {
        'market_id': market_id,
        'selection_id': DK_dict['providerOutcomeId'],
        'selection_name': DK_dict['label'],
        'odds': DK_dict['oddsDecimal'],
        'line': line,
    }
    return Selection(**dict_for_translation)
