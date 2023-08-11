from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up headless browsing with Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # Needed for some systems

# Initialize the browser
browser = webdriver.Chrome(options=chrome_options)

# Load a webpage
url = "https://sportsbook.caesars.com/us/co/bet/americanfootball/6c2530fe-4794-4ae5-8406-e81618cbc125/detroit-lions-at-kansas-city-chiefs"
browser.get(url)

# Execute JavaScript to interact with the webpage if needed
# Example: scroll down the page
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Access JSON API responses
json_response = browser.execute_script(
    'return fetch("https://www.williamhill.com/us/co/bet/api/v3/events/6c2530fe-4794-4ae5-8406-e81618cbc125").then(response => response.json());')
print(json_response)

# Clean up
browser.quit()
