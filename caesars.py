import re
import gzip
import json
import io
from seleniumwire import webdriver

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

# does not run


def request_event(url, event_id, sportsbook):
    state_abbrev = sportsbook[-2:]
    api_endpoint = f'https://api.americanwagering.com/regions/us/locations/{state_abbrev}/brands/czr/sb/v3/events/{event_id}'
    # print("API Endpoint:", api_endpoint)
    content = scrape_w_selenium(url, api_endpoint, event_id)
    return content

# does not run


def scrape_w_selenium(url, api_endpoint, event_id):
    # Set up headless browsing with Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")  # Needed for some systems
    chrome_options.add_argument("--ignore-certificate-errors")
    # Disables various web security features
    chrome_options.add_argument("--disable-proxy-certificate-handler")

    # Initialize the browser
    browser = webdriver.Chrome(options=chrome_options)

    # Load the webpage
    browser.get(url)

    # Find the relevant network request and extract its response
    for request in browser.requests:
        # api_endpoint == request.url:
        if "api.americanwagering.com/regions/us/locations/" in request.url and event_id in request.url:
            print(request.url)
            # Inside your loop that iterates over the requests:
            response_body_bytes = request.response.body
            #
            # # Check for gzip encoding
            if 'gzip' in request.response.headers.get('Content-Encoding', ''):
                buffer = io.BytesIO(response_body_bytes)
                with gzip.GzipFile(fileobj=buffer) as f:
                    response_body_str = f.read().decode('utf-8')
            else:
                response_body_str = response_body_bytes.decode('utf-8')

            if request.response.headers['Content-Type'].startswith('application/json'):
                response_body_json = json.loads(response_body_str)
                # Now you can work with response_body_json as a regular Python object
            else:
                print('Response is not JSON')
    browser.quit()
    return response_body_json
